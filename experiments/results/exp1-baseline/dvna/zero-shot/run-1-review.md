# Security and Code Quality Review

## Critical Security Issues

### SQL-INJECT
**Severity:** CRITICAL
**Impact:** Complete database compromise, data theft, unauthorized access

**Problematic Code:**
```javascript
// appHandler.js:9-10
var query = "SELECT name,id FROM Users WHERE login='" + req.body.login + "'";
db.sequelize.query(query, {
    model: db.User
})
```

**Improved Code:**
```javascript
// Use parameterized queries
db.User.findOne({
    where: {
        login: req.body.login
    },
    attributes: ['name', 'id']
}).then(user => {
    if (user) {
        var output = {
            user: {
                name: user.name,
                id: user.id
            }
        }
        // rest of the logic...
    }
})
```

### CMD-INJECT
**Severity:** CRITICAL  
**Impact:** Remote code execution, server compromise

**Problematic Code:**
```javascript
// appHandler.js:33-38
exec('ping -c 2 ' + req.body.address, function (err, stdout, stderr) {
    output = stdout + stderr
    res.render('app/ping', {
        output: output
    })
})
```

**Improved Code:**
```javascript
const { spawn } = require('child_process');

// Validate input format (IP address or hostname)
const addressRegex = /^[a-zA-Z0-9.-]+$/;
if (!addressRegex.test(req.body.address)) {
    return res.render('app/ping', {
        output: 'Invalid address format'
    });
}

// Use spawn with argument array instead of string concatenation
const ping = spawn('ping', ['-c', '2', req.body.address]);
let output = '';

ping.stdout.on('data', (data) => {
    output += data;
});

ping.stderr.on('data', (data) => {
    output += data;
});

ping.on('close', (code) => {
    res.render('app/ping', {
        output: output
    });
});
```

### UNSAFE-DESERIAL
**Severity:** CRITICAL
**Impact:** Remote code execution through object deserialization

**Problematic Code:**
```javascript
// appHandler.js:185-186
var products = serialize.unserialize(req.files.products.data.toString('utf8'))
```

**Improved Code:**
```javascript
// Use JSON.parse instead of node-serialize
try {
    var products = JSON.parse(req.files.products.data.toString('utf8'));
    
    // Validate the structure
    if (!Array.isArray(products)) {
        throw new Error('Invalid format: expected array');
    }
    
    products.forEach((product, index) => {
        if (!product.name || !product.code) {
            throw new Error(`Invalid product at index ${index}: missing required fields`);
        }
    });
} catch (err) {
    res.render('app/bulkproducts', {
        messages: { danger: 'Invalid file format' },
        legacy: true
    });
    return;
}
```

### XXE-ATTACK
**Severity:** CRITICAL
**Impact:** Local file disclosure, SSRF, DoS

**Problematic Code:**
```javascript
// appHandler.js:202
var products = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), {noent:true,noblanks:true})
```

**Improved Code:**
```javascript
// Disable external entity processing
var products = libxmljs.parseXmlString(req.files.products.data.toString('utf8'), {
    noent: false,     // Disable entity processing
    nonet: true,      // Disable network access
    noblanks: true
});
```

### OPEN-REDIRECT
**Severity:** HIGH
**Impact:** Phishing attacks, credential theft

**Problematic Code:**
```javascript
// appHandler.js:148-153
module.exports.redirect = function (req, res) {
    if (req.query.url) {
        res.redirect(req.query.url)
    } else {
        res.send('invalid redirect url')
    }
}
```

**Improved Code:**
```javascript
module.exports.redirect = function (req, res) {
    if (req.query.url) {
        // Validate that URL is relative or from allowed domains
        const allowedDomains = ['example.com', 'app.example.com'];
        const url = req.query.url;
        
        // Allow relative URLs starting with /
        if (url.startsWith('/')) {
            return res.redirect(url);
        }
        
        // Check if absolute URL is from allowed domain
        try {
            const parsedUrl = new URL(url);
            if (allowedDomains.includes(parsedUrl.hostname)) {
                return res.redirect(url);
            }
        } catch (e) {
            // Invalid URL
        }
        
        res.send('Redirect not allowed');
    } else {
        res.send('invalid redirect url');
    }
}
```

### CODE-INJECT
**Severity:** HIGH
**Impact:** Server-side code execution through math expressions

**Problematic Code:**
```javascript
// appHandler.js:155-163
module.exports.calc = function (req, res) {
    if (req.body.eqn) {
        res.render('app/calc', {
            output: mathjs.eval(req.body.eqn)
        })
    }
}
```

