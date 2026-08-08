# Security & Privacy Python Code Reviewer Skill

A Claude Code skill that reviews Python code for security vulnerabilities and privacy issues using industry best practices from OWASP, CWE, GDPR, and privacy regulations.

## What This Skill Does

This skill transforms Claude into a security and privacy code reviewer who:
- Identifies security vulnerabilities (OWASP Top 10, CWE)
- Detects privacy issues and PII handling problems
- Ensures GDPR, CCPA, and data protection compliance
- Provides secure code alternatives with explanations
- References industry standards and regulations

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r security-privacy-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "security-privacy-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r security-privacy-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/security-privacy-reviewer
git commit -m "Add Security & Privacy Reviewer skill"
```

**✅ Self-Contained:** All 60+ guidelines are embedded directly in skill.md - no external file references needed!

## How to Use

Simply ask Claude to review your Python code:

```
"Review this code for security vulnerabilities"
"Check this for OWASP issues"
"Is this code GDPR compliant?"
"Review for PII handling problems"
"Check for SQL injection vulnerabilities"
```

The skill will automatically activate based on keywords like:
- security, privacy, vulnerability
- OWASP, PII, GDPR
- encryption, authentication
- injection, XSS, CSRF

## What You'll Get

A structured security and privacy review with:
- ✅ **Strengths** - What's secure (with mnemonic IDs)
- 🔴 **Critical Issues** - Must fix immediately (e.g., **SQL-INJECT**, **NO-HARDCODE**)
- ⚠️ **Warnings** - Should fix (e.g., **WEAK-HASH**, **PII-LOG**)
- 💡 **Recommendations** - Best practices (e.g., **MFA-SUPPORT**, **DATA-ANONYMIZE**)
- 📋 **Compliance Checklist** - OWASP, GDPR, PCI DSS status

### Example Review

````markdown
## Security & Privacy Review: user_auth.py

### ✅ Strengths
- **ENCRYPT-TRANSIT**: All API calls use HTTPS with certificate validation
- **VALIDATE-INPUT**: Email validation implemented correctly

### 🔴 Critical Issues (Immediate Fix Required)

#### SQL-INJECT: SQL Injection Vulnerability

**Vulnerable code:**
```python
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
```

**Secure implementation:**
```python
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
```

**Security impact:**
Attackers can execute arbitrary SQL commands by injecting malicious input:
- `username = "admin' OR '1'='1"` bypasses authentication
- `username = "'; DROP TABLE users; --"` deletes data

**Compliance:**
- OWASP A1: Injection
- CWE-89: SQL Injection

---

#### NO-HARDCODE: Hardcoded Database Password

**Vulnerable code:**
```python
DB_PASSWORD = "admin123"
```

**Secure implementation:**
```python
import os
DB_PASSWORD = os.environ['DB_PASSWORD']
```

**Security impact:**
Hardcoded secrets in source code lead to instant compromise if:
- Code is committed to git (even private repos)
- Source code is shared or leaked
- Decompiled from binaries

**Compliance:**
- CWE-798: Use of Hard-coded Credentials

---

### ⚠️ Warnings (Should Fix)

#### PII-LOG: Logging Personally Identifiable Information

**Current code:**
```python
logging.info(f"User login: {email}")
```

**Recommended:**
```python
import hashlib

def hash_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

user_hash = hash_pii(email)
logging.info(f"User login: {user_hash}")
```

**Privacy impact:**
Logs containing PII can be:
- Accessed by unauthorized personnel
- Retained longer than necessary
- Exposed in breach incidents

**Compliance:**
- GDPR Article 32: Security of Processing
- CCPA: Personal Information Protection

---

### 💡 Recommendations (Best Practices)

#### MFA-SUPPORT: Implement Multi-Factor Authentication

**Current:**
```python
def login(username, password):
    if verify_password(username, password):
        create_session(username)
```

**Recommended:**
```python
import pyotp

def login(username, password, totp_code):
    if not verify_password(username, password):
        return False

    user = get_user(username)
    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(totp_code):
        return False

    create_session(username)
