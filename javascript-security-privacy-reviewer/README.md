# JavaScript Security & Privacy Reviewer Skill

A Claude Code skill that reviews JavaScript/TypeScript code for security vulnerabilities and privacy issues. **Comprehensive OWASP-based security review** - covers injection attacks, XSS, authentication, CSRF, API security, data privacy (GDPR/CCPA), cryptography, and platform-specific vulnerabilities.

## What This Skill Does

This skill transforms Claude into a JavaScript/TypeScript security expert who:
- **Identifies security vulnerabilities** - XSS, injection, auth flaws, cryptographic failures
- **Checks privacy compliance** - GDPR, CCPA, PII handling, data minimization
- **Provides secure code examples** - Concrete before/after demonstrations
- **Explains attack scenarios** - How vulnerabilities are exploited
- **Maps to standards** - OWASP Top 10, CWE, GDPR articles
- **Categorizes by severity** - Critical, High, Medium

## Philosophy

> **"Security is not a product, but a process."** - Bruce Schneier

> **"The S in IoT stands for Security"** - Internet joke highlighting security importance

This skill emphasizes defense in depth - multiple layers of security controls to protect against evolving threats.

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r javascript-security-privacy-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "javascript-security-privacy-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r javascript-security-privacy-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/javascript-security-privacy-reviewer
git commit -m "Add JavaScript Security & Privacy Reviewer skill"
```

**✅ Self-Contained:** All 72 guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your code for security or privacy issues:

```
"Review this code for security vulnerabilities"
"Check for XSS vulnerabilities in this React component"
"Review this authentication implementation"
"Check if this code is GDPR compliant"
"Find security issues in this Express API"
"Review this Node.js app for OWASP Top 10 issues"
```

The skill will automatically activate based on keywords like:
- security, vulnerability, OWASP
- XSS, injection, CSRF
- authentication, authorization
- privacy, GDPR, PII
- encryption, cryptography

## What You'll Get

A comprehensive security review with:
- **Severity Classification** - Critical (immediate fix), High (fix soon), Medium (recommended)
- **Vulnerable Code** - Shows the security issue
- **Secure Implementation** - Shows how to fix it
- **Security Impact** - Explains the attack and consequences
- **Compliance Mapping** - OWASP, CWE, GDPR references
- **Mnemonic IDs** - Easy reference (e.g., XSS-ESCAPE, SQL-INJECT)

### Example Review

````markdown
## Security & Privacy Review: UserController

### 🔴 Critical Issues (Immediate Fix Required)

#### SQL-INJECT: SQL Injection Vulnerability

**Vulnerable code:**
```javascript
const userId = req.query.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);
```

**Secure implementation:**
```javascript
const userId = req.query.id;
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

**Security impact:**
SQL injection allows attackers to execute arbitrary SQL, leading to data theft, modification, or deletion.

**Compliance:** OWASP A03:2021 - Injection, CWE-89
````

## The 72 Security Guidelines

### Input Validation & Injection (10 guidelines)
- **SQL-INJECT** - Prevent SQL injection with parameterized queries
- **NOSQL-INJECT** - Prevent NoSQL injection in MongoDB
- **CMD-INJECT** - Prevent command injection in child_process
- **XPATH-INJECT** - Prevent XPath injection
- **LDAP-INJECT** - Prevent LDAP injection
- **TEMPLATE-INJECT** - Prevent server-side template injection
- **PATH-TRAV** - Prevent path traversal attacks
- **CODE-INJECT** - Prevent code injection (eval, Function)
- **PARAM-POLLUT** - Prevent HTTP parameter pollution
- **REGEX-DOS** - Prevent Regular Expression DoS

### XSS Prevention (8 guidelines)
- **XSS-REFLECT** - Prevent reflected XSS
- **XSS-STORED** - Prevent stored XSS
- **XSS-DOM** - Prevent DOM-based XSS
- **XSS-MUTATION** - Prevent mutation XSS (mXSS)
- **XSS-ESCAPE** - Context-aware output escaping
- **CSP-HEADER** - Implement Content Security Policy
- **SANITIZE-LIB** - Use sanitization libraries (DOMPurify)
- **DANGEROUS-HTML** - Avoid React dangerouslySetInnerHTML

### Authentication & Sessions (9 guidelines)
- **PASSWORD-HASH** - Use bcrypt/argon2 for passwords
- **PASSWORD-POLICY** - Enforce strong password requirements
- **JWT-SECRET** - Secure JWT implementation
- **JWT-EXPIRE** - Implement token expiration and refresh
- **SESSION-SECURE** - Secure session management
- **OAUTH-VALIDATE** - Validate OAuth/OIDC properly
- **MFA-IMPLEMENT** - Implement multi-factor authentication
- **CRED-STORE** - Secure credential storage
- **TIMING-ATTACK** - Prevent timing attacks

