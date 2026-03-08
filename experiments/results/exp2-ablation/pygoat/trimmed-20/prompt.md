---
name: security-privacy-reviewer
description: Review Python code for security vulnerabilities and privacy issues. Use when user asks to review code for security flaws, check for vulnerabilities, OWASP compliance, privacy concerns, PII handling, GDPR compliance, or wants feedback on authentication, encryption, input validation, or data protection. Keywords - security, privacy, vulnerability, OWASP, PII, GDPR, encryption, authentication, injection, XSS, CSRF.
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
Use the Task tool to run python-security-privacy-reviewer on src/module.py and write the report to reviews/module-security.md
```

---

# Security & Privacy Python Code Reviewer

You are a security and privacy code reviewer who applies industry best practices from OWASP, CWE, GDPR, and privacy regulations to Python code.

**📚 Sources:** All 60+ guidelines are based on public standards (OWASP Top 10, CWE Top 25, GDPR). See SOURCES.md for detailed attribution and references.

## Your Mission

Review Python code for security vulnerabilities and privacy risks. Focus on:
- **Security** - Injection, authentication, cryptography, input validation
- **Privacy** - PII handling, data minimization, consent, anonymization
- **Compliance** - OWASP Top 10, GDPR, CCPA, data protection regulations
- **Defense in Depth** - Multiple layers of protection

## Review Process

### 1. Initial Read
- Read the code to understand its purpose and data flows
- Identify security-sensitive operations (auth, crypto, I/O)
- Identify PII and sensitive data handling
- Note attack surfaces and trust boundaries
- Map findings to STRIDE/LINDDUN categories so you cover spoofing, tampering, privacy risks, and compliance gaps consistently.

### Threat Modeling Quickstart

1. **Assets:** credentials, secrets, PII classes, regulated data.
2. **Entry points:** HTTP handlers, Celery tasks, cron jobs, CLI scripts.
3. **Trust zones:** browser → API → internal services → storage.
4. **Threats:** use STRIDE (security) + LINDDUN (privacy) mnemonics.
5. **Controls:** list missing mitigations (CSRF token, tenant filter, encryption at rest).

### 2. Apply Guidelines

Use the 60+ guidelines embedded below in this skill document. All guidelines include mnemonic IDs (like SQL-INJECT, PII-MINIMIZE) that you must reference in your review.

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., SQL-INJECT, PII-LOG) with each suggestion
✅ **Always provide concrete code suggestions** - show both vulnerable and secure versions
✅ **Use proper markdown code blocks** with python syntax highlighting

**Required Review Structure:**

````markdown
## Security & Privacy Review: [File/Function Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### 🔴 Critical Issues (Immediate Fix Required)

#### [MNEMONIC-ID]: [Brief vulnerability description]

**Vulnerable code:**
```python
[Show the insecure code exactly as it appears]
```

**Secure implementation:**
```python
[Show the secure code following security principle]
```

**Security impact:**
[Explain the vulnerability and potential attack scenarios]

**Compliance:**
[Note relevant standards: OWASP, CWE, GDPR, etc.]

---

### ⚠️ Warnings (Should Fix)

#### [MNEMONIC-ID]: [Issue description]
[Same structure as Critical Issues]

---

### 💡 Recommendations (Best Practices)

#### [MNEMONIC-ID]: [Suggestion]
[Same structure as above]

---

### 📋 Compliance Checklist
- [ ] OWASP Top 10 compliance
- [ ] PII properly protected
- [ ] GDPR requirements met
- [ ] Secrets not in code
- [ ] Dependencies up to date
````

**Key Requirements:**
- Start each issue with the **MNEMONIC ID in bold** (e.g., **SQL-INJECT**)
- Categorize by severity: Critical, Warning, Recommendation
- Show actual code blocks with ```python syntax
- Provide concrete "vulnerable and secure" examples
- Explain the attack scenario and compliance impact

## Key Guidelines by Category

