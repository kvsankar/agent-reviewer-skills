# Sources and Attribution

All guidelines in the JavaScript/TypeScript Format Refactoring Reviewer skill are based on publicly available documentation, style guides, and established refactoring patterns.

## Primary Sources

### 1. Airbnb JavaScript Style Guide
- **Source:** https://github.com/airbnb/javascript
- **License:** MIT License
- **What we used:** Best practices for JavaScript code style, naming conventions, parameter handling, arrow functions, destructuring, template literals, and React/JSX patterns
- **Guidelines influenced:**
  - JS-LONG-FUNC-PARAMS (destructuring and parameter objects)
  - JS-LONG-CHAIN (method chaining formatting)
  - JS-PARAMS-MANY (options objects)
  - JS-PARAMS-DEFAULT (default parameters)
  - JS-STRING-CONCAT (template literals)
  - JS-JSX-* (all React/JSX guidelines)
  - JS-OBJ-LONG, JS-ARRAY-LONG (object/array formatting)

### 2. ESLint Rules Documentation
- **Source:** https://eslint.org/docs/latest/rules/
- **License:** MIT License
- **What we used:** Official ESLint rule definitions, rationale, and examples
- **Rules covered:**
  - max-len (line length)
  - complexity (cyclomatic complexity)
  - max-params (parameter count)
  - max-statements (statement count)
  - max-depth (nesting depth)
  - max-nested-callbacks (callback nesting)
  - no-nested-ternary (nested ternaries)
  - prefer-template (template literals)
  - default-param-last (default parameters)
  - object-curly-newline (object formatting)
  - array-element-newline (array formatting)

### 3. ESLint React Plugin
- **Source:** https://github.com/jsx-eslint/eslint-plugin-react
- **License:** MIT License
- **What we used:** React-specific ESLint rules and best practices
- **Rules covered:**
  - react/jsx-max-depth (JSX nesting depth)
  - react/jsx-max-props-per-line (props per line)
  - react/jsx-no-bind (inline function performance)
- **Guidelines influenced:**
  - JS-JSX-LONG (extract components)
  - JS-JSX-PROPS (props formatting)
  - JS-JSX-INLINE (inline functions)

### 4. Refactoring: Improving the Design of Existing Code
- **Author:** Martin Fowler
- **What we used:** Classic refactoring patterns and catalog
- **Patterns applied:**
  - Extract Function
  - Extract Variable
  - Introduce Parameter Object
  - Replace Nested Conditional with Guard Clauses
  - Decompose Conditional
  - Replace Conditional with Polymorphism (adapted to lookup objects)
  - Preserve Whole Object
- **Guidelines influenced:**
  - JS-LONG-FUNC-PARAMS (Introduce Parameter Object)
  - JS-COMPLEX-FUNC (Extract Function)
  - JS-LONG-CONDITION (Decompose Conditional)
  - JS-COMPLEX-CONDITION (Extract Predicate)
  - JS-COMPLEX-NESTING (Guard Clauses)

### 5. Clean Code: A Handbook of Agile Software Craftsmanship
- **Author:** Robert C. Martin (Uncle Bob)
- **What we used:** Principles for clean, maintainable code
- **Principles applied:**
  - Single Responsibility Principle
  - Meaningful Names
  - Small Functions
  - Minimize Nesting
  - Avoid Flag Arguments (boolean parameters)
- **Guidelines influenced:**
  - JS-COMPLEX-FUNC (single responsibility)
  - JS-PARAMS-BOOLEAN (avoid boolean flags)
  - JS-COMPLEX-NESTING (minimize nesting)
  - All complexity reduction guidelines

### 6. React Documentation
- **Source:** https://react.dev/
- **License:** CC BY 4.0
- **What we used:** Official React best practices and patterns
- **Patterns covered:**
  - Component composition
  - Props patterns
  - Conditional rendering
  - Lists and keys
  - Performance optimization (useCallback, useMemo)
- **Guidelines influenced:**
  - JS-JSX-LONG (component extraction)
  - JS-JSX-CONDITION (conditional rendering)
  - JS-JSX-MAP (list rendering)
  - JS-JSX-INLINE (performance patterns)

### 7. Prettier
- **Source:** https://prettier.io/
- **License:** MIT License
- **What we used:** Formatting conventions for objects, arrays, and multi-line constructs
- **Guidelines influenced:**
  - JS-OBJ-LONG (object formatting)
  - JS-ARRAY-LONG (array formatting)
  - JS-SPREAD-LONG (spread formatting)
  - Trailing comma conventions

### 8. MDN Web Docs (JavaScript)
- **Source:** https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **License:** CC BY-SA 2.5
- **What we used:** JavaScript language features and best practices
- **Features covered:**
  - Template literals
  - Destructuring
  - Default parameters
  - Spread syntax
  - Arrow functions
  - Async/await
  - Map and object patterns
- **Guidelines influenced:**
  - JS-STRING-CONCAT (template literals)
  - JS-TEMPLATE-* (template patterns)
  - JS-PARAMS-DEFAULT (default parameters)
  - JS-COMPLEX-CALLBACK (async/await)
  - JS-COMPLEX-SWITCH (Maps and objects)

