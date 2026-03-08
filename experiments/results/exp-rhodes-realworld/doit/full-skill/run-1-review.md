## Review: action.py and runner.py

### ✅ Strengths
- **EXPLICIT-NAME**: Good use of descriptive method names like `execute_task()`, `process_task_result()`
- **DICT-COMP**: Proper use of dictionary operations in several places
- **EXCEPT-HIER**: Good custom exception hierarchy with `TaskError`, `TaskFailed`, etc.

### ⚠️ Suggestions

#### HOIST-IO: I/O operations deeply embedded in business logic

**Current code:**
```python
def execute(self, out=None, err=None):
    """Execute command action"""
    # ... business logic mixed with I/O ...
    
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
        # ... more I/O handling mixed with result processing
```

**Suggested refactoring:**
```python
def execute(self, out=None, err=None):
    """Execute command action - pure coordination"""
    try:
        action = self.expand_action()
        process_config = self._build_process_config()
        execution_result = self._run_subprocess(action, process_config)
        return self._evaluate_result(execution_result)
    except Exception as exc:
        return TaskError("CmdAction Error creating command string", exc)

def _run_subprocess(self, action, config):
    """Pure subprocess execution - all I/O isolated here"""
    process = subprocess.Popen(action, **config)
    if self.should_capture_io():
        return self._capture_output(process)
    else:
        return self._direct_output(process)
```

**Why this matters:**
The current `execute()` method mixes subprocess management, threading, I/O redirection, and result evaluation. This makes testing difficult - you need to mock subprocess, threads, and file I/O simultaneously. Separating concerns allows testing the business logic (result evaluation) with simple data structures.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic to remain pure and testable."

---

#### FUNC-SHELL: Mixed imperative shell with functional core

**Current code:**
```python
def execute(self, out=None, err=None):
    """Execute command action - 80+ lines mixing concerns"""
    capture_io = self.task.io.capture if self.task else True
    
    if capture_io:
        # set std stream redirection
        old_stdout = sys.stdout
        output = StringIO()
        # ... 20 lines of I/O setup
        
    kwargs = self._prepare_kwargs()
    
    try:
        returned_value = self.py_callable(*self.args, **kwargs)
        # ... 30 lines of result processing mixed with I/O cleanup
```

**Suggested refactoring:**
```python
def execute(self, out=None, err=None):
    """Imperative shell - coordinates I/O"""
    kwargs = self._prepare_kwargs()
    
    with self._capture_streams(out, err) as captured:
        result = self._execute_callable(kwargs)
        output_data = captured.get_output()
    
    return self._process_execution_result(result, output_data)

def _execute_callable(self, kwargs):
    """Functional core - pure callable execution"""
    return self.py_callable(*self.args, **kwargs)

def _process_execution_result(self, returned_value, output_data):
    """Functional core - pure result evaluation"""
    if returned_value is False:
        return TaskFailed(f"Python Task failed: '{self.py_callable}' returned {returned_value}")
    elif isinstance(returned_value, dict):
        return {'values': returned_value, 'result': returned_value}
    # ... other pure transformations
```

**Why this matters:**
The current approach makes it impossible to test the result processing logic without setting up complex I/O mocking. The functional core becomes easily testable with simple assertions, while the imperative shell handles only the I/O coordination.

**Rhodes' principle:**
"Separate code into a functional core (pure functions) and imperative shell (procedures with I/O)."

---

#### INDENT-LIMIT: Deep nesting exceeds readability threshold

**Current code:**
```python
def run_tasks(self, task_dispatcher):
    """controls subprocesses task dispatching and result collection"""
    # ... setup code
    try:
        while proc_count:
            result = result_q.get()
            if 'exit' in result:
                raise result['exit'](result['exception'])
            node = task_dispatcher.nodes[result['name']]
            task = node.task
            if 'reporter' in result:
                getattr(self.reporter, result['reporter'])(task)
                continue
            self._process_result(node, task, result)
            # ... more nested logic
            for _ in range(free_proc):
                next_job = self.get_next_job(completed)
                if next_job is None:
                    proc_count -= 1
                job_q.put(next_job)
    except (SystemExit, KeyboardInterrupt, Exception):
        # ... cleanup
```

**Suggested refactoring:**
```python
def run_tasks(self, task_dispatcher):
    """controls subprocesses task dispatching and result collection"""
    result_q, job_q, proc_list = self._initialize_multiprocessing(task_dispatcher)
    proc_count = len(proc_list)
    
    try:
        while proc_count:
            result = result_q.get()
            proc_count = self._handle_subprocess_result(result, task_dispatcher, job_q, proc_count)
    except (SystemExit, KeyboardInterrupt, Exception):
        self._cleanup_processes(proc_list)
        raise
    
    self._join_processes(proc_list)
    self._collect_teardown_results(result_q, task_dispatcher)

def _handle_subprocess_result(self, result, task_dispatcher, job_q, proc_count):
    """Handle single subprocess result - reduced nesting"""
    if 'exit' in result:
        raise result['exit'](result['exception'])
    
    if 'reporter' in result:
        self._handle_reporter_message(result, task_dispatcher)
        return proc_count
    
    return self._handle_task_completion(result, task_dispatcher, job_q, proc_count)
```

