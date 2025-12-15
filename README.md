# Claude Code Skills Collection

A curated collection of high-quality Claude Code skills for code review, requirements analysis, and software quality. Each skill focuses on a specific aspect of software development, providing detailed analysis and actionable recommendations.

## 🎯 Available Skills (19 Total)

### JavaScript/TypeScript Skills

#### 1. **JavaScript Test Reviewer**
Reviews JavaScript/TypeScript tests for quality and suggests multiple testing strategies.

**Focus Areas:**
- Test structure (AAA pattern, organization)
- Multiple testing strategies for different scenarios
- Jest, Vitest, Testing Library, Cypress best practices
- User-centric testing (behavior over implementation)
- Mocking strategies (MSW, jest.mock, etc.)
- Component testing and E2E testing
- Test quality over coverage

**Use when:** Reviewing JavaScript/TypeScript tests, learning testing strategies, or improving test quality

---

#### 2. **JavaScript Refactoring Reviewer**
Reviews JavaScript/TypeScript code for refactoring opportunities to improve quality and maintainability.

**Focus Areas:**
- Code smells (long functions, god classes, duplication)
- SOLID principles (SRP, OCP, LSP, DIP)
- Modern JavaScript patterns (ES6+, async/await, functional)
- Testability (dependency injection, pure functions)
- Performance optimization (memoization, debouncing)
- DRY and design patterns

**Use when:** Refactoring JavaScript/TypeScript code, improving maintainability, or applying SOLID principles

---

#### 3. **JavaScript Format/Style Refactoring Reviewer**
Solves JavaScript/TypeScript formatting and style issues through refactoring, not just line wrapping.

**Focus Areas:**
- Line length through extraction
- Complexity reduction (cyclomatic complexity)
- Function design and parameter refactoring
- Code organization and naming
- ESLint/Prettier issue resolution through refactoring

**Use when:** ESLint/Prettier complains and you want structural fixes instead of formatting

---

#### 4. **JavaScript Functional Reviewer**
Reviews JavaScript/TypeScript code using functional programming principles.

**Focus Areas:**
- Pure functions and immutability
- Array methods (map, filter, reduce)
- Function composition
- Avoiding side effects
- Functional patterns in JavaScript

**Use when:** Applying functional programming patterns in JavaScript/TypeScript projects

---

#### 5. **JavaScript Security & Privacy Reviewer**
Reviews JavaScript/TypeScript code for security vulnerabilities and privacy issues.

**Focus Areas:**
- OWASP Top 10 (XSS, injection, authentication, CSRF)
- Input validation and output encoding
- Authentication and session security (JWT, OAuth)
- Security headers (CSP, HSTS, CORS)
- API security (rate limiting, authentication)
- Data privacy (GDPR, CCPA, PII handling)
- Cryptography (strong algorithms, key management)
- Platform-specific (Node.js, React, Express security)

**Use when:** Reviewing JavaScript/TypeScript for security vulnerabilities, checking OWASP compliance, or auditing privacy

---

#### 6. **JavaScript Performance Reviewer**
Reviews JavaScript/TypeScript code for performance optimization opportunities.

**Focus Areas:**
- Algorithm complexity optimization (Big-O analysis, nested loops)
- Data structures (Set vs Array, Map vs Object, typed arrays)
- Memory management (leaks, closures, garbage collection)
- DOM operations (batching, layout thrashing, virtual scrolling)
- Async patterns (Promise.all, Web Workers, lazy loading)
- Bundling optimization (code splitting, tree shaking, compression)
- React-specific (memoization, keys, context splitting)
- Profiling and measurement (Chrome DevTools, Lighthouse)

**Use when:** Code is slow, optimizing performance, finding bottlenecks, improving FPS, or reducing bundle size

---

#### 7. **React Reviewer**
Reviews React code for best practices, patterns, performance, accessibility, and common pitfalls.

**Focus Areas:**
- Component design (single responsibility, composition, props)
- Hooks (dependencies, cleanup, custom hooks, rules)
- State management (lifting state, colocation, derived state)
- Rendering optimization (memoization, keys, lazy loading)
- Patterns (compound components, render props, portals)
- Accessibility (ARIA, keyboard navigation, focus management)
- Error handling (error boundaries, async errors)
- Testing (behavior testing, Testing Library queries)