### 9. JavaScript Design Patterns
- **Various sources:** Addy Osmani's "Learning JavaScript Design Patterns", community patterns
- **What we used:** Common JavaScript patterns and anti-patterns
- **Patterns applied:**
  - Module pattern
  - Builder pattern (for options objects)
  - Factory pattern (for object creation)
  - Strategy pattern (for lookup objects)
- **Guidelines influenced:**
  - JS-PARAMS-MANY (options object pattern)
  - JS-COMPLEX-SWITCH (strategy/lookup pattern)

### 10. TypeScript Handbook
- **Source:** https://www.typescriptlang.org/docs/
- **License:** Apache 2.0
- **What we used:** TypeScript best practices (applicable to JavaScript)
- **Guidelines influenced:**
  - Parameter object typing
  - Interface usage patterns
  - Type-safe refactoring patterns

## Additional References

### YouTube Conference Talks
- **"The Refactoring Tales"** - Various JavaScript conference talks on refactoring
- **React Conf Talks** - Component design and performance patterns
- **JSConf Talks** - Modern JavaScript patterns and practices

### Blog Posts and Articles
- **Kent C. Dodds Blog** - React patterns and testing
- **Dan Abramov's Blog** - React internals and patterns
- **JavaScript Weekly** - Community best practices
- **CSS-Tricks** - Frontend patterns and practices

## Guideline Mapping to Sources

### Line Length Issues
- **JS-LONG-FUNC-PARAMS** → Fowler (Introduce Parameter Object), Airbnb (destructuring)
- **JS-LONG-CHAIN** → Airbnb (method chaining), Prettier (formatting)
- **JS-LONG-CONDITION** → Fowler (Decompose Conditional), Clean Code
- **JS-LONG-TEMPLATE** → MDN (template literals), Prettier
- **JS-LONG-ARRAY** → Airbnb, Prettier (multi-line arrays)
- **JS-LONG-JSX** → React docs (component composition), Airbnb

### Complexity Issues
- **JS-COMPLEX-CONDITION** → Fowler (Decompose Conditional), Clean Code
- **JS-COMPLEX-FUNC** → Fowler (Extract Function), Clean Code (SRP)
- **JS-COMPLEX-TERNARY** → Airbnb (no-nested-ternary), ESLint
- **JS-COMPLEX-SWITCH** → JavaScript patterns (lookup objects), MDN (Maps)
- **JS-COMPLEX-CALLBACK** → MDN (async/await), modern JavaScript patterns
- **JS-COMPLEX-NESTING** → Fowler (Guard Clauses), Clean Code

### Function Parameters
- **JS-PARAMS-MANY** → Fowler (Parameter Object), Airbnb (destructuring)
- **JS-PARAMS-ORDER** → Clean Code (function arguments), Airbnb
- **JS-PARAMS-BOOLEAN** → Clean Code (flag arguments), Fowler
- **JS-PARAMS-DEFAULT** → MDN (default parameters), Airbnb, ESLint

### React/JSX
- **JS-JSX-LONG** → React docs (component composition)
- **JS-JSX-PROPS** → React docs, Airbnb (props patterns)
- **JS-JSX-CONDITION** → React docs (conditional rendering)
- **JS-JSX-MAP** → React docs (lists and keys)
- **JS-JSX-INLINE** → React docs (performance), ESLint React plugin
- **JS-JSX-STYLE** → React docs, CSS-in-JS patterns

### Array/Object
- **JS-OBJ-LONG** → Prettier, Airbnb (object formatting)
- **JS-ARRAY-LONG** → Prettier, Airbnb (array formatting)
- **JS-OBJ-COMPUTED** → MDN (computed properties), JavaScript patterns
- **JS-SPREAD-LONG** → Prettier, MDN (spread syntax)

### String/Template
- **JS-STRING-CONCAT** → Airbnb (prefer-template), ESLint
- **JS-TEMPLATE-LONG** → MDN (template literals), Prettier
- **JS-TEMPLATE-COMPLEX** → JavaScript patterns, Clean Code
- **JS-STRING-SPLIT** → Prettier, formatting conventions

## Verification

All guidelines:
1. **Are based on documented best practices** from authoritative sources
2. **Reference specific ESLint rules** where applicable
3. **Show concrete examples** from real-world scenarios
4. **Provide attribution** to the source of the pattern
5. **Focus on refactoring** rather than just formatting

## Usage and Attribution

This skill is educational and references publicly available:
- Open-source style guides (MIT licensed)
- Official documentation (various open licenses)
- Published refactoring patterns (industry standard)
- Community best practices (publicly shared)

When using this skill, you're applying:
- **Industry-standard patterns** from Airbnb, ESLint, React
- **Classic refactoring techniques** from Fowler's catalog
- **Clean code principles** from Uncle Bob
- **Modern JavaScript features** from ES6+ specifications

## License

The skill implementation itself is licensed under MIT.

All referenced materials (Airbnb Style Guide, ESLint rules, React docs, MDN, Prettier) are used according to their respective licenses for educational purposes.

## Updates

This skill reflects best practices as of 2024-2025. JavaScript and its ecosystem evolve rapidly, so some patterns may become obsolete or new patterns may emerge. The core refactoring principles, however, remain timeless.

---

**Note:** If you find any attribution errors or have questions about sources, please refer to the original documentation linked above.
