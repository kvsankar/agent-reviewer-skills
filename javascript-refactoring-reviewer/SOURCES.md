# Sources and References

## Methodology

This JavaScript Refactoring Reviewer skill was created through extensive research of authoritative refactoring resources, design principles, and modern JavaScript best practices. The skill provides concrete before/after refactoring examples based on established patterns from the software engineering community.

**Philosophy:** Teach developers HOW to refactor JavaScript/TypeScript code systematically, following proven principles (SOLID, DRY) and modern JavaScript patterns (ES6+).

**Created:** January 2025

---

## Primary Sources

### 1. Refactoring Guru

- **Official URL:** https://refactoring.guru/
- **Used for:** Refactoring catalog, code smells, design patterns
- **License:** Content available for educational use
- **Key Topics:**
  - Code smells (Bloaters, OO Abusers, Change Preventers, Dispensables, Couplers)
  - Refactoring techniques (Extract Method, Inline Method, Move Method, etc.)
  - Design patterns (Creational, Structural, Behavioral)
  - SOLID principles with examples

**Relevant Guidelines:**
- EXTRACT-FUNC - Extract Method refactoring
- EXTRACT-CLASS - Extract Class refactoring
- LONG-FUNC - Long Method code smell
- GOD-CLASS - Large Class code smell
- FEATURE-ENVY - Feature Envy code smell
- MESSAGE-CHAIN - Message Chains code smell
- MIDDLE-MAN - Middle Man code smell
- SWITCH-STMT - Replace Conditional with Polymorphism
- DATA-CLUMP - Data Clumps code smell
- PRIMITIVE-OBS - Primitive Obsession code smell

**Key Resources:**
- "Code Smells" - https://refactoring.guru/refactoring/smells
- "Refactoring Techniques" - https://refactoring.guru/refactoring/techniques
- "SOLID Principles" - https://refactoring.guru/design-patterns/principles

**Philosophy:**
> "Refactoring is a controlled technique for improving the design of an existing code base."

---

### 2. clean-code-javascript

- **Repository:** https://github.com/ryanmcdermott/clean-code-javascript
- **Author:** Ryan McDermott
- **License:** MIT License
- **Used for:** JavaScript-specific clean code principles adapted from Robert C. Martin's "Clean Code"

**Key Topics:**
- Variables (meaningful names, pronounceable names, searchable names)
- Functions (small, single responsibility, descriptive names)
- Objects and Data Structures
- Classes (SOLID principles)
- Error Handling
- Formatting
- Comments

**Relevant Guidelines:**
- MEANINGFUL-NAME - Use meaningful variable names
- PRONOUNCE-NAME - Use pronounceable names
- SEARCHABLE-NAME - Use searchable names
- AVOID-MENTAL-MAP - Avoid mental mapping
- MAGIC-NUM - Replace magic numbers
- SRP-VIOLATION - Single Responsibility Principle
- DRY-VIOLATION - Don't Repeat Yourself

**Key Quotes:**
> "Code is read much more often than it is written."
> "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

**Statistics:**
- 91k+ GitHub stars
- Most popular clean code guide for JavaScript

---

### 3. Martin Fowler - Refactoring

- **Book:** "Refactoring: Improving the Design of Existing Code" (2nd Edition)
- **Website:** https://martinfowler.com/
- **Author:** Martin Fowler
- **Used for:** Refactoring principles, catalog, and philosophy

**Key Principles:**
1. **Two Hats** - Adding function vs. refactoring (never both)
2. **Small Steps** - Incremental changes with tests
3. **Code Smells** - Indicators that code needs refactoring
4. **Refactoring Catalog** - Systematic refactoring techniques

**Relevant Guidelines:**
- EXTRACT-FUNC - Extract Function
- DECOMPOSE-COND - Decompose Conditional
- LONG-PARAM - Introduce Parameter Object
- SHOT-GUN - Shotgun Surgery code smell
- DIVERGENT-CHANGE - Divergent Change code smell
- PARALLEL-HIER - Parallel Inheritance Hierarchies

**Key Articles:**
- "Refactoring" - https://martinfowler.com/books/refactoring.html
- "Code Smell" - https://martinfowler.com/bliki/CodeSmell.html

