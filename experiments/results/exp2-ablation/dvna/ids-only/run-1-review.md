## Security & Privacy Review: appHandler.js, authHandler.js, server.js

### 🔴 Critical Issues (Immediate Fix Required)

#### **SQL-INJECT**: Raw SQL Query Construction with User Input

**Vulnerable code:**
```javascript
// appHandler.js - userSearch function
var query = "SELECT name,id FROM Users WHERE login='" + req.body.login + "'";
db.sequelize.query(query, {
    model: db.User
}).then(user => {
    // ... rest of function
});
```

**Secure implementation:**
```javascript
// Use parameterized queries
db.User.findAll({
    where: {
        login: req.body.login
    },
    attributes: ['name', 'id']
}).then(user => {
    // ... rest of function
});

// Or with raw query using replacements
var query = "SELECT name,id FROM Users WHERE login = :login";
db.sequelize.query(query, {
    replacements: { login: req.body.login },
    model: db.User
}).then(user => {
    // ... rest of function
});
```

**Security impact:**
Allows attackers to execute arbitrary SQL commands, potentially leading to data theft, data modification, or complete database compromise. Input like `'; DROP TABLE Users; --` could destroy data.

**Compliance:**
Violates OWASP Top 10 #3 (Injection), CWE-89 (SQL Injection)

---

#### **CMD-INJECT**: Command Injection in Ping Function

**Vulnerable code:**
```javascript
// appHandler.js - ping function
exec('ping -c 2 ' + req.body.address, function (err, stdout, stderr) {
    output = stdout + stderr
    res.render('app/ping', {
        output: output
    })
})
```

**Secure implementation:**
```javascript
const { execFile } = require('child_process');

// Use execFile with argument array to prevent injection
execFile('ping', ['-c', '2', req.body.address], function (err, stdout, stderr) {
    if (err && err.code !== 1) { // ping returns 1 for unreachable hosts
        output = 'Ping failed';
    } else {
        output = stdout + stderr;
    }
    res.render('app/ping', {
        output: output
    });
});

// Alternative: Input validation with allowlist
const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
const hostnameRegex = /^[a-zA-Z0-9.-]+$/;

if (!ipRegex.test(req.body.address) && !hostnameRegex.test(req.body.address)) {
    return res.render('app/ping', {
        output: 'Invalid address format'
    });
}
```

**Security impact:**
Allows arbitrary command execution on the server. Input like `8.8.8.8; rm -rf /` could destroy the entire filesystem.

**Compliance:**
Violates OWASP Top 10 #3 (Injection), CWE-78 (Command Injection)

---

#### **CODE-INJECT**: Code Injection via Math Expression Evaluation

**Vulnerable code:**
```javascript
// appHandler.js - calc function
res.render('app/calc', {
    output: mathjs.eval(req.body.eqn)
})
```

**Secure implementation:**
```javascript
const mathjs = require('mathjs');

// Create restricted parser that only allows safe operations
const limited = mathjs.create(mathjs.all, {
    'import': { isFunction: false },
    'function': { isFunction: false },
    'evaluate': { isFunction: false }
});

// Remove dangerous functions
limited.import({
    'import': function () { throw new Error('Function import is disabled') },
    'createUnit': function () { throw new Error('Function createUnit is disabled') },
    'evaluate': function () { throw new Error('Function evaluate is disabled') },
    'parse': function () { throw new Error('Function parse is disabled') },
    'simplify': function () { throw new Error('Function simplify is disabled') },
    'derivative': function () { throw new Error('Function derivative is disabled') }
}, { override: true });

try {
    const result = limited.evaluate(req.body.eqn);
    res.render('app/calc', {
        output: result
    });
} catch (error) {
    res.render('app/calc', {
        output: 'Invalid mathematical expression'
    });
}
```

**Security impact:**
Math.js eval can execute arbitrary JavaScript code, potentially leading to remote code execution and full server compromise.

**Compliance:**
Violates OWASP Top 10 #3 (Injection), CWE-94 (Code Injection)

