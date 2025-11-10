# Sources and References

This document provides detailed attribution and sources for all guidelines in the Security & Privacy Reviewer skill.

## Methodology

This skill was created on **November 1, 2025** using a combination of:
1. **Web searches** for current best practices
2. **Public standards** (OWASP, CWE, GDPR)
3. **Claude's training knowledge** (pre-January 2025)
4. **Python security community practices**

All guidelines represent industry-standard security and privacy practices documented in publicly available resources.

---

## Primary Sources

### 1. OWASP (Open Web Application Security Project)

**OWASP Top 10 - 2021 Edition**
- Official URL: https://owasp.org/Top10/
- License: Creative Commons Attribution-ShareAlike 4.0 International
- Used for: Core web application security vulnerabilities
- Last updated: 2021 (2024 edition in development)

**Relevant Guidelines:**
- A01:2021 - Broken Access Control → `AUTHZ-CHECK`
- A02:2021 - Cryptographic Failures → `ENCRYPT-REST`, `ENCRYPT-TRANSIT`, `WEAK-HASH`
- A03:2021 - Injection → `SQL-INJECT`, `CMD-INJECT`, `CODE-INJECT`, `PATH-TRAVERSE`, `LDAP-INJECT`, `XML-INJECT`
- A04:2021 - Insecure Design → `PRIVACY-IMPACT`, `DATA-INVENTORY`
- A05:2021 - Security Misconfiguration → `DEBUG-OFF`, `VERSION-HIDE`, `HEADER-SECURE`
- A06:2021 - Vulnerable and Outdated Components → `DEPS-UPDATE`, `DEPS-AUDIT`
- A07:2021 - Identification and Authentication Failures → `HASH-PASSWORD`, `SESSION-SECURE`, `MFA-SUPPORT`
- A08:2021 - Software and Data Integrity Failures → `DEPS-PIN`, `CERT-VALIDATE`
- A09:2021 - Security Logging and Monitoring Failures → `AUDIT-TRAIL`, `LOG-SANITIZE`
- A10:2021 - Server-Side Request Forgery (SSRF) → General input validation

**Additional OWASP Resources:**
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP Developer Guide: https://owasp.org/www-project-developer-guide/

---

### 2. CWE (Common Weakness Enumeration)

**CWE Top 25 Most Dangerous Software Weaknesses**
- Official URL: https://cwe.mitre.org/top25/
- Maintained by: MITRE Corporation
- License: Public domain (U.S. Government work)
- Used for: Detailed vulnerability classification and mitigation

**Key CWE References:**
- CWE-20: Improper Input Validation → `VALIDATE-INPUT`, `TYPE-CHECK`
- CWE-22: Improper Limitation of a Pathname to a Restricted Directory (Path Traversal) → `PATH-TRAVERSE`
- CWE-78: OS Command Injection → `CMD-INJECT`
- CWE-79: Cross-site Scripting (XSS) → `XSS-PREVENT`, `SANITIZE-OUTPUT`
- CWE-89: SQL Injection → `SQL-INJECT`
- CWE-90: LDAP Injection → `LDAP-INJECT`
- CWE-94: Code Injection → `CODE-INJECT`
- CWE-117: Improper Output Neutralization for Logs → `LOG-SANITIZE`
- CWE-176: Improper Handling of Unicode Encoding → `ENCODING-CHECK`
- CWE-184: Incomplete List of Disallowed Inputs → `WHITELIST-INPUT`
- CWE-208: Observable Timing Discrepancy → `TIMING-ATTACK`
- CWE-209: Generation of Error Message Containing Sensitive Information → `NO-STACK-TRACE`
- CWE-295: Improper Certificate Validation → `CERT-VALIDATE`
- CWE-311: Missing Encryption of Sensitive Data → `ENCRYPT-REST`
- CWE-319: Cleartext Transmission of Sensitive Information → `ENCRYPT-TRANSIT`
- CWE-320: Key Management Errors → `KEY-MANAGE`
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm → `WEAK-HASH`, `USE-CRYPTO-LIB`, `AVOID-ECB`
- CWE-330: Use of Insufficiently Random Values → `RANDOM-SECURE`
- CWE-352: Cross-Site Request Forgery (CSRF) → `CSRF-PROTECT`
- CWE-502: Deserialization of Untrusted Data → `CODE-INJECT` (pickle warning)
- CWE-522: Insufficiently Protected Credentials → `ENV-SECRETS`
- CWE-611: Improper Restriction of XML External Entity Reference → `XML-INJECT`
- CWE-613: Insufficient Session Expiration → `TOKEN-EXPIRE`
- CWE-614: Sensitive Cookie in HTTPS Session Without 'Secure' Attribute → `COOKIE-SECURE`
- CWE-755: Improper Handling of Exceptional Conditions → `ERROR-SAFE`
- CWE-759: Use of a One-Way Hash without a Salt → `SALT-HASH`
- CWE-770: Allocation of Resources Without Limits or Throttling → `SIZE-LIMIT`
- CWE-798: Use of Hard-coded Credentials → `NO-HARDCODE`
- CWE-843: Access of Resource Using Incompatible Type (Type Confusion) → `TYPE-CHECK`
- CWE-862: Missing Authorization → `AUTHZ-CHECK`
- CWE-916: Use of Password Hash With Insufficient Computational Effort → `HASH-PASSWORD`
- CWE-942: Permissive Cross-domain Policy with Untrusted Domains → `CORS-RESTRICT`
- CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag → `COOKIE-SECURE`
- CWE-1021: Improper Restriction of Rendered UI Layers or Frames → `CLICK-JACK`