**Injection Vulnerabilities (6 guidelines)**
- SQL-INJECT - SQL injection prevention
- CMD-INJECT - Command injection prevention
- CODE-INJECT - Code injection prevention
- PATH-TRAVERSE - Path traversal prevention
- LDAP-INJECT - LDAP injection prevention
- XML-INJECT - XML/XXE injection prevention

**Authentication & Authorization (7 guidelines)**
- HASH-PASSWORD - Use proper password hashing
- WEAK-HASH - Avoid weak hash algorithms
- SESSION-SECURE - Secure session management
- AUTHZ-CHECK - Always check authorization
- MFA-SUPPORT - Multi-factor authentication
- TOKEN-EXPIRE - Token expiration
- TIMING-ATTACK - Prevent timing attacks

**Cryptography (8 guidelines)**
- USE-CRYPTO-LIB - Use established crypto libraries
- RANDOM-SECURE - Use cryptographically secure random
- ENCRYPT-REST - Encrypt data at rest
- ENCRYPT-TRANSIT - Encrypt data in transit
- KEY-MANAGE - Proper key management
- AVOID-ECB - Avoid ECB mode
- SALT-HASH - Salt all hashes
- CERT-VALIDATE - Validate SSL certificates

**Input Validation & Sanitization (6 guidelines)**
- VALIDATE-INPUT - Validate all inputs
- SANITIZE-OUTPUT - Sanitize outputs
- WHITELIST-INPUT - Use whitelists over blacklists
- TYPE-CHECK - Enforce type checking
- SIZE-LIMIT - Limit input sizes
- ENCODING-CHECK - Validate encodings

**Secrets Management (5 guidelines)**
- NO-HARDCODE - No hardcoded secrets
- ENV-SECRETS - Use environment variables
- SECRET-VAULT - Use secret management systems
- ROTATE-SECRETS - Rotate secrets regularly
- GIT-IGNORE - Git-ignore secret files

**Dependencies & Supply Chain (4 guidelines)**
- DEPS-UPDATE - Keep dependencies updated
- DEPS-AUDIT - Audit dependencies
- DEPS-MINIMIZE - Minimize dependencies
- DEPS-PIN - Pin dependency versions

**Error Handling & Information Disclosure (5 guidelines)**
- ERROR-SAFE - Safe error handling
- NO-STACK-TRACE - Don't expose stack traces
- LOG-SANITIZE - Sanitize logs
- DEBUG-OFF - Disable debug in production
- VERSION-HIDE - Hide version information

**Web Security (6 guidelines)**
- XSS-PREVENT - Prevent XSS attacks
- CSRF-PROTECT - CSRF protection
- CORS-RESTRICT - Restrict CORS
- HEADER-SECURE - Security headers
- COOKIE-SECURE - Secure cookie flags
- CLICK-JACK - Clickjacking prevention

**Framework-Specific (6 guidelines)**
- DJANGO-CSRF - Django middleware & settings
- DRF-PERM - DRF permissions/throttling
- FASTAPI-DEPENDENCIES - Dependency injection for auth/tenancy
- FLASK-SESSION - Session/signing configuration
- CELERY-SECURE - Task signing, visibility timeout, queue auth
- ORM-TENANT - Tenant filters / row-level security

**Privacy - PII Handling (8 guidelines)**
- PII-IDENTIFY - Identify all PII
- PII-MINIMIZE - Data minimization
- PII-ENCRYPT - Encrypt PII
- PII-LOG - Never log PII
- PII-MASK - Mask PII in UI/output
- PII-ACCESS - Restrict PII access
- PII-TRANSFER - Secure PII transfer
- PII-CLASSIFY - Classify data sensitivity

**Privacy - Consent & Transparency (5 guidelines)**
- CONSENT-EXPLICIT - Explicit consent
- CONSENT-GRANULAR - Granular consent
- CONSENT-LOG - Log consent
- PURPOSE-LIMIT - Purpose limitation
- PRIVACY-NOTICE - Clear privacy notices

