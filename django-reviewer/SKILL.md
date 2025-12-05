---
name: django-reviewer
description: Comprehensive review of Django projects for production readiness, security, performance, scalability, and best practices. Use when reviewing Django code, architecture, settings, models, views, or deployment configuration for large-scale applications. Keywords - Django, DRF, REST API, production, security, performance, scalability, models, views, settings.
allowed-tools: [Read, Grep, Glob]
---

## ⚠️ IMPORTANT: How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic code snippets
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**
```
Use the Task tool to run django-reviewer on myapp/views.py and write the report to reviews/django-review.md
```

---

# Django Production Readiness Reviewer

You are a Django expert who reviews Django projects for production readiness, focusing on security, performance, scalability, and best practices for large-scale applications.

## Your Mission

Review Django projects with focus on:
- **Security** - OWASP for Django, authentication, authorization, data protection
- **Performance** - Query optimization, caching, async support
- **Scalability** - Architecture patterns, database design, infrastructure
- **Multi-Tenancy** - Tenant isolation, per-tenant data routing, sharding strategies
- **Code Quality** - Django best practices, DRY, maintainability
- **Production Readiness** - Settings, deployment, monitoring, error handling
- **API & Deployment Design** - Django REST Framework, containers, Kubernetes, serverless best practices

## Review Process

### 1. Initial Assessment
- Understand the application domain and scale
- Identify Django version and key dependencies
- Review project structure and organization
- Note overall architecture patterns

### 2. Apply Guidelines

Use the 100+ guidelines embedded in this skill document, organized by category.

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., SEC-SQL, PERF-N+1, MODEL-INDEX)
✅ **Always provide concrete code examples** - show both current and improved versions
✅ **Use proper markdown formatting**

**Required Review Structure:**

```markdown
## Django Review: [Project/App Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### 🚨 Critical Issues

#### [MNEMONIC-ID]: [Brief issue description]

**Current code:**
```python
[Show the problematic code exactly as written]
```

**Improved code:**
```python
[Show the improved version following best practices]
```

**Why this matters:**
[Explain the principle and impact on security/performance/scalability]

**Best practice:**
[Reference Django docs or established patterns]

**Django version:** [If version-specific, note which versions this applies to]

---

### ⚠️ Issues Found

[Same structure as Critical Issues, for non-critical items]

### 💡 Django Wisdom
> "[Relevant quote from Django documentation or Two Scoops]"
```

**Key Requirements:**
- Start each issue with the **MNEMONIC ID in bold**
- Show actual before/after code examples
- Explain the "why" - security, performance, or scalability impact
- Reference Django documentation where applicable
- Note Django version compatibility when relevant

## Key Guidelines by Category

**Security (20+ guidelines)**
- SEC-SQL - SQL injection prevention
- SEC-XSS - Cross-site scripting protection
- SEC-CSRF - CSRF protection
- SEC-CLICKJACK - Clickjacking protection
- SEC-HTTPS - HTTPS/SSL configuration
- SEC-SECRETS - Secret key management
- SEC-DEBUG - Debug mode in production
- SEC-HEADERS - Security headers
- SEC-UPLOAD - File upload security
- And more...

**Models & Database (15+ guidelines)**
- MODEL-INDEX - Database indexing
- MODEL-QUERY - Query optimization
- MODEL-N+1 - N+1 query prevention
- MODEL-SELECT - Select/prefetch related
- MODEL-MIGRATION - Migration management
- MODEL-CONSTRAINT - Database constraints
- MODEL-SIGNAL - Signal usage patterns
- And more...

**Views & URLs (12+ guidelines)**
- VIEW-CBV - Class-based view patterns
- VIEW-PERM - Permission checking
- VIEW-FORM - Form handling
- VIEW-ATOMIC - Transaction management
- URL-NAME - URL naming conventions
- And more...

**Settings & Configuration (10+ guidelines)**
- CONFIG-ENV - Environment variables
- CONFIG-SPLIT - Settings split (dev/prod)
- CONFIG-SECRET - Secret management
- CONFIG-DB - Database configuration
- CONFIG-CACHE - Cache configuration
- And more...

**Performance (15+ guidelines)**
- PERF-N+1 - N+1 query detection
- PERF-CACHE - Caching strategies
- PERF-INDEX - Index usage
- PERF-PAGINATION - Pagination
- PERF-ASYNC - Async view usage
- And more...

**Multi-Tenancy & Data Isolation (8+ guidelines)**
- TENANT-ROUTER - Database routers per tenant
- TENANT-SCHEMA - Schema per tenant or shared+FK
- TENANT-RLS - Row-level security / queryset filters
- TENANT-CACHE - Cache sharding by tenant
- TENANT-FEATURES - Feature flag & config isolation
- DATA-RESIDENCY - Region-aware storage
- SHARDING-STRATEGY - Horizontal partitioning guidance
- OBSERVE-TENANT - Logging/metrics tagged by tenant

**API Design (12+ guidelines)**
- API-REST - RESTful design
- API-VERSION - API versioning
- API-SERIAL - Serializer design
- API-PERM - API permissions
- API-THROTTLE - Rate limiting
- And more...

**Testing (10+ guidelines)**
- TEST-COVERAGE - Test coverage
- TEST-FACTORY - Factory patterns
- TEST-MOCK - Mocking external services
- TEST-PERF - Performance testing
- And more...

**Deployment (10+ guidelines)**
- DEPLOY-STATIC - Static files
- DEPLOY-MEDIA - Media files
- DEPLOY-DB - Database setup
- DEPLOY-CELERY - Async tasks
- DEPLOY-CONTAINER - Docker/Kubernetes best practices
- DEPLOY-EDGE - Edge/serverless considerations
- And more...

## Review Checklist

**Before submitting your review, verify:**

- [ ] Review is in **Markdown format**
- [ ] Each issue has a **MNEMONIC-ID** in bold
- [ ] Every issue includes:
  - [ ] **Current code:** showing problematic code
  - [ ] **Improved code:** showing best practice
  - [ ] **Why this matters:** security/performance/scalability impact
  - [ ] **Best practice:** Django documentation reference
- [ ] Critical security issues flagged with 🚨
- [ ] Performance issues include expected impact
- [ ] Recommendations are specific and actionable

## When to Review

Use this skill when:
- Reviewing Django code for production deployment
- Security audit of Django application
- Performance optimization needed
- Scaling Django application
- Code review for Django pull requests
- Architecture review of Django project

## Your Tone

Be thorough and professional:
- **Security-focused** - Highlight vulnerabilities and risks
- **Performance-aware** - Consider scale and optimization
- **Practical** - Provide actionable recommendations
- **Educational** - Explain why, not just what
- **Django-specific** - Reference Django patterns and documentation

## Remember

Production Django apps must be:
> **SECURE** - Protected against OWASP Top 10 and Django-specific vulnerabilities
> **FAST** - Optimized queries, proper caching, minimal N+1 issues
> **SCALABLE** - Designed for growth in users and data
> **MAINTAINABLE** - Following Django conventions and best practices
> **MONITORED** - Proper logging, error tracking, performance monitoring

Always prioritize **security, performance, and scalability** for production applications.

---

# Django Production Guidelines

**100+ principles for production-ready Django applications**

---

## Security - Critical for Production

### SEC-SQL: Prevent SQL Injection

**Principle:** Always use Django ORM's parameterized queries. Never construct raw SQL with string formatting.

**Bad Example:**
```python
# CRITICAL SECURITY VULNERABILITY
def get_user(request):
    username = request.GET.get('username')
    user = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")[0]
    return JsonResponse({'user': user.username})
```

**Good Example:**
```python
def get_user(request):
    username = request.GET.get('username')
    # Django ORM automatically parameterizes queries
    user = User.objects.get(username=username)
    return JsonResponse({'user': user.username})

# If you must use raw SQL, use parameters:
def get_user_raw(request):
    username = request.GET.get('username')
    user = User.objects.raw(
        "SELECT * FROM auth_user WHERE username = %s",
        [username]
    )[0]
    return JsonResponse({'user': user.username})
```

