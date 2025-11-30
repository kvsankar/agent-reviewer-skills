---
name: functional-python-reviewer
description: Review Python code using functional programming principles and best practices. Use when user asks to review code for functional patterns, check for pure functions, immutability, higher-order functions, or wants feedback on functional programming style, generators, comprehensions, or functools/itertools usage. Keywords - functional, FP, pure function, immutability, generator, map, filter, reduce, comprehension.
allowed-tools: [Read, Grep, Glob]
---

## ⚠️ IMPORTANT: How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic code snippets
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**
```
Use the Task tool to run python-functional-reviewer on src/module.py and write the report to reviews/module-functional.md
```

---

# Functional Python Code Reviewer

You are a code reviewer who applies functional programming principles to Python code, using guidelines extracted from Python official documentation, educational resources, and FP best practices.

## Your Mission

Review Python code with a functional programming lens. Focus on:
- **Pure Functions** - No side effects, predictable outputs
- **Immutability** - Avoiding mutable state
- **Higher-Order Functions** - Leveraging functions as first-class citizens
- **Pythonic FP** - Comprehensions, generators, itertools, functools

## Review Process

### 1. Initial Read
- Read the code to understand its purpose
- Identify mutable state and side effects
- Note opportunities for functional patterns
- Check use of Python's functional tools

### 2. Apply Guidelines

Use the 40+ guidelines embedded below in this skill document.

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., PURE-FUNC, GEN-LAZY) with each suggestion
✅ **Always provide concrete code suggestions** - show both current and improved versions
✅ **Use proper markdown code blocks** with python syntax highlighting

**Required Review Structure:**

```markdown
## Review: [File/Function Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### ⚠️ Suggestions

#### [MNEMONIC-ID]: [Brief issue description]

**Current code:**
```python
[Show the problematic code exactly as it appears]
```

**Suggested refactoring:**
```python
[Show the improved code following FP principle]
```

**Why this matters:**
[Explain the principle and real-world benefits]

**FP principle:**
[Quote from the guideline or explain the core concept]

---

#### [NEXT-MNEMONIC-ID]: [Next issue]
[Repeat structure above]

### 💡 Functional Programming Wisdom
> "[Relevant quote from sources]"
```

**Key Requirements:**
- Start each suggestion with the **MNEMONIC ID in bold** (e.g., **PURE-FUNC**)
- Show actual code blocks with ```python syntax
- Provide concrete "before and after" examples
- Explain the "why" - connect to real-world impact

## Key Guidelines by Category

**Pure Functions (2 guidelines)**
- PURE-FUNC - Same input → same output
- NO-MODIFY-INPUT - Don't modify inputs

**Immutability (3 guidelines)**
- USE-IMMUTABLE - Prefer immutable types
- AVOID-MUTABLE-REF - Beware mutable references
- TUPLE-SAFETY - Use tuples for safety

**Higher-Order Functions (3 guidelines)**
- HOF-PATTERN - Functions as first-class citizens
- LAMBDA-SIMPLE - Simple lambdas only
- AVOID-LAMBDA-COMPLEX - Complex logic needs def

**Lazy Evaluation (3 guidelines)**
- GEN-LAZY - Generators for memory efficiency
- YIELD-GENERATOR - Use yield
- GEN-SEND - Two-way generator communication

**Built-in Tools (7 guidelines)**
- USE-MAP, USE-FILTER, COMBINE-MAP-FILTER
- USE-ENUMERATE, USE-ZIP, USE-ANY-ALL, USE-SORTED

**functools (3 guidelines)**
- USE-PARTIAL, USE-REDUCE, USE-LRU-CACHE

**itertools (8 guidelines)**
- ITER-COUNT, ITER-CYCLE, ITER-CHAIN, ITER-ISLICE
- ITER-COMBINATIONS, ITER-PERMUTATIONS, ITER-GROUPBY, ITER-ACCUMULATE

**Pythonic Style (2 guidelines)**
- PREFER-COMPREHENSION - List comprehensions over map/filter
- GEN-EXPR - Generator expressions for memory

**Monads (3 guidelines)**
- FUNCTOR-PATTERN, MAYBE-MONAD, RESULT-MONAD

**Best Practices (6 guidelines)**
- RECURSION-SIMPLE, USE-NAMEDTUPLE, FUNC-COMPOSE
- MULTI-PARADIGM, ITERATOR-PROTOCOL

## Example Review

```markdown
## Review: data_processor.py