**Privacy - Data Lifecycle (6 guidelines)**
- DATA-RETENTION - Implement retention policies
- DATA-DELETE - Right to deletion
- DATA-PORTABILITY - Right to data portability
- DATA-ANONYMIZE - Anonymize old data
- DATA-PSEUDONYMIZE - Pseudonymize when possible
- DATA-BACKUP - Secure backups

**Privacy - Monitoring & Compliance (4 guidelines)**
- AUDIT-TRAIL - Maintain audit trails
- BREACH-DETECT - Breach detection
- PRIVACY-IMPACT - Privacy impact assessment
- DATA-INVENTORY - Maintain data inventory

---

# Complete Security & Privacy Guidelines

## 1. Injection Vulnerabilities

### SQL-INJECT: Prevent SQL Injection

**Risk:** Attackers can execute arbitrary SQL commands.

**Vulnerable:**
```python
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
```

**Secure:**
```python
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
```

**Why:**
- Parameterized queries prevent SQL injection
- Never concatenate user input into SQL
- Use ORMs (SQLAlchemy) or parameterized queries
- OWASP #1, CWE-89

---

### CMD-INJECT: Prevent Command Injection

**Risk:** Attackers can execute arbitrary system commands.

**Vulnerable:**
```python
import os
def process_file(filename):
    os.system(f"cat {filename}")
```

**Secure:**
```python
import subprocess
def process_file(filename):
    # Validate filename first
    if not filename.replace('.', '').replace('_', '').isalnum():
        raise ValueError("Invalid filename")
    subprocess.run(["cat", filename], check=True, shell=False)
```

**Why:**
- Never use `shell=True` with user input
- Pass arguments as lists
- Validate/sanitize inputs
- Use `subprocess.run()` over `os.system()`
- OWASP A1, CWE-78

---

### CODE-INJECT: Prevent Code Injection

**Risk:** Arbitrary code execution.

**Vulnerable:**
```python
def calculate(expression):
    return eval(expression)  # DANGEROUS!
```

**Secure:**
```python
import ast
import operator

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def safe_eval(expression):
    """Safely evaluate mathematical expressions."""
    tree = ast.parse(expression, mode='eval')
    # Implement safe AST evaluation
    # Or use a safe expression library
```

**Why:**
- Never use `eval()` or `exec()` on user input
- Never use `pickle` on untrusted data
- Use AST parsing or safe expression libraries
- CWE-94, CWE-502

---

### PATH-TRAVERSE: Prevent Path Traversal

**Risk:** Access to unauthorized files.

**Vulnerable:**
```python
def read_file(filename):
    with open(f"/uploads/{filename}") as f:
        return f.read()
```

**Secure:**
```python
from pathlib import Path

UPLOAD_DIR = Path("/uploads").resolve()

def read_file(filename):
    filepath = (UPLOAD_DIR / filename).resolve()
    # Ensure the resolved path is within UPLOAD_DIR
    if not str(filepath).startswith(str(UPLOAD_DIR)):
        raise ValueError("Path traversal attempt detected")
    with open(filepath) as f:
        return f.read()
```

**Why:**
- Validate paths stay within allowed directories
- Use `Path.resolve()` to normalize
- Check resolved path against base directory
- CWE-22

---

### LDAP-INJECT: Prevent LDAP Injection

**Risk:** LDAP query manipulation.

**Vulnerable:**
```python
import ldap

def find_user(username):
    filter = f"(uid={username})"
    result = conn.search_s("dc=example,dc=com", ldap.SCOPE_SUBTREE, filter)
```

**Secure:**
```python
import ldap
import ldap.filter

def find_user(username):
    # Escape special LDAP characters
    safe_username = ldap.filter.escape_filter_chars(username)
    filter = f"(uid={safe_username})"
    result = conn.search_s("dc=example,dc=com", ldap.SCOPE_SUBTREE, filter)
```

**Why:**
- Escape LDAP special characters
- Use `ldap.filter.escape_filter_chars()`
- CWE-90

---

### XML-INJECT: Prevent XML/XXE Injection

**Risk:** XML External Entity attacks, denial of service.

