# Python Code Review

## File: action.py

### LONG-METHOD-1
**Issue:** The `_prepare_kwargs` method is too long and complex (50+ lines, multiple responsibilities)

**Problematic Code:**
```python
@staticmethod
def _prepare_kwargs(task, func, args, kwargs):
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
        # ... 20+ more lines of complex logic
```

**Improved Code:**
```python
@staticmethod
def _prepare_kwargs(task, func, args, kwargs):
    if not task:
        return kwargs
    
    kwargs = kwargs.copy()
    kwargs = BaseAction._add_meta_arguments(task, func, args, kwargs)
    kwargs = BaseAction._add_option_arguments(task, func, args, kwargs)
    return kwargs

@staticmethod
def _add_meta_arguments(task, func, args, kwargs):
    """Add task meta information as keyword arguments"""
    func_sig = inspect.signature(func)
    bound_args = func_sig.bind_partial(*args)
    
    meta_args = {
        'task': lambda: task,
        'targets': lambda: list(task.targets),
        'dependencies': lambda: list(task.file_dep),
        'changed': lambda: list(task.dep_changed),
    }
    
    for key, value_func in meta_args.items():
        if BaseAction._should_add_argument(key, func_sig, bound_args, task):
            kwargs[key] = value_func()
    return kwargs

@staticmethod
def _should_add_argument(key, func_sig, bound_args, task):
    """Check if argument should be added to kwargs"""
    if key not in func_sig.parameters:
        return False
    
    sig_param = func_sig.parameters[key]
    if sig_param.default != sig_param.empty:
        msg = (f"Task {task.name}, action parameter '{key}' is not allowed "
               "to have a default value (reserved by doit)")
        raise InvalidTask(msg)
    
    return key not in bound_args.arguments
```

**Why this matters:** Single Responsibility Principle - each method should do one thing. Long methods are harder to test, understand, and maintain.

### STRING-FORMAT-1
**Issue:** Using old-style string formatting which can be unsafe and is deprecated

**Problematic Code:**
```python
if self.STRING_FORMAT == 'old':
    return self.action % subs_dict
elif self.STRING_FORMAT == 'new':
    return self.action.format(**subs_dict)
else:
    assert self.STRING_FORMAT == 'both'
    return self.action.format(**subs_dict) % subs_dict
```

**Improved Code:**
```python
if self.STRING_FORMAT == 'old':
    return self.action.format(**subs_dict)
elif self.STRING_FORMAT == 'new':
    return self.action.format(**subs_dict)
else:
    assert self.STRING_FORMAT == 'both'
    # Apply format twice for backwards compatibility
    formatted = self.action.format(**subs_dict)
    return formatted.format(**subs_dict)
```

**Why this matters:** Old-style `%` formatting can be vulnerable to format string attacks and is deprecated in favor of `.format()` or f-strings.

### MAGIC-NUMBER-1
**Issue:** Magic number 125 for process return codes without explanation

**Problematic Code:**
```python
# task error - based on:
# http://www.gnu.org/software/bash/manual/bashref.html#Exit-Status
# it doesnt make so much difference to return as Error or Failed anyway
if process.returncode > 125:
    return TaskError("Command error: '%s' returned %s" %
                     (action, process.returncode))
```

**Improved Code:**
```python
# Exit codes above 125 indicate system-level errors (bash manual)
SYSTEM_ERROR_THRESHOLD = 125

if process.returncode > SYSTEM_ERROR_THRESHOLD:
    return TaskError(f"Command error: '{action}' returned {process.returncode}")
```

**Why this matters:** Magic numbers make code harder to understand and maintain. Named constants provide clarity and make it easier to change values.

### BROAD-EXCEPT-1
**Issue:** Catching all exceptions without specific handling

**Problematic Code:**
```python
try:
    line = read().decode(self.encoding, self.decode_error)
except Exception:
    # happens when fails to decoded input
    process.terminate()
    input_.read()
    raise
```

**Improved Code:**
```python
try:
    line = read().decode(self.encoding, self.decode_error)
except (UnicodeDecodeError, OSError) as e:
    # Handle decoding failures and I/O errors
    process.terminate()
    input_.read()
    raise TaskError(f"Failed to decode process output: {e}") from e
```

**Why this matters:** Catching specific exceptions makes error handling more predictable and helps with debugging. Broad `except Exception` can mask unexpected errors.

### VALIDATION-1
**Issue:** Input validation using multiple `type()` checks instead of isinstance

