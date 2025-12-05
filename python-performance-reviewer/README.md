# Python Performance Reviewer Skill

A Claude Code skill that reviews Python code for performance optimization opportunities. **Comprehensive performance analysis** - covers algorithm complexity, data structures, memory management, I/O optimization, and concurrency.

## What This Skill Does

This skill transforms Claude into a Python performance expert who:
- **Identifies performance bottlenecks** - Slow algorithms, inefficient data structures, memory waste
- **Suggests optimized alternatives** - Faster algorithms, better data structures, efficient patterns
- **Provides concrete examples** - Before/after code with performance measurements
- **Explains performance impact** - Big-O analysis, speedup estimates, memory savings
- **Recommends profiling tools** - cProfile, line_profiler, memory_profiler
- **Categorizes by impact** - Critical, High, Medium, Low

## Philosophy

> **"Premature optimization is the root of all evil."** - Donald Knuth

> **"First, make it work. Then make it right. Then make it fast."** - Kent Beck

> **"Measure, don't guess."** - Performance Engineering Principle

This skill emphasizes **profile-driven optimization** - always measure before optimizing, focus on real bottlenecks, and verify improvements.

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r python-performance-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "python-performance-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r python-performance-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/python-performance-reviewer
git commit -m "Add Python Performance Reviewer skill"
```

**✅ Self-Contained:** All 50+ guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your code for performance:

```
"Review this code for performance issues"
"Find performance bottlenecks in this function"
"How can I make this faster?"
"This code is slow - optimize it"
"Review this loop for performance"
"Check for inefficient algorithms"
"Optimize this database query code"
"Find memory leaks in this code"
```

The skill will automatically activate based on keywords like:
- performance, optimize, slow, fast, bottleneck
- speed, efficiency, memory, CPU
- algorithm, complexity, O(n)
- profile, benchmark

## What You'll Get

A comprehensive performance review with:
- **Impact Classification** - Critical (10-1000x), High (2-10x), Medium (1.5-2x), Low (1.1-1.5x)
- **Slow Code** - Shows the performance issue
- **Fast Code** - Shows the optimized version
- **Performance Impact** - Speedup estimates, Big-O analysis
- **Best Practices** - When to use, pitfalls to avoid
- **Mnemonic IDs** - Easy reference (e.g., ALGO-COMPLEX, LIST-VS-SET)

### Example Review

```markdown
## Performance Review: process_users.py

### 🐌 Performance Issues

#### CRITICAL: ALGO-COMPLEX - Inefficient Algorithm (O(n²))

**Slow code:**
```python
# O(n²) - checking duplicates with nested loops
def has_duplicates(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False
```

**Fast code:**
```python
# O(n) - using set
def has_duplicates(items):
    return len(items) != len(set(items))
```

**Performance impact:**
- 1000x faster for 10,000 items (10s → 10ms)
- Reduces complexity from O(n²) to O(n)

