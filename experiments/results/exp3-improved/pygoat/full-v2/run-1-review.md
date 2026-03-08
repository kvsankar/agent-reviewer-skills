## Security & Privacy Review: views.py

### ✅ Strengths
- **IMPORT-GOOD**: Uses some secure libraries like `argon2` for password hashing
- **AUTH-DECORATOR**: Has an authentication decorator function implemented

### 🔴 Critical Issues (Immediate Fix Required)

#### SQL-INJECT: Direct SQL Query Construction with User Input

**Vulnerable code:**
```python
def sql_lab(request):
    name=request.POST.get('name')
    password=request.POST.get('pass')
    if name:
        sql_query = "SELECT * FROM introduction_login WHERE user='"+name+"' AND password='"+password+"'"
        val=login.objects.raw(sql_query)
```

**Secure implementation:**
```python
def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    if name:
        # Use parameterized queries
        val = login.objects.filter(user=name, password=password)
        # Or if raw SQL is needed:
        # val = login.objects.raw("SELECT * FROM introduction_login WHERE user=%s AND password=%s", [name, password])
```

**Security impact:**
Attackers can execute arbitrary SQL commands, potentially accessing, modifying, or deleting database contents.

**Compliance:**
OWASP A3 (Injection), CWE-89

---

#### CODE-INJECT: Using eval() on User Input

**Vulnerable code:**
```python
def cmd_lab2(request):
    val=request.POST.get('val')
    try:
        output = eval(val)  # DANGEROUS!
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
        # Implement safe AST evaluation with whitelist
        return eval_node(node.body)
    except:
        raise ValueError("Invalid expression")

def cmd_lab2(request):
    val = request.POST.get('val')
    try:
        output = safe_eval(val)
    except:
        output = "Invalid expression"
```

**Security impact:**
Arbitrary code execution on the server, complete system compromise.

**Compliance:**
OWASP A1, CWE-94

---

#### CMD-INJECT: Command Injection via subprocess

**Vulnerable code:**
```python
def cmd_lab(request):
    domain=request.POST.get('domain')
    if(os=='win'):
        command="nslookup {}".format(domain)
    else:
        command = "dig {}".format(domain)
    process = subprocess.Popen(command, shell=True, ...)
```

**Secure implementation:**
```python
import re
import subprocess

def cmd_lab(request):
    domain = request.POST.get('domain', '')
    
    # Validate domain format
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "Invalid domain format"})
    
    os_type = request.POST.get('os')
    
    if os_type == 'win':
        command = ["nslookup", domain]
    else:
        command = ["dig", domain]
    
    try:
        process = subprocess.run(
            command,
            shell=False,  # Never use shell=True
            capture_output=True,
            text=True,
            timeout=10
        )
        output = process.stdout + process.stderr
    except subprocess.TimeoutExpired:
        output = "Command timed out"
    except Exception:
        output = "Command failed"
```

**Security impact:**
Attackers can execute arbitrary system commands with server privileges.

**Compliance:**
OWASP A1, CWE-78

---

#### INSEC-DESERIALIZE: Pickle Deserialization of User Data

**Vulnerable code:**
```python
def insec_des_lab(request):
    token = request.COOKIES.get('token')
    if token:
        token = base64.b64decode(token)
        admin = pickle.loads(token)  # DANGEROUS!
```

**Secure implementation:**
```python
import json
import hmac
import hashlib

SECRET_KEY = os.environ['SECRET_KEY']

def sign_data(data):
    serialized = json.dumps(data)
    signature = hmac.new(SECRET_KEY.encode(), serialized.encode(), hashlib.sha256).hexdigest()
    return base64.b64encode(f"{serialized}.{signature}".encode())

def verify_data(token):
    try:
        decoded = base64.b64decode(token).decode()
        data, signature = decoded.rsplit('.', 1)
        expected_sig = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, expected_sig):
            return json.loads(data)
    except:
        return None

def insec_des_lab(request):
    token = request.COOKIES.get('token')
    if token:
        admin_data = verify_data(token)
        if admin_data and admin_data.get('admin') == 1:
            return render(request, 'Lab/insec_des/insec_des_lab.html', {"message": "Welcome Admin"})
```

**Security impact:**
Arbitrary code execution through malicious serialized objects.

**Compliance:**
OWASP A8, CWE-502

---

#### XXE-INJECT: XML External Entity Processing

**Vulnerable code:**
```python
def xxe_parse(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)  # DANGEROUS!
    doc = parseString(request.body.decode('utf-8'), parser=parser)
```

