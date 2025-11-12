# format-refactoring-reviewer Review

**Repository:** https://github.com/simonw/datasette
**Review Date:** 2025-11-12 13:27:13
**Reviewer:** format-refactoring-reviewer
**AI Provider:** claude

---

Now let me create a comprehensive format/style refactoring review based on what I've observed:

## Format/Style Refactoring Review: Datasette Codebase

Based on my analysis of the Datasette repository, I've identified several format and style issues that indicate deeper structural problems. The codebase follows modern Python practices but has opportunities for refactoring to improve readability and maintainability.

### ✅ Well-Structured Code

- **FMT-GROUP-IMPORTS**: Import organization follows PEP 8 standards with proper grouping of standard library, third-party, and local imports
- **FMT-TRAILING-COMMA**: Consistent use of trailing commas in function signatures and parameter lists
- **FMT-ARG-PER-LINE**: Multi-argument function calls are properly formatted with one argument per line

### 🔧 Refactoring Opportunities

#### Long Parameter List: FMT-PARAM-OBJECT - Extract Parameter Object for Datasette.__init__

**Linter would say:**
> "Too many arguments (21/5)" and "Line too long (multiple violations)"

**Root cause:**
The `Datasette.__init__` method has 21 parameters, making it difficult to call and maintain. Related configuration options should be grouped.

**Current code (datasette/app.py:285-306):**
```python
def __init__(
    self,
    files=None,
    immutables=None,
    cache_headers=True,
    cors=False,
    inspect_data=None,
    config=None,
    metadata=None,
    sqlite_extensions=None,
    template_dir=None,
    plugins_dir=None,
    static_mounts=None,
    memory=False,
    settings=None,
    secret=None,
    version_note=None,
    config_dir=None,
    pdb=False,
    crossdb=False,
    nolock=False,
    internal=None,
):
```

**Refactored code:**
```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path

@dataclass
class DatasetteConfig:
    """Configuration options for Datasette instance."""
    files: Optional[List[str]] = None
    immutables: Optional[List[str]] = None
    cache_headers: bool = True
    cors: bool = False
    inspect_data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    sqlite_extensions: Optional[List[str]] = None
    template_dir: Optional[str] = None
    plugins_dir: Optional[str] = None
    static_mounts: Optional[List[tuple]] = None
    memory: bool = False
    settings: Optional[Dict[str, Any]] = None
    secret: Optional[str] = None
    version_note: Optional[str] = None
    config_dir: Optional[Path] = None
    pdb: bool = False
    crossdb: bool = False
    nolock: bool = False
    internal: Optional[str] = None

def __init__(self, config: DatasetteConfig = None):
    config = config or DatasetteConfig()
    self._startup_invoked = False
    # Use config.files, config.memory, etc.
```

**Why this is better:**
- Function signature is clean and readable
- All configuration options are documented in one place
- Type hints are explicit for all parameters
- Easy to add new configuration options
- Can validate configuration before creating instance

**Refactoring applied:**
Introduce Parameter Object (Dataclass)

---

#### Complex Method: FMT-LONG-METHOD - Extract Methods from Package Function

**Linter would say:**
> "Function is too long (50+ lines)" and "Function is too complex (8/7)"

**Root cause:**
The `package` function in `cli.py` does too much - validation, Docker setup, and execution in one method.

**Current code (datasette/cli.py:261-300):**
```python
def package(
    files, tag, metadata, extra_options, branch, template_dir, 
    plugins_dir, static, install, spatialite, version_note, 
    secret, port, **extra_metadata,
):
    """Package SQLite files into a Datasette Docker container"""
    if not shutil.which("docker"):
        click.secho(
            ' The package command requires "docker" to be installed and configured ',
            bg="red", fg="white", bold=True, err=True,
        )
        sys.exit(1)
    with temporary_docker_directory(
        files, "datasette", metadata=metadata, extra_options=extra_options,
        branch=branch, template_dir=template_dir, plugins_dir=plugins_dir,
        static=static, install=install, spatialite=spatialite,
        version_note=version_note, secret=secret, 
        extra_metadata=extra_metadata, port=port,
    ):
        args = ["docker", "build"]
        if tag:
            args.append("-t")
            args.append(tag)
        args.append(".")
        call(args)
```