**Use when:** Reviewing React components, debugging hooks, improving performance, or ensuring accessibility

---

### Python Skills

#### 8. **Rhodes Python Code Reviewer** ⭐ NEW
Reviews Python code using Brandon Rhodes' 70 coding principles from 15+ years of conference talks.

**Focus Areas:**
- Architecture (HOIST-IO, FUNC-SHELL, composition over inheritance)
- Testing (pure functions, avoiding mocks, test confidence)
- API Design (explicit names, immutability, showing cost)
- Naming (precise nouns, relentless verbs)
- Module Design (from python-patterns.guide)

**Use when:** Reviewing Python code for architecture, testability, clarity, or learning Rhodes' principles

---

#### 9. **Agile Requirements Reviewer**
Reviews software specifications, user stories, and use cases using agile requirements best practices.

**Focus Areas:**
- INVEST criteria for user stories
- Use case quality and completeness
- Problem domain focus (WHAT not HOW)
- Requirements clarity and testability
- Detection of over-engineering and gold-plating

**Use when:** Reviewing requirements, user stories, specifications, or acceptance criteria

---

#### 10. **Django Reviewer**
Comprehensive production readiness review for Django projects focusing on security, performance, and scalability.

**Focus Areas:**
- OWASP Top 10 and Django-specific security
- Database optimization and N+1 query prevention
- Django REST Framework API best practices
- Production configuration and deployment
- Performance and caching strategies
- Authentication and authorization
- Testing and code quality

**Use when:** Reviewing Django projects for production deployment, security audits, or performance optimization

---

#### 11. **Python Functional Reviewer**
Reviews Python code for functional programming patterns and best practices.

**Focus Areas:**
- Pure functions and immutability
- Higher-order functions
- Function composition
- Side effect management

**Use when:** You want to adopt functional programming patterns in Python

---

#### 12. **Python Performance Reviewer**
Reviews Python code for performance optimization opportunities.

**Focus Areas:**
- Algorithm complexity optimization (Big-O analysis)
- Data structures (set vs list, dict, deque, heapq)
- Memory management (generators, __slots__, gc)
- String operations (join, f-strings, compiled regex)
- List/iteration patterns (comprehensions, enumerate, zip)
- I/O optimization (streaming, batching, connection pooling)
- Concurrency (asyncio, threading, multiprocessing, GIL)
- Profiling and measurement (cProfile, line_profiler, memory_profiler)

**Use when:** Code is slow, optimizing performance, or finding bottlenecks

---

#### 13. **Python Security & Privacy Reviewer**
Comprehensive Python security and privacy review covering OWASP Top 10 and data protection.

**Focus Areas:**
- Input validation and injection prevention
- Authentication and authorization
- Data encryption and privacy
- Secure coding practices

**Use when:** Security is critical or handling sensitive data

---

#### 14. **Python Refactoring Reviewer**
Identifies refactoring opportunities to improve code quality, readability, and maintainability.

**Focus Areas:**
- Code smells detection
- SOLID principles
- DRY and design patterns
- Pythonic refactoring

**Use when:** Improving existing code or reducing technical debt

---

#### 15. **Python Zen Reviewer**
Reviews code against the 19 principles of the Zen of Python (PEP 20).

**Focus Areas:**
- Pythonic style and idioms
- Code aesthetics
- Simplicity and readability
- Python philosophy

**Use when:** Ensuring code follows Python's design philosophy

---

#### 16. **Python Format/Style Refactoring Reviewer**
Solves formatting and style issues through refactoring, not just line wrapping.

**Focus Areas:**
- Line length through extraction
- Complexity reduction
- Nesting elimination with guard clauses
- Parameter objects for long signatures

**Use when:** Linters complain and you want structural fixes

---

### General/Cross-Language Skills

#### 17. **Python Test Reviewer**
Reviews Python tests for quality and suggests multiple testing strategies.

