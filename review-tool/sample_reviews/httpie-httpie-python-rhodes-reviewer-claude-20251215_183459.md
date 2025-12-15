# python-rhodes-reviewer Review

**Repository:** https://github.com/httpie/httpie
**Review Date:** 2025-12-15 18:34:59
**Reviewer:** python-rhodes-reviewer
**AI Provider:** claude

---

Based on my exploration of the HTTPie codebase, I can now provide a comprehensive code review following Brandon Rhodes' principles. I've analyzed the core architecture, key modules, testing patterns, and identified several areas that could be improved according to Rhodes' guidelines.

## Review: HTTPie Python Codebase

### ✅ Strengths

- **NAMED-TUPLE**: Excellent use of named tuples for structured data like `ProcessingOptions` and `OutputOptions` (httpie/models.py)
- **DICT-COMP**: Good use of dictionary comprehensions throughout the codebase (httpie/config.py:120, httpie/sessions.py:65)
- **EXPLICIT-NAME**: Method names clearly indicate their purpose (`collect_messages`, `write_message`, `process_request_body`)
- **MODULE-CONST**: Well-defined module-level constants like `DEFAULT_UA`, `JSON_CONTENT_TYPE` (httpie/client.py:34-36)

### ⚠️ Suggestions

#### HOIST-IO: I/O operations mixed with business logic

**Current code (httpie/config.py:103-108):**
```python
def load(self):
    config_type = type(self).__name__.lower()
    data = read_raw_config(config_type, self.path)
    if data is not None:
        data = self.pre_process_data(data)
        self.update(data)
```

**Current code (httpie/config.py:110-130):**
```python
def save(self, *, bump_version: bool = False):
    self.setdefault('__meta__', {})
    if bump_version or 'httpie' not in self['__meta__']:
        self['__meta__']['httpie'] = __version__
    # ... processing logic ...
    self.path.write_text(json_string + '\n', encoding=UTF8)
```

**Suggested refactoring:**
```python
def load_from_data(self, data):
    """Pure function to load config from data."""
    if data is not None:
        data = self.pre_process_data(data)
        self.update(data)

def save_data(self, *, bump_version: bool = False):
    """Pure function to prepare config data for saving."""
    data = self.copy()
    data.setdefault('__meta__', {})
    if bump_version or 'httpie' not in data['__meta__']:
        data['__meta__']['httpie'] = __version__
    return json.dumps(
        obj=self.post_process_data(data),
        indent=4, sort_keys=True, ensure_ascii=True
    )

# Caller handles I/O at top level
def load_config(config_path):
    data = read_raw_config(config_type, config_path)
    config = Config()
    config.load_from_data(data)
    return config
```

**Why this matters:**
Separating I/O from data processing makes the config logic testable without file mocking. You can now test with simple dictionaries in memory, making tests faster and more reliable.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic to remain pure and testable."

---

#### NO-MOCK: Test uses excessive mocking indicating architectural issues

**Current code (tests/test_auth.py:41-47):**
```python
@mock.patch('httpie.cli.argtypes.AuthCredentials._getpass',
            new=lambda self, prompt: 'password')
def test_password_prompt(httpbin):
    r = http('--auth', 'user',
             'GET', httpbin + '/basic-auth/user/password')
    assert HTTP_OK in r
    assert r.json == {'authenticated': True, 'user': 'user'}
```

**Current code (tests/test_auth.py:97-98):**
```python
with mock.patch('requests.sessions.get_netrc_auth') as get_netrc_auth:
    get_netrc_auth.return_value = ('user', 'password')
```

**Suggested refactoring:**
```python
def test_password_prompt():
    # Pass credentials directly instead of mocking getpass
    credentials = AuthCredentials._parse_credentials('user:password')
    assert credentials.username == 'user'
    assert credentials.password == 'password'

def test_netrc_auth():
    # Test with explicit credential injection
    auth = HTTPBasicAuth('user', 'password')
    request = requests.Request('GET', 'http://example.com')
    prepared = auth(request.prepare())
    assert 'Authorization' in prepared.headers
```

**Why this matters:**
If you need `mock.patch()` to test your code, it signals that I/O or external dependencies are too tightly coupled with logic. The architectural fix (HOIST-IO) eliminates the need for mocking entirely.

**Rhodes' principle:**
"If you consider patch() an anti-pattern in production code—why are you doing it in your tests? Mocking signals architectural problems."

---

#### NO-SCATTERED-IFS: Scattered conditionals across the main program function

