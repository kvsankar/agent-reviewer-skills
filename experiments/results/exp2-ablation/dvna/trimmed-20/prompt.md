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

# Complete Security & Privacy Guidelines

## 1. INPUT VALIDATION & INJECTION

### SQL-INJECT: Prevent SQL Injection

**Severity:** Critical

**Vulnerable code:**
```javascript
// Direct string concatenation
const userId = req.query.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// Template literals
const username = req.body.username;
const sql = `SELECT * FROM users WHERE username = '${username}'`;
```

**Secure implementation:**
```javascript
// Use parameterized queries
const userId = req.query.id;
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// With prepared statements
const username = req.body.username;
const stmt = db.prepare('SELECT * FROM users WHERE username = ?');
stmt.get(username);

// ORM usage (e.g., Sequelize)
User.findOne({ where: { username: username } });
```

**Security impact:**
SQL injection allows attackers to execute arbitrary SQL, leading to data theft, modification, or deletion.

**Compliance:** OWASP A03:2021 - Injection, CWE-89

**Attribution:** OWASP, Node.js Security Best Practices

---

### NOSQL-INJECT: Prevent NoSQL Injection

**Severity:** Critical

**Vulnerable code:**
```javascript
// MongoDB - Direct object injection
const username = req.body.username;
const password = req.body.password;
User.findOne({ username: username, password: password });

// Attacker can send: { username: "admin", password: { $ne: null } }

// mongoose with direct object
const filter = JSON.parse(req.query.filter);
User.find(filter); // Dangerous!
```

**Secure implementation:**
```javascript
// Validate and sanitize input
const username = String(req.body.username);
const password = String(req.body.password);
User.findOne({ username, password });

// Use schema validation
const userSchema = new mongoose.Schema({
  username: { type: String, required: true },
  password: { type: String, required: true }
});

// Whitelist allowed fields
const allowedFields = ['username', 'email'];
const filter = {};
allowedFields.forEach(field => {
  if (req.query[field]) filter[field] = String(req.query[field]);
});
User.find(filter);
```

**Security impact:**
NoSQL injection can bypass authentication, access unauthorized data, or modify database content.

**Compliance:** OWASP A03:2021 - Injection, CWE-943

**Attribution:** OWASP, MongoDB Security Checklist

---

### CMD-INJECT: Prevent Command Injection

**Severity:** Critical

**Vulnerable code:**
```javascript
// exec with user input
const { exec } = require('child_process');
const filename = req.query.file;
exec(`cat ${filename}`, (error, stdout) => {
  res.send(stdout);
});

// shell: true is dangerous
const userInput = req.body.name;
spawn('echo', [userInput], { shell: true });
```

**Secure implementation:**
```javascript
// Avoid shell commands entirely
const fs = require('fs');
const path = require('path');
const filename = path.basename(req.query.file); // Sanitize
const safePath = path.join('/safe/directory', filename);
fs.readFile(safePath, 'utf8', (err, data) => {
  if (err) return res.status(404).send('Not found');
  res.send(data);
});

// If shell is necessary, use execFile with array
const { execFile } = require('child_process');
const args = ['-l', '/safe/directory'];
execFile('ls', args, (error, stdout) => {
  res.send(stdout);
});

// Whitelist allowed commands
const allowedCommands = ['list', 'count'];
if (!allowedCommands.includes(req.body.action)) {
  return res.status(400).send('Invalid action');
}
```

**Security impact:**
Command injection allows attackers to execute arbitrary system commands, leading to complete server compromise.

**Compliance:** OWASP A03:2021 - Injection, CWE-78

**Attribution:** OWASP, Node.js Security Best Practices

---

### XPATH-INJECT: Prevent XPath Injection

**Severity:** High

