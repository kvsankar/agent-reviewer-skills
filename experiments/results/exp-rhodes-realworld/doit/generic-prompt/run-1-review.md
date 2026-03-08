# Python Code Review

## Critical Issues

### 1. **LONG-METHOD** - BaseAction._prepare_kwargs
**Current Code:**
```python
@staticmethod
def _prepare_kwargs(task, func, args, kwargs):
    """
    Prepare keyword arguments (targets, dependencies, changed,
    cmd line options)
    Inspect python callable and add missing arguments:
    - that the callable expects
    - have not been passed (as a regular arg or as keyword arg)
    - are available internally through the task object
    """
    # Return just what was passed in task generator
    # dictionary if the task isn't available
    if not task:
        return kwargs

    func_sig = inspect.signature(func)
    sig_params = func_sig.parameters.values()
    func_has_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig_params)

    # use task meta information as extra_args
    meta_args = {
        'task': lambda: task,
        'targets': lambda: list(task.targets),
        'dependencies': lambda: list(task.file_dep),
        'changed': lambda: list(task.dep_changed),
    }

    # start with dict passed together on action definition
    kwargs = kwargs.copy()
    bound_args = func_sig.bind_partial(*args)

    # add meta_args
    for key in meta_args.keys():
        # check key is a positional parameter
        if key in func_sig.parameters:
            sig_param = func_sig.parameters[key]

            # it is forbidden to use default values for this arguments
            # because the user might be unaware of this magic.
            if (sig_param.default != sig_param.empty):
                msg = (f"Task {task.name}, action {func.__name__}():"
                       f"The argument '{key}' is not allowed to have "
                       "a default value (reserved by doit)")
                raise InvalidTask(msg)

            # if value not taken from position parameter
            if key not in bound_args.arguments:
                kwargs[key] = meta_args[key]()

    # add tasks parameter options
    opt_args = dict(task.options)
    if task.pos_arg is not None:
        opt_args[task.pos_arg] = task.pos_arg_val

    for key in opt_args.keys():
        # check key is a positional parameter
        if key in func_sig.parameters:
            # if value not taken from position parameter
            if key not in bound_args.arguments:
                kwargs[key] = opt_args[key]

        # if function has **kwargs include extra_arg on it
        elif func_has_kwargs and key not in kwargs:
            kwargs[key] = opt_args[key]
    return kwargs
```

**Improved Version:**
```python
@staticmethod
def _prepare_kwargs(task, func, args, kwargs):
    """Prepare keyword arguments for task execution."""
    if not task:
        return kwargs
    
    kwargs_builder = _KwargsBuilder(task, func, args, kwargs)
    return kwargs_builder.build()

class _KwargsBuilder:
    """Builds kwargs for task execution with proper separation of concerns."""
    
    def __init__(self, task, func, args, kwargs):
        self.task = task
        self.func_sig = inspect.signature(func)
        self.kwargs = kwargs.copy()
        self.bound_args = self.func_sig.bind_partial(*args)
        self._meta_args = {
            'task': lambda: task,
            'targets': lambda: list(task.targets),
            'dependencies': lambda: list(task.file_dep),
            'changed': lambda: list(task.dep_changed),
        }
    
    def build(self):
        """Build the final kwargs dictionary."""
        self._add_meta_args()
        self._add_task_options()
        return self.kwargs
    
    def _add_meta_args(self):
        """Add meta arguments from task."""
        for key, value_func in self._meta_args.items():
            if self._should_add_meta_arg(key):
                self.kwargs[key] = value_func()
    
    def _should_add_meta_arg(self, key):
        """Check if meta argument should be added."""
        if key not in self.func_sig.parameters:
            return False
        
        sig_param = self.func_sig.parameters[key]
        if sig_param.default != sig_param.empty:
            msg = (f"Task {self.task.name}, action {self.func.__name__}(): "
                   f"Argument '{key}' cannot have default value (reserved by doit)")
            raise InvalidTask(msg)
        
        return key not in self.bound_args.arguments
    
    def _add_task_options(self):
        """Add task options to kwargs."""
        opt_args = dict(self.task.options)
        if self.task.pos_arg is not None:
            opt_args[self.task.pos_arg] = self.task.pos_arg_val
        
        func_has_kwargs = any(p.kind == p.VAR_KEYWORD 
                             for p in self.func_sig.parameters.values())
        
        for key, value in opt_args.items():
            if key in self.func_sig.parameters:
                if key not in self.bound_args.arguments:
                    self.kwargs[key] = value
            elif func_has_kwargs and key not in self.kwargs:
                self.kwargs[key] = value
```

**Principle:** Single Responsibility Principle - Extract complex logic into a dedicated class with focused methods.

