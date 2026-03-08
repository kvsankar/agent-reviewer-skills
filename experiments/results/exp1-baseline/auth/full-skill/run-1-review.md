# Security & Privacy Review: services.py

## ✅ Strengths
- **USE-TRANSACTION**: Proper use of `@transaction.atomic` decorator for data consistency in `create_user_contact`
- **ORM-SAFE**: Using Django ORM parameterized queries prevents SQL injection
- **ROLE-SEPARATION**: Good separation of concerns with capability vs policy model

## 🔴 Critical Issues (Immediate Fix Required)

### PII-ENCRYPT: PII Stored in Plaintext

**Vulnerable code:**
```python
contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value=contact_value,  # Email/phone stored in plaintext!
    # ...
)
```

**Secure implementation:**
```python
from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.environ['PII_ENCRYPTION_KEY'].encode()

def encrypt_pii(data):
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(data.encode())

def decrypt_pii(encrypted):
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(encrypted).decode()

contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value=encrypt_pii(contact_value),  # Encrypt PII at rest
    # ...
)
```

**Security impact:**
Email addresses and phone numbers are stored in plaintext, violating GDPR Article 32 requirements for data protection. Database compromise exposes all PII immediately.

**Compliance:**
GDPR Article 32, PCI DSS (if processing payments), CWE-311

---

### VALIDATE-INPUT: No Input Validation for Contact Values

**Vulnerable code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No validation!
    # ...
):
```

**Secure implementation:**
```python
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_contact_value(contact_type: str, contact_value: str) -> str:
    """Validate contact value based on type."""
    if contact_type == ContactType.EMAIL:
        validate_email(contact_value)  # Django's email validator
        return contact_value.lower().strip()
    
    elif contact_type == ContactType.PHONE:
        # Remove non-digit characters and validate format
        cleaned = re.sub(r'[^\d+]', '', contact_value)
        if not re.match(r'^\+?[1-9]\d{6,14}$', cleaned):
            raise ValidationError("Invalid phone number format")
        return cleaned
    
    elif contact_type == ContactType.SAML_SSO:
        # Validate SSO ID format
        if not re.match(r'^[a-zA-Z0-9._@-]+$', contact_value):
            raise ValidationError("Invalid SSO identifier")
        return contact_value.strip()
    
    raise ValidationError(f"Unknown contact type: {contact_type}")

# In create_user_contact:
contact_value = validate_contact_value(contact_type, contact_value)
```

**Security impact:**
Malformed or malicious input could be stored and potentially cause issues downstream in authentication flows, email sending, or SMS services.

**Compliance:**
OWASP A3 (Injection), CWE-20

---

### AUTHZ-CHECK: Missing Authorization Checks

**Vulnerable code:**
```python
@classmethod
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    """Mark a user contact as verified."""
    contact.is_verified = True
    # No check if verified_by has permission!
```

**Secure implementation:**
```python
@classmethod
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    """Mark a user contact as verified."""
    if verified_by:
        # Check if user has permission to verify contacts
        if not verified_by.has_perm('users.can_verify_contacts'):
            raise PermissionDenied("User not authorized to verify contacts")
        
        # Check if user can verify this specific contact (e.g., same organization)
        if not cls._can_verify_contact(verified_by, contact):
            raise PermissionDenied("User not authorized to verify this contact")
    
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
    
    # Log security event
    cls._log_contact_verification(contact, verified_by)

@classmethod
def _can_verify_contact(cls, user: User, contact: UserContact) -> bool:
    """Check if user can verify specific contact."""
    # Implement business logic (same org, role hierarchy, etc.)
    return True  # Placeholder

@classmethod
def _log_contact_verification(cls, contact: UserContact, verified_by: User | None) -> None:
    """Log contact verification for audit."""
    import logging
    security_logger = logging.getLogger('security')
    security_logger.info(
        "Contact verified",
        extra={
            'contact_id': contact.id,
            'user_id': contact.user.id,
            'verified_by': verified_by.id if verified_by else None,
            'contact_type': contact.contact_type
        }
    )
```

**Security impact:**
Any user could potentially verify any contact if they can call this method, bypassing intended access controls.

**Compliance:**
OWASP A1 (Broken Access Control), CWE-862

---

## ⚠️ Warnings (Should Fix)

### AUDIT-TRAIL: Missing Security Event Logging

**Vulnerable code:**
```python
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # No audit logging for sensitive operations
    contact = UserContact.objects.create(...)
```

**Secure implementation:**
```python
import logging

security_logger = logging.getLogger('security')

def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # Create contact
    contact = UserContact.objects.create(...)
    
    # Log security event (with sanitized PII)
    security_logger.info(
        "User contact created",
        extra={
            'user_id': user.id,
            'contact_type': contact_type,
            'contact_value_hash': hashlib.sha256(contact_value.encode()).hexdigest()[:8],
            'is_primary': is_primary,
            'can_authenticate': kwargs.get('can_authenticate', False)
        }
    )
    
    return contact
