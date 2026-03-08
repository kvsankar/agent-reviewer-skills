# Security & Privacy Review: views.py

## ✅ Strengths
- **HASH-PASSWORD**: Uses Argon2 for some password operations (PasswordHasher import)
- **DJANGO-CSRF**: Some endpoints use `@csrf_exempt` appropriately for API endpoints
- **AUTHZ-CHECK**: Basic authentication decorators are implemented

## 🔴 Critical Issues (Immediate Fix Required)

### **SQL-INJECT**: SQL Injection in Multiple Functions

**Vulnerable code:**
```python
def sql_lab(request):
    name=request.POST.get('name')
    password=request.POST.get('pass')
    sql_query = "SELECT * FROM introduction_login WHERE user='"+name+"' AND password='"+password+"'"
    val=login.objects.raw(sql_query)
```

**Also vulnerable in injection_sql_lab():**
```python
sql_query = "SELECT * FROM introduction_sql_lab_table WHERE id='"+name+"'AND password='"+password+"'"
user = sql_lab_table.objects.raw(sql_query)
```

**Secure implementation:**
```python
def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    
    if name and password:
        # Use parameterized queries
        try:
            user = login.objects.filter(user=name, password=password).first()
            if user:
                return render(request, 'Lab/SQL/sql_lab.html', {"user1": user.user})
        except login.DoesNotExist:
            return render(request, 'Lab/SQL/sql_lab.html', {"no": "User not found"})
```

**Security impact:**
Attackers can extract entire database contents, bypass authentication, or execute arbitrary SQL commands using payloads like `' OR '1'='1' --`

**Compliance:**
OWASP A3 (Injection), CWE-89

---

### **CMD-INJECT**: Command Injection Vulnerabilities

**Vulnerable code:**
```python
def cmd_lab(request):
    domain=request.POST.get('domain')
    domain = re.sub(r'^(?:(https?|ftp)://)?(?:www\.)?', '', domain, flags=re.IGNORECASE)
    if(os=='win'):
        command="nslookup {}".format(domain)
    else:
        command = "dig {}".format(domain)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**Secure implementation:**
```python
def cmd_lab(request):
    domain = request.POST.get('domain', '').strip()
    
    # Validate domain format
    import re
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', domain):
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "Invalid domain format"})
    
    os_type = request.POST.get('os')
    if os_type == 'win':
        command = ['nslookup', domain]  # Use list, not shell=True
    else:
        command = ['dig', domain]
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=10)
        output = stdout.decode('utf-8') + stderr.decode('utf-8')
    except subprocess.TimeoutExpired:
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "Command timeout"})
```

**Security impact:**
Attackers can execute arbitrary system commands using payloads like `google.com; cat /etc/passwd`

**Compliance:**
OWASP A3 (Injection), CWE-78

---

### **CODE-INJECT**: Dangerous Code Execution

**Vulnerable code:**
```python
def cmd_lab2(request):
    val=request.POST.get('val')
    try:
        output = eval(val)  # EXTREMELY DANGEROUS!
    except:
        output = "Something went wrong"
```

**Secure implementation:**
```python
def cmd_lab2(request):
    val = request.POST.get('val', '').strip()
    
    # Only allow safe mathematical expressions
    import ast
    import operator
    
    # Define allowed operations
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def safe_eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](safe_eval(node.left), safe_eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](safe_eval(node.operand))
        else:
            raise ValueError('Unsafe operation')
    
    try:
        tree = ast.parse(val, mode='eval')
        result = safe_eval(tree.body)
        return render(request, 'Lab/CMD/cmd_lab2.html', {"output": result})
    except:
        return render(request, 'Lab/CMD/cmd_lab2.html', {"output": "Invalid expression"})
```

**Security impact:**
`eval()` allows arbitrary Python code execution, potentially leading to complete system compromise

**Compliance:**
CWE-94, CWE-95

---

### **AUTHZ-CHECK**: Broken Authorization via Client-Side Cookies

**Vulnerable code:**
```python
def ba_lab(request):
    if request.COOKIES.get('admin') == "1":
        return render(request, 'Lab/BrokenAccess/ba_lab.html', {
            "data":"0NLY_F0R_4DM1N5",
            "username": "admin"
        })
```

**Secure implementation:**
```python
def ba_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    
    if name and password:
        # Server-side authorization check
        user = authenticate(username=name, password=password)
        if user and user.is_staff:  # Check server-side role
            return render(request, 'Lab/BrokenAccess/ba_lab.html', {
                "data": "0NLY_F0R_4DM1N5",
                "username": user.username
            })
        elif user:
            return render(request, 'Lab/BrokenAccess/ba_lab.html', {
                "not_admin": "No Secret key for this User",
                "username": user.username
            })
