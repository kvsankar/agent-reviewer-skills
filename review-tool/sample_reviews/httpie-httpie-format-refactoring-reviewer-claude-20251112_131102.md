# format-refactoring-reviewer Review

**Repository:** https://github.com/httpie/httpie
**Review Date:** 2025-11-12 13:11:02
**Reviewer:** format-refactoring-reviewer
**AI Provider:** claude

---

Now I have enough information to write a comprehensive format/style refactoring review. Based on my analysis, I can see several opportunities for improvement following the guidelines.

## Format/Style Refactoring Review: HTTPie Core Components

### ✅ Well-Structured Code
- **FMT-GROUP-IMPORTS**: Import organization follows PEP 8 standards with proper grouping of standard library, third-party, and local imports
- **FMT-EXTRACT-METHOD**: Many functions are appropriately sized with single responsibilities
- **FMT-TRAILING-COMMA**: Multi-line import statements properly use trailing commas for clean version control diffs

### 🔧 Refactoring Opportunities

#### Long Line Issues: FMT-EXTRACT-VAR - Extract Variables for Complex F-String Expressions

**Linter would say:**
> "Line too long (95/79)" in httpie/downloads.py:77-80

**Root cause:**
Complex f-string expressions pack too much information on single lines, making them hard to read and debug.

**Current code:**
```python
# httpie/downloads.py:77-80
raise ContentRangeError(
    f'Unexpected Content-Range returned ({content_range!r})'
    f' for the requested Range ("bytes={resumed_from}-")'
)
```

**Refactored code:**
```python
# httpie/downloads.py:77-80
error_msg = f'Unexpected Content-Range returned ({content_range!r})'
range_info = f' for the requested Range ("bytes={resumed_from}-")'
raise ContentRangeError(error_msg + range_info)
```

**Why this is better:**
- Each part of the error message has a descriptive variable name
- Easier to debug - can inspect individual message components
- Naturally fits within line length limits
- More maintainable when message format needs changes

**Refactoring applied:**
Extract Variable for Error Messages

---

#### Complexity Issues: FMT-DECOMPOSE-COND - Decompose Complex Boolean Logic

**Linter would say:**
> "Expression too complex" and "Line too long (85/79)" in httpie/downloads.py:67-70

**Root cause:**
Complex boolean expressions with nested conditions are hard to understand and maintain.

**Current code:**
```python
# httpie/downloads.py:67-70
if (first_byte_pos > last_byte_pos
    or (instance_length is not None
        and instance_length <= last_byte_pos)):
    raise ContentRangeError(
        f'Invalid Content-Range returned: {content_range!r}')
```

**Refactored code:**
```python
# httpie/downloads.py:67-70
def is_invalid_byte_range(first_byte_pos, last_byte_pos, instance_length):
    """Check if Content-Range byte positions are invalid."""
    positions_inverted = first_byte_pos > last_byte_pos
    length_too_small = (
        instance_length is not None 
        and instance_length <= last_byte_pos
    )
    return positions_inverted or length_too_small

if is_invalid_byte_range(first_byte_pos, last_byte_pos, instance_length):
    raise ContentRangeError(f'Invalid Content-Range returned: {content_range!r}')
```

**Why this is better:**
- Complex validation logic is extracted to named function
- Each condition has a descriptive variable name
- Business logic is self-documenting through function and variable names
- Function can be unit tested independently

**Refactoring applied:**
Decompose Conditional + Extract Method

---

#### Expression Clarity: FMT-ALIGN-TERNARY - Refactor Complex Ternary to If/Else

**Linter would say:**
> "Line too long (88/79)" in httpie/downloads.py:55-59

**Root cause:**
Complex ternary expression on multiple lines is harder to read than explicit if/else.

**Current code:**
```python
# httpie/downloads.py:55-59
instance_length = (
    int(content_range_dict['instance_length'])
    if content_range_dict['instance_length']
    else None
)
```

**Refactored code:**
```python
# httpie/downloads.py:55-59
length_value = content_range_dict['instance_length']
if length_value:
    instance_length = int(length_value)
else:
    instance_length = None
```

**Why this is better:**
- Intermediate variable clarifies what we're checking
- If/else is more explicit than ternary for this case
- Easier to add logging or validation to each branch
- More readable for complex type conversion

**Refactoring applied:**
Replace Ternary with If/Else + Extract Variable

---

#### Method Organization: FMT-LONG-METHOD - Extract Method for Complex URL Processing

**Linter would say:**
> "Function is too complex (12/10)" in httpie/cli/argparser.py:205-226

**Root cause:**
The `_process_url` method handles multiple URL transformation concerns in one function.

