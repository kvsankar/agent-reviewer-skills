# python-test-reviewer Review

**Repository:** https://github.com/simonw/datasette
**Review Date:** 2025-11-12 13:29:45
**Reviewer:** python-test-reviewer
**AI Provider:** claude

---

Based on my analysis of the Datasette repository's test suite, I can now provide a comprehensive test review. Let me compile my findings:

# Test Review: Datasette Testing Strategies & Improvements

## ✅ Well-Tested Code

The Datasette test suite demonstrates several strong patterns:

- **TEST-PARAMETRIZE**: Excellent use of parametrized tests for URL handling, SQL validation, and JSON encoding functions
- **TEST-ASYNC**: Proper async test structure with `@pytest.mark.asyncio` for database operations and API endpoints
- **TEST-FIXTURES**: Well-organized fixture architecture in `conftest.py` with proper scope management
- **TEST-COVERAGE-QUALITY**: Comprehensive coverage of both happy paths and error cases in SQL validation

## 🧪 Testing Strategies & Improvements

### TEST-PARAMETRIZE - URL Component Parsing

**Code to test:**
```python
def urlsafe_components(token):
    """Splits token on commas and tilde-decodes each component"""
    return [tilde_decode(b) for b in token.split(",")]

def tilde_decode(s: str) -> str:
    "Decodes a tilde-encoded string, so ``~2Ffoo~2Fbar`` -> ``/foo/bar``"
    temp = secrets.token_hex(16)
    s = s.replace("%", temp)
    decoded = urllib.parse.unquote_plus(s.replace("~", "%"))
    return decoded.replace(temp, "%")
```

**Current Strategy: Basic Parametrize**
```python
@pytest.mark.parametrize(
    "path,expected",
    [
        ("foo", ["foo"]),
        ("foo,bar", ["foo", "bar"]),
        ("123,433,112", ["123", "433", "112"]),
        ("123~2C433,112", ["123,433", "112"]),
        ("123~2F433~2F112", ["123/433/112"]),
    ],
)
def test_urlsafe_components(path, expected):
    assert expected == utils.urlsafe_components(path)
```

**Pros:**
- Clean table format shows expected behavior
- Covers basic encoding cases

**Cons:**
- Missing edge cases (empty strings, malformed encoding)
- No error path testing
- Doesn't verify round-trip encoding/decoding

**Strategy 2: Comprehensive Edge Case Testing**
```python
@pytest.mark.parametrize("path,expected", [
    # Basic cases
    ("foo", ["foo"]),
    ("foo,bar", ["foo", "bar"]),
    
    # Encoding cases
    ("123~2C433,112", ["123,433", "112"]),
    ("123~2F433~2F112", ["123/433/112"]),
    
    # Edge cases
    ("", [""]),
    (",", ["", ""]),
    ("foo,", ["foo", ""]),
    (",bar", ["", "bar"]),
    ("foo,,bar", ["foo", "", "bar"]),
    
    # Special characters
    ("foo~20bar", ["foo bar"]),  # space
    ("foo~21bar", ["foo!bar"]),  # exclamation
    ("foo~25bar", ["foo%bar"]),  # percent preservation
])
def test_urlsafe_components_comprehensive(path, expected):
    result = utils.urlsafe_components(path)
    assert result == expected

def test_urlsafe_components_malformed_encoding():
    # Test partial encoding - should not crash
    result = utils.urlsafe_components("foo~2")
    assert isinstance(result, list)
    
def test_tilde_decode_preserves_percent():
    # Verify that existing % signs are preserved
    result = utils.tilde_decode("foo%20bar~2Cbaz")
    assert result == "foo%20bar,baz"
```

**Strategy 3: Property-Based Round-Trip Testing**
```python
from hypothesis import given, strategies as st

@given(st.lists(st.text(min_size=1, alphabet=st.characters(blacklist_categories=('Cc', 'Cs')))))
def test_urlsafe_components_roundtrip(components):
    # Test that tilde_encode -> urlsafe_components is identity
    encoded = ",".join(utils.tilde_encode(c) for c in components)
    decoded = utils.urlsafe_components(encoded)
    assert decoded == components

@given(st.text(alphabet=st.characters(blacklist_categories=('Cc', 'Cs'))))
def test_tilde_decode_properties(text):
    # Test properties of tilde encoding/decoding
    if "~" in text:
        return  # Skip if already contains tildes
    
    encoded = utils.tilde_encode(text)
    decoded = utils.tilde_decode(encoded)
    assert decoded == text
```

