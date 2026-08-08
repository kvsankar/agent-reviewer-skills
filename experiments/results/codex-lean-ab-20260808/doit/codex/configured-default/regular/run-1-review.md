# Repository Review

## High severity

### 1. `STREAM-LEAK` — Failed argument preparation leaves global streams replaced

**Location:** `doit/action.py:442`, `PythonAction.execute`

**Problematic code:**

```python
sys.stdout = out_writer
sys.stderr = err_writer

kwargs = self._prepare_kwargs()

try:
    returned_value = self.py_callable(*self.args, **kwargs)
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
```

`_prepare_kwargs()` runs after replacing `sys.stdout` and `sys.stderr`, but before entering the protected `try/finally`. Errors from `inspect.signature()`, argument binding, task-option access, or reserved-argument validation escape without restoring either stream.

**Suggested improvement:** Move argument preparation before stream replacement, or wrap the entire capture setup and preparation/execution sequence in one `try/finally`. Convert preparation errors to `TaskError` consistently if that is the intended action contract.

**Why it matters:** One malformed action can permanently redirect process-wide output into abandoned `StringIO` objects. Subsequent tasks, diagnostics, and embedding applications may silently lose output.

---

### 2. `THREAD-STDIO` — Parallel Python actions race over process-global output

**Location:** `doit/action.py:440`, `PythonAction.execute`; `doit/runner.py:563`, `MThreadRunner`

**Problematic code:**

```python
old_stdout = sys.stdout
sys.stdout = out_writer
...
sys.stdout = old_stdout
```

`MThreadRunner` can run several `PythonAction` instances concurrently, while each action independently replaces the same process-global `sys.stdout` and `sys.stderr`. Their save/restore operations can interleave, causing output to enter another task’s capture buffer and potentially leaving the wrong stream installed afterward.

**Suggested improvement:** Avoid global stream replacement during concurrent execution. Use a thread-aware proxy that routes writes through thread-local/context-local state, or explicitly serialize Python actions that require capture. Add a concurrency test with two actions emitting interleaved stdout and stderr.

**Why it matters:** Parallel runs can produce nondeterministic logs, incorrect saved output, and corrupted global process state—the exact conditions under which reliable task diagnostics are most important.

---

### 3. `LOST-READER-ERROR` — Output-thread failures are not propagated

**Location:** `doit/action.py:159` and `doit/action.py:237`, `CmdAction._print_process_output` / `execute`

**Problematic code:**

```python
except Exception:
    process.terminate()
    input_.read()
    raise
```

```python
t_out.start()
t_err.start()
t_out.join()
t_err.join()
...
if process.returncode != 0:
    return TaskFailed(...)
```

Exceptions raised inside the reader threads do not propagate through `Thread.join()`. Failures from decoding, capture writers, or real-time output streams are printed by the threading machinery and then discarded. The action result is determined only from the child’s return code.

**Suggested improvement:** Have each reader catch and place exceptions in a queue or shared result container. After joining, re-raise or return a `TaskError`, while ensuring the child is terminated and reaped. `concurrent.futures` would also provide exception-propagating futures.

**Why it matters:** Output corruption or logging failures may be reported as an unrelated subprocess failure—or even success if the process exits cleanly after the reader fails.

## Medium severity

### 4. `ENV-ALIAS` — Buffering mutates caller configuration and defeats an empty environment

**Location:** `doit/action.py:206`, `CmdAction.execute`

**Problematic code:**

```python
env = subprocess_pkwargs['env']
...
if self.buffering:
    if not env:
        env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
```

A non-empty caller-supplied environment is modified in place because only the outer `pkwargs` dictionary is copied. Conversely, an explicitly supplied empty environment (`env={}`) is treated as absent and replaced with the full parent environment.

**Suggested improvement:**

```python
if self.buffering:
    env = os.environ.copy() if env is None else env.copy()
    env["PYTHONUNBUFFERED"] = "1"
```

**Why it matters:** Reusing the original environment dictionary changes later commands unexpectedly, while replacing `{}` can leak parent credentials or configuration into a subprocess the caller intended to isolate.

---

### 5. `MASKED-OPEN` — JSON database errors can be replaced by `UnboundLocalError`

**Location:** `doit/dependency.py:87`, `JsonDB.dump`

**Problematic code:**

```python
try:
    db_file = open(self.name, 'w')
    db_file.write(self.codec.encode(self._db))
finally:
    db_file.close()
```

If `open()` fails, `db_file` was never assigned, so the `finally` block raises `UnboundLocalError`, hiding the meaningful permission, path, or filesystem error.

**Suggested improvement:** Use a context manager:

```python
with open(self.name, "w", encoding="utf-8") as db_file:
    db_file.write(self.codec.encode(self._db))
```

For stronger correctness, write to a sibling temporary file, flush it, and atomically replace the database.

**Why it matters:** Masking the original exception makes configuration and filesystem failures difficult to diagnose. Directly truncating the database also leaves corrupted state if encoding or writing fails midway.

---

### 6. `GLOBAL-SQLITE-CODEC` — Backend initialization changes SQLite behavior process-wide

**Location:** `doit/dependency.py:253`, `SqliteDB._sqlite3`

**Problematic code:**

```python
sqlite3.register_adapter(list, self.codec.encode)
sqlite3.register_adapter(dict, self.codec.encode)
sqlite3.register_converter("json", converter)
```

SQLite adapters and converters are global registries. Constructing a doit dependency backend therefore changes how every SQLite connection in the hosting process serializes lists, dictionaries, and `json` columns. A custom doit codec can overwrite behavior expected by unrelated application code.

**Suggested improvement:** Encode task data explicitly before passing it to SQL and decode it explicitly after fetching it. Store it as `TEXT` or `BLOB`, avoiding global adapter/converter registration.

**Why it matters:** `doit` is also exposed as an embeddable API. Initializing its backend can unexpectedly break an embedding application’s independent database code.

## Low severity

### 7. `EMPTY-ARGV` — Valid empty arguments crash argument processing

**Location:** `doit/doit_cmd.py:215`, `DoitMain.process_args`; similarly `doit/loader.py:193`, `load_tasks`

**Problematic code:**

```python
for arg in cmd_args:
    if (arg[0] != '-') and ('=' in arg):
```

and:

```python
for index, term in enumerate(args):
    if term[0] != '-':
```

Both paths index the first character without checking whether the string is empty. An empty argument can be supplied through an API or from a shell using `""`, resulting in `IndexError` rather than normal parsing or a structured command error.

**Suggested improvement:** Use guarded predicates such as `not arg.startswith('-')`, and decide explicitly whether empty strings should be retained as positional values or rejected with `CmdParseError`.

**Why it matters:** Command-line parsing should handle arbitrary strings predictably, particularly when the library is driven programmatically rather than solely through a conventional shell.
