# Sources and Attribution

This Django Production Readiness Reviewer skill is based on authoritative sources from the Django community, security organizations, and production best practices.

## Primary Sources

### Django Official Documentation
**Django Software Foundation**
- URL: https://docs.djangoproject.com/
- License: BSD License
- Coverage: Core Django patterns, security, performance, deployment

**Key Documentation Sections:**
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/
- Database Optimization: https://docs.djangoproject.com/en/stable/topics/db/optimization/
- Performance and Optimization: https://docs.djangoproject.com/en/stable/topics/performance/
- Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Class-Based Views: https://docs.djangoproject.com/en/stable/topics/class-based-views/
- Model Best Practices: https://docs.djangoproject.com/en/stable/topics/db/models/

### Two Scoops of Django
**Daniel Roy Greenfeld and Audrey Roy Greenfeld**
- Publisher: Two Scoops Press
- Coverage: Django best practices, patterns, and conventions
- Topics: Models, views, forms, REST APIs, security, testing, deployment

**Key Concepts Applied:**
- Fat models vs service layers
- Settings organization (environment-specific settings)
- Model design patterns
- Form patterns
- CBV usage patterns
- URL naming conventions
- Security best practices

### Django REST Framework Documentation
**Tom Christie and contributors**
- URL: https://www.django-rest-framework.org/
- License: BSD License
- Coverage: API design, serializers, permissions, authentication, throttling

**Key Sections:**
- Serializers: https://www.django-rest-framework.org/api-guide/serializers/
- Permissions: https://www.django-rest-framework.org/api-guide/permissions/
- Authentication: https://www.django-rest-framework.org/api-guide/authentication/
- Throttling: https://www.django-rest-framework.org/api-guide/throttling/
- Versioning: https://www.django-rest-framework.org/api-guide/versioning/

## Security Standards

### OWASP (Open Web Application Security Project)
**OWASP Foundation**
- URL: https://owasp.org/
- Coverage: Web application security standards and best practices

**OWASP Top 10 (2021):**
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery (SSRF)

**OWASP Django Security Cheat Sheet:**
- URL: https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html
- Specific Django security patterns and configurations

### Common Weakness Enumeration (CWE)
**MITRE Corporation**
- URL: https://cwe.mitre.org/
- Coverage: Software weakness classification

**Key CWEs for Django:**
- CWE-89: SQL Injection
- CWE-79: Cross-site Scripting (XSS)
- CWE-352: Cross-Site Request Forgery (CSRF)
- CWE-798: Use of Hard-coded Credentials
- CWE-311: Missing Encryption of Sensitive Data

## Performance and Scalability

### Django Database Optimization
**Django Documentation**
- select_related() and prefetch_related() patterns
- Database indexing strategies
- Query optimization techniques
- Connection pooling

### High Performance Django
**Various contributors and community practices**
- Caching strategies (Redis, Memcached)
- Database query optimization
- Async views and background tasks (Celery)
- CDN usage for static files
- Database replication and read/write splitting

## Testing Best Practices

### pytest-django Documentation
**pytest-dev community**
- URL: https://pytest-django.readthedocs.io/
- Coverage: Testing Django applications with pytest
- Factory patterns for test data

### Model Bakery (formerly Model Mommy)
**Model Bakery contributors**
- URL: https://model-bakery.readthedocs.io/
- Coverage: Smart fixtures for better tests
- Factory patterns

### Django Testing Documentation
**Django Software Foundation**
- URL: https://docs.djangoproject.com/en/stable/topics/testing/
- Coverage: Testing tools, test cases, fixtures, assertions

## Deployment and Production

### Django Deployment Checklist
**Django Software Foundation**
- URL: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Critical settings for production
- Security configuration
- Performance optimization

### Twelve-Factor App
**Heroku**
- URL: https://12factor.net/
- Coverage: Methodology for building SaaS applications
- Environment configuration
- Backing services
- Build, release, run

**Applied Principles:**
- I. Codebase: One codebase in version control
- II. Dependencies: Explicitly declare dependencies
- III. Config: Store config in environment
- IV. Backing services: Treat backing services as attached resources
- V. Build, release, run: Strictly separate build and run stages
- VI. Processes: Execute the app as stateless processes
- X. Dev/prod parity: Keep development and production similar
- XI. Logs: Treat logs as event streams

## Infrastructure and Tools

### WhiteNoise
**David Evans and contributors**
- URL: http://whitenoise.evans.io/
- Coverage: Serving static files in production
- Simplified static file handling