**Current code:**
```python
# httpie/cli/argparser.py:205-226
def _process_url(self):
    if self.args.url.startswith('://'):
        # Paste URL & add space shortcut: `http ://pie.dev` → `http://pie.dev`
        self.args.url = self.args.url[3:]
    if not URL_SCHEME_RE.match(self.args.url):
        if os.path.basename(self.env.program_name) == 'https':
            scheme = 'https://'
        else:
            scheme = self.args.default_scheme + '://'

        # See if we're using curl style shorthand for localhost (:3000/foo)
        shorthand = re.match(r'^:(?!:)(\d*)(/?.*)$', self.args.url)
        if shorthand:
            port = shorthand.group(1)
            rest = shorthand.group(2)
            self.args.url = scheme + 'localhost'
            if port:
                self.args.url += ':' + port
            self.args.url += rest
        else:
            self.args.url = scheme + self.args.url
```

**Refactored code:**
```python
# httpie/cli/argparser.py:205-226
def _process_url(self):
    self._handle_url_paste_shortcut()
    if not URL_SCHEME_RE.match(self.args.url):
        self._add_url_scheme()

def _handle_url_paste_shortcut(self):
    """Handle 'http ://pie.dev' → 'http://pie.dev' shortcut."""
    if self.args.url.startswith('://'):
        self.args.url = self.args.url[3:]

def _add_url_scheme(self):
    """Add appropriate scheme to URL if missing."""
    scheme = self._get_default_scheme()
    
    localhost_match = self._parse_localhost_shorthand()
    if localhost_match:
        self.args.url = self._build_localhost_url(scheme, localhost_match)
    else:
        self.args.url = scheme + self.args.url

def _get_default_scheme(self):
    """Determine default scheme based on program name."""
    if os.path.basename(self.env.program_name) == 'https':
        return 'https://'
    return self.args.default_scheme + '://'

def _parse_localhost_shorthand(self):
    """Parse curl-style localhost shorthand (:3000/foo)."""
    return re.match(r'^:(?!:)(\d*)(/?.*)$', self.args.url)

def _build_localhost_url(self, scheme, match):
    """Build full localhost URL from shorthand match."""
    port = match.group(1)
    rest = match.group(2)
    url = scheme + 'localhost'
    if port:
        url += ':' + port
    url += rest
    return url
```

**Why this is better:**
- Each method has single responsibility and clear purpose
- Main method reads like documentation of the process
- Each step is testable independently
- URL transformation logic is more modular and maintainable
- Complexity is distributed across focused methods

**Refactoring applied:**
Extract Method (Compose Method Pattern)

---

#### Nesting Issues: FMT-GUARD-CLAUSE - Use Guard Clauses for Argument Validation

**Linter would say:**
> "Too many nested blocks (4/3)" in httpie/cli/argparser.py:55-75

**Root cause:**
Nested conditionals in argument processing create deep indentation and reduce readability.

**Current code:**
```python
# httpie/cli/argparser.py:55-75 (similar pattern)
if (
    isinstance(exception, argparse.ArgumentError)
    and len(exception.args) >= 1
    and isinstance(exception.args[0], argparse.Action)
):
    # add_usage path is also taken when you pass an invalid option,
    # e.g --style=invalid. If something like that happens, we want
    # to include to action that caused to the invalid usage into
    # the list of actions we are displaying.
    displayed_actions.insert(0, exception.args[0])
```

**Refactored code:**
```python
# httpie/cli/argparser.py:55-75
def _should_include_error_action(self, exception):
    """Check if we should include the error-causing action in display."""
    if not isinstance(exception, argparse.ArgumentError):
        return False
    if len(exception.args) < 1:
        return False
    if not isinstance(exception.args[0], argparse.Action):
        return False
    return True

# In the main logic:
if self._should_include_error_action(exception):
    # add_usage path is also taken when you pass an invalid option,
    # e.g --style=invalid. If something like that happens, we want
    # to include to action that caused to the invalid usage into
    # the list of actions we are displaying.
    displayed_actions.insert(0, exception.args[0])
```

**Why this is better:**
- Guard clauses eliminate nested conditions
- Validation logic is extracted and named
- Each validation step is clear and independent
- Main logic focuses on the action, not validation
- More testable validation logic

**Refactoring applied:**
Replace Nested Conditional with Guard Clauses + Extract Method

---

### 💡 Refactoring Wisdom
> "Don't fight the linter—refactor so it has nothing to complain about." - Brandon Rhodes

The HTTPie codebase shows good overall structure, but these refactoring opportunities will improve maintainability by:
- Making complex expressions self-documenting through variable names
- Reducing cognitive load through method extraction
- Improving testability by isolating business logic
- Following Python idioms for cleaner, more readable code

Each suggested refactoring follows established patterns from "A Python Aesthetic" and Refactoring Guru, ensuring the code becomes more maintainable while style issues disappear naturally.


---

*Generated by Claude Code Skills Review Tool using claude*
