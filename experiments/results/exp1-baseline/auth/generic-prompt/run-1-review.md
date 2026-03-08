# Security Review: Authentication Service

## Critical Issues

### UNVAL-INPUT
**CWE-20: Improper Input Validation**  
**Severity: Critical**

**Vulnerable Code:**
```python
@transaction.atomic
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # No validation
    # ...
) -> UserContact:
    # contact_value used directly without validation
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=contact_value,  # Potential injection point
        # ...
    )
```

**Secure Alternative:**
```python
from django.core.validators import validate_email
import re

@transaction.atomic
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, **kwargs):
    # Validate based on contact type
    if contact_type == ContactType.EMAIL:
        try:
            validate_email(contact_value)
        except ValidationError:
            raise ValidationError("Invalid email format")
    elif contact_type == ContactType.PHONE:
        if not re.match(r'^\+?1?[2-9][0-8][0-9][2-9][0-9]{6}$', contact_value):
            raise ValidationError("Invalid phone number format")
    elif contact_type == ContactType.SAML_SSO:
        if not re.match(r'^[a-zA-Z0-9@._-]+$', contact_value):
            raise ValidationError("Invalid SSO ID format")
    
    # Sanitize input
    contact_value = contact_value.strip()
```

**Attack Scenario:** Attackers could inject malicious data through unvalidated contact values, potentially leading to XSS, data corruption, or other injection attacks when this data is later displayed or processed.

---

### BROKEN-AUTHZ
**CWE-862: Missing Authorization**  
**Severity: Critical**

**Vulnerable Code:**
```python
@classmethod
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, **kwargs):
    # No authorization check - any caller can create contacts for any user
    contact = UserContact.objects.create(user=user, ...)
```

**Secure Alternative:**
```python
@classmethod
def create_user_contact(cls, requesting_user: User, target_user: User, 
                       contact_type: str, contact_value: str, **kwargs):
    # Authorization check
    if not cls._can_manage_user_contacts(requesting_user, target_user):
        raise PermissionDenied("Insufficient permissions to modify user contacts")
    
@classmethod
def _can_manage_user_contacts(cls, requesting_user: User, target_user: User) -> bool:
    # Users can manage their own contacts
    if requesting_user.id == target_user.id:
        return True
    
    # Admins can manage any user's contacts
    from users.models import Role, UserRole
    admin_roles = [Role.ADMIN, Role.SUPER_ADMIN]
    has_admin_role = UserRole.objects.filter(
        user=requesting_user, 
        role__in=admin_roles, 
        is_deleted=False
    ).exists()
    
    return has_admin_role
```

**Attack Scenario:** Attackers with access to the service layer could create, modify, or access authentication contacts for any user, leading to account takeover or privilege escalation.

---

## High Severity Issues

### INFO-LEAK
**CWE-200: Information Exposure**  
**Severity: High**

**Vulnerable Code:**
```python
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    # Returns detailed policy information that could aid attackers
    return policy.allowed_methods

def get_user_capabilities(cls, user: User) -> list[str]:
    # Exposes user's configured authentication methods
    return list(UserContact.objects.filter(...).values_list("contact_type", flat=True))
```

**Secure Alternative:**
```python
def get_allowed_auth_methods(cls, requesting_user: User, target_user: User) -> list[str]:
    # Authorization check
    if not cls._can_view_user_auth_info(requesting_user, target_user):
        raise PermissionDenied("Cannot view authentication methods")
    
    policy = cls.get_user_policy(target_user)
    if not policy:
        return []
    return policy.allowed_methods

@classmethod
def _can_view_user_auth_info(cls, requesting_user: User, target_user: User) -> bool:
    return requesting_user.id == target_user.id or cls._is_admin(requesting_user)
```

**Attack Scenario:** Attackers could enumerate available authentication methods for target users, helping them plan targeted attacks against specific authentication mechanisms.

---

### RACE-CONDITION
**CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization**  
**Severity: High**

**Vulnerable Code:**
```python
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
    # Race condition: role could be deleted between this check and policy lookup
    if not role_assignment:
        return None
    return AuthMethodPolicy.objects.get(role=role_assignment.role)
```

**Secure Alternative:**
```python
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    try:
        with transaction.atomic():
            # Use select_for_update to prevent race conditions
            role_assignment = UserRole.objects.select_for_update().filter(
                user=user, is_deleted=False
            ).first()
            
            if not role_assignment:
                return None
                
            return AuthMethodPolicy.objects.get(role=role_assignment.role)
    except (UserRole.DoesNotExist, AuthMethodPolicy.DoesNotExist):
        return None
```

**Attack Scenario:** In concurrent environments, role changes during policy lookups could lead to privilege escalation or denial of service.

---

## Medium Severity Issues

### WEAK-DEFAULT
**CWE-1188: Insecure Default Initialization**  
**Severity: Medium**

**Vulnerable Code:**
```python
def get_session_duration(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    return policy.session_duration_hours if policy else 8  # Too permissive

def get_inactivity_timeout(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    return policy.inactivity_timeout_minutes if policy else 15  # Too permissive
```

**Secure Alternative:**
```python
def get_session_duration(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    default_duration = 1  # More secure 1-hour default
    return policy.session_duration_hours if policy else default_duration

def get_inactivity_timeout(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    default_timeout = 5  # More secure 5-minute default
    return policy.inactivity_timeout_minutes if policy else default_timeout
```

**Attack Scenario:** Extended default session times increase the window for session hijacking attacks.

---

### UNSAFE-KWARGS
**CWE-470: Use of Externally-Controlled Input to Select Classes or Code**  
**Severity: Medium**

**Vulnerable Code:**
```python
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, **kwargs):
    # Arbitrary kwargs passed to model creation
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=contact_value,
        **kwargs,  # Uncontrolled input
    )
```

**Secure Alternative:**
```python
def create_user_contact(cls, user: User, contact_type: str, contact_value: str,
                       is_primary: bool = False, is_verified: bool = False,
                       can_receive_otp: bool = False):
    # Explicitly define allowed parameters
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=contact_value,
        is_primary=is_primary,
        is_verified=is_verified,
        can_receive_otp=can_receive_otp,
        can_authenticate=True,
    )
```

**Attack Scenario:** Malicious callers could pass unexpected parameters that modify critical model fields, potentially leading to privilege escalation.

---

## Low Severity Issues

### VERBOSE-ERROR
**CWE-209: Information Exposure Through Error Messages**  
**Severity: Low**

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
    raise ValidationError("Invalid contact type for user")
```

**Attack Scenario:** Detailed error messages reveal system internals that could aid reconnaissance.

---

## Recommendations

### Immediate Actions Required:
1. **Implement authorization checks** for all service methods
2. **Add input validation** for all contact values  
3. **Use select_for_update()** to prevent race conditions
4. **Replace **kwargs** with explicit parameters

### Additional Security Measures:
1. Implement rate limiting for contact creation
2. Add audit logging for all authentication-related operations  
3. Use more restrictive default session timeouts
4. Implement contact verification workflows before enabling authentication

### Testing Recommendations:
1. Add unit tests for authorization bypass attempts
2. Test concurrent access scenarios
3. Validate input sanitization effectiveness
4. Verify error message content doesn't leak sensitive information