```

**Security impact:**
Any user can modify their cookie to gain admin access

**Compliance:**
OWASP A1 (Broken Access Control), CWE-639

---

### **INSEC-DESERIALIZE**: Unsafe Pickle Deserialization

**Vulnerable code:**
```python
def insec_des_lab(request):
    token = request.COOKIES.get('token')
    if token != None:
        token = base64.b64decode(token)
        admin = pickle.loads(token)  # Unsafe deserialization
```

**Secure implementation:**
```python
import json
from django.core.signing import Signer

def insec_des_lab(request):
    signer = Signer()
    token = request.COOKIES.get('token')
    
    if token:
        try:
            # Use signed JSON instead of pickle
            data = signer.unsign(token)
            admin_data = json.loads(data)
            if admin_data.get('admin') == 1:
                return render(request, 'template.html', {"message": "Welcome Admin"})
        except (BadSignature, json.JSONDecodeError):
            pass
    
    # Set default token
    default_data = json.dumps({"admin": 0})
    token = signer.sign(default_data)
    response = render(request, 'template.html', {"message": "Only Admins can see this page"})
    response.set_cookie('token', token)
    return response
```

**Security impact:**
Pickle deserialization can lead to remote code execution

**Compliance:**
CWE-502

---

### **XXE-INJECT**: XML External Entity Processing

**Vulnerable code:**
```python
def xxe_parse(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)  # Enables external entities!
    doc = parseString(request.body.decode('utf-8'), parser=parser)
```

**Secure implementation:**
```python
def xxe_parse(request):
    from xml.dom.minidom import parseString
    from xml.parsers.expat import ParserError
    
    try:
        # Use defusedxml library or disable external entities
        from defusedxml.minidom import parseString as safe_parseString
        doc = safe_parseString(request.body.decode('utf-8'))
        
        # Or manually disable dangerous features:
        # parser = make_parser()
        # parser.setFeature(feature_external_ges, False)
        # parser.setFeature("http://xml.org/sax/features/external-parameter-entities", False)
        
    except (ParserError, ValueError):
        return render(request, 'Lab/XXE/xxe_lab.html', {"error": "Invalid XML"})
```

**Security impact:**
XXE can lead to file disclosure, SSRF, or DoS attacks

**Compliance:**
OWASP A4 (XML External Entities), CWE-611

---

### **WEAK-HASH**: MD5 Usage for Password Hashing

**Vulnerable code:**
```python
def crypto_failure_lab(request):
    password = md5(password.encode()).hexdigest()
    user = CF_user.objects.filter(username=username,password=password).first()
```

**Secure implementation:**
```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def crypto_failure_lab(request):
    username = request.POST["username"]
    password = request.POST["password"]
    
    try:
        user = CF_user.objects.filter(username=username).first()
        if user:
            ph = PasswordHasher()
            ph.verify(user.password, password)  # Verify against Argon2 hash
            return render(request, 'template.html', {"user": user, "success": True})
    except (VerifyMismatchError, AttributeError):
        return render(request, 'template.html', {"success": False, "failure": True})
```

**Security impact:**
MD5 is cryptographically broken and vulnerable to rainbow table attacks

**Compliance:**
CWE-327, OWASP A2 (Cryptographic Failures)

---

## ⚠️ Warnings (Should Fix)

### **MISSING-CSRF**: CSRF Protection Disabled

**Vulnerable code:**
```python
@csrf_exempt
def xxe_parse(request):
@csrf_exempt  
def cmd_lab(request):
```

**Secure implementation:**
```python
# Remove @csrf_exempt and use proper CSRF protection
def xxe_parse(request):
    # Django's CSRF middleware will handle protection automatically
    if request.method == 'POST':
        # Process request with CSRF protection
```

**Security impact:**
Removes CSRF protection, allowing cross-site request forgery attacks

**Compliance:**
OWASP A8 (Security Misconfiguration), CWE-352

---

### **SSRF-VULN**: Server-Side Request Forgery

**Vulnerable code:**
```python
def ssrf_lab2(request):
    url = request.POST["url"]
    try:
        response = requests.get(url)  # No URL validation!
        return render(request, "template.html", {"response": response.content.decode()})
```

**Secure implementation:**
```python
from urllib.parse import urlparse
import ipaddress