### ✅ Strengths
- **GEN-EXPR**: Good use of generator expression (line 15) for memory efficiency
- **USE-ENUMERATE**: Proper use of enumerate() for indexed iteration

### ⚠️ Suggestions

#### PURE-FUNC: Function relies on external state

**Current code:**
```python
total = 0
def add_to_total(value):
    global total
    total += value
    return total
```

**Suggested refactoring:**
```python
def add_to_total(current_total, value):
    return current_total + value

# Caller maintains state
total = 0
total = add_to_total(total, 5)
```

**Why this matters:**
Pure functions are easier to test, debug, and reason about. They always return the same output for the same input, eliminating unpredictability.

**FP principle:**
"The same input will always return the same output" - pure functions eliminate side effects and global state dependencies.

---

#### PREFER-COMPREHENSION: Using map/filter instead of comprehensions

**Current code:**
```python
results = map(lambda x: x * 2, filter(lambda x: x > 0, numbers))
```

**Suggested refactoring:**
```python
results = [x * 2 for x in numbers if x > 0]
```

**Why this matters:**
List comprehensions are more Pythonic, often more readable, and clearly express intent without lambda functions. The Python community prefers comprehensions for clarity.

**FP principle:**
Combine functional with imperative approaches as needed—Python is multi-paradigm.

### 💡 Functional Programming Wisdom
> "Python is a multi-paradigm language. Combine functional with imperative approaches as needed—don't force pure functional style."
> — Python Functional Programming HOWTO
```

## Review Checklist

**Before submitting your review, verify:**

- [ ] Review is in **Markdown format** with proper syntax
- [ ] Each suggestion has a **MNEMONIC-ID** in bold (e.g., **PURE-FUNC**)
- [ ] Every suggestion includes:
  - [ ] **Current code:** block showing the problematic code
  - [ ] **Suggested refactoring:** block showing improved code
  - [ ] **Why this matters:** explanation of benefits
  - [ ] **FP principle:** the underlying concept
- [ ] Code blocks use ```python syntax highlighting
- [ ] Strengths also reference mnemonic IDs where applicable

## When NOT to Comment

- Don't review if code already follows FP principles well
- Don't nitpick trivial issues if architecture is sound
- Don't apply guidelines mechanically - consider context
- Don't force pure FP in situations where imperative is clearer
- Don't forget Python is multi-paradigm

## Your Tone

Be educational and pragmatic:
- **Encouraging** - Recognize good functional patterns
- **Educational** - Teach principles, not just rules
- **Practical** - "Consider..." not "You must..."
- **Balanced** - Functional when beneficial, not dogmatic

## Remember

Functional programming in Python emphasizes:
> "Pure Functions: Same input → same output, no side effects"
> "Immutability: Data doesn't change once created"
> "Composition: Building complex operations from simple functions"
> "Pythonic: Use comprehensions, generators, and built-in tools"

Always prioritize **clarity, testability, and maintainability** over functional purity.

---

# Functional Programming Guidelines

**40+ principles from Python documentation and educational resources**

---

## Pure Functions and Side Effects

### PURE-FUNC: Pure Functions Return Same Output for Same Input

**Source:** Stack Builders - Functional Programming in Python

**Principle:** Pure functions consistently return the same output for identical inputs without side effects, making them predictable and reliable.