**Related:** LIST-VS-SET, DICT-LOOKUP
```

## The 50+ Performance Guidelines

### Algorithm Complexity (8 guidelines)
- **ALGO-COMPLEX** - Choose optimal algorithm complexity (O(n) vs O(n²))
- **NESTED-LOOP** - Avoid nested loops when possible
- **LINEAR-SEARCH** - Use binary search or hash lookup instead
- **SORT-CHOICE** - Choose appropriate sorting algorithm
- **EARLY-EXIT** - Return early to avoid unnecessary work
- **CACHE-RESULT** - Cache expensive computations
- **REDUNDANT-CALC** - Eliminate redundant calculations
- **PRECOMPUTE** - Precompute values when possible

### Data Structures (10 guidelines)
- **LIST-VS-SET** - Use set for membership testing
- **DICT-LOOKUP** - Use dict for fast key lookups
- **DEQUE-USE** - Use deque for queue operations
- **DEFAULTDICT** - Use defaultdict to simplify code
- **COUNTER-USE** - Use Counter for counting
- **BISECT-USE** - Use bisect for sorted lists
- **HEAP-USE** - Use heapq for priority queues
- **NAMEDTUPLE** - Use namedtuple for lightweight objects
- **DATACLASS** - Use dataclass for simple classes
- **FROZENSET** - Use frozenset for immutable sets

### Memory Management (6 guidelines)
- **GENERATOR-USE** - Use generators for large sequences
- **ITERATOR-CHAIN** - Chain iterators instead of concatenating
- **SLOTS-USE** - Use __slots__ to reduce memory
- **DEL-UNUSED** - Delete unused objects explicitly
- **LARGE-LIST** - Avoid keeping large lists in memory
- **MEMORY-VIEW** - Use memoryview for zero-copy slicing

### String Operations (5 guidelines)
- **STRING-CONCAT** - Use join() instead of + for many strings
- **STRING-FORMAT** - Use f-strings for formatting
- **REGEX-COMPILE** - Compile regex patterns
- **STRING-METHOD** - Use str methods instead of regex
- **BYTES-VS-STR** - Use bytes for binary data

### List/Iteration (7 guidelines)
- **LIST-COMP** - Use list comprehensions
- **COMPREHENSION** - Prefer comprehensions over map/filter
- **MAP-FILTER** - Use map/filter for simple transformations
- **ENUMERATE-USE** - Use enumerate() instead of range(len())
- **ZIP-USE** - Use zip() for parallel iteration
- **REVERSED-USE** - Use reversed() instead of slicing
- **ANY-ALL** - Use any()/all() for boolean checks

### I/O Operations (6 guidelines)
- **FILE-BUFFERING** - Use buffered I/O appropriately
- **BATCH-DB** - Batch database operations
- **BULK-INSERT** - Use bulk insert methods
- **CONNECTION-POOL** - Use database connection pooling
- **LAZY-LOAD** - Lazy load large objects
- **STREAM-PROCESS** - Stream large files instead of loading

### Concurrency (5 guidelines)
- **ASYNC-IO** - Use async I/O for I/O-bound tasks
- **THREADING-USE** - Use threading for I/O-bound tasks
- **MULTIPROCESSING** - Use multiprocessing for CPU-bound tasks
- **GIL-AWARE** - Understand Python's Global Interpreter Lock
- **CONCURRENT-FUTURES** - Use concurrent.futures for clean concurrency

### Profiling & Measurement (5 guidelines)
- **PROFILE-FIRST** - Always profile before optimizing
- **TIMEIT-USE** - Use timeit for accurate benchmarks
- **MEMORY-PROFILER** - Profile memory usage
- **LINE-PROFILER** - Use line-level profiling for hotspots
- **BENCHMARK-DATA** - Benchmark with realistic data

## Key Differentiators

### Profile-Driven Optimization

Emphasizes the critical importance of profiling:
- **Measure first** - Don't guess where the bottlenecks are
- **Use tools** - cProfile, line_profiler, memory_profiler
- **Verify results** - Measure before and after optimization
- **Focus effort** - Optimize the 20% that matters

### Real Performance Impact

Every guideline includes:
- Estimated speedup (e.g., "10-100x faster")
- Big-O complexity analysis (e.g., "O(n²) → O(n)")
- Memory impact (e.g., "Constant memory vs. O(n)")
- When the optimization matters (data size thresholds)

### Practical Examples

All examples are:
- **Complete** - Copy-paste ready
- **Realistic** - Based on real-world scenarios
- **Measured** - Include performance numbers
- **Explained** - Show why it's faster

### Multiple Optimization Strategies

For each problem, shows:
- Multiple approaches with trade-offs
- When to use each approach
- Complexity analysis for each
- Real-world considerations

## Common Patterns This Skill Teaches

### ✅ Do This

```python
# Use set for membership testing
items = set(data)  # O(1) lookup
if value in items:
    ...

# Use generators for large sequences
def process_large_file(filename):
    with open(filename) as f:
        for line in f:  # Streams, doesn't load all
            yield process(line)

# Use list comprehensions
squares = [x**2 for x in range(1000)]

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    return complex_calculation(n)

# Use appropriate data structures
from collections import Counter
counts = Counter(items)  # Fast counting

# Use async for I/O-bound tasks
async def fetch_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### ❌ Not This

```python
# O(n) lookup in list
items = list(data)
if value in items:  # Slow for large lists
    ...

# Loading entire file into memory
def process_large_file(filename):
    with open(filename) as f:
        lines = f.readlines()  # Loads entire file
    return [process(line) for line in lines]

# Manual loops instead of comprehensions
squares = []
for x in range(1000):
    squares.append(x**2)

# Repeated expensive computations
for item in items:
    result = expensive_function(item.id)  # Recalculates every time

# Wrong data structure
counts = {}
for item in items:  # Manual counting
    counts[item] = counts.get(item, 0) + 1

# Synchronous I/O
def fetch_urls(urls):
    results = []
    for url in urls:
        results.append(fetch(url))  # Sequential, slow
    return results
```

## Example Use Cases

