## Security & Privacy Review: services.py

### ✅ Strengths
- **SQL-INJECT**: Uses Django ORM with parameterized queries, preventing SQL injection
- **MFA-SUPPORT**: Well-designed MFA framework with policy-driven requirements and method restrictions
- **TYPE-CHECK**: Good use of Python type hints for method signatures and return values
- **AUTHZ-CHECK**: Policy validation in `create_user_contact` prevents unauthorized contact type creation

### 🔴 Critical Issues (Immediate Fix Required)

#### **AUTHZ-CHECK**: Missing User Access Control
**Vulnerable code:**
```python
@classmethod
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    # No check if caller should have access to this user's data
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()

@classmethod
def get_user_capabilities(cls, user: User) -> list[str]:
    # Anyone can get any user's authentication capabilities
    return list(
        UserContact.objects.filter(user=user, can_authenticate=True)
        .values_list("contact_type", flat=True)
        .distinct()
    )
```

**Secure implementation:**
```python
@classmethod
def get_user_policy(cls, user: User, requesting_user: User) -> AuthMethodPolicy | None:
    # Check authorization first
    if not cls._can_access_user_data(requesting_user, user):
        raise PermissionDenied("Access denied to user authentication data")
    
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
    # ... rest of method

@classmethod
def _can_access_user_data(cls, requesting_user: User, target_user: User) -> bool:
    # Users can access their own data
    if requesting_user == target_user:
        return True
    # Admins can access user data in their organization
    if requesting_user.has_permission('view_user_auth_data'):
        return cls._same_organization(requesting_user, target_user)
    return False
```

**Security impact:** Any authenticated user can access any other user's authentication capabilities and policies, leading to information disclosure and potential privilege escalation reconnaissance.

**Compliance:** Violates OWASP A01:2021 (Broken Access Control), GDPR Article 32 (data protection by design)

---

#### **PII-ENCRYPT**: Sensitive Data Not Encrypted at Rest
**Vulnerable code:**
```python
contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value=contact_value,  # Email/phone stored in plaintext
    # ... other fields
)
```

**Secure implementation:**
```python
from django_cryptography.fields import encrypt
from cryptography.fernet import Fernet

class UserContact(models.Model):
    contact_value_encrypted = encrypt(models.TextField())  # Encrypted field
    
    def set_contact_value(self, value: str):
        self.contact_value_encrypted = value
        
    def get_contact_value(self) -> str:
        return self.contact_value_encrypted

# In service layer
contact = UserContact.objects.create(
    user=user,
    contact_type=contact_type,
    contact_value_encrypted=contact_value,  # Automatically encrypted
)
```

**Security impact:** PII (email addresses, phone numbers) stored in plaintext in database, vulnerable to data breaches and insider threats.

**Compliance:** Violates GDPR Article 32 (appropriate security measures), OWASP A02:2021 (Cryptographic Failures)

---

### ⚠️ Warnings (Should Fix)

#### **VALIDATE-INPUT**: Insufficient Input Validation
**Vulnerable code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No validation
    **kwargs,  # Accepts arbitrary fields
) -> UserContact:
```

**Secure implementation:**
```python
import re
from django.core.validators import validate_email

def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    is_primary: bool = False,
    is_verified: bool = False,
    can_receive_otp: bool = False,
    # Remove **kwargs, use explicit parameters
) -> UserContact:
    # Validate contact value based on type
    if contact_type == ContactType.EMAIL:
        validate_email(contact_value)
    elif contact_type == ContactType.PHONE:
        if not re.match(r'^\+?1?\d{9,15}$', contact_value):
            raise ValidationError("Invalid phone number format")
    elif contact_type == ContactType.SAML_SSO:
        if len(contact_value) > 255 or not contact_value.isalnum():
            raise ValidationError("Invalid SSO ID format")
