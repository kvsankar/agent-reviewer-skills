# Sources and References

This document provides detailed attribution and sources for all guidelines in the Python Refactoring Code Reviewer skill.

## Methodology

This skill was created on **November 1, 2025** using:
1. **Web searches** for refactoring catalogs and best practices
2. **Public refactoring resources** (Refactoring Guru, clean-code-python)
3. **Established design principles** (SOLID, DRY, KISS)
4. **Claude's training knowledge** (pre-January 2025)
5. **Python community best practices**

All guidelines represent industry-standard refactoring techniques documented in publicly available resources.

---

## Legal Disclaimer and Copyright Notice

### What This Skill Uses

This skill uses **established refactoring terminology and code smell names** that originated in Martin Fowler's seminal book "Refactoring: Improving the Design of Existing Code" (1999, 2nd edition 2018) and have become **standard industry terminology** in software engineering.

**Specifically:**
- **Code Smell Names:** "Long Method," "God Class," "Feature Envy," "Data Clumps," etc.
- **Refactoring Technique Names:** "Extract Method," "Extract Class," "Replace Conditional with Polymorphism," etc.
- **Design Principles:** SOLID, DRY (Don't Repeat Yourself), KISS (Keep It Simple)

**Legal Basis:**
- These terms represent **fundamental software engineering concepts** and are now part of common professional vocabulary
- **Concept names and terminology are generally NOT copyrightable** under U.S. copyright law (only specific creative expression is copyrightable)
- These concepts are documented in multiple independent sources (academic papers, textbooks, online resources, professional literature)
- We cite sources for attribution and educational purposes, not because the terminology itself is proprietary

### What This Skill Does NOT Use

**We explicitly DID NOT:**
- Copy any descriptive text from copyrighted sources
- Use any code examples from copyrighted sources
- Use any illustrations or diagrams from any source
- Copy any substantial portions of copyrighted works
- Reproduce any proprietary teaching materials

**All content in this skill is original:**
- All code examples were written specifically for this skill
- All descriptions and explanations are original prose
- All "why this matters" sections are original analysis
- The organization and presentation is original

### Attribution and Fair Use

**Why we provide attribution:**
1. **Academic integrity** - Proper credit to those who established these concepts
2. **Educational value** - Directing learners to authoritative sources
3. **Professional courtesy** - Acknowledging the community's contributions
4. **Compliance** - Following usage policies where applicable

**Not because the terminology is proprietary** - We attribute to show respect and provide educational context, even though the fundamental concepts are part of established software engineering knowledge.

### Specific Source Compliance

**Refactoring Guru:**
Their Content Usage Policy states:
> "You can cite any text as long as it's not a substantial part of the cited article"
> "Place a hyperlink to the specific page"

**Our compliance:**
- ✅ Used terminology (which they also sourced from Martin Fowler)
- ✅ Wrote completely original descriptions and code examples
- ✅ Included hyperlinks and attribution
- ✅ Used NO substantial text from their articles
- ✅ Used ZERO illustrations (policy allows up to 10, we used 0)

**clean-code-python:**
- MIT License (very permissive)
- ✅ Full compliance: adapted concepts, wrote original examples, provided attribution

**Martin Fowler's Works:**
- Copyrighted books and articles
- ✅ Referenced concepts and established terminology
- ✅ Included two short quotes with proper attribution
- ✅ Did not copy substantial text or code
- ✅ All code examples are original

### Educational Use

This skill is created for **educational purposes** to help developers learn refactoring techniques. It is:
- **Non-commercial** - Free educational resource
- **Transformative** - Synthesizes multiple sources into a new teaching tool
- **Complementary** - Directs users to original sources for deeper learning
- **Original content** - All examples and explanations are newly created

### Summary

**What is copyrighted:**
- Martin Fowler's books, articles, and specific writings
- Refactoring Guru's specific article text, descriptions, and illustrations
- Individual educational materials from various authors

**What is NOT copyrighted (and what we use):**
- Software engineering terminology and concept names
- Design principle names (SOLID, DRY, etc.)
- Refactoring technique names established in the field
- Code smell taxonomy that is now industry standard

**What we created (original work):**
- All code examples in this skill
- All descriptions and explanations
- All "before/after" refactoring demonstrations
- The organization and pedagogical structure
- The mnemonic ID system
- The intent-based categorization

**If you have concerns:**
This skill can be updated or removed if any copyright holder believes their rights are being infringed. Contact information is provided in the main README.

---

## Primary Sources

### 1. Refactoring Guru

**Website:** https://refactoring.guru/

**Content Used:**
- Code Smells Catalog (24 code smells)
- Refactoring Techniques Catalog (66 techniques)

**License/Usage Rights:**
According to Refactoring Guru's Content Usage Policy:
- Free to cite text with hyperlinks to specific pages
- Can use up to 10 illustrations total
- Source code samples use CC BY-NC-ND 4.0

**What We Used:**
- Concept descriptions and classifications
- Code smell categories (Bloaters, Object-Orientation Abusers, Change Preventers, Dispensables, Couplers)
- Refactoring technique names and descriptions
- All code examples were written specifically for this skill (not copied)

**Usage Compliance:**
- All citations include reference to Refactoring Guru
- No illustrations used (text-only references)
- Concepts adapted for Python-specific implementations

**Attribution in Skill:**
Guidelines derived from Refactoring Guru include attribution note in each guideline.

---

### 2. clean-code-python

**GitHub Repository:** https://github.com/zedr/clean-code-python

**License:** MIT License

**Author:** Maurits van der Schee (zedr)

**Content Covered:**
- Variables (meaningful names, pronounceable names, searchable names)
- Functions (single purpose, parameter limits, default arguments)
- SOLID Principles (SRP, OCP, LSP, ISP, DIP)
- DRY Principle

**MIT License Terms:**
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

**What We Used:**
- Clean Code concepts adapted for Python
- SOLID principles explanations
- Variable and function naming guidelines
- Code organization principles

**How We Used It:**
- Adapted concepts into refactoring guidelines
- Wrote original code examples
- Applied principles to Python 3.7+ idioms

**Attribution in Skill:**
Guidelines derived from clean-code-python include "clean-code-python (MIT)" attribution.

---

### 3. Martin Fowler's Refactoring

**Book:** "Refactoring: Improving the Design of Existing Code" (2nd Edition)
**Author:** Martin Fowler
**Website:** https://refactoring.com/ and https://martinfowler.com/

**Copyright Status:** Copyrighted work

**What We Used:**
- General refactoring concepts and philosophy
- Terminology (code smells, refactoring techniques)
- Best practices for systematic refactoring

**How We Used It:**
- Referenced concepts, not copied text
- Used established terminology
- Applied principles to Python-specific examples
- All code examples are original

**Notable Quotes Used:**
> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
> — Martin Fowler

> "Refactoring is the process of changing a software system in such a way that it does not alter the external behavior of the code yet improves its internal structure."
> — Martin Fowler

**Attribution in Skill:**
- Concept references include "Refactoring catalog" or "Martin Fowler" attribution
- Quotes properly attributed

---

### 4. SOLID Principles

**Origin:** Robert C. Martin (Uncle Bob)

**Public Domain Status:** Principles are widely documented and considered part of software engineering knowledge

**Resources:**
- Original papers and articles by Robert C. Martin
- Numerous educational resources (books, articles, talks)
- Community adaptations for various languages

**The Five Principles:**
1. **Single Responsibility Principle (SRP)** - A class should have one reason to change
2. **Open/Closed Principle (OCP)** - Open for extension, closed for modification
3. **Liskov Substitution Principle (LSP)** - Subtypes must be substitutable for base types
4. **Interface Segregation Principle (ISP)** - Clients shouldn't depend on interfaces they don't use
5. **Dependency Inversion Principle (DIP)** - Depend on abstractions, not concretions

**What We Used:**
- Principle definitions and explanations
- Application to Python code
- Common violations and solutions

**How We Used It:**
- Adapted principles to Python idioms
- Created Python-specific examples
- Integrated with refactoring guidelines

**Attribution in Skill:**
- SOLID principles explicitly referenced
- Individual principles cited (SRP, OCP, LSP, ISP, DIP)

---

### 5. Python Best Practices and PEPs

**Source:** Python Enhancement Proposals (PEPs)
**License:** Public Domain

**Key PEPs Referenced:**
- **PEP 8** - Style Guide for Python Code (Public Domain)
- **PEP 20** - The Zen of Python (Public Domain)
- **PEP 257** - Docstring Conventions

**Python Documentation:**
- Official Python documentation (PSF License - open and permissive)
- Built-in functions and standard library patterns

**What We Used:**
- Pythonic idioms (comprehensions, generators, context managers)
- Standard library patterns (enumerate, zip, decorators)
- Type hints and modern Python features

**How We Used It:**
- Demonstrated Pythonic refactorings
- Showed anti-patterns vs. idiomatic Python
- Referenced modern Python (3.7+) features

**Attribution in Skill:**
- "Python best practices" attribution
- "Pythonic" patterns noted

---

## Web Search Results (November 1, 2025)

### Search 1: "Martin Fowler refactoring catalog open source license"

**Key Findings:**
- Refactoring catalog at refactoring.com is copyrighted
- Concept names and techniques are established in software engineering
- Emily Bache's Theatrical Players kata (GitHub) with multiple language implementations

**How Used:**
- Referenced established terminology
- Did not copy proprietary content
- Used concepts as foundation for original examples

---

### Search 2: "Refactoring Guru code smells patterns license free"

**Key Findings:**
- **Content Usage Policy:** Free citation with hyperlinks, up to 10 illustrations
- **Code Smells:** 21+ smells across 5 categories
- **Refactoring Techniques:** 66 techniques
- **Source Code License:** CC BY-NC-ND 4.0

**How Used:**
- Referenced code smell categories and names
- Adapted concepts for Python
- Wrote original code examples
- Included hyperlinks in attribution

---

### Search 3: "Python refactoring best practices public domain open source 2024"

**Key Findings:**
- **Real Python:** Python refactoring tutorials
- **PEP 8:** Public domain style guide
- **University of Zurich Guide:** CC-BY-SA 4.0
- **Rope/Bowler:** Python refactoring tools

**How Used:**
- Referenced modern Python patterns
- Incorporated public domain PEP guidance
- Applied community best practices

---

### Search 4: "clean code Python patterns anti-patterns catalog open source"

**Key Findings:**
- **zedr/clean-code-python:** MIT Licensed GitHub repository
- **Antipattern catalogs:** Various open source resources
- **Python-specific clean code guides**

**How Used:**
- Primary source for clean code principles
- SOLID principles in Python context
- DRY and other fundamental principles

---

### Search 5: "SOLID principles Python examples public domain creative commons"

**Key Findings:**
- Multiple educational resources with Python examples
- GitHub repositories with examples (various licenses)
- Educational blog posts and tutorials

**How Used:**
- Verified SOLID concepts
- Created original Python examples
- Cross-referenced multiple sources

---

## Guideline-to-Source Mapping

### Readability Guidelines (18)

| Mnemonic ID | Primary Source | Secondary Source |
|-------------|----------------|------------------|
| MEANINGFUL-NAME | clean-code-python | Martin Fowler |
| PRONOUNCE-NAME | clean-code-python | - |
| SEARCHABLE-NAME | clean-code-python | - |
| AVOID-MENTAL-MAP | clean-code-python | - |
| EXTRACT-METHOD | Refactoring Guru | Martin Fowler - Extract Method |
| EXTRACT-VAR | Refactoring Guru | Martin Fowler - Extract Variable |
| DECOMPOSE-COND | Refactoring Guru | Martin Fowler - Decompose Conditional |
| LONG-FUNC | Refactoring Guru | Code smell: Long Method |
| LONG-PARAM | Refactoring Guru | Code smell: Long Parameter List |
| MAGIC-NUM | Refactoring Guru | Replace Magic Number with Symbolic Constant |
| COMMENT-WHY | clean-code-python | Clean code principles |
| COMMENT-SMELL | Refactoring Guru | Code smell: Comments |
| NESTED-DEEP | Refactoring Guru | Replace Nested Conditional with Guard Clauses |
| GUARD-CLAUSE | Refactoring Guru | Replace Nested Conditional with Guard Clauses |
| POSITIVE-COND | Clean code principles | - |
| POLY-COND | Refactoring Guru | Replace Conditional with Polymorphism |
| RENAME-METHOD | Refactoring Guru | Rename Method |
| SINGLE-PURPOSE | clean-code-python | SRP |
| EXPLAIN-VAR | clean-code-python | - |

### Maintainability Guidelines (17)

| Mnemonic ID | Primary Source | Principle |
|-------------|----------------|-----------|
| DRY-VIOLATION | clean-code-python | DRY (Don't Repeat Yourself) |
| EXTRACT-CLASS | Refactoring Guru | Extract Class |
| DUPLICATE-CODE | Refactoring Guru | Code smell: Duplicate Code |
| SRP-VIOLATION | clean-code-python | SOLID - Single Responsibility |
| OCP-VIOLATION | clean-code-python | SOLID - Open/Closed |
| LSP-VIOLATION | clean-code-python | SOLID - Liskov Substitution |
| ISP-VIOLATION | clean-code-python | SOLID - Interface Segregation |
| DIP-VIOLATION | clean-code-python | SOLID - Dependency Inversion |
| GOD-CLASS | Refactoring Guru | Code smell: Large Class |
| DATA-CLASS | Refactoring Guru | Code smell: Data Class |
| LAZY-CLASS | Refactoring Guru | Code smell: Lazy Class |
| FEATURE-ENVY | Refactoring Guru | Code smell: Feature Envy |
| MESSAGE-CHAIN | Refactoring Guru | Code smell: Message Chains |
| MIDDLE-MAN | Refactoring Guru | Code smell: Middle Man |
| SHOT-GUN | Refactoring Guru | Code smell: Shotgun Surgery |
| DIVERGENT-CHANGE | Refactoring Guru | Code smell: Divergent Change |
| PARALLEL-HIER | Refactoring Guru | Code smell: Parallel Inheritance Hierarchies |

### Testability Guidelines (8)

| Mnemonic ID | Primary Source | Principle |
|-------------|----------------|-----------|
| PURE-FUNC | Functional programming | clean-code-python |
| INJECT-DEP | SOLID | Dependency Inversion |
| SEPARATE-QUERY | Martin Fowler | Command-Query Separation |
| HIDDEN-DEP | Dependency Injection | Testing patterns |
| GLOBAL-STATE | Testing best practices | clean-code-python |
| TIGHTLY-COUPLED | SOLID | Dependency Inversion |
| EXTRACT-INTERFACE | Refactoring Guru | Extract Interface |
| FACTORY-METHOD | Refactoring Guru | Replace Constructor with Factory Method |

### Code Smells - Bloaters (5)

| Mnemonic ID | Source | Smell Name |
|-------------|--------|------------|
| LONG-METHOD | Refactoring Guru | Long Method |
| LARGE-CLASS | Refactoring Guru | Large Class |
| LONG-PARAM-LIST | Refactoring Guru | Long Parameter List |
| PRIMITIVE-OBS | Refactoring Guru | Primitive Obsession |
| DATA-CLUMP | Refactoring Guru | Data Clumps |

### Code Smells - Complexity (5)

| Mnemonic ID | Source | Smell Name |
|-------------|--------|------------|
| SWITCH-STMT | Refactoring Guru | Switch Statements |
| NESTED-COND | Refactoring Guru | Nested Conditionals |
| COMPLEX-BOOL | Refactoring Guru | Consolidate Conditional Expression |
| TEMP-FIELD | Refactoring Guru | Temporary Field |
| ALT-CLASSES | Refactoring Guru | Alternative Classes with Different Interfaces |

### Pythonic Patterns (10)

| Mnemonic ID | Source |
|-------------|--------|
| LIST-COMP | Python best practices, clean-code-python |
| DICT-COMP | Python best practices, clean-code-python |
| SET-COMP | Python best practices |
| GENERATOR-EXPR | Python best practices, clean-code-python |
| CONTEXT-MGR | Python best practices |
| DECORATOR-USE | Python best practices |
| ENUMERATE-USE | Python best practices |
| ZIP-USE | Python best practices |
| UNPACK-USE | Python best practices |
| F-STRING | Python best practices (Python 3.6+) |

### Performance (7)

| Mnemonic ID | Source |
|-------------|--------|
| ALGO-COMPLEX | Algorithm optimization principles |
| PREMATURE-OPT | Donald Knuth, programming wisdom |
| CACHE-RESULT | Caching patterns |
| GEN-NOT-LIST | Python generators, clean-code-python |
| SLOT-USE | Python optimization techniques |
| LAZY-EVAL | Lazy evaluation patterns |
| AVOID-COPY | Python optimization |

---

## Code Examples Attribution

### Original Code Examples
All code examples in SKILL.md were **written specifically for this skill** to demonstrate refactoring patterns. No code was copied verbatim from copyrighted sources.

### Example Patterns Derived From:
- **Refactoring Guru:** General refactoring patterns and code smell structures
- **clean-code-python:** Clean Code principles adapted for Python
- **Martin Fowler:** Refactoring concepts and terminology
- **Python Documentation:** Idiomatic Python patterns

### Example Categories:
1. **Variable Naming:** Based on clean-code-python principles
2. **Method Extraction:** Based on Refactoring Guru's Extract Method
3. **SOLID Violations:** Based on clean-code-python SOLID examples
4. **Code Smells:** Based on Refactoring Guru code smell catalog
5. **Pythonic Patterns:** Based on Python documentation and community practices

---

## Claude's Training Knowledge

The following aspects come from Claude's training data (pre-January 2025):

### Refactoring Knowledge
- General refactoring principles and best practices
- Code smell detection patterns
- Refactoring technique applications
- Design pattern knowledge

### Python Expertise
- Python language features and idioms
- Standard library usage patterns
- Modern Python (3.7+) best practices
- Performance optimization techniques

### Software Engineering Principles
- SOLID, DRY, KISS, YAGNI principles
- Object-oriented design
- Functional programming concepts
- Testing best practices

---

## Synthesis and Original Contributions

While all guidelines are based on established refactoring catalogs and principles, the following aspects are original to this skill:

1. **Mnemonic ID System:** The specific mnemonic identifiers (EXTRACT-METHOD, DRY-VIOLATION, etc.) were created for this skill
2. **Intent-Based Organization:** The categorization into Readability, Maintainability, Testability, etc.
3. **Python-Specific Examples:** All code examples written specifically for this skill
4. **Integration:** The synthesis of multiple sources into a cohesive review framework
5. **Review Structure:** The before/after/why format with code smell attribution

---

## References and Further Reading

### Refactoring Resources
- **Refactoring Guru:** https://refactoring.guru/
  - Code Smells: https://refactoring.guru/refactoring/smells
  - Refactoring Catalog: https://refactoring.guru/refactoring/catalog

- **Martin Fowler's Refactoring:** https://refactoring.com/
  - Book: "Refactoring: Improving the Design of Existing Code" (2nd Edition)

- **clean-code-python (MIT):** https://github.com/zedr/clean-code-python

### Design Principles
- **SOLID Principles:** Robert C. Martin
  - Real Python SOLID Tutorial: https://realpython.com/solid-principles-python/

- **DRY Principle:** Andy Hunt and Dave Thomas, "The Pragmatic Programmer"

- **Clean Code:** Robert C. Martin, "Clean Code: A Handbook of Agile Software Craftsmanship"

### Python Resources
- **PEP 8:** https://peps.python.org/pep-0008/ (Public Domain)
- **PEP 20:** https://peps.python.org/pep-0020/ (The Zen of Python)
- **Python Documentation:** https://docs.python.org/

### Refactoring Tools
- **Rope:** Python refactoring library
- **Bowler:** Safe code refactoring for modern Python
- **PyCharm/VSCode:** IDE refactoring support

---

## License and Copyright

### Primary Sources Copyright
- **Refactoring Guru:** Content protected by copyright, used with attribution per Content Usage Policy
- **clean-code-python:** MIT License (permissive open source)
- **Martin Fowler:** Copyrighted works (concepts referenced, not copied)
- **Python Documentation:** PSF License (open and permissive)
- **PEP documents:** Public domain

### This Skill
This skill is licensed under MIT. It synthesizes publicly available refactoring knowledge into a practical code review tool; source materials remain under their respective licenses.

**Created:** November 1, 2025
**Last Updated:** November 1, 2025
**Maintainer:** Claude Skills Collection

---

## Verification and Updates

### How to Verify Sources
All primary sources listed above are publicly accessible:
1. Visit the URLs provided
2. Review official documentation
3. Check license terms
4. Verify refactoring concepts match established catalogs

### Keeping This Skill Updated
To update this skill with new refactoring patterns:
1. Monitor Refactoring Guru for new patterns
2. Review updates to clean-code-python
3. Follow Python PEP updates
4. Track new Python features and idioms
5. Incorporate community feedback

---

## Acknowledgments

Special thanks to:
- **Alexander Shvets** for Refactoring Guru - comprehensive refactoring and code smell catalog
- **Maurits van der Schee (zedr)** for clean-code-python - Clean Code principles for Python
- **Martin Fowler** for establishing refactoring as a discipline and providing foundational concepts
- **Robert C. Martin** for SOLID principles and Clean Code philosophy
- **Python Software Foundation** for excellent documentation and PEPs
- **The Python community** for Pythonic patterns and best practices

This skill exists to help developers write better, more maintainable Python code through systematic refactoring.

---

**Last Updated:** November 1, 2025
