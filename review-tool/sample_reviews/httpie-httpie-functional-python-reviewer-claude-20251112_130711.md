# functional-python-reviewer Review

**Repository:** https://github.com/httpie/httpie
**Review Date:** 2025-11-12 13:07:11
**Reviewer:** functional-python-reviewer
**AI Provider:** claude

---

Based on my exploration of the HTTPie codebase, I can see several areas where functional programming principles could be applied. Let me now provide a comprehensive review focusing on the key modules I examined.

## Review: HTTPie Codebase - Functional Programming Analysis

### ✅ Strengths

- **USE-PARTIAL**: Good use of `functools.partial` in `requestitems.py:123` for creating specialized converter functions
- **USE-FUNCTOOLS**: Proper use of `@functools.wraps` in `requestitems.py:144` for decorators
- **HOF-PATTERN**: Effective use of higher-order functions in `utils.py:252` with `split_iterable()` accepting a key function
- **USE-IMMUTABLE**: Good use of `frozenset` in `client.py:46` for `IGNORE_CONTENT_LENGTH_METHODS`

### ⚠️ Suggestions

#### PURE-FUNC: Functions with side effects in utils.py

**Current code:**
```python
def _max_age_to_expires(cookies, now):
    """
    Translate `max-age` into `expires` for Requests to take it into account.
    """
    for cookie in cookies:
        if 'expires' in cookie:
            continue
        max_age = cookie.get('max-age')
        if max_age and max_age.isdigit():
            cookie['expires'] = now + float(max_age)
```

**Suggested refactoring:**
```python
def _max_age_to_expires(cookies, now):
    """
    Translate `max-age` into `expires` for Requests to take it into account.
    Returns modified cookies without mutating the input.
    """
    modified_cookies = []
    for cookie in cookies:
        new_cookie = cookie.copy()
        if 'expires' not in new_cookie:
            max_age = new_cookie.get('max-age')
            if max_age and max_age.isdigit():
                new_cookie['expires'] = now + float(max_age)
        modified_cookies.append(new_cookie)
    return modified_cookies
```

**Why this matters:**
Pure functions eliminate side effects and make code more predictable. Modifying input parameters can lead to unexpected behavior in calling code and makes testing more difficult.

**FP principle:**
"Same input → same output, no side effects" - pure functions are easier to test, debug, and reason about.

---

#### PREFER-COMPREHENSION: Using filter/map chains in utils.py

**Current code:**
```python
def get_expired_cookies(
    cookies: str,
    now: float = None
) -> List[dict]:

    now = now or time.time()

    def is_expired(expires: Optional[float]) -> bool:
        return expires is not None and expires <= now

    attr_sets: List[Tuple[str, str]] = parse_ns_headers(
        split_cookies(cookies)
    )

    cookies = [
        # The first attr name is the cookie name.
        dict(attrs[1:], name=attrs[0][0])
        for attrs in attr_sets
    ]

    _max_age_to_expires(cookies=cookies, now=now)

    return [
        {
            'name': cookie['name'],
            'path': cookie.get('path', '/')
        }
        for cookie in cookies
        if is_expired(expires=cookie.get('expires'))
    ]
```

**Suggested refactoring:**
```python
def get_expired_cookies(
    cookies: str,
    now: float = None
) -> List[dict]:

    now = now or time.time()

    def is_expired(expires: Optional[float]) -> bool:
        return expires is not None and expires <= now

    def process_attrs(attrs):
        return dict(attrs[1:], name=attrs[0][0])

    attr_sets: List[Tuple[str, str]] = parse_ns_headers(
        split_cookies(cookies)
    )

    # Use comprehension for the entire pipeline
    processed_cookies = [process_attrs(attrs) for attrs in attr_sets]
    cookies_with_expires = _max_age_to_expires(processed_cookies, now)
    
    return [
        {
            'name': cookie['name'],
            'path': cookie.get('path', '/')
        }
        for cookie in cookies_with_expires
        if is_expired(expires=cookie.get('expires'))
    ]
```

**Why this matters:**
List comprehensions are more Pythonic and often more readable than functional chains. They clearly express the transformation pipeline.

**FP principle:**
Combine functional with imperative approaches as needed—Python is multi-paradigm.

---

#### USE-NAMEDTUPLE: Using tuples without names in multiple files

**Current code:**
```python
def process_file_upload_arg(arg: KeyValueArg) -> Tuple[str, IO, str]:
    parts = arg.value.split(SEPARATOR_FILE_UPLOAD_TYPE)
    filename = parts[0]
    mime_type = parts[1] if len(parts) > 1 else None
    try:
        f = open(os.path.expanduser(filename), 'rb')
    except OSError as e:
        raise ParseError(f'{arg.orig!r}: {e}')
    return (
        os.path.basename(filename),
        f,
        mime_type or get_content_type(filename),
    )
```

