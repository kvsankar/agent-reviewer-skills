## Security & Privacy Review: services.py

### ✅ Strengths
- **MFA-SUPPORT**: Good multi-factor authentication support with `requires_mfa()` and `get_mfa_methods()` methods
- **SESSION-SECURE**: Proper session management with configurable duration and inactivity timeouts
- **SQL-INJECT**: Uses Django ORM with parameterized queries, preventing SQL injection

### 🔴 Critical Issues (Immediate Fix Required)

#### PII-ENCRYPT: Contact Information Stored in Plaintext

**Vulnerable code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # Stored in plaintext!
    # ...
) -> UserContact:
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=contact_value,  # PII stored unencrypted
        # ...
    )
```

**Secure implementation:**
```python
from cryptography.fernet import Fernet
import os

CONTACT_ENCRYPTION_KEY = os.environ['CONTACT_ENCRYPTION_KEY'].encode()

def encrypt_contact_value(value: str) -> str:
    """Encrypt contact information for storage."""
    f = Fernet(CONTACT_ENCRYPTION_KEY)
    return f.encrypt(value.encode()).decode()

def decrypt_contact_value(encrypted_value: str) -> str:
    """Decrypt contact information for use."""
    f = Fernet(CONTACT_ENCRYPTION_KEY)
    return f.decrypt(encrypted_value.encode()).decode()

@classmethod
@transaction.atomic
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    # ...
) -> UserContact:
    # Encrypt PII before storage
    encrypted_value = encrypt_contact_value(contact_value)
    
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=encrypted_value,  # Store encrypted
        # ...
    )
```

**Security impact:**
Email addresses and phone numbers are PII that could be exposed in data breaches. Storing them in plaintext violates data protection principles.

**Compliance:**
GDPR Article 32 (Security of processing), PCI DSS if handling payment-related contacts

---

#### VALIDATE-INPUT: No Validation of Contact Values

**Vulnerable code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No validation!
    # ...
):
    # Direct storage without validation
    contact = UserContact.objects.create(
        contact_value=contact_value,
        # ...
    )
```

**Secure implementation:**
```python
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_contact_value(contact_type: str, contact_value: str) -> str:
    """Validate contact values based on type."""
    if contact_type == ContactType.EMAIL:
        try:
            validate_email(contact_value)
        except ValidationError:
            raise ValidationError(f"Invalid email format: {contact_value}")
    
    elif contact_type == ContactType.PHONE:
        # Validate phone format (adjust regex as needed)
        if not re.match(r'^\+?1?[0-9]{10,15}$', contact_value.replace('-', '').replace(' ', '')):
            raise ValidationError(f"Invalid phone format: {contact_value}")
    
    elif contact_type == ContactType.SAML_SSO:
        # Validate SSO ID format
        if not re.match(r'^[a-zA-Z0-9@._-]+$', contact_value):
            raise ValidationError(f"Invalid SSO ID format: {contact_value}")
    
    # Sanitize common injection patterns
    if any(char in contact_value for char in ['<', '>', '"', "'"]):
        raise ValidationError("Contact value contains invalid characters")
    
    return contact_value.strip()

@classmethod
@transaction.atomic
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    # ...
) -> UserContact:
    # Validate input
    validated_value = validate_contact_value(contact_type, contact_value)
    
    # Check if this contact type is allowed by policy
    allowed_methods = cls.get_allowed_auth_methods(user)
    if contact_type not in allowed_methods:
        raise ValidationError(
            f"Contact type '{contact_type}' is not allowed for user type '{user.user_type}'"
        )
```

**Security impact:**
Unvalidated inputs could lead to data corruption, injection attacks, or storing malformed data that breaks authentication flows.

**Compliance:**
CWE-20 (Improper Input Validation), OWASP A3 (Injection)

---

#### AUTHZ-CHECK: Missing Authorization Checks

**Vulnerable code:**
```python
@classmethod
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    """Mark a user contact as verified."""
    # No check if current user can verify this contact!
    contact.is_verified = True
    contact.save()

@classmethod
def get_user_capabilities(cls, user: User) -> list[str]:
    # No check if current user can access this user's data!
    return list(
        UserContact.objects.filter(user=user, can_authenticate=True)
        .values_list("contact_type", flat=True)
        .distinct()
    )
```

**Secure implementation:**
```python
from django.contrib.auth import get_user
from django.core.exceptions import PermissionDenied

@classmethod
def verify_contact(cls, contact: UserContact, verified_by: User, current_user: User) -> None:
    """Mark a user contact as verified."""
    # Check authorization
    if not current_user.has_perm('auth.verify_contact'):
        raise PermissionDenied("Not authorized to verify contacts")
    
    # Log the verification for audit trail
    import logging
    audit_logger = logging.getLogger('security.audit')
    audit_logger.info(
        "Contact verification",
        extra={
            'action': 'verify_contact',
            'contact_id': contact.id,
            'contact_type': contact.contact_type,
            'verified_by': verified_by.id,
            'user_id': contact.user.id
        }
    )
    
    contact.is_verified = True
    contact.verified_at = timezone.now()
    contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])

@classmethod
def get_user_capabilities(cls, user: User, requested_by: User) -> list[str]:
    """Get user capabilities with authorization check."""
    # Users can only see their own capabilities, or admins can see any
    if user != requested_by and not requested_by.has_perm('auth.view_user_capabilities'):
        raise PermissionDenied("Not authorized to view user capabilities")
        
    return list(
        UserContact.objects.filter(user=user, can_authenticate=True)
        .values_list("contact_type", flat=True)
        .distinct()
    )
```

