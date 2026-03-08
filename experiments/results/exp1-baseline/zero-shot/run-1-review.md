# Code Security and Quality Review: services.py

## Critical Security Issues

### AUTH-BYPASS-1: Unauthorized Default Access for Internal Users
**Severity: CRITICAL**

**Problematic Code:**
```python
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    policy = cls.get_user_policy(user)
    if policy:
        return policy.allowed_methods
    # For internal users without a specific policy (e.g., new SSO users
    # who haven't been assigned a role yet), default to email
    if user.user_type == UserType.INT_USER:
        return [ContactType.EMAIL]  # ⚠️ SECURITY ISSUE
    return []
```

**Improved Code:**
```python
def get_allowed_auth_methods(cls, user: User) -> list[str]:
    policy = cls.get_user_policy(user)
    if policy:
        return policy.allowed_methods
    
    # No default access - users must have explicit role assignment
    # Log the attempt for security monitoring
    logger.warning(
        "Access attempt by user without role assignment",
        extra={"user_id": user.id, "user_type": user.user_type}
    )
    return []
```

**Impact:** This allows internal users without role assignments to authenticate using email, bypassing the policy system. An attacker who gains access to an internal user account without proper role setup could authenticate without authorization.

### INPUT-VALID-1: Missing Contact Value Validation
**Severity: HIGH**

**Problematic Code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,  # ⚠️ No validation
    # ...
) -> UserContact:
```

**Improved Code:**
```python
def create_user_contact(
    cls,
    user: User,
    contact_type: str,
    contact_value: str,
    # ...
) -> UserContact:
    # Validate contact value based on type
    cls._validate_contact_value(contact_type, contact_value)
    
    # ... rest of method

@classmethod
def _validate_contact_value(cls, contact_type: str, contact_value: str) -> None:
    """Validate contact value format and content."""
    if not contact_value or not contact_value.strip():
        raise ValidationError("Contact value cannot be empty")
    
    if contact_type == ContactType.EMAIL:
        from django.core.validators import validate_email
        validate_email(contact_value)
    elif contact_type == ContactType.PHONE:
        # Validate phone number format
        import re
        if not re.match(r'^\+?1?\d{9,15}$', contact_value):
            raise ValidationError("Invalid phone number format")
    elif contact_type == ContactType.SAML_SSO:
        # Validate SSO ID format
        if len(contact_value) < 3 or len(contact_value) > 100:
            raise ValidationError("Invalid SSO ID length")
```

**Impact:** Unvalidated input could lead to data integrity issues, potential injection attacks, or system errors when processing malformed contact information.

## High Severity Issues

### AUTHZ-BYPASS-2: Missing Authorization Checks in Contact Setup
**Severity: HIGH**

**Problematic Code:**
```python
def setup_technician_contacts(cls, user: User, phone: str) -> None:
    # Only checks role existence, not authorization to modify this user
    has_tech_role = UserRole.objects.filter(
        user=user, role=Role.EXT_PARTNER_TECH, is_deleted=False
    ).exists()
```

**Improved Code:**
```python
def setup_technician_contacts(cls, user: User, phone: str, requesting_user: User) -> None:
    # Verify authorization to modify this user
    if not cls._can_modify_user_contacts(requesting_user, user):
        raise PermissionError(f"User {requesting_user.id} cannot modify contacts for user {user.id}")
    
    # Verify user has EXT_PARTNER_TECH role
    has_tech_role = UserRole.objects.filter(
        user=user, role=Role.EXT_PARTNER_TECH, is_deleted=False
    ).exists()
    
    if not has_tech_role:
        raise ValueError("This method is only for users with EXT_PARTNER_TECH role")

@classmethod
def _can_modify_user_contacts(cls, requesting_user: User, target_user: User) -> bool:
    """Check if requesting user can modify target user's contacts."""
    # Users can modify their own contacts
    if requesting_user.id == target_user.id:
        return True
    
    # Admins can modify contacts for users in their organization
    # Add appropriate authorization logic here
    return requesting_user.has_perm('users.change_usercontact')
```

**Impact:** Anyone with access to these methods could modify contacts for any user, leading to account takeover scenarios.

### RACE-CONDITION-1: Race Condition in Primary Contact Setting
**Severity: HIGH**

**Problematic Code:**
```python
# If this is primary, unset other primary contacts of the same type
if is_primary:
    UserContact.objects.filter(
        user=user, contact_type=contact_type, is_primary=True
    ).update(is_primary=False)

