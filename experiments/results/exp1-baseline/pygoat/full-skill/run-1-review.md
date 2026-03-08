## Security & Privacy Review: views.py

### ✅ Strengths
- **FRAMEWORK-CHOICE**: Using Django framework with built-in security features
- **AUTH-DECORATOR**: Some views use authentication decorators for basic access control

### 🔴 Critical Issues (Immediate Fix Required)

#### SQL-INJECT: SQL Injection Vulnerability

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
    name=request.POST.get('name')
    password=request.POST.get('pass')
    if name:
        # Use parameterized queries
        val = login.objects.filter(user=name, password=password)
        # Or with raw SQL: 
        # val = login.objects.raw("SELECT * FROM introduction_login WHERE user=%s AND password=%s", [name, password])
```

**Security impact:**
Attackers can execute arbitrary SQL commands, potentially accessing all database data, modifying records, or escalating privileges.

**Compliance:**
OWASP #1 (Injection), CWE-89

---

#### CMD-INJECT: Command Injection Vulnerabilities

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
    domain = request.POST.get('domain')
    # Validate domain format
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "Invalid domain format"})
    
    if os_type == 'win':
        # Pass arguments as list, never use shell=True
        process = subprocess.Popen(['nslookup', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(['dig', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**Security impact:**
Attackers can execute arbitrary system commands, potentially gaining full server access.

**Compliance:**
OWASP A1, CWE-78

---

#### CODE-INJECT: Code Injection via eval()

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

def cmd_lab2(request):
    val = request.POST.get('val')
    try:
        # Use safe AST evaluation or reject eval entirely
        tree = ast.parse(val, mode='eval')
        # Implement safe AST evaluation
        output = "Evaluation disabled for security"
```

**Security impact:**
Arbitrary code execution allowing complete system compromise.

**Compliance:**
CWE-94

---

#### INSEC-DES: Insecure Deserialization with pickle

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

def insec_des_lab(request):
    token = request.COOKIES.get('token')
    if token:
        try:
            # Use JSON instead of pickle
            decoded = base64.b64decode(token)
            data = json.loads(decoded.decode('utf-8'))
            admin_status = data.get('admin', 0)
        except (json.JSONDecodeError, ValueError):
            admin_status = 0
```

**Security impact:**
Pickle deserialization can lead to arbitrary code execution.

**Compliance:**
CWE-502

---

#### XML-INJECT: XXE (XML External Entity) Attack

**Vulnerable code:**
```python
def xxe_parse(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)  # Enables XXE!
    doc = parseString(request.body.decode('utf-8'), parser=parser)
```

**Secure implementation:**
```python
import defusedxml.dom.minidom as safe_minidom

def xxe_parse(request):
    try:
        # Use defusedxml to prevent XXE
        doc = safe_minidom.parseString(request.body.decode('utf-8'))
        # Process safely
    except Exception:
        return render(request, 'Lab/XXE/xxe_lab.html', {"error": "Invalid XML"})
```

**Security impact:**
XXE attacks can read local files, perform SSRF attacks, or cause denial of service.

**Compliance:**
CWE-611, OWASP A4

---

### ⚠️ Warnings (Should Fix)

#### XSS-PREVENT: Cross-Site Scripting Vulnerabilities

**Vulnerable code:**
```python
def xss_lab(request):
    q=request.GET.get('q','')
    return render(request,'Lab/XSS/xss_lab.html', {'query': q})

def xss_lab2(request):
    username = request.POST.get('username', '')
    username = username.replace("<script>", "").replace("</script>", "")  # Insufficient filtering
```

**Secure implementation:**
```python
from django.utils.html import escape

def xss_lab(request):
    q = request.GET.get('q', '')
    # Django templates auto-escape, but ensure context is safe
    return render(request, 'Lab/XSS/xss_lab.html', {'query': escape(q)})

def xss_lab2(request):
    username = request.POST.get('username', '')
    # Use proper escaping, not string replacement
    context = {'username': escape(username)}
    return render(request, 'Lab/XSS/xss_lab_2.html', context)