**Trade-offs:**
- Use **Current Strategy** for basic documentation of behavior
- Use **Strategy 2** for production systems handling user input
- Use **Strategy 3** for mathematical confidence in encoding correctness

**Recommendation:**
Combine strategies 2 and 3. The current tests document expected behavior well, but production code needs edge case testing. Add comprehensive edge cases and property-based testing for encoding correctness.

---

### TEST-EXCEPTIONS - SQL Validation Testing

**Code to test:**
```python
def validate_sql_select(sql):
    sql = "\n".join(
        line for line in sql.split("\n") if not line.strip().startswith("--")
    )
    sql = sql.strip().lower()
    if not any(r.match(sql) for r in allowed_sql_res):
        raise InvalidSql("Statement must be a SELECT")
    for r, msg in disallawed_sql_res:
        if r.search(sql):
            raise InvalidSql(msg)
```

**Current Strategy: Separate Happy/Error Parametrization**
```python
@pytest.mark.parametrize("bad_sql", [
    "update blah;",
    "PRAGMA case_sensitive_like = true",
    "SELECT * FROM pragma_not_on_allow_list('idx52')",
])
def test_validate_sql_select_bad(bad_sql):
    with pytest.raises(utils.InvalidSql):
        utils.validate_sql_select(bad_sql)

@pytest.mark.parametrize("good_sql", [
    "select count(*) from airports",
    "select foo from bar",
    "explain select 1 + 1",
])
def test_validate_sql_select_good(good_sql):
    utils.validate_sql_select(good_sql)  # Should not raise
```

**Pros:**
- Clear separation of valid/invalid cases
- Comprehensive coverage of SQL injection attempts

**Cons:**
- Doesn't verify specific error messages
- No testing of error message quality

**Strategy 2: Detailed Error Message Testing**
```python
@pytest.mark.parametrize("sql,expected_message_fragment", [
    ("update blah;", "Statement must be a SELECT"),
    ("PRAGMA case_sensitive_like = true", "PRAGMA not allowed"),
    ("SELECT * FROM pragma_not_on_allow_list('idx52')", "pragma_not_on_allow_list not allowed"),
    ("delete from users", "Statement must be a SELECT"),
    ("/* comment */ update foo set bar=1", "Statement must be a SELECT"),
])
def test_validate_sql_select_error_messages(sql, expected_message_fragment):
    with pytest.raises(utils.InvalidSql) as exc_info:
        utils.validate_sql_select(sql)
    
    assert expected_message_fragment.lower() in str(exc_info.value).lower()

def test_validate_sql_select_comment_handling():
    # Test that comments are properly stripped
    sql_with_comments = """
    -- This is a comment
    select * from users
    -- Another comment
    """
    # Should not raise - comments are stripped
    utils.validate_sql_select(sql_with_comments)
```

**Strategy 3: Security-Focused Testing**
```python
@pytest.mark.parametrize("attack_vector", [
    # SQL injection attempts
    "'; DROP TABLE users; --",
    "SELECT * FROM users; DELETE FROM users; --",
    "SELECT * FROM users UNION SELECT password FROM secrets",
    
    # Bypass attempts
    "/*comment*/ DELETE FROM users",
    "select 1; update users set admin=1",
    
    # Pragma exploitation
    "SELECT * FROM pragma_table_info('users')",
    "PRAGMA journal_mode=DELETE",
])
def test_validate_sql_select_security(attack_vector):
    with pytest.raises(utils.InvalidSql):
        utils.validate_sql_select(attack_vector)

def test_validate_sql_select_case_insensitive():
    # Ensure case variations are caught
    dangerous_variants = [
        "UPDATE users SET admin=1",
        "update users set admin=1", 
        "UpDaTe users SET admin=1",
    ]
    for variant in dangerous_variants:
        with pytest.raises(utils.InvalidSql):
            utils.validate_sql_select(variant)
```

**Trade-offs:**
- Use **Current Strategy** for basic security testing
- Use **Strategy 2** when error messages are part of user API
- Use **Strategy 3** for security-critical applications