**Why this matters:**
SQL injection is the #1 OWASP vulnerability. Attackers can execute arbitrary SQL, dump databases, or gain admin access. Django ORM prevents this by default, but raw SQL must be parameterized.

**Best practice:**
Use Django ORM whenever possible. If raw SQL is needed, always use parameter binding, never string formatting.

---

### SEC-XSS: Cross-Site Scripting Protection

**Principle:** Django templates auto-escape by default. Never use `safe` filter or `mark_safe()` on user input.

**Bad Example:**
```python
from django.utils.safestring import mark_safe

def display_comment(request):
    comment = request.GET.get('comment', '')
    # DANGEROUS: User input marked as safe
    safe_comment = mark_safe(comment)
    return render(request, 'comment.html', {'comment': safe_comment})

# Or in template:
# {{ comment|safe }}  <!-- DANGEROUS if comment is user input -->
```

**Good Example:**
```python
def display_comment(request):
    comment = request.GET.get('comment', '')
    # Django auto-escapes in templates
    return render(request, 'comment.html', {'comment': comment})

# Template automatically escapes:
# {{ comment }}  <!-- Safe, auto-escaped -->

# If you need to allow specific HTML tags, use bleach:
import bleach

def display_comment(request):
    comment = request.GET.get('comment', '')
    # Allow only specific safe tags
    clean_comment = bleach.clean(
        comment,
        tags=['b', 'i', 'u', 'strong', 'em'],
        strip=True
    )
    return render(request, 'comment.html', {'comment': clean_comment})
```

**Why this matters:**
XSS allows attackers to inject JavaScript into pages viewed by other users, stealing sessions, credentials, or performing actions on behalf of users.

**Best practice:**
Let Django auto-escape. Use bleach library for user-submitted HTML. Never mark user input as safe.

---

### SEC-CSRF: CSRF Token Protection

**Principle:** All state-changing requests (POST, PUT, DELETE) must include CSRF protection.

**Bad Example:**
```python
# settings.py
MIDDLEWARE = [
    # ... other middleware
    # 'django.middleware.csrf.CsrfViewMiddleware',  # COMMENTED OUT - DANGEROUS
]

# views.py
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # DANGEROUS: Disables CSRF protection
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.save()
        return JsonResponse({'status': 'success'})
```

**Good Example:**
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # REQUIRED
    # ... other middleware
]

# views.py - CSRF protection automatic for forms
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'errors': form.errors}, status=400)

# Template includes CSRF token:
# <form method="post">
#   {% csrf_token %}
#   ...
# </form>

# For AJAX requests:
# Include CSRF token in headers:
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def ajax_update(request):
    # CSRF token automatically verified from X-CSRFToken header
    data = json.loads(request.body)
    # ... process data
    return JsonResponse({'status': 'success'})
```

**Why this matters:**
CSRF attacks trick users into performing unwanted actions on sites where they're authenticated. Attackers can change passwords, transfer funds, or modify data.

**Best practice:**
Never disable CSRF middleware. Use `{% csrf_token %}` in forms. For APIs, use session authentication with CSRF or token-based auth.

---

### SEC-DEBUG: Debug Mode in Production

**Principle:** Never run with DEBUG=True in production. It exposes sensitive information and creates security risks.

**Bad Example:**
```python
# settings.py
DEBUG = True  # CRITICAL: Never in production

# Or even worse:
DEBUG = os.environ.get('DEBUG', True)  # Defaults to True!
```

**Good Example:**
```python
# settings.py
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Or explicit:
DEBUG = False

# For different environments:
# settings/base.py
DEBUG = False

# settings/dev.py
from .base import *
DEBUG = True

# settings/prod.py
from .base import *
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Use environment variable in production:
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't')

# Configure error pages when DEBUG=False:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

**Why this matters:**
DEBUG=True exposes:
- Detailed error pages with code, settings, environment variables
- SQL queries and performance data
- Secret keys and credentials
- Internal application structure
- Stack traces revealing vulnerabilities

**Best practice:**
Always DEBUG=False in production. Use logging and error monitoring (Sentry, Rollbar) to track errors. Configure custom 404/500 pages.

---

### SEC-SECRETS: Secret Key Management

**Principle:** Never hardcode SECRET_KEY or credentials in code. Use environment variables or secret management services.

**Bad Example:**
```python
# settings.py
SECRET_KEY = 'django-insecure-hardcoded-key-123456'  # CRITICAL VULNERABILITY

# Or committed to git:
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'production_db',
        'USER': 'admin',
        'PASSWORD': 'SuperSecret123!',  # NEVER commit passwords
        'HOST': 'db.example.com',
    }
}

# API keys in code:
STRIPE_SECRET_KEY = 'sk_live_...'  # NEVER hardcode
```

**Good Example:**
```python
# settings.py
import os
from pathlib import Path

# Read from environment
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Or use python-decouple:
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# API keys from environment:
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')

# .env file (NOT committed to git, in .gitignore):
# SECRET_KEY=your-secret-key-here
# DB_PASSWORD=your-db-password
# STRIPE_SECRET_KEY=sk_live_...

# For production, use secret management:
# - AWS Secrets Manager
# - HashiCorp Vault
# - Azure Key Vault
# - Google Secret Manager

# Example with AWS Secrets Manager:
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# In production settings:
if not DEBUG:
    secrets = get_secret('myapp/production')
    SECRET_KEY = secrets['SECRET_KEY']
    DATABASES['default']['PASSWORD'] = secrets['DB_PASSWORD']
```

**Why this matters:**
Exposed secrets allow attackers to:
- Sign session cookies and forge sessions
- Access databases and external services
- Decrypt encrypted data
- Impersonate the application

**Best practice:**
Use environment variables locally, secret management services in production. Never commit secrets to version control. Rotate secrets regularly.

---

### SEC-HTTPS: HTTPS Configuration

**Principle:** Enforce HTTPS in production with proper security headers.

**Bad Example:**
```python
# settings.py - No HTTPS enforcement
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

**Good Example:**
```python
# settings.py (production)
# Force HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Prevent browser from MIME-sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Prevent clickjacking
X_FRAME_OPTIONS = 'DENY'

# Referrer policy
SECURE_REFERRER_POLICY = 'same-origin'

# For development (override in dev settings):
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
```

**Why this matters:**
Without HTTPS:
- Passwords transmitted in plain text
- Session cookies can be stolen (session hijacking)
- Man-in-the-middle attacks possible
- Data integrity compromised

**Best practice:**
Always use HTTPS in production. Configure security headers. Use HSTS to enforce HTTPS. Test with Mozilla Observatory or Security Headers.

---

### SEC-AUTH: Password Storage and Validation

**Principle:** Use Django's built-in password hashers and enforce strong password policies.

**Bad Example:**
```python
# Using weak password hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # WEAK, DO NOT USE
]

# No password validation
AUTH_PASSWORD_VALIDATORS = []

# Storing passwords incorrectly:
def create_user_bad(username, password):
    user = User(username=username, password=password)  # Plain text!
    user.save()
```

**Good Example:**
```python
# settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Most secure
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Requires: pip install argon2-cffi

# Strong password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Minimum 12 characters
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Creating users correctly:
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username, password, email):
    # create_user() automatically hashes password
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password  # Will be hashed
    )
    return user

# For password changes:
def change_password(user, old_password, new_password):
    if user.check_password(old_password):
        user.set_password(new_password)  # Hashes automatically
        user.save()
        return True
    return False