---

#### **DESERIALIZATION**: Unsafe Deserialization of User Data

**Vulnerable code:**
```javascript
// appHandler.js - bulkProductsLegacy function
var products = serialize.unserialize(req.files.products.data.toString('utf8'))
```

**Secure implementation:**
```javascript
// Replace with JSON parsing and validation
try {
    const productsData = JSON.parse(req.files.products.data.toString('utf8'));
    
    // Validate structure
    if (!Array.isArray(productsData)) {
        throw new Error('Invalid format: expected array');
    }
    
    const products = productsData.map(product => {
        // Validate required fields
        if (!product.name || !product.code) {
            throw new Error('Missing required fields');
        }
        
        return {
            name: String(product.name).trim(),
            code: String(product.code).trim(),
            tags: String(product.tags || '').trim(),
            description: String(product.description || '').trim()
        };
    });
    
    // Process products...
} catch (error) {
    res.render('app/bulkproducts', {
        messages: {danger: 'Invalid file format'}, 
        legacy: true
    });
    return;
}
```

**Security impact:**
Node-serialize can execute arbitrary code during deserialization, leading to remote code execution and full server compromise.

**Compliance:**
Violates OWASP Top 10 #8 (Insecure Deserialization), CWE-502 (Deserialization Vulnerability)

---

#### **XML-EXTERNAL-ENTITY**: XXE Vulnerability in XML Processing

**Vulnerable code:**
```javascript
// appHandler.js - bulkProducts function
var products = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), {noent:true,noblanks:true})
```

**Secure implementation:**
```javascript
// Disable entity processing to prevent XXE
var products = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), {
    noent: false,  // Disable entity processing
    noblanks: true,
    dtdload: false,  // Disable DTD loading
    dtdvalid: false  // Disable DTD validation
});

// Alternative: Use a safer XML parser
const xml2js = require('xml2js');
const parser = new xml2js.Parser({
    explicitArray: false,
    ignoreAttrs: true,
    explicitRoot: false
});

parser.parseString(req.files.products.data.toString('utf8'), (err, result) => {
    if (err) {
        res.render('app/bulkproducts', {
            messages: {danger: 'Invalid XML format'}, 
            legacy: false
        });
        return;
    }
    // Process result...
});
```

**Security impact:**
XXE attacks can read arbitrary files, perform SSRF attacks, or cause denial of service. Attackers could access `/etc/passwd`, internal services, or exhaust server resources.

**Compliance:**
Violates OWASP Top 10 #4 (XXE), CWE-611 (XML External Entity Reference)

---

#### **WEAK-RESET-TOKEN**: Predictable Password Reset Token

**Vulnerable code:**
```javascript
// authHandler.js - resetPw and resetPwSubmit functions
if (req.query.token == md5(req.query.login)) {
    // Allow password reset
}
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Generate cryptographically secure reset token
function generateResetToken() {
    return crypto.randomBytes(32).toString('hex');
}

// Store token with expiration in database
function createPasswordReset(userId, login) {
    const token = generateResetToken();
    const expiry = new Date(Date.now() + 3600000); // 1 hour
    
    return db.PasswordReset.create({
        userId: userId,
        token: crypto.createHash('sha256').update(token).digest('hex'), // Store hashed
        expiry: expiry
    }).then(() => token); // Return plain token for email
}

// Validate token
function validateResetToken(login, providedToken) {
    const hashedToken = crypto.createHash('sha256').update(providedToken).digest('hex');
    
    return db.PasswordReset.findOne({
        where: {
            token: hashedToken,
            expiry: { [Op.gt]: new Date() }
        },
        include: [{
            model: db.User,
            where: { login: login }
        }]
    });
}
```

**Security impact:**
MD5 of username is easily predictable, allowing attackers to reset any user's password without access to their email.

**Compliance:**
Violates OWASP Top 10 #2 (Broken Authentication), CWE-330 (Weak Random Number Generator)

---

### ⚠️ Warnings (Should Fix)

