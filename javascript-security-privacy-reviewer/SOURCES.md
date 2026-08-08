# Sources and References

## Methodology

This JavaScript Security & Privacy Reviewer skill was created through extensive research of authoritative security resources, focusing on **practical vulnerability prevention** and **privacy compliance**. The skill provides concrete secure code examples based on OWASP Top 10, CWE Top 25, GDPR, and platform-specific security best practices.

**Philosophy:** Teach developers HOW to write secure JavaScript/TypeScript code by showing real vulnerabilities and their fixes, mapped to industry standards.

**Created:** November 2025

---

## Primary Sources

### 1. OWASP Top 10 2021

- **Official URL:** https://owasp.org/Top10/
- **Used for:** Web application security risks and mitigation strategies
- **License:** CC-BY-SA 4.0
- **Key Topics:**
  - A01:2021 - Broken Access Control
  - A02:2021 - Cryptographic Failures
  - A03:2021 - Injection
  - A04:2021 - Insecure Design
  - A05:2021 - Security Misconfiguration
  - A06:2021 - Vulnerable and Outdated Components
  - A07:2021 - Identification and Authentication Failures
  - A08:2021 - Software and Data Integrity Failures
  - A09:2021 - Security Logging and Monitoring Failures
  - A10:2021 - Server-Side Request Forgery (SSRF)

**Relevant Guidelines:**
- All injection guidelines (SQL-INJECT, XSS-*, CMD-INJECT)
- Authentication guidelines (PASSWORD-HASH, JWT-*, SESSION-SECURE)
- Cryptography guidelines (CRYPTO-STRONG, KEY-MANAGE)
- Access control (CORS-CONFIG, CSRF-TOKEN)
- Dependency security (NPM-AUDIT, VULN-DEPS)

**Key Resources:**
- OWASP Top 10 2021 - https://owasp.org/Top10/
- Previous versions for historical context

---

### 2. OWASP Cheat Sheet Series

- **Official URL:** https://cheatsheetseries.owasp.org/
- **License:** CC-BY-SA 4.0
- **Used for:** Specific vulnerability prevention techniques

**Key Cheat Sheets:**

1. **XSS Prevention**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
   - Relevant to: XSS-ESCAPE, XSS-REFLECT, XSS-STORED, XSS-DOM

2. **SQL Injection Prevention**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
   - Relevant to: SQL-INJECT

3. **Authentication**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
   - Relevant to: PASSWORD-HASH, PASSWORD-POLICY, MFA-IMPLEMENT

4. **Session Management**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
   - Relevant to: SESSION-SECURE, JWT-EXPIRE

5. **CSRF Prevention**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
   - Relevant to: CSRF-TOKEN, SAMESITE-COOKIE

6. **Cryptographic Storage**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
   - Relevant to: PII-ENCRYPT, ENCRYPT-REST, CRYPTO-STRONG

7. **Logging**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
   - Relevant to: PII-LOG, AUDIT-LOG, ERROR-LOG

8. **Input Validation**
   - URL: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
   - Relevant to: API-VALIDATE, all injection guidelines

---

### 3. CWE Top 25 Most Dangerous Software Weaknesses

- **Official URL:** https://cwe.mitre.org/top25/
- **Maintainer:** MITRE Corporation
- **Used for:** Common weakness enumeration and vulnerability classification

**Key CWEs Covered:**
- CWE-79: Cross-site Scripting (XSS)
- CWE-89: SQL Injection
- CWE-78: OS Command Injection
- CWE-22: Path Traversal
- CWE-352: Cross-Site Request Forgery (CSRF)
- CWE-94: Code Injection
- CWE-502: Deserialization of Untrusted Data
- CWE-327: Use of a Broken or Risky Cryptographic Algorithm
- CWE-798: Use of Hard-coded Credentials
- CWE-209: Information Exposure Through Error Message
- CWE-532: Information Exposure Through Log Files
- CWE-338: Use of Cryptographically Weak PRNG
- CWE-295: Improper Certificate Validation
- CWE-1321: Prototype Pollution

**Relevant Guidelines:**
- All major vulnerability categories mapped to CWEs

---

### 4. Node.js Security Best Practices

- **Official URL:** https://nodejs.org/en/docs/guides/security/
- **Maintainer:** Node.js Foundation
- **License:** Open source documentation
- **Used for:** Node.js-specific security guidance

**Key Topics:**
- Avoiding eval() and code injection
- child_process security
- HTTPS and TLS configuration
- Dependency security with npm audit
- Environment variable management
- Error handling

