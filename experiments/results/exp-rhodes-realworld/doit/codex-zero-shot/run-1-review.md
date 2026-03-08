## Findings (highest severity first)

### 1. `KWARG_OVERRIDE_INJECTION`
Location: [action.py:79](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/action.py#L79)

**Problematic code**
```python
if key not in bound_args.arguments:
    kwargs[key] = meta_args[key]()

...

if key in func_sig.parameters:
    if key not in bound_args.arguments:
        kwargs[key] = opt_args[key]
```

**Improved code**
```python
if key in func_sig.parameters and key not in bound_args.arguments and key not in kwargs:
    kwargs[key] = meta_args[key]()

...

if key in func_sig.parameters:
    if key not in bound_args.arguments and key not in kwargs:
        kwargs[key] = opt_args[key]
elif func_has_kwargs and key not in kwargs:
    kwargs[key] = opt_args[key]
```

**Why it matters**  
Current logic can overwrite user-provided kwargs, which is surprising and violates the method’s own “add missing arguments” contract.

---

### 2. `STD_STREAM_RESTORE_GAP`
Location: [action.py:469](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/action.py#L469)

**Problematic code**
```python
# stdout/stderr are already redirected above
kwargs = self._prepare_kwargs()

try:
    returned_value = self.py_callable(*self.args, **kwargs)
except Exception as exception:
    ...
finally:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
```

**Improved code**
```python
old_stdout, old_stderr = sys.stdout, sys.stderr
output = errput = None
try:
    # redirect stdout/stderr
    ...
    kwargs = self._prepare_kwargs()
    returned_value = self.py_callable(*self.args, **kwargs)
except Exception as exception:
    return TaskError("PythonAction Error", exception)
finally:
    sys.stdout, sys.stderr = old_stdout, old_stderr
    if capture_io and output is not None:
        self.out = output.getvalue()
        self.err = errput.getvalue()
```

**Why it matters**  
If `_prepare_kwargs()` raises, streams remain redirected globally, breaking later output and making failures hard to debug.

---

### 3. `CALLABLE_ACTION_REEVALUATED`
Location: [action.py:283](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/action.py#L283)

**Problematic code**
```python
if isinstance(self.action, list):
    for element in self.action:
        ...
...
return self.action % subs_dict
```

**Improved code**
```python
action = self.action  # evaluate once

if isinstance(action, list):
    ...
    return normalized_action

if self.STRING_FORMAT == 'old':
    return action % subs_dict
elif self.STRING_FORMAT == 'new':
    return action.format(**subs_dict)
return action.format(**subs_dict) % subs_dict
```

**Why it matters**  
If `self._action` is callable, it may run multiple times per execution, causing side effects, inconsistent commands, or extra cost.

---

### 4. `DEVNULL_FILE_DESCRIPTOR_LEAK`
Location: [action.py:225](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/action.py#L225)

**Problematic code**
```python
p_out = p_err = open(os.devnull, "w")
```

**Improved code**
```python
p_out = p_err = subprocess.DEVNULL
```

**Why it matters**  
The opened handle is never closed. Repeated tasks can leak file descriptors.

---

### 5. `MREPORTER_SIGNATURE_MISMATCH`
Location: [runner.py:318](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/runner.py#L318), [runner.py:236](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/runner.py#L236)

**Problematic code**
```python
def rep_method(task):
    self.runner.result_q.put({'name': task.name, 'reporter': method_name})
```
```python
self.reporter.cleanup_error(error)
```

**Improved code**
```python
def rep_method(obj):
    payload = {'reporter': method_name}
    if hasattr(obj, "name"):
        payload['name'] = obj.name
    else:
        payload['error_msg'] = obj.get_msg()
    self.runner.result_q.put(payload)
```

**Why it matters**  
`cleanup_error` receives an exception object, not a task. Accessing `.name` can crash subprocess reporting during teardown failures.

---

### 6. `THREAD_RUNNER_DOUBLE_TEARDOWN`
Location: [runner.py:524](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/runner.py#L524), [runner.py:563](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/runner.py#L563)

**Problematic code**
```python
if job is None:
    self.teardown()
    return
```

**Improved code**
```python
if job is None:
    if self.Child == Process:
        self.teardown()   # per-process teardown
    return                # thread runner: teardown once in main finish()
```

**Why it matters**  
`MThreadRunner` shares the same runner instance across threads. Running teardown in each worker can duplicate cleanup and introduce races.

---

### 7. `ASSERT_USED_FOR_RUNTIME_VALIDATION`
Location: [runner.py:158](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/runner.py#L158), [runner.py:492](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/runner.py#L492)

**Problematic code**
```python
assert node.run_status == 'run'
...
assert len(proc_list) > self.free_proc
```

**Improved code**
```python
if node.run_status != 'run':
    raise RuntimeError(f"{task.name}:{node.run_status}")

if len(proc_list) <= self.free_proc:
    raise RuntimeError("Cyclic dependency or scheduler inconsistency detected")
```

**Why it matters**  
`assert` is stripped with `python -O`, removing critical safety checks in production runs.

---

### 8. `EXACT_TYPE_CHECKS`
Location: [action.py:417](/home/sankar/sankar/projects/claude-skills/experiments/repos/doit-repo/doit/action.py#L417)

**Problematic code**
```python
if type(self.args) is not tuple and type(self.args) is not list:
    ...
if type(self.kwargs) is not dict:
    ...
```

**Improved code**
```python
if not isinstance(self.args, (tuple, list)):
    ...
if not isinstance(self.kwargs, dict):
    ...
```

**Why it matters**  
Exact-type checks reject valid subclasses and are less idiomatic; `isinstance` is more robust and maintainable.

## Testing gaps to add
1. Regression test that explicit action kwargs are not overwritten by auto-injected task/meta args.
2. Test that `PythonAction.execute` always restores `sys.stdout`/`sys.stderr` when `_prepare_kwargs` fails.
3. Test teardown-failure reporting in multiprocessing mode (`cleanup_error` path).