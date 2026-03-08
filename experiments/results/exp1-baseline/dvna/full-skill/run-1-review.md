## Security & Privacy Review: Node.js Application

### ✅ Strengths
- **PASSWORD-HASH**: Uses bcrypt for password hashing with salt generation
- **AUTHZ-CHECK**: Has authentication middleware to protect routes

### 🔴 Critical Issues (Immediate Fix Required)

#### SQL-INJECT: SQL Injection in User Search

**Vulnerable code:**
```javascript
// appHandler.js:8-9
var query = "SELECT name,id FROM Users WHERE login='" + req.body.login + "'";
db.sequelize.query(query, {
    model: db.User
}).then(user => {
```

**Secure implementation:**
```javascript
// Use parameterized queries
db.User.findOne({
    where: {
        login: req.body.login
    },
    attributes: ['name', 'id']
}).then(user => {

// Or with Sequelize raw query
db.sequelize.query(
    "SELECT name,id FROM Users WHERE login = :login",
    {
        replacements: { login: req.body.login },
        model: db.User
    }
).then(user => {
```

**Security impact:**
Allows attackers to execute arbitrary SQL queries, potentially accessing sensitive data, modifying records, or bypassing authentication.

**Compliance:** OWASP A03:2021 - Injection, CWE-89

---

#### CMD-INJECT: Command Injection in Ping Function

**Vulnerable code:**
```javascript
// appHandler.js:36
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

// Use execFile instead of exec to avoid shell interpretation
execFile('ping', ['-c', '2', req.body.address], (err, stdout, stderr) => {
    output = stdout + stderr;
    res.render('app/ping', {
        output: output
    });
});

// Or validate input strictly
const validIpRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/;
if (!validIpRegex.test(req.body.address)) {
    return res.status(400).send('Invalid IP address');
}
```

**Security impact:**
Allows remote code execution on the server through command injection. Attackers could execute arbitrary system commands.

**Compliance:** OWASP A03:2021 - Injection, CWE-78

---

#### DESERIALIZATION: Unsafe Deserialization in Bulk Products

**Vulnerable code:**
```javascript
// appHandler.js:185
var products = serialize.unserialize(req.files.products.data.toString('utf8'))
```

**Secure implementation:**
```javascript
// Use JSON instead of node-serialize
try {
    var products = JSON.parse(req.files.products.data.toString('utf8'));
    
    // Validate structure
    const Joi = require('joi');
    const productSchema = Joi.array().items(Joi.object({
        name: Joi.string().required(),
        code: Joi.string().required(),
        tags: Joi.string(),
        description: Joi.string()
    }));
    
    const { error, value } = productSchema.validate(products);
    if (error) {
        return res.render('app/bulkproducts', {
            messages: { danger: 'Invalid product data format' },
            legacy: true
        });
    }
    products = value;
} catch (err) {
    return res.render('app/bulkproducts', {
        messages: { danger: 'Invalid JSON format' },
        legacy: true
    });
}
```

**Security impact:**
node-serialize allows remote code execution through object deserialization. Attackers can inject malicious code that executes when the object is unserialized.

**Compliance:** OWASP A08:2021 - Software and Data Integrity Failures, CWE-502

---

#### CODE-INJECT: Code Injection via Math Expression

**Vulnerable code:**
```javascript
// appHandler.js:169-170
res.render('app/calc', {
    output: mathjs.eval(req.body.eqn)
})
```

**Secure implementation:**
```javascript
// Restrict mathjs to safe operations only
const math = require('mathjs');

const limitedEvaluate = math.evaluate;
math.import({
    'import':     function () { throw new Error('Function import is disabled') },
    'createUnit': function () { throw new Error('Function createUnit is disabled') },
    'evaluate':   function () { throw new Error('Function evaluate is disabled') },
    'parse':      function () { throw new Error('Function parse is disabled') },
    'simplify':   function () { throw new Error('Function simplify is disabled') },
    'derivative': function () { throw new Error('Function derivative is disabled') }
}, { override: true });

try {
    // Only allow basic math operations
    const expr = req.body.eqn.replace(/[^0-9+\-*/().\s]/g, '');
    const result = math.evaluate(expr);
    res.render('app/calc', { output: result });
} catch (error) {
    res.render('app/calc', { output: 'Invalid expression' });
}
```

**Security impact:**
mathjs.eval() can potentially execute dangerous functions or access Node.js internals, leading to code injection.

**Compliance:** OWASP A03:2021 - Injection, CWE-94

---

#### CRED-STORE: Hardcoded Session Secret

**Vulnerable code:**
```javascript
// server.js:21-22
app.use(session({
  secret: 'keyboard cat',
```

**Secure implementation:**
```javascript
// Use environment variables for secrets
require('dotenv').config();

app.use(session({
    secret: process.env.SESSION_SECRET || (() => {
        if (process.env.NODE_ENV === 'production') {
            throw new Error('SESSION_SECRET environment variable is required in production');
        }
        return require('crypto').randomBytes(32).toString('hex');
    })(),
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        sameSite: 'strict',
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
}));
```

