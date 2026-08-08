# Claude Seed Review

- Upstream: `git@github-kvsankar:pydoit/doit.git`
- Commit: `1f9cbbce78a93f96a35abf2db5425361e2abf142`
- Status: Candidate findings only; not adjudicated ground truth

## Repository Summary

doit is a mature Python build-tool / task-runner (similar to make). The core architecture: a `loader` module reads task-creator functions from a user's `dodo.py`; a `control` module resolves dependency order; a `runner` executes tasks sequentially or in parallel (multiprocessing / threading); a `dependency` module persists task state across runs using one of three DB backends (dbm, json, sqlite). The codebase is about 4 500 lines of library code and a comparable test suite. Overall quality is high — the exception hierarchy, plugin system, and multi-backend DB abstraction are well-designed. The issues below are concrete defects rather than stylistic preferences.

## Scope Notes

Full source review of all files under doit/ and tests/. Doc-sample files and non-Python assets were not analysed. The test suite uses unittest throughout; integration tests run real subprocesses. Only findings that are reproducible from the exact checked-out source are reported.

## Candidate Findings

### B-001: JsonDB.dump() truncates the DB file before encoding completes, and raises NameError when open() itself fails

- Severity: high
- Confidence: high
- Location: `doit/dependency.py:87-93`
- Symbol: `JsonDB.dump`

Two independent bugs in one try/finally block. (1) `open(self.name, 'w')` immediately truncates the on-disk file to zero bytes. If `self.codec.encode(self._db)` subsequently raises (e.g., a non-serialisable value slipped into the DB), the file is left empty and the database is permanently corrupted. (2) If `open()` itself fails (e.g., permission error, disk full), the name `db_file` is never bound; the `finally` clause then raises `NameError: name 'db_file' is not defined`, which replaces and masks the original OS error. Compare with `_load()` in the same class, which correctly opens the file before entering the try block.

**Source evidence**

```text
def dump(self):
    try:
        db_file = open(self.name, 'w')   # truncates immediately
        db_file.write(self.codec.encode(self._db))
    finally:
        db_file.close()                  # NameError if open() raised
```

**Suggested fix**

Write to a temporary file beside the target and rename atomically on success:

import tempfile, os
def dump(self):
    dir_ = os.path.dirname(os.path.abspath(self.name))
    fd, tmp_path = tempfile.mkstemp(dir=dir_)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(self.codec.encode(self._db))
        os.replace(tmp_path, self.name)
    except:
        os.unlink(tmp_path)
        raise

This eliminates both bugs: the original file is only replaced after a successful write, and the file handle is managed by `with`.

**Why it matters**

The dependency DB is the sole persistent record of which tasks are up-to-date. Silently zeroing it forces every task to re-run on the next invocation — a subtle correctness failure that is hard to diagnose. The NameError masking bug makes the real failure (e.g., a permission error) invisible in error logs. REDUND-OK: production systems need defensive redundancy around critical persistent state.

### B-002: PythonAction.pm_pdb is a class-level attribute mutated at runtime, causing a race condition in MThreadRunner

- Severity: medium
- Confidence: high
- Location: `doit/action.py:386-386`
- Symbol: `PythonAction.pm_pdb`

`pm_pdb = False` is declared as a class attribute on `PythonAction`. `Run._execute()` sets it with `PythonAction.pm_pdb = pdb` (cmd_run.py:202) before each run. Because this modifies the class itself, all instances share one value. Under `MThreadRunner`, multiple tasks execute concurrently in different threads; if one thread's action checks `self.pm_pdb` at the same moment another invocation of `Run._execute()` is writing the class attribute (e.g., in a re-entrant API call), the threads observe an inconsistent value. Additionally, `pm_pdb` is never reset to `False` after the run, so a subsequent API call that does not explicitly set `pdb=False` inherits whatever the last run set.

**Source evidence**

```text
# action.py:386
pm_pdb = False  # class attribute

# cmd_run.py:202 — mutates the class before every run
PythonAction.pm_pdb = pdb
```

**Suggested fix**

Move `pm_pdb` out of the class and pass it through the call stack, or store it on the `Runner`/`Stream` configuration object that is already passed to `task.execute(stream)`. A minimal fix is to make it an instance attribute set by `create_action`:

# In create_action, accept an extra kwarg:
def create_action(action, task_ref, param_name, pm_pdb=False):
    ...
    if isinstance(action, ...) or hasattr(action, '__call__'):
        a = PythonAction(action, task=task_ref)
        a.pm_pdb = pm_pdb
        return a

This honours FUNC-SHELL: configuration travels down through explicit parameters, not global class mutation.

**Why it matters**

