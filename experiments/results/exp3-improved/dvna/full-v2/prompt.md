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

### JWT-SECRET: Secure JWT Implementation

**Severity:** Critical

**Vulnerable code:**
```javascript
// Weak secret
const jwt = require('jsonwebtoken');
const token = jwt.sign({ userId: user.id }, 'secret');

// No expiration
const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);

// Algorithm confusion
const token = jwt.sign(payload, publicKey, { algorithm: 'HS256' });
// Attacker can use 'none' algorithm

// No signature verification
const decoded = jwt.decode(token); // Doesn't verify signature!
```

**Secure implementation:**
```javascript
const jwt = require('jsonwebtoken');

// Strong secret (256-bit minimum)
const secret = process.env.JWT_SECRET; // Generate with: crypto.randomBytes(32).toString('hex')

// Sign with expiration
const token = jwt.sign(
  { userId: user.id },
  secret,
  { 
    expiresIn: '15m',
    algorithm: 'HS256',
    issuer: 'your-app',
    audience: 'your-api'
  }
);

// Verify properly
try {
  const decoded = jwt.verify(token, secret, {
    algorithms: ['HS256'], // Whitelist algorithms
    issuer: 'your-app',
    audience: 'your-api'
  });
} catch (err) {
  return res.status(401).send('Invalid token');
}

// Use RS256 for better security (public/private key)
const privateKey = fs.readFileSync('private.pem');
const publicKey = fs.readFileSync('public.pem');

const token = jwt.sign(payload, privateKey, { 
  algorithm: 'RS256',
  expiresIn: '15m'
});

const decoded = jwt.verify(token, publicKey, { 
  algorithms: ['RS256'] 
});
```

**Security impact:**
Weak JWT implementation allows token forgery and unauthorized access.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures, CWE-347

**Attribution:** OWASP, RFC 7519

---

### JWT-EXPIRE: Implement Token Expiration and Refresh

**Severity:** High

**Vulnerable code:**
```javascript
// No expiration
const token = jwt.sign({ userId: user.id }, secret);

// Long-lived tokens
const token = jwt.sign({ userId: user.id }, secret, { expiresIn: '30d' });

// No token refresh mechanism
app.get('/protected', authenticate, (req, res) => {
  // Token never refreshed
});
```

**Secure implementation:**
```javascript
// Short-lived access tokens
function generateAccessToken(user) {
  return jwt.sign(
    { userId: user.id, type: 'access' },
    process.env.ACCESS_TOKEN_SECRET,
    { expiresIn: '15m' }
  );
}

// Long-lived refresh tokens
function generateRefreshToken(user) {
  return jwt.sign(
    { userId: user.id, type: 'refresh' },
    process.env.REFRESH_TOKEN_SECRET,
    { expiresIn: '7d' }
  );
}

// Login endpoint
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body);
  const accessToken = generateAccessToken(user);
  const refreshToken = generateRefreshToken(user);
  
  // Store refresh token in database
  await db.refreshTokens.insert({ 
    userId: user.id, 
    token: refreshToken,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  });
  
  res.json({ accessToken, refreshToken });
});

// Refresh endpoint
app.post('/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  try {
    const decoded = jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET);
    
    // Check if refresh token exists in database
    const storedToken = await db.refreshTokens.findOne({ 
      token: refreshToken,
      userId: decoded.userId 
    });
    
    if (!storedToken) {
      return res.status(403).send('Invalid refresh token');
    }
    
    // Generate new access token
    const accessToken = generateAccessToken({ id: decoded.userId });
    res.json({ accessToken });
  } catch (err) {
    return res.status(403).send('Invalid refresh token');
  }
});

// Logout - revoke refresh token
app.post('/logout', async (req, res) => {
  await db.refreshTokens.deleteOne({ token: req.body.refreshToken });
  res.send('Logged out');
});
```

**Security impact:**
Long-lived tokens increase the window for token theft and unauthorized access.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

**Attribution:** OWASP, OAuth 2.0

---

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

### OAUTH-VALIDATE: Validate OAuth/OIDC Properly

**Severity:** High

**Vulnerable code:**
```javascript
// No state parameter (CSRF)
app.get('/auth/google', (req, res) => {
  const authUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${clientId}&redirect_uri=${redirectUri}`;
  res.redirect(authUrl);
});

// No token validation
app.get('/callback', async (req, res) => {
  const { code } = req.query;
  const token = await getAccessToken(code);
  req.session.token = token; // Trust without validation
});

// No PKCE for public clients
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Use state parameter
app.get('/auth/google', (req, res) => {
  const state = crypto.randomBytes(32).toString('hex');
  req.session.oauthState = state;
  
  const authUrl = `https://accounts.google.com/o/oauth2/auth?` +
    `client_id=${clientId}&` +
    `redirect_uri=${encodeURIComponent(redirectUri)}&` +
    `response_type=code&` +
    `scope=openid%20email%20profile&` +
    `state=${state}`;
  
  res.redirect(authUrl);
});

// Validate state and token
app.get('/callback', async (req, res) => {
  const { code, state } = req.query;
  
  // Validate state (CSRF protection)
  if (state !== req.session.oauthState) {
    return res.status(403).send('Invalid state');
  }
  delete req.session.oauthState;
  
  // Exchange code for token
  const tokens = await getTokens(code);
  
  // Validate ID token
  const jwt = require('jsonwebtoken');
  const jwksClient = require('jwks-rsa');
  
  const client = jwksClient({
    jwksUri: 'https://www.googleapis.com/oauth2/v3/certs'
  });
  
  const getKey = (header, callback) => {
    client.getSigningKey(header.kid, (err, key) => {
      callback(null, key.getPublicKey());
    });
  };
  
  jwt.verify(tokens.id_token, getKey, {
    audience: clientId,
    issuer: 'https://accounts.google.com'
  }, (err, decoded) => {
    if (err) return res.status(401).send('Invalid token');
    req.session.user = decoded;
    res.redirect('/dashboard');
  });
});

// PKCE for SPA/mobile
function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto.createHash('sha256')
    .update(verifier)
    .digest('base64url');
  return { verifier, challenge };
}
```

**Security impact:**
Improper OAuth validation allows account takeover and authorization bypass.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

**Attribution:** OAuth 2.0 RFC 6749, OIDC specification

---

### MFA-IMPLEMENT: Implement Multi-Factor Authentication

**Severity:** Medium

**Vulnerable code:**
```javascript
// Single-factor authentication only
app.post('/login', async (req, res) => {
  const user = await db.users.findOne({ username: req.body.username });
  if (await bcrypt.compare(req.body.password, user.passwordHash)) {
    req.session.user = user;
    res.redirect('/dashboard'); // No MFA
  }
});
```

**Secure implementation:**
```javascript
const speakeasy = require('speakeasy');
const QRCode = require('qrcode');

// Enable TOTP for user
app.post('/mfa/enable', async (req, res) => {
  const secret = speakeasy.generateSecret({
    name: `YourApp (${req.user.email})`
  });
  
  await db.users.update(
    { id: req.user.id },
    { mfaSecret: secret.base32, mfaEnabled: false }
  );
  
  QRCode.toDataURL(secret.otpauth_url, (err, dataUrl) => {
    res.json({ secret: secret.base32, qrCode: dataUrl });
  });
});

// Verify TOTP and enable MFA
app.post('/mfa/verify', async (req, res) => {
  const user = await db.users.findOne({ id: req.user.id });
  const verified = speakeasy.totp.verify({
    secret: user.mfaSecret,
    encoding: 'base32',
    token: req.body.token,
    window: 2
  });
  
  if (verified) {
    await db.users.update({ id: user.id }, { mfaEnabled: true });
    res.send('MFA enabled');
  } else {
    res.status(400).send('Invalid code');
  }
});

// Login with MFA
app.post('/login', async (req, res) => {
  const user = await db.users.findOne({ username: req.body.username });
  
  if (!await bcrypt.compare(req.body.password, user.passwordHash)) {
    return res.status(401).send('Invalid credentials');
  }
  
  if (user.mfaEnabled) {
    req.session.pendingMfa = user.id;
    return res.json({ requiresMfa: true });
  }
  
  req.session.user = user;
  res.redirect('/dashboard');
});

