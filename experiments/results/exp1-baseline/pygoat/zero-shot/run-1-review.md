# Security Review for views.py

## Critical Security Issues

### SQL-INJECT-1: Direct SQL Injection Vulnerability
**Severity: CRITICAL**

**Problematic Code:**
```python
def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    if name:
        sql_query = "SELECT * FROM introduction_login WHERE user='"+name+"' AND password='"+password+"'"
        val = login.objects.raw(sql_query)
```

**Improved Code:**
```python
def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')
    if name:
        # Use parameterized queries or Django ORM
        val = login.objects.filter(user=name, password=password)
        # Or if raw SQL is needed:
        # val = login.objects.raw("SELECT * FROM introduction_login WHERE user=%s AND password=%s", [name, password])
```

**Impact:** Allows attackers to execute arbitrary SQL commands, potentially leading to data breach, data manipulation, or complete database compromise.

### CMD-INJECT-1: Command Injection via subprocess
**Severity: CRITICAL**

**Problematic Code:**
```python
def cmd_lab(request):
    domain = request.POST.get('domain')
    domain = re.sub(r'^(?:(https?|ftp)://)?(?:www\.)?', '', domain, flags=re.IGNORECASE)
    command = "dig {}".format(domain)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```

**Improved Code:**
```python
def cmd_lab(request):
    domain = request.POST.get('domain')
    # Validate domain format
    if not re.match(r'^[a-zA-Z0-9.-]+$', domain):
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "Invalid domain format"})
    
    # Use subprocess with argument list instead of shell=True
    try:
        process = subprocess.Popen(['dig', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    except FileNotFoundError:
        return render(request, 'Lab/CMD/cmd_lab.html', {"output": "dig command not found"})
```

**Impact:** Allows attackers to execute arbitrary system commands on the server.

### CODE-INJECT-1: Code Injection via eval()
**Severity: CRITICAL**

**Problematic Code:**
```python
def cmd_lab2(request):
    val = request.POST.get('val')
    try:
        output = eval(val)
    except:
        output = "Something went wrong"
```

**Improved Code:**
```python
def cmd_lab2(request):
    val = request.POST.get('val')
    try:
        # Use ast.literal_eval for safe evaluation of literals only
        import ast
        output = ast.literal_eval(val)
    except (ValueError, SyntaxError):
        output = "Invalid expression"
```

**Impact:** Allows attackers to execute arbitrary Python code on the server.

### PICKLE-INJECT-1: Insecure Deserialization
**Severity: CRITICAL**

**Problematic Code:**
```python
def insec_des_lab(request):
    token = request.COOKIES.get('token')
    if token:
        token = base64.b64decode(token)
        admin = pickle.loads(token)  # Dangerous!
```

**Improved Code:**
```python
def insec_des_lab(request):
    token = request.COOKIES.get('token')
    if token:
        try:
            # Use JSON instead of pickle
            import json
            token_data = base64.b64decode(token)
            admin_data = json.loads(token_data.decode('utf-8'))
            # Validate the structure
            if 'admin' in admin_data and isinstance(admin_data['admin'], int):
                admin = type('TestUser', (), admin_data)()
            else:
                raise ValueError("Invalid token format")
        except (json.JSONDecodeError, ValueError):
            # Reset to default
            admin = TestUser()
```

**Impact:** Allows attackers to execute arbitrary code during deserialization.

### XXE-1: XML External Entity Processing
**Severity: CRITICAL**

**Problematic Code:**
```python
def xxe_parse(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)  # Enables XXE
    doc = parseString(request.body.decode('utf-8'), parser=parser)
```

**Improved Code:**
```python
def xxe_parse(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, False)  # Disable external entities
    parser.setFeature("http://apache.org/xml/features/disallow-doctype-decl", True)
    try:
        doc = parseString(request.body.decode('utf-8'), parser=parser)
    except Exception as e:
        return render(request, 'Lab/XXE/xxe_lab.html', {"error": "Invalid XML"})
```

**Impact:** Allows attackers to read local files, perform SSRF attacks, or cause denial of service.

## High Severity Issues

### SSRF-1: Server-Side Request Forgery
**Severity: HIGH**

**Problematic Code:**
```python
def ssrf_lab2(request):
    url = request.POST["url"]
    try:
        response = requests.get(url)
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"response": response.content.decode()})
```

**Improved Code:**
```python
def ssrf_lab2(request):
    url = request.POST.get("url")
    if not url:
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"error": "URL required"})
    
    # Validate URL and block internal networks
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.hostname in ['localhost', '127.0.0.1'] or parsed.hostname.startswith('192.168.'):
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"error": "Access denied"})
    
    try:
        response = requests.get(url, timeout=5)
        return render(request, "Lab/ssrf/ssrf_lab2.html", {"response": response.content.decode()})
```

**Impact:** Allows attackers to make requests to internal services and potentially access sensitive information.

### PATH-TRAVERSAL-1: Directory Traversal
**Severity: HIGH**

**Problematic Code:**
```python
def ssrf_lab(request):
    file = request.POST["blog"]
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    file = open(filename, "r")
```

**Improved Code:**
```python
def ssrf_lab(request):
    file = request.POST.get("blog")
    if not file:
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": "No file specified"})
    
    # Validate file path and prevent directory traversal
    import os.path
    dirname = os.path.dirname(__file__)
    filename = os.path.normpath(os.path.join(dirname, file))
    
    # Ensure the file is within the allowed directory
    if not filename.startswith(dirname):
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": "Access denied"})
    
    try:
        with open(filename, "r") as f:
            data = f.read()
        return render(request, "Lab/ssrf/ssrf_lab.html", {"blog": data})
```

