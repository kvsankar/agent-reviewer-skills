# security-privacy-reviewer Review

**Repository:** https://github.com/simonw/datasette
**Review Date:** 2025-11-12 13:33:03
**Reviewer:** security-privacy-reviewer
**AI Provider:** claude

---

Now I'll write a comprehensive security and privacy review based on my exploration of the Datasette codebase.

## Security & Privacy Review: Datasette

### ✅ Strengths

- **SQL-INJECT**: Good use of parameterized queries through SQLite's native execute() method with parameters in `datasette/database.py:274`
- **ESCAPE-SQLITE**: Proper SQL identifier escaping using `escape_sqlite()` function for dynamic column/table names in `datasette/utils/__init__.py:404`
- **VALIDATE-INPUT**: SQL validation through `validate_sql_select()` function prevents dangerous SQL statements in `datasette/utils/__init__.py:315`
- **RANDOM-SECURE**: Uses `secrets` module for cryptographically secure random generation in `datasette/app.py:26`
- **CSRF-PROTECT**: CSRF protection implemented using `asgi_csrf` middleware in `datasette/app.py:1860`
- **TIMING-ATTACK**: Uses `itsdangerous.URLSafeSerializer` for secure token handling in `datasette/app.py:1414`
- **HEADER-SECURE**: Some security headers like `X-Content-Type-Options: nosniff` in blob renderer

### 🔴 Critical Issues (Immediate Fix Required)

#### **CORS-RESTRICT**: Overly Permissive CORS Configuration

**Vulnerable code:**
```python
def add_cors_headers(headers):
    headers["Access-Control-Allow-Origin"] = "*"
    headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    headers["Access-Control-Expose-Headers"] = "Link"
    headers["Access-Control-Allow-Methods"] = "GET, POST, HEAD, OPTIONS"
    headers["Access-Control-Max-Age"] = "3600"
```

**Secure implementation:**
```python
def add_cors_headers(headers, allowed_origins=None):
    # Default to restrictive origins
    allowed_origins = allowed_origins or ["https://localhost:*"]
    origin = headers.get("Origin")
    
    if origin and any(origin.startswith(allowed) for allowed in allowed_origins):
        headers["Access-Control-Allow-Origin"] = origin
    else:
        headers["Access-Control-Allow-Origin"] = "null"
    
    headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    headers["Access-Control-Expose-Headers"] = "Link"
    headers["Access-Control-Allow-Methods"] = "GET, POST, HEAD, OPTIONS"
    headers["Access-Control-Max-Age"] = "3600"
    headers["Access-Control-Allow-Credentials"] = "false"
```

**Security impact:**
The wildcard `*` origin allows any website to make requests to the Datasette instance, potentially exposing sensitive data through cross-origin requests.

**Compliance:**
Violates OWASP A5 (Security Misconfiguration), CWE-942

---

#### **HEADER-SECURE**: Missing Critical Security Headers

**Vulnerable code:**
```python
# Only X-Content-Type-Options in blob renderer
headers = {
    "X-Content-Type-Options": "nosniff",
    "Content-Disposition": f'attachment; filename="{filename}"',
}
```

**Secure implementation:**
```python
def add_security_headers(response):
    response.headers.update({
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
    })
    return response

@app.after_request
def set_security_headers(response):
    return add_security_headers(response)
```

**Security impact:**
Missing security headers leave the application vulnerable to clickjacking, XSS, MIME sniffing attacks, and information disclosure.

**Compliance:**
OWASP A5 (Security Misconfiguration), CWE-693, CWE-1021

---

### ⚠️ Warnings (Should Fix)

#### **NO-HARDCODE**: Environment Variable Secrets Pattern Needs Validation

**Vulnerable code:**
```python
def resolve_env_secrets(config, environ):
    """Create copy that recursively replaces {"$env": "NAME"} with values from environ"""
    if isinstance(config, dict):
        if list(config.keys()) == ["$env"]:
            return environ.get(list(config.values())[0])  # Could return None!
```

**Secure implementation:**
```python
def resolve_env_secrets(config, environ):
    """Create copy that recursively replaces {"$env": "NAME"} with values from environ"""
    if isinstance(config, dict):
        if list(config.keys()) == ["$env"]:
            env_var = list(config.values())[0]
            value = environ.get(env_var)
            if value is None:
                raise ValueError(f"Required environment variable '{env_var}' not found")
            return value
        elif list(config.keys()) == ["$file"]:
            file_path = list(config.values())[0]
            if not os.path.exists(file_path):
                raise ValueError(f"Secret file '{file_path}' not found")
            # Validate file permissions (should be 600)
            stat_info = os.stat(file_path)
            if stat.S_IMODE(stat_info.st_mode) & 0o077:
                raise ValueError(f"Secret file '{file_path}' has overly permissive permissions")
            with open(file_path) as fp:
                return fp.read().strip()
```

