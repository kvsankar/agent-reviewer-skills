# Sources and Attribution

## Primary Sources

### Python Official Documentation

- **Functional Programming HOWTO**
  - URL: https://docs.python.org/3/howto/functional.html
  - Author: A.M. Kuchling
  - Guidelines: ITER-BUILTIN, MAP-FILTER, REDUCE-USE, LAMBDA-SIMPLE, GENERATOR-EXPR, FUNCTOOLS-USE, ITERTOOLS-USE, OPERATOR-USE

### Stack Builders

- **Functional Programming in Python**
  - URL: https://www.stackbuilders.com/blog/functional-programming-in-python/
  - Guidelines: PURE-FUNC, AVOID-MUTABLE-REF, IMMUTABLE-DATA, SIDE-EFFECT-FREE

### Stack Abuse

- **Functional Programming in Python: When and How to Use It**
  - URL: https://stackabuse.com/functional-programming-in-python/
  - Guidelines: FIRST-CLASS-FUNC, HIGHER-ORDER, CLOSURE-USE, DECLARATIVE-STYLE, TUPLE-IMMUTABLE, FROZENSET-USE

### ArjanCodes

- **Functional Programming Principles in Python**
  - URL: https://www.youtube.com/watch?v=F3T8tg2tVKM (YouTube)
  - Guidelines: COMPOSE-FUNC, NO-GLOBAL-STATE, REFERENTIAL-TRANSPARENT

## Guideline Categories

### Core Principles (40+ guidelines)

#### Pure Functions & Immutability
| ID | Source |
|----|--------|
| PURE-FUNC | Stack Builders |
| SIDE-EFFECT-FREE | Stack Builders |
| AVOID-MUTABLE-REF | Stack Builders |
| IMMUTABLE-DATA | Stack Builders |
| TUPLE-IMMUTABLE | Stack Abuse |
| FROZENSET-USE | Stack Abuse |

#### Higher-Order Functions
| ID | Source |
|----|--------|
| FIRST-CLASS-FUNC | Stack Abuse |
| HIGHER-ORDER | Stack Abuse |
| CLOSURE-USE | Stack Abuse |
| MAP-FILTER | Python HOWTO |
| REDUCE-USE | Python HOWTO |

#### Iterators & Generators
| ID | Source |
|----|--------|
| ITER-BUILTIN | Python HOWTO |
| GENERATOR-EXPR | Python HOWTO |
| LAZY-EVAL | Python HOWTO |
| ITERTOOLS-USE | Python HOWTO |

#### Function Composition
| ID | Source |
|----|--------|
| COMPOSE-FUNC | ArjanCodes |
| PARTIAL-USE | Python HOWTO |
| FUNCTOOLS-USE | Python HOWTO |
| OPERATOR-USE | Python HOWTO |

#### Style & Patterns
| ID | Source |
|----|--------|
| DECLARATIVE-STYLE | Stack Abuse |
| NO-GLOBAL-STATE | ArjanCodes |
| REFERENTIAL-TRANSPARENT | ArjanCodes |
| LAMBDA-SIMPLE | Python HOWTO |

## Additional References

### Books

- **Functional Programming in Python** by David Mertz (O'Reilly)
- **Fluent Python** by Luciano Ramalho (O'Reilly) - Chapter on first-class functions

### Python Standard Library

- `functools` module: https://docs.python.org/3/library/functools.html
- `itertools` module: https://docs.python.org/3/library/itertools.html
- `operator` module: https://docs.python.org/3/library/operator.html

### PEP References

- **PEP 289** - Generator Expressions
- **PEP 342** - Coroutines via Enhanced Generators
- **PEP 380** - Syntax for Delegating to a Subgenerator

## Philosophy

This skill emphasizes functional programming as a **style within Python**, not pure FP dogma:

1. **Pragmatic FP** - Use FP where it improves clarity, not everywhere
2. **Python-First** - Respect Pythonic idioms alongside FP principles
3. **Gradual Adoption** - FP patterns can be introduced incrementally
4. **Readability Matters** - FP should make code clearer, not more obscure

## Copyright Notice

- **Python Documentation** - Python Software Foundation License
- **Stack Builders Blog** - Used with attribution
- **Stack Abuse** - Used with attribution
- **ArjanCodes** - Educational content, used with attribution

## Contributing

When adding new patterns:
1. Cite the authoritative source
2. Prefer Python official docs for standard library features
3. Provide clear before/after examples
4. Explain when NOT to use FP (pragmatic approach)