// MFA verification endpoint
app.post('/mfa/login', async (req, res) => {
  if (!req.session.pendingMfa) {
    return res.status(400).send('No pending MFA');
  }
  
  const user = await db.users.findOne({ id: req.session.pendingMfa });
  const verified = speakeasy.totp.verify({
    secret: user.mfaSecret,
    encoding: 'base32',
    token: req.body.token,
    window: 2
  });
  
  if (verified) {
    delete req.session.pendingMfa;
    req.session.user = user;
    res.redirect('/dashboard');
  } else {
    res.status(401).send('Invalid code');
  }
});
```

**Security impact:**
MFA significantly reduces account takeover risk even if passwords are compromised.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

**Attribution:** NIST SP 800-63B

---

### CRED-STORE: Secure Credential Storage

**Severity:** Critical

**Vulnerable code:**
```javascript
// Hardcoded credentials
const dbPassword = 'MyPassword123';
const apiKey = 'sk_live_abc123xyz';

// In config file committed to git
const config = {
  database: {
    password: 'production_password'
  }
};

// Environment variables logged
console.log(process.env); // Leaks secrets in logs
```

**Secure implementation:**
```javascript
// Use environment variables
require('dotenv').config();
const dbPassword = process.env.DB_PASSWORD;
const apiKey = process.env.API_KEY;

// .env file (add to .gitignore!)
/*
DB_PASSWORD=secure_password_here
API_KEY=sk_live_abc123xyz
*/

// Use secret management service
const AWS = require('aws-sdk');
const secretsManager = new AWS.SecretsManager();

async function getSecret(secretName) {
  const data = await secretsManager.getSecretValue({ 
    SecretId: secretName 
  }).promise();
  return JSON.parse(data.SecretString);
}

const dbCreds = await getSecret('production/database');

// Azure Key Vault
const { SecretClient } = require('@azure/keyvault-secrets');
const { DefaultAzureCredential } = require('@azure/identity');

const credential = new DefaultAzureCredential();
const client = new SecretClient(vaultUrl, credential);
const secret = await client.getSecret('database-password');

// Don't log secrets
const safeEnv = { ...process.env };
delete safeEnv.DB_PASSWORD;
delete safeEnv.API_KEY;
console.log(safeEnv);

// Validate .gitignore
/*
.env
.env.local
.env.*.local
config/secrets.json
*/
```

**Security impact:**
Exposed credentials lead to unauthorized access and data breaches.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures, CWE-798

**Attribution:** OWASP

---

### TIMING-ATTACK: Prevent Timing Attacks

**Severity:** Medium

**Vulnerable code:**
```javascript
// String comparison (timing attack)
if (userToken === storedToken) {
  // Granted access
}

// Early return on password comparison
const user = await db.users.findOne({ username });
if (!user) {
  return res.status(401).send('Invalid credentials'); // Fast
}
if (!await bcrypt.compare(password, user.passwordHash)) {
  return res.status(401).send('Invalid credentials'); // Slow
}
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Constant-time comparison
function secureCompare(a, b) {
  return crypto.timingSafeEqual(
    Buffer.from(a),
    Buffer.from(b)
  );
}

if (secureCompare(userToken, storedToken)) {
  // Granted access
}

// Always hash password even if user doesn't exist
const user = await db.users.findOne({ username });
const dummyHash = '$2b$12$dummy.hash.value.here.for.timing';
const hashToCompare = user ? user.passwordHash : dummyHash;
const isValid = await bcrypt.compare(password, hashToCompare);

if (user && isValid) {
  // Login successful
} else {
  // Same response time whether user exists or not
  return res.status(401).send('Invalid credentials');
}

// Or use libraries
const { timingSafeEqual } = require('crypto');
```

**Security impact:**
Timing attacks can reveal whether usernames exist or leak information about secrets.

**Compliance:** CWE-208

**Attribution:** OWASP

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

### SAMESITE-COOKIE: Use SameSite Cookie Attribute

**Severity:** Medium

**Vulnerable code:**
```javascript
// No SameSite attribute
res.cookie('session', sessionId, {
  httpOnly: true,
  secure: true
  // Missing sameSite
});

// SameSite: None without Secure
res.cookie('tracking', trackingId, {
  sameSite: 'none'
  // Missing secure: true
});
```

**Secure implementation:**
```javascript
// Strict SameSite for session cookies
res.cookie('session', sessionId, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict', // Best for auth cookies
  maxAge: 900000
});

// Lax for some functionality
res.cookie('prefs', preferences, {
  httpOnly: false,
  secure: true,
  sameSite: 'lax' // Allows top-level navigation
});

// None only when necessary (with Secure)
res.cookie('embed', embedId, {
  secure: true,
  sameSite: 'none' // For cross-site embeds
});

// Express session config
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict'
  }
}));
```

**Security impact:**
SameSite cookies provide CSRF protection and limit cross-site tracking.

**Compliance:** OWASP A01:2021 - Broken Access Control

**Attribution:** OWASP, RFC 6265bis

---

### HTTPS-ONLY: Enforce HTTPS

**Severity:** High

**Vulnerable code:**
```javascript
// HTTP server
const http = require('http');
http.createServer(app).listen(80);

// Mixed content
res.send('<script src="http://example.com/script.js"></script>');

// No redirect to HTTPS
app.listen(80);
```

**Secure implementation:**
```javascript
// Redirect HTTP to HTTPS
const http = require('http');
const https = require('https');
const fs = require('fs');

// HTTP server redirects to HTTPS
http.createServer((req, res) => {
  res.writeHead(301, { Location: `https://${req.headers.host}${req.url}` });
  res.end();
}).listen(80);

// HTTPS server
const options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
};
https.createServer(options, app).listen(443);

// Or use middleware
app.use((req, res, next) => {
  if (req.secure || req.headers['x-forwarded-proto'] === 'https') {
    next();
  } else {
    res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
});

// Use helmet
const helmet = require('helmet');
app.use(helmet());

// Secure cookies
res.cookie('session', sessionId, {
  secure: true, // HTTPS only
  httpOnly: true
});
```

**Security impact:**
HTTP allows man-in-the-middle attacks, session hijacking, and credential theft.

**Compliance:** OWASP A02:2021 - Cryptographic Failures

**Attribution:** OWASP

---

### HSTS-HEADER: Use HTTP Strict Transport Security

**Severity:** Medium

**Vulnerable code:**
```javascript
// No HSTS header
app.get('/', (req, res) => {
  res.send('Hello');
});
```

**Secure implementation:**
```javascript
// Manual HSTS header
app.use((req, res, next) => {
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=31536000; includeSubDomains; preload'
  );
  next();
});

// Use helmet
const helmet = require('helmet');
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true
}));
```

**Security impact:**
HSTS prevents protocol downgrade attacks and cookie hijacking.

**Compliance:** OWASP A05:2021 - Security Misconfiguration

**Attribution:** OWASP

---

### CSP-POLICY: Strong Content Security Policy

**Severity:** Medium

**Vulnerable code:**
```javascript
// No CSP or weak CSP covered in CSP-HEADER guideline
```

**Secure implementation:**
```javascript
// See CSP-HEADER guideline for complete implementation
```

**Security impact:**
CSP prevents XSS and data injection attacks.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** OWASP

---

### X-FRAME-OPTIONS: Prevent Clickjacking

**Severity:** Medium

**Vulnerable code:**
```javascript
// No X-Frame-Options header
app.get('/', (req, res) => {
  res.send('<html>...</html>');
});
```

**Secure implementation:**
```javascript
// Manual header
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  next();
});

// Or SAMEORIGIN
res.setHeader('X-Frame-Options', 'SAMEORIGIN');

// Use helmet
const helmet = require('helmet');
app.use(helmet.frameguard({ action: 'deny' }));

// Modern alternative: CSP frame-ancestors
app.use(helmet.contentSecurityPolicy({
  directives: {
    frameAncestors: ["'none'"]
  }
}));
```

**Security impact:**
Clickjacking allows attackers to trick users into clicking hidden elements.

**Compliance:** OWASP A04:2021 - Insecure Design

**Attribution:** OWASP

---

### CORS-CONFIG: Secure CORS Configuration

**Severity:** High

**Vulnerable code:**
```javascript
// Allow all origins
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Credentials', 'true'); // Dangerous with *
  next();
});

// Reflect origin without validation
res.header('Access-Control-Allow-Origin', req.headers.origin);
res.header('Access-Control-Allow-Credentials', 'true');
```

**Secure implementation:**
```javascript
const cors = require('cors');

// Whitelist specific origins
const allowedOrigins = [
  'https://app.example.com',
  'https://admin.example.com'
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 600 // 10 minutes
}));

