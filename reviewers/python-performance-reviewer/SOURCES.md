# Sources and Attribution

This Python Performance Reviewer skill is based on established performance optimization techniques, algorithm analysis, and Python best practices from authoritative sources.

## Primary Sources

### 1. Python Official Documentation
**Source:** Python Software Foundation  
**URL:** https://docs.python.org/3/  
**Relevance:** Official Python documentation, performance tips, standard library optimization

**Specific sections used:**
- **Performance Tips** - https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- **Time Complexity** - https://wiki.python.org/moin/TimeComplexity
- **Data Structures** - collections, itertools, functools documentation
- **Concurrency** - threading, multiprocessing, asyncio documentation
- **Profiling** - profile and cProfile documentation

**Guidelines influenced:**
- GENERATOR-USE, ITERATOR-CHAIN (itertools best practices)
- DICT-LOOKUP, LIST-VS-SET (TimeComplexity page)
- ASYNC-IO, THREADING-USE, MULTIPROCESSING (concurrency docs)
- PROFILE-FIRST (profiling documentation)

---

### 2. High Performance Python (2nd Edition)
**Authors:** Micha Gorelick and Ian Ozsvald  
**Publisher:** O'Reilly Media (2020)  
**ISBN:** 978-1492055020  
**Relevance:** Comprehensive guide to Python performance optimization

**Key concepts adopted:**
- Profiling-driven optimization (Chapter 2)
- Memory management and generators (Chapter 3)
- Matrix and vector computation (Chapter 6)
- Concurrency patterns (Chapter 9)
- Multiprocessing vs threading (Chapter 9)

**Guidelines influenced:**
- PROFILE-FIRST, LINE-PROFILER, MEMORY-PROFILER
- GENERATOR-USE, MEMORY-VIEW, SLOTS-USE
- ALGO-COMPLEX, NESTED-LOOP
- GIL-AWARE, MULTIPROCESSING, THREADING-USE
- BENCHMARK-DATA, TIMEIT-USE

---

### 3. Fluent Python (2nd Edition)
**Author:** Luciano Ramalho  
**Publisher:** O'Reilly Media (2022)  
**ISBN:** 978-1492056355  
**Relevance:** Pythonic patterns and performance considerations

**Key concepts adopted:**
- Data structures and algorithms (Part II)
- Generator expressions and iterators (Chapter 17)
- Context managers and with blocks (Chapter 18)
- Concurrency models (Part V)
- Attribute descriptors and slots (Chapter 22)

**Guidelines influenced:**
- LIST-COMP, COMPREHENSION, ENUMERATE-USE, ZIP-USE
- GENERATOR-USE, ITERATOR-CHAIN
- DEQUE-USE, DEFAULTDICT, COUNTER-USE
- SLOTS-USE, NAMEDTUPLE, DATACLASS
- ASYNC-IO, CONCURRENT-FUTURES

---

### 4. Algorithm Analysis and Complexity Theory
**Sources:**
- **Introduction to Algorithms** by Cormen, Leiserson, Rivest, and Stein (CLRS)
- **Algorithm Design Manual** by Steven Skiena
- **Big-O Cheat Sheet** - https://www.bigocheatsheet.com/

**Relevance:** Algorithmic complexity analysis, Big-O notation, data structure time complexity

**Key concepts adopted:**
- Big-O notation (O(1), O(n), O(n log n), O(n²))
- Best/average/worst case analysis
- Space vs time trade-offs
- Data structure complexity (lists, sets, dicts, heaps)

**Guidelines influenced:**
- ALGO-COMPLEX - Algorithm complexity optimization
- NESTED-LOOP - O(n²) → O(n) or O(n log n)
- LINEAR-SEARCH - O(n) → O(log n) or O(1)
- SORT-CHOICE - O(n log n) sorting algorithms
- LIST-VS-SET - O(n) → O(1) membership testing
- DICT-LOOKUP - O(1) hash table lookups
- HEAP-USE - O(log n) priority queue operations
- BISECT-USE - O(log n) binary search

---

### 5. Python Performance Profiling Tools

#### cProfile
**Source:** Python Standard Library  
**Documentation:** https://docs.python.org/3/library/profile.html  
**Relevance:** Built-in function-level profiling

**Guidelines influenced:**
- PROFILE-FIRST - Profile before optimizing

#### line_profiler
**Author:** Robert Kern  
**Repository:** https://github.com/pyutils/line_profiler  
**Relevance:** Line-by-line profiling for detailed analysis

**Guidelines influenced:**
- LINE-PROFILER - Line-level profiling for hotspots

#### memory_profiler
**Author:** Fabian Pedregosa and Philippe Gervais  
**Repository:** https://github.com/pythonprofilers/memory_profiler  
**Relevance:** Memory usage profiling

**Guidelines influenced:**
- MEMORY-PROFILER - Profile memory usage

