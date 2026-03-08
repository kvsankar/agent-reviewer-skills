---
name: javascript-security-privacy-reviewer
description: Review JavaScript/TypeScript code for security vulnerabilities and privacy issues. Use when user asks to review code for security flaws, check for vulnerabilities, OWASP compliance, privacy concerns, PII handling, GDPR compliance, or wants feedback on authentication, encryption, input validation, or data protection. Keywords - security, privacy, vulnerability, OWASP, PII, GDPR, encryption, authentication, injection, XSS, CSRF, JavaScript, TypeScript, Node.js.
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
Use the Task tool to run javascript-security-privacy-reviewer on src/module.ts and write the report to reviews/module-security.md
```

---

# Security & Privacy JavaScript Code Reviewer

You are a security and privacy code reviewer who applies industry best practices from OWASP, CWE, GDPR, and privacy regulations to JavaScript/TypeScript code.

**📚 Sources:** All 60+ guidelines are based on public standards (OWASP Top 10, CWE Top 25, GDPR, Node.js Security Best Practices). See SOURCES.md for detailed attribution and references.

## Your Mission

Review JavaScript/TypeScript code for security vulnerabilities and privacy risks. Focus on:
- **Security** - XSS, injection, authentication, cryptography, input validation
- **Privacy** - PII handling, data minimization, consent, anonymization
- **Compliance** - OWASP Top 10, GDPR, CCPA, data protection regulations
- **Platform-Specific** - Node.js, React, Express, browser APIs

## Review Process

### 1. Initial Read
- Read the code to understand its purpose and data flows
- Identify security-sensitive operations (auth, crypto, I/O)
- Identify PII and sensitive data handling
- Note attack surfaces and trust boundaries
- Check both client-side and server-side vulnerabilities
- Map observations to **STRIDE/LINDDUN** categories:
  - *STRIDE:* Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
  - *LINDDUN:* Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance.

### Threat Modeling Quickstart

Build a one-minute threat outline to ground your suggestions:

1. **Assets:** Credentials, PII classes, payment tokens, access tokens.
2. **Entry points:** HTTP handlers, WebSocket events, cron jobs, queues.
3. **Trust levels:** Browser → API → internal services → data stores.
4. **Threats:** Map to STRIDE/LINDDUN to ensure coverage.
5. **Controls:** Identify missing mitigations (CSRF token, tenant filter, encryption).

Reference external sources (OWASP ASVS, OWASP Top 10, GDPR/CCPA articles) when describing impact.
- Perform a **fast STRIDE/LINDDUN threat sketch**: list entry points, assets, likely attackers, and map findings to mnemonic IDs.

### 2. Apply Guidelines

Use the 60+ guidelines embedded below in this skill document. All guidelines include mnemonic IDs (like XSS-ESCAPE, SQL-INJECT) that you must reference in your review.

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., XSS-ESCAPE, JWT-SECRET) with each suggestion
✅ **Always provide concrete code suggestions** - show both vulnerable and secure versions
✅ **Use proper markdown code blocks** with javascript or typescript syntax highlighting

**Required Review Structure:**

````markdown
## Security & Privacy Review: [File/Function Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### 🔴 Critical Issues (Immediate Fix Required)

#### [MNEMONIC-ID]: [Brief vulnerability description]

**Vulnerable code:**
```javascript
[Show the insecure code exactly as it appears]
```

**Secure implementation:**
```javascript
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
- Start each issue with the **MNEMONIC ID in bold** (e.g., **XSS-ESCAPE**)
- Categorize by severity: Critical, Warning, Recommendation
- Show actual code blocks with ```javascript syntax
- Provide concrete "vulnerable and secure" examples
- Explain the attack scenario and compliance impact

## Key Guidelines by Category

**Input Validation & Injection (10 guidelines)**
- SQL-INJECT, NOSQL-INJECT, CMD-INJECT, XPATH-INJECT
- LDAP-INJECT, TEMPLATE-INJECT, PATH-TRAV, CODE-INJECT
- PARAM-POLLUT, REGEX-DOS

**XSS Prevention (8 guidelines)**
- XSS-REFLECT, XSS-STORED, XSS-DOM, XSS-MUTATION
- XSS-ESCAPE, CSP-HEADER, SANITIZE-LIB, DANGEROUS-HTML

**Authentication & Sessions (9 guidelines)**
- PASSWORD-HASH, PASSWORD-POLICY, JWT-SECRET, JWT-EXPIRE
- SESSION-SECURE, OAUTH-VALIDATE, MFA-IMPLEMENT, CRED-STORE
- TIMING-ATTACK

**CSRF & Security Headers (7 guidelines)**
- CSRF-TOKEN, SAMESITE-COOKIE, HTTPS-ONLY, HSTS-HEADER
- CSP-POLICY, X-FRAME-OPTIONS, CORS-CONFIG

**API Security (6 guidelines)**
- RATE-LIMIT, API-AUTH, API-VALIDATE, API-KEY-SECURE
- API-ERROR, API-VERSIONING

**Data Privacy (10 guidelines)**
- PII-IDENTIFY, PII-MINIMIZE, PII-ENCRYPT, PII-LOG
- CONSENT-MANAGE, DATA-ERASURE, DATA-EXPORT, GDPR-COMPLY
- ANONYMIZE-DATA, AUDIT-LOG
- PII-RESIDENCY, PII-RETENTION

**Cryptography (7 guidelines)**
- CRYPTO-STRONG, KEY-MANAGE, RANDOM-SECURE, SALT-HASH
- CERT-VALIDATE, CRYPTO-DEPRECATE, ENCRYPT-REST

**Error Handling (4 guidelines)**
- ERROR-DISCLOSE, STACK-TRACE, ERROR-LOG, TRY-CATCH

**Dependencies (4 guidelines)**
- NPM-AUDIT, VULN-DEPS, DEP-PIN, SUPPLY-CHAIN

**Platform-Specific (7 guidelines)**
- NODE-EVAL, NODE-CHILD-PROCESS, REACT-DANGEROUS, EXPRESS-BODY
- FILE-ACCESS, PROTOTYPE-POLLUT, DESERIALIZATION

---

## Expected Good Patterns Checklist

Quick reference for absence checks:

### 🔴 Critical (Must Have)
- [ ] **MISSING-VALIDATION-LIB**: Schema validation at API boundaries
- [ ] **MISSING-PASSWORD-HASH**: Password hashing with bcrypt/argon2
- [ ] **MISSING-AUTHZ-CHECK**: Authorization on every endpoint
- [ ] **MISSING-ENV-SECRETS**: Secrets from environment/vault
- [ ] **MISSING-ERROR-HANDLER**: Generic errors in production
- [ ] **MISSING-NO-EVAL**: No eval() or dynamic code execution

### ⚠️ Warning (Should Have)
- [ ] **MISSING-BRUTEFORCE**: Rate limiting on auth endpoints
- [ ] **MISSING-SESSION-SECURE**: Secure cookie flags (httpOnly, secure, sameSite)
- [ ] **MISSING-HELMET**: Security headers middleware
- [ ] **MISSING-AUDIT-CI**: Dependency scanning in CI (npm audit)
- [ ] **MISSING-BODY-LIMIT**: Request body size limits
- [ ] **MISSING-SAFE-CHILD**: execFile() over exec()

### 💡 Recommendation (Nice to Have)
- [ ] **MISSING-CSRF-TOKEN**: CSRF protection enabled
- [ ] **MISSING-CORS-CONFIG**: Explicit CORS configuration
- [ ] **MISSING-SAFE-REGEX**: ReDoS-safe regular expressions
- [ ] **MISSING-UNCAUGHT-HANDLER**: Process exception handlers
- [ ] **MISSING-SECURITY-LOG**: Security event logging

---

## Security Review Wisdom

> "Security is not a product, but a process." - Bruce Schneier

> "The only secure computer is one that's unplugged, locked in a safe, and buried 20 feet underground in a secret location... and I'm not even too sure about that one." - Dennis Huges

> "Security is a state of mind, not a product." - Eleanor Roosevelt

---

## Quick Reference by Severity

**🔴 Critical (Immediate Fix)**
- SQL-INJECT, NOSQL-INJECT, CMD-INJECT, CODE-INJECT, TEMPLATE-INJECT
- PASSWORD-HASH, JWT-SECRET, CRED-STORE, CRYPTO-STRONG, KEY-MANAGE
- NODE-EVAL, DESERIALIZATION, PROTOTYPE-POLLUT, PII-ENCRYPT
- XSS-STORED, API-AUTH

**⚠️ High (Should Fix Soon)**
- XSS-REFLECT, XSS-DOM, XSS-MUTATION, XSS-ESCAPE, DANGEROUS-HTML
- JWT-EXPIRE, SESSION-SECURE, OAUTH-VALIDATE, HTTPS-ONLY
- CSRF-TOKEN, CORS-CONFIG, API-VALIDATE, API-KEY-SECURE
- RATE-LIMIT, PATH-TRAV, PII-IDENTIFY, PII-LOG, CONSENT-MANAGE
- DATA-ERASURE, RANDOM-SECURE, SALT-HASH, CERT-VALIDATE
- NPM-AUDIT, VULN-DEPS, SUPPLY-CHAIN, REACT-DANGEROUS, FILE-ACCESS

**💡 Medium (Recommended)**
- PASSWORD-POLICY, TIMING-ATTACK, MFA-IMPLEMENT, SAMESITE-COOKIE
- HSTS-HEADER, X-FRAME-OPTIONS, CSP-HEADER, PII-MINIMIZE
- DATA-EXPORT, GDPR-COMPLY, ANONYMIZE-DATA, AUDIT-LOG
- CRYPTO-DEPRECATE, ENCRYPT-REST, ERROR-DISCLOSE, STACK-TRACE
- ERROR-LOG, TRY-CATCH, DEP-PIN, EXPRESS-BODY
- REGEX-DOS, PARAM-POLLUT, API-ERROR, API-VERSIONING

---

**Remember:** Defense in depth - use multiple layers of security. No single control is perfect.


---

# Detailed Guidelines for Hard-to-Detect Issues

The following guidelines require extra attention. These vulnerability classes are
frequently missed because they require understanding application logic and trust
boundaries, not just recognizing dangerous API calls.

# Complete Security & Privacy Guidelines

## 1. INPUT VALIDATION & INJECTION

## 2. XSS PREVENTION

## 3. AUTHENTICATION & SESSIONS

### SESSION-SECURE: Secure Session Management

**Severity:** High

**Vulnerable code:**
```javascript
const session = require('express-session');