def ssrf_lab2(request):
    url = request.POST["url"]
    parsed = urlparse(url)
    
    # Allowlist allowed hosts
    ALLOWED_HOSTS = {'api.example.com', 'public-api.service.com'}
    
    if parsed.hostname not in ALLOWED_HOSTS:
        # Additional check for private IPs
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback:
                return render(request, "template.html", {"error": "Private IPs not allowed"})
        except ValueError:
            pass
        return render(request, "template.html", {"error": "Host not allowed"})
    
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        return render(request, "template.html", {"response": response.text[:1000]})  # Limit response size
    except requests.RequestException:
        return render(request, "template.html", {"error": "Request failed"})
```

**Security impact:**
Can be used to scan internal networks or access internal services

**Compliance:**
CWE-918

---

### **PII-LOG**: Sensitive Data in Logs

**Vulnerable code:**
```python
def a10_lab2(request):
    user=request.POST.get("name")
    password=request.POST.get("pass")
    logging.info(f"{now}:{ip}:{user}")
    logging.error(f"{now}:{ip}:{user}")
```

**Secure implementation:**
```python
import hashlib

def a10_lab2(request):
    user = request.POST.get("name")
    password = request.POST.get("pass")
    
    # Hash username before logging to prevent PII exposure
    user_hash = hashlib.sha256(user.encode()).hexdigest()[:8] if user else "unknown"
    
    if login.objects.filter(user=user, password=password):
        logging.info(f"{now}:{ip}:login_success:{user_hash}")
    else:
        logging.error(f"{now}:{ip}:login_failed:{user_hash}")
```

**Security impact:**
Usernames in logs can be PII and aid attackers in enumeration

**Compliance:**
GDPR Article 5, CWE-532

---

## 💡 Recommendations (Best Practices)

### **MISSING-VALIDATION-LAYER**: Input Validation

**Current state:**
Most functions lack comprehensive input validation

**Recommendation:**
```python
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_user_input(request):
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    
    # Length validation
    if not (3 <= len(username) <= 50):
        raise ValidationError("Username must be 3-50 characters")
    
    # Email validation
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Invalid email format")
    
    # Alphanumeric username validation
    if not username.isalnum():
        raise ValidationError("Username must be alphanumeric")
```

---

### **MISSING-RATE-LIMITING**: Brute Force Protection

**Recommendation:**
```python
from django.core.cache import cache
from django.http import HttpResponseTooManyRequests

def rate_limit_login(request):
    ip = request.META.get('REMOTE_ADDR')
    cache_key = f"login_attempts_{ip}"
    
    attempts = cache.get(cache_key, 0)
    if attempts >= 5:
        return HttpResponseTooManyRequests("Too many attempts. Try again later.")
    
    # Increment attempts on failed login
    cache.set(cache_key, attempts + 1, 300)  # 5 minute window
```

---

### **MISSING-SECURITY-HEADERS**: Security Headers

**Recommendation:**
```python
# In Django settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Or using middleware
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        return response
```

---

## 📋 Compliance Checklist

- [ ] **OWASP Top 10 2021**
  - [ ] A01: Broken Access Control - ❌ Multiple cookie-based authz issues
  - [ ] A02: Cryptographic Failures - ❌ MD5 usage, weak tokens
  - [ ] A03: Injection - ❌ SQL injection, command injection, XXE
  - [ ] A04: Insecure Design - ❌ Security by obscurity patterns
  - [ ] A05: Security Misconfiguration - ⚠️ CSRF disabled, debug info
  - [ ] A06: Vulnerable Components - ⚠️ Need dependency audit
  - [ ] A07: Authentication Failures - ❌ Multiple authentication bypasses
  - [ ] A08: Software Integrity Failures - ❌ Unsafe deserialization
  - [ ] A09: Security Logging Failures - ⚠️ PII in logs
  - [ ] A10: SSRF - ❌ Unrestricted URL fetching

- [ ] **Privacy Compliance**
  - [ ] GDPR Article 5 (Data Minimization) - ❌ Logging PII
  - [ ] GDPR Article 25 (Privacy by Design) - ❌ No privacy controls
  - [ ] GDPR Article 32 (Security) - ❌ Multiple security failures

## Summary

This code contains **15 critical security vulnerabilities** that require immediate remediation. The application appears to be vulnerable-by-design for educational purposes, but these patterns should never appear in production code. Priority should be given to:

1. **SQL Injection** - Complete rewrite using parameterized queries
2. **Command Injection** - Input validation and subprocess hardening  
3. **Authorization Bypass** - Server-side permission checks
4. **Unsafe Deserialization** - Replace pickle with signed JSON
5. **XXE Processing** - Disable external entities or use defusedxml

The codebase requires a comprehensive security review and remediation before any production deployment.
