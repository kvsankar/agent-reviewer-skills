Looking at this Django authentication service code, I need to run a comprehensive security and privacy review. Let me analyze the code systematically.

<sub_task>
<Task subagent_type="Explore" prompt="Review the Django authentication service code in services.py for security vulnerabilities and privacy issues. Focus on input validation, PII handling, authorization checks, and data protection. Write a detailed security review report to services-security-review.md">

## Security & Privacy Review: services.py

### ✅ Strengths
- **SQL-INJECT**: Proper use of Django ORM prevents SQL injection vulnerabilities
- **ATOMIC-TRANS**: Uses `@transaction.atomic` decorator for data consistency in `create_user_contact`
- **ROLE-VALIDATE**: Good role validation checks in setup methods (`setup_technician_contacts`, `setup_partner_staff_contacts`)
- **SESSION-SECURE**: Implements session duration and inactivity timeout controls
- **MFA-SUPPORT**: Proper MFA requirement checking and method intersection logic

### 🔴 Critical Issues (Immediate Fix Required)

#### **INPUT-VALIDATE**: Missing Input Validation for Contact Values

**Vulnerable code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No validation!
    is_primary: bool = False,
    is_verified: bool = False,
    can_receive_otp: bool = False,
    **kwargs,
) -> UserContact:
```

**Secure implementation:**
```python
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    is_primary: bool = False,
    is_verified: bool = False,
    can_receive_otp: bool = False,
    **kwargs,
) -> UserContact:
    # Validate contact value based on type
    if contact_type == ContactType.EMAIL:
        try:
            validate_email(contact_value)
        except ValidationError:
            raise ValidationError("Invalid email address format")
    elif contact_type == ContactType.PHONE:
        if not re.match(r'^\+?1?[0-9]{10,15}$', contact_value):
            raise ValidationError("Invalid phone number format")
    
    # Limit contact_value length
    if len(contact_value) > 255:
        raise ValidationError("Contact value too long")
```

**Security impact:**
Attackers could inject malformed data, potentially causing application errors or database corruption. Invalid email/phone formats could break downstream systems.

**Compliance:**
OWASP A3 (Injection), CWE-20 (Input Validation)

---

#### **PII-ENCRYPT**: Contact Information Not Encrypted at Rest

**Vulnerable code:**
```python
contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value=contact_value,  # Stored in plaintext!
    # ...
)
```

**Secure implementation:**
```python
from cryptography.fernet import Fernet
import os

class AuthenticationService:
    ENCRYPTION_KEY = os.environ['CONTACT_ENCRYPTION_KEY'].encode()
    
    @classmethod
    def _encrypt_contact_value(cls, value: str) -> bytes:
        f = Fernet(cls.ENCRYPTION_KEY)
        return f.encrypt(value.encode())
    
    @classmethod
    def _decrypt_contact_value(cls, encrypted_value: bytes) -> str:
        f = Fernet(cls.ENCRYPTION_KEY)
        return f.decrypt(encrypted_value).decode()
    
    def create_user_contact(cls, ...):
        encrypted_value = cls._encrypt_contact_value(contact_value)
        contact = UserContact.objects.create(
            contact_value=encrypted_value,
            # ...
        )
```

**Security impact:**
Database breach exposes all user contact information (emails, phone numbers) in plaintext, violating privacy regulations.

**Compliance:**
GDPR Article 32 (Security of Processing), PCI DSS if handling payment-related contacts

---

#### **AUTHZ-CHECK**: Missing Authorization Checks on Sensitive Methods

**Vulnerable code:**
```python
@classmethod
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    # No check if caller is authorized to access this user's policy!
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
```

**Secure implementation:**
```python
@classmethod
def get_user_policy(cls, user: User, requesting_user: User) -> AuthMethodPolicy | None:
    # Check authorization
    if requesting_user != user and not requesting_user.has_perm('users.view_user_policy'):
        raise PermissionDenied("Not authorized to access user policy")
    
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
    # ...
```

**Security impact:**
Unauthorized users could access authentication policies and capabilities of other users, leading to information disclosure and potential privilege escalation.

**Compliance:**
OWASP A1 (Broken Access Control), CWE-862 (Missing Authorization)

---

### ⚠️ Warnings (Should Fix)

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
    raise ValidationError("Contact type not allowed for this user")
```

**Security impact:**
Error messages reveal internal user types and allowed methods, providing attackers with system reconnaissance information.

**Compliance:**
CWE-209 (Information Exposure Through Error Messages)

---

#### **PII-LOG**: No Safeguards Against PII Logging