**Suggested refactoring:**
```python
from collections import namedtuple

FileUpload = namedtuple('FileUpload', ['filename', 'file_handle', 'content_type'])

def process_file_upload_arg(arg: KeyValueArg) -> FileUpload:
    parts = arg.value.split(SEPARATOR_FILE_UPLOAD_TYPE)
    filename = parts[0]
    mime_type = parts[1] if len(parts) > 1 else None
    try:
        f = open(os.path.expanduser(filename), 'rb')
    except OSError as e:
        raise ParseError(f'{arg.orig!r}: {e}')
    return FileUpload(
        filename=os.path.basename(filename),
        file_handle=f,
        content_type=mime_type or get_content_type(filename),
    )
```

**Why this matters:**
Named tuples provide immutability with clear field names, making data structures more self-documenting and safer than plain tuples.

**FP principle:**
Tuples and namedtuples are more predictable than mutable types.

---

#### FUNC-COMPOSE: Complex functions need decomposition in downloads.py

**Current code:**
```python
def parse_content_range(content_range: str, resumed_from: int) -> int:
    """
    Parse and validate Content-Range header.
    """
    if content_range is None:
        raise ContentRangeError('Missing Content-Range')

    pattern = (
        r'^bytes (?P<first_byte_pos>\d+)-(?P<last_byte_pos>\d+)'
        r'/(\*|(?P<instance_length>\d+))$'
    )
    match = re.match(pattern, content_range)

    if not match:
        raise ContentRangeError(
            f'Invalid Content-Range format {content_range!r}')

    content_range_dict = match.groupdict()
    first_byte_pos = int(content_range_dict['first_byte_pos'])
    last_byte_pos = int(content_range_dict['last_byte_pos'])
    instance_length = (
        int(content_range_dict['instance_length'])
        if content_range_dict['instance_length']
        else None
    )

    # Validation logic...
    if (first_byte_pos > last_byte_pos
        or (instance_length is not None
            and instance_length <= last_byte_pos)):
        raise ContentRangeError(
            f'Invalid Content-Range returned: {content_range!r}')

    if (first_byte_pos != resumed_from
        or (instance_length is not None
            and last_byte_pos + 1 != instance_length)):
        raise ContentRangeError(
            f'Unexpected Content-Range returned ({content_range!r})'
            f' for the requested Range ("bytes={resumed_from}-")'
        )

    return last_byte_pos + 1
```

**Suggested refactoring:**
```python
def _parse_content_range_match(content_range: str):
    """Parse the regex match from content range header."""
    pattern = (
        r'^bytes (?P<first_byte_pos>\d+)-(?P<last_byte_pos>\d+)'
        r'/(\*|(?P<instance_length>\d+))$'
    )
    match = re.match(pattern, content_range)
    if not match:
        raise ContentRangeError(f'Invalid Content-Range format {content_range!r}')
    return match.groupdict()

def _extract_range_values(content_range_dict):
    """Extract and convert range values from parsed dict."""
    return (
        int(content_range_dict['first_byte_pos']),
        int(content_range_dict['last_byte_pos']),
        int(content_range_dict['instance_length']) 
        if content_range_dict['instance_length'] else None
    )

def _validate_content_range(first_byte_pos, last_byte_pos, instance_length, content_range):
    """Validate parsed content range values."""
    if (first_byte_pos > last_byte_pos
        or (instance_length is not None and instance_length <= last_byte_pos)):
        raise ContentRangeError(f'Invalid Content-Range returned: {content_range!r}')

def _validate_range_request(first_byte_pos, last_byte_pos, instance_length, 
                           resumed_from, content_range):
    """Validate that the range matches what we requested."""
    if (first_byte_pos != resumed_from
        or (instance_length is not None and last_byte_pos + 1 != instance_length)):
        raise ContentRangeError(
            f'Unexpected Content-Range returned ({content_range!r})'
            f' for the requested Range ("bytes={resumed_from}-")'
        )

def parse_content_range(content_range: str, resumed_from: int) -> int:
    """Parse and validate Content-Range header."""
    if content_range is None:
        raise ContentRangeError('Missing Content-Range')

    content_range_dict = _parse_content_range_match(content_range)
    first_byte_pos, last_byte_pos, instance_length = _extract_range_values(content_range_dict)
    
    _validate_content_range(first_byte_pos, last_byte_pos, instance_length, content_range)
    _validate_range_request(first_byte_pos, last_byte_pos, instance_length, 
                           resumed_from, content_range)

    return last_byte_pos + 1
```

**Why this matters:**
Breaking problems into small functions creates better modularity and testability. Testing is easier because each function is a potential subject for a unit test.

