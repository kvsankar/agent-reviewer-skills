# python-rhodes-reviewer Review

**Repository:** https://github.com/simonw/datasette
**Review Date:** 2025-12-15 18:06:48
**Reviewer:** python-rhodes-reviewer
**AI Provider:** claude

---

Based on my comprehensive exploration of the Datasette codebase, I now have enough information to provide a thorough Brandon Rhodes-style code review. Let me analyze the key patterns and issues I found.

## Review: Datasette Python Codebase

### ✅ Strengths

- **FUNC-SHELL**: Excellent separation between async database operations and pure utility functions in `datasette/utils/__init__.py`. Functions like `parse_metadata()` handle parsing logic separately from I/O.
- **NAMED-TUPLE**: Good use of named tuples like `AttachedDatabase = namedtuple("AttachedDatabase", ("seq", "name", "file"))` in `datasette/database.py:29` for better type safety and documentation.
- **DICT-COMP**: Effective use of dictionary comprehensions throughout, like in `datasette/database.py:74-78` for building cached table counts.
- **PRECISE-NOUN**: Generally good naming with descriptive variables like `cached_table_counts`, `is_mutable`, `memory_name` in database module.

### ⚠️ Suggestions

#### HOIST-IO: I/O operations embedded within business logic methods

**Current code:**
```python
# datasette/app.py:964-966
def app_css_hash(self):
    if not hasattr(self, "_app_css_hash"):
        with open(os.path.join(str(app_root), "datasette/static/app.css")) as fp:
            self._app_css_hash = hashlib.sha1(fp.read().encode("utf8")).hexdigest()[:6]
    return self._app_css_hash
```

**Suggested refactoring:**
```python
def app_css_hash(self):
    if not hasattr(self, "_app_css_hash"):
        self._app_css_hash = self._compute_css_hash(self._read_app_css())
    return self._app_css_hash

def _read_app_css(self):
    """Pure I/O operation - moved to top level or dependency injected."""
    with open(os.path.join(str(app_root), "datasette/static/app.css")) as fp:
        return fp.read()

def _compute_css_hash(self, css_content):
    """Pure function - easily testable."""
    return hashlib.sha1(css_content.encode("utf8")).hexdigest()[:6]
```

**Why this matters:**
Separating file I/O from hash computation makes the hash logic testable without file system dependencies. You can test `_compute_css_hash()` with simple string data, making tests faster and more reliable.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic to remain pure and testable."

---

#### HOIST-IO: File operations coupled with parsing logic

**Current code:**
```python
# datasette/app.py:400-406
if config_dir and metadata_files and not metadata:
    with metadata_files[0].open() as fp:
        metadata = parse_metadata(fp.read())

if config_dir and config_files and not config:
    with config_files[0].open() as fp:
        config = parse_metadata(fp.read())
```

**Suggested refactoring:**
```python
# At top level (caller manages I/O)
def load_metadata_and_config(config_dir, metadata_files, config_files, metadata=None, config=None):
    if config_dir and metadata_files and not metadata:
        content = metadata_files[0].read_text()
        metadata = parse_metadata(content)
    
    if config_dir and config_files and not config:
        content = config_files[0].read_text()  
        config = parse_metadata(content)
    
    return metadata, config

# parse_metadata remains pure (already good!)
def parse_metadata(content: str) -> dict:
    """Pure function - easily testable."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError:
            raise BadMetadataError("Metadata is not valid JSON or YAML")
```

**Why this matters:**
The `parse_metadata()` function is already pure and testable, but the file reading is scattered across the initialization logic. Consolidating I/O operations makes the code easier to test and reason about.

**Rhodes' principle:**
"Functional core, imperative shell - separate I/O from business logic to create pure functions that are easy to test without mocking."

---

#### NO-SCATTERED-IFS: Format handling scattered across methods

**Current code:**
```python
# datasette/views/database.py:647-665
if format_ == "csv":
    async def fetch_data_for_csv(request, _next=None):
        results = await db.execute(sql, params, truncate=True)
        data = {"rows": results.rows, "columns": results.columns}
        return data, None, None
    return await stream_csv(datasette, fetch_data_for_csv, request, db.name)
    
elif format_ in datasette.renderers.keys():
    # Dispatch request to the correct output format renderer
    result = call_with_supported_arguments(
        datasette.renderers[format_][0],
        datasette=datasette,
        columns=columns,
        rows=rows,
        sql=sql,
        # ... many more parameters
    )
elif format_ == "html":
    # HTML handling logic
```

**Suggested refactoring:**
```python
class FormatRenderer:
    def __init__(self, datasette):
        self.datasette = datasette
        self.renderers = {
            'csv': self._render_csv,
            'html': self._render_html,
            **{fmt: self._render_plugin for fmt in datasette.renderers.keys()}
        }
    
    async def render(self, format_, **context):
        if format_ not in self.renderers:
            raise NotFound(f"Invalid format: {format_}")
        return await self.renderers[format_](**context)
    
    async def _render_csv(self, db, sql, params, request, **kwargs):
        async def fetch_data_for_csv(request, _next=None):
            results = await db.execute(sql, params, truncate=True)
            return {"rows": results.rows, "columns": results.columns}, None, None
        return await stream_csv(self.datasette, fetch_data_for_csv, request, db.name)

# Usage in view
renderer = FormatRenderer(datasette)
return await renderer.render(format_, db=db, sql=sql, params=params, request=request)
```

**Why this matters:**
Scattered `if/elif` statements make adding new formats difficult and testing complex. Each format requires understanding the entire conditional chain. The composition approach isolates format logic and makes it easily extensible.