**Vulnerable code:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    # Contact value (PII) could be logged by Django/audit systems
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
```

**Secure implementation:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None) -> None:
    # Ensure PII is not logged
    with override_settings(LOGGING_CONFIG=None):  # or use custom logger
        contact.is_verified = True
        contact.verified_at = timezone.now()
        if verified_by:
            contact.verified_by = verified_by
        contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
    
    # Log non-PII audit trail
    audit_logger.info(f"Contact verified for user {contact.user.id} by {verified_by.id if verified_by else 'system'}")
```

**Security impact:**
Contact values (emails, phone numbers) could be logged by Django's logging system, creating additional PII exposure points.

**Compliance:**
GDPR Article 25 (Data Protection by Design), PCI DSS logging requirements

---

### 💡 Recommendations (Best Practices)

#### **AUDIT-TRAIL**: Add Audit Logging for Contact Changes

**Current code:**
```python
def create_user_contact(cls, ...):
    contact = UserContact.objects.create(...)
    return contact
```

**Recommended implementation:**
```python
import logging

audit_logger = logging.getLogger('security.audit')

def create_user_contact(cls, ..., created_by: User):
    contact = UserContact.objects.create(...)
    
    # Audit log without PII
    audit_logger.info(
        f"Contact created: user={user.id}, type={contact_type}, "
        f"by={created_by.id}, primary={is_primary}"
    )
    return contact
```

**Security impact:**
Enables detection of unauthorized contact modifications and compliance with audit requirements.

**Compliance:**
GDPR Article 30 (Records of Processing Activities)

---

#### **CONSENT-EXPLICIT**: Add Consent Tracking for Contact Storage

**Recommended implementation:**
```python
def create_user_contact(cls, ..., consent_given: bool = False, consent_purpose: str = None):
    if not consent_given:
        raise ValidationError("Explicit consent required for storing contact information")
    
    contact = UserContact.objects.create(
        consent_given=consent_given,
        consent_purpose=consent_purpose,
        consent_timestamp=timezone.now(),
        ...
    )
```

**Security impact:**
Ensures GDPR compliance for lawful processing of personal data.

**Compliance:**
GDPR Article 6 (Lawfulness of Processing), Article 7 (Conditions for Consent)

---

#### **DATA-RETENTION**: Implement Data Retention Policies

**Recommended implementation:**
```python
from datetime import timedelta

def cleanup_expired_contacts(cls, retention_days: int = 365):
    """Remove unverified contacts older than retention period."""
    cutoff_date = timezone.now() - timedelta(days=retention_days)
    
    expired_contacts = UserContact.objects.filter(
        is_verified=False,
        created_at__lt=cutoff_date
    )
    
    count = expired_contacts.count()
    expired_contacts.delete()
    
    audit_logger.info(f"Cleaned up {count} expired unverified contacts")
```

**Security impact:**
Reduces data exposure by removing unnecessary personal data, meeting GDPR data minimization requirements.

**Compliance:**
GDPR Article 5 (Principles of Processing), Article 17 (Right to Erasure)

---

### 📋 Compliance Checklist
- [ ] OWASP Top 10 compliance (missing input validation, authorization checks)
- [ ] PII properly protected (needs encryption at rest)
- [x] GDPR requirements met (partial - needs consent tracking, retention policies)
- [ ] Secrets not in code (encryption keys need proper management)
- [ ] Dependencies up to date (review Django version for security updates)
- [ ] Audit logging implemented (needs enhancement)
- [x] MFA support implemented
- [ ] Error handling secure (reduce information disclosure)

**Priority Actions:**
1. Implement input validation for contact values
2. Add encryption for contact information at rest
3. Add authorization checks to all methods accessing user data
4. Reduce information disclosure in error messages
5. Implement audit logging and consent tracking
</Task>
</sub_task>

I've completed a comprehensive security and privacy review of the Django authentication service code. The analysis identified several critical security vulnerabilities that should be addressed immediately:

## Key Critical Issues Found:

1. **INPUT-VALIDATE**: No validation of contact values (emails, phone numbers)
2. **PII-ENCRYPT**: Contact information stored without encryption at rest  
3. **AUTHZ-CHECK**: Missing authorization checks on sensitive methods

## Priority Recommendations:

**Immediate fixes needed:**
- Add input validation for email and phone formats
- Implement encryption for contact values in the database
- Add authorization checks to prevent unauthorized access to user policies

**Should implement:**
- Reduce information disclosure in error messages
- Add safeguards against PII logging
- Implement audit trails for contact changes

The code shows good practices in some areas (proper ORM usage, MFA support, role validation) but needs security hardening around input validation, data protection, and access controls to meet enterprise security standards and privacy regulations like GDPR.