**Problematic Code:**
```python
if type(self.args) is not tuple and type(self.args) is not list:
    msg = "%r args must be a 'tuple' or a 'list'. got '%s'."
    raise InvalidTask(msg % (self.task, self.args))
if type(self.kwargs) is not dict:
    msg = "%r kwargs must be a 'dict'. got '%s'"
    raise InvalidTask(msg % (self.task, self.kwargs))
```

**Improved Code:**
```python
if not isinstance(self.args, (tuple, list)):
    msg = f"{self.task!r} args must be a tuple or list, got {type(self.args).__name__}"
    raise InvalidTask(msg)
if not isinstance(self.kwargs, dict):
    msg = f"{self.task!r} kwargs must be a dict, got {type(self.kwargs).__name__}"
    raise InvalidTask(msg)
```

**Why this matters:** `isinstance()` is more Pythonic and handles inheritance correctly. Using f-strings is more readable than old-style formatting.

## File: runner.py

### LONG-METHOD-2
**Issue:** The `run_tasks` method in `MRunner` is too long and complex (80+ lines)

**Problematic Code:**
```python
def run_tasks(self, task_dispatcher):
    """controls subprocesses task dispatching and result collection
    """
    # result queue - result collected from sub-processes
    result_q = self.Queue()
    # task queue - tasks ready to be dispatched to sub-processes
    job_q = self.Queue()
    self._run_tasks_init(task_dispatcher)
    proc_list = self._run_start_processes(job_q, result_q)

    # wait for all processes terminate
    proc_count = len(proc_list)
    try:
        while proc_count:
            # ... 60+ more lines of complex logic
```

**Improved Code:**
```python
def run_tasks(self, task_dispatcher):
    """Controls subprocess task dispatching and result collection"""
    result_q = self.Queue()
    job_q = self.Queue()
    
    self._run_tasks_init(task_dispatcher)
    proc_list = self._run_start_processes(job_q, result_q)
    
    try:
        self._process_task_results(task_dispatcher, job_q, result_q, proc_list)
        self._collect_teardown_results(task_dispatcher, result_q)
    except (SystemExit, KeyboardInterrupt, Exception):
        self._terminate_processes(proc_list)
        raise
    finally:
        self._join_processes(proc_list)

def _process_task_results(self, task_dispatcher, job_q, result_q, proc_list):
    """Process results from worker processes"""
    proc_count = len(proc_list)
    while proc_count:
        result = result_q.get()
        
        if 'exit' in result:
            raise result['exit'](result['exception'])
            
        proc_count = self._handle_task_result(
            result, task_dispatcher, job_q, proc_count)
```

**Why this matters:** Long methods violate the Single Responsibility Principle and are harder to test and maintain. Breaking them into smaller, focused methods improves readability.

### UNUSED-IMPORT-1
**Issue:** Unused import that can be removed

**Problematic Code:**
```python
import pdb
# ... later in code, only used in pragma: no cover block
if self.pm_pdb:  # pragma: no cover
    # start post-mortem debugger
    deb = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
```

**Improved Code:**
```python
# Remove the import at the top, import only when needed
if self.pm_pdb:  # pragma: no cover
    import pdb
    deb = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
```

**Why this matters:** Unused imports clutter the namespace and can slow down module loading. Import modules only when needed.

### TYPE-HINTS-1
**Issue:** Missing type annotations throughout both files

**Problematic Code:**
```python
def normalize_callable(ref):
    """return a list with (callable, *args, **kwargs)
    ref can be a simple callable or a tuple
    """
```

**Improved Code:**
```python
from typing import Union, Callable, Tuple, List, Any, Dict

def normalize_callable(ref: Union[Callable, Tuple[Callable, ...]]) -> List[Any]:
    """Return a list with (callable, *args, **kwargs)
    
    Args:
        ref: A simple callable or a tuple containing callable and arguments
        
    Returns:
        List containing [callable, args, kwargs]
    """
```

**Why this matters:** Type hints improve code documentation, help catch errors early with static analysis tools, and make the code more maintainable.

### MUTABLE-DEFAULT-1
**Issue:** Not technically present but good to watch for - properly handled in PythonAction constructor

**Good Code Example:**
```python
def __init__(self, py_callable, args=None, kwargs=None, task=None):
    if args is None:
        self.args = []
    else:
        self.args = args

    if kwargs is None:
        self.kwargs = {}
    else:
        self.kwargs = kwargs
```

**Why this matters:** This code correctly avoids mutable default arguments, which is a common Python pitfall. The pattern shown is the correct way to handle optional mutable parameters.