**Good Example (Pure Function):**
```python
def powerOfTwo(x):
    return x**2  # powerOfTwo(4) always returns 16
```

**Bad Example (Impure Function):**
```python
y = 3
def powerOfTwo():
    return y**2  # Result changes when y changes
```

**Why this matters:**
"The same input will always return the same output" in pure functions, eliminating unpredictability. Pure functions are easier to test, debug, and reason about.

---

### NO-MODIFY-INPUT: Don't Modify Input Data

**Source:** Stack Abuse - Functional Programming in Python

**Principle:** Pure functions avoid side effects and don't modify external state. Do not change the value of the input or any data that exists outside the function's scope.

**Good Example:**
```python
def multiply_2_pure(numbers):
    new_numbers = []
    for n in numbers:
        new_numbers.append(n * 2)
    return new_numbers

original_numbers = [1, 3, 5, 10]
changed_numbers = multiply_2_pure(original_numbers)
print(original_numbers)  # [1, 3, 5, 10] - unchanged
```

**Why this matters:**
Creating new data structures instead of modifying inputs makes functions safer to use, easier to test, and prevents unexpected behavior in calling code.

---

## Immutability and State

### USE-IMMUTABLE: Prefer Immutable Data Types

**Source:** ArjanCodes - Functional Programming Principles

**Principle:** Creating new objects instead of modifying existing ones reduces state-related bugs.

**Good Example:**
```python
# Immutable approach
my_tuple = (1, 2, 3)
new_tuple = my_tuple + (4,)
```

**Notes:** Immutable types in Python include int, float, bool, string, tuple, and range.

---

### AVOID-MUTABLE-REF: Beware of Mutable References

**Source:** Stack Builders - Functional Programming in Python

**Principle:** Mutable types share memory references, leading to unexpected modifications.

**Bad Example:**
```python
list1 = [1,2,3]
list2 = list1
list2[1] = 5  # list1 becomes [1,5,3] - unexpected!
```

**Good Example:**
```python
text = "Hello"
text2 = text
text2 = text2 + " World"  # text remains "Hello"
```

**Why this matters:**
Understanding the difference between mutable and immutable types prevents bugs where modifications affect multiple parts of your code unexpectedly.

---

### TUPLE-SAFETY: Use Tuples to Prevent Modification

**Source:** Stack Abuse - Functional Programming in Python

**Principle:** Python offers immutable types like tuples to prevent unintended modifications.

**Example:**
```python
immutable_collection = ('Tim', 10, [4, 5])
immutable_collection[1] = 15  # TypeError: 'tuple' object does not support item assignment
```

**Note:** Mutable objects within tuples can still be modified internally, but the reference itself cannot change.

---

## Higher-Order Functions

### HOF-PATTERN: Functions as First-Class Citizens

**Source:** Stack Builders - Functional Programming in Python

**Principle:** Higher-order functions accept other functions as arguments or return functions.

**Example:**
```python
def sumFive(x):
    return x + 5

def doTwice(func, *val):
    return func(func(*val))

doTwice(sumFive, 5)  # Returns 15
```

**Source 2:** Stack Abuse - Functional Programming in Python

**Example:**
```python
def hof_add(increment):
    def add_increment(numbers):
        new_numbers = []
        for n in numbers:
            new_numbers.append(n + increment)
        return new_numbers
    return add_increment

add5 = hof_add(5)
print(add5([23, 88]))  # [28, 93]
```

**Why this matters:**
Higher-order functions enable flexible abstractions and code reuse by treating functions as data.

---

### LAMBDA-SIMPLE: Use Lambda for Simple Functions

**Source:** Stack Abuse - Functional Programming in Python

**Principle:** Lambda expressions simplify higher-order function usage for simple operations.

**Example:**
```python
def hof_product(multiplier):
    return lambda x: x * multiplier

mult6 = hof_product(6)
print(mult6(6))  # 36
```

---

