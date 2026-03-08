# Security & Privacy Review: services.py

## ✅ Strengths
- **SQL-INJECT**: Uses Django ORM throughout, preventing SQL injection vulnerabilities
- **MFA-SUPPORT**: Implements MFA requirement checking and method selection logic
- **TYPE-CHECK**: Uses modern Python type hints for better code clarity

## 🔴 Critical Issues (Immediate Fix Required)

### **AUTHZ-CHECK**: Missing Authorization Checks

**Vulnerable code:**
```python
@classmethod
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    # No check if caller can access this user's policy!
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
```

**Secure implementation:**
```python
@classmethod
def get_user_policy(cls, user: User, requesting_user: User) -> AuthMethodPolicy | None:
    # Check authorization first
    if not can_access_user_data(requesting_user, user):
        raise PermissionError("Unauthorized access to user policy")
    
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
```

**Security impact:**
This creates IDOR (Insecure Direct Object Reference) vulnerabilities. Any authenticated user could potentially access authentication policies, contact information, and capabilities of other users by calling these service methods with different user objects.

**Compliance:**
OWASP A1 (Broken Access Control), CWE-862

---

### **PII-ENCRYPT**: PII Stored in Plaintext

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

def encrypt_pii(data: str) -> bytes:
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(data.encode())

def decrypt_pii(encrypted: bytes) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(encrypted).decode()

# Update model to store encrypted data
contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value_encrypted=encrypt_pii(contact_value),
    # ...
)
```

**Security impact:**
Email addresses and phone numbers are PII that must be encrypted at rest. Database compromise would expose all user contact information in plaintext.

**Compliance:**
GDPR Article 32, CWE-311

---

### **VALIDATE-INPUT**: No Input Validation

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
        try:
            validate_email(contact_value)
        except ValidationError:
            raise ValidationError("Invalid email format")
    
    elif contact_type == ContactType.PHONE:
        # Validate phone number format
        phone_pattern = r'^\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
        if not re.match(phone_pattern, contact_value.strip()):
            raise ValidationError("Invalid phone number format")
    
    # Limit input size
    if len(contact_value) > 255:
        raise ValidationError("Contact value too long")
    
    return contact_value.strip()

def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    # ...
):
    # Validate input
    validated_value = validate_contact_value(contact_type, contact_value)
    # ... rest of method
```

**Security impact:**
Unvalidated input could lead to data corruption, injection attacks in downstream systems, or denial of service through oversized inputs.

**Compliance:**
CWE-20, OWASP A3

---

## ⚠️ Warnings (Should Fix)

### **PII-IDENTIFY**: PII Not Marked or Inventoried

**Vulnerable code:**
```python
@dataclass
class UserContact:
    contact_value: str  # PII not marked!
```

**Secure implementation:**
```python
from typing import Annotated

PII = 'pii'
SENSITIVE_PII = 'sensitive_pii'

@dataclass
class UserContact:
    contact_value: Annotated[str, PII]  # Mark as PII
    # Document in data inventory
    
# Maintain PII inventory
PII_FIELDS = {
    'UserContact': {
        'fields': ['contact_value'],
        'classification': 'CONFIDENTIAL',
        'purpose': 'Authentication and communication',
        'retention': '2 years after account closure'
    }
}
```

**Security impact:**
Without PII identification, developers may not apply appropriate protection measures, violating privacy regulations.

**Compliance:**
GDPR Article 30 (Records of processing activities)

---

### **AUDIT-TRAIL**: No Security Event Logging

**Vulnerable code:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    contact.is_verified = True
    # No audit log of this security event!
```

**Secure implementation:**
```python
import logging

security_logger = logging.getLogger('security.authentication')

def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    # Log security event
    security_logger.info(
        "Contact verification",
        extra={
            'event': 'contact_verified',
            'user_id': contact.user.id,
            'contact_type': contact.contact_type,
            'contact_hash': hash(contact.contact_value)[:8],  # Don't log PII
            'verified_by': verified_by.id if verified_by else None,
            'timestamp': timezone.now().isoformat()
        }
    )
    
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
```

**Security impact:**
No audit trail makes it impossible to detect unauthorized contact modifications or investigate security incidents.

**Compliance:**
GDPR Article 32, SOX compliance requirements

---

### **ERROR-SAFE**: Inconsistent Error Handling

**Vulnerable code:**
```python
def get_primary_contact(cls, user: User, contact_type: str) -> UserContact | None:
    return UserContact.objects.filter(
        user=user, contact_type=contact_type, is_primary=True
    ).first()  # Could raise database errors