**Why this matters:**
Deep nesting makes code hard to follow and test. Each level of indentation represents another mental context switch. Breaking into smaller, focused methods makes the logic clearer and each piece independently testable.

**Rhodes' principle:**
"If you need more than 3 levels of indentation, you're screwed anyway. Use continue statements, method extraction, function factoring, iterator separation."

---

#### PRECISE-NOUN: Vague variable names obscure intent

**Current code:**
```python
def _prepare_kwargs(task, func, args, kwargs):
    # ... complex logic ...
    meta_args = {
        'task': lambda: task,
        'targets': lambda: list(task.targets),
        'dependencies': lambda: list(task.file_dep),
        'changed': lambda: list(task.dep_changed),
    }
    
    kwargs = kwargs.copy()  # What kind of kwargs? From where?
    bound_args = func_sig.bind_partial(*args)  # What args? Function args? Task args?
```

**Suggested refactoring:**
```python
def _prepare_kwargs(task, func, user_args, user_kwargs):
    """Prepare kwargs by merging user args with task metadata"""
    task_metadata = {
        'task': lambda: task,
        'targets': lambda: list(task.targets), 
        'dependencies': lambda: list(task.file_dep),
        'changed': lambda: list(task.dep_changed),
    }
    
    merged_kwargs = user_kwargs.copy()
    bound_user_args = func_sig.bind_partial(*user_args)
    
    # Add task metadata that function signature expects
    for metadata_key in task_metadata.keys():
        if self._should_inject_metadata(func_sig, metadata_key, bound_user_args):
            merged_kwargs[metadata_key] = task_metadata[metadata_key]()
```

**Why this matters:**
Variable names like `kwargs`, `args`, `data`, `result` create a "type desert" where the reader can't understand what data flows where. Precise names like `user_kwargs`, `task_metadata`, `execution_result` make the code self-documenting.

**Rhodes' principle:**
"Nouns should precisely describe objects. When discovering imprecise variable name, refactor throughout."

---

#### NO-GLOBAL-MUT: Mutable class attributes create coupling

**Current code:**
```python
class PythonAction(BaseAction):
    pm_pdb = False  # Global mutable state shared across instances
    
    def execute(self, out=None, err=None):
        # ...
        except Exception as exception:
            if self.pm_pdb:  # Global state affects behavior
                deb = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
```

**Suggested refactoring:**
```python
class PythonAction(BaseAction):
    def __init__(self, py_callable, args=None, kwargs=None, task=None, debug_mode=False):
        # ... existing init ...
        self.debug_mode = debug_mode  # Instance-specific setting
    
    def execute(self, out=None, err=None):
        # ...
        except Exception as exception:
            if self.debug_mode:  # Instance state, not global
                deb = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)

# Usage - explicit configuration
action = PythonAction(my_func, debug_mode=True)
```

**Why this matters:**
Class-level mutable attributes create hidden coupling between instances. Tests become unpredictable because one test can change global state that affects others. Instance-specific configuration makes behavior explicit and testable.

**Rhodes' principle:**
"Mutable globals create dangerous coupling between distant code sections."

---

#### TOP-DOWN: Code organization doesn't follow natural reading flow

**Current code:**
```python
class CmdAction(BaseAction):
    def __init__(self, action, task=None, save_out=None, ...):
        # Constructor first
    
    @property
    def action(self):
        # Property in middle
        
    def _print_process_output(self, process, input_, capture, realtime):
        # Helper method before main method
        
    def execute(self, out=None, err=None):
        # Main method last
```

**Suggested refactoring:**
```python
class CmdAction(BaseAction):
    def __init__(self, action, task=None, save_out=None, ...):
        # Constructor first
        
    def execute(self, out=None, err=None):
        # Main public method next - what users care about
        
    def expand_action(self):
        # Public utilities second
        
    def _print_process_output(self, process, input_, capture, realtime):
        # Private helpers last
        
    @property 
    def action(self):
        # Properties at end
```

**Why this matters:**
Readers want to understand the main purpose first, then drill down to implementation details. Putting helpers before main methods forces readers to understand implementation before seeing the interface.

**Rhodes' principle:**
"Organize code naturally with main logic first, helpers after (not inverted like C requires)."

### 💡 Rhodes Wisdom
> "Separation of Concerns: Keep I/O separate from business logic. Pure Functions: Prefer pure functions that are easy to test. If you consider patch() an anti-pattern in production code—why are you doing it in your tests?"
> — The Clean Architecture in Python (2014)