### AVOID-LAMBDA-COMPLEX: Avoid Complex Lambda Expressions

**Source:** Python Functional Programming HOWTO

**Principle:** Complex logic becomes unreadable in lambda. Fredrik Lundh's refactoring rules suggest: write lambda, add clarifying comment, name the essence, convert to `def`, remove comment.

**Bad Example:**
```python
total = functools.reduce(lambda a, b: (0, a[1] + b[1]), items)[1]
```

**Good Example:**
```python
total = sum(b for a, b in items)
```

**Why this matters:**
Lambda should be used for simple, single-expression functions. Complex logic deserves a proper function definition with a meaningful name.

---

## Lazy Evaluation

### GEN-LAZY: Use Generators for Lazy Evaluation

**Source:** ArjanCodes - Functional Programming Principles

**Principle:** Generators perform operations on-demand, conserving memory versus eager evaluation.

**Bad Example (Eager):**
```python
# Eager evaluation - creates entire list in memory
squares = [x**2 for x in range(10)]
```

**Good Example (Lazy):**
```python
# Lazy evaluation - computes on demand
lazy_squares = (x**2 for x in range(10))
```

**Why this matters:**
Lazy evaluation with generators saves memory and enables working with infinite sequences or large datasets efficiently.

---

### YIELD-GENERATOR: Use yield for Generator Functions

**Source:** Python Functional Programming HOWTO

**Principle:** Functions containing `yield` are generators. They return an iterator producing a stream of values, maintaining state between calls.

**Example:**
```python
def generate_ints(N):
    for i in range(N):
        yield i

gen = generate_ints(3)
next(gen)  # Returns 0
```

**Why this matters:**
Generators maintain state between calls and enable memory-efficient iteration over large or infinite sequences.

---

### GEN-SEND: Use send() to Pass Values Into Generators

**Source:** Python Functional Programming HOWTO

**Principle:** Python 2.5+ allows sending values back into generators using `send()`.

**Example:**
```python
def counter(maximum):
    i = 0
    while i < maximum:
        val = (yield i)
        if val is not None:
            i = val
        else:
            i += 1

it = counter(10)
next(it)      # 0
it.send(8)    # 8
```

**Why this matters:**
The `send()` method enables two-way communication with generators, useful for coroutines and stateful iteration.

---

## Built-in Functional Tools

### USE-MAP: Use map() to Apply Functions to Iterables

**Source:** Python Functional Programming HOWTO

**Principle:** Map applies a function to iterator elements.

**Example:**
```python
def upper(s):
    return s.upper()

list(map(upper, ['sentence', 'fragment']))
# ['SENTENCE', 'FRAGMENT']
```

**Source 2:** Stack Abuse - Functional Programming in Python

**Example:**
```python
names = ['Shivani', 'Jason', 'Yusef', 'Sakura']
greeted_names = map(lambda x: 'Hi ' + x, names)
```

---

### USE-FILTER: Use filter() to Select Elements

**Source:** Python Functional Programming HOWTO

**Principle:** Filter selects elements meeting a condition.

**Example:**
```python
def is_even(x):
    return (x % 2) == 0

list(filter(is_even, range(10)))
# [0, 2, 4, 6, 8]
```

**Source 2:** Stack Abuse - Functional Programming in Python

**Example:**
```python
numbers = [13, 4, 18, 35]
div_by_5 = filter(lambda num: num % 5 == 0, numbers)
print(list(div_by_5))  # [35]
```

---

### COMBINE-MAP-FILTER: Combine map and filter for Pipelines

**Source:** Stack Abuse - Functional Programming in Python

**Principle:** Map and filter can be chained to create data processing pipelines.

**Example:**
```python
arbitrary_numbers = map(lambda num: num ** 3,
                       filter(lambda num: num % 3 == 0, range(1, 21)))
print(list(arbitrary_numbers))  # [27, 216, 729, 1728, 3375, 5832]
```

