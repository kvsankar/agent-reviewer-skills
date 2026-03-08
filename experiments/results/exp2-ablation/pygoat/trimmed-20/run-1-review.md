# Security & Privacy Review: views.py

## ✅ Strengths
- **HASH-PASSWORD**: Some functions use argon2 for password hashing (good practice)
- **AUTHZ-CHECK**: Some views check `request.user.is_authenticated` before proceeding

## 🔴 Critical Issues (Immediate Fix Required)

#### **SQL-INJECT**: Raw SQL Query Construction with User Input

**Vulnerable code:**
```python
def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    sql_query = "SELECT * FROM introduction_login WHERE user='"+name+"' AND password='"+password+"'"
    val = login.objects.raw(sql_query)
```

**Secure implementation:**
```python
def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    # Use Django ORM or parameterized queries
    try:
        user = login.objects.filter(user=name, password=password).first()
        if user:
            return render(request, 'Lab/SQL/sql_lab.html', {"user1": user.user})
    except Exception:
        return render(request, 'Lab/SQL/sql_lab.html', {"error": "Invalid credentials"})
```

**Security impact:**
Attackers can execute arbitrary SQL commands, potentially accessing, modifying, or deleting sensitive data.

**Compliance:**
OWASP A3 (Injection), CWE-89

---

#### **CODE-INJECT**: Use of eval() on User Input

**Vulnerable code:**
```python
def cmd_lab2(request):
    val = request.POST.get('val')
    try:
        output = eval(val)  # EXTREMELY DANGEROUS!
```

**Secure implementation:**
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
    try:
        node = ast.parse(expression, mode='eval')
        # Implement safe AST evaluation or use a safe expression library
        # Never use eval() on user input
        return "Safe evaluation result"
    except:
        return "Invalid expression"
```

**Security impact:**
Remote code execution - attackers can execute arbitrary Python code on the server.

**Compliance:**
CWE-94, OWASP A3

---

#### **CMD-INJECT**: Command Injection via shell=True

**Vulnerable code:**
```python
def cmd_lab(request):
    domain = request.POST.get('domain')
    command = "dig {}".format(domain)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
```

**Secure implementation:**
```python
import subprocess
import re

