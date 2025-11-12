# refactoring-reviewer Review

**Repository:** https://github.com/simonw/datasette
**Review Date:** 2025-11-12 13:20:53
**Reviewer:** refactoring-reviewer
**AI Provider:** claude

---

Now I have enough information to write a comprehensive refactoring review. Based on my analysis of the datasette codebase, I can see several key refactoring opportunities.

## Refactoring Review: Datasette Repository

### ✅ Strengths

- **MEANINGFUL-NAME**: Most classes and functions use descriptive names like `Datasette`, `Database`, `QueryInterrupted`
- **PYTHONIC**: Good use of Python features like dataclasses, type hints, and async/await patterns  
- **MODULAR**: Well-organized package structure with clear separation between views, utils, and core logic
- **F-STRING**: Modern f-string usage throughout the codebase
- **TYPE-HINTS**: Excellent use of type annotations for better code documentation

### 🔨 Refactoring Opportunities

#### **MAINTAINABILITY: GOD-CLASS** - Break Down Datasette Class

**Current code:**
```python
class Datasette:
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
        # 266 lines of initialization logic
        # 47 methods handling:
        # - Database management
        # - Configuration 
        # - Plugin management
        # - Authentication
        # - Template rendering
        # - Metadata management
```

**Refactored code:**
```python
@dataclass
class DatasetteConfig:
    """Handles all configuration concerns."""
    files: tuple = ()
    immutables: set = field(default_factory=set)
    cache_headers: bool = True
    cors: bool = False
    template_dir: Optional[str] = None
    plugins_dir: Optional[str] = None
    static_mounts: List[Tuple[str, str]] = field(default_factory=list)
    # ... other config fields

class DatabaseManager:
    """Manages database connections and operations."""
    def __init__(self, config: DatasetteConfig):
        self.databases = OrderedDict()
        self.config = config
    
    def add_database(self, db, name=None, route=None):
        # Move database management logic here
        pass
    
    def get_database(self, name=None, route=None):
        # Move database retrieval logic here  
        pass

class PluginManager:
    """Handles plugin loading and management."""
    def __init__(self, plugins_dir: Optional[str]):
        self.plugins_dir = plugins_dir
        
    def load_plugins(self):
        # Move plugin loading logic here
        pass

class Datasette:
    def __init__(self, config: DatasetteConfig):
        self.config = config
        self.database_manager = DatabaseManager(config)
        self.plugin_manager = PluginManager(config.plugins_dir)
        self.template_renderer = TemplateRenderer(config)
        # Much simpler initialization
```

**Why this matters:**
The current Datasette class has 47 methods and a 266-line constructor, indicating it's handling too many responsibilities. Breaking it into focused components improves maintainability and testability.

**Code smell addressed:**
God Class - single class doing too much work

---

#### **READABILITY: LONG-PARAM** - Reduce Datasette Constructor Parameters  

**Current code:**
```python
def __init__(
    self,
    files=None,           # 22 parameters!
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
@dataclass
class DatasetteConfig:
    # Database configuration
    files: Optional[List[str]] = None
    immutables: Optional[List[str]] = None
    memory: bool = False
    crossdb: bool = False
    nolock: bool = False
    internal: Optional[str] = None
    
    # Web configuration  
    cache_headers: bool = True
    cors: bool = False
    secret: Optional[str] = None
    
    # Directory configuration
    config_dir: Optional[Path] = None
    template_dir: Optional[str] = None
    plugins_dir: Optional[str] = None
    static_mounts: Optional[List[Tuple[str, str]]] = None
    
    # Other configuration
    inspect_data: Optional[dict] = None
    metadata: Optional[dict] = None
    settings: Optional[dict] = None
    sqlite_extensions: Optional[List[str]] = None
    version_note: Optional[str] = None
    pdb: bool = False

class Datasette:
    def __init__(self, config: DatasetteConfig = None, **kwargs):
        # Handle backward compatibility
        if config is None:
            config = DatasetteConfig(**kwargs)
        self.config = config
        self._init_from_config()
```

**Why this matters:**
22 parameters make the constructor extremely hard to use and understand. Grouping related parameters into a configuration object improves readability and makes it easier to extend.

**Code smell addressed:**
Long Parameter List - too many parameters making function hard to use

---

#### **MAINTAINABILITY: EXTRACT-METHOD** - Break Down Long Constructor

**Current code:**
```python
def __init__(self, ...):
    # 266 lines containing:
    # - Parameter validation
    # - File discovery logic  
    # - Database initialization
    # - Plugin loading
    # - Template setup
    # - Settings validation
    # - Jinja environment setup
```