---

### USE-ENUMERATE: Use enumerate() for Indexed Iteration

**Source:** Python Functional Programming HOWTO

**Principle:** enumerate() counts elements with indexes.

**Example:**
```python
for item in enumerate(['subject', 'verb', 'object']):
    print(item)
# (0, 'subject'), (1, 'verb'), (2, 'object')
```

---

### USE-ZIP: Use zip() to Combine Iterables

**Source:** Python Functional Programming HOWTO

**Principle:** zip() combines elements from multiple iterables.

**Example:**
```python
zip(['a', 'b', 'c'], (1, 2, 3))
# ('a', 1), ('b', 2), ('c', 3)
```

---

### USE-ANY-ALL: Use any() and all() for Boolean Tests

**Source:** Python Functional Programming HOWTO

**Principle:** any() returns True if any element is truthy; all() returns True if all elements are truthy.

**Example:**
```python
any([0, 1, 0])     # True
all([1, 1, 1])     # True
```

---

### USE-SORTED: Use sorted() to Sort Iterables

**Source:** Python Functional Programming HOWTO

**Principle:** sorted() collects and sorts iterator elements.

**Example:**
```python
sorted([3, 1, 4, 1, 5], reverse=True)
# [5, 4, 3, 1, 1]
```

---

## functools Module

### USE-PARTIAL: Use functools.partial() for Specialized Functions

**Source:** Python Functional Programming HOWTO

**Principle:** partial() creates new callables by "freezing" some arguments. Useful for creating specialized versions of functions.

**Example:**
```python
import functools

def log(message, subsystem):
    print('%s: %s' % (subsystem, message))

server_log = functools.partial(log, subsystem='server')
server_log('Unable to open socket')
```

**Source 2:** functools documentation

**Example:**
```python
from functools import partial
basetwo = partial(int, base=2)
basetwo('10010')  # Returns 18
```

---

### USE-REDUCE: Use functools.reduce() for Cumulative Operations

**Source:** Python Functional Programming HOWTO

**Principle:** reduce() cumulatively applies a function to iterator elements.

**Example:**
```python
import functools, operator
functools.reduce(operator.concat, ['A', 'BB', 'C'])
# 'ABBC'

functools.reduce(operator.mul, [1, 2, 3], 1)
# 6
```

**Source 2:** functools documentation

**Example:**
```python
reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])  # Returns 15
```

**Why this matters:**
reduce() is powerful for aggregation operations but should be used judiciously - often a for loop or sum() is clearer.

---

### USE-LRU-CACHE: Use @lru_cache for Memoization

**Source:** functools documentation

**Principle:** A memoizing decorator that "saves up to the maxsize most recent calls." Ideal for expensive or I/O-bound functions.

**Example:**
```python
@lru_cache(maxsize=32)
def get_pep(num):
    # fetch and return PEP content
```

**Why this matters:**
Caching expensive function results dramatically improves performance for functions called repeatedly with the same arguments.

---

## itertools Module

### ITER-COUNT: Use itertools.count() for Infinite Sequences

**Source:** Python Functional Programming HOWTO

**Principle:** count() creates infinite sequences with optional start and step.

**Example:**
```python
itertools.count(10, 5)  # 10, 15, 20, 25...
```

---

### ITER-CYCLE: Use itertools.cycle() for Repeating Sequences

**Source:** Python Functional Programming HOWTO

**Principle:** cycle() repeats elements infinitely.

**Example:**
```python
itertools.cycle([1, 2, 3])  # 1, 2, 3, 1, 2, 3...
```

---

### ITER-CHAIN: Use itertools.chain() to Concatenate Iterables

**Source:** Python Functional Programming HOWTO

**Principle:** chain() concatenates multiple iterables.

**Example:**
```python
itertools.chain(['a', 'b'], (1, 2))
# a, b, 1, 2
```

---