**Recommendation:**
Adopt Strategy 2 + 3 combination. SQL validation is security-critical, so both comprehensive attack vector testing and clear error messages are essential. The current tests are good but miss edge cases.

---

### TEST-ASYNC - Database Testing Patterns

**Code to test:**
```python
class Database:
    async def execute(self, sql, params=None):
        """Execute SQL and return Results object"""
        # Database execution logic
        pass

class Results:
    def __init__(self, rows):
        self.rows = rows
    
    def first(self):
        return self.rows[0] if self.rows else None
    
    def single_value(self):
        if len(self.rows) != 1 or len(self.rows[0]) != 1:
            raise MultipleValues()
        return self.rows[0][0]
```

**Current Strategy: Direct Async Testing**
```python
@pytest.mark.asyncio
async def test_execute(db):
    results = await db.execute("select * from facetable")
    assert isinstance(results, Results)
    assert 15 == len(results)

@pytest.mark.asyncio
async def test_results_first(db):
    assert None is (await db.execute("select * from facetable where pk > 100")).first()
    results = await db.execute("select * from facetable")
    row = results.first()
    assert isinstance(row, sqlite3.Row)
```

**Pros:**
- Direct testing of async behavior
- Uses real database fixture

**Cons:**
- Tightly coupled to test database content
- Tests multiple concerns in single test
- No error path testing

**Strategy 2: Isolated Async Testing with Mocks**
```python
@pytest.mark.asyncio
async def test_database_execute_returns_results():
    # Arrange
    mock_connection = Mock()
    mock_connection.execute.return_value.fetchall.return_value = [
        ("value1", "value2"),
        ("value3", "value4")
    ]
    
    db = Database(connection=mock_connection)
    
    # Act
    results = await db.execute("SELECT * FROM test")
    
    # Assert
    assert isinstance(results, Results)
    assert len(results) == 2
    mock_connection.execute.assert_called_once_with("SELECT * FROM test", None)

@pytest.mark.asyncio 
async def test_results_single_value_success():
    # Test single value extraction
    results = Results([("single_value",)])
    
    assert results.single_value() == "single_value"

@pytest.mark.asyncio
async def test_results_single_value_multiple_rows_error():
    # Test error when multiple rows
    results = Results([("value1",), ("value2",)])
    
    with pytest.raises(MultipleValues):
        results.single_value()

@pytest.mark.asyncio
async def test_results_single_value_multiple_columns_error():
    # Test error when multiple columns
    results = Results([("value1", "value2")])
    
    with pytest.raises(MultipleValues):
        results.single_value()
```

**Strategy 3: Async Integration Testing with Test Database**
```python
@pytest.fixture
async def clean_test_db():
    """Create a clean test database for each test."""
    import tempfile
    import aiosqlite
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        async with aiosqlite.connect(temp_db.name) as conn:
            await conn.execute("""
                CREATE TABLE test_table (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    value INTEGER
                )
            """)
            await conn.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", ("test1", 100))
            await conn.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", ("test2", 200))
            await conn.commit()
            
        yield Database(temp_db.name)

@pytest.mark.asyncio
async def test_database_query_integration(clean_test_db):
    results = await clean_test_db.execute("SELECT name, value FROM test_table WHERE value > ?", (150,))
    
    assert len(results) == 1
    row = results.first()
    assert row["name"] == "test2"
    assert row["value"] == 200

@pytest.mark.asyncio
async def test_database_transaction_rollback(clean_test_db):
    # Test that errors rollback properly
    with pytest.raises(Exception):
        async with clean_test_db.transaction():
            await clean_test_db.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", ("test3", 300))
            raise Exception("Simulated error")
    
    # Verify rollback happened
    results = await clean_test_db.execute("SELECT COUNT(*) FROM test_table")
    assert results.single_value() == 2  # Original 2 rows, insert was rolled back
```

**Strategy 4: Async Error Path Testing**
```python
@pytest.mark.asyncio
async def test_database_connection_error():
    db = Database(connection_string="invalid://connection")
    
    with pytest.raises(ConnectionError):
        await db.execute("SELECT 1")

@pytest.mark.asyncio
async def test_database_sql_syntax_error(clean_test_db):
    with pytest.raises(sqlite3.OperationalError, match="syntax error"):
        await clean_test_db.execute("INVALID SQL SYNTAX")

@pytest.mark.asyncio
async def test_database_timeout(clean_test_db):
    # Test query timeout behavior
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(
            clean_test_db.execute("SELECT * FROM slow_function()"), 
            timeout=0.1
        )
```