**Impact:** Allows attackers to read arbitrary files from the server filesystem.

### YAML-INJECT-1: Unsafe YAML Deserialization
**Severity: HIGH**

**Problematic Code:**
```python
def a9_lab(request):
    file = request.FILES["file"]
    try:
        data = yaml.load(file, yaml.Loader)  # Dangerous!
```

**Improved Code:**
```python
def a9_lab(request):
    file = request.FILES.get("file")
    if not file:
        return render(request, "Lab/A9/a9_lab.html", {"data": "Please upload a file"})
    
    try:
        data = yaml.safe_load(file)  # Use safe_load instead
        return render(request, "Lab/A9/a9_lab.html", {"data": data})
```

**Impact:** Allows attackers to execute arbitrary Python code through malicious YAML files.

### SSTI-1: Server-Side Template Injection
**Severity: HIGH**

**Problematic Code:**
```python
def ssti_lab(request):
    blog = request.POST["blog"]
    blog = filter_blog(blog)  # Insufficient filtering
    prepend_code = "{% extends 'introduction/base.html' %}..."
    blog = prepend_code + blog + "{% endblock %}"
    # Creates template file with user input
```

**Improved Code:**
```python
def ssti_lab(request):
    blog = request.POST.get("blog")
    if not blog:
        return render(request, "Lab_2021/A3_Injection/ssti_lab.html")
    
    # Escape all Django template syntax
    import html
    blog = html.escape(blog)
    
    # Or better: store as data and render safely
    id = str(uuid.uuid4()).split('-')[-1]
    new_blog = Blogs.objects.create(author=request.user, blog_id=id, content=blog)
    return render(request, "Lab_2021/A3_Injection/blog_view.html", {"blog": new_blog})
```

**Impact:** Allows attackers to execute arbitrary code through template injection.

## Medium Severity Issues

### XSS-REFLECT-1: Reflected Cross-Site Scripting
**Severity: MEDIUM**

**Problematic Code:**
```python
def xss_lab(request):
    q = request.GET.get('q', '')
    return render(request, 'Lab/XSS/xss_lab.html', {'query': q})
```

**Improved Code:**
```python
def xss_lab(request):
    q = request.GET.get('q', '')
    # HTML escape the user input
    from django.utils.html import escape
    q = escape(q)
    return render(request, 'Lab/XSS/xss_lab.html', {'query': q})
```

**Impact:** Allows attackers to inject malicious scripts into web pages.

### WEAK-CRYPTO-1: MD5 Password Hashing
**Severity: MEDIUM**

**Problematic Code:**
```python
def crypto_failure_lab(request):
    password = md5(password.encode()).hexdigest()
```

**Improved Code:**
```python
def crypto_failure_lab(request):
    from django.contrib.auth.hashers import make_password, check_password
    # Use Django's built-in password hashing
    hashed_password = make_password(password)
    # For verification: check_password(password, hashed_password)
```

**Impact:** MD5 is cryptographically broken and vulnerable to rainbow table attacks.

### JWT-WEAK-1: JWT Secret Key Exposure
**Severity: MEDIUM**

**Problematic Code:**
```python
from pygoat.settings import SECRET_COOKIE_KEY
def sec_misconfig_lab3(request):
    cookie = jwt.decode(cookie, SECRET_COOKIE_KEY, algorithms=['HS256'])
```

**Improved Code:**
```python
def sec_misconfig_lab3(request):
    # Use Django's SECRET_KEY or separate JWT secret
    from django.conf import settings
    JWT_SECRET = getattr(settings, 'JWT_SECRET_KEY', settings.SECRET_KEY)
    
    try:
        cookie = jwt.decode(cookie, JWT_SECRET, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        # Handle invalid token
        return render(request, "error.html", {"error": "Invalid token"})
```

**Impact:** Weak secret keys can be cracked, allowing token forgery.

## Low Severity Issues

### INFO-DISCLOSURE-1: Debug Information Exposure
**Severity: LOW**

**Problematic Code:**
```python
except:
    print("\nin except\n")
    return render(request, 'Lab/SQL/sql_lab.html', {"sql_error": sql_query})
```

**Improved Code:**
```python
except Exception as e:
    logger.error(f"Database error: {e}")
    return render(request, 'Lab/SQL/sql_lab.html', {"error": "Database error occurred"})
```

**Impact:** Exposes internal system information that could aid attackers.

### HARDCODE-CREDS-1: Hardcoded Credentials
**Severity: LOW**

**Problematic Code:**
```python
USER_A7_LAB3 = {
    "User1": {"password": "491a2800b80719ea9e3c89ca5472a8bda1bdd1533d4574ea5bd85b70a8e93be0"},
    # ... more hardcoded credentials
}
```

**Improved Code:**
```python
# Store credentials in database or environment variables
# Use Django's User model or custom user model
from django.contrib.auth.models import User

def get_user_by_credentials(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        pass
    return None
```

**Impact:** Hardcoded credentials can be discovered through code analysis.

## Summary

This code contains **15 critical security vulnerabilities** that require immediate attention. The most severe issues include SQL injection, command injection, code injection via eval(), insecure deserialization, and XXE vulnerabilities. These vulnerabilities could lead to complete system compromise.

**Immediate Actions Required:**
1. Fix all SQL injection vulnerabilities using parameterized queries
2. Remove use of `eval()` and `pickle.loads()` on user input
3. Disable XXE processing in XML parsers
4. Validate and sanitize all user input
5. Implement proper error handling without information disclosure
6. Use secure cryptographic practices
7. Add proper authentication and authorization checks
