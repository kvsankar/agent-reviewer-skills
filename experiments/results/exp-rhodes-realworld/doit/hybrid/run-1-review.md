## Review: action.py and runner.py

### ✅ Strengths
- **PRECISE-NOUN**: Good use of descriptive class names like `CmdAction`, `PythonAction`, and `BaseAction`
- **FUNC-SHELL**: Clear separation between different action types through inheritance
- **EXPLICIT-NAME**: Method names like `execute()`, `expand_action()`, and `normalize_callable()` clearly indicate their purpose

### ⚠️ Suggestions

#### HOIST-IO: I/O operations deeply embedded in business logic

**Current code:**
```python
def execute(self, out=None, err=None):
    # ... business logic mixed with I/O ...
    process = subprocess.Popen(
        action,
        shell=self.shell,
        stdout=p_out,
        stderr=p_err,
        env=env,
        **subprocess_pkwargs)
    
    if capture_io:
        output = StringIO()
        errput = StringIO()
        t_out = Thread(target=self._print_process_output,
                       args=(process, process.stdout, output, out))
        # ... more I/O operations mixed with logic
```

**Suggested refactoring:**
```python
def execute(self, out=None, err=None):
    """Execute command - delegates I/O to caller"""
    try:
        command_spec = self.prepare_command()
        return self._execute_command_spec(command_spec, out, err)
    except Exception as exc:
        return TaskError("CmdAction Error creating command string", exc)

def prepare_command(self):
    """Pure function - returns command specification"""
    action = self.expand_action()
    env = self._prepare_environment()
    return {
        'command': action,
        'shell': self.shell,
        'env': env,
        'capture': self.task.io.capture if self.task else True,
        **self.pkwargs
    }

def _execute_command_spec(self, spec, out, err):
    """I/O-heavy implementation separated from command preparation"""
    # All subprocess and threading logic here
```

**Why this matters:**
The current `execute()` method mixes command preparation (pure logic) with process execution (I/O). This makes testing difficult - you can't test command preparation without spawning processes. Separating these concerns allows testing command logic with simple assertions.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic to remain pure and testable."

---

#### NO-MOCK: Architecture forces excessive mocking in tests

**Current code:**
```python
class CmdAction:
    def execute(self, out=None, err=None):
        # ... subprocess.Popen called directly inside business logic
        process = subprocess.Popen(action, shell=self.shell, ...)
        # Testing this requires mocking subprocess.Popen
```

**Suggested refactoring:**
```python
def execute(self, out=None, err=None):
    """Execute using injected executor"""
    command_spec = self.prepare_command()
    return self.executor.run(command_spec, out, err)

# Test becomes mockless:
def test_command_preparation():
    action = CmdAction("echo hello")
    spec = action.prepare_command()
    assert spec['command'] == "echo hello"
    assert spec['shell'] == True
```

**Why this matters:**
Current architecture requires `patch('subprocess.Popen')` to test command execution. This signals that I/O is too tightly coupled with logic. The architectural fix (dependency injection + pure functions) eliminates mocking entirely.

**Rhodes' principle:**
"If you need patch() to test your code, it signals that I/O is too tightly coupled with logic. Architecture should make tests mockless."

---

#### FUNC-TEST: Complex class-based testing structure

**Current code:**
```python
# Current classes require complex test setup
class CmdAction(BaseAction):
    def __init__(self, action, task=None, save_out=None, shell=True, ...):
        # Many parameters, complex state
    def execute(self, out=None, err=None):
        # Complex method with many responsibilities
```

**Suggested refactoring:**
```python
# Break into testable functions
def prepare_command_args(action, shell, env_vars):
    """Pure function - easy to test"""
    return {
        'command': action,
        'shell': shell,
        'env': env_vars
    }

def expand_command_template(template, substitutions):
    """Pure function - easy to test"""
    return template % substitutions

# Tests become simple functions
def test_prepare_command_args():
    result = prepare_command_args("echo", True, {"VAR": "value"})
    assert result['shell'] == True
    assert result['env']['VAR'] == "value"
```

