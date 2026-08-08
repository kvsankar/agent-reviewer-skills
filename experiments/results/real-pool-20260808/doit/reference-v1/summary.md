# Review Pool v1

- Upstream: `git@github-kvsankar:pydoit/doit.git`
- Commit: `1f9cbbce78a93f96a35abf2db5425361e2abf142`
- Valid reference findings: 21
- Invalid candidates: 24
- Uncertain candidates: 0

## Scores

| Origin | Review | Valid | Precision | Coverage | Unique |
| --- | --- | ---: | ---: | ---: | ---: |
| B1 | `claude/sonnet/baseline-1` | 9 | 90.0% | 42.9% | 2 |
| X1 | `codex/configured-default/hybrid` | 10 | 100.0% | 47.6% | 4 |
| X2 | `codex/configured-default/ids-only` | 11 | 100.0% | 52.4% | 3 |
| X3 | `codex/configured-default/zero-shot` | 7 | 77.8% | 33.3% | 1 |
| X4 | `pi-ollama/devstral-small-2_latest/hybrid` | 0 | 0.0% | 0.0% | 0 |
| X5 | `pi-ollama/devstral-small-2_latest/ids-only` | 0 | 0.0% | 0.0% | 0 |
| X6 | `pi-ollama/devstral-small-2_latest/zero-shot` | 0 | 0.0% | 0.0% | 0 |
| X7 | `pi-ollama/qwen3-coder_30b/hybrid` | 0 | 0.0% | 0.0% | 0 |
| X8 | `pi-ollama/qwen3-coder_30b/ids-only` | 0 | 0.0% | 0.0% | 0 |
| X9 | `pi-ollama/qwen3-coder_30b/zero-shot` | 0 | 0.0% | 0.0% | 0 |

## Validated Reference Inventory

### R-001: JsonDB.dump() leaves db_file unbound when open() raises, masking the original exception

- Severity: high
- Location: `doit/dependency.py:87-93`
- Symbol: `JsonDB.dump`
- Anonymous candidates: C-002, C-038

This is a concrete, reproducible defect. Any OS-level failure on open() (disk full, permissions, etc.) produces a misleading secondary UnboundLocalError that hides the root cause. The fix requires initializing `db_file = None` before the try, or using a context manager.

```text
Line 89: `try:`, line 90: `db_file = open(self.name, 'w')`, line 93: `finally: db_file.close()`. If `open()` at line 90 raises (e.g. PermissionError), `db_file` is never bound. The `finally` clause then raises `UnboundLocalError: name 'db_file' is not defined`, which replaces the original OS exception in the exception chain.
```

### R-002: get_module() overwrites the module-level initial_workdir on every call

- Severity: low
- Location: `doit/loader.py:46-47`
- Symbol: `get_module`
- Anonymous candidates: C-004, C-021

Actionable in library and test scenarios where get_module() is called more than once per interpreter session. The variable name ('initial') implies it should only be captured once, but the implementation makes it last-write-wins. Low severity because standard CLI usage calls it once.

```text
Lines 46-47: `global initial_workdir; initial_workdir = os.getcwd()`. The module-level variable (defined at line 17) is meant to record 'Directory path from where doit was executed', but is unconditionally overwritten on each call. A second call with a different working directory silently clobbers the first value.
```

### R-003: get_module() changes process CWD with os.chdir but does not restore it if the subsequent import fails

- Severity: medium
- Location: `doit/loader.py:93-96`
- Symbol: `get_module`
- Anonymous candidates: C-005, C-023

If the import fails, the process-wide CWD is left at `full_cwd` for the remainder of the interpreter session. All subsequent relative-path operations are affected. A try/finally restoring `os.getcwd()` captured before line 93 would fix this.

```text
Line 93: `os.chdir(full_cwd)` executes unconditionally. Line 96: `return importlib.import_module(...)` can raise (SyntaxError, ImportError, any exception from module top-level code). There is no try/finally around line 93 to restore the prior CWD on failure.
```

### R-004: get_module() permanently inserts entries into sys.path on every call without cleanup

- Severity: medium
- Location: `doit/loader.py:79-90`
- Symbol: `get_module`
- Anonymous candidates: C-006, C-015, C-022

Each call leaks at least one sys.path entry, which can cause import-name shadowing for modules with the same name in different directories. The effect compounds across successive calls. A try/finally removing the inserted paths would be the appropriate fix.

```text
Line 79: `sys.path.insert(0, base_path)`. Lines 86-90: if `cwd` is provided, `sys.path.insert(0, full_cwd)` as well. Neither insertion is ever removed. In test suites or library usage where get_module() is called repeatedly with different dodo files, sys.path grows without bound and earlier base_path entries shadow modules in later calls.
```