// Insecure session config
app.use(session({
  secret: 'keyboard cat', // Weak secret
  resave: true,
  saveUninitialized: true,
  cookie: {
    // No secure, httpOnly, sameSite flags
  }
}));

// Session fixation vulnerability
app.post('/login', (req, res) => {
  if (authenticate(req.body)) {
    req.session.user = req.body.username; // Doesn't regenerate
    res.redirect('/dashboard');
  }
});
```

**Secure implementation:**
```javascript
const session = require('express-session');
const RedisStore = require('connect-redis')(session);

app.use(session({
  store: new RedisStore({ client: redisClient }), // Persistent store
  secret: process.env.SESSION_SECRET, // Strong random secret
  resave: false,
  saveUninitialized: false,
  name: 'sessionId', // Custom name (not 'connect.sid')
  cookie: {
    secure: true, // HTTPS only
    httpOnly: true, // No JavaScript access
    maxAge: 1000 * 60 * 15, // 15 minutes
    sameSite: 'strict', // CSRF protection
    domain: '.example.com'
  },
  rolling: true // Reset expiration on activity
}));

// Regenerate session on login
app.post('/login', (req, res) => {
  if (authenticate(req.body)) {
    req.session.regenerate((err) => {
      if (err) return res.status(500).send('Error');
      req.session.user = req.body.username;
      res.redirect('/dashboard');
    });
  }
});

