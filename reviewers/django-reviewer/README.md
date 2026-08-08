# Django Production Readiness Reviewer

Comprehensive review skill for Django projects focusing on production readiness, security, performance, and scalability for large-scale applications.

## 🎯 Purpose

This skill provides thorough, expert-level review of Django projects covering:

- **Security** - OWASP Top 10, Django-specific vulnerabilities, authentication, authorization
- **Performance** - Query optimization, N+1 prevention, caching, async operations
- **Scalability** - Database design, architecture patterns, infrastructure
- **Code Quality** - Django best practices, clean architecture, maintainability
- **API Design** - Django REST Framework patterns, versioning, permissions
- **Testing** - Comprehensive test coverage, quality over metrics
- **Deployment** - Production configuration, static files, monitoring

## 📋 Coverage

### Security (20+ Guidelines)
- SQL injection prevention (SEC-SQL)
- XSS protection (SEC-XSS)
- CSRF protection (SEC-CSRF)
- HTTPS configuration (SEC-HTTPS)
- Secret management (SEC-SECRETS)
- Debug mode protection (SEC-DEBUG)
- Password hashing (SEC-AUTH)
- File upload security (SEC-UPLOAD)
- Clickjacking protection (SEC-CLICKJACK)
- Security headers (SEC-HEADERS)

### Models & Database (15+ Guidelines)
- N+1 query prevention (MODEL-N+1)
- Database indexing (MODEL-INDEX)
- Query optimization (MODEL-QUERY)
- select_related/prefetch_related usage (MODEL-SELECT)
- Migration management (MODEL-MIGRATION)
- Database constraints (MODEL-CONSTRAINT)
- Signal patterns (MODEL-SIGNAL)

### Views & URLs (12+ Guidelines)
- Class-based view patterns (VIEW-CBV)
- Permission checking (VIEW-PERM)
- Form handling (VIEW-FORM)
- Transaction management (VIEW-ATOMIC)
- URL naming (URL-NAME)

### Performance (15+ Guidelines)
- Caching strategies (PERF-CACHE)
- Async views (PERF-ASYNC)
- Background tasks (PERF-CELERY)
- Database connection pooling (PERF-DB)
- Query optimization (PERF-QUERY)

### API Design (12+ Guidelines)
- RESTful design (API-REST)
- API versioning (API-VERSION)
- Serializer patterns (API-SERIAL)
- API permissions (API-PERM)
- Rate limiting (API-THROTTLE)
- Authentication (API-AUTH)

### Configuration (10+ Guidelines)
- Settings management (CONFIG-ENV)
- Environment separation (CONFIG-SPLIT)
- Secret management (CONFIG-SECRET)
- Database configuration (CONFIG-DB)
- Cache configuration (CONFIG-CACHE)

### Testing (10+ Guidelines)
- Test coverage (TEST-COVERAGE)
- Factory patterns (TEST-FACTORY)
- Mocking (TEST-MOCK)
- Performance testing (TEST-PERF)

### Deployment (10+ Guidelines)
- Static files (DEPLOY-STATIC)
- Media files (DEPLOY-MEDIA)
- Database setup (DEPLOY-DB)
- Logging (LOG-CONFIG)
- Monitoring (MONITOR-SENTRY)

### Anti-Patterns (5+ Guidelines)
- Fat models (ANTI-FAT-MODELS)
- God objects (ANTI-GOD)
- Premature optimization (ANTI-OPTIMIZE)

## 🚀 Use Cases

### Code Review
```
"Review this Django view for security and performance issues"
"Check this model for query optimization opportunities"
"Analyze this API endpoint for best practices"
```

### Security Audit
```
"Perform a security review of this Django application"
"Check this code for OWASP vulnerabilities"
"Review authentication and authorization implementation"
```

### Performance Optimization
```
"Identify N+1 queries in this code"
"Review caching strategy"
"Optimize database queries in this view"
```

### Production Readiness
```
"Review settings.py for production deployment"
"Check this project for production readiness"
"Validate deployment configuration"
```

### Architecture Review
```
"Review this Django project architecture"
"Evaluate scalability of this design"
"Check database schema design"
```

## 📊 Review Output

Each review includes:

- **Mnemonic IDs** for easy reference (e.g., SEC-SQL, PERF-N+1)
- **Current code** showing the issue
- **Improved code** following best practices
- **Why this matters** explaining security/performance impact
- **Best practice** referencing Django documentation
- **Django version** compatibility notes when relevant

Example output:

````markdown
## Django Review: UserAuthentication Module

### 🚨 Critical Issues

#### SEC-SQL: SQL Injection Vulnerability

**Current code:**
```python
user = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")[0]
```

**Improved code:**
```python
user = User.objects.get(username=username)
```