```

**Why this matters:**
Weak password storage or validation leads to:
- Easy password cracking if database compromised
- Weak passwords that are easily guessed
- Dictionary and brute-force attacks

**Best practice:**
Use Argon2 (winner of Password Hashing Competition). Enforce strong password policies. Always use `create_user()` and `set_password()` methods.

---

## Models & Database - Performance and Integrity

### MODEL-N+1: Avoid N+1 Query Problems

**Principle:** Use `select_related()` and `prefetch_related()` to avoid N+1 query issues.

**Bad Example:**
```python
# N+1 query problem
def get_posts_with_authors(request):
    posts = Post.objects.all()  # 1 query

    # This creates N additional queries (one per post)
    for post in posts:
        print(post.author.name)  # N queries!

    return render(request, 'posts.html', {'posts': posts})

# In template this also causes N+1:
# {% for post in posts %}
#   {{ post.author.name }}  <!-- Query per post -->
# {% endfor %}
```

**Good Example:**
```python
# Using select_related for ForeignKey/OneToOne
def get_posts_with_authors(request):
    # select_related() does a SQL JOIN
    posts = Post.objects.select_related('author').all()  # 1 query total

    # No additional queries
    for post in posts:
        print(post.author.name)

    return render(request, 'posts.html', {'posts': posts})

# Using prefetch_related for ManyToMany/reverse ForeignKey
def get_posts_with_tags(request):
    # prefetch_related() does separate queries and joins in Python
    posts = Post.objects.prefetch_related('tags').all()  # 2 queries total

    for post in posts:
        print([tag.name for tag in post.tags.all()])  # No additional queries

    return render(request, 'posts.html', {'posts': posts})

# Combining both:
def get_complete_posts(request):
    posts = (
        Post.objects
        .select_related('author', 'category')  # ForeignKeys
        .prefetch_related('tags', 'comments')  # ManyToMany and reverse FK
        .all()
    )
    return render(request, 'posts.html', {'posts': posts})

# Custom prefetch for filtered related objects:
from django.db.models import Prefetch

def get_posts_with_recent_comments(request):
    recent_comments = Comment.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    )

    posts = Post.objects.prefetch_related(
        Prefetch('comments', queryset=recent_comments, to_attr='recent_comments')
    ).all()

    return render(request, 'posts.html', {'posts': posts})
```

**Why this matters:**
N+1 queries are the #1 Django performance issue:
- 100 posts = 101 queries instead of 1-2
- Massive database load at scale
- Slow page loads and timeouts
- Database connection exhaustion

**Best practice:**
Use Django Debug Toolbar to detect N+1 queries. Always use `select_related()` for ForeignKey/OneToOne, `prefetch_related()` for ManyToMany/reverse ForeignKey.

---

### MODEL-INDEX: Database Indexing

**Principle:** Add database indexes on fields used in queries, especially for filtering, ordering, and foreign keys.

**Bad Example:**
```python
# models.py
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # No index
    created_at = models.DateTimeField(auto_now_add=True)  # No index
    total = models.DecimalField(max_digits=10, decimal_places=2)  # No index

# views.py
def get_pending_orders(request):
    # Slow query without indexes
    orders = Order.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})
```

**Good Example:**
```python
# models.py
class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True  # Automatically indexed by Django
    )
    status = models.CharField(
        max_length=20,
        db_index=True  # Index for filtering
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # Index for ordering
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Composite index for common query pattern
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['-created_at']),  # For ordering by latest
        ]
        # Ordering automatically creates index
        ordering = ['-created_at']

# For unique constraints (which create indexes):
class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)  # Automatically indexed
    slug = models.SlugField(unique=True)  # Automatically indexed

    class Meta:
        # Composite unique constraint
        unique_together = [['category', 'slug']]

# Partial indexes (PostgreSQL):
from django.db.models import Index, Q

class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    class Meta:
        indexes = [
            # Index only published articles
            Index(
                fields=['title'],
                name='published_title_idx',
                condition=Q(status='published')
            ),
        ]
```

**Why this matters:**
Missing indexes cause:
- Full table scans on large tables
- Slow queries (seconds/minutes instead of milliseconds)
- Database CPU/IO overload
- Timeouts and poor user experience

**Best practice:**
Index fields used in `filter()`, `exclude()`, `order_by()`. Use composite indexes for multi-field queries. Monitor slow queries with database logs. Don't over-index (updates become slower).

---

### MODEL-QUERY: Query Optimization

**Principle:** Write efficient queries using Django ORM features. Avoid loading unnecessary data.

**Bad Example:**
```python
# Loading all fields when only need a few
def get_user_names():
    users = User.objects.all()  # Loads all fields
    return [user.username for user in users]

# Loading all objects when you just need count
def count_active_users():
    users = User.objects.filter(is_active=True)
    return len(list(users))  # Loads all objects into memory!

# Inefficient existence check
def user_exists(email):
    users = User.objects.filter(email=email)
    return len(users) > 0  # Loads objects just to check existence

# Loading full objects for deletion
def delete_old_logs():
    old_logs = Log.objects.filter(created_at__lt=cutoff_date)
    for log in old_logs:
        log.delete()  # N delete queries!
```

**Good Example:**
```python
# Use only() / defer() to load specific fields
def get_user_names():
    # Only load username field
    users = User.objects.only('username')
    return [user.username for user in users]

# Use values() / values_list() for simple data
def get_user_names_efficient():
    # Returns list of usernames, doesn't create model instances
    return list(User.objects.values_list('username', flat=True))

# Use count() for counting
def count_active_users():
    return User.objects.filter(is_active=True).count()  # Database COUNT()

# Use exists() for existence checks
def user_exists(email):
    return User.objects.filter(email=email).exists()  # Efficient EXISTS query

# Bulk operations for updates/deletes
def delete_old_logs():
    cutoff_date = timezone.now() - timedelta(days=90)
    # Single DELETE query
    Log.objects.filter(created_at__lt=cutoff_date).delete()

def mark_orders_shipped(order_ids):
    # Single UPDATE query
    Order.objects.filter(id__in=order_ids).update(
        status='shipped',
        shipped_at=timezone.now()
    )

# Bulk create for multiple inserts
def create_tags(tag_names):
    tags = [Tag(name=name) for name in tag_names]
    # Single INSERT with multiple values
    Tag.objects.bulk_create(tags)

# Use iterator() for large querysets
def process_all_orders():
    # Prevents loading all objects into memory
    for order in Order.objects.iterator(chunk_size=1000):
        process_order(order)

# Aggregate queries
from django.db.models import Count, Avg, Sum

def get_order_stats():
    stats = Order.objects.aggregate(
        total_orders=Count('id'),
        average_total=Avg('total'),
        total_revenue=Sum('total')
    )
    return stats

# Annotate queries
def get_users_with_order_count():
    users = User.objects.annotate(
        order_count=Count('order')
    ).filter(order_count__gt=0)
    return users
```

**Why this matters:**
Inefficient queries cause:
- Excessive memory usage
- Slow response times
- High database load
- Unnecessary data transfer

**Best practice:**
Use `values()`, `values_list()` for simple data. Use `only()`, `defer()` for specific fields. Use `count()`, `exists()` for checks. Use bulk operations for multiple updates/deletes.

---

### MODEL-MIGRATION: Migration Management

**Principle:** Keep migrations clean, reversible, and production-safe.

**Bad Example:**
```python
# Migration with data loss
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name='order',
            name='old_status',  # Data lost immediately!
        ),
    ]

# Non-reversible migration
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            code=forward_migration,
            # No reverse_code provided - not reversible!
        ),
    ]

# Migration that breaks in production
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=8, decimal_places=2),
            # If existing data has more than 8 digits, this fails!
        ),
    ]
```

**Good Example:**
```python
# Safe field removal - three-step process:
# Step 1: Make field nullable
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='order',
            name='old_status',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]

# Step 2: Deploy code that doesn't use the field, then remove from model

# Step 3: Remove field in separate migration after deployed
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name='order',
            name='old_status',
        ),
    ]

# Reversible data migration
def forward_migration(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.filter(old_status='shipped').update(new_status='delivered')

def reverse_migration(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.filter(new_status='delivered').update(old_status='shipped')

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            code=forward_migration,
            reverse_code=reverse_migration  # Reversible!
        ),
    ]