**Why this matters:**
Classes with complex `__init__` and multiple responsibilities require elaborate test setup. Breaking functionality into pure functions enables simple, focused tests without object construction complexity.

**Rhodes' principle:**
"Use function-based tests instead of class-based tests to avoid unnecessary boilerplate and maintain clarity."

---

#### PRECISE-NOUN: Vague variable names obscure intent

**Current code:**
```python
p_out = p_err = subprocess.PIPE
# ... later ...
t_out = Thread(target=self._print_process_output, ...)
t_err = Thread(target=self._print_process_output, ...)
```

**Suggested refactoring:**
```python
stdout_pipe = stderr_pipe = subprocess.PIPE
# ... later ...
stdout_capture_thread = Thread(target=self._capture_process_output, ...)
stderr_capture_thread = Thread(target=self._capture_process_output, ...)
```

**Why this matters:**
`p_out` and `t_out` are type deserts - readers must investigate to understand what these variables represent. Explicit names make the code self-documenting and reduce cognitive load.

**Rhodes' principle:**
"Nouns should precisely describe objects. When discovering imprecise variable name, refactor throughout."

---

#### TOP-DOWN: Methods read bottom-up due to helper placement

**Current code:**
```python
class CmdAction:
    def execute(self, out=None, err=None):
        # Main logic references _print_process_output first
        t_out = Thread(target=self._print_process_output, ...)
    
    def _print_process_output(self, process, input_, capture, realtime):
        # Helper method defined after main method
```

**Suggested refactoring:**
```python
class CmdAction:
    def execute(self, out=None, err=None):
        """Main entry point - reads top to bottom"""
        command_spec = self.prepare_command()
        if self.should_capture_output():
            return self._execute_with_capture(command_spec, out, err)
        else:
            return self._execute_direct(command_spec, out, err)
    
    def prepare_command(self):
        """First helper - command preparation logic"""
        # Implementation here
    
    def should_capture_output(self):
        """Second helper - decision logic"""
        # Implementation here
```

**Why this matters:**
Current organization forces readers to jump around to understand flow. Organizing code with main logic first, then helpers in order of use, creates natural reading flow.

**Rhodes' principle:**
"Organize code naturally with main logic first, helpers after (not inverted like C requires)."

---

#### CONTROL-CALLER: Methods assume too much about output handling

**Current code:**
```python
def execute(self, out=None, err=None):
    # Method decides how to handle all output scenarios
    if capture_io:
        output = StringIO()
        # ... complex threading logic
    else:
        if capture_io is False:
            p_out = out
            p_err = err
        else:  # None
            p_out = p_err = open(os.devnull, "w")
```

**Suggested refactoring:**
```python
def execute(self, output_handler=None):
    """Accept strategy object for output handling"""
    command_spec = self.prepare_command()
    if not output_handler:
        output_handler = DefaultOutputHandler()
    return output_handler.execute_command(command_spec)

# Callers control output behavior
action.execute(ThreadedCaptureHandler(out, err))
action.execute(DirectOutputHandler(out, err))
action.execute(NullOutputHandler())
```

**Why this matters:**
Current method tries to handle every possible output scenario internally. This creates complexity and reduces flexibility. Returning control to the caller through strategy objects simplifies the core logic and increases reusability.

**Rhodes' principle:**
"Return control to the caller rather than trying to solve all downstream problems."

---

#### NO-GLOBAL-MUT: Implicit global state manipulation

**Current code:**
```python
def execute(self, out=None, err=None):
    # Modifies global sys.stdout/stderr
    old_stdout = sys.stdout
    sys.stdout = out_writer
    # ... execute code that might fail ...
    sys.stdout = old_stdout  # Restore in finally
```