**Current code (httpie/core.py:170-280):**
```python
def program(args: argparse.Namespace, env: Environment) -> ExitStatus:
    # ... setup code ...
    try:
        if args.download:
            args.follow = True
            downloader = Downloader(env, output_file=args.output_file, resume=args.download_resume)
            downloader.pre_request(args.headers)
        # ... more processing ...
        for message in messages:
            output_options = OutputOptions.from_message(message, args.output_options)
            if output_options.kind is RequestsMessageKind.REQUEST:
                if not initial_request:
                    initial_request = message
                if output_options.body:
                    is_streamed_upload = not isinstance(message.body, (str, bytes))
                    do_write_body = not is_streamed_upload
                    force_separator = is_streamed_upload and env.stdout_isatty
            else:
                final_response = message
                if args.check_status or downloader:
                    exit_status = http_status_to_exit_status(http_status=message.status_code, follow=args.follow)
```

**Suggested refactoring:**
```python
class RequestProcessor:
    def __init__(self, args, env):
        self.args = args
        self.env = env
        self.downloader = self._setup_downloader() if args.download else None
        
    def _setup_downloader(self):
        self.args.follow = True
        downloader = Downloader(self.env, output_file=self.args.output_file, resume=self.args.download_resume)
        downloader.pre_request(self.args.headers)
        return downloader

class MessageProcessor:
    def __init__(self, args, env):
        self.args = args
        self.env = env
        
    def process_request(self, message, output_options):
        # Handle request-specific logic
        
    def process_response(self, message, output_options, downloader):
        # Handle response-specific logic

def program(args: argparse.Namespace, env: Environment) -> ExitStatus:
    request_processor = RequestProcessor(args, env)
    message_processor = MessageProcessor(args, env)
    
    for message in messages:
        if message.kind is RequestsMessageKind.REQUEST:
            message_processor.process_request(message, output_options)
        else:
            message_processor.process_response(message, output_options, request_processor.downloader)
```

**Why this matters:**
The current approach scatters feature logic across a single large function, making it difficult to test individual behaviors and understand the code flow. Each feature should be encapsulated in its own class with clear responsibilities.

**Rhodes' principle:**
"Scattered `if` statements across methods create maintenance nightmares. Use composition to separate concerns into distinct classes."

---

#### FUNC-SHELL: Mixed functional and imperative code without clear separation

**Current code (httpie/core.py:180-200):**
```python
def request_body_read_callback(chunk: bytes):
    should_pipe_to_stdout = bool(
        # Request body output desired
        OUT_REQ_BODY in args.output_options
        # & not `.read()` already pre-request (e.g., for  compression)
        and initial_request
        # & non-EOF chunk
        and chunk
    )
    if should_pipe_to_stdout:
        return write_raw_data(
            env,
            chunk,
            processing_options=processing_options,
            headers=initial_request.headers
        )
```

**Suggested refactoring:**
```python
def should_pipe_chunk_to_stdout(chunk: bytes, output_options: set, initial_request: Optional[requests.PreparedRequest]) -> bool:
    """Pure function to determine if chunk should be piped to stdout."""
    return bool(
        OUT_REQ_BODY in output_options
        and initial_request
        and chunk
    )

def create_request_body_callback(env: Environment, output_options: set, processing_options: ProcessingOptions):
    """Factory function for the imperative shell."""
    def callback(chunk: bytes):
        if should_pipe_chunk_to_stdout(chunk, output_options, initial_request):
            return write_raw_data(
                env, chunk,
                processing_options=processing_options,
                headers=initial_request.headers
            )
    return callback
```

**Why this matters:**
Separating the decision logic (functional core) from the I/O operations (imperative shell) makes the logic easier to test and understand. The pure function can be tested with simple data, while the I/O wrapper handles side effects.

**Rhodes' principle:**
"Separate code into a functional core (pure functions) and imperative shell (procedures with I/O)."

---

#### NO-GLOBAL-MUT: Mutable module-level state

**Current code (httpie/client.py:33):**
```python
urllib3.disable_warnings()
```

**Current code (httpie/plugins/registry.py - implied from usage):**
```python
# Global plugin_manager instance that gets mutated
plugin_manager = PluginManager()
```

**Suggested refactoring:**
```python
# httpie/client.py
def configure_urllib3():
    """Configure urllib3 settings - call from main()."""
    urllib3.disable_warnings()

# httpie/plugins/registry.py  
def create_plugin_manager():
    """Factory function to create plugin manager."""
    return PluginManager()

# In main()
def main():
    configure_urllib3()
    plugin_manager = create_plugin_manager()
    # Pass plugin_manager explicitly to functions that need it
```

**Why this matters:**
Global mutable state creates problems: data enters functions from multiple directions, testing requires mutating globals, threading causes race conditions, and unclear data provenance.