**Key Quotes:**
> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
> "When you feel the need to write a comment, first try to refactor the code so that any comment becomes superfluous."

---

### 4. SOLID Principles

- **Sources:** Robert C. Martin (Uncle Bob), various educational resources
- **Used for:** Object-oriented design principles
- **License:** Educational principles, widely documented

**The Five Principles:**

1. **Single Responsibility Principle (SRP)**
   - A class should have only one reason to change
   - Guideline: SRP-VIOLATION

2. **Open/Closed Principle (OCP)**
   - Open for extension, closed for modification
   - Guideline: OCP-VIOLATION

3. **Liskov Substitution Principle (LSP)**
   - Subtypes must be substitutable for base types
   - Guideline: LSP-VIOLATION

4. **Interface Segregation Principle (ISP)**
   - Clients shouldn't depend on interfaces they don't use
   - (Less applicable to JavaScript, but covered in design)

5. **Dependency Inversion Principle (DIP)**
   - Depend on abstractions, not concretions
   - Guideline: DIP-VIOLATION

**Relevant Guidelines:**
- SRP-VIOLATION - Single Responsibility Principle
- OCP-VIOLATION - Open/Closed Principle
- LSP-VIOLATION - Liskov Substitution Principle
- DIP-VIOLATION - Dependency Inversion Principle
- INJECT-DEP - Dependency Injection (supports DIP)

**Key Resources:**
- Uncle Bob's SOLID principles articles
- Refactoring Guru SOLID guide
- clean-code-javascript SOLID section

---

### 5. Modern JavaScript Best Practices

- **Sources:** MDN, JavaScript.info, ES6+ specifications
- **Used for:** Modern JavaScript patterns and features
- **License:** Public documentation

**Key Features Covered:**

**ES6 (2015):**
- const/let (block scoping)
- Arrow functions
- Template literals
- Destructuring
- Default parameters
- Spread/rest operators
- Classes

**ES2017:**
- async/await

**ES2020:**
- Optional chaining (?.)
- Nullish coalescing (??)

**Relevant Guidelines:**
- CONST-LET - Use const and let
- ARROW-FUNC - Use arrow functions
- TEMPLATE-LIT - Use template literals
- DESTRUCTURE - Use destructuring
- DEFAULT-PARAM - Use default parameters
- SPREAD-REST - Use spread and rest operators
- ASYNC-AWAIT - Use async/await
- OPT-CHAIN - Use optional chaining
- NULLISH-COAL - Use nullish coalescing

**Key Resources:**
- MDN Web Docs - https://developer.mozilla.org/en-US/docs/Web/JavaScript
- JavaScript.info - https://javascript.info/
- ECMAScript specifications

---

### 6. Functional Programming Principles

- **Sources:** Various FP resources, JavaScript FP guides
- **Used for:** Pure functions, immutability, array methods
- **License:** Educational principles

**Key Concepts:**
- **Pure Functions** - No side effects, same input → same output
- **Immutability** - Avoiding mutable state
- **Array Methods** - map, filter, reduce over loops
- **Function Composition** - Building complex logic from simple functions

**Relevant Guidelines:**
- PURE-FUNC - Prefer pure functions
- ARRAY-METHODS - Use array methods (map, filter, reduce)
- SEPARATE-QUERY - Separate query from command (Command-Query Separation)

**Key Resources:**
- "Functional-Light JavaScript" by Kyle Simpson
- "JavaScript Allongé" by Reg Braithwaite
- Functional programming guides on JavaScript.info

---

### 7. Design Patterns

- **Sources:** Gang of Four, JavaScript design pattern resources
- **Used for:** Factory pattern, Strategy pattern, etc.
- **License:** Educational principles

**Patterns Applied:**

**Creational:**
- **Factory Pattern** - FACTORY-PATTERN guideline
- Dependency Injection - INJECT-DEP guideline

**Behavioral:**
- **Strategy Pattern** - Replacing switch statements (SWITCH-STMT)
- **Command-Query Separation** - SEPARATE-QUERY guideline

