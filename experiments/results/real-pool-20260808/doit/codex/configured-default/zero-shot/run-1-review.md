# Repository Review

## 1. `STATE-CLOBBER` — Existing dependency records are overwritten

**Location:** `doit/dependency.py:183` (`DbmDB.set`), `doit/dependency.py:309` (`SqliteDB.set`)

### Problematic code

```python
def set(self, task_id, dependency, value):
    if task_id not in self._db:
        self._db[task_id] = {}
    self._db[task_id][dependency] = value
```

```python
def set(self, task_id, dependency, value):
    if task_id not in self._cache:
        self._cache[task_id] = {}
    self._cache[task_id][dependency] = value
```

If a task already exists in persistent storage but has not yet been read into the in-memory cache, `set()` starts with an empty dictionary. On `dump()`, that dictionary replaces the complete stored record, silently discarding other dependency states, results, and saved values.

### Improved code

```python
# DbmDB
def set(self, task_id, dependency, value):
    if task_id not in self._db:
        try:
            encoded = self._dbm[task_id]
        except KeyError:
            self._db[task_id] = {}
        else:
            self._db[task_id] = self.codec.decode(encoded.decode("utf-8"))

    self._db[task_id][dependency] = value
    self.dirty.add(task_id)
```

```python
# SqliteDB
def set(self, task_id, dependency, value):
    if task_id not in self._cache:
        self._cache[task_id] = self._get_task_data(task_id)

    self._cache[task_id][dependency] = value
    self._dirty.add(task_id)
```

### Why it matters

This is a data-integrity bug. Updating one field can erase unrelated persisted state and cause unnecessary rebuilds, lost task values, or incorrect dependency decisions on subsequent runs.

---

## 2. `STREAM-TRAP` — Argument preparation can permanently redirect standard streams

**Location:** `doit/action.py:429`, especially `PythonAction.execute` lines 442–480

### Problematic code

```python
sys.stdout = out_writer
sys.stderr = err_writer

kwargs = self._prepare_kwargs()

try:
    returned_value = self.py_callable(*self.args, **kwargs)
except Exception as exception:
    return TaskError("PythonAction Error", exception)
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
```

`_prepare_kwargs()` executes after replacing `sys.stdout` and `sys.stderr`, but before entering the protected `try/finally`. If signature binding or reserved-argument validation raises, the streams are never restored.

### Improved code

```python
try:
    kwargs = self._prepare_kwargs()
    returned_value = self.py_callable(*self.args, **kwargs)
except Exception as exception:
    if self.pm_pdb:  # pragma: no cover
        debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
        debugger.reset()
        debugger.interaction(None, sys.exc_info()[2])
    return TaskError("PythonAction Error", exception)
finally:
    if capture_io:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        self.out = output.getvalue()
        self.err = errput.getvalue()
    else:
        if out:
            sys.stdout = old_stdout
        if err:
            sys.stderr = old_stderr
```

Alternatively, prepare the arguments before redirecting the streams.

### Why it matters

A single invalid action can corrupt process-global I/O for the rest of the run. Later diagnostics, reporters, and tasks may write into stale buffers or apparently produce no output.

---

## 3. `ENV-LEAK` — Command execution mutates the caller’s environment dictionary

**Location:** `doit/action.py:206–215`, `CmdAction.execute`

### Problematic code

```python
env = None
if 'env' in subprocess_pkwargs:
    env = subprocess_pkwargs['env']
    del subprocess_pkwargs['env']

if self.buffering:
    if not env:
        env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
```

When the caller supplies a non-empty `env` dictionary, adding `PYTHONUNBUFFERED` modifies that original dictionary. An explicitly supplied empty environment is also treated as absent and replaced with the full parent environment.

### Improved code

```python
env = subprocess_pkwargs.pop("env", None)

if self.buffering:
    env = os.environ.copy() if env is None else env.copy()
    env["PYTHONUNBUFFERED"] = "1"
```

### Why it matters

Action execution should not unexpectedly change reusable configuration owned by the caller. Treating `{}` as missing also violates subprocess semantics and can unintentionally expose the parent process environment to a child.