**Rhodes' principle:**
"Avoid using mutable globals to eliminate repetition. Use factory functions and dependency injection instead."

---

#### PRECISE-NOUN: Variable names could be more specific

**Current code (httpie/core.py:175-185):**
```python
exit_status = ExitStatus.SUCCESS
downloader = None
initial_request: Optional[requests.PreparedRequest] = None
final_response: Optional[requests.Response] = None
processing_options = ProcessingOptions.from_raw_args(args)
# ... later ...
for message in messages:
    output_options = OutputOptions.from_message(message, args.output_options)
```

**Suggested refactoring:**
```python
http_exit_status = ExitStatus.SUCCESS  # or request_exit_status
file_downloader = None  # or download_manager
first_http_request: Optional[requests.PreparedRequest] = None
last_http_response: Optional[requests.Response] = None
output_processing_options = ProcessingOptions.from_raw_args(args)
# ... later ...
for http_message in messages:
    message_output_options = OutputOptions.from_message(http_message, args.output_options)
```

**Why this matters:**
In duck-typed Python, precise variable names are critical for communicating intent. Generic names like `message`, `options`, and `response` don't clarify what type of data they contain.

**Rhodes' principle:**
"Nouns should precisely describe objects. When discovering imprecise variable name, refactor throughout."

---

#### TOP-DOWN: Code organization could be improved

**Current code (httpie/core.py):**
```python
# Helper functions scattered throughout
def decode_raw_args(args: List[Union[str, bytes]], stdin_encoding: str) -> List[str]:
    # ... 

def raw_main(...):
    # Complex logic with nested functions

def main(...):
    # Simple delegation

def program(...):
    # Main business logic

def print_debug_info(env: Environment):
    # Debug helper
```

**Suggested refactoring:**
```python
def main(args: List[Union[str, bytes]] = sys.argv, env: Environment = Environment()) -> ExitStatus:
    """Main entry point - organize naturally with main logic first."""
    from .cli.definition import parser
    return raw_main(parser=parser, main_program=program, args=args, env=env)

def raw_main(parser, main_program, args, env, use_default_options=True):
    """Main program with error handling."""
    # Main coordination logic here
    
def program(args: argparse.Namespace, env: Environment) -> ExitStatus:
    """Core business logic."""
    # Business logic here

# Helper functions after main logic
def decode_raw_args(args: List[Union[str, bytes]], stdin_encoding: str) -> List[str]:
    # Implementation

def print_debug_info(env: Environment):
    # Implementation
```

**Why this matters:**
Organizing code naturally with main logic first and helpers after improves readability. Python doesn't have C's forward-declaration requirements—organize code naturally for human readers.

**Rhodes' principle:**
"Organize code naturally with main logic first, helpers after (not inverted like C requires)."

---

#### ARG-PER-LINE: Function calls with many parameters should use argument-per-line style

**Current code (httpie/core.py:200):**
```python
messages = collect_messages(env, args=args,
                            request_body_read_callback=request_body_read_callback)
```

**Current code (httpie/client.py:40-45):**
```python
def collect_messages(
    env: Environment,
    args: argparse.Namespace,
    request_body_read_callback: Callable[[bytes], None] = None,
) -> Iterable[RequestsMessage]:
```

**Suggested refactoring:**
```python
messages = collect_messages(
    env=env,
    args=args,
    request_body_read_callback=request_body_read_callback
)

def collect_messages(
    env: Environment,
    args: argparse.Namespace,
    request_body_read_callback: Callable[[bytes], None] = None,
) -> Iterable[RequestsMessage]:
```

**Why this matters:**
Using one argument per line for function calls with many parameters keeps version control clean by isolating changes to single lines and makes the code more readable.

**Rhodes' principle:**
"Use one argument per line for function calls with many parameters to keep version control clean."

### 💡 Rhodes Wisdom

> "Separation of Concerns: Keep I/O separate from business logic. Pure Functions: Prefer pure functions that are easy to test. If your desire to create symmetry requires an `if` statement or `isinstance()` to safely handle return values, the desire for symmetry has led you astray."
> — The Clean Architecture in Python (2014), python-patterns.guide (2016)

---

## Summary

The HTTPie codebase demonstrates good Python practices in many areas but would benefit from applying Rhodes' architectural principles, particularly around separating I/O from business logic, reducing mocking in tests, and organizing complex conditional logic into composable classes. The core issues center around the `program()` function in `httpie/core.py` which mixes multiple concerns and the configuration system which couples file I/O with data processing logic.

The suggested refactorings would create a more testable, maintainable codebase that follows Rhodes' principles of functional cores with imperative shells, explicit naming, and proper separation of concerns.


---

*Generated by Claude Code Skills Review Tool using claude*