#### **OPEN-REDIRECT**: Unvalidated Redirect URL

**Vulnerable code:**
```javascript
// appHandler.js - redirect function
module.exports.redirect = function (req, res) {
    if (req.query.url) {
        res.redirect(req.query.url)
    } else {
        res.send('invalid redirect url')
    }
}
```

**Secure implementation:**
```javascript
// Allowlist approach
const allowedDomains = ['example.com', 'subdomain.example.com'];

function isAllowedRedirect(url) {
    try {
        const parsedUrl = new URL(url);
        return allowedDomains.includes(parsedUrl.hostname);
    } catch {
        return false;
    }
}

module.exports.redirect = function (req, res) {
    if (req.query.url && isAllowedRedirect(req.query.url)) {
        res.redirect(req.query.url);
    } else {
        res.status(400).send('Invalid redirect URL');
    }
}

// Or relative URL only approach
function isRelativeUrl(url) {
    return url && url.startsWith('/') && !url.startsWith('//');
}

module.exports.redirect = function (req, res) {
    if (req.query.url && isRelativeUrl(req.query.url)) {
        res.redirect(req.query.url);
    } else {
        res.status(400).send('Invalid redirect URL');
    }
}
```

**Security impact:**
Allows phishing attacks by redirecting users to malicious domains that appear to come from the trusted application.

**Compliance:**
Violates OWASP Top 10 #10 (Insufficient Logging & Monitoring), CWE-601 (Open Redirect)

---

#### **WEAK-SESSION-SECRET**: Hardcoded Weak Session Secret

**Vulnerable code:**
```javascript
// server.js
app.use(session({
  secret: 'keyboard cat',
  resave: true,
  saveUninitialized: true,
  cookie: { secure: false }
}))
```

**Secure implementation:**
```javascript
// Use environment variable with strong secret
app.use(session({
    secret: process.env.SESSION_SECRET || crypto.randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: false,
    cookie: { 
        secure: process.env.NODE_ENV === 'production', // HTTPS only in production
        httpOnly: true, // Prevent XSS
        maxAge: 3600000, // 1 hour
        sameSite: 'strict' // CSRF protection
    }
}));

// Generate and log a secure secret for production
if (!process.env.SESSION_SECRET) {
    console.warn('WARNING: SESSION_SECRET not set. Generate one with: node -e "console.log(require(\'crypto\').randomBytes(64).toString(\'hex\'))"');
}
```

**Security impact:**
Weak session secrets allow session hijacking and impersonation attacks. The secret 'keyboard cat' is easily guessable.

**Compliance:**
Violates OWASP Top 10 #2 (Broken Authentication), CWE-798 (Use of Hard-coded Credentials)

---

#### **INSECURE-COOKIES**: Missing Security Flags on Session Cookies

**Vulnerable code:**
```javascript
// server.js
cookie: { secure: false }
```

**Secure implementation:**
```javascript
cookie: { 
    secure: process.env.NODE_ENV === 'production', // HTTPS only in production
    httpOnly: true, // Prevent XSS access to cookies
    maxAge: 3600000, // 1 hour expiration
    sameSite: 'strict' // Prevent CSRF
}
```

**Security impact:**
Insecure cookies can be intercepted over HTTP connections and accessed by XSS attacks.

**Compliance:**
Violates OWASP Top 10 #7 (XSS), CWE-614 (Sensitive Cookie Without 'Secure' Attribute)

---

#### **ERROR-DISCLOSE**: Information Disclosure in Error Messages

**Vulnerable code:**
```javascript
// appHandler.js - modifyProductSubmit
.catch(err => {
    output = {
        product: product
    }
    req.flash('danger',err)  // Exposes full error
    res.render('app/modifyproduct', {
        output: output
    })
})
```

**Secure implementation:**
```javascript
.catch(err => {
    console.error('Product modification error:', err); // Log detailed error
    output = {
        product: product
    }
    req.flash('danger', 'Unable to save product. Please try again.');
    res.render('app/modifyproduct', {
        output: output
    })
})
```