```

**Why this matters:**
MFA significantly reduces account takeover risk even if passwords are compromised.

---

### 📋 Compliance Checklist
- [x] OWASP A1 (Injection) - Parameterized queries used
- [ ] OWASP A2 (Auth) - MFA not implemented
- [x] OWASP A3 (XSS) - Output escaping implemented
- [ ] Secrets Management - Hardcoded password found
- [x] PII Encryption - PII encrypted at rest
- [ ] PII Logging - Email logged in plaintext
- [ ] GDPR Article 32 - Security measures incomplete
````

## The 60+ Guidelines

### Security Categories

1. **Injection Vulnerabilities** (6)
   - SQL-INJECT, CMD-INJECT, CODE-INJECT, PATH-TRAVERSE, LDAP-INJECT, XML-INJECT

2. **Authentication & Authorization** (7)
   - HASH-PASSWORD, WEAK-HASH, SESSION-SECURE, AUTHZ-CHECK, MFA-SUPPORT, TOKEN-EXPIRE, TIMING-ATTACK

3. **Cryptography** (8)
   - USE-CRYPTO-LIB, RANDOM-SECURE, ENCRYPT-REST, ENCRYPT-TRANSIT, KEY-MANAGE, AVOID-ECB, SALT-HASH, CERT-VALIDATE

4. **Input Validation & Sanitization** (6)
   - VALIDATE-INPUT, SANITIZE-OUTPUT, WHITELIST-INPUT, TYPE-CHECK, SIZE-LIMIT, ENCODING-CHECK

5. **Secrets Management** (5)
   - NO-HARDCODE, ENV-SECRETS, SECRET-VAULT, ROTATE-SECRETS, GIT-IGNORE

6. **Dependencies & Supply Chain** (4)
   - DEPS-UPDATE, DEPS-AUDIT, DEPS-MINIMIZE, DEPS-PIN

7. **Error Handling & Information Disclosure** (5)
   - ERROR-SAFE, NO-STACK-TRACE, LOG-SANITIZE, DEBUG-OFF, VERSION-HIDE

8. **Web Security** (6)
   - XSS-PREVENT, CSRF-PROTECT, CORS-RESTRICT, HEADER-SECURE, COOKIE-SECURE, CLICK-JACK

### Privacy Categories

#### 9. PII Handling (8)

- PII-IDENTIFY, PII-MINIMIZE, PII-ENCRYPT, PII-LOG, PII-MASK, PII-ACCESS, PII-TRANSFER, PII-CLASSIFY

#### 10. Consent & Transparency (5)

- CONSENT-EXPLICIT, CONSENT-GRANULAR, CONSENT-LOG, PURPOSE-LIMIT, PRIVACY-NOTICE

#### 11. Data Lifecycle (6)

- DATA-RETENTION, DATA-DELETE, DATA-PORTABILITY, DATA-ANONYMIZE, DATA-PSEUDONYMIZE, DATA-BACKUP

#### 12. Monitoring & Compliance (4)

- AUDIT-TRAIL, BREACH-DETECT, PRIVACY-IMPACT, DATA-INVENTORY

All 60+ guidelines with complete code examples are embedded in skill.md.

## Severity Levels

Reviews categorize issues by severity:

- **🔴 Critical** - Fix immediately (injection, hardcoded secrets, no auth, PII logged)
- **⚠️ Warning** - Should fix (weak crypto, missing headers, no retention policy)
- **💡 Recommendation** - Best practices (MFA, anonymization, enhanced monitoring)

## Standards & Compliance

This skill helps ensure compliance with:

- **OWASP Top 10** - Web application security risks
- **CWE Top 25** - Common weakness enumeration
- **GDPR** - General Data Protection Regulation
- **CCPA** - California Consumer Privacy Act
- **PCI DSS** - Payment Card Industry Data Security Standard
- **HIPAA** - Health Insurance Portability and Accountability Act (basics)

## Example Use Cases

### Security Review
```
"Review this authentication code for security issues"
"Check this API endpoint for OWASP vulnerabilities"
"Is this cryptography implementation secure?"
```

### Privacy Review
```
"Review this for GDPR compliance"
"Check if PII is handled correctly"
"Does this implement user data deletion properly?"
```

### Compliance Audit
```
"Audit this code for OWASP Top 10"
"Check compliance with privacy regulations"
"Review for PCI DSS requirements"
```

## Benefits

- ✅ **Comprehensive** - 60+ security and privacy guidelines
- ✅ **Actionable** - Concrete code fixes, not just descriptions
- ✅ **Educational** - Explains why each issue matters
- ✅ **Compliance-Focused** - References OWASP, GDPR, CWE, etc.
- ✅ **Practical** - Real-world examples and attack scenarios
- ✅ **Up-to-Date** - Based on latest security best practices

## What Gets Checked

### Security Checks
- SQL, command, and code injection vulnerabilities
- Authentication and authorization flaws
- Cryptography misuse (weak algorithms, ECB mode, etc.)
- Input validation gaps
- Hardcoded secrets and poor key management
- Vulnerable dependencies
- Information disclosure (stack traces, debug mode)
- XSS, CSRF, and web security issues

### Privacy Checks
- PII identification and classification
- Data minimization and retention
- Encryption of sensitive data
- PII in logs and outputs
- Consent management
- User rights (deletion, portability, access)
- Anonymization and pseudonymization
- Audit trails and breach detection

## Sources and Attribution

This skill is based on public standards and best practices:
- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [GDPR](https://gdpr.eu/)
- Python Security Best Practices
- Cloud Security Alliance Guidelines

**📚 [View Complete Sources Documentation →](SOURCES.md)**

The SOURCES.md file provides detailed attribution for all 60+ guidelines, including:
- Specific OWASP/CWE/GDPR article mappings for each guideline
- Web search results and research methodology
- Python library documentation references
- Code example attribution
- License information for all source materials

## License

This skill compilation is provided for educational and security improvement purposes. The standards referenced (OWASP, CWE, GDPR) are public domain or openly available.

---

**Stay Secure. Protect Privacy. Build Trust.** 🔒🛡️