// Manual implementation
app.use((req, res, next) => {
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.header('Access-Control-Allow-Origin', origin);
    res.header('Access-Control-Allow-Credentials', 'true');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  }
  next();
});

// Preflight request handling
app.options('*', cors());
```

**Security impact:**
Misconfigured CORS allows unauthorized cross-origin access to sensitive data.

**Compliance:** OWASP A01:2021 - Broken Access Control, CWE-346

**Attribution:** OWASP

---

## 5. API SECURITY

### RATE-LIMIT: Implement Rate Limiting

**Severity:** Medium

**Vulnerable code:**
```javascript
// No rate limiting
app.post('/login', (req, res) => {
  // Vulnerable to brute force
});

app.post('/api/search', (req, res) => {
  // Vulnerable to DoS
});
```

**Secure implementation:**
```javascript
const rateLimit = require('express-rate-limit');

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/api/', apiLimiter);

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 attempts
  skipSuccessfulRequests: true,
  message: 'Too many login attempts, please try again later'
});

app.post('/login', authLimiter, (req, res) => {
  // ...
});

// Use Redis for distributed rate limiting
const RedisStore = require('rate-limit-redis');
const redis = require('redis');
const client = redis.createClient();

const limiter = rateLimit({
  store: new RedisStore({
    client: client,
    prefix: 'rl:'
  }),
  windowMs: 15 * 60 * 1000,
  max: 100
});

// Per-user rate limiting
const userLimiter = rateLimit({
  keyGenerator: (req) => req.user?.id || req.ip,
  windowMs: 60 * 1000,
  max: 10
});
```

**Security impact:**
No rate limiting allows brute force attacks, credential stuffing, and DoS.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

**Attribution:** OWASP API Security Top 10

---

### API-AUTH: Secure API Authentication

**Severity:** Critical

**Vulnerable code:**
```javascript
// No authentication
app.get('/api/users', (req, res) => {
  const users = await db.users.find();
  res.json(users);
});

// API key in URL
app.get('/api/data', (req, res) => {
  const apiKey = req.query.api_key; // Logged in access logs!
  if (apiKey === storedKey) {
    // ...
  }
});
```

**Secure implementation:**
```javascript
// Bearer token authentication
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  const token = authHeader.substring(7);
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}

app.get('/api/users', authenticate, (req, res) => {
  // ...
});

// API key in header (not URL)
function validateApiKey(req, res, next) {
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }
  
  // Hash comparison to prevent timing attacks
  const hashedKey = crypto.createHash('sha256').update(apiKey).digest('hex');
  const validHash = process.env.API_KEY_HASH;
  
  if (hashedKey !== validHash) {
    return res.status(403).json({ error: 'Invalid API key' });
  }
  
  next();
}

app.get('/api/data', validateApiKey, (req, res) => {
  // ...
});
```

**Security impact:**
Unauthenticated APIs expose sensitive data and functionality.

**Compliance:** OWASP A01:2021 - Broken Access Control

**Attribution:** OWASP API Security Top 10

---

### API-VALIDATE: Validate API Input

**Severity:** High

**Vulnerable code:**
```javascript
// No validation
app.post('/api/users', (req, res) => {
  const user = req.body;
  db.users.insert(user); // Accepts any input
});

// Type confusion
const userId = req.params.id;
db.users.findOne({ id: userId }); // String vs number
```

**Secure implementation:**
```javascript
const { body, param, query, validationResult } = require('express-validator');

// Schema validation
app.post('/api/users',
  body('email').isEmail().normalizeEmail(),
  body('age').isInt({ min: 0, max: 120 }),
  body('username').trim().isLength({ min: 3, max: 20 }).matches(/^[a-zA-Z0-9_]+$/),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    const user = {
      email: req.body.email,
      age: req.body.age,
      username: req.body.username
    };
    
    await db.users.insert(user);
    res.json(user);
  }
);

// Use Joi for complex schemas
const Joi = require('joi');

const userSchema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(0).max(120),
  password: Joi.string().pattern(/^[a-zA-Z0-9]{3,30}$/).required()
});

app.post('/api/users', async (req, res) => {
  try {
    const value = await userSchema.validateAsync(req.body);
    await db.users.insert(value);
    res.json(value);
  } catch (err) {
    res.status(400).json({ error: err.details[0].message });
  }
});

// Path parameter validation
app.get('/api/users/:id',
  param('id').isInt(),
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    const userId = parseInt(req.params.id);
    const user = await db.users.findOne({ id: userId });
    res.json(user);
  }
);
```

**Security impact:**
Unvalidated input leads to injection, data corruption, and business logic bypass.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** OWASP API Security Top 10

---

### API-KEY-SECURE: Secure API Key Management

**Severity:** High

**Vulnerable code:**
```javascript
// API key in code
const STRIPE_KEY = 'sk_live_abc123xyz';

// API key in client-side code
const script = `
  <script>
    const apiKey = '${process.env.API_KEY}';
    fetch('/api/data?key=' + apiKey);
  </script>
`;
```

**Secure implementation:**
```javascript
// Server-side only
require('dotenv').config();
const stripeKey = process.env.STRIPE_SECRET_KEY;

// Separate public and secret keys
const publicKey = process.env.STRIPE_PUBLIC_KEY; // OK for client
const secretKey = process.env.STRIPE_SECRET_KEY; // Server only

// Pass to client safely
res.render('checkout', {
  stripePublicKey: publicKey // Public key only
});

// Rotate keys regularly
// Use key versioning
const apiKeys = {
  'v1': process.env.API_KEY_V1,
  'v2': process.env.API_KEY_V2
};

function validateApiKey(req, res, next) {
  const keyVersion = req.headers['x-api-version'] || 'v2';
  const providedKey = req.headers['x-api-key'];
  
  if (apiKeys[keyVersion] === providedKey) {
    next();
  } else {
    res.status(403).json({ error: 'Invalid API key' });
  }
}

// Use OAuth for third-party access
// Implement key scopes
const keyScopes = {
  'key_abc': ['read:users'],
  'key_xyz': ['read:users', 'write:users']
};
```

**Security impact:**
Exposed API keys allow unauthorized access to services and data.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

**Attribution:** OWASP

---

### API-ERROR: Secure Error Responses

**Severity:** Medium

**Vulnerable code:**
```javascript
// Detailed error messages
app.get('/api/user/:id', async (req, res) => {
  try {
    const user = await db.users.findOne({ id: req.params.id });
    res.json(user);
  } catch (err) {
    res.status(500).json({
      error: err.message, // Database error details
      stack: err.stack // Stack trace
    });
  }
});

