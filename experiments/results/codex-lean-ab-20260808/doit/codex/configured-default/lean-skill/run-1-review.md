# Repository Review

## 1. **DATA-INTEGRITY — Incremental DB updates can erase existing task metadata**

**Files:** `doit/dependency.py:183` (`DbmDB.set`), `doit/dependency.py:309` (`SqliteDB.set`)

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

After reopening an existing database, calling `set()` before `get()` initializes an empty mapping instead of loading the task’s persisted record. At `dump()`, that empty-derived mapping replaces the record, silently deleting sibling values such as dependency hashes, task results, and ignore status.

**Suggested improvement:** On a cache miss, load the existing task data before changing one key:

```python
if task_id not in self._cache:
    self._cache[task_id] = self._get_task_data(task_id)
```

Apply equivalent behavior to `DbmDB`, and add reopen-then-update tests for every backend.

**Why it matters:** The backends do not honor their advertised key/value update semantics and can silently corrupt dependency state across invocations.

---

## 2. **NO-MUTARGS — Task construction mutates the caller’s `uptodate` list**

**File:** `doit/task.py:230-237` (`Task.__init__`)

**Problematic code:**

```python
uptodate = uptodate if uptodate else []

self.getargs = getargs
if self.getargs:
    uptodate.extend(self._init_getargs())
```

A non-empty caller-owned list is retained and extended in place. Reusing the task definition or constructing another `Task` from it accumulates generated checks and changes external configuration unexpectedly.

**Suggested improvement:** Always make a local copy before extending it:

```python
uptodate = list(uptodate or ())
```

Add a test asserting that the supplied list is unchanged after construction.

**Why it matters:** Hidden mutation makes task definitions non-repeatable and can produce duplicate checks when an API consumer loads tasks multiple times in one process.

---

## 3. **NO-MUTARGS — Command execution mutates a supplied environment mapping**

**File:** `doit/action.py:207-215` (`CmdAction.execute`)

**Problematic code:**

```python
subprocess_pkwargs = self.pkwargs.copy()
env = subprocess_pkwargs['env']
...
if self.buffering:
    if not env:
        env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
```

Only the outer keyword dictionary is copied. A non-empty `env` mapping remains caller-owned and is modified by adding or replacing `PYTHONUNBUFFERED`.

**Suggested improvement:** Copy the environment mapping before changing it:

```python
env = subprocess_pkwargs.pop('env', None)
if env is not None:
    env = env.copy()
if self.buffering:
    env = os.environ.copy() if env is None else env
    env['PYTHONUNBUFFERED'] = '1'
```

**Why it matters:** Reusing the environment elsewhere can unexpectedly change subsequent subprocess behavior, especially in long-running applications embedding doit.

---

## 4. **NO-GLOBAL-MUT — Loading a dodo file can return the wrong cached module**

**File:** `doit/loader.py:76-96` (`get_module`)

**Problematic code:**

```python
sys.path.insert(0, base_path)
...
return importlib.import_module(os.path.splitext(file_name)[0])
```

The loader imports solely by basename. If two different directories contain identically named dodo files, the second call can return the first module from `sys.modules`. The inserted `sys.path` entries also accumulate indefinitely.

**Suggested improvement:** Load the exact file under a unique module key using `importlib.util.spec_from_file_location()` and `module_from_spec()`. Scope any temporary path insertion with `try/finally`.

**Why it matters:** Embedders, test suites, and tooling that load multiple projects in one interpreter can execute tasks from the wrong project.

---

## 5. **SAFE-DEFAULT — JSON dependency persistence is non-atomic**

**File:** `doit/dependency.py:87-93` (`JsonDB.dump`)

**Problematic code:**

```python
db_file = open(self.name, 'w')
db_file.write(self.codec.encode(self._db))
```

Opening with `"w"` truncates the valid database before encoding and writing have completed. Serialization errors, disk exhaustion, interruption, or process termination can leave an empty or partial dependency database. Additionally, if `open()` fails, `finally` attempts to close an unassigned `db_file`, masking the original exception.

**Suggested improvement:** Encode first, write to a temporary file in the same directory, flush and optionally `fsync()`, then atomically replace the destination with `os.replace()`. Use context managers for file ownership.

**Why it matters:** A failed persistence operation can destroy previously valid dependency history and cause unnecessary rebuilds or lost saved task values.

---

## 6. **EXCEPT-HIER — Invalid TOML plugin types are validated with `assert`**

**File:** `doit/doit_cmd.py:133-136` (`DoitConfig.load_config_toml`)

**Problematic code:**

```python
for plugin_type, plugins in doit_toml.pop('plugins', {}).items():
    assert plugin_type in self.PLUGIN_TYPES
    toml_config[plugin_type.upper()] = plugins
```

Assertions are disabled under `python -O`. Without them, unsupported plugin sections flow into configuration silently; with them enabled, users receive an uncaught `AssertionError` instead of a configuration-specific diagnostic.

**Suggested improvement:** Perform explicit validation and raise `InvalidCommand`, `ValueError`, or a dedicated configuration exception containing the invalid name and supported plugin types.

**Why it matters:** Behavior changes with interpreter optimization settings, and malformed user configuration is reported as an internal programming failure.

---

## 7. **EXPLICIT-BOOL — Empty command-line arguments cause an uncaught indexing error**

**File:** `doit/doit_cmd.py:208-221` (`DoitMain.process_args`)

**Problematic code:**

```python
for arg in cmd_args:
    if (arg[0] != '-') and ('=' in arg):
```

An empty argument, possible through the programmatic API or a quoted shell argument, raises `IndexError`. This occurs before the command execution exception handling in `DoitMain.run`.

**Suggested improvement:** Avoid indexing and express the condition safely:

```python
if arg and not arg.startswith('-') and '=' in arg:
```

Alternatively, reject empty arguments with a deliberate `CmdParseError`.

**Why it matters:** Benign malformed input bypasses normal CLI error reporting and crashes API callers unexpectedly.