**Security impact:**
Hardcoded secrets allow attackers to forge sessions and impersonate users.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures, CWE-798

---

### ⚠️ Warnings (Should Fix)

#### CRYPTO-STRONG: Weak Password Reset Token

**Vulnerable code:**
```javascript
// authHandler.js:47, 70
if (req.query.token == md5(req.query.login)) {
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Generate secure random token
function generateResetToken() {
    return crypto.randomBytes(32).toString('hex');
}

// Store tokens with expiration in database
const resetToken = generateResetToken();
const expiresAt = new Date(Date.now() + 60 * 60 * 1000); // 1 hour

await db.PasswordReset.create({
    userId: user.id,
    token: crypto.createHash('sha256').update(resetToken).digest('hex'),
    expiresAt: expiresAt
});

// Verify token
const hashedToken = crypto.createHash('sha256').update(req.query.token).digest('hex');
const resetRecord = await db.PasswordReset.findOne({
    where: {
        token: hashedToken,
        expiresAt: { [Op.gt]: new Date() }
    }
});
```

**Security impact:**
MD5 is cryptographically broken and predictable tokens allow password reset attacks.

**Compliance:** OWASP A02:2021 - Cryptographic Failures, CWE-327

---

#### TIMING-ATTACK: Timing Attack in Token Comparison

**Vulnerable code:**
```javascript
// authHandler.js:47
if (req.query.token == md5(req.query.login)) {
```

**Secure implementation:**
```javascript
const crypto = require('crypto');

// Constant-time comparison
function secureCompare(a, b) {
    if (a.length !== b.length) {
        return false;
    }
    return crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
}

const expectedToken = crypto.createHash('sha256').update(user.login + user.salt).digest('hex');
if (secureCompare(req.query.token, expectedToken)) {
    // Valid token
}
```

**Security impact:**
Timing differences can reveal information about valid tokens through side-channel attacks.

**Compliance:** CWE-208

---

#### SESSION-SECURE: Insecure Session Configuration

**Vulnerable code:**
```javascript
// server.js:21-26
app.use(session({
  secret: 'keyboard cat',
  resave: true,
  saveUninitialized: true,
  cookie: { secure: false }
}))
```

**Secure implementation:**
```javascript
// Already shown in CRED-STORE example above
```

**Security impact:**
Insecure session settings allow session hijacking and fixation attacks.

**Compliance:** OWASP A07:2021 - Identification and Authentication Failures

---

#### XXE-ATTACK: XML External Entity Vulnerability

**Vulnerable code:**
```javascript
// appHandler.js:196-197
var products = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), {noent:true,noblanks:true})
```

**Secure implementation:**
```javascript
// Disable entity processing
var products = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), {
    noent: false,    // Disable entity processing
    nonet: true,     // Disable network access
    noblanks: true
});

// Better: Use JSON instead of XML
```

**Security impact:**
XXE attacks can lead to file disclosure, SSRF, or denial of service.

**Compliance:** OWASP A05:2021 - Security Misconfiguration, CWE-611

---

### 💡 Recommendations (Best Practices)

#### MISSING-HELMET: No Security Headers

**Recommendation:**
```javascript
// server.js - Add after other middleware
const helmet = require('helmet');

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
        includeSubDomains: true
    }
}));
```

**Security impact:**
Missing security headers leave the application vulnerable to XSS, clickjacking, and other attacks.

---

#### MISSING-RATE-LIMIT: No Rate Limiting

**Recommendation:**
```javascript
const rateLimit = require('express-rate-limit');

// General rate limiting
app.use(rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // requests per window
}));

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5 // login attempts
});

app.use('/login', authLimiter);
app.use('/forgotpw', authLimiter);
```

**Security impact:**
No rate limiting allows brute force attacks and DoS.

---

#### MISSING-VALIDATION: No Input Validation

**Recommendation:**
```javascript
const { body, validationResult } = require('express-validator');

// Add validation middleware
app.post('/app/usersearch',
    body('login').trim().isLength({ min: 1, max: 50 }).escape(),
    (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        // Continue with handler
    }
);
```

**Security impact:**
Lack of input validation increases attack surface for injection attacks.

---

### 📋 Compliance Checklist
- [ ] ❌ OWASP Top 10 compliance (Multiple A03 injection issues)
- [ ] ❌ Session security (Weak secret, insecure cookies)
- [ ] ❌ Cryptographic security (MD5 usage, weak tokens)
- [ ] ❌ Input validation (Multiple injection points)
- [ ] ❌ Error handling (May leak stack traces)
- [ ] ❌ Dependencies security (Need npm audit)

**Priority Action Items:**
1. Fix SQL injection in userSearch immediately
2. Fix command injection in ping function
3. Remove unsafe deserialization
4. Implement proper session security
5. Add comprehensive input validation
6. Implement security headers and rate limiting