### Sentry
**Sentry**
- URL: https://docs.sentry.io/platforms/python/guides/django/
- Coverage: Error tracking and monitoring
- Performance monitoring

### Celery
**Ask Solem and contributors**
- URL: https://docs.celeryproject.org/
- Coverage: Distributed task queue
- Async task processing
- Periodic tasks

### Django Debug Toolbar
**Rob Hudson and contributors**
- URL: https://django-debug-toolbar.readthedocs.io/
- Coverage: Performance profiling and debugging
- Query analysis and N+1 detection

## Database

### PostgreSQL Documentation
**PostgreSQL Global Development Group**
- URL: https://www.postgresql.org/docs/
- Coverage: Database configuration, indexes, performance tuning

### pgBouncer
**pgBouncer contributors**
- URL: https://www.pgbouncer.org/
- Coverage: Connection pooling for PostgreSQL
- Scalability patterns

## Books and Publications

### Two Scoops of Django 3.x
**Daniel Roy Greenfeld and Audrey Roy Greenfeld**
- Best practices for Django development
- Coding standards and patterns
- Security recommendations
- Testing strategies

### High Performance Django
**Peter Baumgartner and Yann Malet**
- Performance optimization techniques
- Caching strategies
- Database optimization
- Profiling and monitoring

### Django Design Patterns and Best Practices
**Arun Ravindran**
- Design patterns for Django
- Architectural patterns
- Common pitfalls and solutions

## Community Resources

### Django Project Best Practices
- Django community conventions
- Package recommendations
- Deployment patterns
- Monitoring and logging strategies

### Real World Django Projects
**Production Django applications and their patterns:**
- Instagram engineering blog
- Pinterest engineering blog
- Mozilla Django patterns
- Django Stars blog

## Standards and Specifications

### PEP 8 - Style Guide for Python Code
**Python Software Foundation**
- URL: https://www.python.org/dev/peps/pep-0008/
- Python coding conventions

### HTTP Specification
**IETF**
- RFC 7231: HTTP/1.1 Semantics and Content
- RFC 6265: HTTP State Management Mechanism (Cookies)
- RFC 7540: HTTP/2

### REST API Design
**Roy Fielding's Dissertation**
- Architectural Styles and the Design of Network-based Software Architectures
- RESTful principles

## Package Documentation

### django-environ
- Environment variable management
- Settings configuration

### django-cors-headers
- CORS header management
- Cross-origin resource sharing

### django-filter
- Generic filtering for Django REST Framework

### dj-database-url
- Database URL configuration
- 12-factor compliance

### django-storages
- Custom storage backends
- S3/CloudFront integration

## Attribution

This skill synthesizes knowledge from:

- **Django Official Documentation** - Core patterns and best practices
- **Django Software Foundation** - Security guidelines and deployment checklists
- **OWASP** - Security standards and vulnerability classifications
- **Two Scoops of Django** - Community best practices and patterns
- **Django REST Framework** - API design patterns
- **Production Django deployments** - Real-world patterns and solutions
- **Django community** - Collective wisdom and conventions

## License and Usage

This skill is provided for use with Claude Code. All references to external documentation, tools, and resources remain under their respective licenses:

- Django Documentation: BSD License
- Django REST Framework: BSD License
- OWASP Resources: Creative Commons Attribution-ShareAlike 4.0
- Python documentation: Python Software Foundation License

## Disclaimer

This skill provides guidance based on established best practices and documentation. Always:

- Verify recommendations against current Django version documentation
- Test thoroughly in staging environments
- Consider specific application requirements
- Stay updated with security advisories
- Follow your organization's security policies

## Version Compatibility

Guidelines in this skill are primarily based on:
- Django 3.2 LTS and Django 4.x (current stable versions)
- Django REST Framework 3.x
- Python 3.8+

For older or newer versions, always consult official documentation for version-specific features and deprecations.

## Contributing to Django

To contribute to Django itself:
- Django Project: https://www.djangoproject.com/
- Contribution Guide: https://docs.djangoproject.com/en/dev/internals/contributing/
- Django GitHub: https://github.com/django/django

## Security Reporting

To report Django security issues:
- Security Policy: https://www.djangoproject.com/security/
- Email: security@djangoproject.com
- **Never** report security issues publicly

---

**Last Updated:** 2025
**Skill Version:** 1.0
**Maintained by:** Claude Code Skills Collection

This skill respects and acknowledges the extensive work of the Django community, Django Software Foundation, and all contributors to the ecosystem.