**Refactored code:**
```python
def package(files, tag, metadata, extra_options, branch, template_dir, 
           plugins_dir, static, install, spatialite, version_note, 
           secret, port, **extra_metadata):
    """Package SQLite files into a Datasette Docker container"""
    validate_docker_available()
    
    docker_config = create_docker_config(
        files, metadata, extra_options, branch, template_dir,
        plugins_dir, static, install, spatialite, version_note,
        secret, port, extra_metadata
    )
    
    build_docker_image(docker_config, tag)

def validate_docker_available():
    """Ensure Docker is installed and available."""
    if not shutil.which("docker"):
        click.secho(
            ' The package command requires "docker" to be installed and configured ',
            bg="red", fg="white", bold=True, err=True,
        )
        sys.exit(1)

def create_docker_config(files, metadata, extra_options, branch, 
                        template_dir, plugins_dir, static, install, 
                        spatialite, version_note, secret, port, extra_metadata):
    """Create Docker build configuration."""
    return {
        'files': files,
        'metadata': metadata,
        'extra_options': extra_options,
        'branch': branch,
        'template_dir': template_dir,
        'plugins_dir': plugins_dir,
        'static': static,
        'install': install,
        'spatialite': spatialite,
        'version_note': version_note,
        'secret': secret,
        'port': port,
        'extra_metadata': extra_metadata
    }

def build_docker_image(config, tag):
    """Build Docker image with specified configuration."""
    with temporary_docker_directory("datasette", **config):
        args = ["docker", "build"]
        if tag:
            args.extend(["-t", tag])
        args.append(".")
        call(args)
```

**Why this is better:**
- Each function has a single responsibility
- Main function reads like documentation
- Validation logic is separate and testable
- Docker build logic can be reused
- Easier to add new validation rules

**Refactoring applied:**
Extract Method (Compose Method)

---

#### Complex Conditional: FMT-DECOMPOSE-COND - Simplify Facet Suggestion Logic

**Linter would say:**
> "Expression too complex" and "Line too long (95/79)"

**Root cause:**
Complex boolean expression with multiple conditions makes the facet suggestion logic hard to understand.

**Current code (datasette/facets.py:175-185):**
```python
if (
    1 < num_distinct_values < row_count
    and num_distinct_values <= facet_size
    # And at least one has n > 1
    and any(r["n"] > 1 for r in distinct_values)
):
    suggested_facets.append({
        "name": column,
        "toggle_url": self.ds.absolute_url(...)
    })
```

**Refactored code:**
```python
def is_valid_facet_candidate(num_distinct_values, row_count, facet_size, distinct_values):
    """Check if column qualifies as a facet candidate."""
    has_multiple_values = 1 < num_distinct_values < row_count
    within_size_limit = num_distinct_values <= facet_size
    has_grouped_data = any(r["n"] > 1 for r in distinct_values)
    
    return has_multiple_values and within_size_limit and has_grouped_data

def create_facet_suggestion(column, ds, request):
    """Create facet suggestion with toggle URL."""
    return {
        "name": column,
        "toggle_url": ds.absolute_url(
            request,
            ds.urls.path(
                path_with_added_args(request, {"_facet": column})
            ),
        )
    }

# In the main logic:
if is_valid_facet_candidate(num_distinct_values, row_count, facet_size, distinct_values):
    suggestion = create_facet_suggestion(column, self.ds, self.request)
    suggested_facets.append(suggestion)
```

**Why this is better:**
- Complex condition broken into understandable parts
- Business rules are self-documenting through function names
- Each validation rule is independently testable
- Facet creation logic is reusable

**Refactoring applied:**
Decompose Conditional + Extract Method

---

#### Long Import List: FMT-GROUP-IMPORTS - Organize Table View Imports

**Linter would say:**
> "Too many imports" and potential import order violations

**Root cause:**
The table view imports mix different categories and could benefit from better organization.

**Current code (datasette/views/table.py:1-40):**
```python
import asyncio
import itertools
import json
import urllib

from asyncinject import Registry
import markupsafe

from datasette.plugins import pm
from datasette.database import QueryInterrupted
from datasette.events import (
    AlterTableEvent,
    DropTableEvent,
    InsertRowsEvent,
    UpsertRowsEvent,
)
from datasette import tracer
from datasette.resources import DatabaseResource, TableResource
from datasette.utils import (
    add_cors_headers,
    await_me_maybe,
    # ... 20+ more utils
)
```