**Security impact:**
Missing authorization checks could allow users to modify or access other users' authentication data, leading to account takeover.

**Compliance:**
OWASP A1 (Broken Access Control), CWE-862 (Missing Authorization)

---

### ⚠️ Warnings (Should Fix)

#### PII-IDENTIFY: PII Fields Not Clearly Marked

**Issue:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # This is PII but not marked
    # ...
):
```

**Secure implementation:**
```python
from typing import Annotated

# Mark PII fields clearly
PII = 'pii'
SENSITIVE_PII = 'sensitive_pii'

def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: Annotated[str, PII],  # Clearly marked as PII
    # ...
):
    """Create a new user contact.
    
    Args:
        contact_value: PII - Contact information (email/phone/SSO ID)
    """
```

**Compliance:**
GDPR Article 30 (Records of processing activities)

---

#### LOG-SANITIZE: Potential PII Exposure in Error Messages

**Vulnerable code:**
```python
if contact_type not in allowed_methods:
    raise ValidationError(
        f"Contact type '{contact_type}' is not allowed for user type '{user.user_type}'"
    )
    # Could log user type and contact type
```

**Secure implementation:**
```python
import logging
security_logger = logging.getLogger('security')

if contact_type not in allowed_methods:
    # Log without PII
    security_logger.warning(
        "Invalid contact type attempt",
        extra={
            'user_id_hash': hashlib.sha256(str(user.id).encode()).hexdigest()[:8],
            'contact_type': contact_type,  # This is not PII
            'allowed_methods_count': len(allowed_methods)
        }
    )
    # Generic error message to user
    raise ValidationError("Invalid contact type for your account")
```

**Compliance:**
GDPR Article 32, CWE-117 (Log Injection)

---

### 💡 Recommendations (Best Practices)

#### AUDIT-TRAIL: Add Comprehensive Audit Logging

**Current code:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    # No audit trail
    contact.is_verified = True
```

**Secure implementation:**
```python
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditEvent:
    timestamp: datetime
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    ip_address: str | None = None

def log_audit_event(event: AuditEvent):
    """Log security-relevant events."""
    audit_logger = logging.getLogger('security.audit')
    audit_logger.info(
        f"Security event: {event.action}",
        extra={
            'timestamp': event.timestamp.isoformat(),
            'user_id': event.user_id,
            'action': event.action,
            'resource_type': event.resource_type,
            'resource_id': event.resource_id,
            'ip_address': event.ip_address
        }
    )

@classmethod
def verify_contact(cls, contact: UserContact, verified_by: User, ip_address: str = None) -> None:
    """Mark a user contact as verified with audit trail."""
    log_audit_event(AuditEvent(
        timestamp=timezone.now(),
        user_id=str(verified_by.id),
        action='verify_contact',
        resource_type='user_contact',
        resource_id=str(contact.id),
        ip_address=ip_address
    ))
    
    contact.is_verified = True
    contact.verified_at = timezone.now()
    contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
```

---

#### MISSING-VALIDATION-LAYER: Centralized Validation

**Recommendation:**
```python
from pydantic import BaseModel, validator
from typing import Literal

class ContactValidation(BaseModel):
    contact_type: Literal['email', 'phone', 'saml_sso']
    contact_value: str
    
    @validator('contact_value')
    def validate_contact_value(cls, v, values):
        contact_type = values.get('contact_type')
        
        if contact_type == 'email':
            return cls._validate_email(v)
        elif contact_type == 'phone':
            return cls._validate_phone(v)
        elif contact_type == 'saml_sso':
            return cls._validate_sso_id(v)
        
        return v
    
    @staticmethod
    def _validate_email(email: str) -> str:
        from django.core.validators import validate_email
        validate_email(email)
        return email.lower().strip()
    
    @staticmethod
    def _validate_phone(phone: str) -> str:
        import re
        cleaned = re.sub(r'[^\d+]', '', phone)
        if not re.match(r'^\+?1?[0-9]{10,15}$', cleaned):
            raise ValueError("Invalid phone number format")
        return cleaned
```

---

### 📋 Compliance Checklist

- [ ] **OWASP A1** - Missing authorization checks identified
- [ ] **OWASP A3** - Input validation gaps found
- [x] **OWASP A8** - CSRF protection (framework level)
- [ ] **PII properly protected** - Contact values need encryption
- [ ] **GDPR requirements met** - Need PII marking and audit trails
- [x] **Secrets not in code** - No hardcoded secrets found
- [ ] **Dependencies up to date** - Cannot assess from this file

### Summary

The authentication service has a solid foundation with good MFA support and session management, but needs immediate attention for:

1. **Encrypt PII at rest** (contact values)
2. **Add input validation** for all contact values
3. **Implement authorization checks** for sensitive operations
4. **Add audit logging** for compliance
5. **Mark PII fields clearly** for data inventory

These fixes will bring the service into compliance with GDPR and OWASP security standards.