**Why this matters:**
SQL injection allows attackers to execute arbitrary SQL...

**Best practice:**
Use Django ORM's parameterized queries...

---

#### PERF-N+1: N+1 Query Problem

**Current code:**
```python
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # N queries!
```

**Improved code:**
```python
posts = Post.objects.select_related('author').all()
```

**Why this matters:**
N+1 queries create massive database load...
````

## ✅ Best For

- Large-scale production Django applications
- Security-critical applications
- High-traffic websites
- API-first applications (Django REST Framework)
- Projects requiring high performance
- Enterprise Django applications

## 📚 Based On

- Django Official Documentation
- Two Scoops of Django
- Django Security Documentation
- OWASP Top 10
- Django REST Framework Best Practices
- Production deployment patterns
- Real-world large-scale Django applications

## 🔍 What This Skill Checks

### Security Review
- OWASP Top 10 vulnerabilities
- Django-specific security issues
- Authentication and authorization
- Secret and credential management
- HTTPS and SSL configuration
- Input validation and sanitization
- File upload security
- Session security

### Performance Review
- Database query optimization
- N+1 query detection
- Proper use of select_related/prefetch_related
- Index usage
- Caching implementation
- Async view usage
- Background task processing

### Code Quality Review
- Django conventions and best practices
- Model design patterns
- View organization (CBVs vs FBVs)
- Form handling
- URL design
- Template usage
- Service layer architecture

### API Review (Django REST Framework)
- Serializer design
- Permission system
- Authentication methods
- API versioning
- Rate limiting
- Error handling
- Response formatting

### Configuration Review
- Settings organization (dev/prod split)
- Environment variable usage
- Secret management
- Database configuration
- Cache configuration
- Static/media file setup
- Middleware configuration

### Test Coverage Review
- Test quality and coverage
- Factory usage
- Mocking patterns
- Integration tests
- API tests
- Performance tests

### Deployment Review
- Production settings
- Static file configuration
- Media file handling
- Database setup (connection pooling, replicas)
- Logging configuration
- Error monitoring (Sentry)
- Performance monitoring

## 💡 Tips for Best Results

1. **Provide Context**: Mention if this is for a new project, refactoring, or production deployment
2. **Specify Concerns**: Indicate specific areas (security, performance, scalability)
3. **Include Related Code**: Show models, views, and serializers together for better analysis
4. **Mention Scale**: Indicate expected user load and data volume
5. **Django Version**: Specify Django version for version-specific recommendations

## 🎓 Learning Opportunity

Each review is educational, explaining:
- **Why** something is a problem
- **How** it impacts production
- **What** the best practice is
- **Where** to find more information

## ⚠️ Not Covered

This skill focuses on Django-specific patterns. It does NOT cover:
- Frontend JavaScript frameworks (React, Vue)
- CSS/styling issues
- DevOps/infrastructure setup details
- Database administration
- Network configuration
- General Python style (use other Python reviewers for that)

## 🔧 Complementary Skills

Use alongside:
- **python-security-privacy-reviewer** - For deeper security analysis
- **python-refactoring-reviewer** - For general Python refactoring
- **python-test-reviewer** - For test quality review
- **python-zen-reviewer** - For Pythonic code style

## 📈 Typical Issues Found

**Most Common Critical Issues:**
1. SQL injection vulnerabilities in raw queries
2. N+1 query problems in views
3. Missing database indexes
4. DEBUG=True in production
5. Hardcoded secrets in code
6. Missing CSRF protection
7. No HTTPS configuration
8. Missing permission checks

**Most Common Performance Issues:**
1. N+1 queries (70% of Django performance issues)
2. Missing select_related/prefetch_related
3. No caching implementation
4. Missing database indexes
5. Synchronous views for I/O operations
6. No connection pooling
7. Inefficient querysets

**Most Common API Issues:**
1. Exposing sensitive fields in serializers
2. No rate limiting
3. Weak permission checks
4. No API versioning
5. Missing pagination
6. Poor error handling

## 🎯 Success Criteria

After applying recommendations, your Django application should have:

- ✅ Zero critical security vulnerabilities
- ✅ Optimized database queries (no N+1 issues)
- ✅ Proper caching at multiple levels
- ✅ Production-ready settings configuration
- ✅ Comprehensive error handling and logging
- ✅ Strong authentication and authorization
- ✅ API best practices (if using DRF)
- ✅ High test coverage with quality tests
- ✅ Scalable architecture patterns

## 📞 When to Use

- Before deploying to production
- During code review process
- When experiencing performance issues
- For security audits
- When scaling the application
- Learning Django best practices
- Refactoring legacy code

---

**Production-ready Django applications through comprehensive expert review.**