**Relevant Guidelines:**
- NODE-EVAL - Avoiding eval()
- NODE-CHILD-PROCESS - Secure process execution (CMD-INJECT)
- CRED-STORE - Environment variables
- CERT-VALIDATE - TLS configuration
- NPM-AUDIT - Dependency security

**Key Resources:**
- Security Best Practices - https://nodejs.org/en/docs/guides/security/
- npm Security - https://docs.npmjs.com/audit

---

### 5. GDPR (General Data Protection Regulation)

- **Official URL:** https://gdpr.eu/
- **Used for:** Privacy and data protection requirements
- **Jurisdiction:** European Union
- **Effective:** May 25, 2018

**Key Articles:**
- **Article 4** - Definitions (personal data, processing, consent)
- **Article 5** - Principles (lawfulness, data minimization, accuracy, storage limitation)
- **Article 7** - Conditions for consent
- **Article 15** - Right of access
- **Article 16** - Right to rectification
- **Article 17** - Right to erasure ("right to be forgotten")
- **Article 20** - Right to data portability
- **Article 25** - Data protection by design and by default
- **Article 30** - Records of processing activities
- **Article 32** - Security of processing
- **Article 33** - Breach notification

**Relevant Guidelines:**
- PII-IDENTIFY - Personal data classification
- PII-MINIMIZE - Data minimization (Art. 5)
- PII-ENCRYPT - Security of processing (Art. 32)
- CONSENT-MANAGE - Conditions for consent (Art. 7)
- DATA-ERASURE - Right to erasure (Art. 17)
- DATA-EXPORT - Right to data portability (Art. 20)
- GDPR-COMPLY - Overall compliance
- AUDIT-LOG - Records of processing (Art. 30)

**Key Resources:**
- Official GDPR Text - https://gdpr.eu/tag/gdpr/
- ICO Guidance - https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/

---

### 6. CCPA (California Consumer Privacy Act)

- **Official URL:** https://oag.ca.gov/privacy/ccpa
- **Used for:** California privacy rights
- **Effective:** January 1, 2020

**Key Rights:**
- Right to know what personal information is collected
- Right to deletion
- Right to opt-out of sale
- Right to non-discrimination

**Relevant Guidelines:**
- PII-IDENTIFY - Know what data is collected
- DATA-ERASURE - Right to deletion
- DATA-EXPORT - Right to know
- CONSENT-MANAGE - Opt-out mechanisms

---

### 7. NIST (National Institute of Standards and Technology)

- **Official URL:** https://www.nist.gov/
- **Used for:** Cryptographic standards and password guidance

**Key Publications:**

1. **NIST SP 800-63B** - Digital Identity Guidelines (Authentication)
   - Password requirements
   - Multi-factor authentication
   - Session management
   - Relevant to: PASSWORD-POLICY, PASSWORD-HASH, MFA-IMPLEMENT

2. **NIST SP 800-57** - Key Management
   - Key generation and storage
   - Key rotation
   - Relevant to: KEY-MANAGE

3. **NIST SP 800-111** - Storage Encryption
   - Encryption at rest
   - Relevant to: ENCRYPT-REST, PII-ENCRYPT

4. **FIPS 140-2** - Cryptographic Module Validation
   - Approved algorithms
   - Relevant to: CRYPTO-STRONG, CRYPTO-DEPRECATE

---

### 8. React Security Documentation

- **Official URL:** https://react.dev/
- **Maintainer:** Meta (Facebook)
- **License:** MIT
- **Used for:** React-specific security guidance

**Key Topics:**
- dangerouslySetInnerHTML risks
- XSS in React
- Secure data fetching
- Client-side routing security

**Relevant Guidelines:**
- REACT-DANGEROUS - dangerouslySetInnerHTML
- XSS-DOM - DOM-based XSS in React
- DANGEROUS-HTML - General React security

**Key Resources:**
- React Documentation - https://react.dev/learn
- Security FAQ - React community resources

---

### 9. Express.js Security Best Practices

- **Official URL:** https://expressjs.com/en/advanced/best-practice-security.html
- **License:** MIT
- **Used for:** Express.js security configuration

**Key Topics:**
- Helmet middleware
- HTTPS configuration
- Session security
- Body parsing limits
- CORS configuration

**Relevant Guidelines:**
- EXPRESS-BODY - Body parser configuration
- SESSION-SECURE - Express session
- CORS-CONFIG - CORS middleware
- HSTS-HEADER, CSP-HEADER - Helmet usage

---

### 10. JWT (JSON Web Tokens) Security

- **Specification:** RFC 7519
- **Official URL:** https://jwt.io/
- **Used for:** Token-based authentication security

**Key Topics:**
- Algorithm confusion attacks
- Token expiration
- Secret management
- Signature verification