**Security impact:**
Detailed error messages can reveal database structure, file paths, and internal system information to attackers.

**Compliance:**
Violates OWASP Top 10 #3 (Sensitive Data Exposure), CWE-209 (Information Exposure Through Error Messages)

---

### 💡 Recommendations (Best Practices)

#### **MISSING-VALIDATION-LIB**: No Input Validation Framework

**Current state:** Input validation is inconsistent and ad-hoc across the application.

**Recommended implementation:**
```javascript
const Joi = require('joi');

// Define validation schemas
const userSearchSchema = Joi.object({
    login: Joi.string().alphanum().min(3).max(30).required()
});

const productSchema = Joi.object({
    name: Joi.string().min(1).max(100).required(),
    code: Joi.string().alphanum().min(1).max(20).required(),
    description: Joi.string().max(500).optional(),
    tags: Joi.string().max(200).optional()
});

// Validation middleware
function validateBody(schema) {
    return (req, res, next) => {
        const { error } = schema.validate(req.body);
        if (error) {
            req.flash('danger', 'Invalid input data');
            return res.redirect('back');
        }
        next();
    };
}

// Use in routes
module.exports.userSearch = [
    validateBody(userSearchSchema),
    function (req, res) {
        // Safe to use req.body.login
    }
];
```

**Security impact:**
Comprehensive input validation prevents many injection attacks and ensures data integrity.

**Compliance:**
Addresses OWASP Top 10 #3 (Injection), multiple CWE categories

---

#### **MISSING-AUTHZ-CHECK**: Missing Authorization Checks

**Current state:** Many functions lack proper authorization verification beyond authentication.

**Recommended implementation:**
```javascript
// Authorization middleware
function requireOwnership(req, res, next) {
    // Check if user owns the resource
    if (req.body.id && req.body.id !== req.user.id && !req.user.isAdmin) {
        req.flash('danger', 'Unauthorized access');
        return res.redirect('/app');
    }
    next();
}

function requireAdmin(req, res, next) {
    if (!req.user.isAdmin) {
        req.flash('danger', 'Admin access required');
        return res.redirect('/app');
    }
    next();
}

// Apply to sensitive operations
module.exports.userEditSubmit = [
    authHandler.isAuthenticated,
    requireOwnership,
    function(req, res) { /* ... */ }
];
```

**Security impact:**
Prevents privilege escalation and unauthorized access to sensitive operations.

**Compliance:**
Addresses OWASP Top 10 #5 (Broken Access Control), CWE-862 (Missing Authorization)

---

#### **MISSING-SECURITY-HEADERS**: No Security Headers Middleware

**Current state:** Application lacks security headers protection.

**Recommended implementation:**
```javascript
const helmet = require('helmet');

// Add security headers
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            scriptSrc: ["'self'"],
            imgSrc: ["'self'", "data:", "https:"]
        }
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    }
}));
```

**Security impact:**
Security headers provide defense-in-depth against XSS, clickjacking, and other client-side attacks.

**Compliance:**
Addresses OWASP Top 10 #7 (XSS), multiple security best practices

---

### 📋 Compliance Checklist

- [ ] **OWASP Top 10 compliance** - Multiple critical violations (Injection, Broken Auth, XSS, XXE, Broken Access Control)
- [ ] **PII properly protected** - No evidence of PII handling controls
- [ ] **GDPR requirements met** - No privacy controls implemented
- [ ] **Secrets not in code** - Session secret hardcoded, no environment variables
- [ ] **Dependencies up to date** - Several outdated packages with known vulnerabilities
- [ ] **Input validation** - Minimal validation across the application
- [ ] **Output encoding** - Templates may be vulnerable to XSS
- [ ] **Authentication security** - Weak password reset mechanism
- [ ] **Session management** - Insecure session configuration
- [ ] **Error handling** - Information disclosure in error messages

**Overall Security Posture:** 🔴 **CRITICAL** - This application has multiple severe vulnerabilities that could lead to complete system compromise. Immediate remediation required before any production deployment.