// SQL error messages
// "Column 'ssn' not found" - reveals schema
```

**Secure implementation:**
```javascript
// Generic error messages to client
app.get('/api/user/:id', async (req, res) => {
  try {
    const user = await db.users.findOne({ id: req.params.id });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    // Log detailed error server-side
    console.error('Error fetching user:', err);
    logger.error({ err, userId: req.params.id }, 'Failed to fetch user');
    
    // Generic error to client
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handler middleware
app.use((err, req, res, next) => {
  // Log full error
  logger.error({
    err,
    req: {
      method: req.method,
      url: req.url,
      headers: req.headers
    }
  });
  
  // Return generic error
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' });
  } else {
    // Detailed errors in development only
    res.status(500).json({
      error: err.message,
      stack: err.stack
    });
  }
});
```

**Security impact:**
Detailed errors leak sensitive information about system internals.

**Compliance:** OWASP A04:2021 - Insecure Design, CWE-209

**Attribution:** OWASP

---

### API-VERSIONING: API Versioning and Deprecation

**Severity:** Low

**Vulnerable code:**
```javascript
// No versioning
app.get('/api/users', (req, res) => {
  // Breaking changes affect all clients
});

// Breaking changes without notice
app.get('/api/data', (req, res) => {
  // Changed response format
});
```

**Secure implementation:**
```javascript
// URL-based versioning
app.get('/api/v1/users', (req, res) => {
  // Version 1
});

app.get('/api/v2/users', (req, res) => {
  // Version 2 with new features
});

// Header-based versioning
app.get('/api/users', (req, res) => {
  const version = req.headers['api-version'] || '1';
  
  if (version === '1') {
    // Legacy format
  } else if (version === '2') {
    // New format
  }
});

// Deprecation warnings
app.get('/api/v1/users', (req, res) => {
  res.setHeader('X-API-Warn', 'Deprecated: Use /api/v2/users. Removal date: 2024-12-31');
  res.setHeader('X-API-Deprecation-Date', '2024-12-31');
  // ...
});

// Sunset header
res.setHeader('Sunset', 'Sat, 31 Dec 2024 23:59:59 GMT');
```

**Security impact:**
Proper versioning prevents breaking changes and allows security updates.

**Compliance:** Best practice

**Attribution:** REST API Best Practices

---

## 6. DATA PRIVACY

### PII-IDENTIFY: Identify and Classify PII

**Severity:** High

**Vulnerable code:**
```javascript
// No PII awareness
const user = {
  name: req.body.name,
  email: req.body.email,
  ssn: req.body.ssn,
  phone: req.body.phone
};
db.users.insert(user);
```

**Secure implementation:**
```javascript
// Classify data
const UserSchema = new mongoose.Schema({
  // Public
  username: { type: String, required: true },
  
  // PII - Sensitive
  email: { type: String, required: true, pii: true },
  phone: { type: String, pii: true },
  
  // PII - Highly Sensitive
  ssn: { type: String, select: false, encrypted: true, pii: true },
  dateOfBirth: { type: Date, pii: true },
  
  // Metadata
  createdAt: { type: Date, default: Date.now }
});

// Document PII handling
/*
PII Classification:
- Email: PII, encrypted at rest, access logged
- Phone: PII, encrypted at rest
- SSN: Highly sensitive, encrypted, minimal access
- DOB: PII, restricted access
*/

// Access control
function requirePIIAccess(req, res, next) {
  if (!req.user.roles.includes('pii-access')) {
    logger.warn({ userId: req.user.id }, 'Unauthorized PII access attempt');
    return res.status(403).send('Insufficient permissions');
  }
  next();
}

app.get('/api/users/:id/pii', authenticate, requirePIIAccess, async (req, res) => {
  // Log PII access
  await auditLog.create({
    userId: req.user.id,
    action: 'pii-access',
    targetId: req.params.id,
    timestamp: new Date()
  });
  
  const user = await User.findById(req.params.id).select('+ssn');
  res.json(user);
});
```

**Security impact:**
Unidentified PII leads to privacy violations and regulatory non-compliance.

**Compliance:** GDPR Art. 4, CCPA

**Attribution:** GDPR, CCPA

---

### PII-MINIMIZE: Data Minimization

**Severity:** Medium

**Vulnerable code:**
```javascript
// Collecting unnecessary data
const userSchema = new Schema({
  name: String,
  email: String,
  phone: String,
  ssn: String, // Not needed for app
  dob: Date, // Collecting when only age needed
  mothersMaidenName: String, // Security question anti-pattern
  race: String, // Unnecessary sensitive data
  medicalHistory: String // Irrelevant to app
});
```

**Secure implementation:**
```javascript
// Collect only necessary data
const userSchema = new Schema({
  username: { type: String, required: true },
  email: { type: String, required: true }, // Required for password reset
  // Don't collect: ssn, dob (only age if needed), mother's maiden name
});

// Compute derived data instead of storing
UserSchema.virtual('age').get(function() {
  if (!this.dateOfBirth) return null;
  const today = new Date();
  const birthDate = new Date(this.dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
});

// Age verification without storing DOB
const isOver18 = req.body.birthYear < (new Date().getFullYear() - 18);
db.users.insert({ username, email, isAdult: isOver18 });

// Progressive disclosure - collect when needed
// Initial signup
const user = { email, password };

// Later, if needed for feature
if (userWantsShipping) {
  user.shippingAddress = req.body.address;
}
```

**Security impact:**
Excess data collection increases breach impact and privacy risk.

**Compliance:** GDPR Art. 5(1)(c), CCPA

**Attribution:** GDPR Principles

---

### PII-ENCRYPT: Encrypt PII at Rest

**Severity:** Critical

**Vulnerable code:**
```javascript
// Plain text PII storage
const user = {
  email: req.body.email,
  ssn: req.body.ssn, // Stored in plain text
  creditCard: req.body.card
};
await db.users.insert(user);
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Field-level encryption
const algorithm = 'aes-256-gcm';
const key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex'); // 32 bytes

function encrypt(text) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}

function decrypt(encrypted, ivHex, authTagHex) {
  const decipher = crypto.createDecipheriv(
    algorithm,
    key,
    Buffer.from(ivHex, 'hex')
  );
  
  decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

// Mongoose plugin for encryption
const mongooseFieldEncryption = require('mongoose-field-encryption').fieldEncryption;

const UserSchema = new Schema({
  email: String,
  ssn: String,
  creditCard: String
});

UserSchema.plugin(mongooseFieldEncryption, {
  fields: ['ssn', 'creditCard'],
  secret: process.env.ENCRYPTION_KEY
});

// Or manual encryption
const ssnData = encrypt(req.body.ssn);
const user = {
  email: req.body.email,
  ssn: ssnData.encrypted,
  ssnIv: ssnData.iv,
  ssnAuthTag: ssnData.authTag
};
await db.users.insert(user);
```

**Security impact:**
Unencrypted PII in databases leads to massive breaches when databases are compromised.

**Compliance:** GDPR Art. 32, PCI-DSS Requirement 3, CWE-311

**Attribution:** GDPR, PCI-DSS

---

### PII-LOG: Don't Log PII

**Severity:** High

**Vulnerable code:**
```javascript
// Logging sensitive data
console.log('User logged in:', req.body);
// Logs: { username: 'john', password: 'secret123', ssn: '123-45-6789' }

logger.info({ user: req.user }, 'Profile updated');
// Logs entire user object with PII

console.log(`Processing payment for ${user.email} with card ${user.creditCard}`);
```

**Secure implementation:**
```javascript
// Sanitize before logging
function sanitizeForLogging(obj) {
  const piiFields = ['password', 'ssn', 'creditCard', 'dob'];
  const sanitized = { ...obj };
  
  piiFields.forEach(field => {
    if (sanitized[field]) {
      sanitized[field] = '[REDACTED]';
    }
  });
  
  return sanitized;
}

logger.info(sanitizeForLogging(req.body), 'User logged in');

// Log only necessary fields
logger.info({  
  userId: req.user.id,
  username: req.user.username
  // Don't log: email, phone, address
}, 'Profile updated');

// Mask sensitive data
function maskCard(card) {
  return `****-****-****-${card.slice(-4)}`;
}

logger.info(`Processing payment for user ${user.id} with card ${maskCard(user.creditCard)}`);

// Use structured logging library with filters
const pino = require('pino');
const logger = pino({
  redact: {
    paths: ['req.body.password', 'req.body.ssn', '*.creditCard'],
    remove: true
  }
});
```

**Security impact:**
PII in logs creates compliance issues and increases breach surface area.

**Compliance:** GDPR Art. 5, CWE-532

**Attribution:** OWASP Logging Cheat Sheet

---

### PII-RESIDENCY: Enforce Data Localization

**Principle:** Jurisdictions such as EU (GDPR Art. 44-50), Brazil (LGPD Art. 33), and India (DPDP) mandate that certain data reside in-region or follow approved transfer mechanisms.

**Implementation:**
```javascript
const region = tenant.dataRegion; // e.g., 'eu-west-1'
const db = getRegionalMongoClient(region);
await db.collection('profiles').insertOne({ ...profile, tenantId: tenant.id });
```

- Route DB/cache/storage clients using residency metadata.
- Disable cross-region replication for sensitive buckets and log any cross-border transfers.
- Ensure subprocessors (logging, analytics) support EU/US data centers with DPAs/SCCs executed.

---

### PII-RETENTION: Honor Retention & Deletion SLAs

**Principle:** GDPR Art. 5(1)(e) and SOC 2 CC8 require data minimization over time, not just at ingestion.

**Implementation:**
```javascript
const cutoff = subDays(new Date(), 90);
await db.collection('audit_logs').deleteMany({ createdAt: { $lt: cutoff } });
```

- Define per-field retention policies (e.g., IP logs 30 days, payment tokens 1 year).
- Provide user-initiated erasure endpoints and verify cascading deletes (DB, caches, S3, analytics).
- Track legal holds/exceptions with immutable audit events.

---

### CONSENT-MANAGE: Implement Consent Management

**Severity:** High (for GDPR compliance)

**Vulnerable code:**
```javascript
// No consent tracking
app.post('/newsletter', (req, res) => {
  db.subscribers.insert({ email: req.body.email });
  sendWelcomeEmail(req.body.email);
});

// Pre-checked boxes
res.send(`
  <form>
    <input type="checkbox" checked name="marketing"> Marketing emails
  </form>
`);
```

**Secure implementation:**
```javascript
// Explicit consent with granular options
const ConsentSchema = new Schema({
  userId: { type: ObjectId, required: true },
  marketing: {
    granted: { type: Boolean, default: false },
    timestamp: Date,
    method: String // 'web', 'app', 'phone'
  },
  analytics: {
    granted: { type: Boolean, default: false },
    timestamp: Date
  },
  thirdPartySharing: {
    granted: { type: Boolean, default: false },
    timestamp: Date
  },
  consentVersion: String, // Track policy version
  ipAddress: String,
  userAgent: String
});

// Consent form (not pre-checked)
res.send(`
  <form method="POST" action="/consent">
    <label>
      <input type="checkbox" name="marketing"> 
      I agree to receive marketing emails
    </label>
    <label>
      <input type="checkbox" name="analytics">
      I agree to analytics tracking
    </label>
    <button type="submit">Save Preferences</button>
  </form>
`);

// Record consent
app.post('/consent', async (req, res) => {
  await Consent.create({
    userId: req.user.id,
    marketing: {
      granted: req.body.marketing === 'on',
      timestamp: new Date(),
      method: 'web'
    },
    analytics: {
      granted: req.body.analytics === 'on',
      timestamp: new Date()
    },
    consentVersion: '1.0',
    ipAddress: req.ip,
    userAgent: req.headers['user-agent']
  });
  
  res.send('Preferences saved');
});

// Check consent before action
async function requireConsent(consentType) {
  return async (req, res, next) => {
    const consent = await Consent.findOne({ userId: req.user.id });
    
    if (!consent || !consent[consentType].granted) {
      return res.status(403).send('Consent required');
    }
    
    next();
  };
}

app.post('/send-marketing-email', 
  requireConsent('marketing'),
  (req, res) => {
    // ...
  }
);
```

**Security impact:**
Missing consent management violates privacy regulations and user trust.

**Compliance:** GDPR Art. 7, CCPA

**Attribution:** GDPR

---

### DATA-ERASURE: Implement Right to Erasure

**Severity:** High (for GDPR)

**Vulnerable code:**
```javascript
// Soft delete only
app.delete('/account', async (req, res) => {
  await User.update({ id: req.user.id }, { deleted: true });
  // Data still in database
});

// No data retention policy
// Data kept forever
```

**Secure implementation:**
```javascript
// Complete data erasure
app.delete('/account', async (req, res) => {
  const userId = req.user.id;
  
  // Log deletion request (compliance)
  await AuditLog.create({
    action: 'account-deletion',
    userId,
    timestamp: new Date()
  });
  
  // Delete from all tables
  await Promise.all([
    User.deleteOne({ id: userId }),
    Profile.deleteOne({ userId }),
    Orders.deleteMany({ userId }),
    Sessions.deleteMany({ userId }),
    AuditLogs.deleteMany({ userId }) // After retention period
  ]);
  
  // Delete files
  const userFiles = await Files.find({ userId });
  for (const file of userFiles) {
    await deleteFile(file.path);
  }
  await Files.deleteMany({ userId });
  
  // Anonymize references (can't delete due to integrity)
  await Reviews.updateMany(
    { userId },
    { userId: null, userName: '[Deleted User]' }
  );
  
  res.send('Account deleted');
});

// Automated data retention
async function cleanupOldData() {
  const retentionDays = 90;
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - retentionDays);
  
  // Delete old logs
  await AuditLog.deleteMany({
    timestamp: { $lt: cutoffDate }
  });
  
  // Delete old sessions
  await Session.deleteMany({
    lastActivity: { $lt: cutoffDate }
  });
}

// Run cleanup daily
setInterval(cleanupOldData, 24 * 60 * 60 * 1000);
```

**Security impact:**
Inability to delete data violates user rights and regulations.

**Compliance:** GDPR Art. 17, CCPA

**Attribution:** GDPR Right to Erasure

---

### DATA-EXPORT: Implement Right to Data Portability

**Severity:** Medium (for GDPR)

**Vulnerable code:**
```javascript
// No data export
// Users can't get their data in machine-readable format
```

**Secure implementation:**
```javascript
// Export user data
app.get('/api/my-data', authenticate, async (req, res) => {
  const userId = req.user.id;
  
  // Gather all user data
  const [user, profile, orders, reviews] = await Promise.all([
    User.findById(userId).lean(),
    Profile.findOne({ userId }).lean(),
    Order.find({ userId }).lean(),
    Review.find({ userId }).lean()
  ]);
  
  // Decrypt PII if necessary
  if (user.ssnEncrypted) {
    user.ssn = decrypt(user.ssnEncrypted, user.ssnIv, user.ssnAuthTag);
    delete user.ssnEncrypted;
    delete user.ssnIv;
    delete user.ssnAuthTag;
  }
  
  // Remove internal fields
  delete user.passwordHash;
  delete user._id;
  delete user.__v;
  
  const exportData = {
    exportDate: new Date().toISOString(),
    user,
    profile,
    orders,
    reviews
  };
  
  // Return as JSON or CSV
  if (req.query.format === 'csv') {
    const csv = convertToCSV(exportData);
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename=my-data.csv');
    res.send(csv);
  } else {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', 'attachment; filename=my-data.json');
    res.json(exportData);
  }
  
  // Log export (compliance)
  await AuditLog.create({
    action: 'data-export',
    userId,
    format: req.query.format || 'json',
    timestamp: new Date()
  });
});
```

**Security impact:**
Users unable to export their data violates portability rights.

**Compliance:** GDPR Art. 20

**Attribution:** GDPR Data Portability

---

### GDPR-COMPLY: GDPR Compliance Checklist

**Severity:** High (if operating in EU)

**Implementation:**
```javascript
// 1. Lawful basis for processing
const ProcessingBases = {
  CONSENT: 'consent',
  CONTRACT: 'contract',
  LEGAL_OBLIGATION: 'legal',
  VITAL_INTERESTS: 'vital',
  PUBLIC_TASK: 'public',
  LEGITIMATE_INTERESTS: 'legitimate'
};

// 2. Privacy policy and notices
app.get('/privacy', (req, res) => {
  res.render('privacy-policy');
});

// 3. Data Protection Officer (if required)
// Contact: dpo@example.com

// 4. Data Processing Records
const ProcessingRecord = new Schema({
  purpose: String,
  legalBasis: String,
  dataCategories: [String],
  recipients: [String],
  retentionPeriod: String,
  securityMeasures: [String]
});

// 5. Data Breach Notification
async function notifyDataBreach(breachDetails) {
  // Notify supervisory authority within 72 hours
  await notifySupervisoryAuthority(breachDetails);
  
  // Notify affected individuals if high risk
  if (breachDetails.riskLevel === 'high') {
    await notifyAffectedUsers(breachDetails);
  }
  
  // Log breach
  await BreachLog.create({
    date: new Date(),
    description: breachDetails.description,
    affectedUsers: breachDetails.userCount,
    mitigationSteps: breachDetails.mitigation
  });
}

// 6. Privacy by Design
// - Data minimization
// - Encryption by default
// - Pseudonymization where possible
// - Access controls

// 7. Cross-border transfers
// - Use SCCs or adequacy decisions
// - Document transfer mechanisms
```

**Compliance:** GDPR (全体)

**Attribution:** GDPR

---

### ANONYMIZE-DATA: Data Anonymization

**Severity:** Medium

**Vulnerable code:**
```javascript
// Analytics with identifiable data
analytics.track({
  userId: user.id,
  email: user.email, // PII in analytics
  name: user.name,
  action: 'purchase'
});
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Pseudonymize user ID
function pseudonymizeUserId(userId) {
  return crypto
    .createHash('sha256')
    .update(userId + process.env.PSEUDONYM_SALT)
    .digest('hex')
    .substring(0, 16);
}

// Analytics without PII
analytics.track({
  pseudoId: pseudonymizeUserId(user.id),
  // Don't include: email, name, phone
  action: 'purchase',
  category: 'electronics',
  value: 99.99
});

// Aggregate data (fully anonymous)
const stats = await Order.aggregate([
  {
    $group: {
      _id: '$category',
      totalSales: { $sum: '$amount' },
      count: { $sum: 1 }
    }
  }
]);

// K-anonymity for public data
// Ensure at least K users share same quasi-identifiers
function checkKAnonymity(dataset, k = 5) {
  // Group by quasi-identifiers (age, zip, gender)
  const groups = {};
  dataset.forEach(record => {
    const key = `${record.ageRange}-${record.zipPrefix}-${record.gender}`;
    groups[key] = (groups[key] || 0) + 1;
  });
  
  // Check if all groups have at least k members
  return Object.values(groups).every(count => count >= k);
}
```

**Security impact:**
Identifiable data in analytics violates privacy and GDPR.

**Compliance:** GDPR Art. 4(5)

**Attribution:** GDPR

---

### AUDIT-LOG: Implement Audit Logging

**Severity:** Medium

**Vulnerable code:**
```javascript
// No audit trail
app.post('/admin/delete-user', (req, res) => {
  User.deleteOne({ id: req.params.id });
  res.send('Deleted');
});

// Who deleted what? When? No record.
```

**Secure implementation:**
```javascript
const AuditLogSchema = new Schema({
  timestamp: { type: Date, default: Date.now, index: true },
  userId: { type: String, index: true },
  action: { type: String, required: true, index: true },
  resource: String,
  resourceId: String,
  changes: Object, // Before/after
  ipAddress: String,
  userAgent: String,
  result: String // 'success' or 'failure'
});

// Audit middleware
async function auditLog(action, resource) {
  return async (req, res, next) => {
    const originalJson = res.json.bind(res);
    const originalStatus = res.status.bind(res);
    let statusCode = 200;
    
    res.status = function(code) {
      statusCode = code;
      return originalStatus(code);
    };
    
    res.json = async function(data) {
      // Log after action completes
      await AuditLog.create({
        userId: req.user?.id,
        action,
        resource,
        resourceId: req.params.id,
        ipAddress: req.ip,
        userAgent: req.headers['user-agent'],
        result: statusCode < 400 ? 'success' : 'failure',
        changes: req.body
      });
      
      return originalJson(data);
    };
    
    next();
  };
}

// Usage
app.post('/admin/delete-user/:id',
  authenticate,
  authorize('admin'),
  auditLog('delete', 'user'),
  async (req, res) => {
    await User.deleteOne({ id: req.params.id });
    res.send('Deleted');
  }
);

// PII access logging (GDPR requirement)
app.get('/api/users/:id/pii',
  authenticate,
  auditLog('pii-access', 'user'),
  async (req, res) => {
    const user = await User.findById(req.params.id);
    res.json(user);
  }
);

// Query audit logs
app.get('/admin/audit-logs', authenticate, authorize('admin'), async (req, res) => {
  const logs = await AuditLog.find({
    timestamp: { $gte: new Date(req.query.startDate) }
  }).sort({ timestamp: -1 }).limit(100);
  
  res.json(logs);
});
```

**Security impact:**
No audit trail prevents forensics, compliance, and accountability.

**Compliance:** GDPR Art. 30, SOC 2, PCI-DSS

**Attribution:** OWASP, GDPR

---

## 7. CRYPTOGRAPHY

### CRYPTO-STRONG: Use Strong Cryptography

**Severity:** Critical

**Vulnerable code:**
```javascript
// Weak algorithms
const hash = crypto.createHash('md5').update(data).digest('hex');
const hash = crypto.createHash('sha1').update(data).digest('hex');

// ECB mode (insecure)
const cipher = crypto.createCipheriv('aes-256-ecb', key, '');

// Weak key derivation
const key = crypto.createHash('sha256').update(password).digest();
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Strong hashing
const hash = crypto.createHash('sha256').update(data).digest('hex');
const hash = crypto.createHash('sha3-512').update(data).digest('hex');

// Strong encryption (AES-256-GCM)
function encrypt(plaintext, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let ciphertext = cipher.update(plaintext, 'utf8', 'hex');
  ciphertext += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    ciphertext,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}

// Strong key derivation (PBKDF2)
function deriveKey(password, salt) {
  return crypto.pbkdf2Sync(
    password,
    salt,
    100000, // iterations
    32, // key length
    'sha512'
  );
}

// Or use scrypt (even better)
function deriveKeyScrypt(password, salt) {
  return crypto.scryptSync(password, salt, 32, {
    N: 2 ** 14,
    r: 8,
    p: 1
  });
}
```

**Security impact:**
Weak cryptography can be broken, exposing sensitive data.

**Compliance:** OWASP A02:2021 - Cryptographic Failures, CWE-327

**Attribution:** NIST, OWASP

---

### KEY-MANAGE: Secure Key Management

**Severity:** Critical

**Vulnerable code:**
```javascript
// Hardcoded key
const encryptionKey = 'my-secret-key-12345678901234567890';

// Key in code repository
const config = {
  encryption: {
    key: 'abcdef1234567890abcdef1234567890'
  }
};

// Reusing keys
const key = 'same-key-for-everything';
```

**Secure implementation:**
```javascript
// Environment variables
require('dotenv').config();
const encryptionKey = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');

// Key rotation
const keyRotationSchema = new Schema({
  keyId: String,
  key: String, // Encrypted master key
  createdAt: Date,
  rotatedAt: Date,
  active: Boolean
});

async function getActiveKey() {
  const keyRecord = await KeyRotation.findOne({ active: true });
  return Buffer.from(keyRecord.key, 'hex');
}

// Different keys for different purposes
const keys = {
  session: Buffer.from(process.env.SESSION_KEY, 'hex'),
  encryption: Buffer.from(process.env.ENCRYPTION_KEY, 'hex'),
  signing: Buffer.from(process.env.SIGNING_KEY, 'hex')
};

// Use KMS (AWS KMS, Azure Key Vault, etc.)
const AWS = require('aws-sdk');
const kms = new AWS.KMS();

async function encryptWithKMS(plaintext) {
  const params = {
    KeyId: process.env.KMS_KEY_ID,
    Plaintext: plaintext
  };
  
  const result = await kms.encrypt(params).promise();
  return result.CiphertextBlob.toString('base64');
}

async function decryptWithKMS(ciphertext) {
  const params = {
    CiphertextBlob: Buffer.from(ciphertext, 'base64')
  };
  
  const result = await kms.decrypt(params).promise();
  return result.Plaintext.toString('utf8');
}
```

**Security impact:**
Poor key management leads to key exposure and data breaches.

**Compliance:** OWASP A02:2021 - Cryptographic Failures, PCI-DSS

**Attribution:** NIST SP 800-57

---

### RANDOM-SECURE: Use Cryptographically Secure Random

**Severity:** High

**Vulnerable code:**
```javascript
// Math.random() is NOT cryptographically secure
const token = Math.random().toString(36).substring(2);
const sessionId = Math.floor(Math.random() * 1000000);

// Predictable
for (let i = 0; i < 10; i++) {
  console.log(Math.random()); // Can be predicted
}
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Secure random bytes
const token = crypto.randomBytes(32).toString('hex');
const sessionId = crypto.randomBytes(16).toString('base64');

// Secure random integers
function secureRandomInt(min, max) {
  const range = max - min;
  const bytesNeeded = Math.ceil(Math.log2(range) / 8);
  const maxValue = Math.pow(256, bytesNeeded);
  const randomBytes = crypto.randomBytes(bytesNeeded);
  const randomValue = randomBytes.readUIntBE(0, bytesNeeded);
  
  if (randomValue >= maxValue - (maxValue % range)) {
    return secureRandomInt(min, max); // Retry to avoid bias
  }
  
  return min + (randomValue % range);
}

// UUID v4 (uses crypto.randomBytes)
const { v4: uuidv4 } = require('uuid');
const id = uuidv4();

// Generate secure API keys
function generateApiKey() {
  return crypto.randomBytes(32).toString('base64url');
}
```

**Security impact:**
Weak random numbers allow prediction of tokens, session IDs, and cryptographic keys.

**Compliance:** OWASP A02:2021 - Cryptographic Failures, CWE-338

**Attribution:** OWASP

---

### SALT-HASH: Always Salt Hashes

**Severity:** High

**Vulnerable code:**
```javascript
// No salt
const hash = crypto.createHash('sha256').update(password).digest('hex');

// Same salt for all users
const GLOBAL_SALT = 'my-app-salt';
const hash = crypto.createHash('sha256')
  .update(password + GLOBAL_SALT)
  .digest('hex');
```

**Secure implementation:**
```javascript
// bcrypt (includes salt automatically)
const bcrypt = require('bcrypt');
const saltRounds = 12;
const hash = await bcrypt.hash(password, saltRounds);

// Manual salting
function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex');
  return { salt, hash };
}

function verifyPassword(password, salt, storedHash) {
  const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex');
  return hash === storedHash;
}

// Usage
const { salt, hash } = hashPassword('user-password');
await db.users.insert({ username, passwordHash: hash, salt });

// Verify
const user = await db.users.findOne({ username });
const isValid = verifyPassword(inputPassword, user.salt, user.passwordHash);
```

**Security impact:**
Unsalted hashes are vulnerable to rainbow table attacks.

**Compliance:** OWASP A02:2021 - Cryptographic Failures

**Attribution:** OWASP

---

### CERT-VALIDATE: Validate SSL/TLS Certificates

**Severity:** High

**Vulnerable code:**
```javascript
const https = require('https');

// Disabling certificate validation
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'; // Never do this!

// Ignoring certificate errors
const agent = new https.Agent({
  rejectUnauthorized: false
});

fetch(url, { agent });
```

**Secure implementation:**
```javascript
const https = require('https');
const fs = require('fs');

// Proper certificate validation (default)
fetch(url); // Validates certificates

// Custom CA certificates
const agent = new https.Agent({
  ca: fs.readFileSync('./ca-cert.pem'),
  rejectUnauthorized: true // Explicitly enable
});

fetch(url, { agent });

// Certificate pinning
const expectedFingerprint = '59:7A:E6:14:...';

const agent = new https.Agent({
  rejectUnauthorized: true,
  checkServerIdentity: (hostname, cert) => {
    const fingerprint = cert.fingerprint256;
    if (fingerprint !== expectedFingerprint) {
      throw new Error('Certificate fingerprint mismatch');
    }
  }
});

// For internal services only
if (process.env.NODE_ENV === 'development') {
  // Only in development
  const agent = new https.Agent({ rejectUnauthorized: false });
}
```

**Security impact:**
Disabled certificate validation allows man-in-the-middle attacks.

**Compliance:** OWASP A02:2021 - Cryptographic Failures, CWE-295

**Attribution:** OWASP

---

### CRYPTO-DEPRECATE: Avoid Deprecated Cryptography

**Severity:** Medium

**Vulnerable code:**
```javascript
// Deprecated algorithms
crypto.createCipher('des', password); // DES deprecated
crypto.createCipher('rc4', password); // RC4 deprecated
crypto.createHash('md5'); // MD5 deprecated
crypto.createHash('sha1'); // SHA-1 deprecated
```

**Secure implementation:**
```javascript
// Use modern algorithms
crypto.createCipheriv('aes-256-gcm', key, iv); // AES-256
crypto.createHash('sha256'); // SHA-256 or SHA-3
crypto.createHash('sha3-512'); // SHA-3

// TLS versions
const https = require('https');
const server = https.createServer({
  minVersion: 'TLSv1.2', // Minimum TLS 1.2
  maxVersion: 'TLSv1.3', // Prefer TLS 1.3
  ciphers: [
    'TLS_AES_128_GCM_SHA256',
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256'
  ].join(':')
});

// Check Node.js crypto support
const { getCiphers, getHashes } = require('crypto');
console.log('Supported ciphers:', getCiphers());
console.log('Supported hashes:', getHashes());
```

**Security impact:**
Deprecated algorithms have known vulnerabilities.

**Compliance:** OWASP A02:2021 - Cryptographic Failures

**Attribution:** NIST, OWASP

---

### ENCRYPT-REST: Encrypt Data at Rest

**Severity:** High

**Vulnerable code:**
```javascript
// Storing sensitive files unencrypted
fs.writeFileSync('user-data.json', JSON.stringify(userData));

// Database without encryption
const client = new MongoClient(uri);
```

**Secure implementation:**
```javascript
// File encryption
const crypto = require('crypto');

function encryptFile(inputPath, outputPath, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  const input = fs.createReadStream(inputPath);
  const output = fs.createWriteStream(outputPath);
  
  output.write(iv);
  
  input.pipe(cipher).pipe(output);
  
  return new Promise((resolve, reject) => {
    output.on('finish', () => {
      const authTag = cipher.getAuthTag();
      fs.appendFileSync(outputPath, authTag);
      resolve();
    });
    output.on('error', reject);
  });
}

// MongoDB encryption at rest
const client = new MongoClient(uri, {
  autoEncryption: {
    keyVaultNamespace: 'encryption.__keyVault',
    kmsProviders: {
      aws: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
      }
    }
  }
});

