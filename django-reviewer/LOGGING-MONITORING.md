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

### LOG-GETLOGGER: Use Module-Level Logger with `__name__`

**Principle:** Always initialize loggers using `__name__` for automatic namespace organization.

**Bad Example:**
```python
# views.py
import logging

# Anti-pattern: Generic logger name
logger = logging.getLogger('myapp')  # Loses file context

# Anti-pattern: Hardcoded string
logger = logging.getLogger('views')  # Doesn't match module path

# Anti-pattern: Root logger
logger = logging.getLogger()  # Too broad, affects all logging

def my_view(request):
    logger.info('Processing request')  # Which view? Which module?
```

**Good Example:**
```python
# myapp/views.py
import logging

# Best practice: Use __name__ for automatic module path
logger = logging.getLogger(__name__)  # 'myapp.views'

def my_view(request):
    logger.info('Processing request')  # Clear: myapp.views


# myapp/services/payment.py
import logging

logger = logging.getLogger(__name__)  # 'myapp.services.payment'

class PaymentService:
    def process(self, order):
        logger.info('Processing payment for order %s', order.id)
```

**Why this matters:**
- `__name__` automatically creates hierarchical logger names (`myapp.views`, `myapp.models`)
- Enables fine-grained control: silence `myapp.services` while keeping `myapp.views` at DEBUG
- Log messages include module context for easier debugging
- Matches Django's own logging hierarchy

