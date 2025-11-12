# functional-python-reviewer Review

**Repository:** https://github.com/simonw/datasette
**Review Date:** 2025-11-12 13:23:31
**Reviewer:** functional-python-reviewer
**AI Provider:** claude

---

Now I have sufficient understanding of the codebase. I can see several areas where functional programming principles could improve the code. Let me write my comprehensive review:

## Review: Datasette Codebase - Functional Programming Analysis

### ✅ Strengths

- **USE-NAMEDTUPLE**: Good use of namedtuples for immutable data structures (line 25, PaginatedResources dataclass)
- **GEN-EXPR**: Effective use of generator expressions throughout, especially in `tilde_encode` function (utils/__init__.py:371)
- **USE-ENUMERATE**: Proper use of enumerate() in various iterator contexts
- **PREFER-COMPREHENSION**: Good use of list comprehensions over map/filter in many places, such as `path_from_row_pks` function

### ⚠️ Suggestions

#### PURE-FUNC: Functions with Side Effects Should Be Made Pure

**Current code:**
```python
def count_params(params):
    nonlocal count
    for param in params:
        count += 1
        yield param
```
*database.py:155-160*

**Suggested refactoring:**
```python
def count_params_pure(params):
    """Pure generator that yields params and returns count separately."""
    params_list = list(params)
    count = len(params_list)
    return (param for param in params_list), count

# Usage in execute_write_many:
def _inner(conn):
    param_generator, count = count_params_pure(params_seq)
    return conn.executemany(sql, param_generator), count
```

**Why this matters:**
The current `count_params` function has side effects by modifying the `count` variable from its enclosing scope. Pure functions are easier to test, debug, and reason about.

**FP principle:**
Pure functions consistently return the same output for identical inputs without side effects, making them predictable and reliable.

---

#### USE-REDUCE: Replace Manual Accumulation with functools.reduce

**Current code:**
```python
def compound_keys_after_sql(pks, start_index=0):
    or_clauses = []
    pks_left = pks[:]
    while pks_left:
        and_clauses = []
        last = pks_left[-1]
        rest = pks_left[:-1]
        and_clauses = [
            f"{escape_sqlite(pk)} = :p{i + start_index}" for i, pk in enumerate(rest)
        ]
        and_clauses.append(f"{escape_sqlite(last)} > :p{len(rest) + start_index}")
        or_clauses.append(f"({' and '.join(and_clauses)})")
        pks_left.pop()
    or_clauses.reverse()
    return "({})".format("\n  or\n".join(or_clauses))
```
*utils/__init__.py:195-215*

**Suggested refactoring:**
```python
from functools import reduce

def compound_keys_after_sql(pks, start_index=0):
    def build_or_clause(pks_subset):
        *rest, last = pks_subset
        and_clauses = [
            f"{escape_sqlite(pk)} = :p{i + start_index}" 
            for i, pk in enumerate(rest)
        ]
        and_clauses.append(f"{escape_sqlite(last)} > :p{len(rest) + start_index}")
        return f"({' and '.join(and_clauses)})"
    
    # Create all subsequences: [pks], [pks[:-1]], [pks[:-2]], etc.
    subsequences = [pks[:i+1] for i in range(len(pks))]
    or_clauses = [build_or_clause(subseq) for subseq in subsequences]
    
    return "({})".format("\n  or\n".join(or_clauses))
```

**Why this matters:**
The refactored version eliminates mutable state (`pks_left.pop()`) and uses functional composition to build the result. It's more declarative about the intent of creating subsequences.

**FP principle:**
Avoid mutable state and side effects. Use functional composition to build complex operations from simple functions.

---

#### PREFER-COMPREHENSION: Replace filter() with List Comprehension

**Current code:**
```python
def get_outbound_foreign_keys(conn, table):
    # ... existing code ...
    id_counts = Counter(fk["id"] for fk in fks)
    return [
        {
            "column": fk["column"],
            "other_table": fk["other_table"],
            "other_column": fk["other_column"],
        }
        for fk in fks
        if id_counts[fk["id"]] == 1
    ]
```
*utils/__init__.py:580-595*

**Suggested refactoring:**
```python
def get_outbound_foreign_keys(conn, table):
    """Get outbound foreign keys, filtering out compound keys."""
    infos = conn.execute(f"PRAGMA foreign_key_list([{table}])").fetchall()
    
    # Transform raw pragma results to structured data
    fks = [
        {
            "column": from_,
            "other_table": table_name,
            "other_column": to_,
            "id": id,
            "seq": seq,
        }
        for info in infos
        if info is not None
        for id, seq, table_name, from_, to_, on_update, on_delete, match in [info]
    ]
    
    # Filter out compound foreign keys using comprehension
    id_counts = Counter(fk["id"] for fk in fks)
    return [
        {
            "column": fk["column"],
            "other_table": fk["other_table"],
            "other_column": fk["other_column"],
        }
        for fk in fks
        if id_counts[fk["id"]] == 1
    ]
```

