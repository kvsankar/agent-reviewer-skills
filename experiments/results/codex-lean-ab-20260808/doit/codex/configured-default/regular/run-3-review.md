## Findings

### 1. `KW-CLOBBER` — Explicit action arguments are silently overwritten

- **File:** `doit/action.py:60-92`
- **Problematic code:**

```python
kwargs = kwargs.copy()
bound_args = func_sig.bind_partial(*args)
...
if key not in bound_args.arguments:
    kwargs[key] = meta_args[key]()
...
if key not in bound_args.arguments:
    kwargs[key] = opt_args[key]
```

`bind_partial()` receives only positional arguments, so an explicitly supplied keyword such as `targets=...` or a task-option keyword is absent from `bound_args.arguments` and gets overwritten by doit-generated metadata.

- **Suggested improvement:** Bind both sources with `func_sig.bind_partial(*args, **kwargs)`, or require that the key is absent from both `bound_args.arguments` and `kwargs` before injecting it.
- **Why it matters:** Callers cannot reliably override keyword arguments, contradicting the method’s own “have not been passed … as keyword arg” contract and potentially executing actions with unintended inputs.

### 2. `ENV-LEAK` — Buffered commands mutate the caller’s environment dictionary

- **File:** `doit/action.py:206-215`
- **Problematic code:**

```python
if 'env' in subprocess_pkwargs:
    env = subprocess_pkwargs['env']
...
if self.buffering:
    if not env:
        env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
```

When a nonempty `env` dictionary is supplied, `PYTHONUNBUFFERED` is inserted directly into that caller-owned dictionary. An explicitly empty environment is instead replaced with the entire parent environment.

- **Suggested improvement:** Distinguish `env is None` from an empty dictionary and always copy a supplied mapping before modifying it:

```python
env = os.environ.copy() if env is None else env.copy()
env['PYTHONUNBUFFERED'] = '1'
```

- **Why it matters:** Action execution gains hidden side effects, and commands requesting an isolated empty environment unexpectedly inherit credentials, paths, and other process variables.

### 3. `IMPORT-COLLISION` — Dodo files are loaded by basename through the global module cache

- **File:** `doit/loader.py:76-96`, symbol `get_module`
- **Problematic code:**

```python
sys.path.insert(0, base_path)
...
return importlib.import_module(os.path.splitext(file_name)[0])
```

Two different files named `dodo.py` resolve to the same `sys.modules["dodo"]` entry. Filenames containing additional dots are also interpreted as package paths rather than literal file paths. Each call permanently prepends entries to `sys.path`.

- **Suggested improvement:** Load the resolved path with `importlib.util.spec_from_file_location()` under a unique module name derived from the absolute path. Add import paths only for the duration required, or explicitly document and manage retained paths.
- **Why it matters:** Long-running API users can receive tasks from the wrong project, while repeated loads accumulate global interpreter state and make behavior depend on load order.

### 4. `JSON-TRUNCATE` — Dependency state is rewritten non-atomically

- **File:** `doit/dependency.py:87-93`, symbol `JsonDB.dump`
- **Problematic code:**

```python
try:
    db_file = open(self.name, 'w')
    db_file.write(self.codec.encode(self._db))
finally:
    db_file.close()
```

Opening with `"w"` truncates the valid database before serialization and writing have succeeded. A crash, encoding failure, or disk-full error leaves a corrupt dependency database. If `open()` itself fails, `db_file.close()` raises `UnboundLocalError`, masking the original error.

- **Suggested improvement:** Encode first, write through a context manager to a temporary file in the same directory, flush and optionally `fsync`, then atomically replace the destination with `os.replace()`.
- **Why it matters:** A routine interrupted run can destroy all cached task state and force rebuilds; the unbound local also obscures actionable filesystem errors.

### 5. `PIPE-THREAD` — Output-reader failures are lost across threads

- **File:** `doit/action.py:164-178, 237-254`, symbols `_print_process_output` and `CmdAction.execute`
- **Problematic code:**

```python
except Exception:
    process.terminate()
    input_.read()
    raise
...
t_out.start()
t_err.start()
t_out.join()
t_err.join()
...
process.wait()
```

Exceptions raised by either reader thread are printed by Python’s thread exception handler but are not propagated to `execute()`. Execution continues and classifies the task solely from the subprocess return code.

- **Suggested improvement:** Capture thread exceptions in a shared result or use futures, then re-raise or return a `TaskError` after joining. Ensure both pipes and the process are cleaned up in `finally`.
- **Why it matters:** Decode and stream-write failures can be reported as misleading command failures—or even success—while captured output is incomplete.

### 6. `DUMP-HANDLE` — `dumpdb` never closes the opened database

- **File:** `doit/cmd_dumpdb.py:40-50`, symbol `DumpDB.execute`
- **Problematic code:**

```python
data = dbm.open(dep_file)
for key, value_str in dbm_iter(data):
    ...
```

The DBM object is left open on both normal completion and decoding/printing errors.

- **Suggested improvement:** Wrap it with `contextlib.closing(dbm.open(dep_file))` or an explicit `try/finally`.
- **Why it matters:** Leaked descriptors accumulate in embedded use, and DBM implementations that hold locks can prevent subsequent commands from opening or modifying the dependency database.

### 7. `TEST-ENV` — A basic CLI test depends on an undeclared-at-runtime repository tool

- **Files:** `tests/test___main__.py:8-11`; `dodo.py:7`
- **Problematic code:**

```python
subprocess.call([executable, '-m', 'doit', 'list', ...])
```

combined with:

```python
from pyflakes.api import checkPath
```

Running `pytest -q` produced **1 failure, 882 passes, 8 skips** because the subprocess discovers the repository’s `dodo.py`, which imports the development-only `pyflakes` package at module import time.

- **Suggested improvement:** Make the test execute from an isolated temporary directory with a minimal dodo file, or defer the `pyflakes` import to the lint task/action. Ensure the documented test command installs the development dependency group when repository tooling is intentionally exercised.
- **Why it matters:** The core test suite’s result depends on the checkout directory and optional tooling rather than solely on the behavior under test, reducing reproducibility in minimal CI and package-validation environments.
