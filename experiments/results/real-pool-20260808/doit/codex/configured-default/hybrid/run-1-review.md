# Repository Review

## Strengths

- **FUNC-SHELL**: The command classes generally keep CLI orchestration separate from task and dependency objects.
- **SENTINEL-OBJ**: `PluginEntry.NOT_LOADED` cleanly distinguishes an unloaded plugin from one whose value might legitimately be `None`.
- **EXPLICIT-NAME**: Core concepts such as `Dependency`, `TaskControl`, `CmdAction`, and `DelayedLoader` are named clearly.

## Findings

### 1. **NO-MUTARGS**: Task construction mutates the caller’s `uptodate` list

**Location:** `doit/task.py:230-234`, `Task.__init__`

**Current code:**

```python
uptodate = uptodate if uptodate else []

self.getargs = getargs
if self.getargs:
    uptodate.extend(self._init_getargs())
```

When a caller supplies a non-empty list, `extend()` modifies that same list. Reusing the task definition can therefore accumulate implicit checks or produce different tasks on later calls.

**Suggested refactoring:**

```python
uptodate_items = list(uptodate or ())

self.getargs = getargs
if self.getargs:
    uptodate_items.extend(self._init_getargs())

self.uptodate = self._init_uptodate(uptodate_items)
```

**Why this matters:**

Constructing a `Task` should not silently alter its input specification. Copying at the boundary makes repeated task generation deterministic and prevents state from leaking between tasks or tests.

**Rhodes’ principle:**

Avoid mutation through APIs; callers should retain ownership of objects they pass into a method.

---

### 2. **NO-MUTARGS**: Executing a buffered command modifies the caller’s environment mapping

**Location:** `doit/action.py:206-215`, `CmdAction.execute`

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

The outer `pkwargs` dictionary is copied, but its `env` value is not. If the caller supplied a non-empty environment dictionary, `PYTHONUNBUFFERED` is inserted into that original dictionary. An explicitly empty environment is also replaced with the entire parent environment because `if not env` conflates `{}` with `None`.

**Suggested refactoring:**

```python
subprocess_pkwargs = self.pkwargs.copy()
provided_env = subprocess_pkwargs.pop('env', None)
env = provided_env.copy() if provided_env is not None else None

if self.buffering:
    if env is None:
        env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
```

**Why this matters:**

The mutation can affect later subprocesses that reuse the mapping. Preserving an empty dictionary is also important: callers may intentionally request a scrubbed environment for reproducibility or security.

**Rhodes’ principle:**

Public operations should avoid surprising mutation, and distinct states such as “missing” and “explicitly empty” should remain distinct.

---

### 3. **NO-IMPORT-FX**: Dodo modules are loaded by basename and can collide in `sys.modules`

**Location:** `doit/loader.py:76-96`, `get_module`

**Current code:**

```python
base_path, file_name = os.path.split(dodo_path)
sys.path.insert(0, base_path)

# ...

os.chdir(full_cwd)

# get module containing the tasks
return importlib.import_module(os.path.splitext(file_name)[0])
```

Two files such as `/project-a/dodo.py` and `/project-b/dodo.py` share the module name `dodo`. Loading the second in the same interpreter can return the first cached module. The function also permanently grows `sys.path`, including when importing fails.

**Suggested refactoring:**

```python
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import hashlib

def load_dodo_module(dodo_path):
    resolved_path = Path(dodo_path).resolve()
    digest = hashlib.sha256(str(resolved_path).encode()).hexdigest()
    module_name = f"_doit_dodo_{digest}"

    spec = spec_from_file_location(module_name, resolved_path)
    if spec is None or spec.loader is None:
        raise InvalidDodoFile(f"Could not load dodo file {resolved_path!s}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

If sibling imports require temporarily changing `sys.path`, that change should be scoped with `try/finally` and removed afterward.

**Why this matters:**

Long-running processes, test suites, notebooks, and applications embedding `DoitMain` can execute tasks from the wrong project. Persistent import-path mutation also makes later imports depend on call order.

**Rhodes’ principle:**

Import behavior should be predictable and should avoid hidden global side effects.

---

### 4. **EXCEPT-HIER**: Plugin loading misreports dependency failures as missing plugins

**Location:** `doit/plugin.py:43-55`, `PluginEntry.load`

**Current code:**

```python
try:
    module = importlib.import_module(module_name)
except ImportError:
    raise Exception('Plugin {} module `{}` not found.'.format(
        self.category, module_name))
