# Security and Code Quality Review

## Critical Security Issues

### AUTH-BYPASS-DEFAULT
**Severity: CRITICAL**

```python
# Problematic code
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    policy = cls.get_user_policy(user)
    if policy:
        return policy.allowed_methods
    # For internal users without a specific policy (e.g., new SSO users
    # who haven't been assigned a role yet), default to email
    if user.user_type == UserType.INT_USER:
        return [ContactType.EMAIL]  # ← Default access granted
    return []
```

```python
# Improved code
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    policy = cls.get_user_policy(user)
    if policy:
        return policy.allowed_methods
    
    # Log security event for users without policies
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"User {user.id} has no authentication policy assigned")
    
    # Require explicit policy assignment - no default access
    return []
```

**Impact**: Internal users without assigned roles get automatic email authentication access, potentially allowing unauthorized access during the gap between user creation and role assignment.

### FIELD-INJECTION
**Severity: HIGH**

```python
# Problematic code
def create_user_contact(
    cls, user: User, contact_type: str, contact_value: str,
    is_primary: bool = False, is_verified: bool = False,
    can_receive_otp: bool = False, **kwargs  # ← Allows arbitrary fields
) -> UserContact:
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=contact_value,
        is_primary=is_primary,
        is_verified=is_verified,
        can_receive_otp=can_receive_otp,
        **kwargs,  # ← Could inject sensitive fields
    )
```

```python
# Improved code
def create_user_contact(
    cls, user: User, contact_type: str, contact_value: str,
    is_primary: bool = False, is_verified: bool = False,
    can_receive_otp: bool = False, can_authenticate: bool = True
) -> UserContact:
    # Explicit field whitelist - no **kwargs
    contact = UserContact.objects.create(
        user=user,
        contact_type=contact_type,
        contact_value=contact_value,
        is_primary=is_primary,
        is_verified=is_verified,
        can_receive_otp=can_receive_otp,
        can_authenticate=can_authenticate,
    )
```

**Impact**: Attackers could potentially inject sensitive fields like `is_verified=True` or `verified_by` through the kwargs parameter.

### RACE-CONDITION-PRIMARY
**Severity: HIGH**

```python
# Problematic code
if is_primary:
    UserContact.objects.filter(
        user=user, contact_type=contact_type, is_primary=True
    ).update(is_primary=False)  # ← Not atomic with creation

# Create the contact
contact = UserContact.objects.create(...)  # ← Race window here
```

```python
# Improved code
@transaction.atomic
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # Use select_for_update to prevent race conditions
    if is_primary:
        UserContact.objects.select_for_update().filter(
            user=user, contact_type=contact_type, is_primary=True
        ).update(is_primary=False)
    
    contact = UserContact.objects.create(...)
```

**Impact**: Race conditions could result in multiple primary contacts of the same type, breaking authentication logic.

## High Priority Security Issues

### NO-INPUT-VALIDATION
**Severity: HIGH**

```python
# Problematic code
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # No validation of contact_value format
    contact = UserContact.objects.create(
        contact_value=contact_value,  # ← Could be malicious input
    )
```

```python
# Improved code
def create_user_contact(cls, user: User, contact_type: str, contact_value: str, ...):
    # Validate contact value based on type
    from django.core.validators import validate_email
    import re
    
    if contact_type == ContactType.EMAIL:
        validate_email(contact_value)
    elif contact_type == ContactType.PHONE:
        if not re.match(r'^\+?1?\d{9,15}$', contact_value):
            raise ValidationError("Invalid phone number format")
    elif contact_type == ContactType.SAML_SSO:
        if not contact_value.strip():
            raise ValidationError("SSO ID cannot be empty")
    
    contact = UserContact.objects.create(...)
```

**Impact**: Malformed or malicious contact values could cause authentication failures or injection attacks.

### QUERY-TIMING-ATTACK
**Severity: MEDIUM**

```python
# Problematic code
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
    if not role_assignment:
        return None  # ← Quick return reveals user existence

    try:
        return AuthMethodPolicy.objects.get(role=role_assignment.role)
    except AuthMethodPolicy.DoesNotExist:
        return None  # ← Different timing
```

```python
# Improved code
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    # Use consistent timing regardless of user existence
    import time
    start_time = time.time()
    
    try:
        role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
        if role_assignment:
            policy = AuthMethodPolicy.objects.get(role=role_assignment.role)
        else:
            policy = None
    except AuthMethodPolicy.DoesNotExist:
        policy = None
    
    # Ensure minimum processing time to prevent timing attacks
    elapsed = time.time() - start_time
    if elapsed < 0.01:  # Minimum 10ms
        time.sleep(0.01 - elapsed)
    
    return policy
```

**Impact**: Timing differences could reveal information about user existence and role assignments.

## Code Quality Issues

### CIRCULAR-IMPORTS
**Severity: MEDIUM**

```python
# Problematic code
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    # Import here to avoid circular import
    from users.models import UserRole  # noqa: PLC0415
```

```python
# Improved code - Restructure imports
# In services.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import UserRole

def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    # Import at module level or use dependency injection
    from django.apps import apps
    UserRole = apps.get_model('users', 'UserRole')
```

**Impact**: Circular imports indicate architectural issues and make code harder to test and maintain.

### QUERY-ORDERING
**Severity: MEDIUM**

```python
# Problematic code
role_assignment = UserRole.objects.filter(user=user, is_deleted=False).first()
```

```python
# Improved code
role_assignment = UserRole.objects.filter(
    user=user, is_deleted=False
).order_by('-created_at').first()  # Explicit ordering
```

**Impact**: `.first()` without ordering can return unpredictable results in PostgreSQL and other databases.

### HARDCODED-CONSTANTS
**Severity: LOW**

```python
# Problematic code
has_tech_role = UserRole.objects.filter(
    user=user, role=Role.EXT_PARTNER_TECH, is_deleted=False  # ← Hardcoded
).exists()
```

```python
# Improved code
from django.conf import settings

TECHNICIAN_ROLES = getattr(settings, 'TECHNICIAN_ROLES', ['EXT_PARTNER_TECH'])

has_tech_role = UserRole.objects.filter(
    user=user, role__code__in=TECHNICIAN_ROLES, is_deleted=False
).exists()
```

**Impact**: Hardcoded role types make the system inflexible and harder to configure for different deployments.

## Summary

The code has several **critical security vulnerabilities** that should be addressed immediately:

1. **AUTH-BYPASS-DEFAULT**: Remove default authentication access for users without policies
2. **FIELD-INJECTION**: Eliminate `**kwargs` parameter to prevent field injection
3. **RACE-CONDITION-PRIMARY**: Use proper locking for primary contact updates

The **architectural issues** with circular imports suggest the need for refactoring to improve maintainability. Consider using dependency injection or restructuring the module hierarchy.

Overall security posture can be significantly improved by adding input validation, consistent timing behavior, and removing default access patterns.