**Relevant Guidelines:**
- JWT-SECRET - Secure implementation
- JWT-EXPIRE - Expiration and refresh

**Key Resources:**
- RFC 7519 - https://tools.ietf.org/html/rfc7519
- JWT.io Introduction - https://jwt.io/introduction

---

### 11. OAuth 2.0 and OpenID Connect

- **OAuth 2.0 RFC:** RFC 6749
- **OIDC Specification:** https://openid.net/connect/
- **Used for:** OAuth/OIDC security

**Key Topics:**
- State parameter (CSRF protection)
- PKCE (Proof Key for Code Exchange)
- Token validation
- ID token verification

**Relevant Guidelines:**
- OAUTH-VALIDATE - OAuth/OIDC validation

---

### 12. npm Security

- **Official URL:** https://docs.npmjs.com/audit
- **Used for:** Dependency security

**Key Topics:**
- npm audit
- Security advisories
- Dependency pinning
- Supply chain attacks

**Relevant Guidelines:**
- NPM-AUDIT - Running audits
- VULN-DEPS - Monitoring vulnerabilities
- DEP-PIN - Version pinning
- SUPPLY-CHAIN - Supply chain security

---

### 13. DOMPurify

- **Repository:** https://github.com/cure53/DOMPurify
- **Maintainer:** Cure53
- **License:** Apache 2.0 / MPL 2.0
- **Used for:** HTML sanitization

**Relevant Guidelines:**
- SANITIZE-LIB - Using DOMPurify
- XSS-MUTATION - mXSS prevention

---

### 14. bcrypt and argon2

- **bcrypt:** https://github.com/kelektiv/node.bcrypt.js
- **argon2:** https://github.com/ranisalt/node-argon2
- **Used for:** Password hashing

**Relevant Guidelines:**
- PASSWORD-HASH - Secure hashing
- SALT-HASH - Salting

---

## Research Process

### Web Searches Performed
1. **"OWASP Top 10 2021"** - Latest web security risks
2. **"Node.js security best practices 2025"** - Platform-specific security
3. **"JavaScript XSS prevention"** - XSS mitigation techniques
4. **"GDPR technical requirements"** - Privacy compliance
5. **"JWT security best practices"** - Token security
6. **"React security dangerouslySetInnerHTML"** - Framework security
7. **"MongoDB NoSQL injection prevention"** - Database security
8. **"npm audit supply chain security"** - Dependency security
9. **"Prototype pollution JavaScript"** - Platform vulnerabilities
10. **"Express.js security headers helmet"** - Web framework security

### Methodology
1. **Identify authoritative sources** - OWASP, CWE, NIST, GDPR official documentation
2. **Map to JavaScript/TypeScript** - Adapt generic security principles to JS ecosystem
3. **Gather concrete examples** - Real vulnerable code and secure fixes
4. **Validate against standards** - Ensure compliance with OWASP, CWE, GDPR
5. **Include platform specifics** - Node.js, React, Express, MongoDB

---

## Guideline Structure

Each guideline follows this format:

### Severity Classification
- **Critical:** Immediate fix required (RCE, data breach)
- **High:** Should fix soon (XSS, injection, auth bypass)
- **Medium:** Recommended (security hardening)

### Code Examples
- **Vulnerable code:** Shows the security issue
- **Secure implementation:** Shows the fix
- Includes explanations and context

### Security Impact
Explains:
- How the vulnerability is exploited
- Potential consequences
- Real-world attack scenarios

### Compliance Mapping
References to:
- OWASP Top 10 categories
- CWE numbers
- GDPR articles (for privacy)
- PCI-DSS requirements (where applicable)

### Attribution
Source of the guideline or pattern

---

## Mnemonic ID Convention

All guidelines use category-based prefixes:
- **Injection** - SQL-INJECT, NOSQL-INJECT, CMD-INJECT, XSS-*, etc.
- **Authentication** - PASSWORD-*, JWT-*, SESSION-*, OAUTH-*, MFA-*
- **Security Headers** - CSRF-*, HSTS-*, CSP-*, CORS-*
- **API Security** - API-*, RATE-LIMIT
- **Privacy** - PII-*, CONSENT-*, DATA-*, GDPR-*
- **Cryptography** - CRYPTO-*, KEY-*, RANDOM-*, SALT-*, CERT-*, ENCRYPT-*
- **Error Handling** - ERROR-*, STACK-*, TRY-CATCH
- **Dependencies** - NPM-*, VULN-*, DEP-*, SUPPLY-CHAIN
- **Platform** - NODE-*, REACT-*, EXPRESS-*, PROTOTYPE-*, DESERIALIZATION