**Improved Code:**
```javascript
module.exports.calc = function (req, res) {
    if (req.body.eqn) {
        try {
            // Create a restricted math.js instance
            const math = mathjs.create({
                functionScope: 'limited',
                objectScope: 'limited'
            });
            
            // Validate input - only allow basic math operations
            const allowedChars = /^[0-9+\-*/.() ]+$/;
            if (!allowedChars.test(req.body.eqn)) {
                throw new Error('Invalid characters in equation');
            }
            
            const result = math.evaluate(req.body.eqn);
            res.render('app/calc', {
                output: result
            });
        } catch (err) {
            res.render('app/calc', {
                output: 'Invalid equation'
            });
        }
    } else {
        res.render('app/calc', {
            output: 'Enter a valid math string like (3+3)*2'
        });
    }
}
```

## High Security Issues

### WEAK-RESET-TOKEN
**Severity:** HIGH
**Impact:** Account takeover through predictable password reset tokens

**Problematic Code:**
```javascript
// authHandler.js:31, 49
if (req.query.token == md5(req.query.login)) {
```

**Improved Code:**
```javascript
const crypto = require('crypto');

// When generating reset token (in forgotPw function)
const resetToken = crypto.randomBytes(32).toString('hex');
const resetExpiry = new Date(Date.now() + 3600000); // 1 hour expiry

user.resetToken = resetToken;
user.resetExpiry = resetExpiry;
await user.save();

// When validating reset token
if (req.query.token === user.resetToken && new Date() < user.resetExpiry) {
    // Valid token
} else {
    req.flash('danger', "Invalid or expired reset token");
    res.redirect('/forgotpw');
}
```

### HARDCODED-SECRET
**Severity:** HIGH
**Impact:** Session hijacking, authentication bypass

**Problematic Code:**
```javascript
// server.js:24-29
app.use(session({
  secret: 'keyboard cat',
  resave: true,
  saveUninitialized: true,
  cookie: { secure: false }
}))
```

**Improved Code:**
```javascript
app.use(session({
  secret: process.env.SESSION_SECRET || crypto.randomBytes(64).toString('hex'),
  resave: false,
  saveUninitialized: false,
  cookie: { 
    secure: process.env.NODE_ENV === 'production', // HTTPS only in production
    httpOnly: true,
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}))
```

## Medium Security Issues

### INFO-DISCLOSURE
**Severity:** MEDIUM
**Impact:** Information leakage through error messages

**Problematic Code:**
```javascript
// appHandler.js:87-96
.catch(err => {
    output = {
        product: product
    }
    req.flash('danger',err)
    res.render('app/modifyproduct', {
        output: output
    })
})
```

**Improved Code:**
```javascript
.catch(err => {
    console.error('Product modification error:', err); // Log full error
    output = {
        product: product
    }
    req.flash('danger', 'Unable to save product. Please try again.')
    res.render('app/modifyproduct', {
        output: output
    })
})
```

### MISSING-VALIDATION
**Severity:** MEDIUM  
**Impact:** Data integrity issues, potential XSS

**Problematic Code:**
```javascript
// appHandler.js:78-82
product.code = req.body.code
product.name = req.body.name
product.description = req.body.description
product.tags = req.body.tags
```

**Improved Code:**
```javascript
// Validate and sanitize inputs
const validator = require('validator');

if (!req.body.code || !validator.isLength(req.body.code, {min: 1, max: 50})) {
    req.flash('danger', 'Product code is required and must be 1-50 characters');
    return res.render('app/modifyproduct', {output: {product: product}});
}

if (!req.body.name || !validator.isLength(req.body.name, {min: 1, max: 100})) {
    req.flash('danger', 'Product name is required and must be 1-100 characters');
    return res.render('app/modifyproduct', {output: {product: product}});
}

product.code = validator.escape(req.body.code);
product.name = validator.escape(req.body.name);
product.description = validator.escape(req.body.description || '');
product.tags = validator.escape(req.body.tags || '');
```

### DEPRECATED-FIND
**Severity:** LOW
**Impact:** Future compatibility issues

**Problematic Code:**
```javascript
// Multiple locations using deprecated Sequelize methods
db.Product.find({
    where: {
        'id': req.query.id
    }
})
```

**Improved Code:**
```javascript
// Use findOne instead of deprecated find
db.Product.findOne({
    where: {
        'id': req.query.id
    }
})
```

## Summary

This application contains **4 critical vulnerabilities** that allow remote code execution and complete system compromise. The most urgent fixes needed are:

1. Replace raw SQL with parameterized queries
2. Fix command injection in ping functionality  
3. Remove unsafe deserialization
4. Disable XML external entities
5. Implement proper redirect validation
6. Secure the math expression evaluator
7. Use cryptographically secure password reset tokens
8. Move session secret to environment variables

All critical and high-severity issues should be addressed immediately before deploying to production.