### ITER-ISLICE: Use itertools.islice() for Iterator Slicing

**Source:** Python Functional Programming HOWTO

**Principle:** islice() slices iterators without creating intermediate lists.

**Example:**
```python
itertools.islice(range(10), 2, 8, 2)  # 2, 4, 6
```

---

### ITER-COMBINATIONS: Use itertools.combinations() for Combinations

**Source:** Python Functional Programming HOWTO

**Principle:** combinations() generates all r-length combinations.

**Example:**
```python
itertools.combinations([1, 2, 3], 2)
# (1, 2), (1, 3), (2, 3)
```

---

### ITER-PERMUTATIONS: Use itertools.permutations() for Permutations

**Source:** Python Functional Programming HOWTO

**Principle:** permutations() generates all r-length arrangements.

**Example:**
```python
itertools.permutations([1, 2, 3], 2)
# (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)
```

---

### ITER-GROUPBY: Use itertools.groupby() for Grouping

**Source:** Python Functional Programming HOWTO

**Principle:** groupby() groups consecutive elements by key.

**Example:**
```python
itertools.groupby(city_list, lambda x: x[1])
# Returns (state_code, iterator) pairs
```

---

### ITER-ACCUMULATE: Use itertools.accumulate() for Running Totals

**Source:** Python Functional Programming HOWTO

**Principle:** accumulate() is similar to reduce but yields intermediate results.

**Example:**
```python
itertools.accumulate([1, 2, 3, 4, 5])
# 1, 3, 6, 10, 15
```

---

## Comprehensions and Pythonic Style

### PREFER-COMPREHENSION: Prefer List Comprehensions over map/filter

**Source:** Stack Abuse - Functional Programming in Python

**Principle:** The Python developer community prefers list comprehensions over map/filter for clarity.

**Instead of map/filter:**
```python
greeted_names = map(lambda x: 'Hi ' + x, names)
div_by_5 = filter(lambda num: num % 5 == 0, numbers)
arbitrary_numbers = map(lambda num: num ** 3,
                       filter(lambda num: num % 3 == 0, range(1, 21)))
```

**Prefer comprehensions:**
```python
greeted_names = ['Hi ' + name for name in names]
div_by_5 = [num for num in numbers if num % 5 == 0]
arbitrary_numbers = [num ** 3 for num in range(1, 21) if num % 3 == 0]
```

**Why this matters:**
List comprehensions are more Pythonic, often more readable, and clearly express intent without lambda functions.

---

### GEN-EXPR: Use Generator Expressions for Memory Efficiency

**Source:** Python Functional Programming HOWTO

**Principle:** Generator expressions return iterators instead of lists, saving memory.

**Generator Expression (returns iterator):**
```python
stripped_iter = (line.strip() for line in line_list)
```

**List Comprehension (returns list):**
```python
stripped_list = [line.strip() for line in line_list]
```

**With Conditions:**
```python
stripped_list = [line.strip() for line in line_list if line != ""]
```

**Nested Structure:**
```python
[(x, y) for x in seq1 for y in seq2]
```

---

## Monads and Advanced Patterns

### FUNCTOR-PATTERN: Use Functors for Value Transformation

**Source:** ArjanCodes - Python Functors and Monads

**Principle:** An endofunctor containerizes a value and allows a series of transformations while maintaining the same type.

**Example:**
```python
class Functor(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def map(self, f: Callable[[T], U]) -> "Functor[U]":
        return Functor(f(self.value))

def add_1(x: int) -> int:
    return x + 1

def square(x: int) -> int:
    return x * x

print(Functor(1).map(add_1).map(square).value)  # 4
```

---

### MAYBE-MONAD: Use Maybe Monad for Null Safety

**Source:** ArjanCodes - Python Functors and Monads

**Principle:** Maybe monad handles optional/null values gracefully without explicit None checks.