Class-level mutation is a textbook NO-MUTABLE-GLOBAL violation. Under threading, the race is real: `MThreadRunner` (runner.py:563) uses daemon threads and dispatches multiple `execute_task` calls concurrently without any lock around the class attribute. A user running `doit -n 4 --pdb` may get inconsistent debugger behaviour.

### B-003: get_module() mutates the process CWD and a module-level global as invisible side effects

- Severity: medium
- Confidence: high
- Location: `doit/loader.py:46-93`
- Symbol: `get_module`

Two hidden global mutations: (1) `global initial_workdir; initial_workdir = os.getcwd()` writes to a module-level variable used by `doit.get_initial_workdir()`. Any user code that calls `get_module()` more than once (or via the API) observes whichever invocation ran last. (2) `os.chdir(full_cwd)` at line 93 changes the working directory for the entire process without restoring it. If `importlib.import_module()` raises (e.g., a SyntaxError in dodo.py), the CWD is left changed. Tests that run in sequence are affected: `tests/test___init__.py` must work around this. Furthermore, `sys.path.insert(0, base_path)` (and potentially a second insert at line 90) are never cleaned up; every call permanently lengthens `sys.path`.

**Source evidence**

```text
global initial_workdir
initial_workdir = os.getcwd()   # line 47 — module global mutation
...
sys.path.insert(0, base_path)   # line 79 — permanent sys.path growth
...
os.chdir(full_cwd)              # line 93 — process CWD mutation, not restored
```

**Suggested fix**

Return `initial_workdir` as part of the function's return value instead of storing it in a global. Save and restore `sys.path` and CWD around the import:

def get_module(dodo_file, cwd=None, seek_parent=False):
    original_cwd = os.getcwd()
    original_path = sys.path[:]
    try:
        # ... path resolution logic ...
        sys.path.insert(0, base_path)
        os.chdir(full_cwd)
        module = importlib.import_module(...)
        return module, original_cwd  # return initial_workdir to caller
    except:
        sys.path[:] = original_path
        os.chdir(original_cwd)
        raise

Callers store the returned `initial_workdir`. This is HOIST-IO applied to filesystem state: side effects are explicit and reversible.

**Why it matters**

An unrevertible `os.chdir()` inside a library function breaks any caller that relies on relative paths after the call returns. Tests that exercise multiple dodo files in the same process will corrupt each other's CWD. The perpetually growing `sys.path` can cause surprising import shadowing when paths from previous invocations are searched first. This is a direct NO-GLOBAL-MUT violation.

### B-004: _CMDLINE_VARS is a module-level mutable dict used as a global registry for command-line variables

- Severity: medium
- Confidence: high
- Location: `doit/doit_cmd.py:29-44`
- Symbol: `_CMDLINE_VARS`

`_CMDLINE_VARS` is a module-level name that starts as `None` and is reset to `{}` by `reset_vars()` which is called inside `DoitMain.process_args()`. `get_var()` contains an explicit `None`-guard with a comment explaining it is a workaround for Windows multiprocessing. The design means: (a) any call to `get_var()` before `reset_vars()` silently returns `None` for every key, masking configuration errors; (b) successive `DoitMain().run()` calls from the same process share state unless `reset_vars()` happens to be called in between; (c) the module-level sentinel makes the code hard to test in isolation.

**Source evidence**

```text
_CMDLINE_VARS = None          # line 29
def reset_vars():
    global _CMDLINE_VARS
    _CMDLINE_VARS = {}           # line 33
def get_var(name, default=None):
    if _CMDLINE_VARS is None:   # workaround for Windows MP
        return None
    return _CMDLINE_VARS.get(name, default)
```

**Suggested fix**

Store the variable map on the `DoitMain` instance and pass it explicitly to the command, or use the PREBOUND-METHOD pattern with a small helper class:

class _CmdlineVars:
    def __init__(self):
        self._store = {}
    def reset(self): self._store = {}
    def set(self, name, value): self._store[name] = value
    def get(self, name, default=None): return self._store.get(name, default)

cmdline_vars = _CmdlineVars()

This makes the state object injectable and testable without touching module globals. Aligns with PREBOUND-METHOD.

**Why it matters**

Module-level mutable state that is conditionally `None` is a classic source of ordering-dependent bugs. The Windows multiprocessing workaround (returning `None` for every key when not initialised) means that any user of `get_var()` in a subprocess silently gets wrong defaults with no diagnostic. NO-GLOBAL-MUT: mutable globals create tests that cannot safely run in parallel.

### B-005: Dependency.get_value() raises bare Exception, bypassing the established exception hierarchy

- Severity: medium
- Confidence: high
- Location: `doit/dependency.py:564-570`
- Symbol: `Dependency.get_value`