**Refactored code:**
```python
def __init__(self, config: DatasetteConfig = None, **kwargs):
    if config is None:
        config = DatasetteConfig(**kwargs)
    self.config = config
    self._init_from_config()

def _init_from_config(self):
    self._validate_config()
    self._discover_database_files()
    self._setup_databases()
    self._setup_plugins()
    self._setup_templates()
    self._setup_settings()
    self._setup_jinja_environment()

def _validate_config(self):
    """Validate configuration parameters."""
    if self.config.files is not None and isinstance(self.config.files, str):
        raise ValueError("files= must be a list of paths, not a string")
    
    if self.config.config_dir and not isinstance(self.config.config_dir, Path):
        raise ValueError("config_dir= should be a pathlib.Path")

def _discover_database_files(self):
    """Discover database files from config directory."""
    if not self.config.config_dir:
        return
        
    db_files = []
    for ext in ("db", "sqlite", "sqlite3"):
        db_files.extend(self.config.config_dir.glob(f"*.{ext}"))
    self.config.files = (self.config.files or ()) + tuple(str(f) for f in db_files)
```

**Why this matters:**
Breaking the constructor into focused methods makes the initialization process clear and testable. Each method has a single responsibility.

**Code smell addressed:**
Long Method - constructor doing too much work

---

#### **READABILITY: MAGIC-NUM** - Replace Magic Numbers with Constants

**Current code:**
```python
self._permission_checks = collections.deque(maxlen=200)

# In utils:
@dataclasses.dataclass  
class PaginatedResources:
    _limit: int = dataclasses.field(default=100, repr=False)
```

**Refactored code:**
```python
# In constants.py or at module level
DEFAULT_PERMISSION_CHECK_HISTORY = 200
DEFAULT_PAGINATION_LIMIT = 100

class Datasette:
    def __init__(self, config: DatasetteConfig):
        # ...
        self._permission_checks = collections.deque(
            maxlen=DEFAULT_PERMISSION_CHECK_HISTORY
        )

@dataclasses.dataclass  
class PaginatedResources:
    _limit: int = dataclasses.field(default=DEFAULT_PAGINATION_LIMIT, repr=False)
```

**Why this matters:**
Magic numbers lack context and are hard to maintain. Named constants make the intent clear and provide a single place to update values.

**Code smell addressed:**
Magic numbers without clear meaning

---

#### **MAINTAINABILITY: DRY-VIOLATION** - Eliminate Database Extension Logic Duplication

**Current code:**
```python
# In Datasette.__init__:
if config_dir:
    db_files = []
    for ext in ("db", "sqlite", "sqlite3"):
        db_files.extend(config_dir.glob("*.{}".format(ext)))

# In config file discovery:
metadata_files = [
    config_dir / filename
    for filename in ("metadata.json", "metadata.yaml", "metadata.yml")
    if (config_dir / filename).exists()
]
config_files = [
    config_dir / filename  
    for filename in ("datasette.json", "datasette.yaml", "datasette.yml")
    if (config_dir / filename).exists()
]
```

**Refactored code:**
```python
# In utils/file_discovery.py
DATABASE_EXTENSIONS = ("db", "sqlite", "sqlite3")
METADATA_FILENAMES = ("metadata.json", "metadata.yaml", "metadata.yml") 
CONFIG_FILENAMES = ("datasette.json", "datasette.yaml", "datasette.yml")

def find_files_with_extensions(directory: Path, extensions: Tuple[str, ...]) -> List[Path]:
    """Find all files with given extensions in directory."""
    files = []
    for ext in extensions:
        files.extend(directory.glob(f"*.{ext}"))
    return files

def find_first_existing_file(directory: Path, filenames: Tuple[str, ...]) -> Optional[Path]:
    """Find the first existing file from a list of candidate filenames."""
    for filename in filenames:
        filepath = directory / filename
        if filepath.exists():
            return filepath
    return None

# In Datasette:
def _discover_database_files(self):
    if not self.config.config_dir:
        return
    db_files = find_files_with_extensions(self.config.config_dir, DATABASE_EXTENSIONS)
    self.config.files = (self.config.files or ()) + tuple(str(f) for f in db_files)

def _load_metadata_from_config_dir(self):
    if not self.config.config_dir or self.config.metadata:
        return None
    metadata_file = find_first_existing_file(self.config.config_dir, METADATA_FILENAMES)
    return parse_metadata(metadata_file.read_text()) if metadata_file else None
```