**Secure implementation:**
```python
import defusedxml.pulldom as defused_pulldom

def xxe_parse(request):
    try:
        # Use defusedxml to prevent XXE
        doc = defused_pulldom.parseString(request.body.decode('utf-8'))
        for event, node in doc:
            if event == defused_pulldom.START_ELEMENT and node.tagName == 'text':
                doc.expandNode(node)
                text = node.toxml()
        # Process text safely...
    except Exception:
        return HttpResponseBadRequest("Invalid XML")
```

**Security impact:**
File disclosure, SSRF, denial of service through external entity attacks.

**Compliance:**
OWASP A4, CWE-611

---

#### AUTHZ-CHECK: Missing Authorization Controls

**Vulnerable code:**
```python
def ba_lab(request):
    if request.COOKIES.get('admin') == "1":  # Trusting client cookie!
        return render(request, 'Lab/BrokenAccess/ba_lab.html', {"data":"0NLY_F0R_4DM1N5"})
```

**Secure implementation:**
```python
def ba_lab(request):
    # Check server-side session/user role
    if not request.user.is_staff:
        return HttpResponseForbidden("Access denied")
    
    # Log admin access
    logging.info(f"Admin access by user {request.user.id}")
    return render(request, 'Lab/BrokenAccess/ba_lab.html', {"data":"0NLY_F0R_4DM1N5"})
```

**Security impact:**
Users can escalate privileges by modifying client-side cookies.

**Compliance:**
OWASP A1, CWE-862

---

#### XSS-PREVENT: Reflected XSS Vulnerabilities

**Vulnerable code:**
```python
def xss_lab(request):
    q=request.GET.get('q','')
    return render(request,'Lab/XSS/xss_lab.html', {'query': q})
```

**Secure implementation:**
```python
from django.utils.html import escape

def xss_lab(request):
    q = request.GET.get('q', '')
    # Template auto-escaping should handle this, but ensure it's enabled
    # Or manually escape if needed
    safe_q = escape(q)
    return render(request, 'Lab/XSS/xss_lab.html', {'query': safe_q})
```

**Security impact:**
Script injection in user browsers, session theft, defacement.

**Compliance:**
OWASP A3, CWE-79

---

#### WEAK-HASH: MD5 Hash Usage

**Vulnerable code:**
```python
from hashlib import md5

def crypto_failure_lab(request):
    password = md5(password.encode()).hexdigest()
```

**Secure implementation:**
```python
import bcrypt

def crypto_failure_lab(request):
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
```

**Security impact:**
MD5 is cryptographically broken and vulnerable to collision attacks.

**Compliance:**
OWASP A2, CWE-327

---

#### PATH-TRAVERSE: File Path Manipulation

**Vulnerable code:**
```python
def ssrf_lab(request):
    file=request.POST["blog"]
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)  # User controls path!
    file = open(filename,"r")
```

**Secure implementation:**
```python
from pathlib import Path

def ssrf_lab(request):
    file = request.POST.get("blog", "")
    
    # Validate filename
    if not re.match(r'^[a-zA-Z0-9_.-]+\.txt$', file):
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": "Invalid filename"})
    
    dirname = Path(__file__).parent
    blog_dir = dirname / "blogs"  # Restrict to blogs directory
    filepath = (blog_dir / file).resolve()
    
    # Ensure path is within allowed directory
    if not str(filepath).startswith(str(blog_dir.resolve())):
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": "Access denied"})
    
    try:
        with open(filepath, "r") as f:
            data = f.read()
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": data})
    except FileNotFoundError:
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": "File not found"})
```

**Security impact:**
Unauthorized file access, potential source code disclosure.

**Compliance:**
OWASP A6, CWE-22

---

### ⚠️ Warnings (Should Fix)

#### RANDOM-SECURE: Weak Random Number Generation

**Vulnerable code:**
```python
import random
from random import randint

def Otp(request):
    otpN=randint(100,999)  # Predictable!
```

**Secure implementation:**
```python
import secrets

def Otp(request):
    otpN = secrets.randbelow(900) + 100  # Cryptographically secure
```

**Security impact:**
Predictable OTP values enable account takeover.

**Compliance:**
CWE-330

---

#### CSRF-PROTECT: Missing CSRF Protection

**Vulnerable code:**
```python
@csrf_exempt
def xxe_parse(request):
    # CSRF protection disabled
```

**Secure implementation:**
```python
# Remove @csrf_exempt and ensure CSRF middleware is enabled
def xxe_parse(request):
    # CSRF protection will be enforced automatically
```

**Security impact:**
Cross-site request forgery attacks possible.

**Compliance:**
OWASP A8, CWE-352

---