Format: `CATEGORY-KEYWORD`
Examples: `XSS-ESCAPE`, `JWT-SECRET`, `PII-ENCRYPT`

---

## Code Example Attribution

All code examples were:
1. **Inspired by** OWASP, CWE, and security research
2. **Adapted for JavaScript/TypeScript** - Modern ES6+, Node.js, React patterns
3. **Created as original demonstrations** - Showing specific vulnerabilities and fixes
4. **Validated against standards** - OWASP cheat sheets, CWE descriptions

### Example Pattern:
- **Vulnerable Code:** Common anti-pattern or real vulnerability
- **Secure Code:** Best practice following OWASP/CWE guidance
- **Explanation:** Why it's vulnerable and how the fix works

---

## Compliance Standards Summary

This skill covers:

1. **OWASP Top 10 2021** - All 10 categories
2. **CWE Top 25** - Most dangerous weaknesses
3. **GDPR** - Data protection and privacy (Articles 5, 7, 15-17, 20, 25, 30, 32-33)
4. **CCPA** - California privacy rights
5. **NIST SP 800-63B** - Password and authentication
6. **NIST SP 800-57** - Key management
7. **PCI-DSS** - Payment card security (where applicable)
8. **SOC 2** - Security logging and audit

---

## Verification

All guidelines were verified against:
1. ✅ OWASP Top 10 2021
2. ✅ OWASP Cheat Sheet Series
3. ✅ CWE Top 25
4. ✅ Node.js Security Best Practices
5. ✅ GDPR Official Text
6. ✅ React Security Documentation
7. ✅ Express.js Security Guide
8. ✅ JWT Security Best Practices
9. ✅ npm Security Documentation
10. ✅ NIST Guidelines

---

## Updates and Maintenance

- **Version:** 1.0
- **Created:** November 2025
- **Last Updated:** November 2025
- **JavaScript Compatibility:** ES6+, Node.js 14+
- **Framework Coverage:** React, Vue, Angular, Express, Fastify, NestJS

**Future Updates May Include:**
- Deno and Bun security patterns
- GraphQL security
- WebSocket security
- Serverless (AWS Lambda, Azure Functions) security
- Container security (Docker, Kubernetes)

---

## Acknowledgments

Special thanks to:
- **OWASP Foundation** - Web application security standards
- **MITRE Corporation** - CWE database
- **Node.js Foundation** - Platform security documentation
- **European Commission** - GDPR regulation
- **NIST** - Cryptographic standards
- **React Team** (Meta) - Framework security guidance
- **Express.js Maintainers** - Web framework security
- **DOMPurify Team** (Cure53) - XSS prevention
- **npm Team** - Dependency security tools
- **Security Researchers** - Vulnerability discoveries and mitigations
- **JavaScript Community** - Security best practices

---

## Real-World Vulnerabilities Referenced

While creating examples, referenced patterns from:
- OWASP WebGoat vulnerabilities
- Real CVEs (anonymized and simplified)
- Security research papers
- Bug bounty disclosures
- Common security audit findings

All examples were:
1. Simplified for clarity
2. Made self-contained
3. Focused on teaching the principle
4. Not direct copies of real exploits

---

## Legal and Attribution

### Official Standards
- **OWASP, CWE, NIST:** Public domain or CC-BY-SA
- **GDPR:** EU regulation, publicly available
- **RFCs:** IETF public standards

### Documentation
- **Node.js, React, Express, npm:** Open source licenses (MIT, Apache)
- **Usage:** Freely referenceable for educational purposes

### Code Examples
- **Original examples:** Created for this skill
- **Inspired by:** OWASP cheat sheets, CWE examples, security research
- **Skill license:** MIT

---

## Security Principles Summary

This skill emphasizes:

1. **Defense in Depth** - Multiple layers of security
2. **Secure by Default** - Safe defaults, opt-in for risky features
3. **Fail Securely** - Deny by default, secure error handling
4. **Least Privilege** - Minimal permissions
5. **Input Validation** - Validate all untrusted input
6. **Output Encoding** - Context-aware escaping
7. **Cryptographic Agility** - Use strong, modern algorithms
8. **Privacy by Design** - GDPR principles built-in
9. **Audit and Logging** - Security event tracking
10. **Patch Management** - Keep dependencies updated

All based on OWASP, CWE, NIST, and GDPR standards.

---

**Note:** This skill prioritizes practical security guidance based on real vulnerabilities and industry standards. The goal is to help developers write secure JavaScript/TypeScript code and comply with privacy regulations.

---

**Created:** November 2025
**Last Updated:** November 2025
**Skill Version:** 1.0
**Focus:** OWASP Top 10, GDPR/CCPA compliance, JavaScript/Node.js security
