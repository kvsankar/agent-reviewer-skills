# Claude Code Skills - Python Code Reviewer Collection

A curated collection of high-quality Claude Code skills for reviewing Python code. Each skill focuses on a specific aspect of code quality, providing detailed analysis and actionable recommendations.

## 🎯 Available Skills

### 1. **Functional Python Reviewer**
Reviews Python code for functional programming patterns and best practices.

**Focus Areas:**
- Pure functions and immutability
- Higher-order functions
- Function composition
- Side effect management

**Use when:** You want to adopt functional programming patterns in Python

---

### 2. **Security & Privacy Reviewer**
Comprehensive security and privacy review covering OWASP Top 10 and data protection.

**Focus Areas:**
- Input validation and injection prevention
- Authentication and authorization
- Data encryption and privacy
- Secure coding practices

**Use when:** Security is critical or handling sensitive data

---

### 3. **Refactoring Reviewer**
Identifies refactoring opportunities to improve code quality, readability, and maintainability.

**Focus Areas:**
- Code smells detection
- SOLID principles
- DRY and design patterns
- Pythonic refactoring

**Use when:** Improving existing code or reducing technical debt

---

### 4. **Zen of Python Reviewer**
Reviews code against the 19 principles of the Zen of Python (PEP 20).

**Focus Areas:**
- Pythonic style and idioms
- Code aesthetics
- Simplicity and readability
- Python philosophy

**Use when:** Ensuring code follows Python's design philosophy

---

### 5. **Format/Style Refactoring Reviewer**
Solves formatting and style issues through refactoring, not just line wrapping.

**Focus Areas:**
- Line length through extraction
- Complexity reduction
- Nesting elimination with guard clauses
- Parameter objects for long signatures

**Use when:** Linters complain and you want structural fixes

---

### 6. **Python Test Reviewer**
Reviews Python tests for quality and suggests multiple testing strategies.

**Focus Areas:**
- Test structure (AAA pattern)
- Multiple testing strategies
- Test doubles (mocks, stubs, fakes)
- Test quality over coverage

**Use when:** Reviewing tests or learning testing strategies

---

## 🚀 Installation

### Personal Installation (Available in All Projects)

Copy the entire collection to your personal Claude directory:

```bash
# Linux/Mac
git clone https://github.com/YOUR_USERNAME/claude-skills.git
cp -r claude-skills ~/.claude/skills/

# Windows (PowerShell)
git clone https://github.com/YOUR_USERNAME/claude-skills.git
Copy-Item -Recurse "claude-skills" "$env:USERPROFILE\.claude\skills\"
```

### Project Installation (For Teams)

Clone into your project's `.claude/skills/` directory:

```bash
cd your-project
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/YOUR_USERNAME/claude-skills.git
```

Then update your project's `.claude/settings.json`:

```json
{
  "skills": [
    {
      "name": "security-privacy-reviewer",
      "path": "./.claude/skills/claude-skills/security-privacy-reviewer"
    }
  ]
}
```

### Individual Skill Installation

To install just one skill:

```bash
# Copy single skill to personal directory
cp -r functional-python-reviewer ~/.claude/skills/

# Or to project directory
cp -r functional-python-reviewer .claude/skills/
```

## 💡 How to Use

Once installed, skills activate automatically based on keywords in your requests:

```
"Review this code for security issues"
"Make this code more Pythonic"
"Refactor this to be more maintainable"
"Review these tests for quality"
"Fix this line length issue through refactoring"
```

Or invoke directly:
```
"Use the security reviewer on this file"
"Apply functional Python patterns here"
```

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
- **PEP 8, PEP 20** - Python style and philosophy
- **OWASP Top 10** - Security standards
- **Refactoring Guru** - Refactoring patterns
- **Martin Fowler** - Software design principles
- **pytest Documentation** - Testing best practices
- **Hypothesis** - Property-based testing

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

```markdown
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
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Follow the existing skill structure
2. Include comprehensive SOURCES.md with attribution
3. Provide complete code examples
4. Test skills thoroughly

## 📄 License

This collection is provided as-is for use with Claude Code. Individual skills include detailed attribution to their sources in SOURCES.md files.

## 🙏 Acknowledgments

These skills build upon the work of many contributors to Python and software engineering best practices:

- **Python Software Foundation** - PEP 8, PEP 20, Python documentation
- **OWASP Foundation** - Security standards and guidelines
- **Refactoring Guru** - Refactoring patterns catalog
- **Martin Fowler** - Software design and testing principles
- **pytest Development Team** - Testing framework and documentation
- **Testing Community** - Established testing patterns and practices

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check individual skill README files for specific guidance

---

**Quality code reviews for better Python projects.**