try:
    obj = getattr(module, obj_name)
except AttributeError:
    raise Exception('Plugin {}:{} module `{}` has no {}.'.format(
        self.category, self.name, module_name, obj_name))
```

`ImportError` can originate inside an existing plugin—for example, because one of its dependencies is missing or incompatible. This code then incorrectly claims that the plugin module itself was not found and discards the useful exception chain. It also raises generic `Exception` values that callers cannot classify.

**Suggested refactoring:**

```python
class PluginLoadError(Exception):
    """A configured plugin could not be loaded."""


def load(self):
    module_name, obj_name = self.location.split(':', 1)

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        if exc.name == module_name:
            raise PluginLoadError(
                f"Plugin {self.category} module {module_name!r} was not found."
            ) from exc
        raise PluginLoadError(
            f"Plugin {self.category}:{self.name} has a missing dependency: "
            f"{exc.name!r}."
        ) from exc
    except ImportError as exc:
        raise PluginLoadError(
            f"Plugin {self.category}:{self.name} failed during import."
        ) from exc

    try:
        return getattr(module, obj_name)
    except AttributeError as exc:
        raise PluginLoadError(
            f"Plugin {self.category}:{self.name} module {module_name!r} "
            f"has no attribute {obj_name!r}."
        ) from exc
```

**Why this matters:**

Accurate diagnostics substantially reduce plugin troubleshooting time. A dedicated exception also lets the CLI handle configuration errors without confusing them with internal failures.

**Rhodes’ principle:**

Use an exception hierarchy that preserves the reason for failure and lets callers respond at the appropriate level.

---

### 5. **SAFE-DEFAULT**: Empty command-line arguments can crash argument processing

**Locations:** `doit/doit_cmd.py:208-221`, `DoitMain.process_args`; `doit/loader.py:190-195`, `load_tasks`

**Current code:**

```python
for arg in cmd_args:
    if (arg[0] != '-') and ('=' in arg):
        name, value = arg.split('=', 1)
        set_var(name, value)
```

A similar unchecked index appears in task loading:

```python
for index, term in enumerate(args):
    if term[0] != '-':
        arg_pos[term] = index
```

An empty string is a valid process argument and can be produced by shell quoting or direct API use. Either path raises `IndexError` instead of treating it as positional input or returning a parse error.

**Suggested refactoring:**

```python
for arg in cmd_args:
    if arg and not arg.startswith('-') and '=' in arg:
        name, value = arg.split('=', 1)
        set_var(name, value)
    else:
        args_no_vars.append(arg)
```

```python
for index, term in enumerate(args):
    if term and not term.startswith('-'):
        arg_pos[term] = index
```

If empty task names are invalid, reject them explicitly with `CmdParseError` rather than indexing blindly.

**Why this matters:**

Malformed or unusual user input should produce a controlled diagnostic, not an internal traceback. The fix also makes the programmatic API safer.

**Rhodes’ principle:**

Safe APIs validate boundary input explicitly and fail in terms meaningful to their caller.

---

### 6. **SAFE-DEFAULT**: Configuration validation relies on an optimizable assertion

**Location:** `doit/doit_cmd.py:133-136`, `DoitConfig.load_config_toml`

**Current code:**

```python
for plugin_type, plugins in doit_toml.pop('plugins', {}).items():
    assert plugin_type in self.PLUGIN_TYPES
    toml_config[plugin_type.upper()] = plugins
```

Assertions disappear when Python runs with `-O`. Under optimization, an unsupported plugin category is accepted into the configuration and may then be silently ignored. Without optimization, users receive an `AssertionError`, which presents validatable configuration input as a programmer defect.

**Suggested refactoring:**

```python
for plugin_type, plugins in doit_toml.pop('plugins', {}).items():
    if plugin_type not in self.PLUGIN_TYPES:
        allowed = ', '.join(self.PLUGIN_TYPES)
        raise InvalidCommand(
            f"Unknown plugin type {plugin_type!r}; expected one of: {allowed}."
        )
    toml_config[plugin_type.upper()] = plugins
```

**Why this matters:**

Configuration behavior should not change with interpreter flags. An explicit domain exception also tells users exactly how to repair the file.

**Rhodes’ principle:**

Assertions document internal invariants; explicit validation protects boundaries controlled by users.

## Rhodes Wisdom

> “Move all I/O operations to the program’s top level, allowing core logic to remain pure and testable.”
>
> — *Hoisting Your I/O* (2015)