// Field-level encryption
const encryptedField = await encryptField(value, encryptionKey);
await db.collection.insertOne({ encryptedField });

// Disk encryption (OS-level)
// Use LUKS (Linux), BitLocker (Windows), FileVault (macOS)
```

**Security impact:**
Unencrypted data at rest is exposed when storage is compromised.

**Compliance:** GDPR Art. 32, PCI-DSS Requirement 3

**Attribution:** NIST SP 800-111

---

## 8. ERROR HANDLING & LOGGING

### ERROR-DISCLOSE: Prevent Information Disclosure

**Severity:** Medium

**Vulnerable code:**
```javascript
// Covered in API-ERROR guideline
```

**Secure implementation:**
```javascript
// See API-ERROR guideline for full implementation
```

**Security impact:**
Error messages leak system information.

**Compliance:** OWASP A04:2021 - Insecure Design, CWE-209

**Attribution:** OWASP

---

### STACK-TRACE: Don't Expose Stack Traces

**Severity:** Medium

**Vulnerable code:**
```javascript
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack // Exposed in production
  });
});
```

**Secure implementation:**
```javascript
app.use((err, req, res, next) => {
  // Log full error server-side
  logger.error({ err, req: { url: req.url, method: req.method } });
  
  // Generic error in production
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' });
  } else {
    // Detailed in development
    res.status(500).json({
      error: err.message,
      stack: err.stack
    });
  }
});
```

**Security impact:**
Stack traces reveal code paths and internal structure.

**Compliance:** OWASP A04:2021 - Insecure Design

**Attribution:** OWASP

---

### ERROR-LOG: Secure Error Logging

**Severity:** Medium

**Vulnerable code:**
```javascript
// Logging to console
console.error(err);