#### SESSION-SECURE: Insecure Session Management

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
    httponly=True,
    secure=True,  # HTTPS only
    samesite='Lax'  # CSRF protection
)
```

**Security impact:**
Session hijacking through insecure cookies.

**Compliance:**
OWASP A2, CWE-614

---

#### LOG-SANITIZE: Unsanitized Logging

**Vulnerable code:**
```python
def a10_lab2(request):
    logging.info(f"{now}:{ip}:{user}")  # User input in logs
```

**Secure implementation:**
```python
import re

def sanitize_log_input(value):
    # Remove control characters and limit length
    return re.sub(r'[\n\r\t\x00-\x1f]', '', str(value)[:100])

def a10_lab2(request):
    user = sanitize_log_input(request.POST.get("name", ""))
    logging.info("Login attempt", extra={
        'timestamp': now,
        'ip': ip,
        'user_hash': hashlib.sha256(user.encode()).hexdigest()[:8]
    })
```

**Security impact:**
Log injection attacks, PII exposure in logs.

**Compliance:**
CWE-117

---

#### SSRF-PREVENT: Server-Side Request Forgery

**Vulnerable code:**
```python
def ssrf_lab2(request):
    url = request.POST["url"]
    response = requests.get(url)  # User controls destination!
```

**Secure implementation:**
```python
from urllib.parse import urlparse
import ipaddress

ALLOWED_HOSTS = {'httpbin.org', 'api.github.com'}

def ssrf_lab2(request):
    url = request.POST.get("url", "")
    parsed = urlparse(url)
    
    # Validate scheme
    if parsed.scheme not in ('http', 'https'):
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"error": "Invalid scheme"})
    
    # Validate host
    if parsed.hostname not in ALLOWED_HOSTS:
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"error": "Host not allowed"})
    
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"response": response.text[:1000]})
    except requests.RequestException:
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"error": "Request failed"})
```

**Security impact:**
Internal network access, credential theft, data exfiltration.

**Compliance:**
OWASP A10, CWE-918

---

### 💡 Recommendations (Best Practices)

#### MISSING-VALIDATION-LAYER: No Centralized Input Validation

**Current state:**
```python
# Ad-hoc validation throughout views
```

**Secure implementation:**
```python
from django import forms
from django.core.validators import RegexValidator

class SecureUserForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$')]
    )
    email = forms.EmailField()
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError("Username too short")
        return username
```

**Security impact:**
Inconsistent validation leads to security gaps.

**Compliance:**
OWASP Top 10

---

#### MISSING-SECURITY-HEADERS: No Security Headers

**Current state:**
```python
# No security headers set
```

**Secure implementation:**
```python
def set_security_headers(response):
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response['Content-Security-Policy'] = "default-src 'self'"
    return response

# Apply to all responses
@app.after_request
def add_security_headers(response):
    return set_security_headers(response)
```

**Security impact:**
Missing defense against various client-side attacks.

**Compliance:**
OWASP Security Headers

---

#### MISSING-SECRET-MGMT: Hardcoded Values

**Current state:**
```python
# Various hardcoded strings and secrets throughout code
```

**Secure implementation:**
```python
import os
from django.conf import settings

# In settings.py
SECRET_COOKIE_KEY = os.environ['SECRET_COOKIE_KEY']
DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']

# Use Django's SECRET_KEY instead of custom secrets
JWT_SECRET = settings.SECRET_KEY
```

**Security impact:**
Secrets exposure in source code.

**Compliance:**
CWE-798

---

### 📋 Compliance Checklist

- [ ] ❌ OWASP Top 10 compliance - Multiple A1, A2, A3, A8 violations
- [ ] ❌ PII properly protected - No PII handling controls
- [ ] ❌ Secrets not in code - Some hardcoded values present  
- [ ] ❌ Dependencies up to date - Cannot verify without requirements.txt
- [ ] ❌ Input validation - No centralized validation layer
- [ ] ❌ Authentication secure - Multiple authentication bypasses
- [ ] ❌ Authorization implemented - Client-side trust issues
- [ ] ❌ Error handling safe - Stack traces and sensitive info exposed
- [ ] ❌ Logging secure - Unsanitized user input in logs
- [ ] ❌ Sessions secure - Insecure cookie configuration

**Priority Actions:**
1. **Immediate**: Fix SQL injection, command injection, and code injection
2. **High**: Implement proper authentication and authorization
3. **Medium**: Add input validation and security headers
4. **Ongoing**: Establish secure development practices and code review process

This codebase appears to be intentionally vulnerable for educational purposes, but contains numerous critical security issues that would be unacceptable in production systems.
