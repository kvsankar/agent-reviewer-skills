# Security Code Review - views.py

This Django views file contains **multiple critical security vulnerabilities** that expose the application to severe attacks. Below is a detailed analysis of the most significant issues.

## Critical Vulnerabilities

### 1. SQL-INJECT
**CWE-89: SQL Injection**  
**Severity: Critical**

**Vulnerable Code:**
```python
# Line ~143 in sql_lab function
sql_query = "SELECT * FROM introduction_login WHERE user='"+name+"' AND password='"+password+"'"
val=login.objects.raw(sql_query)

# Line ~818 in injection_sql_lab function  
sql_query = "SELECT * FROM introduction_sql_lab_table WHERE id='"+name+"'AND password='"+password+"'"
user = sql_lab_table.objects.raw(sql_query)
```

**Secure Alternative:**
```python
# Use parameterized queries
val = login.objects.filter(user=name, password=password)
# Or with raw SQL if needed:
sql_query = "SELECT * FROM introduction_login WHERE user=%s AND password=%s"
val = login.objects.raw(sql_query, [name, password])
```

**Attack Scenario:** Attacker sends `'; DROP TABLE users; --` as username, leading to database destruction or unauthorized data access.

### 2. CMD-INJECT
**CWE-78: Command Injection**  
**Severity: Critical**

**Vulnerable Code:**
```python
# Line ~524 in cmd_lab function
command="nslookup {}".format(domain)
# or
command = "dig {}".format(domain)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**Secure Alternative:**
```python
# Use subprocess with list arguments, no shell=True
import shlex
command_args = ['nslookup', domain] if os=='win' else ['dig', domain]
process = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**Attack Scenario:** Attacker inputs `google.com; rm -rf /` leading to file system destruction.

### 3. CODE-INJECT
**CWE-94: Code Injection**  
**Severity: Critical**

**Vulnerable Code:**
```python
# Line ~566 in cmd_lab2 function
output = eval(val)

# Line ~1050 in a9_lab2 function
output = ImageMath.eval(function_str, img=img, b=b, r=r, g=g)
```

**Secure Alternative:**
```python
# Use ast.literal_eval for safe evaluation of literals only
import ast
try:
    output = ast.literal_eval(val)
except (ValueError, SyntaxError):
    output = "Invalid input"

# For ImageMath, validate function_str against whitelist
ALLOWED_FUNCTIONS = ['convert', 'add', 'subtract', 'multiply']
if any(func in function_str for func in ALLOWED_FUNCTIONS):
    output = ImageMath.eval(function_str, img=img, b=b, r=r, g=g)
```

**Attack Scenario:** Attacker inputs `__import__('os').system('rm -rf /')` leading to arbitrary code execution.

### 4. PICKLE-DESER
**CWE-502: Insecure Deserialization**  
**Severity: Critical**

**Vulnerable Code:**
```python
# Line ~199 in insec_des_lab function
token = base64.b64decode(token)
admin = pickle.loads(token)
```

**Secure Alternative:**
```python
# Use JSON instead of pickle for data serialization
import json
try:
    token_data = json.loads(base64.b64decode(token).decode())
    admin_status = token_data.get('admin', 0)
except (json.JSONDecodeError, ValueError):
    admin_status = 0
```

**Attack Scenario:** Attacker crafts malicious pickle payload to execute arbitrary code during deserialization.

### 5. XXE-ATTACK
**CWE-611: XML External Entity**  
**Severity: Critical**

**Vulnerable Code:**
```python
# Line ~245 in xxe_parse function
parser = make_parser()
parser.setFeature(feature_external_ges, True)
doc = parseString(request.body.decode('utf-8'), parser=parser)
```

**Secure Alternative:**
```python
# Disable external entity processing
parser = make_parser()
parser.setFeature(feature_external_ges, False)
parser.setFeature("http://apache.org/xml/features/disallow-doctype-decl", True)
# Or use defusedxml library
from defusedxml import sax
parser = sax.make_parser()
```

**Attack Scenario:** Attacker sends XML with external entity references to read local files or perform SSRF attacks.

### 6. XSS-REFLECT
**CWE-79: Cross-Site Scripting**  
**Severity: High**

**Vulnerable Code:**
```python
# Line ~108 in xss_lab function
return render(request,'Lab/XSS/xss_lab.html', {'query': q})

# Line ~123 in xss_lab2 function
username = username.replace("<script>", "").replace("</script>", "")
context = {'username': username}
```

**Secure Alternative:**
```python
from django.utils.html import escape
# Always escape user input in templates
return render(request,'Lab/XSS/xss_lab.html', {'query': escape(q)})

# Use Django's built-in XSS protection (don't disable it)
# Templates should use {{ username|escape }} or auto-escaping
```