**Security impact:**
Missing environment variables silently become None, potentially causing authentication bypasses.

**Compliance:**
CWE-798, CWE-522

---

#### **PII-LOG**: Potential PII in Request Logging

**Vulnerable code:**
```python
# datasette/views/special.py:100
token = request.args.get("token") or ""
# No validation that this isn't logged elsewhere
```

**Secure implementation:**
```python
def sanitize_for_logging(request_path, params):
    """Remove sensitive parameters from logging"""
    sensitive_params = {'token', 'password', 'secret', 'key', 'auth'}
    
    sanitized_params = {}
    for key, value in params.items():
        if key.lower() in sensitive_params:
            sanitized_params[key] = "[REDACTED]"
        else:
            sanitized_params[key] = value
    return sanitized_params

# In logging contexts
safe_params = sanitize_for_logging(request.path, request.args)
logger.info(f"Request to {request.path} with params: {safe_params}")
```

**Security impact:**
Authentication tokens and sensitive data could be exposed in application logs.

**Compliance:**
GDPR Article 32, CWE-532

---

### 💡 Recommendations (Best Practices)

#### **ENCRYPT-TRANSIT**: Enforce HTTPS in Production

**Current implementation allows HTTP. Consider:**
```python
def require_https(datasette, request):
    """Middleware to enforce HTTPS in production"""
    if datasette.setting("force_https_urls") and not request.url.scheme == "https":
        if request.url.hostname not in ("localhost", "127.0.0.1"):
            raise Forbidden("HTTPS required")

# Add to middleware chain
```

**Security impact:**
Data transmitted in plaintext over HTTP can be intercepted.

**Compliance:**
GDPR Article 32, CWE-319

---

#### **DEPS-UPDATE**: Dependency Security Monitoring

**Recommendation:**
```python
# Add to pyproject.toml
[tool.safety]
continue-on-error = false
full-report = true

# Add to CI/CD pipeline
pip install safety
safety check --exit-code 1
```

**Security impact:**
Outdated dependencies may contain known vulnerabilities.

**Compliance:**
OWASP A6 (Vulnerable and Outdated Components)

---

#### **AUTHZ-CHECK**: Enhanced Permission Validation

**Current code has permission checks, but consider strengthening:**
```python
async def check_permission_with_audit(datasette, actor, action, resource=None):
    """Enhanced permission check with audit logging"""
    result = await datasette.permission_allowed(actor, action, resource)
    
    # Log all permission decisions for security audit
    log_permission_decision(
        actor_id=actor.get("id") if actor else "anonymous",
        action=action,
        resource=str(resource),
        allowed=result,
        timestamp=datetime.utcnow(),
        ip_address=getattr(g, 'request_ip', 'unknown')
    )
    
    return result
```

**Security impact:**
Better audit trail for security investigations.

**Compliance:**
GDPR Article 30, SOC 2

---

### 📋 Compliance Checklist

- [x] **OWASP Top 10 - A1 Injection**: SQL injection prevented through parameterized queries ✅
- [x] **OWASP Top 10 - A2 Auth**: Token-based authentication implemented ✅
- [ ] **OWASP Top 10 - A3 XSS**: Template auto-escaping needs verification ⚠️
- [x] **OWASP Top 10 - A4 XXE**: Uses JSON primarily, limited XML usage ✅
- [ ] **OWASP Top 10 - A5 Security Config**: Missing security headers 🔴
- [ ] **OWASP Top 10 - A6 Vulnerable Components**: Need dependency scanning ⚠️
- [x] **OWASP Top 10 - A7 Insufficient Auth**: Permission system in place ✅
- [x] **OWASP Top 10 - A8 CSRF**: CSRF protection implemented ✅
- [ ] **OWASP Top 10 - A9 Known Vulns**: Need regular security updates ⚠️
- [ ] **OWASP Top 10 - A10 Insufficient Logging**: Need security event logging ⚠️

### Privacy Compliance

- [ ] **GDPR Article 25**: Privacy by design needs improvement ⚠️
- [x] **GDPR Article 32**: Basic security measures in place ✅
- [ ] **Data Minimization**: No clear data retention policies visible ⚠️
- [ ] **Audit Trail**: Enhanced logging recommended for GDPR compliance 💡

### Summary

Datasette shows good security fundamentals with proper SQL injection prevention and CSRF protection. However, critical issues exist around CORS configuration and missing security headers that should be addressed immediately. The codebase would benefit from enhanced security monitoring, stricter HTTPS enforcement, and better audit logging for compliance requirements.


---

*Generated by Claude Code Skills Review Tool using claude*
