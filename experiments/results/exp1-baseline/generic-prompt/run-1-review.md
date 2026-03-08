# Security Review: Django Authentication Service

## Executive Summary

The authentication service contains several **CRITICAL** and **HIGH** severity vulnerabilities that could lead to privilege escalation, data injection, and authorization bypass. The most concerning issues involve lack of input validation, weak authorization controls, and potential race conditions in critical authentication flows.

---

## Critical Vulnerabilities

### 1. PRIV-ESCALATION - Authorization Bypass for Internal Users
**CWE-863: Incorrect Authorization**  
**Severity: CRITICAL**

**Vulnerable Code:**
```python
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    policy = cls.get_user_policy(user)
    if policy:
        return policy.allowed_methods
    # For internal users without a specific policy (e.g., new SSO users
    # who haven't been assigned a role yet), default to email
    if user.user_type == UserType.INT_USER:
        return [ContactType.EMAIL]
    return []
```

**Secure Alternative:**
```python
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    policy = cls.get_user_policy(user)
    if policy:
        return policy.allowed_methods
    
    # Require explicit role assignment for all users
    # No default permissions for unassigned users
    return []
```

**Attack Scenario:**
An attacker who gains access to create `INT_USER` accounts without role assignments automatically gets email authentication capabilities, bypassing the role-based access control system. This violates the principle of least privilege.

---

### 2. INPUT-INJECT - Unvalidated Contact Values
**CWE-20: Improper Input Validation**  
**Severity: CRITICAL**

**Vulnerable Code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No validation
    is_primary: bool = False,
    # ...
) -> UserContact:
```

**Secure Alternative:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    is_primary: bool = False,
    # ...
) -> UserContact:
    # Validate contact_type is a valid ContactType
    if contact_type not in [choice[0] for choice in ContactType.choices]:
        raise ValidationError(f"Invalid contact type: {contact_type}")
    
    # Validate contact_value based on type
    if contact_type == ContactType.EMAIL:
        from django.core.validators import validate_email
        validate_email(contact_value)
    elif contact_type == ContactType.PHONE:
        if not re.match(r'^\+?1?\d{9,15}$', contact_value):
            raise ValidationError("Invalid phone number format")
    elif contact_type == ContactType.SAML_SSO:
        if len(contact_value) > 255 or not contact_value.strip():
            raise ValidationError("Invalid SSO identifier")
    
    # Sanitize input
    contact_value = contact_value.strip()[:255]
```

**Attack Scenario:**
Attackers can inject malicious payloads into contact values (emails, phone numbers) that could lead to XSS when displayed, injection attacks in downstream systems, or data corruption.

---

## High Severity Vulnerabilities

### 3. RACE-CONDITION - Primary Contact Race Condition
**CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization**  
**Severity: HIGH**

**Vulnerable Code:**
```python
@transaction.atomic
def create_user_contact(cls, ...):
    # If this is primary, unset other primary contacts of the same type
    if is_primary:
        UserContact.objects.filter(
            user=user, contact_type=contact_type, is_primary=True
        ).update(is_primary=False)
    
    # Create the contact
    contact = UserContact.objects.create(...)
```

**Secure Alternative:**
```python
@transaction.atomic
def create_user_contact(cls, ...):
    if is_primary:
        # Use select_for_update to prevent race conditions
        UserContact.objects.filter(
            user=user, contact_type=contact_type, is_primary=True
        ).select_for_update().update(is_primary=False)
    
    contact = UserContact.objects.create(...)
```

**Attack Scenario:**
Concurrent requests to create primary contacts could result in multiple primary contacts of the same type, breaking business logic and potentially bypassing authentication controls.

---

### 4. INFO-DISCLOSURE - Detailed Error Messages
**CWE-209: Information Exposure Through Error Messages**  
**Severity: HIGH**

**Vulnerable Code:**
```python
if contact_type not in allowed_methods:
    raise ValidationError(
        f"Contact type '{contact_type}' is not allowed for user type '{user.user_type}'"
    )
```

