# Repository Review

## Review: `doit`

### ✅ Strengths

- **FUNC-SHELL**: Command orchestration, task definitions, dependency tracking, and actions are split into focused modules instead of being concentrated in one large entry point.
- **EXCEPT-HIER**: User-facing failures have domain-specific types such as `InvalidTask`, `InvalidCommand`, `TaskError`, and `TaskFailed`.
- **PURE-TEST**: The test suite frequently constructs tasks and actions directly, allowing much of the behavior to be tested without invoking the full CLI.

### ⚠️ Suggestions

#### **NO-GLOBAL-MUT**: Loading a task file permanently changes interpreter state

**Location:** `doit/loader.py:37-96`, `get_module()`

**Current code:**

```python
global initial_workdir
initial_workdir = os.getcwd()

# ...

sys.path.insert(0, base_path)

# ...

if not os.path.isdir(full_cwd):
    msg = "Specified 'dir' path must be a directory.\nGot '%s'(%s)."
    raise InvalidCommand(msg % (cwd, full_cwd))
sys.path.insert(0, full_cwd)

# file specified on dodo file are relative to cwd
os.chdir(full_cwd)

return importlib.import_module(os.path.splitext(file_name)[0])
```

**Suggested refactoring:**

```python
from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location


@contextmanager
def task_environment(workdir, import_paths):
    previous_cwd = os.getcwd()
    previous_path = sys.path[:]
    try:
        sys.path[:0] = import_paths
        os.chdir(workdir)
        yield
    finally:
        os.chdir(previous_cwd)
        sys.path[:] = previous_path


def load_module_from_path(dodo_path, workdir):
    module_name = f"_doit_dodo_{hash(dodo_path)}"
    spec = spec_from_file_location(module_name, dodo_path)
    module = module_from_spec(spec)

    with task_environment(workdir, [os.path.dirname(dodo_path), workdir]):
        spec.loader.exec_module(module)

    return module
```

**Why this matters:**

Each call currently accumulates entries in `sys.path`, changes the process-wide working directory, and updates a mutable global. An invalid `cwd` can even leave `base_path` inserted before raising. Long-lived API users and test processes can consequently import modules from an earlier project or resolve relative paths against an unexpected directory.

Importing only by basename also lets `sys.modules` return the wrong module when two task files in different directories share a filename such as `dodo.py`.

**Rhodes' principle:**

Keep mutable process state at the imperative boundary, restore it deterministically, and avoid global state that makes behavior depend on call history.

---

#### **NO-MUTARGS**: Executing a buffered command mutates the caller’s environment dictionary

**Location:** `doit/action.py:206-215`, `CmdAction.execute()`

**Current code:**

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

**Suggested refactoring:**

```python
subprocess_pkwargs = self.pkwargs.copy()
configured_env = subprocess_pkwargs.pop("env", None)
env = None if configured_env is None else configured_env.copy()

if self.buffering:
    if env is None:
        env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
```

A regression test should verify that the supplied dictionary remains unchanged:

```python
def test_buffering_does_not_mutate_supplied_environment():
    supplied_env = {"MODE": "test"}
    action = CmdAction("command", buffering=1, env=supplied_env)

    # Execute with Popen replaced by a small process-boundary test fixture.

    assert supplied_env == {"MODE": "test"}
```

**Why this matters:**

The outer `pkwargs` dictionary is copied, but its nested `env` dictionary is not. Setting `PYTHONUNBUFFERED` therefore modifies an object owned by the caller. Reusing that dictionary for another command silently changes its behavior, making execution depend on which action ran first.

The `if not env` check also treats an intentionally empty environment like a missing environment and replaces it with the entire parent environment. Testing `env is None` preserves the distinction.

**Rhodes' principle:**

Methods should not introduce hidden mutation through their arguments. Copy caller-owned mutable data before adding execution-specific values.

---

#### **HOIST-IO**: The null-output file descriptor is opened inside execution and never closed

**Location:** `doit/action.py:217-235`, `CmdAction.execute()`

**Current code:**

```python
if capture_io:
    p_out = p_err = subprocess.PIPE
else:
    if capture_io is False:
        p_out = out
        p_err = err
    else:  # None
        p_out = p_err = open(os.devnull, "w")

process = subprocess.Popen(
    action,
    shell=self.shell,
    stdout=p_out,
    stderr=p_err,
    env=env,
    **subprocess_pkwargs)
```

**Suggested refactoring:**

```python
from contextlib import nullcontext


if capture_io is None:
    output_target = open(os.devnull, "w")
    output_context = output_target
else:
    output_target = None
    output_context = nullcontext()

with output_context:
    if capture_io:
        p_out = p_err = subprocess.PIPE
    elif capture_io is False:
        p_out, p_err = out, err
    else:
        p_out = p_err = output_target

    process = subprocess.Popen(
        action,
        shell=self.shell,
        stdout=p_out,
        stderr=p_err,
        env=env,
        **subprocess_pkwargs,
    )
    process.wait()
```

An even clearer design would move stream selection into a context manager whose sole responsibility is owning and closing any files it opens.