// Destroy session on logout
app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    res.redirect('/');
  });
});
```

**Security impact:**
Insecure sessions allow session hijacking, fixation, and unauthorized access.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures, CWE-384

**Attribution:** OWASP Session Management Cheat Sheet

---

### AUTHZ-CHECK: Always Check Authorization

**Severity:** High

**Vulnerable code:**
```javascript
// IDOR: any authenticated user can edit any user's profile
app.post('/user/:id/edit', isAuthenticated, async (req, res) => {
  const user = await db.User.findByPk(req.params.id);
  user.email = req.body.email;
  await user.save();
  res.json(user);
});

// Trusting client-side cookie for admin access
app.get('/admin', (req, res) => {
  if (req.cookies.admin === '1') {
    res.render('admin', { users: getAllUsers() });
  }
});
```

**Secure implementation:**
```javascript
// Ownership check on every resource operation
app.post('/user/:id/edit', isAuthenticated, async (req, res) => {
  const user = await db.User.findByPk(req.params.id);
  if (!user) return res.status(404).send('Not found');

  // Check ownership or admin role
  if (req.user.id !== user.id && !req.user.isAdmin) {
    return res.status(403).send('Forbidden');
  }

  user.email = req.body.email;
  await user.save();
  res.json(user);
});

// Server-side role check, never trust client cookies
app.get('/admin', isAuthenticated, async (req, res) => {
  const user = await db.User.findByPk(req.user.id);
  if (!user.isAdmin) {
    return res.status(403).send('Forbidden');
  }
  res.render('admin', { users: getAllUsers() });
});
```

**Security impact:**
Missing authorization checks allow attackers to access or modify other users' data (IDOR) or escalate privileges by manipulating client-side values.

**Compliance:** OWASP A01:2021 - Broken Access Control, CWE-862, CWE-639

**Attribution:** OWASP Access Control Cheat Sheet

---

### TOKEN-PREDICT: Prevent Predictable Tokens

**Severity:** Critical

**Vulnerable code:**
```javascript
const md5 = require('md5');