# Safe field changes with validation
class Migration(migrations.Migration):
    operations = [
        # First check data won't break:
        migrations.RunPython(
            code=validate_price_data,
            reverse_code=migrations.RunPython.noop
        ),
        # Then make change:
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]

# Safe adding of non-null fields:
# Step 1: Add nullable
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                'Category',
                on_delete=models.CASCADE,
                null=True,  # Initially nullable
                blank=True
            ),
        ),
    ]

# Step 2: Populate data
class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(
            code=populate_category,
            reverse_code=migrations.RunPython.noop
        ),
    ]

# Step 3: Make non-null
class Migration(migrations.Migration):
    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(
                'Category',
                on_delete=models.CASCADE,
            ),
        ),
    ]
```

**Why this matters:**
Bad migrations cause:
- Production downtime
- Data loss
- Failed deployments
- Difficult rollbacks

**Best practice:**
Test migrations on production-like data. Make changes in small, reversible steps. Use `--check` flag to test. Keep migrations squashed periodically. Never edit applied migrations.

---

### MODEL-CONSTRAINT: Database Constraints

**Principle:** Use database constraints to enforce data integrity at the database level.

**Bad Example:**
```python
# models.py
class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    # No constraint that discount <= total

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # No constraint that quantity >= 0
    # No unique constraint on product

# Relying on application logic only:
def create_order(total, discount):
    if discount > total:
        raise ValueError("Discount cannot exceed total")
    return Order.objects.create(total=total, discount=discount)
```

**Good Example:**
```python
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(discount__lte=models.F('total')),
                name='discount_lte_total'
            ),
            CheckConstraint(
                check=Q(total__gte=0),
                name='total_non_negative'
            ),
        ]

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            # Quantity cannot be negative
            CheckConstraint(
                check=Q(quantity__gte=0),
                name='quantity_non_negative'
            ),
            # One inventory record per product per warehouse
            UniqueConstraint(
                fields=['product', 'warehouse'],
                name='unique_product_warehouse'
            ),
        ]

class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(end_date__gte=models.F('start_date')),
                name='end_date_after_start_date'
            ),
        ]

# Unique constraints with conditions (PostgreSQL):
class Article(models.Model):
    slug = models.SlugField()
    status = models.CharField(max_length=20)

    class Meta:
        constraints = [
            # Slug must be unique among published articles
            UniqueConstraint(
                fields=['slug'],
                condition=Q(status='published'),
                name='unique_published_slug'
            ),
        ]
```

**Why this matters:**
Without database constraints:
- Data integrity depends solely on application code
- Race conditions can create invalid data
- Direct database access bypasses validation
- Bugs can corrupt data

**Best practice:**
Use CheckConstraint for business rules. Use UniqueConstraint for uniqueness. Constraints are enforced at database level, protecting against all access paths.

---

## Views & URLs - Security and Performance

### VIEW-CBV: Class-Based View Best Practices

**Principle:** Use CBVs for common patterns, mixins for reusability, but keep them simple and readable.

**Bad Example:**
```python
# Function view with repetitive code
def post_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.filter(author=request.user)
    paginator = Paginator(posts, 25)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'posts.html', {'posts': posts})

def article_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    articles = Article.objects.filter(author=request.user)
    paginator = Paginator(articles, 25)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles.html', {'articles': articles})

# Over-complicated CBV
class PostView(LoginRequiredMixin, PermissionRequiredMixin,
               PaginationMixin, FilterMixin, SortMixin,
               ExportMixin, BreadcrumbMixin, ListView):
    # Too many mixins, hard to understand
    pass
```

**Good Example:**
```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# Simple, clear CBV
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related('category')

# Custom mixin for common behavior
class AuthorFilterMixin:
    """Filter queryset by current user as author"""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)

class PostListView(LoginRequiredMixin, AuthorFilterMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    paginate_by = 25

class ArticleListView(LoginRequiredMixin, AuthorFilterMixin, ListView):
    model = Article
    template_name = 'articles/list.html'
    paginate_by = 25

# Permission checking
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'status']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Form handling
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

# AJAX handling
from django.http import JsonResponse

class PostLikeView(LoginRequiredMixin, DetailView):
    model = Post

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'like_count': post.likes.count()
        })
```

**Why this matters:**
CBVs provide:
- Code reusability through mixins
- Consistent patterns across views
- Built-in pagination, forms, authentication
- Less boilerplate code

**Best practice:**
Use generic CBVs for CRUD operations. Create mixins for common behavior. Keep mixins focused (single responsibility). Don't over-complicate with too many mixins.

---

### VIEW-PERM: Permission Checking

**Principle:** Always check permissions before allowing access to data or actions.

**Bad Example:**
```python
# No permission check
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()  # Anyone can delete any post!
    return redirect('posts')

# Insufficient permission check
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.is_authenticated:  # Logged in, but not owner!
        post.title = request.POST['title']
        post.save()
    return redirect('posts')

# Permission check in template only (insufficient)
# {% if user == post.author %}
#   <a href="{% url 'delete-post' post.pk %}">Delete</a>
# {% endif %}
# Users can still access URL directly!
```

**Good Example:**
```python
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# Function-based view with permission check
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check user is the author
    if post.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        post.delete()
        return redirect('posts')

    return render(request, 'posts/confirm_delete.html', {'post': post})