Two `raise Exception(...)` calls exist where `DependencyError` (already defined in exceptions.py) should be used. A FIXME comment in the code acknowledges this explicitly. The consequence is concrete: in `runner.py:164`, the exception handler is `except Exception as exception:` which catches both the bare `Exception` from here and any other unexpected errors. The caller cannot distinguish a legitimate 'task has no saved value' condition from a programming error without inspecting the message string.

**Source evidence**

```text
if not self._in(task_id):
    # FIXME do not use generic exception
    raise Exception("taskid '%s' has no computed value!" % task_id)
...
    raise Exception(msg % (task_id, key_name))

# runner.py:164 — handler that catches these:
except Exception as exception:
    msg = ("ERROR getting value for argument\n" + str(exception))
    self._handle_task_error(node, DependencyError(msg))
```

**Suggested fix**

Replace the two bare `Exception` raises with `DependencyError` (or a new `MissingValue(DependencyError)` subclass for precision):

from .exceptions import DependencyError

if not self._in(task_id):
    raise DependencyError("taskid '%s' has no computed value!" % task_id)
...
raise DependencyError(msg % (task_id, key_name))

This resolves the acknowledged FIXME and aligns with EXCEPT-HIER: 'define custom exception hierarchy and raise it in business logic'.

**Why it matters**

Raising bare `Exception` means any downstream `except DependencyError` handler (in plugins or user code) will silently miss these failures. It also makes test assertions fragile — tests must assert on the message string instead of the exception type. The FIXME comment confirms the maintainers know this is wrong but it has not been addressed.

### B-006: File handle for os.devnull is opened but never closed in CmdAction.execute()

- Severity: low
- Confidence: high
- Location: `doit/action.py:225-225`
- Symbol: `CmdAction.execute`

When `task.io.capture` is `None` (neither `True` nor `False`), the code opens `/dev/null` for writing and passes the handle directly to `subprocess.Popen`. Neither the handle nor the subprocess pipe is ever explicitly closed in this branch. The handle is held open until garbage-collected. Under Python's reference-counting GC this is usually prompt, but under PyPy or if the task loop is tight it delays release of OS file descriptors.

**Source evidence**

```text
else:  # None
    p_out = p_err = open(os.devnull, "w")  # handle never closed

# spawn task process
process = subprocess.Popen(
    action, shell=self.shell,
    stdout=p_out, stderr=p_err, ...)
```

**Suggested fix**

Use `subprocess.DEVNULL` (available since Python 3.3) instead of manually opening `/dev/null`:

else:  # capture is None
    p_out = p_err = subprocess.DEVNULL

This eliminates the manual file handle entirely. `subprocess.DEVNULL` is an integer constant; `Popen` handles it directly without allocating a file object.

**Why it matters**

Beyond the descriptor leak, using `subprocess.DEVNULL` is the documented idiomatic approach. The current code invents a workaround that Python's standard library already solves. On Windows, file handles are a scarcer resource than on Linux, so this matters more in cross-platform use.

### B-007: assert used to validate user-supplied TOML configuration, stripped under python -O

- Severity: medium
- Confidence: high
- Location: `doit/doit_cmd.py:135-135`
- Symbol: `DoitConfig.load_config_toml`

`assert plugin_type in self.PLUGIN_TYPES` validates a value read from a user's `pyproject.toml`. Python's `-O` (optimise) and `-OO` flags, as well as certain packaging workflows and some CI environments, strip all `assert` statements. Under those conditions, an invalid plugin type (e.g., a typo like `'comand'`) passes silently and the result is `toml_config['COMAND'] = plugins` — an unreachable key that causes the plugin to be silently ignored with no error message.

**Source evidence**

```text
for plugin_type, plugins in doit_toml.pop('plugins', {}).items():
    assert plugin_type in self.PLUGIN_TYPES   # stripped by python -O
    toml_config[plugin_type.upper()] = plugins
```

**Suggested fix**

Replace the assert with an explicit check that raises `InvalidDodoFile`:

for plugin_type, plugins in doit_toml.pop('plugins', {}).items():
    if plugin_type not in self.PLUGIN_TYPES:
        raise InvalidDodoFile(
            f"Invalid plugin type '{plugin_type}' in TOML config. "
            f"Must be one of: {self.PLUGIN_TYPES}")
    toml_config[plugin_type.upper()] = plugins

This is consistent with the rest of the codebase which uses explicit `raise InvalidDodoFile(...)` for config validation errors.

**Why it matters**

Using `assert` for input validation is a well-known Python anti-pattern. The Python documentation explicitly states asserts are for internal invariants, not external validation. A user who misspells a plugin type in their config will get no feedback — plugins simply won't load. The existing `InvalidDodoFile` exception exists precisely for this purpose and is already handled at the top of `DoitMain.run()`.