### CSRF & Security Headers (7 guidelines)
- **CSRF-TOKEN** - Implement CSRF protection
- **SAMESITE-COOKIE** - Use SameSite cookie attribute
- **HTTPS-ONLY** - Enforce HTTPS
- **HSTS-HEADER** - Use HTTP Strict Transport Security
- **CSP-POLICY** - Strong Content Security Policy
- **X-FRAME-OPTIONS** - Prevent clickjacking
- **CORS-CONFIG** - Secure CORS configuration

### API Security (6 guidelines)
- **RATE-LIMIT** - Implement rate limiting
- **API-AUTH** - Secure API authentication
- **API-VALIDATE** - Validate API input
- **API-KEY-SECURE** - Secure API key management
- **API-ERROR** - Secure error responses
- **API-VERSIONING** - API versioning and deprecation

### Data Privacy (10 guidelines)
- **PII-IDENTIFY** - Identify and classify PII
- **PII-MINIMIZE** - Data minimization principle
- **PII-ENCRYPT** - Encrypt PII at rest
- **PII-LOG** - Don't log PII
- **CONSENT-MANAGE** - Implement consent management
- **DATA-ERASURE** - Implement right to erasure (GDPR)
- **DATA-EXPORT** - Implement right to data portability
- **GDPR-COMPLY** - GDPR compliance checklist
- **ANONYMIZE-DATA** - Data anonymization
- **AUDIT-LOG** - Implement audit logging

### Cryptography (7 guidelines)
- **CRYPTO-STRONG** - Use strong cryptographic algorithms
- **KEY-MANAGE** - Secure key management
- **RANDOM-SECURE** - Use cryptographically secure random
- **SALT-HASH** - Always salt hashes
- **CERT-VALIDATE** - Validate SSL/TLS certificates
- **CRYPTO-DEPRECATE** - Avoid deprecated cryptography
- **ENCRYPT-REST** - Encrypt data at rest

### Error Handling (4 guidelines)
- **ERROR-DISCLOSE** - Prevent information disclosure
- **STACK-TRACE** - Don't expose stack traces
- **ERROR-LOG** - Secure error logging
- **TRY-CATCH** - Proper exception handling

### Dependencies (4 guidelines)
- **NPM-AUDIT** - Run npm audit regularly
- **VULN-DEPS** - Monitor vulnerable dependencies
- **DEP-PIN** - Pin dependency versions
- **SUPPLY-CHAIN** - Supply chain security

### Platform-Specific (7 guidelines)
- **NODE-EVAL** - Avoid eval() and Function constructor
- **NODE-CHILD-PROCESS** - Secure child_process usage
- **REACT-DANGEROUS** - Avoid dangerouslySetInnerHTML
- **EXPRESS-BODY** - Secure body parsing
- **FILE-ACCESS** - Secure file operations
- **PROTOTYPE-POLLUT** - Prevent prototype pollution
- **DESERIALIZATION** - Secure deserialization

## Key Differentiators

### OWASP Top 10 Coverage

Full coverage of OWASP Top 10 2021:
- **A01:2021** - Broken Access Control (CORS, CSRF, PATH-TRAV)
- **A02:2021** - Cryptographic Failures (CRYPTO-STRONG, KEY-MANAGE, ENCRYPT-REST)
- **A03:2021** - Injection (SQL, NoSQL, XSS, CMD, CODE)
- **A04:2021** - Insecure Design (ERROR-DISCLOSE, API-ERROR)
- **A05:2021** - Security Misconfiguration (CSP, HSTS, CORS)
- **A06:2021** - Vulnerable Components (NPM-AUDIT, VULN-DEPS)
- **A07:2021** - Identification/Authentication Failures (PASSWORD-HASH, JWT, SESSION)
- **A08:2021** - Software and Data Integrity Failures (PROTOTYPE-POLLUT, DESERIALIZATION)
- **A09:2021** - Security Logging Failures (AUDIT-LOG, ERROR-LOG)
- **A10:2021** - Server-Side Request Forgery (SSRF) - Covered in validation guidelines

### GDPR/CCPA Compliance

Privacy regulation coverage:
- Data minimization (PII-MINIMIZE)
- Consent management (CONSENT-MANAGE)
- Right to erasure (DATA-ERASURE)
- Right to portability (DATA-EXPORT)
- Data protection by design (PII-ENCRYPT)
- Breach notification (GDPR-COMPLY)
- Audit trails (AUDIT-LOG)

### Platform-Specific Security

JavaScript/TypeScript/Node.js specific:
- eval() and code injection
- Prototype pollution
- Node.js child_process security
- React security (dangerouslySetInnerHTML)
- Express.js security
- npm dependency security
- JWT and session management

### Before/After Code Examples

Every guideline includes:
- Vulnerable code showing the security issue
- Secure implementation showing the fix
- Explanation of the attack scenario
- Compliance mapping (OWASP, CWE, GDPR)

## Common Patterns This Skill Teaches

### ✅ Do This
```javascript
// Parameterized queries
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// Strong password hashing
const hash = await bcrypt.hash(password, 12);

// Secure session config
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict'
  }
}));

// Input validation
const schema = Joi.object({
  email: Joi.string().email().required()
});
```