**Relevant Guidelines:**
- FACTORY-PATTERN - Use factory for object creation
- OCP-VIOLATION - Strategy pattern for extensibility
- SWITCH-STMT - Replace switch with polymorphism

**Key Resources:**
- Refactoring Guru Design Patterns
- "Learning JavaScript Design Patterns" by Addy Osmani

---

### 8. Performance Optimization

- **Sources:** Web performance guides, algorithm optimization resources
- **Used for:** Performance-related refactorings

**Key Topics:**
- Algorithm complexity (Big O)
- Memoization
- Lazy evaluation
- Debouncing and throttling
- Closure optimization

**Relevant Guidelines:**
- ALGO-COMPLEX - Optimize algorithm complexity
- MEMO-RESULT - Memoize expensive computations
- LAZY-EVAL - Use lazy evaluation
- AVOID-CLOSURE-LOOP - Fix closure issues in loops
- DEBOUNCE-THROTTLE - Debounce/throttle frequent events

**Key Resources:**
- "High Performance JavaScript" by Nicholas Zakas
- Web.dev performance guides
- MDN performance documentation

---

### 9. Testing and Testability

- **Sources:** Test-Driven Development resources, testing best practices
- **Used for:** Testability refactorings

**Key Principles:**
- Dependency injection for testability
- Pure functions are easy to test
- Avoid global state
- Expose dependencies explicitly
- Loose coupling

**Relevant Guidelines:**
- INJECT-DEP - Use dependency injection
- PURE-FUNC - Prefer pure functions
- GLOBAL-STATE - Avoid global state
- HIDDEN-DEP - Expose hidden dependencies
- TIGHTLY-COUPLED - Reduce tight coupling
- SEPARATE-QUERY - Separate query from command

**Key Resources:**
- "Test-Driven Development" by Kent Beck
- Testing best practices from Testing Library principles

---

### 10. Kent Beck - Extreme Programming

- **Author:** Kent Beck
- **Used for:** Refactoring philosophy, incremental improvement
- **License:** Published works, educational use

**Key Principles:**
- Make it work, make it right, make it fast
- Incremental refactoring
- Simple design
- Boy Scout Rule (leave code better than you found it)

**Relevant to:** Overall refactoring philosophy and approach

**Key Quote:**
> "Make it work, make it right, make it fast."

---

## Research Process

### Web Searches Performed
1. **"JavaScript refactoring best practices 2024"** - Modern refactoring patterns
2. **"SOLID principles JavaScript examples"** - SOLID in JavaScript context
3. **"clean-code-javascript patterns"** - Clean code for JavaScript
4. **"Martin Fowler refactoring catalog"** - Refactoring techniques
5. **"JavaScript code smells"** - Common anti-patterns
6. **"ES6+ modern JavaScript patterns"** - Modern JavaScript features
7. **"Dependency injection JavaScript"** - DI patterns in JavaScript
8. **"JavaScript performance optimization patterns"** - Performance refactorings
9. **"Pure functions JavaScript"** - Functional programming in JS
10. **"Callback hell solutions async await"** - Modern async patterns

### Methodology
1. **Identify authoritative sources** - Refactoring Guru, Martin Fowler, clean-code-javascript
2. **Adapt for JavaScript** - Convert language-agnostic principles to JavaScript/TypeScript
3. **Include modern patterns** - ES6+, async/await, functional programming
4. **Provide concrete examples** - Before/after code for each guideline
5. **Explain trade-offs** - When to apply each refactoring
6. **Focus on practical value** - Real-world refactoring scenarios

---

## Guideline Structure

Each guideline follows this format:

### Intent
Primary goal: Readability, Maintainability, Testability, or Performance

### Code Smell
The anti-pattern or problem being addressed

### Before/After Examples
- **Bad code** - Shows the problem
- **Good code** - Shows the refactored solution

### Why This Matters
- Benefits of the refactoring
- Impact on code quality
- Connection to principles (SOLID, DRY, etc.)

### Attribution
Source of the refactoring technique

---

## Mnemonic ID Convention