#### py-spy
**Author:** Ben Frederickson  
**Repository:** https://github.com/benfred/py-spy  
**Relevance:** Sampling profiler for production

**Guidelines influenced:**
- PROFILE-FIRST - Production profiling techniques

---

### 6. Python String Performance
**Sources:**
- Python Wiki - https://wiki.python.org/moin/PythonSpeed/PerformanceTips#String_Concatenation
- Python str documentation
- PEP 498 - Literal String Interpolation (f-strings)

**Key concepts adopted:**
- String concatenation with join() is O(n), + is O(n²)
- f-strings are faster than % or .format()
- Compiled regex is faster for repeated patterns
- bytes vs str for binary data

**Guidelines influenced:**
- STRING-CONCAT - Use join() for multiple strings
- STRING-FORMAT - Use f-strings for formatting
- REGEX-COMPILE - Compile regex patterns
- STRING-METHOD - Use str methods over regex
- BYTES-VS-STR - Use bytes for binary data

---

### 7. Database Performance Best Practices
**Sources:**
- SQLAlchemy documentation - https://docs.sqlalchemy.org/
- PostgreSQL documentation - https://www.postgresql.org/docs/
- MySQL documentation - https://dev.mysql.com/doc/
- Django ORM documentation - https://docs.djangoproject.com/

**Key concepts adopted:**
- Batch operations reduce roundtrips
- Connection pooling reuses connections
- Bulk inserts bypass SQL parsing
- Lazy loading reduces initial queries
- N+1 query problem

**Guidelines influenced:**
- BATCH-DB - Batch database operations
- BULK-INSERT - Use bulk insert methods
- CONNECTION-POOL - Use connection pooling
- LAZY-LOAD - Lazy load large objects

---

### 8. Python Concurrency Models
**Sources:**
- Python asyncio documentation - https://docs.python.org/3/library/asyncio.html
- PEP 3156 - Asynchronous IO Support
- David Beazley - "Understanding the Python GIL" (PyCon 2010)
- Python threading documentation
- Python multiprocessing documentation

**Key concepts adopted:**
- GIL prevents true parallelism in pure Python
- asyncio for I/O-bound tasks (non-blocking)
- threading for I/O-bound with blocking libraries
- multiprocessing for CPU-bound tasks
- concurrent.futures for clean concurrency API

**Guidelines influenced:**
- ASYNC-IO - Async I/O for I/O-bound tasks
- THREADING-USE - Threading for I/O-bound tasks
- MULTIPROCESSING - Multiprocessing for CPU-bound tasks
- GIL-AWARE - Understand the Global Interpreter Lock
- CONCURRENT-FUTURES - Clean concurrency API

---

### 9. Python Data Structures (collections module)
**Source:** Python Standard Library - collections  
**Documentation:** https://docs.python.org/3/library/collections.html  
**Relevance:** Specialized container datatypes

**Key concepts adopted:**
- deque for O(1) append/pop on both ends
- defaultdict for automatic default values
- Counter for efficient counting
- namedtuple for lightweight records
- ChainMap for chaining mappings

**Guidelines influenced:**
- DEQUE-USE - Use deque for queues
- DEFAULTDICT - Use defaultdict
- COUNTER-USE - Use Counter for counting
- NAMEDTUPLE - Use namedtuple for lightweight objects

---

### 10. Memory Management and Optimization
**Sources:**
- Python Memory Management documentation
- **Python 3 Patterns, Recipes and Idioms** by Bruce Eckel
- **Effective Python** (2nd Edition) by Brett Slatkin

**Key concepts adopted:**
- Generators for memory efficiency
- __slots__ reduces memory overhead
- memoryview for zero-copy buffer access
- del for explicit garbage collection hints
- Reference counting and cyclic GC

**Guidelines influenced:**
- GENERATOR-USE - Generators for large sequences
- SLOTS-USE - Use __slots__ to reduce memory
- MEMORY-VIEW - Zero-copy slicing with memoryview
- DEL-UNUSED - Delete unused objects
- LARGE-LIST - Avoid large lists in memory
- ITERATOR-CHAIN - Chain iterators

---

### 11. File I/O and Streaming
**Sources:**
- Python io module documentation
- Pandas documentation - chunking
- CSV module documentation

**Key concepts adopted:**
- Buffered I/O for performance
- Streaming large files line-by-line
- Chunking with pandas
- Binary vs text mode

**Guidelines influenced:**
- FILE-BUFFERING - Use buffered I/O
- STREAM-PROCESS - Stream large files
- LAZY-LOAD - Lazy loading strategies

---

### 12. Python Idioms and Best Practices
**Sources:**
- **Effective Python** (2nd Edition) by Brett Slatkin
- **Python Cookbook** (3rd Edition) by David Beazley and Brian K. Jones
- PEP 8 - Style Guide for Python Code
- PEP 20 - The Zen of Python

**Key concepts adopted:**
- List comprehensions are faster than loops
- enumerate() is more Pythonic than range(len())
- zip() for parallel iteration
- any()/all() for boolean checks
- Early returns for efficiency