### ❌ Not This
```javascript
// SQL injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Weak password storage
const hash = crypto.createHash('md5').update(password).digest('hex');

// Insecure sessions
app.use(session({
  secret: 'keyboard cat',
  cookie: {}
}));

// No validation
const email = req.body.email; // Trust user input
```

## Example Use Cases

### Security Audit
- "Review this Express API for OWASP Top 10 vulnerabilities"
- "Check this authentication system for security issues"
- "Find XSS vulnerabilities in this React app"

### Pre-Production Review
- "Security review before deployment"
- "Check if this handles PII securely"
- "Verify HTTPS and security headers are configured"

### Incident Response
- "We were hacked - what vulnerabilities exist?"
- "Review logs for security issues"
- "Check if we're vulnerable to the latest CVE"

### Compliance Check
- "Is this GDPR compliant?"
- "Check CCPA compliance for data handling"
- "Verify we meet PCI-DSS requirements"

## Benefits

- ✓ **Find vulnerabilities** - XSS, injection, auth flaws before production
- ✓ **OWASP Top 10 coverage** - Industry-standard security checklist
- ✓ **Privacy compliance** - GDPR, CCPA, PII handling
- ✓ **Secure code examples** - Copy-paste-ready fixes
- ✓ **Attack explanations** - Understand the "why" behind security
- ✓ **Severity classification** - Prioritize fixes (Critical/High/Medium)
- ✓ **Platform-specific** - JavaScript, Node.js, React, Express security
- ✓ **Compliance mapping** - OWASP, CWE, GDPR references

## What Gets Checked

### Input Validation
- SQL, NoSQL, command, XPath, LDAP injection
- Path traversal
- Code injection (eval, Function)
- Parameter pollution
- ReDoS (Regular Expression DoS)

### Output Encoding
- Reflected, stored, DOM-based XSS
- Context-aware escaping (HTML, JS, URL, CSS)
- Template injection
- Mutation XSS

### Authentication & Authorization
- Password hashing (bcrypt, argon2)
- JWT security (secret, expiration, algorithm)
- Session management (secure, httpOnly, sameSite)
- OAuth/OIDC validation
- Multi-factor authentication

### Security Headers
- CSRF protection (tokens, SameSite)
- HTTPS enforcement
- HSTS, CSP, X-Frame-Options
- CORS configuration

### Cryptography
- Strong algorithms (AES-256, SHA-256)
- Key management
- Secure random generation
- Certificate validation
- Avoiding deprecated crypto (MD5, SHA-1, DES)

### Privacy & Data Protection
- PII identification and classification
- Data minimization
- Encryption at rest
- Consent management
- Right to erasure and portability
- GDPR/CCPA compliance

### Platform Security
- eval() and code execution
- Prototype pollution
- Deserialization attacks
- Dependency vulnerabilities
- npm audit issues

## Supported Technologies

- **Runtime:** Node.js, Deno, Bun
- **Frameworks:** Express, Fastify, Koa, Hapi, NestJS
- **Frontend:** React, Vue, Angular, Svelte
- **Databases:** MongoDB, PostgreSQL, MySQL, Redis
- **Auth:** JWT, OAuth, Session-based, Passport.js
- **Testing:** Can review security tests

## Sources and Attribution

All guidelines are based on:
- **OWASP Top 10 2021** - Web application security risks
- **OWASP Cheat Sheets** - XSS, SQL Injection, Authentication, Session Management
- **CWE Top 25** - Most dangerous software weaknesses
- **Node.js Security Best Practices** - Official Node.js security guide
- **GDPR** - General Data Protection Regulation
- **CCPA** - California Consumer Privacy Act
- **NIST Guidelines** - Cryptography, password hashing
- **React Security** - Official React security documentation
- **npm Security** - npm audit, dependency security

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## Security Philosophy

### Defense in Depth

Use multiple layers of security:
1. Input validation
2. Output encoding
3. Authentication and authorization
4. HTTPS and security headers
5. Rate limiting
6. Logging and monitoring

### Principle of Least Privilege

- Minimal permissions for users and services
- API keys with scoped access
- Database users with minimal grants

### Secure by Default

- HTTPS by default
- httpOnly, secure cookies
- Strong crypto algorithms
- Auto-escaping in templates

### Fail Securely

- Deny by default
- Generic error messages
- Graceful degradation

## Tips for Getting the Most Out of This Skill

1. **Provide context**: "This is a payment API handling credit cards"
2. **Specify concerns**: "Focus on XSS and authentication"
3. **Include dependencies**: Mention frameworks (Express, React, etc.)
4. **Ask about compliance**: "Check GDPR compliance"
5. **Request severity**: "Show only Critical and High severity issues"

## License

This skill is licensed under MIT. It is based on public security standards (OWASP, CWE, GDPR) and best practices.

---

**Security is a journey, not a destination. Review early, review often.**
