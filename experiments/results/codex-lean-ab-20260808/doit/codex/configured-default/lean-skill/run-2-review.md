# Repository Review

## 1. **MODULE-COLLIDE** — Dodo files can resolve to the wrong cached module

**Location:** `doit/loader.py:76–96`, `get_module`

**Problematic code:**

```python
base_path, file_name = os.path.split(dodo_path)
sys.path.insert(0, base_path)
os.chdir(full_cwd)
return importlib.import_module(os.path.splitext(file_name)[0])
```

Python caches imports by module name. Loading `/project-a/dodo.py` and then `/project-b/dodo.py` in the same process will return the first cached `dodo` module. Non-identifier filenames and two files with the same basename are also handled unreliably.

**Suggested improvement:** Load the exact resolved path with `importlib.util.spec_from_file_location()` and a path-derived unique module name. Define explicitly whether repeated loading should reuse or replace that module.

**Why it matters:** Embedded/API users can silently execute tasks from the wrong project, which is a serious correctness and potentially security-sensitive failure.

---

## 2. **NO-GLOBAL-MUT** — Python action output capture is unsafe under threaded execution

**Location:** `doit/action.py:440–492`, `PythonAction.execute`

**Problematic code:**

```python
old_stdout = sys.stdout
...
sys.stdout = out_writer
...
old_stderr = sys.stderr
...
sys.stderr = err_writer
...
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
```

`sys.stdout` and `sys.stderr` are process-wide globals, while `MThreadRunner` can execute multiple Python actions concurrently. Actions can therefore capture one another’s output or restore streams in the wrong order.

**Suggested improvement:** Avoid global stream replacement for concurrent actions. Pass output writers explicitly through the action boundary, use a thread-aware proxy based on thread-local/context-local state, or prohibit Python-action capture in the threaded runner.

**Why it matters:** Parallel task logs become nondeterministic and may be attributed to the wrong task; the process can also be left with an incorrect global stream.

---

## 3. **SAFE-DEFAULT** — JSON dependency persistence can destroy the previous database

**Location:** `doit/dependency.py:87–93`, `JsonDB.dump`

**Problematic code:**

```python
try:
    db_file = open(self.name, 'w')
    db_file.write(self.codec.encode(self._db))
finally:
    db_file.close()
```

Opening with `"w"` truncates the existing dependency database before encoding and writing have succeeded. A serialization error, disk-full condition, or interrupted write leaves an empty or partial database. If `open()` itself fails, `db_file` is unbound in `finally`, masking the original exception with `UnboundLocalError`.

**Suggested improvement:** Encode before opening the destination, write to a temporary file in the same directory, flush and optionally `fsync`, then atomically replace the old file with `os.replace()`. Use a `with` statement for file ownership.

**Why it matters:** An otherwise recoverable save error can erase all recorded task state and cause unnecessary or incorrect rebuild decisions.

---

## 4. **NO-MUTARGS** — Command execution mutates the caller’s environment mapping

**Location:** `doit/action.py:207–215`, `CmdAction.execute`

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

Only `pkwargs` is copied; its nested `env` dictionary remains caller-owned. When buffering is enabled, execution adds or overwrites `PYTHONUNBUFFERED` in that original dictionary.

**Suggested improvement:**

```python
supplied_env = subprocess_pkwargs.pop("env", None)
env = supplied_env.copy() if supplied_env is not None else None
```

Then apply action-specific changes to the copy. Use `env is None` rather than `if not env`, since an intentionally empty environment is valid.

**Why it matters:** Reusing the environment mapping for another subprocess can unexpectedly change its behavior, making task execution order-dependent.

---

## 5. **CONTROL-CALLER** — Reader-thread failures are lost and can hang command execution

**Location:** `doit/action.py:159–182, 237–254`, `CmdAction._print_process_output` and `CmdAction.execute`

**Problematic code:**

```python
t_out = Thread(target=self._print_process_output, ...)
t_err = Thread(target=self._print_process_output, ...)
t_out.start()
t_err.start()
t_out.join()
t_err.join()
...
process.wait()
```

Exceptions raised in either reader thread are printed by Python but are not propagated to `execute()`. In particular, if a real-time output writer raises, that reader stops draining its pipe. A child producing enough output can then block on the full pipe while the parent waits indefinitely.

**Suggested improvement:** Have reader threads communicate exceptions through a queue or `concurrent.futures`, terminate and reap the subprocess when either reader fails, and return a `TaskError` containing the original failure.

**Why it matters:** Output-stream failures can be reported as unrelated command failures, lose output, or deadlock an entire build.

---

## 6. **HOIST-IO** — Importing the repository dodo file requires an optional lint dependency

**Location:** `dodo.py:7, 23–24`

**Problematic code:**

```python
from pyflakes.api import checkPath
...
def _check_pyflakes(py_file):
    return not bool(checkPath(py_file))
```

Merely loading the task definitions requires `pyflakes`, even for commands unrelated to linting. In the inspected environment, this caused `python3 -m pytest -q` to fail at `tests/test___main__.py::TestMain.test_execute`: its `doit list` subprocess exited with code 3 because `dodo.py` could not import `pyflakes`.

**Suggested improvement:** Import `checkPath` inside `_check_pyflakes`, or isolate lint tasks in a module loaded only when those tasks execute. Ensure the subprocess test either uses a minimal fixture dodo file or declares the required development dependency.

**Why it matters:** Basic commands such as `doit list` and the repository’s own test suite fail in otherwise functional installations that omit an unrelated lint tool.
