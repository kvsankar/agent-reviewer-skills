## Findings

### 1. `CACHE-COLLISION` — Dodo modules can resolve to the wrong file

**Location:** `doit/loader.py:76-96`, `get_module`

**Problematic code:**

```python
base_path, file_name = os.path.split(dodo_path)
sys.path.insert(0, base_path)
...
return importlib.import_module(os.path.splitext(file_name)[0])
```

Loading is based only on the filename-derived module name. If two directories contain `dodo.py`, the second call can return the first module from `sys.modules`. Repeated calls also leave duplicate paths in `sys.path`.

**Suggested improvement:** Load the exact path with `importlib.util.spec_from_file_location`, using a unique module name derived from the absolute path. Limit or restore temporary `sys.path` changes where possible.

**Why it matters:** Long-running processes, embedded API users, and tests can silently execute tasks from the wrong project.

---

### 2. `STATE-CLOBBER` — Incremental database writes discard existing task data

**Locations:**

- `doit/dependency.py:183-188`, `DbmDB.set`
- `doit/dependency.py:309-314`, `SqliteDB.set`

**Problematic code:**

```python
if task_id not in self._db:
    self._db[task_id] = {}
self._db[task_id][dependency] = value
```

```python
if task_id not in self._cache:
    self._cache[task_id] = {}
self._cache[task_id][dependency] = value
```

When a task already exists in persistent storage but has not been read into the in-memory cache, `set()` starts from an empty dictionary. `dump()` then replaces the complete record. For example, `Dependency.ignore()` can erase saved values, result hashes, and dependency states in the DBM and SQLite backends. `JsonDB` does not have this inconsistency because it eagerly loads the full database.

**Suggested improvement:** On the first `set()` for a task, load its existing record from the backend before updating one field. Add cross-backend contract tests covering `set()` on an existing, uncached record.

**Why it matters:** Backend choice changes behavior, and metadata can be silently lost after commands intended to update only one property.

---

### 3. `SPAWN-ESCAPE` — Process-start failures bypass normal task failure handling

**Location:** `doit/action.py:227-235`, `CmdAction.execute`

**Problematic code:**

```python
process = subprocess.Popen(
    action,
    shell=self.shell,
    stdout=p_out,
    stderr=p_err,
    env=env,
    **subprocess_pkwargs)
```

Only command expansion is protected by the earlier `try` block. Errors from `Popen`, such as a missing executable for a list action, invalid working directory, or permission failure, escape `CmdAction.execute` instead of becoming a `TaskError`.

**Suggested improvement:** Catch expected `OSError`/`ValueError` exceptions around `Popen` and return a `TaskError` containing the command and original exception. Preserve interrupts and other control-flow exceptions.

**Why it matters:** A routine task failure becomes a framework traceback, bypassing reporter formatting and `--continue` behavior.

---

### 4. `IMPORT-MASK` — Plugin import errors are reported as missing plugins

**Location:** `doit/plugin.py:43-50`, `PluginEntry.load`

**Problematic code:**

```python
try:
    module = importlib.import_module(module_name)
except ImportError:
    raise Exception(
        'Plugin {} module `{}` not found.'.format(self.category, module_name))
```

This catches every `ImportError` raised while executing the plugin module, including imports of missing transitive dependencies and deliberate imports inside plugin code. The resulting message incorrectly claims that the plugin module itself was not found and discards the original context.

**Suggested improvement:** Catch `ModuleNotFoundError` and only translate it when `exception.name == module_name`. Otherwise re-raise with exception chaining:

```python
raise PluginError(...) from exception
```

**Why it matters:** Valid plugin installations with missing dependencies become unnecessarily difficult to diagnose.

---

### 5. `TRUNCATE-FIRST` — JSON dependency persistence is not crash-safe

**Location:** `doit/dependency.py:87-93`, `JsonDB.dump`

**Problematic code:**

```python
db_file = open(self.name, 'w')
db_file.write(self.codec.encode(self._db))
```

Opening with `"w"` truncates the existing database before encoding and writing completes. Serialization errors, disk exhaustion, interruption, or process termination can leave an empty or partial dependency database.

**Suggested improvement:** Encode first, write to a temporary file in the same directory, flush and optionally `fsync`, then atomically replace the destination with `os.replace`.

**Why it matters:** An interrupted run can corrupt all cached dependency state, forcing unnecessary rebuilds and manual cleanup.