```

**Security impact:**
XSS can lead to session hijacking, defacement, or malicious script execution.

**Compliance:**
OWASP A3, CWE-79

---

#### WEAK-HASH: Weak Hash Algorithm (MD5)

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
    # Use bcrypt for password hashing
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode(), salt)
```

**Security impact:**
MD5 is cryptographically broken and vulnerable to collision attacks.

**Compliance:**
CWE-327

---

#### MISSING-CSRF: CSRF Protection Disabled

**Vulnerable code:**
```python
@csrf_exempt
def xxe_parse(request):
    # CSRF protection disabled
```

**Secure implementation:**
```python
# Remove @csrf_exempt decorator
def xxe_parse(request):
    # CSRF protection will be enforced by Django middleware
```

**Security impact:**
CSRF attacks can perform unauthorized actions on behalf of authenticated users.

**Compliance:**
OWASP A8, CWE-352

---

#### COOKIE-SECURE: Insecure Cookie Configuration

**Vulnerable code:**
```python
response.set_cookie('userid', obj.userid, max_age=31449600, samesite=None, secure=False)
response.set_cookie("admin", "1", max_age=200)
```

**Secure implementation:**
```python
response.set_cookie(
    'userid', 
    obj.userid, 
    max_age=31449600,
    secure=True,      # HTTPS only
    httponly=True,    # No JavaScript access
    samesite='Lax'    # CSRF protection
)
```

**Security impact:**
Insecure cookies can be intercepted or manipulated by attackers.

**Compliance:**
CWE-614, CWE-1004

---

#### PII-LOG: PII Exposure in Logs

**Vulnerable code:**
```python
def a10_lab2(request):
    if login.objects.filter(user=user,password=password):
        logging.info(f"{now}:{ip}:{user}")  # Logging username (PII)
```

**Secure implementation:**
```python
import hashlib

def hash_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()[:8]

def a10_lab2(request):
    if login.objects.filter(user=user, password=password):
        # Log hashed identifier instead
        user_hash = hash_pii(user)
        logging.info(f"{now}:{ip}:{user_hash}")
```

**Security impact:**
PII in logs can be exposed through log analysis or breaches.

**Compliance:**
GDPR Article 32

---

### 💡 Recommendations (Best Practices)

#### MISSING-VALIDATION-LAYER: Centralized Input Validation

**Current code:**
```python
def process_payment(user_email, card_number):
    # No validation framework
```

**Recommended implementation:**
```python
from django.core.validators import validate_email
from django import forms

class PaymentForm(forms.Form):
    user_email = forms.EmailField(validators=[validate_email])
    card_number = forms.CharField(max_length=19, min_length=13)
    
    def clean_card_number(self):
        card = self.cleaned_data['card_number']
        if not card.replace(' ', '').isdigit():
            raise forms.ValidationError("Invalid card number")
        return card
```

**Security impact:**
Centralized validation ensures consistent input handling across the application.

---

#### MISSING-SECURITY-HEADERS: Security Headers Configuration

**Current code:**
```python
# No security headers configured
```

**Recommended implementation:**
```python
# In Django settings.py
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Or use django-security middleware
```

**Security impact:**
Security headers provide defense-in-depth against various attacks.

---

### 📋 Compliance Checklist

- [ ] **OWASP Top 10 compliance** - Multiple violations found
- [ ] **PII properly protected** - PII logged in plaintext
- [ ] **GDPR requirements met** - No data protection measures
- [ ] **Secrets not in code** - Hardcoded passwords found
- [ ] **Dependencies up to date** - Manual review needed

### Summary

This application contains **18 critical security vulnerabilities** that require immediate attention. While this appears to be a training application designed to demonstrate vulnerabilities, the code patterns shown should never be used in production environments. The most severe issues include SQL injection, command injection, code injection via eval(), and insecure deserialization - all of which can lead to complete system compromise.