```

**Secure implementation:**
```python
def get_primary_contact(cls, user: User, contact_type: str) -> UserContact | None:
    try:
        return UserContact.objects.filter(
            user=user, contact_type=contact_type, is_primary=True
        ).first()
    except Exception as e:
        logger.error(f"Error retrieving primary contact: {e}", exc_info=True)
        return None
```

**Security impact:**
Unhandled database exceptions could expose sensitive information or cause application crashes.

**Compliance:**
CWE-755

---

## 💡 Recommendations (Best Practices)

### **DATA-RETENTION**: Implement Data Retention Policy

**Current code:**
```python
# Contacts stored indefinitely
```

**Recommended implementation:**
```python
from datetime import timedelta

class UserContact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # Add retention tracking
    
    @property
    def should_delete(self):
        # Delete contacts 2 years after user account closure
        if self.user.is_deleted:
            deletion_date = self.user.deleted_at + timedelta(days=730)
            return timezone.now() > deletion_date
        return False

def cleanup_expired_contacts():
    """Remove contacts past retention period."""
    expired_contacts = UserContact.objects.filter(
        user__is_deleted=True,
        user__deleted_at__lt=timezone.now() - timedelta(days=730)
    )
    count = expired_contacts.count()
    expired_contacts.delete()
    logger.info(f"Cleaned up {count} expired contacts")
```

**Compliance:**
GDPR Article 5(1)(e) (Storage limitation)

---

### **ORM-TENANT**: Add Tenant Filtering for Multi-Tenant Applications

**Current code:**
```python
UserContact.objects.filter(user=user, contact_type=contact_type)
```

**Recommended implementation:**
```python
# If this is a multi-tenant application
def get_tenant_aware_queryset(user: User, requesting_user: User):
    """Ensure queries are scoped to the correct tenant."""
    base_query = UserContact.objects.filter(user=user)
    
    # Add tenant filtering if needed
    if hasattr(user, 'tenant_id') and hasattr(requesting_user, 'tenant_id'):
        if user.tenant_id != requesting_user.tenant_id:
            raise PermissionError("Cross-tenant access denied")
        base_query = base_query.filter(user__tenant_id=requesting_user.tenant_id)
    
    return base_query
```

**Security impact:**
Prevents accidental cross-tenant data access in multi-tenant applications.

---

### **CONSENT-LOG**: Implement Consent Logging

**Current code:**
```python
# No consent handling for contact collection
```

**Recommended implementation:**
```python
@dataclass
class ConsentRecord:
    user_id: str
    purpose: str
    granted: bool
    timestamp: datetime
    contact_type: str

def create_user_contact(cls, user, contact_type, contact_value, **kwargs):
    # Log consent for contact collection
    ConsentRecord.create(
        user_id=user.id,
        purpose='authentication',
        granted=True,
        timestamp=timezone.now(),
        contact_type=contact_type
    )
    # ... rest of method
```

**Compliance:**
GDPR Article 7 (Consent requirements)

---

## 📋 Compliance Checklist
- [ ] **OWASP Top 10 compliance** - Missing access control (A1), input validation (A3)
- [ ] **PII properly protected** - Not encrypted at rest
- [ ] **GDPR requirements met** - Missing consent logging, data inventory, retention policy
- [ ] **Access control implemented** - Missing authorization checks
- [ ] **Audit trail maintained** - No security event logging

## Summary

This authentication service has significant security gaps around **authorization controls** and **PII protection**. The most critical issues are the lack of authorization checks (allowing IDOR attacks) and storing PII in plaintext. Input validation is also completely missing, creating potential injection and DoS vectors.

**Priority fixes:**
1. Add authorization checks to all service methods
2. Implement PII encryption at rest
3. Add comprehensive input validation
4. Implement security event logging
5. Add data retention and consent management