**Guidelines influenced:**
- LIST-COMP - Use list comprehensions
- COMPREHENSION - Prefer comprehensions
- ENUMERATE-USE - Use enumerate()
- ZIP-USE - Use zip()
- ANY-ALL - Use any()/all()
- EARLY-EXIT - Return early
- REVERSED-USE - Use reversed()

---

### 13. Scientific Python Performance
**Sources:**
- NumPy documentation - https://numpy.org/doc/
- Pandas documentation - https://pandas.pydata.org/docs/
- SciPy documentation - https://docs.scipy.org/

**Key concepts adopted:**
- Vectorized operations in NumPy
- Pandas optimizations (vectorization, categoricals)
- Binary search with bisect
- Heap operations with heapq

**Guidelines influenced:**
- BISECT-USE - Binary search on sorted lists
- HEAP-USE - Priority queues with heapq
- MEMORY-VIEW - Buffer protocol usage

---

### 14. Benchmarking and Testing
**Sources:**
- timeit module documentation
- pytest-benchmark documentation
- Python Performance Testing best practices

**Key concepts adopted:**
- timeit for micro-benchmarks
- Multiple runs for statistical validity
- Realistic data for benchmarks
- Comparing multiple approaches

**Guidelines influenced:**
- TIMEIT-USE - Accurate micro-benchmarks
- BENCHMARK-DATA - Realistic test data
- PROFILE-FIRST - Measure before optimizing

---

### 15. Caching and Memoization
**Sources:**
- functools module documentation - lru_cache
- Python caching strategies

**Key concepts adopted:**
- LRU cache for repeated computations
- Memoization patterns
- Cache invalidation strategies

**Guidelines influenced:**
- CACHE-RESULT - Cache expensive computations
- PRECOMPUTE - Precompute when possible

---

## Research Methodology

The guidelines in this skill were developed through:

1. **Literature Review**
   - Studied authoritative books on Python performance
   - Reviewed official Python documentation
   - Analyzed algorithm textbooks for complexity theory

2. **Profiling Analysis**
   - Used cProfile, line_profiler, memory_profiler on real code
   - Measured actual performance improvements
   - Tested different data sizes for scalability

3. **Benchmark Testing**
   - Created micro-benchmarks for each optimization
   - Measured speedups (e.g., "10x faster")
   - Tested with realistic data distributions

4. **Community Best Practices**
   - Reviewed Python PEPs (Python Enhancement Proposals)
   - Studied high-performance Python libraries (NumPy, Pandas)
   - Analyzed production code patterns

5. **Tool Documentation**
   - Studied profiling tools (cProfile, line_profiler, memory_profiler)
   - Reviewed asyncio and concurrency libraries
   - Analyzed database library documentation

## Additional Resources

### Books
- **High Performance Python** (2nd Edition) by Gorelick & Ozsvald - O'Reilly, 2020
- **Fluent Python** (2nd Edition) by Luciano Ramalho - O'Reilly, 2022
- **Effective Python** (2nd Edition) by Brett Slatkin - Addison-Wesley, 2019
- **Introduction to Algorithms** (CLRS) - MIT Press, 2009
- **Python Cookbook** (3rd Edition) by Beazley & Jones - O'Reilly, 2013

### Online Resources
- Python Performance Tips - https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- Time Complexity - https://wiki.python.org/moin/TimeComplexity
- Big-O Cheat Sheet - https://www.bigocheatsheet.com/
- Python Module of the Week - https://pymotw.com/

### Tools
- cProfile - https://docs.python.org/3/library/profile.html
- line_profiler - https://github.com/pyutils/line_profiler
- memory_profiler - https://github.com/pythonprofilers/memory_profiler
- py-spy - https://github.com/benfred/py-spy
- scalene - https://github.com/plasma-umass/scalene

### Talks and Presentations
- "Understanding the Python GIL" - David Beazley (PyCon 2010)
- "Fast Python, Slow Python" - Alex Gaynor (PyCon 2014)
- "Performance Python" - Łukasz Langa (PyCon 2016)

## Attribution Note

This skill synthesizes knowledge from multiple authoritative sources to provide comprehensive Python performance guidance. All recommendations are based on established best practices, measured performance data, and algorithmic analysis from the sources listed above.

The examples are original implementations demonstrating the principles from these sources, adapted for practical use with Claude Code.

## Version History

- **v1.0** (2025-01-19) - Initial release with 50+ performance guidelines
  - Algorithm complexity optimization (8 guidelines)
  - Data structures (10 guidelines)
  - Memory management (6 guidelines)
  - String operations (5 guidelines)
  - List/iteration (7 guidelines)
  - I/O operations (6 guidelines)
  - Concurrency (5 guidelines)
  - Profiling & measurement (5 guidelines)

---

**All sources are publicly available and represent industry-standard best practices for Python performance optimization.**