**Focus Areas:**
- Test structure (AAA pattern)
- Multiple testing strategies
- Test doubles (mocks, stubs, fakes)
- Test quality over coverage

**Use when:** Reviewing tests or learning testing strategies

---

#### 18. **OpenAPI Reviewer**
Reviews OpenAPI/Swagger specifications for completeness, consistency, and API design best practices.

**Focus Areas:**
- OpenAPI 3.x structure and format
- RESTful path naming and HTTP methods
- Schema definitions and validation
- Security schemes and requirements
- Complete documentation with examples
- Response definitions and error handling

**Use when:** Reviewing API specifications, validating OpenAPI/Swagger files, or checking REST API design

---

#### 19. **Database Schema Reviewer**
Reviews relational database schemas for normalization, performance, and data integrity.

**Focus Areas:**
- Normalization (1NF through 5NF)
- Primary keys and foreign key relationships
- Indexing strategies and performance optimization
- Data types and column sizing
- Database-specific best practices (MySQL, PostgreSQL, SQL Server)
- Naming conventions and constraints

**Use when:** Reviewing database designs, DDL scripts, schema migrations, or optimizing database performance

---

## 🚀 Installation

### Automated Installation (Recommended)

The easiest way to install all skills to both Windows and WSL:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/claude-skills-public.git
cd claude-skills-public