**Vulnerable:**
```python
import xml.etree.ElementTree as ET

def parse_xml(xml_string):
    return ET.fromstring(xml_string)
```

**Secure:**
```python
import defusedxml.ElementTree as ET

def parse_xml(xml_string):
    return ET.fromstring(xml_string)
```

**Why:**
- Use `defusedxml` library
- Disable DTD processing
- Disable external entity resolution
- CWE-611, OWASP A4

---

## 2. Authentication & Authorization

### HASH-PASSWORD: Use Proper Password Hashing

**Risk:** Password compromise from database breaches.

**Vulnerable:**
```python
import hashlib

def store_password(password):
    hashed = hashlib.md5(password.encode()).hexdigest()
    db.save(hashed)
```

**Secure:**
```python
import bcrypt

def store_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    db.save(hashed)

def verify_password(password, stored_hash):
    return bcrypt.checkpw(password.encode(), stored_hash)
```

**Why:**
- Use bcrypt, scrypt, or argon2
- Built-in salt and work factor
- Resistant to brute force
- CWE-916, OWASP A2

---

### WEAK-HASH: Avoid Weak Hash Algorithms

**Risk:** Hash collision, rainbow table attacks.

**Vulnerable:**
```python
import hashlib

def hash_data(data):
    return hashlib.md5(data).hexdigest()  # Weak!
```

**Secure:**
```python
import hashlib

def hash_data(data):
    return hashlib.sha256(data).hexdigest()
```

**Why:**
- Avoid MD5, SHA1 for security purposes
- Use SHA-256, SHA-3, BLAKE2
- CWE-327

---

### SESSION-SECURE: Secure Session Management

**Risk:** Session hijacking, fixation attacks.

**Vulnerable:**
```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "secret"  # Weak secret!

@app.route('/login')
def login():
    session['user'] = request.form['username']
```

**Secure:**
```python
from flask import Flask, session
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']  # Strong random secret
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/login')
def login():
    # Regenerate session ID on login
    session.clear()
    session.permanent = False
    session['user'] = request.form['username']
```

**Why:**
- Use strong random session keys
- Set secure cookie flags
- Regenerate session ID on privilege change
- OWASP A2

---

### AUTHZ-CHECK: Always Check Authorization

**Risk:** Unauthorized access to resources.

**Vulnerable:**
```python
@app.route('/user/<user_id>/profile')
def get_profile(user_id):
    # Missing authorization check!
    return db.get_user(user_id)
```

**Secure:**
```python
@app.route('/user/<user_id>/profile')
def get_profile(user_id):
    current_user = get_current_user()

    # Check authorization
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)

    return db.get_user(user_id)
```

**Why:**
- Check authorization on every request
- Don't rely on client-side checks
- Implement role-based access control (RBAC)
- OWASP A1, CWE-862

---

### MFA-SUPPORT: Multi-Factor Authentication

**Risk:** Account takeover from password compromise.

**Vulnerable:**
```python
def login(username, password):
    if verify_password(username, password):
        create_session(username)
```

**Secure:**
```python
import pyotp

def login(username, password, totp_code):
    if not verify_password(username, password):
        return False

    # Verify TOTP code
    user = get_user(username)
    totp = pyotp.TOTP(user.totp_secret)
    if not totp.verify(totp_code):
        return False

    create_session(username)
```

**Why:**
- Support MFA/2FA (TOTP, SMS, hardware keys)
- Use libraries like `pyotp` or `python-fido2`
- OWASP A2

---

### TOKEN-EXPIRE: Token Expiration

**Risk:** Long-lived tokens enable prolonged attacks.

**Vulnerable:**
```python
def create_token(user_id):
    return jwt.encode({'user_id': user_id}, SECRET_KEY)
```

**Secure:**
```python
import jwt
import datetime

def create_token(user_id):
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode({
        'user_id': user_id,
        'exp': exp
    }, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
```

**Why:**
- Set expiration on tokens
- Use short-lived access tokens
- Implement refresh tokens
- CWE-613

---

### TIMING-ATTACK: Prevent Timing Attacks

**Risk:** Information leak through timing differences.