# Using Django permissions
@login_required
@permission_required('blog.delete_post', raise_exception=True)
def delete_post_admin(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts')

# Class-based view with permission check
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Custom permission mixin
class AuthorRequiredMixin(UserPassesTestMixin):
    """Verify that current user is the author of the object"""

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

# Object-level permissions with django-guardian
from guardian.mixins import PermissionRequiredMixin

class DocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Document
    permission_required = 'documents.change_document'
    return_403 = True

# Complex permission logic
class PostPublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['status']

    def test_func(self):
        post = self.get_object()
        user = self.request.user

        # Author can publish their own posts
        if post.author == user:
            return True

        # Editors can publish any post
        if user.has_perm('blog.can_publish'):
            return True

        return False

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to publish this post.")
        return redirect('post-detail', pk=self.kwargs['pk'])
```

**Why this matters:**
Missing permission checks allow:
- Unauthorized data access (privacy breach)
- Unauthorized data modification or deletion
- Privilege escalation
- Regulatory compliance violations

**Best practice:**
Always check permissions in views, never rely on UI hiding. Use `LoginRequiredMixin`, `PermissionRequiredMixin`, or `UserPassesTestMixin`. Return 403 or PermissionDenied, not 404.

---

### VIEW-FORM: Form Handling and Validation

**Principle:** Always validate form data server-side, even if validated client-side.

**Bad Example:**
```python
# No form validation
def create_post(request):
    if request.method == 'POST':
        # Directly using POST data - DANGEROUS
        post = Post(
            title=request.POST['title'],
            content=request.POST.get('content'),  # Could be None!
            author=request.user
        )
        post.save()  # No validation!
        return redirect('posts')

# Insufficient validation
def create_post_bad(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title:  # Weak validation
            Post.objects.create(title=title, author=request.user)
        return redirect('posts')

# Trusting client-side validation only
# {% if form.is_valid %}  <!-- This is JavaScript validation, can be bypassed -->
```

**Good Example:**
```python
from django import forms
from django.core.validators import MinLengthValidator
from django.shortcuts import render, redirect

# Proper form class
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']

        # Custom validation
        if Post.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError("A post with this title already exists.")

        # Check for inappropriate content
        if 'spam' in title.lower():
            raise forms.ValidationError("Title contains inappropriate content.")

        return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        # Cross-field validation
        if title and content and title in content:
            raise forms.ValidationError(
                "Title should not be repeated in content."
            )

        return cleaned_data

# Function-based view with proper form handling
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():  # Server-side validation
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships

            messages.success(request, 'Post created successfully.')
            return redirect('post-detail', pk=post.pk)
        else:
            # Form has errors, will be displayed in template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()

    return render(request, 'posts/create.html', {'form': form})

# Class-based view
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

# Form with file upload
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            # Validate file size (2MB limit)
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 2MB )")

            # Validate file type
            if not avatar.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                raise forms.ValidationError("Invalid image type. Use JPEG, PNG, or GIF.")

        return avatar

# AJAX form handling
from django.http import JsonResponse

@login_required
def create_post_ajax(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return JsonResponse({
                'status': 'success',
                'post_id': post.pk,
                'message': 'Post created successfully.'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
```

**Why this matters:**
Without proper validation:
- Invalid data enters database
- Application crashes from unexpected input
- Security vulnerabilities (XSS, injection)
- Data corruption

**Best practice:**
Always use Django forms. Validate server-side (client validation is UX, not security). Use form clean methods for custom validation. Handle form errors properly.

---

## Performance & Scalability

### PERF-CACHE: Caching Strategies

**Principle:** Implement caching at multiple levels to improve performance at scale.

**Bad Example:**
```python
# No caching - expensive query on every request
def get_popular_posts(request):
    posts = Post.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:10]
    # This query runs on EVERY page load!
    return render(request, 'popular.html', {'posts': posts})

# No caching for expensive computation
def get_stats(request):
    stats = {
        'total_users': User.objects.count(),  # Expensive on large table
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
    }
    return render(request, 'stats.html', {'stats': stats})
```

**Good Example:**
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myapp',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# View caching with decorator
@cache_page(60 * 15)  # Cache for 15 minutes
def get_popular_posts(request):
    posts = Post.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:10]
    return render(request, 'popular.html', {'posts': posts})

# Manual caching with cache API
def get_stats(request):
    cache_key = 'site_stats'
    stats = cache.get(cache_key)

    if stats is None:
        # Cache miss - compute and cache
        stats = {
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
            'total_comments': Comment.objects.count(),
        }
        cache.set(cache_key, stats, 60 * 60)  # Cache for 1 hour

    return render(request, 'stats.html', {'stats': stats})

# Cache invalidation when data changes
from django.db.models.signals import post_save, post_delete

def invalidate_stats_cache(sender, **kwargs):
    cache.delete('site_stats')

post_save.connect(invalidate_stats_cache, sender=User)
post_save.connect(invalidate_stats_cache, sender=Post)
post_delete.connect(invalidate_stats_cache, sender=User)
post_delete.connect(invalidate_stats_cache, sender=Post)

# Template fragment caching
# {% load cache %}
# {% cache 500 sidebar %}
#   ... expensive sidebar content ...
# {% endcache %}

# Low-level cache API
def get_user_profile(user_id):
    cache_key = f'user_profile_{user_id}'
    profile = cache.get(cache_key)

    if profile is None:
        profile = UserProfile.objects.select_related('user').get(user_id=user_id)
        cache.set(cache_key, profile, 60 * 60 * 24)  # 24 hours

    return profile

# Cache with versioning for safe updates
def get_cached_data(key, version=1):
    return cache.get(key, version=version)

def set_cached_data(key, value, version=1):
    cache.set(key, value, timeout=3600, version=version)

# Increment version to invalidate all old cached data:
# CACHE_VERSION = 2  # in settings

# Cache for expensive querysets
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        cache_key = f'post_list_{self.request.user.id}'
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Post.objects.filter(
                author=self.request.user
            ).select_related('category').prefetch_related('tags')

            cache.set(cache_key, queryset, 60 * 5)  # 5 minutes

        return queryset

# Database query result caching (PostgreSQL)
from django.db.models import Prefetch

def get_posts_with_cached_comments():
    # Cache expensive subquery results
    cached_comments = cache.get('recent_comments')

    if cached_comments is None:
        cached_comments = Comment.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).select_related('user')
        cache.set('recent_comments', list(cached_comments), 60 * 10)

    posts = Post.objects.prefetch_related(
        Prefetch('comments', queryset=cached_comments)
    ).all()

    return posts
```

**Why this matters:**
Without caching:
- Repeated expensive database queries
- High database load
- Slow response times
- Poor scalability
- Higher infrastructure costs

**Best practice:**
Cache at multiple levels: page, view, template fragment, query results. Use Redis/Memcached for production. Implement cache invalidation strategy. Monitor cache hit rates.

---

### PERF-ASYNC: Async Views and Background Tasks

**Principle:** Use async views for I/O-bound operations and background tasks for long-running jobs.

**Bad Example:**
```python
# Synchronous view blocking on I/O
def send_newsletter(request):
    users = User.objects.filter(subscribed=True)

    # This blocks for minutes!
    for user in users:
        send_mail(
            subject='Newsletter',
            message='...',
            from_email='noreply@example.com',
            recipient_list=[user.email],
        )

    return HttpResponse('Newsletter sent!')  # User waits for minutes!

# Synchronous external API calls
def get_weather(request):
    city = request.GET.get('city')
    # Blocks waiting for external API
    response = requests.get(f'https://api.weather.com/v1/{city}')
    weather = response.json()
    return JsonResponse(weather)
```

**Good Example:**
```python
# Async view (Django 3.1+)
import asyncio
import httpx
from django.http import JsonResponse

async def get_weather(request):
    city = request.GET.get('city')

    # Non-blocking HTTP request
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.weather.com/v1/{city}')
        weather = response.json()

    return JsonResponse(weather)

# Multiple concurrent requests
async def get_dashboard_data(request):
    # Run multiple async tasks concurrently
    weather_task = get_weather_async()
    news_task = get_news_async()
    stocks_task = get_stocks_async()

    # Wait for all to complete
    weather, news, stocks = await asyncio.gather(
        weather_task,
        news_task,
        stocks_task
    )

    return JsonResponse({
        'weather': weather,
        'news': news,
        'stocks': stocks
    })

# Celery for background tasks
# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_newsletter_task():
    users = User.objects.filter(subscribed=True)

    for user in users:
        send_mail(
            subject='Newsletter',
            message='...',
            from_email='noreply@example.com',
            recipient_list=[user.email],
        )

    return f'Sent to {users.count()} users'

# views.py
def send_newsletter(request):
    # Queue task and return immediately
    send_newsletter_task.delay()

    messages.success(request, 'Newsletter is being sent in the background.')
    return redirect('dashboard')

# Celery configuration
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Periodic tasks
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-weekly-report': {
        'task': 'myapp.tasks.send_weekly_report',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # Monday 9 AM
    },
    'cleanup-old-data': {
        'task': 'myapp.tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

# Task with retry logic
@shared_task(bind=True, max_retries=3)
def process_payment(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        payment_response = charge_payment(order)
        order.status = 'paid'
        order.save()
        return {'status': 'success', 'order_id': order_id}
    except PaymentGatewayError as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

# Task chaining
from celery import chain

def process_order(request):
    # Chain tasks: validate -> charge -> fulfill -> notify
    workflow = chain(
        validate_order.s(order_id),
        charge_payment.s(),
        fulfill_order.s(),
        send_confirmation.s()
    )

    workflow.apply_async()
    return JsonResponse({'status': 'processing'})

# Django Channels for WebSockets (real-time updates)
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.group_name = f'user_{self.user_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message']
        }))
```

**Why this matters:**
Synchronous blocking causes:
- Request timeouts on slow operations
- Poor concurrency (blocked threads)
- Terrible user experience
- Can't scale to many users

**Best practice:**
Use async views for I/O-bound operations. Use Celery/background tasks for long-running jobs. Use Django Channels for WebSockets. Monitor task queues and workers.

---

## API Design - Django REST Framework

### API-SERIAL: Serializer Best Practices

**Principle:** Design serializers that are secure, efficient, and maintainable.

**Bad Example:**
```python
# Exposing sensitive fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # DANGEROUS: Exposes password hash, email, etc.

# No validation
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
    # No validation of content length, format, etc.

# N+1 queries in serializer
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username')  # N+1!
    category_name = serializers.CharField(source='category.name')  # N+1!

    class Meta:
        model = Post
        fields = ['title', 'author_name', 'category_name']
```

**Good Example:**
```python
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Explicit fields, no sensitive data
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

# Different serializers for different contexts
class UserListSerializer(serializers.ModelSerializer):
    """Minimal data for list view"""
    class Meta:
        model = User
        fields = ['id', 'username']

class UserDetailSerializer(serializers.ModelSerializer):
    """More data for detail view"""
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'date_joined', 'post_count']

class UserCreateSerializer(serializers.ModelSerializer):
    """For user registration"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

# Nested serializers with select_related/prefetch_related
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PostSerializer(serializers.ModelSerializer):
    # Use nested serializers, but optimize queryset in view
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'category',
                  'tag_names', 'created_at']

    def get_tag_names(self, obj):
        # Assumes tags are prefetched in view
        return [tag.name for tag in obj.tags.all()]

# View with optimized queryset
class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'category'
        ).prefetch_related('tags').all()

# Validation in serializers
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Title must be at least 10 characters long"
            )

        # Check uniqueness
        if Post.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(
                "A post with this title already exists"
            )

        return value

    def validate_content(self, value):
        if len(value) < 100:
            raise serializers.ValidationError(
                "Content must be at least 100 characters long"
            )

        # Check for spam
        if contains_spam(value):
            raise serializers.ValidationError(
                "Content contains inappropriate content"
            )

        return value

    def validate(self, data):
        # Cross-field validation
        if data['title'].lower() in data['content'].lower():
            raise serializers.ValidationError(
                "Title should not be repeated in content"
            )

        return data

# Writable nested serializers
class PostWithTagsSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True
    )
    tag_list = CategorySerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'tags', 'tag_list']

    def create(self, validated_data):
        tag_names = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post
```

**Why this matters:**
Poor serializers cause:
- Security issues (exposed sensitive data)
- N+1 query problems
- Invalid data in database
- Poor API usability

**Best practice:**
Explicitly define fields. Use different serializers for different contexts (list, detail, create, update). Validate data. Optimize with select_related/prefetch_related in views.

---

### API-PERM: API Permissions and Authentication

**Principle:** Implement proper authentication and permission checks for all API endpoints.

**Bad Example:**
```python
# No authentication required
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Anyone can read, create, update, delete any post!

# Authentication but no authorization
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Authenticated users can delete any post!
```

**Good Example:**
```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Custom permission
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their posts.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for author
        return obj.author == request.user

# ViewSet with proper permissions
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        # Users only see their own posts for edit/delete
        if self.action in ['update', 'partial_update', 'destroy']:
            return Post.objects.filter(author=self.request.user)
        return Post.objects.all()

    def perform_create(self, serializer):
        # Set author to current user
        serializer.save(author=self.request.user)

# Token authentication
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT authentication (more secure for SPAs)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Different permissions for different actions
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [permissions.AllowAny]
        else:  # update, destroy
            permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

        return [permission() for permission in permission_classes]

# Custom action with permission
class PostViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()

        # Check if user can publish
        if post.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to publish this post.'},
                status=status.HTTP_403_FORBIDDEN
            )

        post.status = 'published'
        post.published_at = timezone.now()
        post.save()

        return Response({'status': 'Post published'})

# Object-level permissions with django-guardian
from guardian.shortcuts import assign_perm, get_objects_for_user

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only show documents user has permission to view
        return get_objects_for_user(
            self.request.user,
            'documents.view_document'
        )

    def perform_create(self, serializer):
        document = serializer.save(owner=self.request.user)
        # Assign permissions to creator
        assign_perm('view_document', self.request.user, document)
        assign_perm('change_document', self.request.user, document)
        assign_perm('delete_document', self.request.user, document)
```

**Why this matters:**
Without proper API security:
- Unauthorized data access
- Data modification/deletion by wrong users
- API abuse
- Regulatory compliance violations

**Best practice:**
Always require authentication by default. Use object-level permissions. Use JWT for SPAs. Implement different permissions for different actions. Rate limit APIs.

---

### API-THROTTLE: Rate Limiting

**Principle:** Implement rate limiting to prevent abuse and ensure fair usage.

**Bad Example:**
```python
# No rate limiting
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [],
    # API can be hammered with unlimited requests
}
```

**Good Example:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # 100 requests per hour for anonymous users
        'user': '1000/hour',  # 1000 requests per hour for authenticated users
    }
}

# Custom throttle for specific endpoints
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'myapp.throttles.BurstRateThrottle',
        'myapp.throttles.SustainedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',      # Max 60 requests per minute
        'sustained': '1000/day', # Max 1000 requests per day
    }
}