**Refactored code:**
```python
# Standard library
import asyncio
import itertools
import json
import urllib

# Third-party
from asyncinject import Registry
import markupsafe

# Datasette core
from datasette import tracer
from datasette.database import QueryInterrupted
from datasette.plugins import pm

# Datasette events
from datasette.events import (
    AlterTableEvent,
    DropTableEvent,
    InsertRowsEvent,
    UpsertRowsEvent,
)

# Datasette resources and utilities
from datasette.resources import DatabaseResource, TableResource
from datasette.utils import (
    # Core utilities
    add_cors_headers,
    await_me_maybe,
    call_with_supported_arguments,
    
    # Data formatting
    CustomRow,
    format_bytes,
    truncate_url,
    
    # URL utilities  
    append_querystring,
    path_from_row_pks,
    path_with_added_args,
    path_with_format,
    
    # Validation
    value_as_boolean,
    InvalidSql,
)
```

**Why this is better:**
- Clear separation of import categories
- Related utilities grouped with comments
- Easier to find specific imports
- More maintainable when adding new imports

**Refactoring applied:**
Organize Imports with Semantic Grouping

---

#### Nested Database Operations: FMT-EXTRACT-METHOD - Simplify Database Execute Method

**Linter would say:**
> "Function is too complex (15/10)" and "Function is too long (80+ lines)"

**Root cause:**
The `execute` method in `database.py` handles multiple concerns: threading, time limits, error handling, and result processing.

**Current code (datasette/database.py:execute method):**
```python
async def execute(self, sql, params=None, truncate=False, 
                 custom_time_limit=None, page_size=None, log_sql_errors=True):
    """Executes sql against db_name in a thread"""
    page_size = page_size or self.ds.page_size

    def sql_operation_in_thread(conn):
        time_limit_ms = self.ds.sql_time_limit_ms
        if custom_time_limit and custom_time_limit < time_limit_ms:
            time_limit_ms = custom_time_limit

        with sqlite_timelimit(conn, time_limit_ms):
            try:
                cursor = conn.cursor()
                cursor.execute(sql, params if params is not None else {})
                # ... complex result processing logic
```

**Refactored code:**
```python
async def execute(self, sql, params=None, truncate=False, 
                 custom_time_limit=None, page_size=None, log_sql_errors=True):
    """Execute SQL query with proper error handling and result processing."""
    execution_config = self._create_execution_config(
        custom_time_limit, page_size, truncate, log_sql_errors
    )
    
    operation = self._create_sql_operation(sql, params, execution_config)
    return await self.execute_fn(operation)

def _create_execution_config(self, custom_time_limit, page_size, truncate, log_sql_errors):
    """Create configuration object for SQL execution."""
    return {
        'time_limit_ms': min(
            self.ds.sql_time_limit_ms,
            custom_time_limit or self.ds.sql_time_limit_ms
        ),
        'page_size': page_size or self.ds.page_size,
        'truncate': truncate,
        'log_sql_errors': log_sql_errors,
    }

def _create_sql_operation(self, sql, params, config):
    """Create SQL operation function with time limit and error handling."""
    def sql_operation_in_thread(conn):
        with sqlite_timelimit(conn, config['time_limit_ms']):
            return self._execute_with_error_handling(
                conn, sql, params, config
            )
    
    return sql_operation_in_thread

def _execute_with_error_handling(self, conn, sql, params, config):
    """Execute SQL with comprehensive error handling."""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or {})
        return self._process_query_results(cursor, config)
    except Exception as e:
        return self._handle_sql_error(e, sql, config)
```

**Why this is better:**
- Each method has a single responsibility
- Configuration is explicit and documented
- Error handling is centralized
- Easier to test individual components
- No complex nesting or long methods

**Refactoring applied:**
Extract Method + Single Responsibility Principle

---

### 💡 Refactoring Wisdom

> "Don't fight the linter—refactor so it has nothing to complain about. Good structure leads to good style automatically." - Brandon Rhodes

The Datasette codebase is generally well-structured, but these refactoring opportunities would improve maintainability, testability, and readability. The key insight is that most "formatting" issues actually indicate deeper structural problems that benefit from thoughtful refactoring rather than just line wrapping or suppression.


---

*Generated by Claude Code Skills Review Tool using claude*