**Why this matters:**

Every action using `io.capture = None` leaks a file descriptor. Large task graphs or a persistent process can eventually exhaust the descriptor limit and fail unrelated file or subprocess operations. Explicit ownership also ensures cleanup if `Popen()` or `wait()` raises.

**Rhodes' principle:**

Keep resource acquisition visible at the I/O boundary and pair it structurally with cleanup.

---

#### **HOIST-IO**: The dependency database is opened without deterministic cleanup

**Location:** `doit/cmd_dumpdb.py:40-50`, `DumpDB.execute()`

**Current code:**

```python
data = dbm.open(dep_file)
for key, value_str in dbm_iter(data):
    value_dict = json.loads(value_str.decode('utf-8'))
    value_fmt = pprint.pformat(value_dict, indent=4, width=100)
    print("{key} -> {value}".format(key=key, value=value_fmt))
```

**Suggested refactoring:**

```python
with dbm.open(dep_file) as data:
    for key, value_bytes in dbm_iter(data):
        value = json.loads(value_bytes.decode("utf-8"))
        formatted_value = pprint.pformat(value, indent=4, width=100)
        print(f"{key} -> {formatted_value}")
```

If compatibility with a backend lacking context-manager support is required:

```python
from contextlib import closing


with closing(dbm.open(dep_file)) as data:
    for key, value_bytes in dbm_iter(data):
        value = json.loads(value_bytes.decode("utf-8"))
        print(f"{key} -> {pprint.pformat(value, indent=4, width=100)}")
```

**Why this matters:**

A DBM backend can retain file descriptors and locks until it is closed. Relying on garbage collection makes cleanup implementation-dependent and can prevent subsequent commands from reopening or replacing the dependency database, especially on platforms with strict file locking.

**Rhodes' principle:**

I/O-owning code should make the lifetime of external resources explicit and deterministic.

---

#### **EXCEPT-HIER**: Dependency lookup exposes generic exceptions with no semantic contract

**Location:** `doit/dependency.py:558-571`, `Dependency.get_value()`

**Current code:**

```python
if not self._in(task_id):
    # FIXME do not use generic exception
    raise Exception("taskid '%s' has no computed value!" % task_id)
values = self.get_values(task_id)
if key_name not in values:
    msg = "Invalid arg name. Task '%s' has no value for '%s'."
    raise Exception(msg % (task_id, key_name))
return values[key_name]
```

**Suggested refactoring:**

```python
class DependencyValueError(LookupError):
    """Base class for failures while resolving saved task values."""


class MissingTaskValue(DependencyValueError):
    pass


class MissingValueKey(DependencyValueError):
    pass


def get_value(self, task_id, key_name):
    if not self._in(task_id):
        raise MissingTaskValue(
            f"Task {task_id!r} has no computed value."
        )

    values = self.get_values(task_id)
    if key_name not in values:
        raise MissingValueKey(
            f"Task {task_id!r} has no value for {key_name!r}."
        )

    return values[key_name]
```

**Why this matters:**

Callers cannot distinguish missing task results from programming errors without parsing message text or catching every `Exception`. A specific hierarchy lets the CLI translate expected lookup failures into concise user errors while allowing unexpected defects to retain their tracebacks.

**Rhodes' principle:**

An exception hierarchy is part of an API’s vocabulary: callers should be able to respond to categories of failure instead of matching prose.

---

#### **EXCEPT-HIER**: Argument parsing catches defects unrelated to invalid command-line input

**Location:** `doit/cmdparse.py:306-324`, `CmdParse.parse_only()`

**Current code:**

```python
try:
    opts, args = getopt.getopt(in_args, self.get_short(),
                               self.get_long())
except Exception as error:
    msg = (f"Error parsing {self._type}: {error} "
           f"(parsing options: {self.options}). Got: {in_args}")
    raise CmdParseError(msg)
```

**Suggested refactoring:**

```python
try:
    opts, args = getopt.getopt(
        in_args,
        self.get_short(),
        self.get_long(),
    )
except getopt.GetoptError as error:
    message = (
        f"Error parsing {self._type}: {error} "
        f"(parsing options: {self.options}). Got: {in_args}"
    )
    raise CmdParseError(message) from error
```

The boolean conversion has the same issue and should catch only the expected lookup failure:

```python
def str2boolean(self, string_value):
    try:
        return self._boolean_states[string_value.lower()]
    except KeyError as error:
        raise ValueError(f"Not a boolean: {string_value}") from error
```

**Why this matters:**

Catching `Exception` converts bugs in option construction, unexpected input types, and internal failures into misleading “invalid command line” messages. Narrow catches preserve tracebacks for actual defects. Explicit exception chaining also retains the low-level cause for diagnostics.

**Rhodes' principle:**

Catch only exceptions that the current layer knows how to interpret; allow unrelated failures to remain visible.

---

### 💡 Rhodes Wisdom

> “Move all I/O operations to the program’s top level, allowing core logic to remain pure and testable.”
>
> — *Hoisting Your I/O* (2015)