**Attack Scenario:** Attacker inputs `<img src=x onerror=alert('XSS')>` to execute JavaScript in victim's browser.

## High Severity Vulnerabilities

### 7. SSRF-ATTACK
**CWE-918: Server-Side Request Forgery**  
**Severity: High**

**Vulnerable Code:**
```python
# Line ~897 in ssrf_lab2 function
url = request.POST["url"]
response = requests.get(url)
```

**Secure Alternative:**
```python
from urllib.parse import urlparse
import ipaddress

def is_safe_url(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False
        # Resolve hostname and check for internal IPs
        ip = socket.gethostbyname(parsed.hostname)
        return not ipaddress.ip_address(ip).is_private
    except:
        return False

if is_safe_url(url):
    response = requests.get(url, timeout=5)
```

**Attack Scenario:** Attacker accesses internal services via `http://127.0.0.1:8080/admin`.

### 8. YAML-DESER
**CWE-502: Unsafe YAML Deserialization**  
**Severity: High**

**Vulnerable Code:**
```python
# Line ~1003 in a9_lab function
data = yaml.load(file, yaml.Loader)
```

**Secure Alternative:**
```python
# Use safe loader
data = yaml.safe_load(file)
# Or restrict to basic types only
data = yaml.load(file, Loader=yaml.SafeLoader)
```

**Attack Scenario:** Attacker uploads YAML with Python object constructors to execute arbitrary code.

### 9. WEAK-CRYPTO
**CWE-327: Weak Cryptography**  
**Severity: High**

**Vulnerable Code:**
```python
# Line ~1142 in crypto_failure_lab function
password = md5(password.encode()).hexdigest()

# Line ~1198 in crypto_failure_lab3 function
cookie = f"{username}|{expire}"  # No integrity protection
```

**Secure Alternative:**
```python
# Use strong password hashing
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)

# Use signed cookies
from django.core.signing import Signer
signer = Signer()
cookie = signer.sign(f"{username}|{expire}")
```

**Attack Scenario:** Attacker cracks MD5 hashes or tampers with unsigned cookies.

### 10. AUTH-BYPASS
**CWE-287: Improper Authentication**  
**Severity: High**

**Vulnerable Code:**
```python
# Line ~300 in ba_lab function
if request.COOKIES.get('admin') == "1":
    # Grant admin access

# Line ~1360 in auth_failure_lab3 function
if USER_A7_LAB3[username]['password'] == password:
    # Direct comparison without rate limiting
```

**Secure Alternative:**
```python
# Use Django's built-in authentication
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def admin_view(request):
    # Admin functionality

# Implement rate limiting
from django_ratelimit.decorators import ratelimit
@ratelimit(key='ip', rate='5/m')
def login_view(request):
    # Login logic with rate limiting
```

**Attack Scenario:** Attacker sets admin cookie to "1" or brute forces credentials without rate limiting.

## Medium Severity Vulnerabilities

### 11. INFO-LEAK
**CWE-209: Information Disclosure**  
**Severity: Medium**

**Vulnerable Code:**
```python
# Line ~149 - SQL error disclosure
return render(request, 'Lab/SQL/sql_lab.html', {"sql_error": sql_query})

# Debug mode exposure in settings
```

**Secure Alternative:**
```python
# Generic error messages
return render(request, 'Lab/SQL/sql_lab.html', {"error": "Login failed"})

# Ensure DEBUG = False in production
```

### 12. CSRF-MISS
**CWE-352: Cross-Site Request Forgery**  
**Severity: Medium**

**Vulnerable Code:**
```python
@csrf_exempt
def xxe_parse(request):
@csrf_exempt  
def cmd_lab(request):
```

**Secure Alternative:**
```python
# Remove @csrf_exempt and use CSRF tokens
# Use Django's built-in CSRF protection
def secure_view(request):
    # CSRF protection enabled by default
```

## Recommendations

1. **Immediate Actions:**
   - Replace all raw SQL with parameterized queries
   - Remove `eval()` and `exec()` calls
   - Disable XXE in XML parsers
   - Implement input validation and output encoding

2. **Authentication & Authorization:**
   - Use Django's built-in authentication system
   - Implement proper session management
   - Add rate limiting for login attempts
   - Use strong password hashing (Argon2)

3. **General Security:**
   - Enable Django's security middleware
   - Set `DEBUG = False` in production
   - Implement Content Security Policy
   - Add proper error handling without information disclosure
   - Use HTTPS only with secure cookie flags

This application appears to be intentionally vulnerable for security training purposes, but these patterns should never be used in production code.