### R-006: Dependency.get_value() raises bare Exception instead of a domain-specific error type

- Severity: medium
- Location: `doit/dependency.py:558-571`
- Symbol: `Dependency.get_value`
- Anonymous candidates: C-008, C-029

Callers cannot distinguish a missing-task error from a missing-key error without string-parsing, and neither can be caught specifically. A dedicated exception type (e.g. a subclass of the existing DatabaseException) is needed. The FIXME makes this an acknowledged, actionable defect.

```text
Line 565: `# FIXME do not use generic exception`. Lines 566, 570: `raise Exception(...)` in both error branches. The FIXME comment is the codebase's own acknowledgement of the defect.
```

### R-007: CmdAction.execute() opens os.devnull but never closes the file handle

- Severity: medium
- Location: `doit/action.py:224-235`
- Symbol: `CmdAction.execute`
- Anonymous candidates: C-009, C-027, C-037

Each task execution with `capture_io=None` leaks one file descriptor. Under CPython, refcount-based GC typically closes it promptly, but this is an implementation detail. Under PyPy or with many short-lived tasks, the process can exhaust its FD limit. Using a context manager or explicitly closing the devnull handle is the correct fix.

```text
Line 225: `p_out = p_err = open(os.devnull, 'w')`. The returned file object is passed to `subprocess.Popen` as stdout/stderr (lines 231-232). Popen duplicates the FD into the child process but does not close the Python-side file object. There is no `close()` call and no context manager on this path.
```

### R-008: DoitConfig.load_config_toml validates plugin_type with assert, which is stripped by python -O

- Severity: medium
- Location: `doit/doit_cmd.py:135-135`
- Symbol: `DoitConfig.load_config_toml`
- Anonymous candidates: C-010, C-020

This is a concrete correctness defect. The fix is to replace the assert with an explicit `if/raise` using a descriptive error message.

```text
Line 135: `assert plugin_type in self.PLUGIN_TYPES`. Under `python -O` or `python -OO`, all assert statements are removed. An unknown plugin_type from the TOML file then silently passes this check and is stored in `toml_config[plugin_type.upper()]`, producing undefined behavior downstream.
```

### R-009: CmdAction.execute() mutates the caller's original env dict via shallow copy of pkwargs

- Severity: high
- Location: `doit/action.py:206-215`
- Symbol: `CmdAction.execute`
- Anonymous candidates: C-012, C-025, C-035

Any code that reuses a CmdAction or shares the env dict across actions will observe the spurious PYTHONUNBUFFERED key. The fix is `env = subprocess_pkwargs['env'].copy()` (or a deep copy of pkwargs) before mutating.

```text
Line 207: `subprocess_pkwargs = self.pkwargs.copy()` is a shallow copy, so `subprocess_pkwargs['env']` and `self.pkwargs['env']` reference the same dict object. Line 210: `env = subprocess_pkwargs['env']` captures this shared reference. Line 215: `env['PYTHONUNBUFFERED'] = '1'` modifies the dict in place when `self.buffering` is truthy, permanently altering the caller's original dictionary.
```

### R-010: CmdAction.execute() conflates an explicitly empty env dict {} with no env via 'if not env'

- Severity: medium
- Location: `doit/action.py:212-215`
- Symbol: `CmdAction.execute`
- Anonymous candidates: C-013, C-026, C-036

The correct guard is `if env is None` to distinguish the 'not supplied' case from the 'explicitly empty' case. This is a real behavioral defect for callers who intentionally supply an empty environment.

```text
Lines 212-215: `if self.buffering: if not env: env = os.environ.copy()`. The condition `not env` is True for both `None` (env not provided) and `{}` (explicitly empty environment). A caller who passes `env={}` to spawn a subprocess with a clean environment will instead receive a copy of the full parent environment.
```

### R-011: get_module() imports dodo files by basename, causing sys.modules cache collisions for same-named files in different directories

- Severity: medium
- Location: `doit/loader.py:79-96`
- Symbol: `get_module`
- Anonymous candidates: C-014, C-024, C-039

This is a concrete defect in library and test usage where get_module() is called more than once per interpreter. The fix is to use importlib machinery that bypasses the sys.modules cache (e.g. importlib.util.spec_from_file_location with a unique module name).

```text
Line 79: `sys.path.insert(0, base_path)`. Line 96: `return importlib.import_module(os.path.splitext(file_name)[0])`. `importlib.import_module` checks `sys.modules` first. If `/project-a/dodo.py` was already imported (as module 'dodo'), a subsequent call for `/project-b/dodo.py` returns the cached module from sys.modules even though `base_path` was updated in sys.path.
```

### R-012: load_tasks() raises IndexError when args contains an empty string

- Severity: medium
- Location: `doit/loader.py:192-195`
- Symbol: `load_tasks`
- Anonymous candidates: C-019, C-040

An empty string in args is a legitimate misuse that should produce a clear error message. The IndexError propagates as an internal traceback confusing to the user. A guard `if term and term[0] != '-'` fixes this.

```text
Lines 193-195: `for index, term in enumerate(args): if term[0] != '-': arg_pos[term] = index`. If any element of `args` is the empty string `''`, `term[0]` raises `IndexError: string index out of range` instead of a controlled diagnostic error.
```

### R-013: JsonDB.dump() truncates the database file before encoding completes, leaving it empty on serialization failure

- Severity: high
- Location: `doit/dependency.py:87-93`
- Symbol: `JsonDB.dump`
- Anonymous candidates: C-001

This is a data-integrity defect. The standard fix is to write to a temporary file and rename it atomically, or to encode into a string first and only open the file for writing after encoding succeeds.

```text
Line 90: `db_file = open(self.name, 'w')` truncates the file to zero bytes immediately. Line 91: `db_file.write(self.codec.encode(self._db))` — if `self.codec.encode()` raises (e.g. non-serializable value), the file is left empty and the database is permanently lost.
```

### R-014: PythonAction.pm_pdb is a class-level attribute mutated per-run in cmd_run.py

- Severity: low
- Location: `doit/action.py:386-386`
- Symbol: `PythonAction.pm_pdb`
- Anonymous candidates: C-003

The attribute is per-run configuration that belongs on the instance or as a parameter. Class mutation is a design flaw. In concurrent test scenarios, the wrong pm_pdb value may be observed. Severity is low because concurrent Run._execute() calls are rare in practice.

```text
action.py line 386: `pm_pdb = False` (class attribute). cmd_run.py line 202: `PythonAction.pm_pdb = pdb` modifies the class, affecting all instances. All PythonAction instances in all threads see the same value. If two Run._execute() calls overlap (e.g. in test harnesses), the attribute has a race condition.
```

### R-015: Task.__init__ mutates the caller's uptodate list in-place via extend()

- Severity: medium
- Location: `doit/task.py:230-234`
- Symbol: `Task.__init__`
- Anonymous candidates: C-011

This is a genuine mutation-of-caller-argument bug. The fix is `uptodate = list(uptodate) if uptodate else []` to always work on a copy.

```text
Line 230: `uptodate = uptodate if uptodate else []`. If the caller passes a non-empty list, `uptodate` is the same object. Line 233-234: `if self.getargs: uptodate.extend(self._init_getargs())` mutates that list in place, adding result_dep entries. A caller who reuses the same uptodate list across multiple task definitions accumulates extra entries.
```

### R-016: PluginEntry.load catches bare ImportError, misreporting a broken dependency inside a found module as 'module not found'

- Severity: medium
- Location: `doit/plugin.py:47-50`
- Symbol: `PluginEntry.load`
- Anonymous candidates: C-016

A user seeing 'module not found' for a module that is actually installed will waste time debugging. The fix is to catch only `ModuleNotFoundError` (Python 3.6+) or check `e.name` against `module_name` to distinguish a missing module from a broken one, and raise with `from error` to preserve the chain.

```text
Lines 47-50: `except ImportError: raise Exception('Plugin {} module `{}` not found.')`. If the target module exists but one of its imports raises ImportError (e.g. a missing dependency), this is caught and reported as if the module itself was not found, discarding the actual error chain.
```

### R-017: PluginEntry.load raises generic Exception for both module-not-found and attribute-not-found failures

- Severity: low
- Location: `doit/plugin.py:43-55`
- Symbol: `PluginEntry.load`
- Anonymous candidates: C-017

A dedicated PluginLoadError (or similar) would allow callers to distinguish plugin load failures from other errors without parsing messages. The lack of `raise ... from error` chains means the root cause is lost. This is an actionable API quality defect.

```text
Lines 49-50: `raise Exception('Plugin {} module...')`. Lines 54-55: `raise Exception('Plugin {}:{} module...')`. Both failure branches raise a bare `Exception` with no exception chaining (`from`), so callers cannot programmatically distinguish the two failure modes and the original traceback is discarded.
```

### R-018: DoitMain.process_args raises IndexError when cmd_args contains an empty string

- Severity: medium
- Location: `doit/doit_cmd.py:215-216`
- Symbol: `DoitMain.process_args`
- Anonymous candidates: C-018

This is a concrete crash on a reachable code path. A guard `if arg and arg[0] != '-'` corrects the behavior.

```text
Lines 215-216: `for arg in cmd_args: if (arg[0] != '-') and ('=' in arg):`. If any element of `cmd_args` is `''`, `arg[0]` raises `IndexError: string index out of range`. An empty string is a plausible input from shell interpolation or API call.
```

### R-019: DumpDB.execute() opens the DBM file without a context manager, risking unreleased file locks

- Severity: medium
- Location: `doit/cmd_dumpdb.py:46-50`
- Symbol: `DumpDB.execute`
- Anonymous candidates: C-028

The fix is `with dbm.open(dep_file) as data:`. This is a concrete resource-management defect with observable consequences (lock contention) on some DBM backends.

```text
Line 46: `data = dbm.open(dep_file)`. The returned object is iterated but never explicitly closed. Some DBM backends hold exclusive file locks until the database is closed. If an exception occurs during iteration or if the GC is delayed, the lock persists, preventing other commands from opening the same DB.
```

### R-020: CmdParse.parse_only() catches bare Exception instead of getopt.GetoptError

- Severity: low
- Location: `doit/cmdparse.py:318-324`
- Symbol: `CmdParse.parse_only`
- Anonymous candidates: C-030

The overly broad catch converts internal bugs into misleading diagnostics and masks tracebacks that would help identify real defects. Narrowing to `getopt.GetoptError` is the correct fix.

```text
Lines 318-324: `try: opts, args = getopt.getopt(...) except Exception as error: raise CmdParseError(msg)`. Catching `Exception` instead of `getopt.GetoptError` means any programming error in `self.get_short()` or `self.get_long()` (e.g. a bug in option construction) is swallowed and reported as a user-facing parse error with a misleading message.
```

### R-021: CmdParse.parse_only() does not chain the caught exception when raising CmdParseError

- Severity: low
- Location: `doit/cmdparse.py:321-324`
- Symbol: `CmdParse.parse_only`
- Anonymous candidates: C-031

Using `raise CmdParseError(msg) from error` preserves the causal chain and is a concrete improvement to diagnostics. Low severity since the message string usually contains enough context.

```text
Line 324: `raise CmdParseError(msg)` without `from error`. The original getopt error is discarded from the exception chain, so `__cause__` is None. Callers and debuggers lose the low-level context (which option triggered the failure, etc.).
```

### R-024: PythonAction.execute() redirects sys.stdout/sys.stderr before the try/finally that would restore them

- Severity: high
- Location: `doit/action.py:442-469`
- Symbol: `PythonAction.execute`
- Anonymous candidates: C-034

This is a concrete, reproducible defect: any function that uses 'task', 'targets', 'dependencies', or 'changed' as argument names with defaults will trigger InvalidTask from _prepare_kwargs(), leaving the process I/O broken. The fix is to move the _prepare_kwargs() call before stream redirection, or wrap the entire block in a try/finally.

```text
Lines 451/459: `sys.stdout = out_writer` and `sys.stderr = err_writer` execute outside any try block. Line 469: `kwargs = self._prepare_kwargs()` executes after the redirection but before the `try:` at line 472 whose `finally` restores the streams. If `_prepare_kwargs()` raises InvalidTask (e.g. a reserved argument name has a default value), the finally at line 481 is never reached and sys.stdout/sys.stderr are left permanently corrupted.
```

## Adjudication Scope Notes

All 45 candidate groups were examined against the actual source. Files read: doit/dependency.py, doit/loader.py, doit/action.py, doit/doit_cmd.py, doit/task.py, doit/plugin.py, doit/cmdparse.py, doit/cmd_dumpdb.py, doit/__init__.py, doit/cmd_run.py. Key invalidations: G-030 (no STRING_FORMAT assignment inside expand_action — claim is factually wrong), G-031 (DbmDB.in_() appears exactly once — duplication claim is wrong), G-022/G-023 (save_success() correctly rebuilds the full record on every run; the only impact of set-before-get is bypassing the MD5 timestamp-skip optimization, not data corruption), G-005 (reset_vars() is called at the start of every process_args(), making successive-run corruption impossible; None sentinel is explicitly documented). Groups G-025 through G-045 covering style, docstring format, comment quality, test design, and refactoring suggestions are all marked invalid as they do not represent concrete, actionable defects in the current revision.