**Sources:** [Django Logging](https://docs.djangoproject.com/en/5.2/topics/logging/), [Lincoln Loop](https://lincolnloop.com/blog/django-logging-right-way/)

---

### LOG-EXCEPTION: Use `logger.exception()` for Tracebacks

**Principle:** Always use `logger.exception()` in except blocks to capture full tracebacks.

**Bad Example:**
```python
# Anti-pattern: Swallowing exceptions
try:
    process_payment(order)
except Exception:
    pass  # Silent failure!

# Anti-pattern: Losing traceback
try:
    process_payment(order)
except Exception as e:
    logger.error(f'Payment failed: {e}')  # No traceback!

# Anti-pattern: Print statements
try:
    process_payment(order)
except Exception as e:
    print(f'Error: {e}')  # Lost in production!
```

**Good Example:**
```python
import logging

logger = logging.getLogger(__name__)

# Best practice: logger.exception() captures traceback automatically
try:
    process_payment(order)
except PaymentError as e:
    logger.exception('Payment failed for order %s', order.id)
    raise  # Re-raise after logging

# Alternative: logger.error() with exc_info=True
try:
    process_payment(order)
except PaymentError as e:
    logger.error(
        'Payment failed for order %s: %s',
        order.id,
        e,
        exc_info=True  # Include traceback
    )
    raise

# For non-exception context but want stack trace
logger.warning(
    'Unexpected state in order %s',
    order.id,
    stack_info=True  # Include call stack
)
```

**Why this matters:**
- `logger.exception()` automatically includes full traceback
- `print()` statements don't appear in production logs
- Without tracebacks, debugging production issues is nearly impossible
- `exc_info=True` achieves the same but requires explicit flag

**Sources:** [Django Logging](https://docs.djangoproject.com/en/5.2/topics/logging/), [Python Logging Best Practices](https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/)

---

### LOG-NO-PRINT: Never Use Print Statements in Production Code

**Principle:** Replace all `print()` statements with proper logging calls.

**Bad Example:**
```python
# Anti-pattern: Print statements everywhere
def process_order(order):
    print(f'Processing order {order.id}')  # Lost in production!

    if order.total > 1000:
        print('High value order')  # No log level control

    print(f'Order {order.id} complete')  # Can't filter or route


class PaymentView(View):
    def post(self, request):
        print(request.POST)  # Security risk! May log sensitive data
        # ...
```

**Good Example:**
```python
import logging

logger = logging.getLogger(__name__)

def process_order(order):
    logger.info('Processing order %s', order.id)

    if order.total > 1000:
        logger.info('High value order: %s (total: %s)', order.id, order.total)

    logger.info('Order %s complete', order.id)


class PaymentView(View):
    def post(self, request):
        # Log safely without sensitive data
        logger.debug(
            'Payment request received',
            extra={'user_id': request.user.id}
        )
        # ...
```

**Why this matters:**
- `print()` goes to stdout which may not be captured in production
- No log levels - can't filter debug vs error messages
- No timestamps, module names, or other metadata
- Can't route to different destinations (file, Sentry, etc.)
- May accidentally log sensitive data

**Sources:** [Django Logging Guide](https://mattsegal.dev/file-logging-django.html)

---

### LOG-SENSITIVE: Never Log Sensitive Data

**Principle:** Explicitly prevent logging of passwords, tokens, PII, and other sensitive information.

**Bad Example:**
```python
# Anti-pattern: Logging credentials
def authenticate(username, password):
    logger.info(f'Login attempt: {username}, {password}')  # PASSWORD LOGGED!
    # ...

# Anti-pattern: Logging full request
def payment_view(request):
    logger.debug(f'Request data: {request.POST}')  # Credit card in logs!
    # ...

# Anti-pattern: Logging tokens
def api_call(api_key):
    logger.info(f'API call with key: {api_key}')  # API KEY EXPOSED!
    # ...

# Anti-pattern: AdminEmailHandler with include_html
LOGGING = {
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,  # DANGER: Full stack with local vars!
        },
    },
}
```

**Good Example:**
```python
import logging

logger = logging.getLogger(__name__)

# Best practice: Never log credentials
def authenticate(username, password):
    logger.info('Login attempt for user: %s', username)  # No password!
    # ...

# Best practice: Log only safe fields
def payment_view(request):
    logger.info(
        'Payment request',
        extra={
            'user_id': request.user.id,
            'amount': request.POST.get('amount'),
            # Never log: card_number, cvv, etc.
        }
    )
    # ...

# Best practice: Mask sensitive values
def api_call(api_key):
    masked_key = f'{api_key[:4]}...{api_key[-4:]}' if len(api_key) > 8 else '***'
    logger.info('API call with key: %s', masked_key)
    # ...

# Best practice: Use Django's sensitive filtering
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters

@sensitive_variables('password', 'api_key')
@sensitive_post_parameters('password', 'credit_card')
def process_payment(request):
    password = request.POST['password']
    # Variables marked as sensitive won't appear in error reports
    # ...

# Safe AdminEmailHandler config
LOGGING = {
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': False,  # Safe: No local variable values
        },
    },
}

# Better: Use Sentry for error tracking
import sentry_sdk

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    send_default_pii=False,  # Don't send PII to Sentry
)
```

**Why this matters:**
- Logged credentials can be stolen from log files
- PII in logs violates GDPR/CCPA and privacy regulations
- `AdminEmailHandler` with `include_html=True` emails full stack traces with variable values
- Log files often have less restrictive access than production databases

**Sources:** [Django Logging Security](https://docs.djangoproject.com/en/5.2/topics/logging/), [Django Sensitive Data](https://docs.djangoproject.com/en/5.2/howto/error-reporting/)

---

### LOG-LEVELS: Use Appropriate Log Levels

**Principle:** Match log level to message severity for effective filtering and alerting.

**Bad Example:**
```python
# Anti-pattern: Everything at INFO
logger.info('Starting server')
logger.info('User not found')  # Should be WARNING
logger.info('Database connection failed')  # Should be ERROR!
logger.info('Processing item 1 of 1000')  # Should be DEBUG

# Anti-pattern: Everything at ERROR
logger.error('Request received')  # Not an error!
logger.error('Cache miss')  # Normal operation
```

**Good Example:**
```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: Detailed diagnostic information (development only)
logger.debug('Query parameters: %s', params)
logger.debug('Cache key: %s', cache_key)
logger.debug('Entering function with args: %s', args)

# INFO: Normal operation events worth recording
logger.info('User %s logged in', user.id)
logger.info('Order %s created', order.id)
logger.info('Email sent to %s', email)

# WARNING: Unexpected but handled situations
logger.warning('Cache miss for key: %s', key)
logger.warning('Deprecated API called: %s', endpoint)
logger.warning('Rate limit approaching for user %s', user.id)
logger.warning('Retry %d of %d for operation', attempt, max_attempts)

# ERROR: Failures requiring attention
logger.error('Payment failed for order %s: %s', order.id, error)
logger.error('External API unavailable: %s', service_name)
logger.error('Database query timeout')

# CRITICAL: System-wide failures (rarely used)
logger.critical('Database connection pool exhausted')
logger.critical('Out of disk space')

# Production logging config
LOGGING = {
    'loggers': {
        'django': {
            'level': 'INFO',  # Production default
        },
        'django.db.backends': {
            'level': 'WARNING',  # Reduce SQL noise
        },
        'myapp': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),  # Configurable
        },
    },
}
```

**Log Level Guidelines:**

| Level | Use For | Production Default |
|-------|---------|-------------------|
| DEBUG | Development diagnostics, SQL queries | OFF |
| INFO | Business events, user actions | ON |
| WARNING | Handled anomalies, deprecations | ON |
| ERROR | Failures requiring investigation | ON + Alert |
| CRITICAL | System-wide failures | ON + Page |

**Why this matters:**
- Proper levels enable filtering: show only ERRORs in production
- Alerting systems can trigger on ERROR/CRITICAL only
- DEBUG in production creates massive, unreadable logs
- Wrong levels hide real problems or create alert fatigue

**Sources:** [Django Logging](https://docs.djangoproject.com/en/5.2/topics/logging/)

---

### LOG-FORMAT: Use Structured Logging for Production

**Principle:** Use JSON or structured logging format for machine-parseable logs in production.

**Bad Example:**
```python
# Anti-pattern: Unstructured string logging
logger.info(f'User {user.id} logged in from {ip} at {datetime.now()}')
logger.info(f'Order {order.id} created by user {user.id} for ${amount}')

# Hard to parse, grep, or analyze
# Different formats across different log lines
```

**Good Example:**
```python
import logging
import json

logger = logging.getLogger(__name__)

# Option 1: Use 'extra' for structured context
logger.info(
    'User logged in',
    extra={
        'user_id': user.id,
        'ip_address': ip,
        'user_agent': user_agent,
    }
)

logger.info(
    'Order created',
    extra={
        'order_id': order.id,
        'user_id': user.id,
        'amount': str(order.total),
        'items_count': order.items.count(),
    }
)

# Option 2: JSON formatter configuration
LOGGING = {
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',  # JSON output
        },
    },
}

# Option 3: django-structlog for comprehensive structured logging
# pip install django-structlog

# settings.py
INSTALLED_APPS = [
    'django_structlog',
    # ...
]

MIDDLEWARE = [
    'django_structlog.middlewares.RequestMiddleware',
    # ...
]

# Produces logs like:
# {"request_id": "abc-123", "user_id": 1, "ip": "1.2.3.4",
#  "event": "user_logged_in", "level": "info"}

# Option 4: Request correlation ID
# pip install django-cid or asgi-correlation-id

# Adds request_id to all logs for tracing
logger.info('Processing payment', extra={'request_id': request.correlation_id})
```

**Why this matters:**
- JSON logs can be parsed by log aggregators (CloudWatch, Datadog, ELK)
- Structured data enables queries: "show all logs where user_id=123"
- Request IDs correlate logs across services
- Consistent format enables automated analysis and alerting

**Sources:** [django-structlog](https://django-structlog.readthedocs.io/), [SigNoz Django Logging](https://signoz.io/guides/django-logging/)

---

### LOG-ROTATION: Configure Log Rotation in Production

**Principle:** Use `RotatingFileHandler` or `TimedRotatingFileHandler` to prevent disk exhaustion.

**Bad Example:**
```python
# Anti-pattern: FileHandler without rotation
LOGGING = {
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',  # Grows forever!
            'filename': '/var/log/django/app.log',
        },
    },
}

# Result: Log file grows until disk is full
# Production crashes at 3am
```

**Good Example:**
```python
LOGGING = {
    'handlers': {
        # Size-based rotation
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'maxBytes': 1024 * 1024 * 50,  # 50MB per file
            'backupCount': 10,  # Keep 10 old files
            'formatter': 'verbose',
        },
        # Time-based rotation
        'daily_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'when': 'midnight',  # Rotate at midnight
            'interval': 1,  # Every 1 day
            'backupCount': 30,  # Keep 30 days
            'formatter': 'verbose',
        },
        # Separate error log
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# For containerized apps: Log to stdout and let orchestrator handle
LOGGING = {
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
# Docker/K8s captures stdout and handles rotation/aggregation
```

**Why this matters:**
- Unrotated logs fill disk, crashing production
- `RotatingFileHandler` limits total disk usage
- Separate error logs make critical issues easier to find
- Containerized apps should use stdout (12-factor app principle)

**Sources:** [Django Logging](https://docs.djangoproject.com/en/5.2/topics/logging/), [Django Circle](https://djangocircle.com/best-practices-and-solutions-for-managing-django-logs-in-production/)

---

### LOG-DISABLE-EXISTING: Never Set `disable_existing_loggers: True`

**Principle:** Keep `disable_existing_loggers: False` to preserve Django's default logging.

**Bad Example:**
```python
# Anti-pattern: Disabling existing loggers
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,  # DANGER!
    # ...
}

# Result:
# - django.request logger silenced
# - django.security logger silenced
# - Third-party library loggers silenced
# - Only your explicitly defined loggers work
```

**Good Example:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Always False!
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # Customize specific loggers while keeping defaults
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Silence noisy third-party loggers
        'urllib3': {
            'level': 'WARNING',
        },
        'boto3': {
            'level': 'WARNING',
        },
    },
}
```

**Why this matters:**
- `disable_existing_loggers: True` silently discards logs from unconfigured loggers
- Django's security and request loggers become useless
- Hard to debug because logs simply disappear
- Default `dictConfig` behavior is `True` - must explicitly set `False`

**Sources:** [Django Logging](https://docs.djangoproject.com/en/5.2/topics/logging/)

---

### LOG-REQUEST: Log Request Context with Middleware

**Principle:** Use middleware to automatically log request lifecycle and add context.

**Bad Example:**
```python
# Anti-pattern: Manual logging in every view
class OrderView(View):
    def post(self, request):
        logger.info('Request started')  # Repetitive
        # ... process
        logger.info('Request completed')  # Forget to add sometimes
```

**Good Example:**
```python
# middleware.py
import logging
import time
import uuid

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add request ID for correlation
        request.request_id = str(uuid.uuid4())

        # Log request start
        start_time = time.time()
        logger.info(
            'Request started',
            extra={
                'request_id': request.request_id,
                'method': request.method,
                'path': request.path,
                'user_id': getattr(request.user, 'id', None),
                'ip': self.get_client_ip(request),
            }
        )

        response = self.get_response(request)

        # Log request end
        duration = time.time() - start_time
        logger.info(
            'Request completed',
            extra={
                'request_id': request.request_id,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
            }
        )

        # Add request ID to response headers for debugging
        response['X-Request-ID'] = request.request_id

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


# settings.py
MIDDLEWARE = [
    'myapp.middleware.RequestLoggingMiddleware',  # Early in stack
    # ...
]

# Or use django-structlog for this built-in
MIDDLEWARE = [
    'django_structlog.middlewares.RequestMiddleware',
    # ...
]
```

**Why this matters:**
- Automatic logging for all requests
- Request IDs enable tracing across logs
- Duration tracking identifies slow endpoints
- Consistent context (IP, user, path) in all logs

**Sources:** [django-structlog](https://django-structlog.readthedocs.io/), [Better Stack](https://betterstack.com/community/guides/scaling-python/error-handling-django/)

---

### LOG-DB-QUERIES: Monitor Database Query Performance

**Principle:** Enable query logging in development and monitor slow queries in production.

**Bad Example:**
```python
# No query logging - unaware of N+1 problems
# No slow query monitoring - performance issues go unnoticed
```

**Good Example:**
```python
# Development: Log all SQL queries
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Shows all SQL
            'propagate': False,
        },
    },
}

# Production: Log only slow queries
# Option 1: Use django-debug-toolbar in dev
# Option 2: Custom middleware for slow queries

class SlowQueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.db import connection

        initial_queries = len(connection.queries)
        response = self.get_response(request)

        final_queries = len(connection.queries)
        total_time = sum(
            float(q['time'])
            for q in connection.queries[initial_queries:]
        )

        query_count = final_queries - initial_queries

        if total_time > 1.0:  # More than 1 second
            logger.warning(
                'Slow database queries',
                extra={
                    'path': request.path,
                    'query_count': query_count,
                    'total_time_seconds': round(total_time, 3),
                }
            )

        if query_count > 50:  # Possible N+1
            logger.warning(
                'High query count (possible N+1)',
                extra={
                    'path': request.path,
                    'query_count': query_count,
                }
            )

        return response

# Production config: Only warnings and errors for db.backends
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # Only warnings in production
            'propagate': False,
        },
    },
}
```

**Why this matters:**
- DEBUG level in development reveals N+1 queries early
- Slow query alerts catch performance regressions
- High query count warnings indicate missing `select_related`
- Production shouldn't log every query (too verbose)

**Sources:** [Django Logging](https://docs.djangoproject.com/en/5.2/topics/logging/)

---