// No error monitoring
```

**Secure implementation:**
```javascript
// Use structured logging
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Error monitoring (Sentry, etc.)
const Sentry = require('@sentry/node');
Sentry.init({ dsn: process.env.SENTRY_DSN });

app.use(Sentry.Handlers.errorHandler());

// Custom error handler
app.use((err, req, res, next) => {
  logger.error({
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    userId: req.user?.id
  });
  
  Sentry.captureException(err);
  
  res.status(500).json({ error: 'Internal server error' });
});
```

**Security impact:**
Poor error logging hinders incident response and debugging.

**Compliance:** Best practice

**Attribution:** OWASP

---

### TRY-CATCH: Proper Exception Handling

**Severity:** Medium

**Vulnerable code:**
```javascript
// Unhandled promise rejection
app.get('/data', async (req, res) => {
  const data = await fetchData(); // Can throw
  res.json(data); // No error handling
});

// process crashes on error
```

**Secure implementation:**
```javascript
// Async error handling
app.get('/data', async (req, res, next) => {
  try {
    const data = await fetchData();
    res.json(data);
  } catch (err) {
    next(err); // Pass to error handler
  }
});

// Or use express-async-errors
require('express-async-errors');

app.get('/data', async (req, res) => {
  const data = await fetchData(); // Errors automatically caught
  res.json(data);
});