**Why this matters:**
Centralizes file discovery logic, eliminates duplication, and makes it easy to add new file types or extensions.

**Code smell addressed:**
Duplicate Code - repeated file discovery patterns

---

#### **TESTABILITY: EXTRACT-INTERFACE** - Create Database Interface

**Current code:**
```python
class Database:
    # Concrete implementation directly used everywhere
    def execute(self, sql, params=None):
        # SQLite-specific implementation
        pass
```

**Refactored code:**
```python
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    """Abstract interface for database operations."""
    
    @abstractmethod
    async def execute(self, sql: str, params=None):
        """Execute SQL query."""
        pass
    
    @abstractmethod
    async def execute_write(self, sql: str, params=None):
        """Execute write operation."""
        pass

class SQLiteDatabase(DatabaseInterface):
    """SQLite implementation of database interface."""
    
    async def execute(self, sql: str, params=None):
        # SQLite-specific implementation
        pass
    
    async def execute_write(self, sql: str, params=None):
        # SQLite-specific implementation
        pass

class MockDatabase(DatabaseInterface):
    """Mock implementation for testing."""
    
    def __init__(self, responses: Dict[str, Any] = None):
        self.responses = responses or {}
    
    async def execute(self, sql: str, params=None):
        return self.responses.get(sql, [])
    
    async def execute_write(self, sql: str, params=None):
        return {"changes": 1}
```

**Why this matters:**
Makes the code highly testable by allowing mock databases to be injected. Follows Dependency Inversion Principle.

**Code smell addressed:**
Hard to test due to concrete dependencies

---

#### **READABILITY: COMPLEX-BOOL** - Simplify Complex Conditional Logic

**Current code:**
```python
# In load_facet_configs function:
if (
    config_dir
    and (config_dir / "inspect-data.json").exists()
    and not inspect_data
):
```

**Refactored code:**
```python
def _should_load_inspect_data_from_config(self) -> bool:
    """Check if inspect data should be loaded from config directory."""
    has_config_dir = bool(self.config.config_dir)
    inspect_file_exists = (
        has_config_dir and 
        (self.config.config_dir / "inspect-data.json").exists()
    )
    no_existing_inspect_data = not self.config.inspect_data
    
    return inspect_file_exists and no_existing_inspect_data

# Usage:
if self._should_load_inspect_data_from_config():
    inspect_data = json.loads(
        (self.config.config_dir / "inspect-data.json").read_text()
    )
```

**Why this matters:**
Complex boolean expressions are hard to understand and debug. Breaking them into named methods with clear intent improves readability.

**Code smell addressed:**
Complex Boolean Expressions - hard to understand logic

---

#### **PERFORMANCE: GEN-NOT-LIST** - Use Generators for Database File Discovery

**Current code:**
```python
db_files = []
for ext in ("db", "sqlite", "sqlite3"):
    db_files.extend(config_dir.glob("*.{}".format(ext)))
self.files += tuple(str(f) for f in db_files)
```

**Refactored code:**
```python
def _discover_database_files(self) -> Generator[str, None, None]:
    """Generator that yields database file paths."""
    if not self.config.config_dir:
        return
    
    for ext in DATABASE_EXTENSIONS:
        for file_path in self.config.config_dir.glob(f"*.{ext}"):
            yield str(file_path)

# Usage:
def _init_databases(self):
    base_files = tuple(self.config.files or [])
    discovered_files = tuple(self._discover_database_files())
    self.files = base_files + discovered_files
```

**Why this matters:**
For directories with many database files, generators provide better memory efficiency by yielding files one at a time instead of loading all into memory.

**Code smell addressed:**
Loading entire dataset into memory unnecessarily

---

### 💡 Refactoring Wisdom
> "The first rule of functions is that they should be small. The second rule of functions is that they should be smaller than that." - Robert Martin

The Datasette codebase shows good Python practices but suffers from the common issue of classes growing too large over time. The main `Datasette` class has accumulated too many responsibilities and would benefit from being broken into focused components. The 266-line constructor with 22 parameters is a clear indication that refactoring is needed.

**Priority Recommendations:**
1. **Start with the God Class** - Break down `Datasette` into focused components
2. **Extract Configuration** - Create a proper configuration object to reduce parameter lists
3. **Break Down Constructor** - Extract initialization logic into focused methods
4. **Add Interfaces** - Create abstractions for better testability
5. **Eliminate Duplication** - Centralize repeated file discovery patterns

The codebase is well-structured overall and shows good use of modern Python features. These refactorings would improve maintainability without changing the external API.


---

*Generated by Claude Code Skills Review Tool using claude*