All guidelines use descriptive prefixes:
- **Readability** - MEANINGFUL-NAME, EXTRACT-FUNC, TEMPLATE-LIT
- **Maintainability** - DRY-VIOLATION, SRP-VIOLATION, GOD-CLASS
- **Testability** - PURE-FUNC, INJECT-DEP, GLOBAL-STATE
- **Code Smells** - LONG-METHOD, LARGE-CLASS, CALLBACK-HELL
- **Modern JS** - DESTRUCTURE, ASYNC-AWAIT, OPT-CHAIN
- **Performance** - ALGO-COMPLEX, MEMO-RESULT, DEBOUNCE-THROTTLE

Format: Descriptive short form
Examples: `EXTRACT-FUNC`, `DRY-VIOLATION`, `ASYNC-AWAIT`

---

## Code Example Attribution

All code examples were:
1. **Inspired by** authoritative sources listed above
2. **Adapted for JavaScript/TypeScript** - Modern syntax, realistic scenarios
3. **Created as original examples** - Demonstrating specific refactoring patterns
4. **Structured for education** - Clear before/after comparisons

### Example Pattern:
- **Bad Code:** Common anti-pattern or code smell
- **Good Code:** Refactored solution following best practices
- **Explanation:** Why the refactoring improves code quality

---

## Refactoring Principles Summary

This skill emphasizes:

1. **Readability** - Code is read more than written
2. **SOLID Principles** - Better OOP design
3. **DRY** - Don't Repeat Yourself
4. **Pure Functions** - Predictable, testable code
5. **Dependency Injection** - Loose coupling, testability
6. **Modern JavaScript** - ES6+, async/await, functional patterns
7. **Incremental Refactoring** - Small, safe steps
8. **Code Smells** - Recognize and fix anti-patterns

All based on established refactoring catalogs, design principles, and modern JavaScript best practices.

---

## Key Differentiators from Other Refactoring Guides

### 1. JavaScript-Specific
Adapted for JavaScript/TypeScript with modern syntax:
- ES6+ features (destructuring, spread, arrow functions)
- async/await instead of callbacks
- const/let instead of var
- Template literals
- Optional chaining, nullish coalescing

### 2. Comprehensive Coverage
50+ guidelines covering:
- Readability (12)
- Maintainability (15)
- Testability (7)
- Code Smells (9)
- Modern JavaScript (8)
- Performance (5)

### 3. Concrete Examples
Every guideline has:
- Before code (the problem)
- After code (the solution)
- Explanation (why it matters)
- Code smell addressed

### 4. SOLID Principles
Full SOLID coverage with JavaScript examples:
- SRP, OCP, LSP, ISP, DIP
- Practical applications in JavaScript

### 5. Testability Focus
Strong emphasis on testable code:
- Dependency injection
- Pure functions
- Avoiding global state
- Loose coupling

---

## Verification

All guidelines were verified against:
1. ✅ Refactoring Guru refactoring catalog
2. ✅ clean-code-javascript repository
3. ✅ Martin Fowler's refactoring principles
4. ✅ SOLID principles documentation
5. ✅ Modern JavaScript (ES6+) best practices
6. ✅ Functional programming principles
7. ✅ Design pattern resources
8. ✅ Performance optimization guides

---

## Updates and Maintenance

- **Version:** 1.0
- **Created:** January 2025
- **Last Updated:** January 2025
- **JavaScript Compatibility:** ES6+ (ES2015 and later)
- **TypeScript Compatibility:** All examples work in TypeScript

**Future Updates May Include:**
- More TypeScript-specific refactorings
- React/Vue component refactoring patterns
- Node.js backend-specific patterns
- More performance optimization patterns
- Additional design patterns

---

## Acknowledgments

Special thanks to:
- **Martin Fowler** - For comprehensive refactoring catalog and principles
- **Robert C. Martin (Uncle Bob)** - For Clean Code and SOLID principles
- **Kent Beck** - For Test-Driven Development and XP practices
- **Ryan McDermott** - For clean-code-javascript adaptation
- **Refactoring Guru** - For comprehensive code smell and pattern documentation
- **Gang of Four** - For foundational design patterns
- **JavaScript Community** - For modern JavaScript best practices
- **MDN Contributors** - For excellent JavaScript documentation

---