**Secure Alternative:**
```python
if contact_type not in allowed_methods:
    raise ValidationError("Contact type not permitted")
    # Log detailed info for admins only
    logger.warning(
        f"Unauthorized contact creation attempt",
        extra={
            'user_id': user.id,
            'contact_type': contact_type,
            'user_type': user.user_type
        }
    )
```

**Attack Scenario:**
Error messages reveal the internal user type and allowed contact types, helping attackers understand the authorization model and plan privilege escalation attacks.

---

### 5. NO-AUDIT - Missing Security Audit Trail
**CWE-778: Insufficient Logging**  
**Severity: HIGH**

**Vulnerable Code:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
    # No audit logging
```

**Secure Alternative:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
    
    # Audit critical security event
    logger.info(
        "Contact verified",
        extra={
            'contact_id': contact.id,
            'user_id': contact.user.id,
            'contact_type': contact.contact_type,
            'verified_by': verified_by.id if verified_by else None,
            'timestamp': timezone.now().isoformat()
        }
    )
```

**Attack Scenario:**
Lack of audit logging makes it impossible to detect or investigate unauthorized contact verifications, privilege escalations, or other security incidents.

---

## Medium Severity Vulnerabilities

### 6. ROLE-BYPASS - Weak Role Validation
**CWE-285: Improper Authorization**  
**Severity: MEDIUM**

**Vulnerable Code:**
```python
def setup_technician_contacts(cls, user: User, phone: str) -> None:
    has_tech_role = UserRole.objects.filter(
        user=user, role=Role.EXT_PARTNER_TECH, is_deleted=False
    ).exists()
    if not has_tech_role:
        raise ValueError("This method is only for users with EXT_PARTNER_TECH role")
```

**Secure Alternative:**
```python
def setup_technician_contacts(cls, user: User, phone: str) -> None:
    # Check both role assignment and user type for defense in depth
    has_tech_role = UserRole.objects.filter(
        user=user, role=Role.EXT_PARTNER_TECH, is_deleted=False
    ).exists()
    
    if not has_tech_role or user.user_type != UserType.EXT_PARTNER_STAFF:
        raise PermissionError("Insufficient privileges for technician contact setup")
```

**Attack Scenario:**
An attacker who can manipulate role assignments might bypass user type checks, potentially setting up technician contacts for unauthorized user types.

---

### 7. LENGTH-DOS - No Input Length Limits
**CWE-770: Allocation of Resources Without Limits or Throttling**  
**Severity: MEDIUM**

**Vulnerable Code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No length validation
    # ...
```

**Secure Alternative:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    # ...
):
    # Enforce reasonable length limits
    if len(contact_value) > 255:
        raise ValidationError("Contact value exceeds maximum length")
    
    if len(contact_type) > 50:
        raise ValidationError("Contact type exceeds maximum length")
```

**Attack Scenario:**
Attackers could submit extremely long contact values, potentially causing memory exhaustion, database performance issues, or application crashes.

---

## Recommendations

### Immediate Actions (Critical)
1. **Remove default permissions** for unassigned internal users
2. **Implement comprehensive input validation** for all contact values
3. **Add select_for_update** to prevent race conditions in primary contact assignment
4. **Sanitize error messages** to prevent information disclosure

### Short Term (High Priority)
1. **Implement comprehensive audit logging** for all authentication operations
2. **Add rate limiting** to prevent brute force attacks on contact creation
3. **Implement proper exception handling** with sanitized error messages

### Medium Term
1. **Add input length validation** and resource limits
2. **Implement defense-in-depth** role validation
3. **Add monitoring and alerting** for suspicious authentication activities
4. **Regular security testing** of authentication flows

### Security Headers and Configuration
- Ensure Django's `SECRET_KEY` is properly randomized and protected
- Use HTTPS for all authentication-related operations
- Implement proper session management with secure cookie flags
- Consider implementing CSRF protection for state-changing operations