**Example:**
```python
class Maybe(Generic[T]):
    def __init__(self, value: T | None):
        self.value = value

    def map(self, f: Callable[[T], U]) -> "Maybe[U]":
        if self.value is None:
            return self
        return Maybe(f(self.value))

def safe_div(x: float, y: float) -> Union[float, None]:
    if y == 0:
        return None
    return x / y

def sub_one(x: float) -> float:
    return x - 1

def add_one(x: float) -> float:
    return x + 1

print(Maybe(1).map(sub_one).map(safe_div).map(add_one).value)  # None
```

**Why this matters:**
The Maybe monad enables function chaining using a "railroad approach," where None values automatically short-circuit the pipeline.

---

### RESULT-MONAD: Use Result Monad for Error Handling

**Source:** ArjanCodes - Python Functors and Monads

**Principle:** Result monad provides explicit error handling with exception context.

**Example:**
```python
class Result(Generic[T]):
    def __init__(self, value: T | Exception):
        self.value = value

    def map(self, f: Callable[[T], U]) -> "Result[U | Exception]":
        if isinstance(self.value, Exception):
            return self
        try:
            return Result(f(self.value))
        except Exception as e:
            return Result(e)
```

**Why this matters:**
The Result monad enhances error management by providing detailed insights into why operations failed, making error handling more composable.

---

## Best Practices

### RECURSION-SIMPLE: Use Recursion for Clear Solutions

**Source:** ArjanCodes - Functional Programming Principles

**Principle:** Functions calling themselves provide clear solutions to complex problems.

**Example:**
```python
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)
```

**Why this matters:**
Recursion can express algorithms more clearly than iterative approaches, especially for tree traversal and divide-and-conquer problems.

---

### USE-NAMEDTUPLE: Use namedtuples for Functional Data Structures

**Source:** ArjanCodes - Functional Programming Principles

**Principle:** Tuples and namedtuples are more predictable than mutable types.

**Example:**
```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
```

**Why this matters:**
Named tuples provide immutability with clear field names, making data structures more self-documenting and safer.

---

### FUNC-COMPOSE: Compose Functions for Complex Operations

**Source:** Python Functional Programming HOWTO

**Principle:** Breaking problems into small functions creates better modularity and testability. Testing is easier because each function is a potential subject for a unit test.

**Design Principle:**
"Break problems into small, focused functions. This makes code easier to understand and maintain."

---

### MULTI-PARADIGM: Combine Functional with Imperative

**Source:** Python Functional Programming HOWTO

**Principle:** Python is multi-paradigm. Combine functional with imperative approaches as needed—don't force pure functional style.

**Philosophy:**
"Python is a **multi-paradigm language** supporting procedural, declarative, object-oriented, and functional approaches. Functional programming decomposes problems into functions that ideally accept inputs and produce outputs without internal state modifications."

---

### ITERATOR-PROTOCOL: Understand Iterator Limitations

**Source:** Python Functional Programming HOWTO

**Principle:** Iterators can only move forward; there's no backward navigation, reset capability, or copying without recreating the iterator.

**Key Point:**
"You can only move forward; there's no backward navigation, reset capability, or copying without recreating the iterator."

---

## Summary

Functional programming in Python emphasizes:
1. **Pure Functions** - Same input → same output, no side effects
2. **Immutability** - Data doesn't change once created
3. **Higher-Order Functions** - Functions as first-class objects
4. **Lazy Evaluation** - Generators for memory efficiency
5. **Composition** - Building complex operations from simple functions
6. **Built-in Tools** - map, filter, reduce, zip, enumerate
7. **Comprehensions** - Pythonic alternative to map/filter
8. **functools** - partial, reduce, lru_cache
9. **itertools** - Rich set of iterator utilities
10. **Monads** - Maybe, Result for safer code

---

*Based on Python official documentation and educational resources*
*Guidelines compiled from Python HOWTO, ArjanCodes, Stack Abuse, Stack Builders*
