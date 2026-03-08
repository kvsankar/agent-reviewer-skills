## Security & Privacy Review: services.py

### ✅ Strengths
- **TRANSACTION-SAFE**: Proper use of `@transaction.atomic` decorator for data consistency in `create_user_contact`
- **ORM-SAFE**: Uses Django ORM which provides protection against SQL injection
- **TYPE-HINTS**: Good use of type hints for better code clarity and some type safety

### 🔴 Critical Issues (Immediate Fix Required)

#### **AUTHZ-CHECK**: Missing Authorization Checks

**Vulnerable code:**
```python
@classmethod
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # No check if caller has permission to create contacts for this user!
    allowed_methods = cls.get_allowed_auth_methods(user)
    # ... creates contact for any user
```

**Secure implementation:**
```python
@classmethod
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, 
                       requesting_user: User, ...):
    # Check authorization first
    if not (requesting_user == user or requesting_user.is_staff):
        raise PermissionError("Not authorized to create contacts for this user")
    
    allowed_methods = cls.get_allowed_auth_methods(user)
    # ... rest of method
```

**Security impact:**
Any authenticated user could potentially create, verify, or modify contacts for any other user. This violates the principle of least privilege and could lead to unauthorized access or account takeover.

**Compliance:**
OWASP A1 (Broken Access Control), CWE-862 (Missing Authorization)

---

#### **PII-ENCRYPT**: Sensitive Data Not Encrypted at Rest

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

CONTACT_ENCRYPTION_KEY = os.environ['CONTACT_ENCRYPTION_KEY'].encode()

def encrypt_contact_value(value: str) -> bytes:
    f = Fernet(CONTACT_ENCRYPTION_KEY)
    return f.encrypt(value.encode())

def decrypt_contact_value(encrypted_value: bytes) -> str:
    f = Fernet(CONTACT_ENCRYPTION_KEY)
    return f.decrypt(encrypted_value).decode()

contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value=encrypt_contact_value(contact_value),
    # ...
)
```

**Security impact:**
Email addresses and phone numbers are PII. Database breaches would expose this sensitive information in plaintext.

**Compliance:**
GDPR Article 32 (Security of Processing), PCI DSS (if applicable), CWE-311

---

### ⚠️ Warnings (Should Fix)

#### **VALIDATE-INPUT**: Missing Input Validation

**Vulnerable code:**
```python
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # No validation of contact_value format!
    contact = UserContact.objects.create(contact_value=contact_value, ...)
```

**Secure implementation:**
```python
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_contact_value(contact_type: str, contact_value: str) -> None:
    if contact_type == ContactType.EMAIL:
        validate_email(contact_value)
    elif contact_type == ContactType.PHONE:
        # Sanitize and validate phone number
        phone_pattern = re.compile(r'^\+?1?[0-9]{10,15}$')
        clean_phone = re.sub(r'[^\d+]', '', contact_value)
        if not phone_pattern.match(clean_phone):
            raise ValidationError("Invalid phone number format")
    elif contact_type == ContactType.SAML_SSO:
        if not contact_value or len(contact_value) > 255:
            raise ValidationError("Invalid SSO ID")

def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    validate_contact_value(contact_type, contact_value)
    # ... rest of method
```

**Security impact:**
Invalid data could cause application errors or bypass security checks. Malformed emails/phones could be used for injection attacks downstream.

**Compliance:**
OWASP A3 (Injection), CWE-20

---

#### **AUDIT-TRAIL**: No Audit Logging for Sensitive Operations

**Vulnerable code:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None):
    contact.is_verified = True
    contact.verified_at = timezone.now()
    # No audit log of this critical security event!
```

**Secure implementation:**
```python
import logging

security_logger = logging.getLogger('security')

def verify_contact(cls, contact: UserContact, verified_by: User | None = None):
    old_status = contact.is_verified
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
    
    # Audit log
    security_logger.info(
        "Contact verified",
        extra={
            "event": "contact_verified",
            "user_id": contact.user.id,
            "contact_type": contact.contact_type,
            "contact_id": contact.id,
            "verified_by": verified_by.id if verified_by else None,
            "previous_status": old_status
        }
    )
```

**Security impact:**
No trail of who verified contacts when. Critical for compliance and incident response.

**Compliance:**
GDPR Article 30 (Records of Processing), SOX, PCI DSS

---

#### **ERROR-SAFE**: Information Disclosure in Error Messages

**Vulnerable code:**
```python
if contact_type not in allowed_methods:
    raise ValidationError(
        f"Contact type '{contact_type}' is not allowed for user type '{user.user_type}'"
    )
```

**Secure implementation:**
```python
if contact_type not in allowed_methods:
    # Log detailed error internally
    logger.warning(
        f"Unauthorized contact type attempt: {contact_type} for user {user.id}"
    )
    # Generic error to user
    raise ValidationError("Contact type not allowed")
```

**Security impact:**
Error messages reveal internal system information (user types, policies) that could aid attackers.

**Compliance:**
CWE-209 (Information Exposure Through Error Messages)

---

### 💡 Recommendations (Best Practices)

#### **SIZE-LIMIT**: Implement Input Size Limits

```python
MAX_CONTACT_VALUE_LENGTH = 255
MAX_PHONE_LENGTH = 20

def validate_contact_value(contact_type: str, contact_value: str) -> None:
    if len(contact_value) > MAX_CONTACT_VALUE_LENGTH:
        raise ValidationError("Contact value too long")
    # ... type-specific validation
```

#### **RATE-LIMIT**: Add Rate Limiting for Contact Creation

```python
from django.core.cache import cache

def create_user_contact(cls, user: User, contact_type: str, ...):
    # Rate limit contact creation
    cache_key = f"contact_creation:{user.id}"
    attempts = cache.get(cache_key, 0)
    if attempts >= 5:  # Max 5 contacts per hour
        raise ValidationError("Too many contact creation attempts")
    cache.set(cache_key, attempts + 1, 3600)
    # ... rest of method
```

#### **DATA-RETENTION**: Add Data Retention Policies

```python
def cleanup_old_unverified_contacts():
    """Remove unverified contacts older than 30 days"""
    cutoff = timezone.now() - timedelta(days=30)
    UserContact.objects.filter(
        is_verified=False,
        created_at__lt=cutoff
    ).delete()
```

---

### 📋 Compliance Checklist
- [ ] **OWASP Top 10 compliance** - Missing authorization checks (A1)
- [ ] **PII properly protected** - Contact values need encryption
- [x] **GDPR requirements met** - Has some privacy controls but needs audit trails
- [ ] **Secrets not in code** - Will need encryption keys in environment
- [ ] **Dependencies up to date** - Not directly applicable to this service layer

**Priority:** Fix authorization checks and PII encryption immediately, then add input validation and audit logging.