---

## 4. `DEVNULL-LEAK` — Suppressed-output actions leak file descriptors

**Location:** `doit/action.py:217–235`, `CmdAction.execute`

### Problematic code

```python
else:  # None
    p_out = p_err = open(os.devnull, "w")

process = subprocess.Popen(
    action,
    shell=self.shell,
    stdout=p_out,
    stderr=p_err,
    env=env,
    **subprocess_pkwargs
)
```

The opened `/dev/null` stream is never closed. Repeated actions with `capture_io is None` accumulate descriptors until garbage collection or process termination.

### Improved code

```python
devnull = None
try:
    if capture_io:
        p_out = p_err = subprocess.PIPE
    elif capture_io is False:
        p_out, p_err = out, err
    else:
        devnull = open(os.devnull, "w")
        p_out = p_err = devnull

    process = subprocess.Popen(
        action,
        shell=self.shell,
        stdout=p_out,
        stderr=p_err,
        env=env,
        **subprocess_pkwargs,
    )
finally:
    if devnull is not None:
        devnull.close()
```

### Why it matters

Long-running builds or services can eventually hit the operating system’s open-file limit, producing failures far removed from the source of the leak.

---

## 5. `CLOSE-MASK` — JSON database write failures can be hidden by `UnboundLocalError`

**Location:** `doit/dependency.py:87–93`, `JsonDB.dump`

### Problematic code

```python
def dump(self):
    try:
        db_file = open(self.name, 'w')
        db_file.write(self.codec.encode(self._db))
    finally:
        db_file.close()
```

If `open()` fails, `db_file` was never assigned. The `finally` block then raises `UnboundLocalError`, masking the useful permission, path, or filesystem exception.

### Improved code

```python
def dump(self):
    encoded = self.codec.encode(self._db)
    with open(self.name, "w", encoding="utf-8") as db_file:
        db_file.write(encoded)
```

For stronger crash safety, write to a temporary file in the same directory and replace the database atomically.

### Why it matters

Masking the original exception makes operational failures difficult to diagnose. Encoding before opening also avoids truncating the existing database if serialization fails.

---

## 6. `MODULE-COLLIDE` — Dodo files are imported by basename rather than path

**Location:** `doit/loader.py:76–96`, `get_module`

### Problematic code

```python
base_path, file_name = os.path.split(dodo_path)
sys.path.insert(0, base_path)
os.chdir(full_cwd)

return importlib.import_module(os.path.splitext(file_name)[0])
```

Python caches imports by module name. Loading `/project-a/dodo.py` and then `/project-b/dodo.py` in the same process can return the already cached first module because both are named `dodo`.

### Improved code

```python
import hashlib
import importlib.util

resolved_path = os.path.realpath(dodo_path)
suffix = hashlib.sha256(resolved_path.encode("utf-8")).hexdigest()
module_name = f"_doit_dodo_{suffix}"

spec = importlib.util.spec_from_file_location(module_name, resolved_path)
if spec is None or spec.loader is None:
    raise InvalidDodoFile(f"Could not load dodo file {resolved_path!r}")

module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
return module
```

The associated `sys.path` and working-directory changes should also be scoped or explicitly restored when used through an embedded API.

### Why it matters

Programmatic users, test suites, and repeated invocations can execute tasks from the wrong project. The failure is order-dependent and therefore particularly difficult to reproduce.

---

## 7. `EMPTY-ARG` — Empty arguments cause an indexing failure

**Location:** `doit/loader.py:190–195`, `load_tasks`

### Problematic code

```python
arg_pos = {}
for index, term in enumerate(args):
    if term[0] != '-':
        arg_pos[term] = index
```

An empty string in `args` raises `IndexError` at `term[0]`.

### Improved code

```python
arg_pos = {
    term: index
    for index, term in enumerate(args)
    if term and not term.startswith("-")
}
```

If empty task names are invalid input, rejecting them with a domain-specific parsing exception would be even clearer.

### Why it matters

Public and programmatic callers should receive a meaningful command-line error rather than an internal traceback for malformed input.