**Suggested refactoring:**
```python
def execute_with_redirected_streams(self, stdout=None, stderr=None):
    """Explicitly manage stream context"""
    with StreamRedirector(stdout, stderr) as redirector:
        return self._execute_callable(redirector.streams)

class StreamRedirector:
    def __init__(self, stdout=None, stderr=None):
        self.new_stdout = stdout
        self.new_stderr = stderr
        
    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        if self.new_stdout:
            sys.stdout = self.new_stdout
        if self.new_stderr:
            sys.stderr = self.new_stderr
        return self
        
    def __exit__(self, *args):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
```

**Why this matters:**
Direct manipulation of `sys.stdout/stderr` creates invisible global state changes that affect the entire process. Context managers make the state changes explicit and ensure proper cleanup even on exceptions.

**Rhodes' principle:**
"Global mutable state creates problems: testing requires mutating globals, threading causes race conditions, unclear data provenance."

---

#### KEY-SHARE: Missed optimization opportunity in object creation

**Current code:**
```python
class CmdAction(BaseAction):
    def __init__(self, action, task=None, save_out=None, shell=True,
                 encoding='utf-8', decode_error='replace', buffering=0,
                 **pkwargs):
        # Attributes assigned conditionally and in different methods
        self._action = action
        self.task = task
        # ... some attributes assigned later in other methods
```

**Suggested refactoring:**
```python
class CmdAction(BaseAction):
    def __init__(self, action, task=None, save_out=None, shell=True,
                 encoding='utf-8', decode_error='replace', buffering=0,
                 **pkwargs):
        # Assign ALL possible attributes in __init__ for memory efficiency
        self._action = action
        self.task = task
        self.out = None
        self.err = None
        self.result = None
        self.values = {}
        self.save_out = save_out
        self.shell = shell
        self.encoding = encoding
        self.decode_error = decode_error
        self.pkwargs = pkwargs
        self.buffering = buffering
```

**Why this matters:**
Python 3.3+ shares common key structures across instances when all attributes are assigned in `__init__()`, reducing memory usage by ~2/3. Conditional attribute assignment breaks this optimization.

**Rhodes' principle:**
"Assign every possible attribute in `__init__()` for maximum memory efficiency."

---

#### EXCEPT-HIER: Scattered exception handling without hierarchy

**Current code:**
```python
# Scattered try/except blocks throughout
try:
    line = read().decode(self.encoding, self.decode_error)
except Exception:
    process.terminate()
    input_.read()
    raise

# Different exception handling in another method
except Exception as exception:
    if self.pm_pdb:
        # start post-mortem debugger
    return TaskError("PythonAction Error", exception)
```

**Suggested refactoring:**
```python
# Define clear exception hierarchy
class ActionError(Exception):
    """Base for all action errors"""
    pass

class CommandExecutionError(ActionError):
    """Command execution failures"""
    pass

class OutputCaptureError(ActionError):
    """Output capture failures"""
    pass

# Use hierarchy consistently
def _capture_process_output(self, process, input_, capture, realtime):
    try:
        line = read().decode(self.encoding, self.decode_error)
    except UnicodeDecodeError as e:
        raise OutputCaptureError(f"Failed to decode process output: {e}")
    except Exception as e:
        process.terminate()
        raise CommandExecutionError(f"Process capture failed: {e}")
```

**Why this matters:**
Scattered exception handling creates inconsistent error reporting and makes it difficult to handle different failure types appropriately. A clear hierarchy allows callers to catch specific error types and respond accordingly.

**Rhodes' principle:**
"Define custom exception hierarchy and use consistent error handlers to eliminate error-checking code from business logic."

### 💡 Rhodes Wisdom
> "Separation of Concerns: Keep I/O separate from business logic. Pure Functions: Prefer pure functions that are easy to test. If you consider patch() an anti-pattern in production code—why are you doing it in your tests?"
> — The Clean Architecture in Python (2014) & Hoisting Your I/O (2015)