**Why this matters:**
The current code is already well-written with comprehensions, but the initial transformation could be more functional by avoiding the manual unpacking loop.

**FP principle:**
List comprehensions are more Pythonic and often more readable than map/filter combinations.

---

#### FUNC-COMPOSE: Break Down Complex Functions

**Current code:**
```python
def filters_should_redirect(special_args):
    redirect_params = []
    # Handle _filter_column=foo&_filter_op=exact&_filter_value=...
    filter_column = special_args.get("_filter_column")
    filter_op = special_args.get("_filter_op") or ""
    filter_value = special_args.get("_filter_value") or ""
    if "__" in filter_op:
        filter_op, filter_value = filter_op.split("__", 1)
    if filter_column:
        redirect_params.append((f"{filter_column}__{filter_op}", filter_value))
    for key in ("_filter_column", "_filter_op", "_filter_value"):
        if key in special_args:
            redirect_params.append((key, None))
    # Now handle _filter_column_1=name&_filter_op_1=contains&_filter_value_1=hello
    column_keys = [k for k in special_args if filter_column_re.match(k)]
    for column_key in column_keys:
        number = column_key.split("_")[-1]
        column = special_args[column_key]
        op = special_args.get(f"_filter_op_{number}") or "exact"
        value = special_args.get(f"_filter_value_{number}") or ""
        if "__" in op:
            op, value = op.split("__", 1)
        if column:
            redirect_params.append((f"{column}__{op}", value))
        redirect_params.extend(
            [
                (f"_filter_column_{number}", None),
                (f"_filter_op_{number}", None),
                (f"_filter_value_{number}", None),
            ]
        )
    return redirect_params
```
*utils/__init__.py:709-750*

**Suggested refactoring:**
```python
def parse_filter_args(special_args):
    """Parse single filter arguments (_filter_column, _filter_op, _filter_value)."""
    filter_column = special_args.get("_filter_column")
    filter_op = special_args.get("_filter_op") or ""
    filter_value = special_args.get("_filter_value") or ""
    
    if "__" in filter_op:
        filter_op, filter_value = filter_op.split("__", 1)
    
    params = []
    if filter_column:
        params.append((f"{filter_column}__{filter_op}", filter_value))
    
    # Add cleanup params
    params.extend(
        (key, None) for key in ("_filter_column", "_filter_op", "_filter_value")
        if key in special_args
    )
    return params

def parse_numbered_filter_args(special_args):
    """Parse numbered filter arguments (_filter_column_1, etc.)."""
    column_keys = [k for k in special_args if filter_column_re.match(k)]
    params = []
    
    for column_key in column_keys:
        number = column_key.split("_")[-1]
        column = special_args[column_key]
        op = special_args.get(f"_filter_op_{number}") or "exact"
        value = special_args.get(f"_filter_value_{number}") or ""
        
        if "__" in op:
            op, value = op.split("__", 1)
        
        if column:
            params.append((f"{column}__{op}", value))
        
        # Add cleanup params
        params.extend([
            (f"_filter_column_{number}", None),
            (f"_filter_op_{number}", None),
            (f"_filter_value_{number}", None),
        ])
    
    return params

def filters_should_redirect(special_args):
    """Determine redirect parameters for filter arguments."""
    return (
        parse_filter_args(special_args) + 
        parse_numbered_filter_args(special_args)
    )
```

**Why this matters:**
Breaking the complex function into smaller, focused functions makes the code easier to understand, test, and maintain. Each function has a single responsibility.

**FP principle:**
"Break problems into small, focused functions. This makes code easier to understand and maintain."

---

#### USE-IMMUTABLE: Replace Mutable Default Arguments

**Current code:**
```python
def path_from_row_pks(row, pks, use_rowid, quote=True):
    """Generate an optionally tilde-encoded unique identifier
    for a row from its primary keys."""
    if use_rowid:
        bits = [row["rowid"]]
    else:
        bits = [
            row[pk]["value"] if isinstance(row[pk], dict) else row[pk] for pk in pks
        ]
    if quote:
        bits = [tilde_encode(str(bit)) for bit in bits]
    else:
        bits = [str(bit) for bit in bits]

    return ",".join(bits)
```
*utils/__init__.py:178-192*

**Suggested refactoring:**
```python
def path_from_row_pks(row, pks, use_rowid, quote=True):
    """Generate an optionally tilde-encoded unique identifier
    for a row from its primary keys."""
    # Extract values functionally
    if use_rowid:
        raw_bits = (row["rowid"],)
    else:
        raw_bits = tuple(
            row[pk]["value"] if isinstance(row[pk], dict) else row[pk] 
            for pk in pks
        )
    
    # Transform values functionally
    string_bits = tuple(map(str, raw_bits))
    final_bits = tuple(map(tilde_encode, string_bits)) if quote else string_bits
    
    return ",".join(final_bits)
```

