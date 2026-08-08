# Repository Review

## 1. **DATA-PRESERVE** — Incremental writes erase persisted task metadata

**Location:** `doit/dependency.py:183` (`DbmDB.set`), `doit/dependency.py:309` (`SqliteDB.set`)

**Problematic code:**

```python
# DbmDB
if task_id not in self._db:
    self._db[task_id] = {}
self._db[task_id][dependency] = value
```

```python
# SqliteDB
if task_id not in self._cache:
    self._cache[task_id] = {}
self._cache[task_id][dependency] = value
```

When a task already exists in persistent storage but has not been loaded into the in-memory cache, `set()` starts from an empty dictionary. On `dump()`, that partial dictionary replaces the complete persisted record.

For example, reopening a database containing `{"a": 1}` and setting only `"b"` produces `{"b": 2}`; `"a"` is lost. This affects both DBM and SQLite backends, while `JsonDB` preserves the existing record.

**Suggested improvement:**

Load the existing task record before updating it:

```python
if task_id not in self._db:
    self._db[task_id] = self.codec.decode(
        self._dbm[task_id].decode("utf-8")
    ) if self._in_dbm(task_id) else {}
```

Use the corresponding `_get_task_data()` operation for SQLite. Add backend-parametrized tests that close, reopen, add a second field without first reading, and verify both fields survive.

**Why it matters:** Commands that update a single field, such as marking a previously executed task ignored, can silently discard dependency signatures, saved values, results, and checker metadata. This is a data-integrity defect that causes unnecessary reruns and lost task state.

---

## 2. **IMPORT-IDENTITY** — Dodo files with the same basename reuse the wrong module

**Location:** `doit/loader.py:76-96` (`get_module`)

**Problematic code:**

```python
base_path, file_name = os.path.split(dodo_path)
sys.path.insert(0, base_path)
...
return importlib.import_module(os.path.splitext(file_name)[0])
```

The absolute path is reduced to a basename such as `dodo`, then loaded through Python’s global module cache. Loading `/project-a/dodo.py` followed by `/project-b/dodo.py` in the same process returns the already-cached `project-a` module.

The inserted `sys.path` entries also remain process-wide, further making later imports dependent on earlier calls.

**Suggested improvement:**

Load the file from its resolved path with `importlib.util.spec_from_file_location()` and a module identity derived from that path. Limit temporary `sys.path` changes with `try/finally` where they remain necessary.

Add a test that loads two different files sharing the same basename in one process and verifies that each module’s own tasks are returned.

**Why it matters:** Embedded API users, test suites, notebooks, and long-running processes can execute tasks from the wrong project without receiving an error.

---

## 3. **NO-MUTARGS** — Command execution mutates the caller’s environment mapping

**Location:** `doit/action.py:206-215` (`CmdAction.execute`)

**Problematic code:**

```python
subprocess_pkwargs = self.pkwargs.copy()
env = None
if 'env' in subprocess_pkwargs:
    env = subprocess_pkwargs['env']
    del subprocess_pkwargs['env']
if self.buffering:
    if not env:
        env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
```

Only the outer `pkwargs` dictionary is copied. A caller-provided `env` dictionary remains shared and is modified in place when buffering is enabled.

An explicitly supplied empty environment is also treated as absent because of `if not env`, causing it to be replaced with the complete parent environment.

**Suggested improvement:**

Distinguish `None` from an intentionally empty mapping and always copy caller-owned data:

```python
if self.buffering:
    env = os.environ.copy() if env is None else env.copy()
    env["PYTHONUNBUFFERED"] = "1"
```

Add tests confirming that both non-empty and empty caller-provided mappings remain unchanged.

**Why it matters:** Reusing the environment dictionary for later processes produces order-dependent behavior, while replacing an empty environment can unexpectedly expose parent-process variables to a child.

---

## 4. **THREAD-ERROR** — Output-reader failures are not propagated to action execution

**Location:** `doit/action.py:159-182`, `doit/action.py:237-254` (`_print_process_output`, `CmdAction.execute`)

**Problematic code:**

```python
t_out = Thread(target=self._print_process_output, ...)
t_err = Thread(target=self._print_process_output, ...)
t_out.start()
t_err.start()
t_out.join()
t_err.join()

self.out = output.getvalue()
self.err = errput.getvalue()
```

Exceptions raised by `_print_process_output()` occur in worker threads. `join()` waits for those threads but does not propagate their exceptions, so `execute()` continues and reports only the subprocess return code. Decode errors and failures writing to real-time streams are therefore printed asynchronously or reduced to an unrelated task failure.

**Suggested improvement:**

Use futures, an exception queue, or a thread wrapper that captures `BaseException`. After joining, terminate and reap the child if necessary, then return a `TaskError` containing the original exception. Test `execute()` itself with strict decoding and invalid bytes instead of testing only `_print_process_output()` directly.

**Why it matters:** The actionable cause of a failed command is lost, partial output can be accepted as complete, and callers cannot reliably distinguish subprocess failure from output-processing failure.

---

## 5. **EXCEPT-PRESERVE** — JSON database write failures can be masked by `UnboundLocalError`

**Location:** `doit/dependency.py:87-93` (`JsonDB.dump`)

**Problematic code:**

```python
try:
    db_file = open(self.name, 'w')
    db_file.write(self.codec.encode(self._db))
finally:
    db_file.close()
```

If `open()` fails—for example, because the directory is missing or permissions deny writing—`db_file` is never assigned. The `finally` block then raises `UnboundLocalError`, masking the original filesystem exception.

**Suggested improvement:**

Use a context manager:

```python
with open(self.name, "w", encoding="utf-8") as db_file:
    db_file.write(self.codec.encode(self._db))
```

For stronger data integrity, write to a temporary file in the same directory and atomically replace the database after encoding and writing succeed.

**Why it matters:** Users receive a misleading exception instead of the real path or permission error, and direct writes can leave the dependency database truncated if serialization or writing fails.