// Global handlers
process.on('unhandledRejection', (reason, promise) => {
  logger.error({ reason, promise }, 'Unhandled Rejection');
  Sentry.captureException(reason);
});

process.on('uncaughtException', (err) => {
  logger.error({ err }, 'Uncaught Exception');
  Sentry.captureException(err);
  process.exit(1); // Exit after logging
});
```

**Security impact:**
Unhandled exceptions can crash the application or leak information.

**Compliance:** Best practice

**Attribution:** Node.js documentation

---

## 9. DEPENDENCIES

### NPM-AUDIT: Run npm audit

**Severity:** High

**Vulnerable code:**
```javascript
// Never running security audits
// Using outdated packages
```

**Secure implementation:**
```bash
# Regular audits
npm audit

# Fix vulnerabilities
npm audit fix

# Force fix (may break compatibility)
npm audit fix --force

# CI/CD integration
npm audit --audit-level=high

# Automated dependency updates
npm install -g npm-check-updates
ncu -u
npm install

# GitHub Dependabot
# Enable in repository settings

# Snyk integration
npm install -g snyk
snyk test
snyk monitor
```

**Security impact:**
Known vulnerabilities in dependencies can be exploited.

**Compliance:** OWASP A06:2021 - Vulnerable and Outdated Components

**Attribution:** OWASP

---

### VULN-DEPS: Monitor Vulnerable Dependencies

**Severity:** High

**Vulnerable code:**
```javascript
// package.json with vulnerable versions
{
  "dependencies": {
    "express": "3.0.0", // Outdated, vulnerable
    "lodash": "4.17.15" // Known CVE
  }
}
```

**Secure implementation:**
```json
// package.json with updated versions
{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21"
  },
  "scripts": {
    "audit": "npm audit",
    "audit:fix": "npm audit fix"
  }
}
```

```javascript
// Automated scanning in CI/CD
// .github/workflows/security.yml
/*
name: Security Audit
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm audit --audit-level=moderate
*/