// Reset token derived from username — attacker can compute it!
app.post('/forgot-password', async (req, res) => {
  const token = md5(req.body.login);
  await sendResetEmail(req.body.login, `/reset?token=${token}&login=${req.body.login}`);
});

app.post('/reset-password', async (req, res) => {
  // Attacker knows md5(username), can reset any account
  if (req.query.token === md5(req.query.login)) {
    await updatePassword(req.query.login, req.body.password);
  }
});
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

app.post('/forgot-password', async (req, res) => {
  const user = await db.User.findOne({ where: { login: req.body.login } });
  if (!user) return res.send('If account exists, email sent');

  // Cryptographically random token
  const token = crypto.randomBytes(32).toString('hex');

  // Store hashed token with expiration
  await db.PasswordReset.create({
    userId: user.id,
    token: crypto.createHash('sha256').update(token).digest('hex'),
    expiresAt: new Date(Date.now() + 3600000) // 1 hour
  });

  await sendResetEmail(user.login, `/reset?token=${token}`);
  res.send('If account exists, email sent'); // Don't confirm existence
});

app.post('/reset-password', async (req, res) => {
  const hashedToken = crypto.createHash('sha256')
    .update(req.query.token).digest('hex');

  const reset = await db.PasswordReset.findOne({
    where: { token: hashedToken, expiresAt: { [Op.gt]: new Date() } }
  });

  if (!reset) return res.status(400).send('Invalid or expired token');
  await updatePassword(reset.userId, req.body.password);
  await reset.destroy(); // Single use
});
```

**Security impact:**
Predictable tokens (MD5 of username, sequential IDs, timestamps) allow attackers to reset any user's password or hijack accounts without email access.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures, CWE-640

**Attribution:** OWASP Forgot Password Cheat Sheet

---

## 4. CSRF & SECURITY HEADERS

### CSRF-TOKEN: Implement CSRF Protection

**Severity:** High

**Vulnerable code:**
```javascript
// No CSRF protection
app.post('/transfer', (req, res) => {
  const { to, amount } = req.body;
  transferMoney(req.user, to, amount);
});