**Why this matters:**
Using tuples instead of lists emphasizes immutability. The functional approach with map makes the transformations more explicit and composable.

**FP principle:**
Prefer immutable data types and functional transformations over mutable operations.

---

#### MAYBE-MONAD: Improve Null Safety in Dictionary Access

**Current code:**
```python
async def initial_path_for_datasette(datasette):
    """Return suggested path for opening this Datasette, based on number of DBs and tables"""
    databases = dict([p for p in datasette.databases.items() if p[0] != "_internal"])
    if len(databases) == 1:
        db_name = next(iter(databases.keys()))
        path = datasette.urls.database(db_name)
        # Does this DB only have one table?
        db = next(iter(databases.values()))
        tables = await db.table_names()
        # ... continues with nested conditionals
```
*utils/__init__.py:1220-1240*

**Suggested refactoring:**
```python
from typing import Optional

class Maybe:
    def __init__(self, value):
        self.value = value
    
    def map(self, func):
        if self.value is None:
            return Maybe(None)
        try:
            return Maybe(func(self.value))
        except:
            return Maybe(None)
    
    def flat_map(self, func):
        if self.value is None:
            return Maybe(None)
        return func(self.value)

async def initial_path_for_datasette(datasette):
    """Return suggested path using Maybe monad for safer navigation."""
    databases = {
        name: db for name, db in datasette.databases.items() 
        if name != "_internal"
    }
    
    def get_single_db(databases_dict):
        return next(iter(databases_dict.values())) if len(databases_dict) == 1 else None
    
    def get_db_name(databases_dict):
        return next(iter(databases_dict.keys())) if len(databases_dict) == 1 else None
    
    async def get_single_table_path(db):
        tables = await db.table_names()
        if len(tables) == 1:
            return datasette.urls.table(db.name, tables[0])
        return datasette.urls.database(db.name)
    
    result = await (Maybe(databases)
                   .map(get_single_db)
                   .flat_map(lambda db: Maybe(db))
                   .map(lambda db: get_single_table_path(db)))
    
    return result.value if result.value else datasette.urls.index()
```

**Why this matters:**
The Maybe monad pattern helps avoid nested None checks and makes error handling more composable. It provides a cleaner way to handle the optional chain of database → table lookups.

**FP principle:**
Maybe monad handles optional/null values gracefully without explicit None checks using a "railroad approach."

---

#### ITER-CHAIN: Use itertools.chain() for Sequence Concatenation

**Current code:**
```python
def resolve_env_secrets(config, environ):
    """Create copy that recursively replaces {"$env": "NAME"} with values from environ"""
    if isinstance(config, dict):
        if list(config.keys()) == ["$env"]:
            return environ.get(list(config.values())[0])
        elif list(config.keys()) == ["$file"]:
            with open(list(config.values())[0]) as fp:
                return fp.read()
        else:
            return {
                key: resolve_env_secrets(value, environ)
                for key, value in config.items()
            }
    elif isinstance(config, list):
        return [resolve_env_secrets(value, environ) for value in config]
    else:
        return config
```
*utils/__init__.py:1110-1125*

**Suggested refactoring:**
```python
from functools import singledispatch

@singledispatch
def resolve_env_secrets(config, environ):
    """Default case: return config as-is."""
    return config

@resolve_env_secrets.register
def _(config: dict, environ):
    """Handle dictionary configurations."""
    keys = list(config.keys())
    
    if keys == ["$env"]:
        return environ.get(list(config.values())[0])
    elif keys == ["$file"]:
        with open(list(config.values())[0]) as fp:
            return fp.read()
    else:
        return {
            key: resolve_env_secrets(value, environ)
            for key, value in config.items()
        }

@resolve_env_secrets.register
def _(config: list, environ):
    """Handle list configurations."""
    return [resolve_env_secrets(value, environ) for value in config]
```

**Why this matters:**
Using `@singledispatch` makes the type-based branching more explicit and extensible. This is a functional programming pattern that eliminates the isinstance checks.

**FP principle:**
Use functional dispatching patterns instead of explicit type checking for cleaner, more extensible code.

### 💡 Functional Programming Wisdom

> "Python is a multi-paradigm language. Combine functional with imperative approaches as needed—don't force pure functional style."
> — Python Functional Programming HOWTO

The Datasette codebase already demonstrates good functional programming practices in many areas, particularly with its use of comprehensions and generator expressions. The suggested improvements focus on making functions more pure, reducing mutable state, and leveraging Python's functional tools for cleaner, more maintainable code.


---

*Generated by Claude Code Skills Review Tool using claude*