### 2. **GOD-CLASS** - CmdAction.execute Method
**Current Code:**
```python
def execute(self, out=None, err=None):
    """Execute command action"""
    try:
        action = self.expand_action()
    except Exception as exc:
        return TaskError("CmdAction Error creating command string", exc)

    # set environ to change output buffering
    subprocess_pkwargs = self.pkwargs.copy()
    env = None
    if 'env' in subprocess_pkwargs:
        env = subprocess_pkwargs['env']
        del subprocess_pkwargs['env']
    if self.buffering:
        if not env:
            env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

    capture_io = self.task.io.capture if self.task else True
    if capture_io:
        p_out = p_err = subprocess.PIPE
    else:
        if capture_io is False:
            p_out = out
            p_err = err
        else:  # None
            p_out = p_err = open(os.devnull, "w")

    # spawn task process
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
        t_err = Thread(target=self._print_process_output,
                       args=(process, process.stderr, errput, err))
        t_out.start()
        t_err.start()
        t_out.join()
        t_err.join()

        self.out = output.getvalue()
        self.err = errput.getvalue()
        self.result = self.out + self.err

    # make sure process really terminated
    process.wait()

    # task error - based on:
    # http://www.gnu.org/software/bash/manual/bashref.html#Exit-Status
    if process.returncode > 125:
        return TaskError("Command error: '%s' returned %s" %
                         (action, process.returncode))

    # task failure
    if process.returncode != 0:
        return TaskFailed("Command failed: '%s' returned %s" %
                          (action, process.returncode))

    # save stdout in values
    if self.save_out:
        self.values[self.save_out] = self.out
```

**Improved Version:**
```python
def execute(self, out=None, err=None):
    """Execute command action."""
    try:
        action = self.expand_action()
    except Exception as exc:
        return TaskError("CmdAction Error creating command string", exc)
    
    executor = _ProcessExecutor(self, out, err)
    return executor.execute(action)

class _ProcessExecutor:
    """Handles subprocess execution with proper I/O management."""
    
    def __init__(self, cmd_action, out_stream, err_stream):
        self.cmd_action = cmd_action
        self.out_stream = out_stream
        self.err_stream = err_stream
    
    def execute(self, action):
        """Execute the command and return result."""
        env = self._prepare_environment()
        stdout, stderr = self._prepare_streams()
        
        process = subprocess.Popen(
            action,
            shell=self.cmd_action.shell,
            stdout=stdout,
            stderr=stderr,
            env=env,
            **self.cmd_action.pkwargs
        )
        
        if self._should_capture_io():
            self._capture_output(process)
        
        process.wait()
        return self._process_result(process, action)
    
    def _prepare_environment(self):
        """Prepare environment variables."""
        env = None
        if 'env' in self.cmd_action.pkwargs:
            env = self.cmd_action.pkwargs['env'].copy()
        
        if self.cmd_action.buffering:
            if not env:
                env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
        
        return env
    
    def _prepare_streams(self):
        """Prepare stdout and stderr streams."""
        if self._should_capture_io():
            return subprocess.PIPE, subprocess.PIPE
        
        capture_io = self.cmd_action.task.io.capture if self.cmd_action.task else True
        if capture_io is False:
            return self.out_stream, self.err_stream
        
        return open(os.devnull, "w"), open(os.devnull, "w")
    
    def _should_capture_io(self):
        """Check if I/O should be captured."""
        return self.cmd_action.task.io.capture if self.cmd_action.task else True
    
    def _capture_output(self, process):
        """Capture process output using threads."""
        output, errput = StringIO(), StringIO()
        
        t_out = Thread(target=self.cmd_action._print_process_output,
                       args=(process, process.stdout, output, self.out_stream))
        t_err = Thread(target=self.cmd_action._print_process_output,
                       args=(process, process.stderr, errput, self.err_stream))
        
        t_out.start()
        t_err.start()
        t_out.join()
        t_err.join()
        
        self.cmd_action.out = output.getvalue()
        self.cmd_action.err = errput.getvalue()
        self.cmd_action.result = self.cmd_action.out + self.cmd_action.err
    
    def _process_result(self, process, action):
        """Process the execution result and return appropriate status."""
        if process.returncode > 125:
            return TaskError(f"Command error: '{action}' returned {process.returncode}")
        
        if process.returncode != 0:
            return TaskFailed(f"Command failed: '{action}' returned {process.returncode}")
        
        if self.cmd_action.save_out:
            self.cmd_action.values[self.cmd_action.save_out] = self.cmd_action.out
        
        return None
```

**Principle:** Single Responsibility Principle and Dependency Inversion - Extract complex subprocess handling logic.

### 3. **PARAM-COUNT** - CmdAction Constructor
**Current Code:**
```python
def __init__(self, action, task=None, save_out=None, shell=True,
             encoding='utf-8', decode_error='replace', buffering=0,
             **pkwargs):
```