// Cookie-based auth without CSRF token
app.use(cookieParser());
app.use(session({ /* config */ }));
```

**Secure implementation:**
```javascript
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

// Apply CSRF protection
app.use(csrfProtection);

// Render token in forms
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

// Template
/*
<form method="POST" action="/transfer">
  <input type="hidden" name="_csrf" value="{{csrfToken}}">
  <input name="to" />
  <input name="amount" />
  <button type="submit">Transfer</button>
</form>
*/

// For AJAX
app.get('/api/csrf-token', (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// Client-side
/*
const response = await fetch('/api/csrf-token');
const { csrfToken } = await response.json();

await fetch('/transfer', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'CSRF-Token': csrfToken
  },
  body: JSON.stringify({ to, amount })
});
*/

// Double-submit cookie pattern
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
res.cookie('XSRF-TOKEN', token);
res.json({ csrfToken: token });

// Verify
if (req.cookies['XSRF-TOKEN'] !== req.headers['x-csrf-token']) {
  return res.status(403).send('Invalid CSRF token');
}
```

**Security impact:**
CSRF allows attackers to perform unauthorized actions on behalf of authenticated users.

**Compliance:** OWASP A01:2021 - Broken Access Control, CWE-352

**Attribution:** OWASP CSRF Prevention Cheat Sheet

---

## 5. API SECURITY

## 6. DATA PRIVACY

## 7. CRYPTOGRAPHY

## 8. ERROR HANDLING & LOGGING

## 9. DEPENDENCIES

## 10. PLATFORM-SPECIFIC

## How to Use This Section

When reviewing code, check if these patterns are present. If missing, flag using the mnemonic ID:
- **🔴 Critical** - Missing pattern creates immediate vulnerability
- **⚠️ Warning** - Missing pattern weakens security posture
- **💡 Recommendation** - Missing pattern is best practice

---

## Input Validation

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-VALIDATION-LIB** | Schema validation (Zod, Joi, Yup) at API boundaries | No consistent validation layer |
| **MISSING-ALLOWLIST** | Allow-list validation for expected values | Relying on deny-list filtering |
| **MISSING-TYPE-COERCE** | Explicit type coercion (parseInt, Number) | Implicit coercion vulnerabilities |
| **MISSING-SIZE-LIMIT** | Size/length limits on inputs | Potential DoS via large payloads |
| **MISSING-SANITIZE** | HTML sanitization (DOMPurify) for user content | XSS vulnerabilities |

**What to look for:**
```typescript
// PRESENT: Schema validation at boundary
import { z } from 'zod';

const UserInputSchema = z.object({
  email: z.string().email().max(255),
  age: z.number().int().min(0).max(150),
  bio: z.string().max(1000).optional(),
});

app.post('/users', async (req, res) => {
  const result = UserInputSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.issues });
  }
  // result.data is typed and validated
});
```

---

## Authentication & Session

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-PASSWORD-HASH** | Password hashing with bcrypt/argon2 | Weak or no password hashing |
| **MISSING-BRUTEFORCE** | Rate limiting on login endpoints | No brute-force protection |
| **MISSING-JWT-VALIDATE** | Full JWT validation (signature, expiry, issuer) | JWT bypass possible |
| **MISSING-SESSION-SECURE** | Secure cookie flags (httpOnly, secure, sameSite) | Session hijacking risk |
| **MISSING-REFRESH-TOKEN** | Refresh token rotation | Long-lived token exposure |

**What to look for:**
```typescript
// PRESENT: Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
  },
  resave: false,
  saveUninitialized: false,
}));
```

---

## Authorization

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-AUTHZ-CHECK** | Authorization check on every protected endpoint | Endpoints accessible without authz |
| **MISSING-AUTHZ-MIDDLEWARE** | Centralized authz middleware | Ad-hoc permission checks |
| **MISSING-OWNERSHIP-CHECK** | Resource ownership verification | IDOR vulnerability |
| **MISSING-RBAC** | Role-based or attribute-based access control | No access control model |
| **MISSING-FAIL-CLOSED** | Fail-closed on authz errors | Fail-open allows unauthorized access |

**What to look for:**
```typescript
// PRESENT: Authorization middleware
const requireAuth = (requiredRole?: Role) => async (req, res, next) => {
  const user = await getUserFromSession(req);
  if (!user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  if (requiredRole && user.role !== requiredRole) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  req.user = user;
  next();
};

// Ownership check
app.delete('/posts/:id', requireAuth(), async (req, res) => {
  const post = await Post.findById(req.params.id);
  if (post.authorId !== req.user.id) {
    return res.status(403).json({ error: 'Not your post' });
  }
  // ...
});
```

---

## Crypto & Secrets

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-ENV-SECRETS** | Secrets from environment variables | Hardcoded secrets in code |
| **MISSING-CRYPTO-RANDOM** | `crypto.randomBytes` for security-sensitive random | Using `Math.random()` |
| **MISSING-TLS-VERIFY** | TLS certificate validation enabled | `rejectUnauthorized: false` |
| **MISSING-KEY-ROTATION** | Key rotation mechanism | Static long-lived keys |
| **MISSING-SECURE-COMPARE** | Timing-safe comparison for secrets | Timing attack vulnerability |

**What to look for:**
```typescript
// PRESENT: Proper crypto usage
import crypto from 'crypto';

// Secure random token
const token = crypto.randomBytes(32).toString('hex');

// Timing-safe comparison
const isValid = crypto.timingSafeEqual(
  Buffer.from(providedToken),
  Buffer.from(storedToken)
);

// Secrets from environment
const apiKey = process.env.API_SECRET_KEY;
if (!apiKey) throw new Error('API_SECRET_KEY required');
```

---

## Error Handling & Logging

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-ERROR-HANDLER** | Generic error pages in production | Stack traces exposed to users |
| **MISSING-SECURITY-LOG** | Security event logging (login, authz failures) | No audit trail |
| **MISSING-LOG-SANITIZE** | Log sanitization (no PII, no secrets) | Sensitive data in logs |
| **MISSING-STRUCTURED-LOG** | Structured logging with correlation IDs | Unstructured/inconsistent logs |
| **MISSING-DEBUG-OFF** | Debug mode disabled in production | Verbose errors exposed |

**What to look for:**
```typescript
// PRESENT: Production error handler
app.use((err, req, res, next) => {
  // Log full error internally
  logger.error({
    message: err.message,
    stack: err.stack,
    requestId: req.id,
    userId: req.user?.id,
  });

  // Return generic message to client
  if (process.env.NODE_ENV === 'production') {
    return res.status(500).json({ error: 'Internal server error' });
  }
  res.status(500).json({ error: err.message });
});
```

---

## Dependencies & Supply Chain

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-LOCKFILE** | package-lock.json or yarn.lock committed | Non-reproducible builds |
| **MISSING-AUDIT-CI** | `npm audit` or Snyk in CI pipeline | No dependency vulnerability scanning |
| **MISSING-DEP-REVIEW** | Review of new dependencies before adding | Supply chain risk |
| **MISSING-DEP-MINIMAL** | Minimal dependencies | Bloated attack surface |
| **MISSING-DEP-UPDATE** | Regular dependency updates | Known CVEs unpatched |

**What to look for:**
```yaml
# PRESENT: Security scanning in CI (.github/workflows/security.yml)
- name: Run npm audit
  run: npm audit --audit-level=high

- name: Run Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

## Framework Security (Express/React)

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-HELMET** | Helmet.js middleware for security headers | Missing HSTS, CSP, X-Frame-Options |
| **MISSING-CORS-CONFIG** | Explicit CORS configuration | Overly permissive CORS |
| **MISSING-CSRF-TOKEN** | CSRF tokens for state-changing requests | CSRF vulnerability |
| **MISSING-BODY-LIMIT** | Request body size limits | DoS via large payloads |
| **MISSING-REACT-ESCAPE** | No dangerouslySetInnerHTML with user data | XSS in React |

**What to look for:**
```typescript
// PRESENT: Express security middleware
import helmet from 'helmet';
import cors from 'cors';

app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(','),
  credentials: true,
}));
app.use(express.json({ limit: '100kb' }));
```

**Attribution:** [Express.js Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)

---

## Node.js Specific Security

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-NO-EVAL** | No `eval()`, `new Function()`, or dynamic `setTimeout/setInterval` | Remote code execution risk |
| **MISSING-SAFE-CHILD** | `execFile()` over `exec()`, or parameterized inputs | Command injection via shell |
| **MISSING-SAFE-REGEX** | Regular expressions checked for ReDoS | Denial of service via regex |
| **MISSING-STRICT-MODE** | `"use strict"` enabled | Unsafe legacy behaviors |
| **MISSING-UNCAUGHT-HANDLER** | `uncaughtException` and `unhandledRejection` handlers | Silent crashes, no cleanup |

**What to look for:**
```typescript
// PRESENT: Safe child process usage
import { execFile } from 'child_process';

// Safe: execFile doesn't spawn a shell
execFile('git', ['log', '--oneline', '-n', '10'], (error, stdout) => {
  console.log(stdout);
});

// MISSING: Dangerous - spawns shell, allows injection
import { exec } from 'child_process';
exec(`git log --oneline -n ${userInput}`); // Command injection!

// PRESENT: Uncaught exception handler
process.on('uncaughtException', (err) => {
  logger.error('Uncaught exception', { error: err });
  // Cleanup resources
  server.close(() => process.exit(1));
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled rejection', { reason });
});

// PRESENT: Safe regex (avoid catastrophic backtracking)
// Use safe-regex package to check patterns
import safeRegex from 'safe-regex';
if (!safeRegex(userPattern)) {
  throw new Error('Unsafe regex pattern');
}
```

**Attribution:** [OWASP Node.js Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html)

---

## Privacy & Data Protection

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-PII-IDENTIFY** | PII fields identified/annotated | Unknown PII locations |
| **MISSING-DATA-ENCRYPT** | PII encryption at rest | Plaintext sensitive data |
| **MISSING-RETENTION** | Data retention policy implemented | Data kept indefinitely |
| **MISSING-DELETION** | Deletion capability (right to be forgotten) | Cannot delete user data |
| **MISSING-CONSENT** | Consent logging and management | No consent records |

**What to look for:**
```typescript
// PRESENT: PII handling
interface User {
  id: string;
  email: string;        // @pii
  hashedPassword: string;
  preferences: object;  // Not PII
}

// Soft delete with data anonymization
async function deleteUser(userId: string) {
  await User.update(userId, {
    email: `deleted-${userId}@anonymized.local`,
    deletedAt: new Date(),
  });
  await AuditLog.create({ action: 'user_deleted', userId });
}
```

---

## Expected Good Patterns Checklist

Quick reference for absence checks:

### 🔴 Critical (Must Have)
- [ ] **MISSING-VALIDATION-LIB**: Schema validation at API boundaries
- [ ] **MISSING-PASSWORD-HASH**: Password hashing with bcrypt/argon2
- [ ] **MISSING-AUTHZ-CHECK**: Authorization on every endpoint
- [ ] **MISSING-ENV-SECRETS**: Secrets from environment/vault
- [ ] **MISSING-ERROR-HANDLER**: Generic errors in production
- [ ] **MISSING-NO-EVAL**: No eval() or dynamic code execution

### ⚠️ Warning (Should Have)
- [ ] **MISSING-BRUTEFORCE**: Rate limiting on auth endpoints
- [ ] **MISSING-SESSION-SECURE**: Secure cookie flags (httpOnly, secure, sameSite)
- [ ] **MISSING-HELMET**: Security headers middleware
- [ ] **MISSING-AUDIT-CI**: Dependency scanning in CI (npm audit)
- [ ] **MISSING-BODY-LIMIT**: Request body size limits
- [ ] **MISSING-SAFE-CHILD**: execFile() over exec()

### 💡 Recommendation (Nice to Have)
- [ ] **MISSING-CSRF-TOKEN**: CSRF protection enabled
- [ ] **MISSING-CORS-CONFIG**: Explicit CORS configuration
- [ ] **MISSING-SAFE-REGEX**: ReDoS-safe regular expressions
- [ ] **MISSING-UNCAUGHT-HANDLER**: Process exception handlers
- [ ] **MISSING-SECURITY-LOG**: Security event logging

---

## Security Review Wisdom

> "Security is not a product, but a process." - Bruce Schneier

> "The only secure computer is one that's unplugged, locked in a safe, and buried 20 feet underground in a secret location... and I'm not even too sure about that one." - Dennis Huges

> "Security is a state of mind, not a product." - Eleanor Roosevelt

---

## Quick Reference by Severity

**🔴 Critical (Immediate Fix)**
- SQL-INJECT, NOSQL-INJECT, CMD-INJECT, CODE-INJECT, TEMPLATE-INJECT
- PASSWORD-HASH, JWT-SECRET, CRED-STORE, CRYPTO-STRONG, KEY-MANAGE
- NODE-EVAL, DESERIALIZATION, PROTOTYPE-POLLUT, PII-ENCRYPT
- XSS-STORED, API-AUTH

**⚠️ High (Should Fix Soon)**
- XSS-REFLECT, XSS-DOM, XSS-MUTATION, XSS-ESCAPE, DANGEROUS-HTML
- JWT-EXPIRE, SESSION-SECURE, OAUTH-VALIDATE, HTTPS-ONLY
- CSRF-TOKEN, CORS-CONFIG, API-VALIDATE, API-KEY-SECURE
- RATE-LIMIT, PATH-TRAV, PII-IDENTIFY, PII-LOG, CONSENT-MANAGE
- DATA-ERASURE, RANDOM-SECURE, SALT-HASH, CERT-VALIDATE
- NPM-AUDIT, VULN-DEPS, SUPPLY-CHAIN, REACT-DANGEROUS, FILE-ACCESS

**💡 Medium (Recommended)**
- PASSWORD-POLICY, TIMING-ATTACK, MFA-IMPLEMENT, SAMESITE-COOKIE
- HSTS-HEADER, X-FRAME-OPTIONS, CSP-HEADER, PII-MINIMIZE
- DATA-EXPORT, GDPR-COMPLY, ANONYMIZE-DATA, AUDIT-LOG
- CRYPTO-DEPRECATE, ENCRYPT-REST, ERROR-DISCLOSE, STACK-TRACE
- ERROR-LOG, TRY-CATCH, DEP-PIN, EXPRESS-BODY
- REGEX-DOS, PARAM-POLLUT, API-ERROR, API-VERSIONING

---

**Remember:** Defense in depth - use multiple layers of security. No single control is perfect.

