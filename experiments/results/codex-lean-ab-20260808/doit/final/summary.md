# Codex regular vs lean-skill evaluation

## Condition summary

| Condition | Runs | Frozen recall | Validated/run | Total valid hits | Distinct valid | Novel invalid | Evidence flags |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| lean-skill | 3 | 30.2% | 8.33 | 25 | 13 | 0 | 0 |
| regular | 3 | 28.5% | 8.67 | 26 | 18 | 0 | 1 |

## Novel adjudications

### NV-001: DbmDB.set and SqliteDB.set initialize empty in-memory dict without loading persisted data, causing dump() to silently erase sibling keys

- Verdict: valid
- Severity: high
- Location: `doit/dependency.py:183-188`
- Candidates: N-001, N-005, N-010

The bug is concrete and mechanical: `set()` on either backend skips loading persisted data before initialising the in-memory entry, so the first `set()` call on a task that is present in storage but absent from the cache destroys all sibling keys at the next dump(). The `Ignore` command (cmd_ignore.py:30) calls ignore() with no preceding get/get_status, making this a real, reproducible data-loss path. For DbmDB, get() (lines 201-215) loads from _dbm only when task_id is absent from _db; once set() has created the empty entry, subsequent get() calls return from the incomplete in-memory dict, so the persistent data is never merged.

### NV-002: PythonAction.execute replaces process-global sys.stdout/sys.stderr without synchronization, corrupting output capture under MThreadRunner

- Verdict: valid
- Severity: high
- Location: `doit/action.py:429-493`
- Candidates: N-002, N-007

The manipulation of sys.stdout and sys.stderr at lines 451/459/484/485 is non-atomic and unguarded. Under MThreadRunner the DaemonThread children all share the same process address space and thus the same sys.stdout/sys.stderr globals. Interleaved assignments cause output from Task A to appear in Task B's captured output and vice-versa; the final restoration may leave sys.stdout pointing at a Writer whose StringIO has already been discarded. This is a concrete, deterministic race condition whenever two PythonAction tasks execute concurrently.

### NV-003: Exceptions raised inside _print_process_output reader threads are silently discarded after Thread.join(); a write failure also stops pipe draining and can deadlock process.wait()

- Verdict: valid
- Severity: medium
- Location: `doit/action.py:159-247`
- Candidates: N-003, N-006, N-008, N-013

Python's Thread.join() does not propagate exceptions; the re-raise in the decode-error handler (line 176) terminates the thread with an unhandled exception that disappears. execute() sees a TaskFailed with a signal exit code but no information about the actual failure. For write errors on lines 179-182 there is no exception handler at all, so the thread exits mid-loop with the pipe potentially un-drained. Since process.stdout is still open (held by the Popen object), the child's write end of the pipe is not broken; the child can block forever filling the buffer, and process.wait() hangs.

### NV-004: Top-level `from pyflakes.api import checkPath` in dodo.py causes ImportError and breaks all doit invocations in environments where pyflakes is absent

- Verdict: valid
- Severity: high
- Location: `dodo.py:7-7`
- Candidates: N-004, N-014

The fix is to move the import inside the `_check_pyflakes` function (deferred import). At module scope the import is unconditional and fatal on missing pyflakes, even for commands like `doit ut` or `doit list` that have no relation to linting. This breaks the developer workflow entirely in clean environments or CI pipelines that install only the test dependencies.

### NV-005: SqliteDB._sqlite3 registers process-global sqlite3 adapters and converters, polluting every sqlite3 connection in the host process

- Verdict: valid
- Severity: low
- Location: `doit/dependency.py:267-269`
- Candidates: N-009

The registrations are idempotent for doit's own connections but affect all sqlite3 connections in the process. For a standalone tool this is harmless, but when doit is used as a library the silent global mutation can corrupt the embedding application's sqlite3 column marshalling. The converter is a closure over `self.codec` created at `SqliteDB` construction time, so re-instantiating SqliteDB also rotates which codec is active for all connections.

### NV-006: subprocess.Popen call in CmdAction.execute is not wrapped in try-except, so OSError/ValueError escapes as a raw exception instead of TaskError

- Verdict: valid
- Severity: high
- Location: `doit/action.py:228-235`
- Candidates: N-011

CmdAction.execute() is documented to return TaskError or TaskFailed on failure and None on success; it never raises. Popen failures break this contract. In the single-process Runner the uncaught exception aborts run_tasks() mid-loop, leaving remaining tasks unexecuted even under --continue. The MRunner/MThreadRunner subprocess loop catches all Exceptions (runner.py:556) so the bug only manifests in the base Runner, but that is the most common execution path.

### NV-007: _prepare_kwargs calls bind_partial with positional args only, so explicitly supplied keyword arguments are not protected and can be silently overwritten by doit metadata or task options

- Verdict: valid
- Severity: low
- Location: `doit/action.py:62-97`
- Candidates: N-012

The fix is `func_sig.bind_partial(*args, **kwargs)` so that explicitly provided keyword arguments appear in bound_args.arguments and are excluded from injection. The inconsistency is observable: for a function `def f(targets): ...` invoked as `(f, [], {'targets': custom})`, the user's custom targets list is unconditionally replaced by `list(task.targets)` with no warning. The same applies to opt_args for regular named parameters.