**FP principle:**
"Break problems into small, focused functions. This makes code easier to understand and maintain."

---

#### NO-MODIFY-INPUT: Modifying input collections in sessions.py

**Current code:**
```python
def _compute_new_headers(self, request_headers: HTTPHeadersDict) -> HTTPHeadersDict:
    new_headers = HTTPHeadersDict()
    for name, value in request_headers.copy().items():
        if value is None:
            continue  # Ignore explicitly unset headers

        original_value = value
        if type(value) is not str:
            value = value.decode()

        if name.lower() == 'user-agent' and value.startswith('HTTPie/'):
            continue

        if name.lower() == 'cookie':
            for cookie_name, morsel in SimpleCookie(value).items():
                if not morsel['path']:
                    morsel['path'] = DEFAULT_COOKIE_PATH
                self.cookie_jar.set(cookie_name, morsel)

            request_headers.remove_item(name, original_value)  # Modifies input!
            continue
        # ... rest of method
```

**Suggested refactoring:**
```python
def _compute_new_headers(self, request_headers: HTTPHeadersDict) -> HTTPHeadersDict:
    new_headers = HTTPHeadersDict()
    headers_to_remove = []  # Track what to remove instead of modifying input
    
    for name, value in request_headers.copy().items():
        if value is None:
            continue  # Ignore explicitly unset headers

        original_value = value
        if type(value) is not str:
            value = value.decode()

        if name.lower() == 'user-agent' and value.startswith('HTTPie/'):
            continue

        if name.lower() == 'cookie':
            for cookie_name, morsel in SimpleCookie(value).items():
                if not morsel['path']:
                    morsel['path'] = DEFAULT_COOKIE_PATH
                self.cookie_jar.set(cookie_name, morsel)

            headers_to_remove.append((name, original_value))
            continue
        # ... rest of method
    
    # Return both new headers and items to remove for caller to handle
    return new_headers, headers_to_remove
```

**Why this matters:**
Pure functions avoid side effects and don't modify external state. Modifying input parameters can cause unexpected behavior in calling code and makes functions harder to test and reason about.

**FP principle:**
"Do not change the value of the input or any data that exists outside the function's scope."

---

#### USE-LRU-CACHE: Expensive operations without caching

**Current code:**
```python
def get_content_type(filename):
    """
    Return the content type for ``filename`` in format appropriate
    for Content-Type headers, or ``None`` if the file type is unknown
    to ``mimetypes``.
    """
    return mimetypes.guess_type(filename, strict=False)[0]
```

**Suggested refactoring:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_content_type(filename):
    """
    Return the content type for ``filename`` in format appropriate
    for Content-Type headers, or ``None`` if the file type is unknown
    to ``mimetypes``.
    """
    return mimetypes.guess_type(filename, strict=False)[0]
```

**Why this matters:**
Caching expensive function results dramatically improves performance for functions called repeatedly with the same arguments. `mimetypes.guess_type` performs file system operations that can benefit from caching.

**FP principle:**
A memoizing decorator that "saves up to the maxsize most recent calls." Ideal for expensive or I/O-bound functions.

---

#### GEN-EXPR: Using list comprehensions where generators would be better

**Current code:**
```python
def materialize_cookies(jar: RequestsCookieJar) -> List[Dict[str, Any]]:
    return [
        materialize_cookie(cookie)
        for cookie in jar
    ]

def materialize_headers(headers: Dict[str, str]) -> List[Dict[str, Any]]:
    return [
        {
            'name': name,
            'value': value
        }
        for name, value in headers.copy().items()
    ]
```

**Suggested refactoring:**
```python
def materialize_cookies(jar: RequestsCookieJar) -> Iterator[Dict[str, Any]]:
    return (
        materialize_cookie(cookie)
        for cookie in jar
    )

def materialize_headers(headers: Dict[str, str]) -> Iterator[Dict[str, Any]]:
    return (
        {
            'name': name,
            'value': value
        }
        for name, value in headers.copy().items()
    )

# If lists are specifically needed, callers can use list(materialize_cookies(jar))
```

**Why this matters:**
Generator expressions return iterators instead of lists, saving memory for large collections and enabling lazy evaluation. This is especially important when the results might not be fully consumed.

**FP principle:**
Generators perform operations on-demand, conserving memory versus eager evaluation.

### 💡 Functional Programming Wisdom
> "Python is a multi-paradigm language. Combine functional with imperative approaches as needed—don't force pure functional style."
> — Python Functional Programming HOWTO

The HTTPie codebase shows good understanding of Python's functional features in some areas, but could benefit from more consistent application of functional programming principles, especially around pure functions, immutability, and memory-efficient lazy evaluation patterns.


---

*Generated by Claude Code Skills Review Tool using claude*