---

### 3. GDPR (General Data Protection Regulation)

**Official GDPR Text**
- Official URL: https://gdpr.eu/
- Legal basis: EU Regulation 2016/679
- Jurisdiction: European Union
- Effective: May 25, 2018

**Key Articles Referenced:**

**Principles (Article 5)**
- Article 5(1)(b) - Purpose Limitation → `PURPOSE-LIMIT`
- Article 5(1)(c) - Data Minimization → `PII-MINIMIZE`
- Article 5(1)(e) - Storage Limitation → `DATA-RETENTION`, `DATA-ANONYMIZE`

**Lawfulness, Consent (Article 7)**
- Article 7(1) - Conditions for Consent → `CONSENT-EXPLICIT`, `CONSENT-LOG`
- Article 7(2) - Granular Consent → `CONSENT-GRANULAR`

**Transparency (Articles 13-14)**
- Articles 13-14 - Information to Data Subjects → `PRIVACY-NOTICE`

**Data Subject Rights**
- Article 17 - Right to Erasure (Right to be Forgotten) → `DATA-DELETE`
- Article 20 - Right to Data Portability → `DATA-PORTABILITY`

**Security and Accountability**
- Article 30 - Records of Processing Activities → `DATA-INVENTORY`, `AUDIT-TRAIL`
- Article 32 - Security of Processing → `PII-ENCRYPT`, `PII-LOG`, `PII-ACCESS`, `PII-TRANSFER`, `DATA-BACKUP`
- Articles 33-34 - Breach Notification → `BREACH-DETECT`
- Article 35 - Data Protection Impact Assessment → `PRIVACY-IMPACT`