def cmd_lab(request):
    domain = request.POST.get('domain')
    # Validate domain format
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "Invalid domain format"})
    
    try:
        # Use argument list instead of shell=True
        result = subprocess.run(['dig', domain], capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Command timed out"
    except Exception:
        output = "Command execution failed"
```

**Security impact:**
Command injection allows attackers to execute arbitrary system commands.

**Compliance:**
CWE-78, OWASP A1

---

#### **INSEC-DESERIALIZE**: Unsafe Pickle Deserialization

**Vulnerable code:**
```python
def insec_des_lab(request):
    token = request.COOKIES.get('token')
    token = base64.b64decode(token)
    admin = pickle.loads(token)  # DANGEROUS!
```

**Secure implementation:**
```python
import json
import jwt
from django.conf import settings

def secure_des_lab(request):
    token = request.COOKIES.get('token')
    try:
        # Use JWT instead of pickle
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        admin_status = payload.get('admin', 0)
    except jwt.InvalidTokenError:
        admin_status = 0
    
    if admin_status == 1:
        return render(request, 'template.html', {"message": "Welcome Admin"})
```

**Security impact:**
Arbitrary code execution through malicious serialized objects.

**Compliance:**
CWE-502, OWASP A8

---

#### **XXE-INJECT**: XML External Entity Processing Enabled

**Vulnerable code:**
```python
def xxe_parse(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)  # DANGEROUS!
    doc = parseString(request.body.decode('utf-8'), parser=parser)
```

**Secure implementation:**
```python
import defusedxml.pulldom as safe_pulldom

def xxe_parse(request):
    try:
        # Use defusedxml to prevent XXE attacks
        doc = safe_pulldom.parseString(request.body.decode('utf-8'))
        # Process XML safely
    except Exception:
        return render(request, 'Lab/XXE/xxe_lab.html', {"error": "Invalid XML"})
```

**Security impact:**
File disclosure, SSRF, denial of service through XML external entity attacks.

**Compliance:**
CWE-611, OWASP A4

---

#### **WEAK-HASH**: MD5 Used for Password Hashing

**Vulnerable code:**
```python
def crypto_failure_lab(request):
    password = md5(password.encode()).hexdigest()
    user = CF_user.objects.filter(username=username, password=password).first()
```

**Secure implementation:**
```python
import bcrypt

def secure_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    
    try:
        user = CF_user.objects.get(username=username)
        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return render(request, 'success.html', {"user": user})
    except CF_user.DoesNotExist:
        pass
    
    return render(request, 'failure.html', {"error": "Invalid credentials"})
```

**Security impact:**
MD5 is cryptographically broken and vulnerable to rainbow table attacks.

**Compliance:**
CWE-327, OWASP A2

---

## ⚠️ Warnings (Should Fix)

#### **RANDOM-SECURE**: Insecure Random Number Generation

**Vulnerable code:**
```python
def Otp(request):
    otpN = randint(100, 999)
```

**Secure implementation:**
```python
import secrets

def Otp(request):
    otpN = secrets.randbelow(900) + 100  # Secure random for OTP
```

**Security impact:**
Predictable OTP generation allows brute force attacks.

**Compliance:**
CWE-330

---

#### **CSRF-PROTECT**: Missing CSRF Protection

**Vulnerable code:**
```python
@csrf_exempt
def xxe_parse(request):  # CSRF protection disabled
```

**Secure implementation:**
```python
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def xxe_parse(request):
    # Handle CSRF token validation properly
```

**Security impact:**
Cross-Site Request Forgery attacks possible.

**Compliance:**
CWE-352, OWASP A1

---

#### **PII-LOG**: Logging Sensitive Information

**Vulnerable code:**
```python
def a10_lab2(request):
    user = request.POST.get("name")
    logging.info(f"{now}:{ip}:{user}")  # Logs username
```

**Secure implementation:**
```python
def secure_login_log(request):
    user = request.POST.get("name")
    # Hash or pseudonymize username for logging
    user_hash = hashlib.sha256(user.encode()).hexdigest()[:8]
    logging.info(f"{now}:{ip}:user_{user_hash}")
```

**Security impact:**
PII exposure in log files violates privacy regulations.

**Compliance:**
GDPR Article 5, CCPA

---

#### **SESSION-SECURE**: Insecure Session Management

**Vulnerable code:**
```python
response.set_cookie('userid', obj.userid, max_age=31449600, samesite=None, secure=False)
```

**Secure implementation:**
```python
response.set_cookie(
    'userid', 
    obj.userid, 
    max_age=3600,  # Shorter session
    samesite='Lax', 
    secure=True,   # HTTPS only
    httponly=True  # Prevent XSS access
)
```

**Security impact:**
Session hijacking and fixation attacks.

**Compliance:**
OWASP A2

---

## 💡 Recommendations (Best Practices)

#### **ERROR-SAFE**: Information Disclosure in Error Messages

**Vulnerable code:**
```python
except:
    return render(request, 'template.html', {"sql_error": sql_query})
```

**Secure implementation:**
```python
except Exception as e:
    logger.error(f"Database error: {str(e)}")
    return render(request, 'template.html', {"error": "An error occurred"})
```

**Security impact:**
Detailed error messages reveal system information to attackers.

---

#### **VALIDATE-INPUT**: Missing Input Validation

**Vulnerable code:**
```python
def xss_lab(request):
    q = request.GET.get('q', '')  # No validation
```

**Secure implementation:**
```python
import re
from django.utils.html import escape

def xss_lab(request):
    q = request.GET.get('q', '')
    # Validate and sanitize input
    if not re.match(r'^[a-zA-Z0-9\s]+$', q):
        q = ''
    q = escape(q)  # HTML escape for output
```

---

#### **DEPS-UPDATE**: Insecure YAML Loading

**Vulnerable code:**
```python
data = yaml.load(file, yaml.Loader)  # Unsafe loader
```

**Secure implementation:**
```python
data = yaml.safe_load(file)  # Use safe_load
```

---

## 📋 Compliance Checklist
- [ ] OWASP Top 10 compliance (Multiple violations found)
- [ ] PII properly protected (Username logging violations)
- [ ] GDPR requirements met (Missing privacy controls)
- [ ] Secrets not in code (Some hardcoded credentials found)
- [ ] Dependencies up to date (Unsafe YAML/XML libraries)

**Critical Priority**: Fix SQL injection, command injection, code injection, and unsafe deserialization immediately. These allow complete system compromise.