**Trade-offs:**
- Use **Current Strategy** for simple integration testing
- Use **Strategy 2** for unit testing Results class behavior
- Use **Strategy 3** for comprehensive database integration testing  
- Use **Strategy 4** to ensure error paths are handled

**Recommendation:**
Use a combination of all strategies. Strategy 2 for fast unit tests of Results class logic, Strategy 3 for database integration confidence, and Strategy 4 for error handling. The current tests are good for happy path integration but miss unit testing and error paths.

---

### TEST-FIXTURES - Fixture Scope Optimization

**Current fixture patterns:**
```python
@pytest.fixture
def db(app_client):
    return app_client.ds.get_database("fixtures")

@pytest.fixture(scope="session", autouse=True)
def check_actions_are_documented():
    # Validation logic
    pass
```

**Strategy 1: Optimized Fixture Scoping**
```python
@pytest.fixture(scope="session")
def app_instance():
    """Create expensive app instance once per session."""
    from datasette.app import Datasette
    return Datasette(
        files=["fixtures.db"],
        metadata={"title": "Test Instance"}
    )

@pytest.fixture(scope="module")  
def db_connection(app_instance):
    """Module-scoped database connection for read-only tests."""
    return app_instance.get_database("fixtures")

@pytest.fixture
def clean_db_connection(app_instance):
    """Function-scoped clean database for write tests."""
    db = app_instance.get_database("fixtures")
    # Setup clean state
    yield db
    # Cleanup after test
    
@pytest.fixture
def api_client(app_instance):
    """Fresh API client per test."""
    return TestClient(app_instance.app)
```

**Strategy 2: Factory Fixtures for Flexibility**
```python
@pytest.fixture
def make_database():
    """Factory for creating test databases with custom data."""
    databases = []
    
    def _make_db(tables=None, metadata=None):
        import tempfile
        db_path = tempfile.mktemp(suffix='.db')
        
        # Create database with specified tables
        conn = sqlite3.connect(db_path)
        if tables:
            for table_name, schema in tables.items():
                conn.execute(f"CREATE TABLE {table_name} {schema}")
        conn.close()
        
        databases.append(db_path)
        return Database(db_path, metadata=metadata)
    
    yield _make_db
    
    # Cleanup
    for db_path in databases:
        os.unlink(db_path)

def test_custom_table_structure(make_database):
    db = make_database(tables={
        "users": "(id INTEGER PRIMARY KEY, name TEXT)",
        "posts": "(id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT)"
    })
    
    # Test with custom schema
    results = await db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in results]
    assert "users" in table_names
    assert "posts" in table_names
```

**Trade-offs:**
- Use **module/session scope** for expensive setup (database creation, app initialization)
- Use **function scope** when tests need isolation or modify state
- Use **factory fixtures** when tests need variations

**Recommendation:**
Optimize fixture scoping for performance while maintaining test isolation. Use session scope for app creation, module scope for read-only database connections, and function scope for tests that modify state.

---

### 💡 Testing Wisdom

> "The best tests tell a story about how your code should behave, not just what it currently does." - Effective Testing Patterns

**Key Improvements for Datasette:**

1. **Add Edge Case Testing**: Current parametrized tests are good but miss edge cases like empty strings, malformed input
2. **Enhance Error Message Testing**: SQL validation tests should verify error messages are helpful
3. **Add Property-Based Testing**: For encoding/decoding functions, use Hypothesis to find edge cases
4. **Optimize Fixture Scoping**: Use session/module scope for expensive setup while maintaining test isolation
5. **Add Security-Focused Testing**: SQL injection attempts and security bypasses need comprehensive coverage
6. **Separate Unit vs Integration Tests**: Mix of unit tests (mocked) and integration tests (real database) for better coverage

The Datasette test suite shows excellent testing practices overall, with room for improvement in edge case coverage and test performance optimization.


---

*Generated by Claude Code Skills Review Tool using claude*