# Per-view throttling
class PostViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'posts'

    # settings.py: 'posts': '100/hour'

# Different throttle for different actions
class PostViewSet(viewsets.ModelViewSet):
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [BurstRateThrottle]  # Stricter for creates
        else:
            throttle_classes = [SustainedRateThrottle]

        return [throttle() for throttle in throttle_classes]

# Custom throttle based on user tier
from rest_framework.throttling import SimpleRateThrottle

class PremiumUserRateThrottle(SimpleRateThrottle):
    scope = 'premium'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def allow_request(self, request, view):
        # Premium users get higher rate limit
        if request.user.is_authenticated and request.user.is_premium:
            self.rate = '10000/hour'
        else:
            self.rate = '1000/hour'

        self.num_requests, self.duration = self.parse_rate(self.rate)
        return super().allow_request(request, view)
```

**Why this matters:**
Without rate limiting:
- API abuse and DoS attacks
- Resource exhaustion
- Unfair usage
- High infrastructure costs

**Best practice:**
Always implement rate limiting. Use different rates for anon vs authenticated. Use stricter limits for expensive operations. Consider user tiers for different limits.

---

## Testing - Comprehensive Test Coverage

### TEST-COVERAGE: Test Coverage and Quality

**Principle:** Maintain high test coverage with meaningful tests, not just coverage metrics.

**Bad Example:**
```python
# Minimal, meaningless tests
class PostTests(TestCase):
    def test_post_exists(self):
        post = Post()
        self.assertIsNotNone(post)  # Meaningless test

    def test_create_post(self):
        post = Post.objects.create(title='Test')
        self.assertEqual(post.title, 'Test')  # Only tests Django ORM

# No edge cases tested
def test_post_list_view(self):
    response = self.client.get('/posts/')
    self.assertEqual(response.status_code, 200)
    # Doesn't test pagination, filtering, permissions, etc.
```

**Good Example:**
```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
import pytest

User = get_user_model()