**Improved Version:**
```python
@dataclass
class CmdConfig:
    """Configuration for command execution."""
    shell: bool = True
    encoding: str = 'utf-8'
    decode_error: str = 'replace'
    buffering: int = 0
    save_out: Optional[str] = None

class CmdAction(BaseAction):
    def __init__(self, action, task=None, config=None, **pkwargs):
        """Initialize command action with configuration object."""
        for forbidden in ('stdout', 'stderr'):
            if forbidden in pkwargs:
                raise InvalidTask(f"CmdAction can't take param named '{forbidden}'.")
        
        self._action = action
        self.task = task
        self.config = config or CmdConfig()
        self.pkwargs = pkwargs
        self._reset_state()
    
    def _reset_state(self):
        """Reset execution state."""
        self.out = None
        self.err = None
        self.result = None
        self.values = {}
    
    @property
    def shell(self):
        return self.config.shell
    
    @property
    def encoding(self):
        return self.config.encoding
    
    @property
    def decode_error(self):
        return self.config.decode_error
    
    @property
    def buffering(self):
        return self.config.buffering
    
    @property
    def save_out(self):
        return self.config.save_out
```

**Principle:** Parameter Object pattern - Reduce parameter count by grouping related parameters.

### 4. **OLD-FORMAT** - String Formatting
**Current Code:**
```python
return TaskError("Command error: '%s' returned %s" %
                 (action, process.returncode))
```

**Improved Version:**
```python
return TaskError(f"Command error: '{action}' returned {process.returncode}")
```

**Principle:** Modern Python idioms - Use f-strings for better readability and performance.

### 5. **MAGIC-NUM** - Hard-coded Return Codes
**Current Code:**
```python
if process.returncode > 125:
    return TaskError("Command error: '%s' returned %s" %
                     (action, process.returncode))
```

**Improved Version:**
```python
class ExitCodes:
    """Standard exit code constants."""
    SUCCESS = 0
    GENERAL_ERROR = 1
    MISUSE_SHELL_BUILTIN = 2
    COMMAND_ERROR_THRESHOLD = 125  # Bash manual reference

if process.returncode > ExitCodes.COMMAND_ERROR_THRESHOLD:
    return TaskError(f"Command error: '{action}' returned {process.returncode}")
```

**Principle:** Named constants improve readability and maintainability.

### 6. **MIXED-CONCERNS** - Runner Class
**Current Code:**
```python
class Runner():
    """Task runner"""
    def __init__(self, dep_manager, reporter, continue_=False,
                 always_execute=False, stream=None):
        # ... too many responsibilities mixed together
```

**Improved Version:**
```python
class TaskExecutor:
    """Handles individual task execution."""
    
    def execute_task(self, task, stream):
        """Execute a single task."""
        if task.teardown:
            # Register for cleanup
            pass
        return task.execute(stream)

class TaskSelector:
    """Handles task selection logic."""
    
    def should_execute(self, node, tasks_dict, dep_manager, always_execute):
        """Determine if task should be executed."""
        # Task selection logic here
        pass

class Runner:
    """Orchestrates task execution with clear separation of concerns."""
    
    def __init__(self, dep_manager, reporter, config):
        self.dep_manager = dep_manager
        self.reporter = reporter
        self.config = config
        self.task_executor = TaskExecutor()
        self.task_selector = TaskSelector()
        self.teardown_list = []
        self.final_result = SUCCESS
        self._stop_running = False
    
    def run_all(self, task_dispatcher):
        """Entry point with clear orchestration."""
        try:
            self._initialize(task_dispatcher)
            self._run_tasks(task_dispatcher)
        except InvalidTask as exception:
            self.reporter.runtime_error(str(exception))
            self.final_result = ERROR
        finally:
            return self._finish()
```

**Principle:** Single Responsibility Principle - Separate task execution, selection, and orchestration concerns.

## Medium Priority Issues

### 7. **USE-CONST** - Hardcoded Strings
**Current Code:**
```python
node.run_status = "failure"
node.run_status = "successful"
```

**Improved Version:**
```python
class TaskStatus:
    FAILURE = "failure"
    SUCCESSFUL = "successful"
    IGNORE = "ignore"
    RUN = "run"
    UP_TO_DATE = "up-to-date"

node.run_status = TaskStatus.FAILURE
node.run_status = TaskStatus.SUCCESSFUL
```

### 8. **BROAD-EXCEPT** - Generic Exception Handling
**Current Code:**
```python
try:
    returned_value = self.py_callable(*self.args, **kwargs)
except Exception as exception:
    # ... handle all exceptions the same way
```

**Improved Version:**
```python
try:
    returned_value = self.py_callable(*self.args, **kwargs)
except (TypeError, ValueError) as exc:
    return TaskError("PythonAction argument error", exc)
except KeyboardInterrupt:
    raise  # Let system interrupts propagate
except Exception as exc:
    return TaskError("PythonAction execution error", exc)
```

## Summary

The main issues are:
1. **Long methods** that violate Single Responsibility Principle
2. **God classes** with too many responsibilities
3. **High parameter counts** that make APIs hard to use
4. **Mixed concerns** making testing and maintenance difficult
5. **Old Python patterns** that reduce readability

The fixes focus on:
- **Extracting classes** for complex logic
- **Using configuration objects** to reduce parameter counts
- **Separating concerns** into focused responsibilities
- **Modern Python idioms** like f-strings and dataclasses
- **Named constants** for better maintainability