**Vulnerable code:**
```javascript
const xpath = require('xpath');
const username = req.query.username;
const query = `//users/user[username='${username}']`;
const nodes = xpath.select(query, xmlDoc);
```

**Secure implementation:**
```javascript
// Escape special characters
function escapeXPath(str) {
  return str.replace(/'/g, "&apos;").replace(/"/g, "&quot;");
}

const username = escapeXPath(req.query.username);
const query = `//users/user[username='${username}']`;
const nodes = xpath.select(query, xmlDoc);

// Better: Use parameterized XPath (library-dependent)
// Or switch to JSON/MongoDB instead of XML
```

**Security impact:**
XPath injection can bypass authentication or access unauthorized XML data.

**Compliance:** OWASP A03:2021 - Injection, CWE-643

**Attribution:** OWASP

---

### LDAP-INJECT: Prevent LDAP Injection

**Severity:** High

**Vulnerable code:**
```javascript
const ldap = require('ldapjs');
const username = req.body.username;
const filter = `(uid=${username})`;
client.search('ou=users,dc=example,dc=com', { filter }, callback);
```

**Secure implementation:**
```javascript
// Escape LDAP special characters
function escapeLDAP(str) {
  return str
    .replace(/\\/g, '\\5c')
    .replace(/\*/g, '\\2a')
    .replace(/\(/g, '\\28')
    .replace(/\)/g, '\\29')
    .replace(/\0/g, '\\00');
}

const username = escapeLDAP(req.body.username);
const filter = `(uid=${username})`;
client.search('ou=users,dc=example,dc=com', { filter }, callback);
```

**Security impact:**
LDAP injection can bypass authentication or access unauthorized directory information.

**Compliance:** OWASP A03:2021 - Injection, CWE-90

**Attribution:** OWASP

---

### TEMPLATE-INJECT: Prevent Template Injection

**Severity:** Critical

**Vulnerable code:**
```javascript
// Server-Side Template Injection (SSTI)
const ejs = require('ejs');
const template = req.body.template; // User-controlled
const html = ejs.render(template, { user: req.user });

// Handlebars with SafeString abuse
const Handlebars = require('handlebars');
const userInput = req.body.message;
return new Handlebars.SafeString(userInput); // Dangerous!
```

**Secure implementation:**
```javascript
// Don't allow user input as templates
const ejs = require('ejs');
const template = fs.readFileSync('templates/safe.ejs', 'utf8');
const html = ejs.render(template, { 
  message: req.body.message // Data only, not template
});

// Use auto-escaping
const Handlebars = require('handlebars');
Handlebars.registerHelper('escape', function(str) {
  return Handlebars.escapeExpression(str);
});

// Sanitize if SafeString is necessary
const sanitizeHtml = require('sanitize-html');
const clean = sanitizeHtml(userInput, {
  allowedTags: ['b', 'i', 'em', 'strong'],
  allowedAttributes: {}
});
return new Handlebars.SafeString(clean);
```

**Security impact:**
Template injection can lead to remote code execution on the server.

**Compliance:** OWASP A03:2021 - Injection, CWE-94

**Attribution:** OWASP, PortSwigger Research

---

### PATH-TRAV: Prevent Path Traversal

**Severity:** High

**Vulnerable code:**
```javascript
// Direct file access
const filename = req.query.file;
const filePath = './uploads/' + filename;
fs.readFile(filePath, callback);
// Attacker: ?file=../../../etc/passwd

// Express static with wrong config
app.use('/files', express.static('uploads'));
// Vulnerable to ../../../etc/passwd
```

**Secure implementation:**
```javascript
const path = require('path');

// Normalize and validate path
const filename = path.basename(req.query.file); // Removes directory
const uploadsDir = path.resolve('./uploads');
const filePath = path.join(uploadsDir, filename);

// Ensure file is within allowed directory
if (!filePath.startsWith(uploadsDir)) {
  return res.status(403).send('Access denied');
}

fs.readFile(filePath, callback);

// Whitelist allowed files
const allowedFiles = ['file1.txt', 'file2.pdf'];
if (!allowedFiles.includes(filename)) {
  return res.status(404).send('Not found');
}
```

**Security impact:**
Path traversal allows attackers to read arbitrary files, potentially including sensitive configuration or system files.

**Compliance:** OWASP A01:2021 - Broken Access Control, CWE-22

**Attribution:** OWASP

---

### CODE-INJECT: Prevent Code Injection

**Severity:** Critical

**Vulnerable code:**
```javascript
// eval() with user input
const userCode = req.body.code;
const result = eval(userCode); // Never do this!

// Function constructor
const userFunc = req.body.function;
const fn = new Function(userFunc);
fn();

// vm module misuse
const vm = require('vm');
const script = new vm.Script(req.body.script);
script.runInThisContext(); // Still dangerous
```

**Secure implementation:**
```javascript
// Don't execute user code on server
// If you must allow custom logic, use a sandboxed environment

// Option 1: Use JSON for data, not code
const config = JSON.parse(req.body.config); // Data only

// Option 2: Use a safe expression evaluator
const mathjs = require('mathjs');
const result = mathjs.evaluate(req.body.expression); // Math only

// Option 3: Use vm2 for proper sandboxing
const { VM } = require('vm2');
const vm = new VM({
  timeout: 1000,
  sandbox: { value: 42 }
});
const result = vm.run(req.body.code);

// Option 4: Whitelist allowed operations
const allowedOps = { add: (a, b) => a + b, multiply: (a, b) => a * b };
const op = req.body.operation;
if (!allowedOps[op]) return res.status(400).send('Invalid operation');
const result = allowedOps[op](req.body.a, req.body.b);
```

**Security impact:**
Code injection leads to remote code execution, complete server compromise.

**Compliance:** OWASP A03:2021 - Injection, CWE-94

**Attribution:** OWASP, Node.js Security Best Practices

---

### PARAM-POLLUT: Prevent Parameter Pollution

**Severity:** Medium

**Vulnerable code:**
```javascript
// Multiple parameters with same name
// GET /api/users?id=1&id=2
const userId = req.query.id; // Could be "1" or ["1", "2"]

// Inconsistent handling
if (userId === '1') { // Fails if userId is array
  // ...
}

// Business logic bypass
const isAdmin = req.query.admin;
if (isAdmin === 'true') { // Can be bypassed with ?admin=true&admin=false
  grantAdminAccess();
}
```

**Secure implementation:**
```javascript
// Always handle as array or single value explicitly
const userId = Array.isArray(req.query.id) 
  ? req.query.id[0] 
  : req.query.id;

// Validate type
if (typeof userId !== 'string') {
  return res.status(400).send('Invalid parameter');
}

// Use middleware to prevent pollution
const hpp = require('hpp');
app.use(hpp()); // HTTP Parameter Pollution protection

// For critical parameters, enforce single value
const isAdmin = req.query.admin;
if (Array.isArray(isAdmin)) {
  return res.status(400).send('Invalid request');
}
```

**Security impact:**
Parameter pollution can bypass security checks or cause unexpected behavior.

**Compliance:** CWE-235

**Attribution:** OWASP

---

### REGEX-DOS: Prevent Regular Expression Denial of Service

**Severity:** Medium

**Vulnerable code:**
```javascript
// Evil regex with catastrophic backtracking
const emailRegex = /^([a-zA-Z0-9]+)*@[a-zA-Z0-9]+\.[a-zA-Z]+$/;
const email = req.body.email;
if (emailRegex.test(email)) { // Can hang with: "aaaaaaaaaaaaaaaaaaaaaa!"
  // ...
}

// Another example
const regex = /(a+)+b/;
const input = 'aaaaaaaaaaaaaaaaaaaaac'; // Takes exponential time
regex.test(input);
```

**Secure implementation:**
```javascript
// Use simple, non-backtracking regex
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

// Set timeout for regex operations
const safeRegexTest = (regex, str, timeout = 100) => {
  return new Promise((resolve) => {
    const timer = setTimeout(() => resolve(false), timeout);
    const result = regex.test(str);
    clearTimeout(timer);
    resolve(result);
  });
};

// Use validator library
const validator = require('validator');
if (validator.isEmail(req.body.email)) {
  // ...
}

// Check regex safety
const safe = require('safe-regex');
const regex = /^([a-zA-Z0-9]+)*@/;
if (!safe(regex)) {
  throw new Error('Unsafe regex pattern');
}
```

**Security impact:**
ReDoS can cause CPU exhaustion, leading to denial of service.

**Compliance:** CWE-1333

**Attribution:** OWASP

---

## 2. XSS PREVENTION

### XSS-REFLECT: Prevent Reflected XSS

**Severity:** High

**Vulnerable code:**
```javascript
// Directly reflecting user input
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${query}</h1>`);
  // Attacker: ?q=<script>alert('XSS')</script>
});

// Template without escaping
res.send(`<div>Welcome ${req.query.name}!</div>`);
```

**Secure implementation:**
```javascript
// Use templating with auto-escaping
const Handlebars = require('handlebars');
const template = Handlebars.compile('<h1>Results for: {{query}}</h1>');
res.send(template({ query: req.query.q }));

// HTML escape manually
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

res.send(`<h1>Results for: ${escapeHtml(req.query.q)}</h1>`);

// Use React (auto-escapes by default)
function SearchResults({ query }) {
  return <h1>Results for: {query}</h1>;
}
```

**Security impact:**
Reflected XSS allows attackers to execute JavaScript in victim's browser, stealing cookies or performing actions as the user.

**Compliance:** OWASP A03:2021 - Injection, CWE-79

**Attribution:** OWASP

---

### XSS-STORED: Prevent Stored XSS

**Severity:** Critical

**Vulnerable code:**
```javascript
// Storing unsanitized user input
app.post('/comment', async (req, res) => {
  const comment = req.body.comment;
  await db.comments.insert({ text: comment }); // Stored as-is
});

// Displaying without escaping
app.get('/comments', async (req, res) => {
  const comments = await db.comments.find();
  const html = comments.map(c => `<p>${c.text}</p>`).join('');
  res.send(html); // XSS when displayed
});
```

**Secure implementation:**
```javascript
// Sanitize on input
const sanitizeHtml = require('sanitize-html');

app.post('/comment', async (req, res) => {
  const comment = sanitizeHtml(req.body.comment, {
    allowedTags: ['b', 'i', 'em', 'strong', 'a'],
    allowedAttributes: {
      'a': ['href']
    },
    allowedSchemes: ['http', 'https', 'mailto']
  });
  await db.comments.insert({ text: comment });
});

// Escape on output (defense in depth)
app.get('/comments', async (req, res) => {
  const comments = await db.comments.find();
  res.render('comments', { comments }); // Use template with auto-escape
});

// React example
function Comment({ text }) {
  return <p>{text}</p>; // Auto-escaped
}
```

**Security impact:**
Stored XSS is more dangerous than reflected XSS as it affects all users who view the malicious content.

**Compliance:** OWASP A03:2021 - Injection, CWE-79

**Attribution:** OWASP

---

### XSS-DOM: Prevent DOM-Based XSS

**Severity:** High

**Vulnerable code:**
```javascript
// innerHTML with user input
const name = new URLSearchParams(location.search).get('name');
document.getElementById('greeting').innerHTML = `Hello ${name}!`;

// document.write
document.write('<h1>' + location.hash.substring(1) + '</h1>');

// Unsafe jQuery
const userInput = location.hash.substring(1);
$('#content').html(userInput);
```

**Secure implementation:**
```javascript
// Use textContent instead of innerHTML
const name = new URLSearchParams(location.search).get('name');
document.getElementById('greeting').textContent = `Hello ${name}!`;

// Create elements safely
const heading = document.createElement('h1');
heading.textContent = location.hash.substring(1);
document.body.appendChild(heading);

// Use jQuery text() instead of html()
const userInput = location.hash.substring(1);
$('#content').text(userInput);

// React (auto-escapes)
function Greeting({ name }) {
  return <div>Hello {name}!</div>;
}
```

**Security impact:**
DOM-based XSS bypasses server-side protections and executes in the browser.

**Compliance:** OWASP A03:2021 - Injection, CWE-79

**Attribution:** OWASP

---

### XSS-MUTATION: Prevent Mutation XSS (mXSS)

**Severity:** High

**Vulnerable code:**
```javascript
// DOMPurify misuse
const dirty = '<svg><style><img src=x onerror=alert(1)></style></svg>';
const clean = DOMPurify.sanitize(dirty);
div.innerHTML = clean; // Can still execute in some browsers

// Sanitizing after DOM insertion
div.innerHTML = userInput;
DOMPurify.sanitize(div.innerHTML); // Too late!
```

**Secure implementation:**
```javascript
// Use DOMPurify correctly with SAFE_FOR_TEMPLATES
const dirty = userInput;
const clean = DOMPurify.sanitize(dirty, { SAFE_FOR_TEMPLATES: true });
div.innerHTML = clean;

// Or use textContent when possible
div.textContent = userInput;

// Sanitize BEFORE DOM insertion
const clean = DOMPurify.sanitize(userInput);
div.innerHTML = clean;

// Set correct RETURN_DOM or RETURN_DOM_FRAGMENT
const cleanElement = DOMPurify.sanitize(dirty, { 
  RETURN_DOM: true,
  RETURN_DOM_FRAGMENT: false
});
```

**Security impact:**
Mutation XSS can bypass sanitization libraries through browser quirks.

**Compliance:** CWE-79

**Attribution:** DOMPurify documentation, Cure53

---

### XSS-ESCAPE: Context-Aware Output Escaping

**Severity:** High

**Vulnerable code:**
```javascript
// HTML context - need HTML escaping
res.send(`<div>${userInput}</div>`); // Vulnerable

// JavaScript context - need JavaScript escaping  
res.send(`<script>var name = '${userInput}';</script>`); // Vulnerable

// URL context - need URL encoding
res.send(`<a href="/search?q=${userInput}">Search</a>`); // Vulnerable

// CSS context - need CSS escaping
res.send(`<div style="color: ${userColor}">Text</div>`); // Vulnerable
```

**Secure implementation:**
```javascript
// HTML context
function escapeHtml(str) {
  return str.replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;',
    '"': '&quot;', "'": '&#x27;'
  }[char]));
}
res.send(`<div>${escapeHtml(userInput)}</div>`);

// JavaScript context
function escapeJs(str) {
  return str.replace(/[\\'"]/g, '\\$&').replace(/\n/g, '\\n');
}
res.send(`<script>var name = '${escapeJs(userInput)}';</script>`);

// URL context
const encoded = encodeURIComponent(userInput);
res.send(`<a href="/search?q=${encoded}">Search</a>`);

// CSS context - whitelist approach
const allowedColors = ['red', 'blue', 'green'];
const safeColor = allowedColors.includes(userColor) ? userColor : 'black';
res.send(`<div style="color: ${safeColor}">Text</div>`);
```

**Security impact:**
Incorrect escaping for context allows XSS attacks.

**Compliance:** OWASP A03:2021 - Injection, CWE-79

**Attribution:** OWASP XSS Prevention Cheat Sheet

---

### CSP-HEADER: Implement Content Security Policy

**Severity:** Medium

**Vulnerable code:**
```javascript
// No CSP header
app.get('/', (req, res) => {
  res.send('<html>...</html>');
});

// Weak CSP
res.setHeader('Content-Security-Policy', "default-src *");

// unsafe-inline and unsafe-eval
res.setHeader('Content-Security-Policy', 
  "script-src 'unsafe-inline' 'unsafe-eval'");
```

**Secure implementation:**
```javascript
// Strong CSP with nonce
const crypto = require('crypto');
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", (req, res) => `'nonce-${res.locals.cspNonce}'`],
    styleSrc: ["'self'", "'unsafe-inline'"], // For inline styles
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],
    upgradeInsecureRequests: []
  }
}));

// Generate nonce per request
app.use((req, res, next) => {
  res.locals.cspNonce = crypto.randomBytes(16).toString('base64');
  next();
});

// Use nonce in script tags
res.send(`<script nonce="${res.locals.cspNonce}">...</script>`);

// Report violations
app.use(helmet.contentSecurityPolicy({
  directives: {
    // ... other directives
    reportUri: '/csp-violation-report'
  }
}));
```

**Security impact:**
CSP provides defense-in-depth against XSS attacks by restricting script sources.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** OWASP, MDN Web Docs

---

### SANITIZE-LIB: Use Sanitization Libraries

**Severity:** Medium

**Vulnerable code:**
```javascript
// Manual sanitization (incomplete)
function sanitize(str) {
  return str.replace(/<script>/g, '');
  // Bypassed by: <Script>, <script src=...>, <img onerror=...>
}

// Regex-based (fragile)
const cleaned = userInput.replace(/<[^>]*>/g, '');
```

**Secure implementation:**
```javascript
// Use DOMPurify for HTML
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');
const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const clean = DOMPurify.sanitize(userInput, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
  ALLOWED_ATTR: ['href']
});

// Or use sanitize-html
const sanitizeHtml = require('sanitize-html');
const clean = sanitizeHtml(userInput, {
  allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img']),
  allowedAttributes: {
    'a': ['href', 'name', 'target'],
    'img': ['src', 'alt']
  },
  allowedSchemes: ['http', 'https', 'mailto']
});

// For markdown
const marked = require('marked');
const DOMPurify = require('isomorphic-dompurify');
const html = marked.parse(userMarkdown);
const clean = DOMPurify.sanitize(html);
```

**Security impact:**
Proper sanitization libraries handle edge cases and bypass attempts.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** DOMPurify, sanitize-html documentation

---

### DANGEROUS-HTML: Avoid Dangerous HTML Patterns

**Severity:** High

**Vulnerable code:**
```javascript
// React dangerouslySetInnerHTML
function Comment({ htmlContent }) {
  return <div dangerouslySetInnerHTML={{ __html: htmlContent }} />;
}

// Vue v-html
<template>
  <div v-html="userContent"></div>
</template>

// Angular bypassSecurityTrustHtml
constructor(private sanitizer: DomSanitizer) {}
getTrustedHtml() {
  return this.sanitizer.bypassSecurityTrustHtml(this.userInput);
}
```

**Secure implementation:**
```javascript
// React - Sanitize before using dangerouslySetInnerHTML
import DOMPurify from 'isomorphic-dompurify';

function Comment({ htmlContent }) {
  const cleanHtml = DOMPurify.sanitize(htmlContent);
  return <div dangerouslySetInnerHTML={{ __html: cleanHtml }} />;
}

// Better: Avoid dangerouslySetInnerHTML, use markdown
import ReactMarkdown from 'react-markdown';

function Comment({ markdown }) {
  return <ReactMarkdown>{markdown}</ReactMarkdown>;
}

// Vue - Sanitize in computed property
<script>
import DOMPurify from 'isomorphic-dompurify';

export default {
  computed: {
    sanitizedContent() {
      return DOMPurify.sanitize(this.userContent);
    }
  }
}
</script>
<template>
  <div v-html="sanitizedContent"></div>
</template>

// Angular - Don't bypass, let Angular sanitize
<div [innerHTML]="userInput"></div> <!-- Angular sanitizes automatically -->
```

**Security impact:**
Bypassing framework security features introduces XSS vulnerabilities.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** React, Vue, Angular security documentation

---

## 3. AUTHENTICATION & SESSIONS

### PASSWORD-HASH: Use Strong Password Hashing

**Severity:** Critical

**Vulnerable code:**
```javascript
// Plain text passwords
const password = req.body.password;
await db.users.insert({ username, password }); // Never!

// Weak hashing (MD5, SHA1)
const crypto = require('crypto');
const hash = crypto.createHash('md5').update(password).digest('hex');

// SHA-256 without salt
const hash = crypto.createHash('sha256').update(password).digest('hex');
```

**Secure implementation:**
```javascript
// Use bcrypt
const bcrypt = require('bcrypt');
const saltRounds = 12;

// Hash password
const hash = await bcrypt.hash(password, saltRounds);
await db.users.insert({ username, passwordHash: hash });

// Verify password
const user = await db.users.findOne({ username });
const isValid = await bcrypt.compare(password, user.passwordHash);

// Or use argon2 (even better)
const argon2 = require('argon2');

// Hash password
const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 2 ** 16, // 64 MB
  timeCost: 3,
  parallelism: 1
});

// Verify password
const isValid = await argon2.verify(hash, password);
```

**Security impact:**
Weak password hashing allows attackers to crack passwords from database dumps.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures, CWE-327

**Attribution:** OWASP, NIST

---

### PASSWORD-POLICY: Enforce Strong Password Policy

**Severity:** Medium

**Vulnerable code:**
```javascript
// No password requirements
app.post('/register', (req, res) => {
  const password = req.body.password;
  // Accept any password, even "123"
});

// Only length check
if (password.length < 6) {
  return res.status(400).send('Password too short');
}
```

**Secure implementation:**
```javascript
// Comprehensive password validation
function validatePassword(password) {
  const minLength = 12;
  const errors = [];

  if (password.length < minLength) {
    errors.push(`Minimum ${minLength} characters`);
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Must contain lowercase letter');
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Must contain uppercase letter');
  }

  if (!/[0-9]/.test(password)) {
    errors.push('Must contain number');
  }

  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Must contain special character');
  }

  // Check against common passwords
  const commonPasswords = ['password', '12345678', 'qwerty'];
  if (commonPasswords.includes(password.toLowerCase())) {
    errors.push('Password too common');
  }

  return errors.length === 0 ? null : errors;
}

// Use library
const passwordValidator = require('password-validator');
const schema = new passwordValidator();
schema
  .is().min(12)
  .is().max(128)
  .has().uppercase()
  .has().lowercase()
  .has().digits()
  .has().symbols()
  .has().not().spaces()
  .is().not().oneOf(['Password123!', 'Admin123!']);

if (!schema.validate(password)) {
  return res.status(400).send('Password does not meet requirements');
}
```

**Security impact:**
Weak passwords are easily cracked by attackers.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

**Attribution:** OWASP, NIST SP 800-63B

---


> *20 of the most relevant guidelines shown. Remaining guidelines omitted.*

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