```

**Security impact:**
No audit trail for authentication-related changes makes it impossible to detect unauthorized modifications or investigate security incidents.

**Compliance:**
GDPR Article 30, SOX, PCI DSS

---

### SIZE-LIMIT: No Input Size Limits

**Vulnerable code:**
```python
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # contact_value could be extremely long
```

**Secure implementation:**
```python
MAX_CONTACT_VALUE_LENGTH = 255

def validate_contact_value(contact_type: str, contact_value: str) -> str:
    if len(contact_value) > MAX_CONTACT_VALUE_LENGTH:
        raise ValidationError(f"Contact value too long (max {MAX_CONTACT_VALUE_LENGTH} chars)")
    
    # ... rest of validation
```

**Security impact:**
Large inputs could cause memory exhaustion or database issues.

**Compliance:**
CWE-770

---

### TIMING-ATTACK: User Enumeration Risk

**Vulnerable code:**
```python
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
    if not role_assignment:
        return None  # Different timing than when role exists
```

**Secure implementation:**
```python
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    try:
        role_assignment = UserRole.objects.select_related('role').get(
            user=user, 
            is_deleted=False
        )
        return AuthMethodPolicy.objects.get(role=role_assignment.role)
    except (UserRole.DoesNotExist, AuthMethodPolicy.DoesNotExist):
        # Always perform database lookup to normalize timing
        AuthMethodPolicy.objects.filter(role__isnull=True).first()
        return None
```

**Security impact:**
Timing differences could allow attackers to enumerate valid users or roles.

**Compliance:**
CWE-208

---

## 💡 Recommendations (Best Practices)

### PII-IDENTIFY: Explicit PII Classification

**Current code:**
```python
# PII fields not explicitly marked
contact_value=contact_value,
```

**Suggested improvement:**
```python
from typing import Annotated
from dataclasses import dataclass

PII = 'pii'
SENSITIVE_PII = 'sensitive_pii'

@dataclass
class ContactData:
    user_id: str  # Not PII
    contact_type: str  # Not PII  
    contact_value: Annotated[str, PII]  # Mark as PII
    phone_number: Annotated[str, SENSITIVE_PII]  # More sensitive
    
# Document PII inventory
PII_FIELDS = {
    'UserContact': ['contact_value'],
    'User': ['first_name', 'last_name', 'email']
}
```

**Why:** GDPR Article 30 requires data inventory and classification.

---

### DATA-RETENTION: Implement Retention Policies

**Suggested implementation:**
```python
from datetime import datetime, timedelta

class ContactRetentionService:
    @classmethod
    def cleanup_expired_contacts(cls):
        """Remove contacts for deleted users after retention period."""
        cutoff = datetime.now() - timedelta(days=365)  # 1 year retention
        
        expired_contacts = UserContact.objects.filter(
            user__is_deleted=True,
            user__deleted_at__lt=cutoff
        )
        
        for contact in expired_contacts:
            cls._log_contact_deletion(contact, "retention_policy")
            contact.delete()
```

**Why:** GDPR Article 5(1)(e) requires data not be kept longer than necessary.

---

### RATE-LIMIT: Authentication Method Changes

**Suggested implementation:**
```python
from django.core.cache import cache

class AuthenticationService:
    @classmethod
    def create_user_contact(cls, user: User, contact_type: str, ...):
        # Rate limit contact creation
        cache_key = f"contact_creation:{user.id}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:  # Max 5 contacts per hour
            raise ValidationError("Too many contact creation attempts")
        
        cache.set(cache_key, attempts + 1, 3600)  # 1 hour
        
        # ... rest of method
```

**Why:** Prevents abuse of contact creation and potential spam/DoS.

---

## 📋 Compliance Checklist

### Security
- [ ] ❌ SQL injection prevention (ORM used ✓, but validation missing)
- [ ] ❌ Input validation implemented  
- [ ] ❌ Authorization checks on sensitive operations
- [ ] ❌ Audit logging for security events
- [ ] ❌ Rate limiting for sensitive operations
- [ ] ❌ PII encrypted at rest

### Privacy (GDPR)
- [ ] ❌ PII properly identified and classified
- [ ] ❌ Data retention policies implemented
- [ ] ❌ PII encryption at rest
- [ ] ❌ Audit trail for PII access
- [ ] ❌ Data minimization principles applied

### Framework (Django)
- [ ] ✅ ORM parameterized queries used
- [ ] ✅ Transaction handling implemented
- [ ] ❌ Permission system integration
- [ ] ❌ Security logging configured

## Summary

This authentication service handles sensitive PII and authentication logic but lacks critical security controls. **Priority fixes:**

1. **Encrypt PII at rest** (emails, phone numbers)
2. **Add input validation** for all contact values  
3. **Implement authorization checks** for sensitive operations
4. **Add security event logging** for audit trails

The code shows good Django practices but needs security hardening before production deployment.
