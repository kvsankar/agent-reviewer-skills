## Review: doit Python Library

### ✅ Strengths
- **FUNC-SHELL**: The code follows functional core, imperative shell principle with clear separation of I/O operations from business logic in module loading and task execution.
- **HOIST-IO**: Core tasks processing uses HOIST-IO principle by managing I/O at the command level rather than deeply embedded in business logic functions.
- **LANG-PATTERN**: Uses Python built-in features like `collections.OrderedDict`, `inspect.isgenerator` instead of custom patterns, following "PYTHON-PATTERNS".
- **NO-MUTARGS**: Function parameters are not mutated in-place throughout the system.
- **DICT-COMP**: Clean dictionary comprehension usage where appropriate.

### ⚠️ Suggestions

#### PURE-TEST: Test functions that could run without IO dependencies don't use external files

**Current code:**
```python
def testProcessRun(self):
    output = StringIO()
    cmd_run = CmdFactory(Run, backend='dbm', dep_file=self.depfile_name,
                         task_list=tasks_sample(self.dependency1))
```
The testing approach still heavily uses temporary files and DB implementations.

**Suggested refactoring:**
```python
def testProcessRun(self):
    # Tests should be isolated from file I/O where possible
    with patch('doit.cmd_run.TaskControl') as mock_control:
        # Mock control to avoid file system interaction
        mock_control_instance = mock_control.return_value
        mock_control_instance.selected_tasks = ['t1', 't2']  # Mock task list

        output = StringIO()
        cmd_run = CmdFactory(Run)
        result = cmd_run._execute(output)
        # Verify the mocked results without real file creation etc.
```

**Why this matters:**
Tests should ideally be fast, isolated and repeatable. The current approach requires the temporary files that complicate running individual tests.

**Rhodes' principle:**
"Pure functions are easier to test and understand, so when you find yourself needing mocks for files or system resources, you might have architectural coupling."

---

#### NO-MOCK: Excessive reliance on mocking indicates architectural issues

**Current code:**
Looking at the cmd_run tests, they extensively use `patch` and other mock patterns to replace real I/O operations, particularly with:
```python
with patch.object(runner.MRunner, "available",
                          Mock(return_value=False)):
```

**Suggested refactoring:**
The test design should allow more of the logic to run through normal flow paths. Instead of mocking runner availability, consider creating test infrastructure that avoids the complex mocking entirely.

**Why this matters:**
If you need `patch()` to test your code, it signals that I/O is too tightly coupled with logic. This suggests architectural problems.

**Rhodes' principle:**
"If you consider patch() an anti-pattern in production code—why are you doing it in your tests? Mocking signals architectural problems."

---

#### FUNC-SHELL: Business logic isn't well separated from imperative shell

**Current code:**
In `doit_cmd.py`, I see a lot of imperative control flow:
```python
def run(self, all_args):
    # ... process args ...
    try:
        # ... many operations ...
        return command.parse_execute(args)
    except (CmdParseError, InvalidDodoFile,
            InvalidCommand, InvalidTask) as err:
        # ... error handling ...
```

**Suggested refactoring:**
The main `run` method should be broken down into smaller pure functions that handle specific pieces of logic and can be tested independently with fewer mocks.

```python
def run(self, all_args):
    """Entry point for command execution."""
    sub_cmds = self.get_cmds()
    task_loader = get_loader(self.config, self.task_loader, sub_cmds)

    # Handle special parameters first - pure function
    args_no_vars = self.process_args(all_args)

    # Determine command and parse arguments - pure function
    cmd_name, cmd_args = self._determine_command(args_no_vars, sub_cmds)

    # Create and execute command - imperitive shell with proper separation
    return self._execute_command(cmd_name, sub_cmds, task_loader, cmd_args)
```

**Why this matters:**
By separating imperative execution from the pure logic components, testing becomes more straightforward. The core argument parsing can be fully tested without external dependencies.

**Rhodes' principle:**
"Have a functional core and imperative shell - keep I/O at the top level where it's easier to test."

---

#### EXPLICIT-NAME: Some function names could be clearer

**Current code:**
```python
def flat_generator(gen, gen_doc=''):
```
**Suggested refactoring:**
```python
def _flatten_generator(gen, generator_doc=''):
    """Flattens a nested generator."""
    # implementation unchanged
```

**Why this matters:**
Using an underscore prefix makes clear this is an internal helper function and improves readability.

**Rhodes' principle:**
"Use verbs for functions that perform actions - explicit method naming makes code self-documenting."

---

#### PYTHON-PATTERNS: Inconsistent use of Python constructs vs custom patterns

Looking at the `TaskControl` class, `load_tasks` function, and other components, we can see good usage of built-in Python features:

- **DICT-COMP**: Good usage with comprehension patterns
- **LIST-FRONT**: No evidence of `list.insert(0, x)` causing performance issues in key places, which is good

But there are still some areas where patterns that could be simplified with Python features are not fully leveraged.

**Current code:**
In task handling logic around line 189 in `task.py`:
```python
if isinstance(target, str):
    targets.append(target)
elif isinstance(target, PurePath):
    targets.append(str(target))
```

**Suggested refactoring:**
Could be refactored to use a more Pythonic approach or even leverage existing pathlib conversion features in some cases.

**Why this matters:**
Reduced complexity and better alignment with established conventions improves code maintainability.

**Rhodes' principle:**
"Where Python provides powerful built-in constructs, don't recreate patterns that already exist."

---

### 💡 Rhodes Wisdom
> "Don't let the tools you know become the problem — if you find yourself using mock.patch() too often in tests, you’ve created coupling between your business logic and implementation details."
> — Functional Core / Imperative Shell (2018)

> "The goal isn't just to write code that works, but code that makes it easy to reason about and change when requirements evolve."
> — Clean Code vs. Clean Architecture (2017)