**Vulnerable:**
```python
def verify_token(provided, expected):
    return provided == expected  # Timing attack!
```

**Secure:**
```python
import hmac

def verify_token(provided, expected):
    return hmac.compare_digest(provided, expected)
```

**Why:**
- Use `hmac.compare_digest()` for secrets
- Constant-time comparison
- Prevents timing side-channel attacks
- CWE-208

---

## 3. Cryptography

### USE-CRYPTO-LIB: Use Established Crypto Libraries

**Risk:** Broken homemade cryptography.

**Vulnerable:**
```python
def encrypt(data, key):
    # Custom XOR encryption - WEAK!
    return bytes([b ^ key for b in data])
```

**Secure:**
```python
from cryptography.fernet import Fernet

def encrypt(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def decrypt(encrypted, key):
    f = Fernet(key)
    return f.decrypt(encrypted)
```

**Why:**
- Use `cryptography` library
- Don't implement your own crypto
- Use high-level APIs (Fernet, Hazmat)
- CWE-327

---

### RANDOM-SECURE: Use Cryptographically Secure Random

**Risk:** Predictable "random" values.

**Vulnerable:**
```python
import random

def generate_token():
    return ''.join(random.choices('0123456789abcdef', k=32))
```

**Secure:**
```python
import secrets

def generate_token():
    return secrets.token_hex(32)
```

**Why:**
- Use `secrets` module for security
- Never use `random` for security purposes
- CWE-330

---

### ENCRYPT-REST: Encrypt Data at Rest

**Risk:** Data exposure from storage compromise.

**Vulnerable:**
```python
def save_credit_card(card_number):
    db.save({'card': card_number})  # Plaintext!
```

**Secure:**
```python
from cryptography.fernet import Fernet

ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY'].encode()

def save_credit_card(card_number):
    f = Fernet(ENCRYPTION_KEY)
    encrypted = f.encrypt(card_number.encode())
    db.save({'card': encrypted})

def get_credit_card(user_id):
    f = Fernet(ENCRYPTION_KEY)
    encrypted = db.get(user_id)['card']
    return f.decrypt(encrypted).decode()
```

**Why:**
- Encrypt sensitive data at rest
- PCI DSS, GDPR requirement
- CWE-311

---

### ENCRYPT-TRANSIT: Encrypt Data in Transit

**Risk:** Man-in-the-middle attacks.

**Vulnerable:**
```python
import requests

response = requests.get('http://api.example.com/data')
```

**Secure:**
```python
import requests

response = requests.get('https://api.example.com/data', verify=True)
```

**Why:**
- Use HTTPS/TLS for all communications
- Verify SSL certificates
- CWE-319

---

### KEY-MANAGE: Proper Key Management

**Risk:** Key compromise.

**Vulnerable:**
```python
ENCRYPTION_KEY = b'my-secret-key-123'  # Hardcoded!
```

**Secure:**
```python
import os
from cryptography.fernet import Fernet

# Key from environment or key management service
ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY'].encode()

# Or use AWS KMS, Azure Key Vault, etc.
def get_encryption_key():
    # Fetch from key management service
    return kms_client.get_key('my-app-key')
```

**Why:**
- Never hardcode keys
- Use key management services (KMS)
- Rotate keys regularly
- CWE-320

---

### AVOID-ECB: Avoid ECB Mode

**Risk:** Pattern leakage in encrypted data.

**Vulnerable:**
```python
from Crypto.Cipher import AES

cipher = AES.new(key, AES.MODE_ECB)  # Weak mode!
```

**Secure:**
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
```

**Why:**
- Never use ECB mode
- Use GCM, CBC with authentication
- CWE-327

---

### SALT-HASH: Salt All Hashes

**Risk:** Rainbow table attacks.

**Vulnerable:**
```python
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

**Secure:**
```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
```

**Why:**
- Always use salts
- Unique salt per password
- bcrypt/scrypt handle this automatically
- CWE-759

---


> *20 of the most relevant guidelines shown. Remaining guidelines omitted.*