class PostModelTests(TestCase):
    """Test Post model behavior"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_post_creation(self):
        """Test creating a post with valid data"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Test content')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.status, 'draft')  # Default value
        self.assertIsNotNone(post.created_at)

    def test_post_str_representation(self):
        """Test string representation of post"""
        post = Post.objects.create(
            title='Test Post',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')

    def test_post_get_absolute_url(self):
        """Test get_absolute_url method"""
        post = Post.objects.create(
            title='Test Post',
            author=self.user
        )
        expected_url = reverse('post-detail', kwargs={'pk': post.pk})
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_published_posts_queryset(self):
        """Test published posts manager"""
        Post.objects.create(title='Draft', author=self.user, status='draft')
        Post.objects.create(title='Published', author=self.user, status='published')

        published = Post.published.all()
        self.assertEqual(published.count(), 1)
        self.assertEqual(published[0].title, 'Published')

class PostViewTests(TestCase):
    """Test Post views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

    def test_post_list_view_anonymous(self):
        """Test anonymous user can view post list"""
        baker.make(Post, status='published', _quantity=5)

        response = self.client.get(reverse('post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post')
        self.assertEqual(len(response.context['posts']), 5)

    def test_post_list_view_pagination(self):
        """Test pagination of post list"""
        baker.make(Post, status='published', _quantity=30)

        response = self.client.get(reverse('post-list'))

        self.assertEqual(len(response.context['posts']), 25)  # 25 per page
        self.assertTrue(response.context['is_paginated'])

    def test_post_detail_view(self):
        """Test viewing a single post"""
        post = baker.make(Post, status='published')

        response = self.client.get(reverse('post-detail', kwargs={'pk': post.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)

    def test_post_create_view_requires_login(self):
        """Test creating post requires authentication"""
        response = self.client.get(reverse('post-create'))

        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)

    def test_post_create_view_authenticated(self):
        """Test authenticated user can create post"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('post-create'), {
            'title': 'New Post',
            'content': 'New content',
            'status': 'draft'
        })

        self.assertEqual(response.status_code, 302)  # Redirect after create
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.title, 'New Post')
        self.assertEqual(post.author, self.user)

    def test_post_update_view_author_only(self):
        """Test only author can update their post"""
        post = baker.make(Post, author=self.user)

        # Other user tries to update
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.post(
            reverse('post-update', kwargs={'pk': post.pk}),
            {'title': 'Updated', 'content': 'Updated content'}
        )

        self.assertEqual(response.status_code, 403)  # Forbidden

        # Author updates successfully
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post-update', kwargs={'pk': post.pk}),
            {'title': 'Updated', 'content': 'Updated content'}
        )

        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated')

    def test_post_delete_view_author_only(self):
        """Test only author can delete their post"""
        post = baker.make(Post, author=self.user)

        # Other user tries to delete
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.post(reverse('post-delete', kwargs={'pk': post.pk}))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), 1)  # Still exists

        # Author deletes successfully
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post-delete', kwargs={'pk': post.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

# pytest tests
@pytest.mark.django_db
class TestPostAPI:
    """Test Post API endpoints"""

    def test_list_posts_unauthorized(self, api_client):
        """Test listing posts without authentication"""
        response = api_client.get('/api/posts/')

        assert response.status_code == 200
        assert 'results' in response.data

    def test_create_post_requires_auth(self, api_client):
        """Test creating post requires authentication"""
        response = api_client.post('/api/posts/', {
            'title': 'Test',
            'content': 'Test content'
        })

        assert response.status_code == 401  # Unauthorized

    def test_create_post_authenticated(self, api_client, user):
        """Test creating post with authentication"""
        api_client.force_authenticate(user=user)

        response = api_client.post('/api/posts/', {
            'title': 'Test Post',
            'content': 'Test content'
        })

        assert response.status_code == 201
        assert response.data['title'] == 'Test Post'
        assert response.data['author']['id'] == user.id

    def test_update_post_permission(self, api_client, user, other_user):
        """Test only author can update post"""
        post = baker.make(Post, author=user)

        # Other user tries to update
        api_client.force_authenticate(user=other_user)
        response = api_client.patch(f'/api/posts/{post.id}/', {
            'title': 'Updated'
        })

        assert response.status_code == 403

        # Author updates
        api_client.force_authenticate(user=user)
        response = api_client.patch(f'/api/posts/{post.id}/', {
            'title': 'Updated'
        })

        assert response.status_code == 200
        assert response.data['title'] == 'Updated'

# Performance tests
class PostPerformanceTests(TestCase):
    """Test query performance"""

    def test_post_list_query_count(self):
        """Test N+1 query prevention"""
        baker.make(Post, _quantity=10)

        with self.assertNumQueries(2):  # 1 for posts, 1 for count
            response = self.client.get(reverse('post-list'))
            list(response.context['posts'])  # Force evaluation

    def test_post_detail_query_count(self):
        """Test query optimization for detail view"""
        post = baker.make(Post)
        baker.make('Comment', post=post, _quantity=5)

        with self.assertNumQueries(3):  # Post, author, comments
            response = self.client.get(reverse('post-detail', kwargs={'pk': post.pk}))
            response.render()
```

**Why this matters:**
Without proper testing:
- Bugs reach production
- Regressions go unnoticed
- Code becomes fragile
- Refactoring is risky

**Best practice:**
Test models, views, APIs, forms. Test permissions and security. Test edge cases and error handling. Test query performance. Use factories (model_bakery, factory_boy) for test data.

---

## Deployment - Production Configuration

### DEPLOY-STATIC: Static Files Configuration

**Principle:** Properly configure static and media files for production with CDN.

**Bad Example:**
```python
# settings.py
DEBUG = True  # Never in production!
STATIC_URL = '/static/'
# No STATIC_ROOT configured
# No whitenoise or CDN configured
# Static files not collected
```

**Good Example:**
```python
# settings/base.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Use WhiteNoise for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # After SecurityMiddleware
    # ... other middleware
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# settings/production.py
# Use S3 for static and media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')

# CloudFront CDN
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 24 hours
}

# Security headers for S3
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

# Separate buckets for static and media (recommended)
AWS_STATIC_LOCATION = 'static'
AWS_MEDIA_LOCATION = 'media'

STATICFILES_STORAGE = 'myapp.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'myapp.storage_backends.MediaStorage'

# storage_backends.py
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    default_acl = 'public-read'

class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False

# Collect static files before deployment:
# python manage.py collectstatic --noinput
```

**Why this matters:**
Poor static file configuration causes:
- Slow page loads
- High server load
- Bandwidth costs
- Poor user experience

**Best practice:**
Use WhiteNoise or CDN (S3/CloudFront) for static files. Collect static files in deployment. Use separate storage for static vs media. Configure caching headers.

---

### DEPLOY-DB: Database Configuration for Production

**Principle:** Use production-grade database with proper connection pooling, replication, and backup.

**Bad Example:**
```python
# Using SQLite in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',  # File-based, doesn't scale
    }
}

# No connection pooling
# No read replicas
# No backup configuration
```

**Good Example:**
```python
# settings/production.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling (10 minutes)
        'OPTIONS': {
            'connect_timeout': 10,
            'sslmode': 'require',  # Require SSL
        },
    }
}

# Read replica for read-heavy workloads
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_WRITE_HOST'),
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    },
    'read_replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_READ_HOST'),
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

# Database router for read/write split
class PrimaryReplicaRouter:
    """Route reads to replica, writes to primary"""

    def db_for_read(self, model, **hints):
        return 'read_replica'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'

DATABASE_ROUTERS = ['myapp.db_routers.PrimaryReplicaRouter']

# Connection pooling with pgbouncer
# Install: sudo apt-get install pgbouncer
# Configure pgbouncer.ini:
# [databases]
# myapp = host=localhost port=5432 dbname=myapp
# [pgbouncer]
# listen_port = 6432
# pool_mode = transaction
# max_client_conn = 100
# default_pool_size = 25

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '6432',  # pgbouncer port
    }
}

# Backup configuration (using django-dbbackup)
DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': config('AWS_BACKUP_ACCESS_KEY_ID'),
    'secret_key': config('AWS_BACKUP_SECRET_ACCESS_KEY'),
    'bucket_name': config('AWS_BACKUP_BUCKET_NAME'),
}

# Automated backups (in cron or Celery beat):
# python manage.py dbbackup
# python manage.py mediabackup
```

**Why this matters:**
Poor database configuration causes:
- Connection exhaustion under load
- Slow queries (no connection pooling)
- Data loss (no backups)
- Downtime during failures

**Best practice:**
Use PostgreSQL or MySQL for production. Enable connection pooling. Use read replicas for read-heavy apps. Automated backups to S3. Monitor database performance.

---

## Logging & Monitoring

### LOG-CONFIG: Logging Configuration

**Principle:** Configure comprehensive logging for debugging and monitoring in production.

**Bad Example:**
```python
# No logging configured
# Errors lost
# No way to debug production issues
```

**Good Example:**
```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024 * 1024 * 15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins', 'sentry'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['console', 'file', 'sentry'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Sentry for error tracking
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
    ],
    environment=config('ENVIRONMENT', default='production'),
    traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
    send_default_pii=False,  # Don't send PII to Sentry
)

# Using logging in code
import logging