# Run the installation script
python install_skills.py
```

This will automatically:
- Install all 19 skills to `~/.claude/skills/` on Windows
- Install all 19 skills to `~/.claude/skills/` on WSL (if available)
- Handle existing installations by replacing them with the latest version

### Manual Installation

#### Personal Installation (Available in All Projects)

Copy the entire collection to your personal Claude directory:

```bash
# Linux/Mac
git clone https://github.com/YOUR_USERNAME/claude-skills-public.git
cp -r claude-skills-public/*-reviewer ~/.claude/skills/

# Windows (PowerShell)
git clone https://github.com/YOUR_USERNAME/claude-skills-public.git
Copy-Item -Recurse "claude-skills-public\*-reviewer" "$env:USERPROFILE\.claude\skills\"
```

#### Project Installation (For Teams)

Clone into your project's `.claude/skills/` directory:

```bash
cd your-project
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/YOUR_USERNAME/claude-skills-public.git
```

Then update your project's `.claude/settings.json`:

```json
{
  "skills": [
    {
      "name": "python-security-privacy-reviewer",
      "path": "./.claude/skills/claude-skills-public/python-security-privacy-reviewer"
    }
  ]
}
```

### Individual Skill Installation

To install just one skill:

```bash
# Copy single skill to personal directory
cp -r python-functional-reviewer ~/.claude/skills/

# Or to project directory
cp -r python-functional-reviewer .claude/skills/
```

## 💡 How to Use

Once installed, skills activate automatically based on keywords in your requests:

```
"Review these Jest tests for quality"
"Refactor this JavaScript code to follow SOLID principles"
"Fix this ESLint complexity warning through refactoring"
"Apply functional patterns to this JavaScript"
"Review this code for XSS vulnerabilities"
"Check if this Node.js code is secure"
"This React component is slow - optimize it"
"Review this React component for best practices"
"Check my React hooks for issues"
"Find performance bottlenecks in this function"
"Review this user story for quality"
"Review this Django view for security and performance"
"Check this Django model for N+1 queries"
"Optimize this slow Python code"
"Find performance bottlenecks in this function"
"Review this code for security issues"
"Review this Python code using Rhodes guidelines"
"What would Brandon Rhodes say about this architecture?"
"Make this code more Pythonic"
"Refactor this Python code to be more maintainable"
"Review these pytest tests for quality"
"Fix this line length issue through refactoring"
"Review this OpenAPI specification"
"Review this database schema for normalization"
```

Or invoke directly:
```
"Use the javascript-test-reviewer on these tests"
"Use the javascript-refactoring-reviewer on this code"
"Use the javascript-format-refactoring-reviewer on this file"
"Use the javascript-functional-reviewer on this module"
"Use the javascript-security-privacy-reviewer on this API"
"Use the javascript-performance-reviewer on this slow component"
"Use the react-reviewer on this React component"
"Use the agile-requirements-reviewer on this specification"
"Use the python-rhodes-reviewer on this Python code"
"Use the django-reviewer on this Django project"
"Use the python-performance-reviewer on this slow code"
"Use the python-security-privacy-reviewer on this file"
"Use the python-refactoring-reviewer on this code"
"Use the python-zen-reviewer on this code"
"Use the python-functional-reviewer on this module"
"Use the openapi-reviewer on this API spec"
"Use the database-schema-reviewer on this DDL script"
```

## 🤖 Agentic Review Tool

**NEW:** Automated code review tool that reviews GitHub repositories using Claude Code skills!

Generate comprehensive markdown review reports for any public GitHub repository:

```bash
# Navigate to review-tool directory
cd review-tool

# Set your API key
export ANTHROPIC_API_KEY='your-key-here'

# Review a Django project
uv run review.py --repo https://github.com/django/django --reviewer django-reviewer --output-dir reports

# Multiple reviewers at once
uv run review.py --repo https://github.com/user/project \
  --reviewer django-reviewer \
  --reviewer python-security-privacy-reviewer \
  --output-dir reports
```

**Features:**
- 🔍 Automatically discovers and reviews relevant files
- 📊 Generates detailed markdown reports with findings
- 🎯 Supports all 19 reviewers
- ⚡ Can run multiple reviewers in one command
- 🛡️ Includes security, performance, and quality analysis
- 📦 Uses uv for fast, modern Python management

**Perfect for:**
- Demonstrating skill capabilities with real examples
- Automated code review in CI/CD
- Learning from popular open source projects
- Security audits and pre-production checks

👉 **See [review-tool/README.md](./review-tool/README.md) for complete documentation**

---

## 📚 Skill Details

### Comprehensive Coverage

Each skill provides:
- ✅ **Detailed analysis** with specific recommendations
- ✅ **Concrete examples** showing before/after code
- ✅ **Mnemonic IDs** for easy reference
- ✅ **Attribution** to authoritative sources
- ✅ **Best practices** from industry standards

### Quality Over Quantity

These skills focus on **depth and quality**:
- Detailed explanations, not just pattern matching
- Multiple approaches with trade-offs
- Complete, runnable code examples
- Educational content that teaches concepts

### Authoritative Sources

Based on established resources:
- **JavaScript/TypeScript:**
  - **Jest Documentation** - Jest testing best practices
  - **Vitest Documentation** - Modern testing patterns
  - **Testing Library** - User-centric component testing (Kent C. Dodds)
  - **clean-code-javascript** - JavaScript clean code principles
  - **Refactoring Guru** - Refactoring patterns
  - **ES6+ Best Practices** - Modern JavaScript patterns
  - **Functional JavaScript Principles** - FP in JavaScript
- **Python:**
  - **PEP 8, PEP 20** - Python style and philosophy
  - **pytest Documentation** - Python testing best practices
  - **Functional Programming Principles** - FP in Python
- **Django:**
  - **Django Documentation** - Official Django patterns, security, and best practices
  - **Two Scoops of Django** - Django community best practices
  - **Django REST Framework** - API design and implementation
- **API & Database:**
  - **OpenAPI Specification 3.x** - Official OpenAPI/Swagger standards
  - **REST API Design Principles** - Industry best practices for RESTful APIs
  - **Database Normalization Theory** - Codd, Date, Fagin (1NF-5NF, BCNF)
  - **MySQL/PostgreSQL/SQL Server Docs** - Database-specific best practices
- **Cross-Cutting:**
  - **IEEE 830, BABOK** - Requirements engineering standards
  - **INVEST Criteria** - Agile user story best practices
  - **OWASP Top 10** - Security standards
  - **Martin Fowler** - Software design and refactoring principles
  - **SOLID Principles** - Object-oriented design (Robert C. Martin)

## 🏗️ Skill Architecture

Each skill includes:

```
skill-name-reviewer/
├── SKILL.md       # Main skill definition with guidelines
├── README.md      # User documentation
└── SOURCES.md     # Detailed attribution
```

All guidelines are **self-contained** - no external dependencies needed.

## 🔍 Example Review

When you use a skill, you get structured feedback:

`````markdown
## Security Review: user_authentication.py

### ✅ Security Strengths
- **AUTH-BCRYPT**: Properly uses bcrypt for password hashing (line 45)

### 🚨 Security Issues

#### CRITICAL: SQL-INJECT - SQL Injection Vulnerability

**Current code:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**Secure code:**
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**Why this matters:**
Prevents attackers from injecting malicious SQL...

---
`````

**📂 See more examples:** [sample_reviews/](review-tool/sample_reviews/) contains 16 complete reviews of real open source projects including [HTTPie](https://github.com/httpie/cli) and [Datasette](https://github.com/simonw/datasette).

## 🤝 Contributing

Contributions are welcome! Please:
1. Follow the existing skill structure
2. Include comprehensive SOURCES.md with attribution
3. Provide complete code examples
4. Test skills thoroughly

## 📄 License

This collection is provided as-is for use with Claude Code. Individual skills include detailed attribution to their sources in SOURCES.md files.

## 🙏 Acknowledgments

These skills build upon the work of many contributors to software engineering best practices.

### Special Thanks to Brandon Rhodes

> Hey, folks, this is Brandon Rhodes, making a personal comment on this project, since Sankar was kind enough to ask my permission before making it public! While I myself am dismayed at the broad impact of AI on society so far, and have always been skeptical about automated code review (I've always used 'pyflakes' instead of 'flake8' because flake8's clumsy attempts to apply PEP-8 produce so much noise), I see no reason to stand in the way of this experiment. It tries to distill some of the guidelines that I've offered in my talks into a set of rules that can be applied by machine. I can't guess whether Claude Code will really understand when my ideas are useful and when they're not, but it's interesting to see how many pieces of advice worked their way into my talks over so many years.
>
> — Brandon Rhodes (December 2025)

The **Rhodes Python Code Reviewer** skill summarizes 70 coding principles from Brandon Rhodes' 15+ years of conference presentations (2010-2024) and his [Python Patterns Guide](https://python-patterns.guide/). This skill was released with Brandon Rhodes' permission. We are grateful for his decades of contributions to Python education.

- **Website:** https://rhodesmill.org/brandon/
- **Talks:** https://rhodesmill.org/brandon/talks/
- **Python Patterns:** https://python-patterns.guide/

### Additional Acknowledgments

**JavaScript/TypeScript:**
- **Jest Team** - Jest documentation and testing best practices
- **Vitest Team** (Anthony Fu and contributors) - Modern testing innovation
- **Testing Library Team** (Kent C. Dodds) - User-centric testing principles
- **Ryan McDermott** - clean-code-javascript adaptation
- **JavaScript Community** - ES6+ best practices and modern patterns

**Python:**
- **Python Software Foundation** - PEP 8, PEP 20, Python documentation
- **pytest Development Team** - Testing framework and documentation
- **Django Software Foundation** - Django documentation, security guidelines, best practices
- **Two Scoops of Django authors** - Django community standards and patterns
- **Django REST Framework contributors** - API design best practices

**API & Database:**
- **OpenAPI Initiative** - OpenAPI Specification 3.x standards
- **REST API Design Community** - RESTful API best practices (Google, Microsoft, Zalando, PayPal)
- **Database Theory Pioneers** - E.F. Codd, C.J. Date, Ronald Fagin (normalization theory)
- **MySQL/PostgreSQL/SQL Server Teams** - Database vendor documentation and best practices

**Software Engineering:**
- **Martin Fowler** - Refactoring, software design, and testing principles
- **Robert C. Martin (Uncle Bob)** - Clean Code and SOLID principles
- **Kent Beck** - Test-Driven Development and Extreme Programming
- **Refactoring Guru** - Refactoring patterns catalog
- **OWASP Foundation** - Security standards and guidelines
- **IEEE & IIBA** - Requirements engineering standards (IEEE 830, BABOK)
- **Agile Community** - INVEST criteria and agile requirements practices
- **Functional Programming Community** - FP principles and patterns

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check individual skill README files for specific guidance

---

**Quality reviews for better software projects.**
