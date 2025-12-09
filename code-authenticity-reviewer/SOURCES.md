# Sources and References

This document lists the sources, research, and best practices that informed the Code Authenticity Reviewer guidelines.

## LLM Code Generation Research

### Hallucination in Code Generation
- **"Large Language Models for Code: Security Hardening and Adversarial Testing"** - Research on LLM code generation vulnerabilities and hallucination patterns
- **"Do Users Write More Insecure Code with AI Assistants?"** (Stanford, 2022) - Study on AI-assisted code quality
- **"Lost in the Middle: How Language Models Use Long Contexts"** - Research on LLM context handling and potential fabrication

### Code Quality and Fabrication
- **"An Empirical Study of ChatGPT for Code Generation"** - Analysis of ChatGPT code generation patterns and common issues
- **"GitHub Copilot Investigation"** - Studies on AI pair programming quality and fabrication rates

## Software Testing Best Practices

### Test Quality
- **"xUnit Test Patterns"** by Gerard Meszaros - Patterns for effective test design
- **"The Art of Unit Testing"** by Roy Osherove - Guidelines for meaningful assertions
- **Google Testing Blog** - Best practices for avoiding brittle tests
- **Martin Fowler's Testing Articles** - Test doubles, mocking best practices

### Test Anti-Patterns
- **"Test Smells"** research - Cataloging problematic test patterns
- **"Why Most Unit Testing is Waste"** by James Coplien - Discussion on meaningful vs. trivial tests

## Code Quality Standards

### Dead Code and Unreachable Logic
- **"Clean Code"** by Robert C. Martin - Principles on removing dead code
- **Static Analysis Research** - Patterns for detecting unreachable code
- **Compiler Optimization Literature** - Dead code elimination techniques

### Code Smells
- **"Refactoring"** by Martin Fowler - Catalog of code smells including unused parameters
- **SonarQube Rules** - Static analysis rules for code quality issues
- **ESLint/Pylint Rules** - Linter rules for detecting unused variables and parameters

## Complexity Analysis

### Algorithmic Complexity
- **"Introduction to Algorithms"** (CLRS) - Standard reference for algorithm analysis
- **Big-O Cheat Sheet** - Common algorithm complexities
- **"Algorithm Design Manual"** by Steven Skiena - Practical complexity analysis

## API and Documentation Quality

### Documentation Accuracy
- **Write the Docs Community** - Standards for accurate technical documentation
- **API Documentation Best Practices** - Guidelines for accurate API references

### Cross-Reference Verification
- **Documentation Linters** - Tools for verifying documentation accuracy
- **Docstring Verification Tools** - Ensuring code-documentation consistency

## Security Considerations

### Fabricated Security Claims
- **OWASP Guidelines** - Security testing standards
- **"Secure Coding Practices"** - Ensuring security claims are verified

## Specific Pattern Sources

### Magic Numbers and Constants
- **"Clean Code"** Chapter 17 - Smells and Heuristics (G25: Replace Magic Numbers)
- **Code Complete** by Steve McConnell - Discussion on meaningful constants

### Unused Parameters
- **"Refactoring"** - Remove Parameter smell
- **Static analysis tools** - Rules for detecting unused function parameters

### Brittle Tests
- **"Working Effectively with Unit Tests"** by Jay Fields
- **Test Pyramid** concept by Mike Cohn
- **Google's Testing on the Toilet** series

### Mock Abuse
- **"Mocks Aren't Stubs"** by Martin Fowler
- **"Don't Mock What You Don't Own"** principle

## Related Tools and Approaches

### Static Analysis
- **SonarQube** - Code quality and security analysis
- **CodeClimate** - Automated code review
- **Pylint/ESLint** - Language-specific linters

### Code Coverage
- **Coverage.py** - Python code coverage
- **Istanbul/NYC** - JavaScript code coverage
- **JaCoCo** - Java code coverage

### Mutation Testing
- **mutmut** (Python) - Mutation testing to verify test quality
- **Stryker** (JavaScript) - Mutation testing framework
- **PIT** (Java) - Mutation testing

## Academic References

### Program Analysis
- **"Principles of Program Analysis"** by Nielson, Nielson, and Hankin
- **Data Flow Analysis** literature - Techniques for tracking variable usage

### Software Verification
- **Formal Methods** literature - Verification of program properties
- **Design by Contract** - Bertrand Meyer's work on assertions and contracts

## Industry Experience

### Code Review Practices
- **Google's Code Review Guidelines** - Industry-standard review practices
- **Microsoft's Code Review Best Practices** - Large-scale code review experience

### AI Code Review
- **GitHub Copilot Documentation** - Understanding AI-generated code patterns
- **Amazon CodeWhisperer Guidelines** - AI code generation best practices

---

## Note on Original Content

Many patterns in this reviewer are derived from:
1. Direct observation of LLM-generated code fabrication patterns
2. Common code review findings in AI-assisted development
3. Adaptation of traditional code smells to the AI generation context

The guidelines synthesize these sources into actionable patterns specifically designed to detect fabrication in code, with particular emphasis on issues common in LLM-generated code.