# Create the contact
contact = UserContact.objects.create(...)  # ⚠️ Race condition possible
```

**Improved Code:**
```python
@classmethod
@transaction.atomic
def create_user_contact(cls, ...):
    # Use select_for_update to prevent race conditions
    with transaction.atomic():
        if is_primary:
            # Lock existing primary contacts to prevent race conditions
            UserContact.objects.select_for_update().filter(
                user=user, contact_type=contact_type, is_primary=True
            ).update(is_primary=False)

        # Create the contact
        contact = UserContact.objects.create(...)
```

**Impact:** Concurrent requests could result in multiple primary contacts of the same type, violating business rules.

## Medium Severity Issues

### CIRCULAR-IMPORT-1: Poor Module Architecture
**Severity: MEDIUM**

**Problematic Code:**
```python
# Import here to avoid circular import
from users.models import UserRole  # noqa: PLC0415
```

**Improved Code:**
```python
# In a separate module (e.g., users/types.py):
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from users.models import UserRole

# Or restructure to avoid circular dependencies entirely
```

**Impact:** Circular imports indicate architectural problems and can lead to import errors or maintenance issues.

### MAGIC-VALUES-1: Hardcoded Configuration Values
**Severity: MEDIUM**

**Problematic Code:**
```python
def get_session_duration(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    return policy.session_duration_hours if policy else 8  # ⚠️ Magic number

def get_inactivity_timeout(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    return policy.inactivity_timeout_minutes if policy else 15  # ⚠️ Magic number
```

**Improved Code:**
```python
from django.conf import settings

def get_session_duration(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    return policy.session_duration_hours if policy else getattr(
        settings, 'DEFAULT_SESSION_DURATION_HOURS', 8
    )

def get_inactivity_timeout(cls, user: User) -> int:
    policy = cls.get_user_policy(user)
    return policy.inactivity_timeout_minutes if policy else getattr(
        settings, 'DEFAULT_INACTIVITY_TIMEOUT_MINUTES', 15
    )
```

**Impact:** Hardcoded values make the system less configurable and harder to adjust for different environments.

## Low Severity Issues

### ERROR-HANDLE-1: Inconsistent Error Handling
**Severity: LOW**

**Problematic Code:**
```python
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    try:
        return AuthMethodPolicy.objects.get(role=role_assignment.role)
    except AuthMethodPolicy.DoesNotExist:
        return None  # ⚠️ Silent failure
```

**Improved Code:**
```python
def get_user_policy(cls, user: User) -> AuthMethodPolicy | None:
    try:
        return AuthMethodPolicy.objects.get(role=role_assignment.role)
    except AuthMethodPolicy.DoesNotExist:
        logger.info(
            "No auth policy found for role",
            extra={"user_id": user.id, "role": role_assignment.role}
        )
        return None
```

**Impact:** Silent failures make debugging and monitoring more difficult.

### METHOD-RESP-1: Multiple Responsibilities in Single Method
**Severity: LOW**

**Problematic Code:**
```python
def create_user_contact(cls, ...):
    # 1. Validates policy
    # 2. Updates existing primary contacts  
    # 3. Creates new contact
    # Multiple responsibilities in one method
```

**Improved Code:**
```python
def create_user_contact(cls, ...):
    cls._validate_contact_creation(user, contact_type)
    if is_primary:
        cls._unset_existing_primary_contacts(user, contact_type)
    return cls._create_contact_record(...)

@classmethod
def _validate_contact_creation(cls, user: User, contact_type: str) -> None:
    # Policy validation logic

@classmethod  
def _unset_existing_primary_contacts(cls, user: User, contact_type: str) -> None:
    # Primary contact management logic

@classmethod
def _create_contact_record(cls, ...) -> UserContact:
    # Contact creation logic
```

**Impact:** Methods with multiple responsibilities are harder to test, maintain, and debug.

## Summary

The most critical issues are:
1. **AUTH-BYPASS-1**: Default email access for internal users without roles
2. **INPUT-VALID-1**: Missing validation of contact values  
3. **AUTHZ-BYPASS-2**: Missing authorization checks in contact setup methods
4. **RACE-CONDITION-1**: Potential race condition in primary contact setting

These issues should be addressed immediately as they pose significant security risks to the authentication system.