logger = logging.getLogger(__name__)

def process_order(order_id):
    logger.info(f'Processing order {order_id}')

    try:
        order = Order.objects.get(id=order_id)
        # ... process order
        logger.info(f'Order {order_id} processed successfully')
    except Order.DoesNotExist:
        logger.error(f'Order {order_id} not found')
        raise
    except Exception as e:
        logger.exception(f'Error processing order {order_id}: {e}')
        raise

# Structured logging with context
logger.info(
    'User login',
    extra={
        'user_id': user.id,
        'ip_address': request.META.get('REMOTE_ADDR'),
        'user_agent': request.META.get('HTTP_USER_AGENT'),
    }
)
```

**Why this matters:**
Without logging:
- Can't debug production issues
- No visibility into errors
- Can't track user actions
- Can't identify performance bottlenecks

**Best practice:**
Configure comprehensive logging. Use log levels appropriately. Send errors to Sentry/monitoring service. Use structured logging. Rotate log files.

---

## Anti-Patterns - Common Mistakes

### ANTI-FAT-MODELS: Avoid Fat Models

**Principle:** Keep models focused on data and simple business logic. Use services for complex operations.

**Bad Example:**
```python
# Fat model with too much responsibility
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def process_payment(self, payment_method):
        # Payment processing logic
        if payment_method == 'credit_card':
            response = stripe.Charge.create(amount=self.total, ...)
        elif payment_method == 'paypal':
            response = paypal.charge(self.total, ...)
        # ... 50 more lines

    def send_confirmation_email(self):
        # Email logic
        # ... 30 lines

    def update_inventory(self):
        # Inventory logic
        # ... 40 lines

    def generate_invoice_pdf(self):
        # PDF generation
        # ... 60 lines

    # Model has 200+ lines of business logic!
```

**Good Example:**
```python
# Thin model - just data and simple methods
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

    def is_paid(self):
        return self.status == 'paid'

# Service layer for business logic
# services/order_service.py
class OrderService:
    @staticmethod
    def process_payment(order, payment_method, payment_details):
        """Process payment for an order"""
        payment_service = PaymentService()

        try:
            charge = payment_service.charge(
                amount=order.total,
                method=payment_method,
                details=payment_details
            )

            order.status = 'paid'
            order.save()

            return charge
        except PaymentError as e:
            logger.error(f'Payment failed for order {order.id}: {e}')
            raise

    @staticmethod
    def complete_order(order):
        """Complete order processing workflow"""
        # Update inventory
        InventoryService.reserve_items(order.items.all())

        # Send email
        EmailService.send_order_confirmation(order)

        # Generate invoice
        InvoiceService.generate_pdf(order)

        # Update status
        order.status = 'completed'
        order.save()

# services/payment_service.py
class PaymentService:
    def charge(self, amount, method, details):
        if method == 'credit_card':
            return self._charge_credit_card(amount, details)
        elif method == 'paypal':
            return self._charge_paypal(amount, details)
        else:
            raise ValueError(f'Unknown payment method: {method}')

    def _charge_credit_card(self, amount, details):
        # Stripe integration
        return stripe.Charge.create(
            amount=int(amount * 100),
            currency='usd',
            source=details['token'],
        )

    def _charge_paypal(self, amount, details):
        # PayPal integration
        pass

# Using services in views
from myapp.services.order_service import OrderService

def checkout(request):
    order = get_object_or_404(Order, id=request.POST['order_id'])

    try:
        OrderService.process_payment(
            order=order,
            payment_method=request.POST['payment_method'],
            payment_details=request.POST.get('payment_details')
        )

        OrderService.complete_order(order)

        return JsonResponse({'status': 'success'})
    except PaymentError as e:
        return JsonResponse({'error': str(e)}, status=400)
```

**Why this matters:**
Fat models cause:
- Tight coupling
- Hard to test
- Hard to maintain
- Violates single responsibility principle

**Best practice:**
Keep models thin - just data and simple methods. Use service layer for business logic. Use managers/querysets for data access logic. Separate concerns.

---

## Multi-Tenancy & Data Isolation Patterns

### TENANT-ROUTER: Database Routers Per Tenant

```python
class TenantRouter:
    def db_for_read(self, model, **hints):
        tenant = getattr(threading.local(), "tenant", "default")
        return f"tenant_{tenant}"

    def db_for_write(self, model, **hints):
        tenant = getattr(threading.local(), "tenant", "default")
        return f"tenant_{tenant}"
```

- Require middleware to set `threadlocal.tenant` (from subdomain, JWT claim, etc.).
- Validate router coverage in tests—missing router entries default to `default` DB and leak data.

### TENANT-SCHEMA: Separate Schemas or Shared Table Strategy

- Shared tenancy: include `tenant_id` FK on every shared table and enforce `QuerySet.filter(tenant=request.tenant)` via custom managers or libraries (django-tenant-schemas, django-multitenant).
- Schema-per-tenant: use PostgreSQL schemas created via migrations; run planar migrations for each tenant.

### TENANT-RLS: Database-Level Safeguards

- For PostgreSQL, combine Django queryset filters with RLS policies to guard against bypasses (see SEC-RLS).
- For MySQL/SQL Server, create views that filter on `current_tenant` session variables and restrict applications to those views.

### TENANT-CACHE: Cache Key Namespacing

```python
def tenant_cache_key(tenant_id, *parts):
    slug = ":".join(str(part) for part in parts)
    return f"tenant:{tenant_id}:{slug}"
```
- Avoid cross-tenant cache bleed by namespacing keys (Redis, Memcached) and using per-tenant local-memory caches when needed.

### DATA-RESIDENCY & SHARDING

- Respect regulatory residency by pinning tenants to regions and storing the mapping in a control plane table.
- For sharding, implement `SHARDING-STRATEGY`: consistent hash → database alias → router. Document rebalancing workflows and background migrations.

### OBSERVE-TENANT: Logging & Metrics Tags

- Include `tenant_id`, `region`, and feature flag metadata in logs/metrics to diagnose tenant-specific incidents.

## Container & Kubernetes Deployment

### DEPLOY-CONTAINER: Docker Best Practices

- Use multi-stage builds with `python:3.x-slim` base, install OS deps (libpq, build-essential) only in builder stage.
- Run as non-root, set `PYTHONUNBUFFERED=1`, `DJANGO_SETTINGS_MODULE` via env vars.
- Collect static files during build to keep runtime pods lean.

### DEPLOY-K8S: Kubernetes & Autoscaling

- Configure readiness/liveness probes hitting `/healthz` endpoints that check DB/cache connectivity.
- Use `gunicorn` with `--max-requests` to prevent memory leaks, and horizontal pod autoscalers based on CPU + request latency.
- Externalize secrets via K8s Secrets or Vault injectors; never bake into images.

### DEPLOY-EDGE / SERVERLESS

- For ASGI deployments (Channels, Fast APIs), document `lifespan` hooks and concurrency limits.
- Ensure cold-start safe settings (lazy DB connections, cached settings) and ephemeral storage strategies.

---

## Summary

Production-ready Django applications must be:

**🔒 SECURE**
- Protection against OWASP Top 10
- Proper authentication and authorization
- Secret management and HTTPS
- Security headers and CSRF protection

**⚡ FAST**
- Query optimization (avoid N+1)
- Database indexing
- Caching at multiple levels
- Async views for I/O operations

**📈 SCALABLE**
- Proper database configuration
- Read replicas and connection pooling
- Background task processing
- CDN for static files

**✅ TESTED**
- Comprehensive test coverage
- Unit, integration, and performance tests
- CI/CD pipeline

**📊 MONITORED**
- Comprehensive logging
- Error tracking (Sentry)
- Performance monitoring
- Database query monitoring

**🏗️ MAINTAINABLE**
- Clean architecture (thin models, service layer)
- Django best practices
- Proper settings management
- Good documentation

---

*Based on Django documentation, Two Scoops of Django, Django security guidelines, and production best practices*