```

**Security impact:** Malformed or malicious contact values could cause application errors or be used in attacks.

**Compliance:** OWASP A03:2021 (Injection), CWE-20 (Improper Input Validation)

---

#### **ERROR-SAFE**: Information Disclosure in Error Messages
**Vulnerable code:**
```python
raise ValidationError(
    f"Contact type '{contact_type}' is not allowed for user type '{user.user_type}'"
)
```

**Secure implementation:**
```python
# Log detailed error for debugging
logger.warning(
    "Contact creation failed",
    extra={
        'user_id': user.id,
        'contact_type': contact_type,
        'user_type': user.user_type,
    }
)
# Return generic error to user
raise ValidationError("Contact type not allowed for this user")
```

**Security impact:** Error messages reveal internal user types and system structure to potential attackers.

**Compliance:** OWASP A01:2021 (Broken Access Control), CWE-209 (Information Exposure)

---

#### **PII-LOG**: Potential PII in Logs
**Vulnerable code:**
```python
# Django DEBUG logging might capture method parameters
def verify_contact(cls, contact: UserContact, verified_by: User | None = None):
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
    # If Django logging captures this, contact.contact_value (email/phone) gets logged
```

**Secure implementation:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None):
    # Log verification without PII
    logger.info(
        "Contact verified",
        extra={
            'contact_id': contact.id,
            'contact_type': contact.contact_type,
            'verified_by_id': verified_by.id if verified_by else None,
        }
    )
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
```

**Security impact:** PII could be inadvertently logged, violating data protection regulations.

**Compliance:** GDPR Article 5 (data minimization), CCPA compliance

---

### 💡 Recommendations (Best Practices)

#### **AUDIT-TRAIL**: Add Authentication Event Logging
**Current code:**
```python
# No audit trail for authentication-related operations
def verify_contact(cls, contact: UserContact, verified_by: User | None = None):
    contact.is_verified = True
```

**Secure implementation:**
```python
def verify_contact(cls, contact: UserContact, verified_by: User | None = None):
    # Create audit trail
    AuthenticationAuditLog.objects.create(
        user=contact.user,
        action='CONTACT_VERIFIED',
        contact_type=contact.contact_type,
        performed_by=verified_by,
        timestamp=timezone.now(),
        ip_address=get_current_request().META.get('REMOTE_ADDR'),
    )
    
    contact.is_verified = True
    contact.verified_at = timezone.now()
    if verified_by:
        contact.verified_by = verified_by
    contact.save(update_fields=["is_verified", "verified_at", "verified_by"])
```

**Security impact:** Improves incident response and compliance reporting capabilities.

**Compliance:** GDPR Article 30 (records of processing), SOC 2 audit requirements

---

#### **PII-MINIMIZE**: Return Minimal Data
**Current code:**
```python
def get_user_capabilities(cls, user: User) -> list[str]:
    return list(
        UserContact.objects.filter(user=user, can_authenticate=True)
        .values_list("contact_type", flat=True)
        .distinct()
    )
```

**Secure implementation:**
```python
def get_user_capabilities(cls, user: User, requesting_user: User, purpose: str) -> list[str]:
    cls._validate_access(requesting_user, user)
    
    # Return different levels of detail based on purpose
    if purpose == 'LOGIN_OPTIONS':
        # Only return what's needed for login
        return list(
            UserContact.objects.filter(
                user=user, 
                can_authenticate=True,
                is_verified=True
            ).values_list("contact_type", flat=True).distinct()
        )
    elif purpose == 'ADMIN_REVIEW':
        # Return more detail for admin operations
        return list(
            UserContact.objects.filter(user=user, can_authenticate=True)
            .values_list("contact_type", flat=True)
            .distinct()
        )
```

**Security impact:** Reduces data exposure and implements principle of least privilege.

**Compliance:** GDPR Article 5 (data minimization), privacy by design

---

### 📋 Compliance Checklist
- [ ] **OWASP Top 10 compliance** - Missing access controls (A01), input validation (A03)
- [ ] **PII properly protected** - Contact values not encrypted, potential logging issues
- [ ] **GDPR requirements met** - Missing consent mechanisms, audit trails, data minimization
- [ ] **Secrets not in code** - ✅ No hardcoded secrets found
- [ ] **Dependencies up to date** - ✅ Using Django framework (verify version separately)

**Priority Actions:**
1. Implement user access controls for all methods
2. Encrypt PII fields at rest
3. Add input validation for contact values
4. Implement audit logging for authentication events
5. Add data minimization controls