## Anti-Patterns Explicitly Avoided

This skill teaches developers to AVOID:

### 1. var Keyword
- **Why avoided:** Function scoping, hoisting issues
- **What to use instead:** const (preferred) or let
- **Guideline:** CONST-LET

### 2. Callback Hell
- **Why avoided:** Hard to read, error-prone
- **What to use instead:** async/await
- **Guideline:** CALLBACK-HELL, ASYNC-AWAIT

### 3. String Concatenation
- **Why avoided:** Less readable, no multi-line support
- **What to use instead:** Template literals
- **Guideline:** TEMPLATE-LIT

### 4. Magic Numbers
- **Why avoided:** Unclear meaning, hard to maintain
- **What to use instead:** Named constants
- **Guideline:** MAGIC-NUM

### 5. God Classes
- **Why avoided:** Too many responsibilities, hard to maintain
- **What to use instead:** Extract classes, apply SRP
- **Guideline:** GOD-CLASS, SRP-VIOLATION

### 6. Hard-Coded Dependencies
- **Why avoided:** Tight coupling, hard to test
- **What to use instead:** Dependency injection
- **Guideline:** INJECT-DEP, TIGHTLY-COUPLED

### 7. Global State
- **Why avoided:** Hidden dependencies, testing interference
- **What to use instead:** Encapsulated state, dependency injection
- **Guideline:** GLOBAL-STATE

### 8. Long Functions
- **Why avoided:** Hard to understand, test, and maintain
- **What to use instead:** Extract smaller functions
- **Guideline:** LONG-FUNC, EXTRACT-FUNC

### 9. Duplicate Code
- **Why avoided:** Maintenance burden, bug propagation
- **What to use instead:** Extract common logic
- **Guideline:** DRY-VIOLATION, DUPLICATE-CODE

### 10. Complex Conditionals
- **Why avoided:** Hard to understand and maintain
- **What to use instead:** Guard clauses, explaining variables, polymorphism
- **Guideline:** NESTED-COND, DECOMPOSE-COND, SWITCH-STMT

---

## Real-World Examples Referenced

While creating examples, consulted:
- Open-source JavaScript projects on GitHub
- React, Vue, Angular codebases
- Node.js/Express applications
- Refactoring Guru examples
- clean-code-javascript examples

All examples were then:
1. Simplified for clarity
2. Made self-contained
3. Annotated with explanations
4. Structured to show clear before/after

---

## Legal and Attribution

### Books and Publications
- **"Refactoring"** by Martin Fowler - Educational reference
- **"Clean Code"** by Robert C. Martin - Educational reference
- Principles and patterns documented for educational use

### Open Source Resources
- **clean-code-javascript** - MIT licensed, GitHub repository
- **Refactoring Guru** - Educational content, freely available

### Design Principles
- **SOLID, DRY, KISS** - Industry-standard principles, widely documented
- **Educational use:** Freely applicable for teaching and learning

### Code Examples
- **Original examples:** Created for this skill
- **Inspired by:** Authoritative sources listed above
- **License:** Provided as-is for educational use with Claude Code

---

## Refactoring Philosophy Summary

This skill follows Martin Fowler's refactoring philosophy:

1. **Refactoring is NOT rewriting** - Incremental improvements
2. **Two hats approach** - Add features OR refactor, not both
3. **Small steps** - Each refactoring is a small, safe change
4. **Tests are essential** - Ensure refactoring doesn't break behavior
5. **Code smells guide refactoring** - Indicators of where to improve
6. **Refactoring improves design** - Not just cosmetic changes

Combined with modern JavaScript best practices:
- Use modern syntax (ES6+)
- Favor functional patterns (pure functions, immutability)
- Write testable code (dependency injection, loose coupling)
- Follow SOLID principles
- Keep it simple (KISS principle)

---

**Note:** This skill prioritizes practical refactoring techniques that improve real-world JavaScript/TypeScript code. The goal is to help developers write maintainable, testable, and performant code through systematic refactoring.

---

**Created:** January 2025
**Last Updated:** January 2025
**Skill Version:** 1.0
**Focus:** Practical JavaScript/TypeScript refactoring based on established principles and modern best practices