**Additional GDPR Resources:**
- ICO (UK Information Commissioner's Office): https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/
- EDPB (European Data Protection Board): https://edpb.europa.eu/

---

### 4. Python Security Best Practices

**OpenSSF Secure Coding Guide for Python**
- URL: https://best.openssf.org/Secure-Coding-Guide-for-Python/
- Organization: Open Source Security Foundation (Linux Foundation)
- License: CC-BY-4.0
- Used for: Python-specific security implementations

**Python Official Documentation**
- URL: https://docs.python.org/
- Security-relevant modules:
  - `secrets` module → `RANDOM-SECURE`
  - `hashlib` module → `WEAK-HASH`, `HASH-PASSWORD`
  - `hmac` module → `TIMING-ATTACK`
  - `ssl` module → `CERT-VALIDATE`
- License: Python Software Foundation License

**Python Cryptography Library**
- URL: https://cryptography.io/
- Used for: Modern cryptography examples (`Fernet`, `hazmat`)
- Examples: `USE-CRYPTO-LIB`, `ENCRYPT-REST`, `ENCRYPT-TRANSIT`

**defusedxml Library**
- URL: https://github.com/tiran/defusedxml
- Used for: XML security → `XML-INJECT`
- Purpose: Protection against XML bombs and XXE attacks

---

### 5. Web Search Results (November 1, 2025)

**Search 1: "OWASP Top 10 Python security best practices 2024"**

Found resources:
1. **"The Pythonista's Guide to the OWASP Top 10"** (devm.io)
   - Python-specific OWASP implementations

2. **"Python and OWASP Top 10: A Developer's Guide"** (Qwiet AI)
   - Injection prevention in Python
   - Authentication best practices

3. **"Secure Coding One Stop Shop for Python"** (OpenSSF)
   - Comprehensive Python security guide
   - References OWASP Developer Guide and CWE Top 25

4. **"API Security: Best Practices for Python Developers"** (Vidoc Security Lab)
   - API-specific security patterns

Key findings used:
- Werkzeug's `generate_password_hash` for password hashing
- ItsDangerous for secure tokens
- Principle of Least Privilege
- Environment variables for sensitive configuration

**Search 2: "Python privacy PII GDPR best practices data protection"**

Found resources:
1. **"Personal Data And PII: A Guide To Data Privacy Under GDPR"** (Protecto.ai)
   - PII classification
   - Data anonymization techniques

2. **"Data Privacy and Anonymization in Python Course"** (DataCamp)
   - Python privacy implementations

3. **"Best Practices for handling PII data"** (Andrew Weaver, Databricks)
   - Enterprise PII handling

4. **"PII Security Best Practices"** (Piiano)
   - Field-level encryption
   - PII masking techniques

5. **"How can Python be used to ensure data privacy and compliance with regulations like GDPR"** (Brecht Corbeel, Medium)
   - Python cryptography packages (PyCrypto, cryptography.io)
   - Django/Flask consent mechanisms
   - Anonymization techniques: data suppression, masking, synthetic data, generalization

Key findings used:
- Data minimization principle
- Encryption, pseudonymization, anonymization hierarchy
- Python's cryptography packages for GDPR compliance
- Consent logging with timestamp, IP, user agent
- GDPR penalties: up to 4% annual turnover or €20 million

---

### 6. Additional Privacy Standards

**CCPA (California Consumer Privacy Act)**
- URL: https://oag.ca.gov/privacy/ccpa
- Jurisdiction: California, USA
- Effective: January 1, 2020
- Used for: Privacy rights (similar to GDPR)
- Relevant Guidelines: Data deletion, portability, opt-out rights

**PCI DSS (Payment Card Industry Data Security Standard)**
- URL: https://www.pcisecuritystandards.org/
- Used for: Credit card data security
- Relevant Guidelines: `PII-MASK` (card number masking), `PII-ENCRYPT`, `ENCRYPT-TRANSIT`

**NIST Privacy Framework**
- URL: https://www.nist.gov/privacy-framework
- Organization: National Institute of Standards and Technology (USA)
- Used for: Data classification levels → `PII-CLASSIFY`

---

## Python Libraries Referenced

All Python libraries mentioned in code examples are real, actively maintained, and widely used:

### Security Libraries
- **bcrypt** - Password hashing (https://github.com/pyca/bcrypt/)
- **cryptography** - Modern cryptography (https://cryptography.io/)
- **secrets** - Cryptographically strong random (Python stdlib)
- **hashlib** - Hash algorithms (Python stdlib)
- **hmac** - Hash-based message authentication (Python stdlib)
- **pyotp** - TOTP/HOTP for 2FA (https://github.com/pyauth/pyotp)
- **defusedxml** - Safe XML parsing (https://github.com/tiran/defusedxml)

### Web Framework Security
- **Flask-WTF** - CSRF protection for Flask (https://flask-wtf.readthedocs.io/)
- **Flask-CORS** - CORS handling for Flask (https://flask-cors.readthedocs.io/)
- **Flask-Talisman** - Security headers for Flask (https://github.com/GoogleCloudPlatform/flask-talisman)
- **Django** - Built-in security features (https://www.djangoproject.com/)

### Security Auditing
- **safety** - Dependency vulnerability scanning (https://github.com/pyupio/safety)
- **pip-audit** - Audit Python packages (https://github.com/pypa/pip-audit)
- **bandit** - Security linting (https://github.com/PyCQA/bandit)

---

## Code Examples

### Example Attribution

All code examples in SKILL.md are:
1. **Original compositions** demonstrating security principles
2. **Common patterns** from public security documentation
3. **Adaptations** of examples from OWASP cheat sheets and Python documentation

**No code was copied verbatim** from copyrighted sources. All examples were written specifically for this skill to illustrate security and privacy principles.

### Example Patterns Sources
- **Parameterized queries**: Standard practice documented in OWASP SQL Injection Prevention Cheat Sheet
- **bcrypt usage**: Standard pattern from bcrypt library documentation
- **Fernet encryption**: Standard pattern from cryptography library documentation
- **Flask security headers**: Common patterns from Flask-Talisman and OWASP Secure Headers Project
- **GDPR consent logging**: Common implementation pattern from privacy engineering guides

---

## Claude's Training Knowledge

The following aspects come from Claude's training data (pre-January 2025):

### Security Knowledge
- Common vulnerability patterns and attack vectors
- Python security library APIs and best practices
- Secure coding principles (defense in depth, least privilege, etc.)
- Cryptography fundamentals (why ECB is bad, why salts matter, etc.)

### Privacy Knowledge
- GDPR requirements and technical implementations
- PII classification and handling best practices
- Privacy engineering principles (minimization, anonymization, etc.)
- Consent management patterns

### Python Expertise
- Python standard library security features
- Third-party security library usage
- Framework-specific security features (Django, Flask)
- Common Python anti-patterns and security pitfalls

---

## Synthesis and Original Contributions

While all guidelines are based on established standards, the following aspects are original to this skill:

1. **Mnemonic ID System**: The specific mnemonic identifiers (SQL-INJECT, PII-LOG, etc.) were created for this skill
2. **Organization**: The categorization into 12 sections is original
3. **Code Examples**: All code examples were written specifically for this skill
4. **Review Structure**: The Critical/Warning/Recommendation severity system
5. **Compliance Mapping**: The explicit mapping between guidelines and standards
6. **Attack Scenarios**: The specific attack explanations for each vulnerability

---

## Limitations and Disclaimers

### Not Legal Advice
This skill provides technical guidance based on security and privacy standards but does not constitute legal advice. Organizations should consult with legal counsel for compliance questions.

### Standards Evolution
Security and privacy standards evolve continuously:
- OWASP Top 10 is updated periodically (2021 edition current as of creation)
- GDPR remains stable but case law evolves
- New vulnerabilities and attack techniques emerge constantly

### Python Ecosystem Changes
Python libraries and best practices evolve. Always:
- Check library documentation for current best practices
- Audit dependencies regularly
- Follow security advisories for libraries you use

---

## Verification and Updates

### How to Verify Sources
All primary sources listed above are publicly accessible:
1. Visit the URLs provided
2. Review official documentation
3. Check version/date information
4. Verify recommendations match current standards

### Keeping This Skill Updated
To update this skill with new security/privacy guidelines:
1. Monitor OWASP Top 10 updates
2. Review CWE Top 25 annual updates
3. Follow Python security advisories
4. Track GDPR guidance updates
5. Review new vulnerability disclosures

---

## Community and Contributions

### Security Community Sources
- OWASP Community: https://owasp.org/
- Python Security Response Team: https://www.python.org/news/security/
- PyPI Security: https://pypi.org/security/
- Open Source Security Foundation: https://openssf.org/

### Reporting Issues
If you find errors or outdated information in this skill:
1. Check the source documentation links above
2. Verify against current standards
3. Submit an issue to the repository

---

## License and Copyright

### Primary Sources Copyright
- **OWASP**: CC-BY-SA 4.0 International
- **CWE**: Public domain (U.S. Government)
- **GDPR**: EU Law (public domain)
- **Python Documentation**: Python Software Foundation License
- **OpenSSF Guide**: CC-BY-4.0

### This Skill
This skill compilation is provided for educational purposes. It synthesizes publicly available security and privacy standards into a practical code review tool.

**Created**: November 1, 2025
**Last Updated**: November 1, 2025
**Maintainer**: Claude Skills Collection

---

## Acknowledgments

Special thanks to:
- **OWASP** for maintaining comprehensive security resources
- **MITRE** for the CWE database
- **EU** for establishing GDPR privacy standards
- **OpenSSF** for Python security guidance
- **Python Security Team** for maintaining a secure language ecosystem
- **Security researchers** worldwide who discover and document vulnerabilities

This skill exists to help developers write more secure and privacy-respecting Python code. All sources are credited, and all standards are publicly available for verification.

---

**Last Updated**: November 1, 2025