// Runtime monitoring
const requireSafe = require('require-safe');
requireSafe({ throw: true });
```

**Security impact:**
Vulnerable dependencies are common attack vectors.

**Compliance:** OWASP A06:2021 - Vulnerable and Outdated Components

**Attribution:** npm, OWASP

---

### DEP-PIN: Pin Dependency Versions

**Severity:** Medium

**Vulnerable code:**
```json
// package.json with loose versioning
{
  "dependencies": {
    "express": "*", // Any version
    "lodash": "^4.0.0" // Major version changes
  }
}
```

**Secure implementation:**
```json
// package.json with pinned versions
{
  "dependencies": {
    "express": "4.18.2", // Exact version
    "lodash": "4.17.21"
  }
}
```

```bash
# Generate package-lock.json
npm install

# Use exact versions
npm install --save-exact express

# Verify integrity
npm ci # Uses package-lock.json exactly
```

**Security impact:**
Unpinned dependencies can introduce breaking changes or vulnerabilities.

**Compliance:** Best practice

**Attribution:** npm best practices

---

### SUPPLY-CHAIN: Supply Chain Security

**Severity:** High

**Vulnerable code:**
```javascript
// Installing untrusted packages
npm install some-random-package

// No integrity checks
```

**Secure implementation:**
```bash
# Check package before installing
npm view package-name
npm info package-name

# Verify package integrity
npm install --ignore-scripts # Skip install scripts

# Use private registry for internal packages
npm config set registry https://registry.internal.com

# Socket.dev or similar tools
npx socket npm install package-name

# Review package before using
# Check: downloads, last publish, maintainers, repo activity
```

```json
// package.json - specify allowed registries
{
  "publishConfig": {
    "registry": "https://registry.npmjs.org/"
  }
}
```

**Security impact:**
Compromised packages can execute malicious code during installation.

**Compliance:** OWASP A06:2021 - Vulnerable and Outdated Components

**Attribution:** OWASP, npm security best practices

---

## 10. PLATFORM-SPECIFIC

### NODE-EVAL: Avoid eval() and Variants

**Severity:** Critical

**Vulnerable code:**
```javascript
// eval with user input
const userCode = req.body.code;
eval(userCode); // Remote code execution!

// Function constructor
const userFunc = new Function(req.body.function);

// require with user input
const moduleName = req.query.module;
require(moduleName); // Can load any module
```

**Secure implementation:**
```javascript
// Don't execute user code
// Use JSON for data
const data = JSON.parse(req.body.data);

// If custom expressions needed, use safe evaluator
const mathjs = require('mathjs');
const result = mathjs.evaluate(req.body.expression);

// Sandbox with vm2
const { VM } = require('vm2');
const vm = new VM({
  timeout: 1000,
  sandbox: {}
});
const result = vm.run(req.body.code);

// Whitelist for require
const allowedModules = ['fs', 'path', 'crypto'];
if (!allowedModules.includes(moduleName)) {
  throw new Error('Module not allowed');
}
```

**Security impact:**
eval() and variants allow arbitrary code execution.

**Compliance:** OWASP A03:2021 - Injection, CWE-95

**Attribution:** OWASP, Node.js Security Best Practices

---

### NODE-CHILD-PROCESS: Secure child_process Usage

**Severity:** Critical

**Vulnerable code:**
```javascript
// Covered in CMD-INJECT guideline
```

**Secure implementation:**
```javascript
// See CMD-INJECT guideline
```

**Security impact:**
Unsafe child_process usage allows command injection.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** Node.js security best practices

---

### REACT-DANGEROUS: Avoid dangerouslySetInnerHTML

**Severity:** High

**Vulnerable code:**
```javascript
// Covered in DANGEROUS-HTML guideline
```

**Secure implementation:**
```javascript
// See DANGEROUS-HTML guideline
```

**Security impact:**
dangerouslySetInnerHTML bypasses React's XSS protection.

**Compliance:** OWASP A03:2021 - Injection

**Attribution:** React documentation

---

### EXPRESS-BODY: Secure Body Parsing

**Severity:** Medium

**Vulnerable code:**
```javascript
// No size limit
app.use(express.json());

// Allowing any content type
app.use(bodyParser.json({ type: '*/*' }));
```

**Secure implementation:**
```javascript
// Set size limits
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: true, limit: '100kb' }));

// Specific content types only
app.use(express.json({ type: 'application/json' }));

// Parameter limit
app.use(express.urlencoded({ 
  extended: true,
  parameterLimit: 1000
}));

// Use helmet
const helmet = require('helmet');
app.use(helmet());
```

**Security impact:**
Large payloads can cause DoS, incorrect parsing allows attacks.

**Compliance:** Best practice

**Attribution:** Express.js best practices

---

### FILE-ACCESS: Secure File Operations

**Severity:** High

**Vulnerable code:**
```javascript
// Covered in PATH-TRAV guideline
```

**Secure implementation:**
```javascript
// See PATH-TRAV guideline
```

**Security impact:**
Unsafe file access allows path traversal.

**Compliance:** OWASP A01:2021 - Broken Access Control

**Attribution:** OWASP

---

### PROTOTYPE-POLLUT: Prevent Prototype Pollution

**Severity:** High

**Vulnerable code:**
```javascript
// Unsafe object merge
function merge(target, source) {
  for (let key in source) {
    target[key] = source[key]; // Can pollute __proto__
  }
}

// User input merged into object
const config = {};
merge(config, JSON.parse(req.body.config));
// Input: {"__proto__": {"isAdmin": true}}
```

**Secure implementation:**
```javascript
// Safe merge
function merge(target, source) {
  for (let key in source) {
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
        continue; // Skip dangerous keys
      }
      target[key] = source[key];
    }
  }
}

// Use Object.assign with null prototype
const config = Object.create(null);
Object.assign(config, JSON.parse(req.body.config));

// Use libraries with protection
const _ = require('lodash');
_.merge(target, source); // lodash protects against pollution

// Freeze prototypes
Object.freeze(Object.prototype);
Object.freeze(Array.prototype);
```

**Security impact:**
Prototype pollution can bypass security checks and cause RCE.

**Compliance:** OWASP A08:2021 - Software and Data Integrity Failures, CWE-1321

**Attribution:** OWASP, Snyk

---

### DESERIALIZATION: Secure Deserialization

**Severity:** Critical

**Vulnerable code:**
```javascript
// Unsafe deserialization
const serialize = require('node-serialize');
const obj = serialize.unserialize(req.body.data); // RCE risk

// eval in deserialize
const data = req.cookies.session;
eval('obj = ' + data);
```

**Secure implementation:**
```javascript
// Use JSON only
const data = JSON.parse(req.body.data); // Safe, no code execution

// Validate structure
const Joi = require('joi');
const schema = Joi.object({
  username: Joi.string().required(),
  age: Joi.number().integer()
});

const { error, value } = schema.validate(JSON.parse(req.body.data));
if (error) {
  return res.status(400).send('Invalid data');
}

// If binary serialization needed, use safe formats
const msgpack = require('msgpack-lite');
const data = msgpack.decode(buffer);

// Never deserialize untrusted data with node-serialize, pickle, etc.
```

**Security impact:**
Unsafe deserialization allows remote code execution.

**Compliance:** OWASP A08:2021 - Software and Data Integrity Failures, CWE-502

**Attribution:** OWASP Deserialization Cheat Sheet

---

# Expected Good Patterns (Check for Absence)

Beyond flagging vulnerabilities, check whether **expected security patterns are missing**. The absence of good practices is itself a finding.

Based on [OWASP Node.js Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html), [Express.js Security Best Practices](https://expressjs.com/en/advanced/best-practice-security.html), [Helmet.js](https://helmetjs.github.io/), and [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices).

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