### Algorithm Optimization
- "This loop is O(n²) - how can I make it faster?"
- "Find inefficient algorithms in this code"
- "Optimize this search function"

### Memory Optimization
- "This code uses too much memory"
- "Find memory leaks"
- "How can I reduce memory usage?"

### I/O Optimization
- "This file processing is slow"
- "Optimize these database queries"
- "Speed up API calls"

### Concurrency
- "Should I use threading or multiprocessing?"
- "Make this code run in parallel"
- "Optimize this I/O-bound code"

### Pre-Production Review
- "Review for performance before deployment"
- "Find performance bottlenecks"
- "Performance audit this codebase"

## Benefits

- ✓ **Find bottlenecks** - Identify slow code before it reaches production
- ✓ **Concrete speedups** - See exact performance improvements (e.g., "10x faster")
- ✓ **Big-O analysis** - Understand algorithmic complexity
- ✓ **Memory optimization** - Reduce memory usage and prevent leaks
- ✓ **Profiling guidance** - Learn to use cProfile, line_profiler, memory_profiler
- ✓ **Best practices** - Learn when to optimize and when to keep it simple
- ✓ **Impact classification** - Prioritize fixes (Critical/High/Medium/Low)
- ✓ **Real examples** - Copy-paste ready optimizations

## What Gets Checked

### Algorithms
- Nested loops → Better complexity
- Linear search → Binary search or hash lookup
- Inefficient sorting
- Redundant calculations
- Missing caching

### Data Structures
- List → Set/Dict for lookups
- List → Deque for queues
- Manual counting → Counter
- Manual defaults → defaultdict
- Sorted lists → bisect

### Memory
- Large lists → Generators
- Unnecessary copies
- Missing __slots__
- Memory leaks
- Large objects in memory

### Strings

- `+` concatenation → `''.join(...)`
- `%` formatting → f-strings
- Repeated regex → compiled regex
- Regex → string methods

### I/O
- Loading entire files → Streaming
- Individual DB queries → Batching
- No connection pooling
- Synchronous I/O → Async I/O

### Concurrency
- Missing parallelization
- Wrong concurrency model (threading vs multiprocessing)
- GIL issues
- Race conditions

### Profiling
- No profiling data
- Guessing bottlenecks
- Missing benchmarks
- Unrealistic test data

## Supported Technologies

- **Python:** 3.7+
- **Async:** asyncio, aiohttp, aiofiles
- **Databases:** SQLAlchemy, psycopg2, pymongo, MySQL
- **Data:** pandas, numpy, scipy
- **Profiling:** cProfile, line_profiler, memory_profiler, py-spy
- **Concurrency:** threading, multiprocessing, concurrent.futures

## Sources and Attribution

All guidelines are based on:
- **Python Documentation** - Official performance tips
- **Python Performance Tips** - Community best practices
- **High Performance Python** - Book by Micha Gorelick and Ian Ozsvald
- **Fluent Python** - Book by Luciano Ramalho
- **Algorithm Analysis** - Big-O complexity theory
- **Profiling Tools Docs** - cProfile, line_profiler, memory_profiler
- **Real-World Experience** - Production performance optimization

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## Performance Philosophy

### Profile First

Never optimize without profiling:
1. Use cProfile to find slow functions
2. Use line_profiler for line-level detail
3. Use memory_profiler for memory issues
4. Measure before and after optimization

### Focus on Impact

Not all optimizations are worth it:
- **Critical** (10-1000x): Always optimize
- **High** (2-10x): Usually worth it
- **Medium** (1.5-2x): Depends on hotness
- **Low** (1.1-1.5x): Often not worth complexity

### Optimize What Matters

80/20 rule:
- 20% of code takes 80% of time
- Focus on that 20%
- Don't optimize code that rarely runs

### Keep It Readable

Avoid premature optimization:
- Readability > Performance for cold paths
- Performance > Readability for hot paths
- Profile to know which is which

## Tips for Getting the Most Out of This Skill

1. **Provide context**: "This processes 1M rows" or "This runs 1000x/sec"
2. **Share profiling data**: "cProfile shows this function takes 80% of time"
3. **Specify constraints**: "Need to reduce memory usage" or "Must be faster"
4. **Include data sizes**: "Processing 10GB files" or "100K database rows"
5. **Ask about trade-offs**: "Is this optimization worth the complexity?"

## License

This skill is provided as-is for use with Claude Code. Based on public performance best practices, Python documentation, and established algorithms.

---

**Fast code is good code. But first, make it correct. Then make it fast.**