**Rhodes' principle:**
"Scattered `if` statements across methods create maintenance nightmares. Use composition to separate concerns into distinct classes."

---

#### NO-GLOBAL-MUT: Thread-local global state usage

**Current code:**
```python
# datasette/database.py:26
connections = threading.local()

# datasette/database.py:41-45
class Database:
    _thread_local_id_counter = 1
    
    def __init__(self, ds, path=None, ...):
        self._thread_local_id = f"x{self._thread_local_id_counter}"
        Database._thread_local_id_counter += 1
```

**Suggested refactoring:**
```python
class ConnectionManager:
    """Manages database connections without global state."""
    def __init__(self):
        self._connections = threading.local()
        self._id_counter = 1
    
    def get_connection_id(self):
        id = f"x{self._id_counter}"
        self._id_counter += 1
        return id
    
    def get_connection(self, key):
        return getattr(self._connections, key, None)
    
    def set_connection(self, key, conn):
        setattr(self._connections, key, conn)

class Database:
    def __init__(self, ds, connection_manager, path=None, ...):
        self._thread_local_id = connection_manager.get_connection_id()
        self.connection_manager = connection_manager
        # ... rest of initialization
```

**Why this matters:**
Global mutable state creates dangerous coupling between distant code sections. Tests become coupled and cannot run safely in parallel. Dependency injection makes the connection management explicit and testable.

**Rhodes' principle:**
"Mutable globals create dangerous coupling between distant code sections. Tests become coupled and cannot run safely in parallel."

---

#### EXPLICIT-NAME: Method names that don't reveal intent

**Current code:**
```python
# datasette/database.py:89
def connect(self, write=False):
    # Method that both creates AND configures connections
    extra_kwargs = {}
    if write:
        extra_kwargs["isolation_level"] = "IMMEDIATE"
    # ... connection creation and configuration logic
```

**Suggested refactoring:**
```python
def create_connection(self, write=False):
    """Create a new database connection with appropriate configuration."""
    extra_kwargs = {}
    if write:
        extra_kwargs["isolation_level"] = "IMMEDIATE"
    
    if self.memory_name:
        return self._create_memory_connection(**extra_kwargs)
    elif self.is_memory:
        return self._create_temp_memory_connection()
    else:
        return self._create_file_connection(**extra_kwargs)

def get_connection(self, write=False):
    """Get or create a connection for current thread."""
    # Connection pooling logic here
    pass
```

**Why this matters:**
`connect()` is ambiguous - does it establish a new connection or retrieve an existing one? The method actually creates new connections each time, which should be explicit in the name.

**Rhodes' principle:**
"Use explicit method names that reveal intent. Clear naming eliminates the need for documentation."

---

#### DICT-JOIN: O(nm) lookup pattern in visibility checking

**Current code:**
```python
# Pattern visible in datasette/views/database.py:47-51
for item in collection:
    if item.name in allowed_names:  # Potential O(n) lookup repeated m times
        visible_items.append(item)
```

**Suggested refactoring:**
```python
# Convert to set for O(1) lookups
allowed_names_set = set(allowed_names)

# Or better - dictionary join pattern
visible_items = [
    item for item in collection 
    if item.name in allowed_names_set
]

# For more complex joins, use dict mapping
allowed_map = {name: permissions for name, permissions in allowed_items}
visible_items = []
for item in collection:
    if item.name in allowed_map:
        item.permissions = allowed_map[item.name]
        visible_items.append(item)
```

**Why this matters:**
Converting lists to sets for membership testing changes O(nm) performance to O(n+m). With hundreds of tables and complex permission checks, this can significantly impact response times.

**Rhodes' principle:**
"Use dictionaries for constant-time lookups to avoid O(nm) performance problems."

---

#### PASS-FUNC: Passing data instead of functions for flexibility

**Current code:**
```python
# datasette/views/database.py:648-652
async def fetch_data_for_csv(request, _next=None):
    results = await db.execute(sql, params, truncate=True)
    data = {"rows": results.rows, "columns": results.columns}
    return data, None, None

return await stream_csv(datasette, fetch_data_for_csv, request, db.name)
```

**Suggested refactoring:**
```python
# Pass the execution function, not just data
async def create_csv_executor(db, sql, params):
    """Return a function that executes the query when called."""
    async def execute_query(request, _next=None):
        results = await db.execute(sql, params, truncate=True)
        return {"rows": results.rows, "columns": results.columns}, None, None
    return execute_query

# More flexible - allows for different execution strategies
csv_executor = await create_csv_executor(db, sql, params)
return await stream_csv(datasette, csv_executor, request, db.name)
```

**Why this matters:**
Passing functions instead of data enables better composition and testing. You can easily swap execution strategies (cached vs live queries) without changing the streaming logic.

**Rhodes' principle:**
"Pass functions not data - enables nested animations, transparent effect composition, and better code organization."

---

### 💡 Rhodes Wisdom

> "If you consider patch() an anti-pattern in production code—why are you doing it in your tests? Mocking signals architectural problems."
> — Hoisting Your I/O (2015)

> "When code feels backward or requires excessive workarounds, consider whether a Copernican refactoring—repositioning a central element—could provide elegant simplification rather than incremental fixes."
> — Copernican Refactoring (2013)

The Datasette codebase shows strong architectural foundations with good separation of concerns in many areas. The main opportunities for improvement center around hoisting I/O operations to higher levels, reducing scattered conditionals through composition, and eliminating global mutable state. These changes would make the codebase more testable and maintainable while following Brandon Rhodes' core principles of functional core/imperative shell architecture.


---

*Generated by Claude Code Skills Review Tool using claude*
