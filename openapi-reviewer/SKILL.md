---
name: openapi-reviewer
description: Review OpenAPI/Swagger specifications for completeness, consistency, best practices, and API design quality. Use when user asks to review OpenAPI specs, Swagger files, API definitions, REST API design, or wants feedback on API documentation quality. Keywords - OpenAPI, Swagger, API spec, REST API, YAML, API design, endpoints, schemas.
allowed-tools: [Read, Grep, Glob]
---

## ⚠️ IMPORTANT: How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic sections
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**
```
Use the Task tool to run openapi-reviewer on api/openapi.yaml and write the report to reviews/api-review.md
```

---

# OpenAPI Specification Reviewer

You are an API specification reviewer who applies industry best practices from OpenAPI Specification, REST API design principles, and API documentation standards.

**📚 Sources:** All 50+ guidelines are based on OpenAPI Specification 3.x, REST API best practices, and industry standards. See SOURCES.md for detailed attribution and references.

## Your Mission

Review OpenAPI/Swagger specifications for quality, completeness, and best practices. Focus on:
- **Structure** - Proper OpenAPI format, valid schema, required fields
- **API Design** - REST principles, resource naming, HTTP methods
- **Documentation** - Clear descriptions, examples, comprehensive coverage
- **Data Models** - Schema definitions, validation, reusability
- **Security** - Authentication schemes, security requirements
- **Consistency** - Naming conventions, patterns, standards
- **Async Workflows** - Callbacks, webhooks, streaming, long-running operations

## Review Process

### 1. Initial Read
- Read the OpenAPI specification file
- Validate OpenAPI version and basic structure
- Identify API purpose and resources
- Note security schemes and authentication

### 2. Apply Guidelines

Use the 50+ guidelines embedded below in this skill document. All guidelines include mnemonic IDs (like API-VERSION, SCHEMA-REQUIRED) that you must reference in your review.

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., API-VERSION, PATH-NAMING) with each suggestion
✅ **Always provide concrete examples** - show both problematic and improved versions
✅ **Use proper markdown code blocks** with yaml syntax highlighting

**Required Review Structure:**

```markdown
## OpenAPI Specification Review: [API Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### 🔴 Critical Issues (Must Fix)

#### [MNEMONIC-ID]: [Brief issue description]

**Current specification:**
```yaml
[Show the problematic YAML exactly as it appears]
```

**Recommended specification:**
```yaml
[Show the improved YAML following best practices]
```

**Impact:**
[Explain why this matters and potential issues]

**Standards:**
[Note relevant standards: OpenAPI 3.x, REST principles, etc.]

---

### ⚠️ Warnings (Should Fix)

#### [MNEMONIC-ID]: [Issue description]
[Same structure as Critical Issues]

---

### 💡 Recommendations (Best Practices)

#### [MNEMONIC-ID]: [Suggestion]
[Same structure as above]

---

### 📋 API Quality Checklist
- [ ] OpenAPI 3.x compliant
- [ ] All required fields present
- [ ] Consistent naming conventions
- [ ] Complete security definitions
- [ ] Examples provided
- [ ] Error responses documented
```

**Key Requirements:**
- Start each issue with the **MNEMONIC ID in bold** (e.g., **API-VERSION**)
- Categorize by severity: Critical, Warning, Recommendation
- Show actual YAML blocks with ```yaml syntax
- Provide concrete "before and after" examples
- Explain the impact and reference standards

## Key Guidelines by Category

**Structure & Format (8 guidelines)**
- API-VERSION - OpenAPI version specification
- INFO-REQUIRED - Required info object fields
- SERVERS-DEFINED - Server URLs defined
- PATHS-REQUIRED - Paths object present
- COMPONENTS-REUSE - Reusable components
- TAGS-ORGANIZED - Tag organization
- EXTERNAL-DOCS - External documentation
- VALID-YAML - Valid YAML syntax
- CALLBACKS-SECTION - Callback/webhook section when async events exist

**Path & Operations (10 guidelines)**
- PATH-NAMING - RESTful path naming
- PATH-PARAMETERS - Parameter definitions
- OPERATION-ID - Unique operation IDs
- OPERATION-SUMMARY - Operation summaries
- OPERATION-DESC - Detailed descriptions
- HTTP-METHODS - Appropriate HTTP methods
- OPERATION-TAGS - Operation categorization
- DEPRECATED-FLAG - Deprecation markers
- RESPONSE-CODES - HTTP response codes
- REQUEST-BODY - Request body definitions
- CALLBACKS-DEFINED - Callback objects for async flows
- LINKS-DEFINED - Link relationships between operations

**Parameters (6 guidelines)**
- PARAM-REQUIRED - Required parameter markers
- PARAM-DESC - Parameter descriptions
- PARAM-EXAMPLES - Parameter examples
- PARAM-VALIDATION - Parameter validation rules
- QUERY-NAMING - Query parameter naming
- PATH-PARAM-REQUIRED - Path parameters required

**Schemas & Data Models (8 guidelines)**
- SCHEMA-REQUIRED - Schema definitions
- SCHEMA-TYPES - Proper type definitions
- SCHEMA-PROPERTIES - Property descriptions
- SCHEMA-VALIDATION - Validation constraints
- SCHEMA-EXAMPLES - Schema examples
- SCHEMA-REUSE - Component schema reuse
- ENUM-VALUES - Enumeration definitions
- DISCRIMINATOR - Polymorphism support

**Responses (6 guidelines)**
- RESPONSE-REQUIRED - Required responses
- RESPONSE-DESC - Response descriptions
- RESPONSE-SCHEMA - Response schemas
- ERROR-RESPONSES - Error response definitions
- SUCCESS-EXAMPLES - Success response examples
- ERROR-EXAMPLES - Error response examples

**Security (6 guidelines)**
- SECURITY-SCHEMES - Security scheme definitions
- SECURITY-REQUIRED - Security requirements
- API-KEY-HEADER - API key header naming
- OAUTH-SCOPES - OAuth scope definitions
- SECURITY-DESC - Security descriptions
- AUTH-ERRORS - Authentication error responses

**Documentation (6 guidelines)**
- DESC-COMPLETE - Complete descriptions
- DESC-CLEAR - Clear, concise descriptions
- EXAMPLES-PROVIDED - Examples for all types
- MARKDOWN-FORMAT - Markdown in descriptions
- CONTACT-INFO - Contact information
- LICENSE-INFO - License information

**API Lifecycle (4 guidelines)**
- VERSION-STRATEGY - Semantic versioning and stability labels
- SUNSET-POLICY - Deprecation/sunset headers documented
- CHANGELOG-LINK - Link to release notes/changelog
- EXTENSIONS-VENDOR - `x-*` vendor extensions documented

---

# Complete OpenAPI Guidelines

## 1. Structure & Format

### API-VERSION: OpenAPI Version Specification

**Issue:** Missing or incorrect OpenAPI version.

**Problematic:**
```yaml
# Missing openapi version
info:
  title: My API
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
```

**Why:**
- OpenAPI version is required
- Specifies parser behavior
- Use OpenAPI 3.0.x or 3.1.x
- OpenAPI Spec requirement

---

### INFO-REQUIRED: Required Info Object Fields

**Issue:** Missing required info fields.

**Problematic:**
```yaml
openapi: 3.0.3
info:
  title: My API
  # Missing version
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
  description: A comprehensive API for managing user resources
  contact:
    name: API Support
    email: support@example.com
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html
```

**Why:**
- Title and version are required
- Description helps users understand the API
- Contact and license improve documentation
- OpenAPI Spec requirement

---

### SERVERS-DEFINED: Server URLs Defined

**Issue:** Missing or incomplete server definitions.

**Problematic:**
```yaml
openapi: 3.0.3
info:
  title: My API
# No servers defined
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: http://localhost:8000/v1
    description: Development server
```

**Why:**
- Servers define where API is hosted
- Support multiple environments
- Include base paths in server URLs
- Best practice for API usability

---

### PATHS-REQUIRED: Paths Object Present

**Issue:** Missing paths object.

**Problematic:**
```yaml
openapi: 3.0.3
info:
  title: My API
# No paths defined
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Successful response
```

**Why:**
- Paths object is required
- Defines API endpoints
- Core of the API specification
- OpenAPI Spec requirement

---

### COMPONENTS-REUSE: Reusable Components

**Issue:** Duplicated schemas instead of reusable components.

**Problematic:**
```yaml
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  id: {type: integer}
                  name: {type: string}
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              # Duplicated schema!
              type: object
              properties:
                id: {type: integer}
                name: {type: string}
```

**Recommended:**
```yaml
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
      required:
        - id
        - name
```

**Why:**
- Reduces duplication
- Easier maintenance
- Consistent schemas across endpoints
- Best practice for large APIs

---

### TAGS-ORGANIZED: Tag Organization

**Issue:** Missing or inconsistent tags.

**Problematic:**
```yaml
paths:
  /users:
    get:
      summary: List users
      # No tags
  /products:
    get:
      summary: List products
      # No tags
```

**Recommended:**
```yaml
tags:
  - name: Users
    description: User management operations
  - name: Products
    description: Product catalog operations

paths:
  /users:
    get:
      summary: List users
      tags:
        - Users
  /products:
    get:
      summary: List products
      tags:
        - Products
```

**Why:**
- Organizes endpoints into logical groups
- Improves documentation readability
- Enables better code generation
- Best practice for API documentation

---

### EXTERNAL-DOCS: External Documentation

**Issue:** Missing external documentation links.

**Problematic:**
```yaml
openapi: 3.0.3
info:
  title: My API
# No external documentation
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
externalDocs:
  description: Find more info here
  url: https://docs.example.com/api

paths:
  /users:
    get:
      summary: List users
      externalDocs:
        description: User management guide
        url: https://docs.example.com/users
```

**Why:**
- Links to additional documentation
- Provides context and tutorials
- Improves developer experience
- Best practice for comprehensive docs

---

### VALID-YAML: Valid YAML Syntax

**Issue:** Invalid YAML syntax or structure.

**Problematic:**
```yaml
openapi: 3.0.3
info:
  title: My API
paths:
  /users:
  get:  # Invalid indentation
    summary: List users
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
```

**Why:**
- Valid YAML is essential
- Use YAML linters
- Consistent indentation (2 spaces)
- Prevents parser errors

---

## 2. Path & Operations

### PATH-NAMING: RESTful Path Naming

**Issue:** Non-RESTful path naming conventions.

**Problematic:**
```yaml
paths:
  /getUsers:  # Verb in path
    get:
      summary: Get users
  /user:  # Singular resource
    get:
      summary: List all users
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
  /users/{id}:
    get:
      summary: Get a specific user
      operationId: getUser
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
```

**Why:**
- Use nouns, not verbs in paths
- Use plural for collections
- HTTP method conveys the action
- REST API best practice

---

### PATH-PARAMETERS: Parameter Definitions

**Issue:** Missing or incomplete path parameter definitions.

**Problematic:**
```yaml
paths:
  /users/{id}:
    get:
      summary: Get user
      # Missing parameter definition
```

**Recommended:**
```yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          description: Unique identifier of the user
          schema:
            type: integer
            format: int64
            minimum: 1
      responses:
        '200':
          description: User found
        '404':
          description: User not found
```

**Why:**
- All path parameters must be defined
- Include type and validation
- Required is always true for path params
- OpenAPI Spec requirement

---

### OPERATION-ID: Unique Operation IDs

**Issue:** Missing or duplicate operation IDs.

**Problematic:**
```yaml
paths:
  /users:
    get:
      summary: List users
      # No operationId
    post:
      summary: Create user
      # No operationId
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      responses:
        '200':
          description: Success
    post:
      summary: Create user
      operationId: createUser
      responses:
        '201':
          description: Created
```

**Why:**
- Enables code generation
- Must be unique across all operations
- Use camelCase convention
- Best practice for tooling

---

### OPERATION-SUMMARY: Operation Summaries

**Issue:** Missing operation summaries.

**Problematic:**
```yaml
paths:
  /users:
    get:
      # No summary
      responses:
        '200':
          description: Success
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List all users
      description: |
        Retrieves a paginated list of all users in the system.
        Supports filtering, sorting, and pagination.
      responses:
        '200':
          description: Successful response with user list
```

**Why:**
- Summary provides quick overview
- Description gives detailed information
- Improves documentation readability
- OpenAPI best practice

---

### OPERATION-DESC: Detailed Descriptions

**Issue:** Missing detailed operation descriptions.

**Problematic:**
```yaml
paths:
  /users:
    post:
      summary: Create user
      # No detailed description
```

**Recommended:**
```yaml
paths:
  /users:
    post:
      summary: Create a new user
      description: |
        Creates a new user account with the provided information.

        **Note:** Email must be unique. If the email already exists,
        a 409 Conflict error will be returned.

        **Rate limit:** 10 requests per minute per IP address.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
```

**Why:**
- Provides implementation details
- Documents business rules
- Markdown formatting supported
- Improves developer experience

---

### HTTP-METHODS: Appropriate HTTP Methods

**Issue:** Incorrect HTTP method usage.

**Problematic:**
```yaml
paths:
  /users/delete/{id}:
    post:  # Should use DELETE
      summary: Delete user
  /users/update/{id}:
    get:  # Should use PUT/PATCH
      summary: Update user
```

**Recommended:**
```yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      operationId: getUser
    put:
      summary: Update user (full replacement)
      operationId: updateUser
    patch:
      summary: Partially update user
      operationId: patchUser
    delete:
      summary: Delete user
      operationId: deleteUser
```

**Why:**
- Use standard HTTP methods
- GET (read), POST (create), PUT (replace), PATCH (update), DELETE (delete)
- Avoid verbs in paths
- REST API best practice

---

### OPERATION-TAGS: Operation Categorization

**Issue:** Operations not tagged for organization.

**Problematic:**
```yaml
paths:
  /users:
    get:
      summary: List users
      # No tags
  /users/{id}:
    get:
      summary: Get user
      # No tags
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List users
      tags:
        - Users
      operationId: listUsers
  /users/{id}:
    get:
      summary: Get user
      tags:
        - Users
      operationId: getUser
```

**Why:**
- Groups related operations
- Improves documentation navigation
- Enables better code organization
- Best practice for large APIs

---

### DEPRECATED-FLAG: Deprecation Markers

**Issue:** No deprecation warnings for old endpoints.

**Problematic:**
```yaml
paths:
  /api/v1/users:
    get:
      summary: Old user endpoint (being replaced)
      # No deprecation flag
```

**Recommended:**
```yaml
paths:
  /api/v1/users:
    get:
      summary: List users (deprecated)
      deprecated: true
      description: |
        **DEPRECATED:** This endpoint is deprecated and will be removed in v2.0.
        Please use `/api/v2/users` instead.
      tags:
        - Users (Deprecated)
  /api/v2/users:
    get:
      summary: List users
      description: New and improved user listing endpoint
      tags:
        - Users
```

**Why:**
- Warns developers about deprecated endpoints
- Provides migration guidance
- Maintains backward compatibility
- API lifecycle management best practice

---

### RESPONSE-CODES: HTTP Response Codes

**Issue:** Missing or incomplete response codes.

**Problematic:**
```yaml
paths:
  /users/{id}:
    get:
      summary: Get user
      responses:
        '200':
          description: Success
        # Missing error responses
```

**Recommended:**
```yaml
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User found successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid user ID provided
        '401':
          description: Authentication required
        '404':
          description: User not found
        '500':
          description: Internal server error
```

**Why:**
- Document all possible responses
- Include success and error cases
- Helps client error handling
- Complete API contract

---

### REQUEST-BODY: Request Body Definitions

**Issue:** Missing request body schemas.

**Problematic:**
```yaml
paths:
  /users:
    post:
      summary: Create user
      # No request body defined
      responses:
        '201':
          description: Created
```

**Recommended:**
```yaml
paths:
  /users:
    post:
      summary: Create a new user
      requestBody:
        required: true
        description: User object to be created
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
            examples:
              example1:
                summary: Basic user creation
                value:
                  name: John Doe
                  email: john@example.com
      responses:
        '201':
          description: User created successfully
```

**Why:**
- Documents expected request format
- Enables validation
- Provides examples for developers
- OpenAPI best practice

---

## 3. Parameters

### PARAM-REQUIRED: Required Parameter Markers

**Issue:** Missing required flags on parameters.

**Problematic:**
```yaml
parameters:
  - name: userId
    in: path
    # Missing required field
    schema:
      type: integer
```

**Recommended:**
```yaml
parameters:
  - name: userId
    in: path
    required: true  # Always true for path parameters
    description: Unique identifier of the user
    schema:
      type: integer
      format: int64
  - name: includeDeleted
    in: query
    required: false  # Optional query parameter
    description: Include soft-deleted users in results
    schema:
      type: boolean
      default: false
```

**Why:**
- Required must be specified
- Path parameters are always required
- Query/header parameters default to optional
- Clear API contract

---

### PARAM-DESC: Parameter Descriptions

**Issue:** Missing parameter descriptions.

**Problematic:**
```yaml
parameters:
  - name: limit
    in: query
    schema:
      type: integer
    # No description
```

**Recommended:**
```yaml
parameters:
  - name: limit
    in: query
    required: false
    description: Maximum number of items to return (default 20, max 100)
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
  - name: offset
    in: query
    required: false
    description: Number of items to skip for pagination
    schema:
      type: integer
      minimum: 0
      default: 0
```

**Why:**
- Explains parameter purpose
- Documents constraints and defaults
- Improves developer experience
- Best practice for clarity

---

### PARAM-EXAMPLES: Parameter Examples

**Issue:** No examples provided for complex parameters.

**Problematic:**
```yaml
parameters:
  - name: filter
    in: query
    description: Filter expression
    schema:
      type: string
    # No examples
```

**Recommended:**
```yaml
parameters:
  - name: filter
    in: query
    description: |
      Filter expression using a simple query language.
      Supports: field operators (eq, ne, gt, lt) and logical operators (and, or).
    schema:
      type: string
    examples:
      simpleFilter:
        summary: Simple equality filter
        value: status eq 'active'
      complexFilter:
        summary: Complex filter with multiple conditions
        value: (age gt 18) and (status eq 'active')
```

**Why:**
- Examples clarify usage
- Reduces developer confusion
- Documents query language syntax
- Best practice for complex parameters

---

### PARAM-VALIDATION: Parameter Validation Rules

**Issue:** Missing validation constraints.

**Problematic:**
```yaml
parameters:
  - name: age
    in: query
    schema:
      type: integer
    # No validation
```

**Recommended:**
```yaml
parameters:
  - name: age
    in: query
    description: Filter users by minimum age
    schema:
      type: integer
      minimum: 0
      maximum: 150
      exclusiveMinimum: false
  - name: email
    in: query
    description: Filter by email address
    schema:
      type: string
      format: email
      maxLength: 255
  - name: status
    in: query
    description: Filter by user status
    schema:
      type: string
      enum: [active, inactive, pending, suspended]
```

**Why:**
- Defines acceptable values
- Enables automatic validation
- Prevents invalid requests
- Clear constraints documentation

---

### QUERY-NAMING: Query Parameter Naming

**Issue:** Inconsistent query parameter naming.

**Problematic:**
```yaml
parameters:
  - name: user_id  # snake_case
    in: query
  - name: maxResults  # camelCase
    in: query
  - name: sort-by  # kebab-case
    in: query
```

**Recommended:**
```yaml
# Choose one convention and stick to it (camelCase recommended for OpenAPI)
parameters:
  - name: userId
    in: query
    schema:
      type: integer
  - name: maxResults
    in: query
    schema:
      type: integer
  - name: sortBy
    in: query
    schema:
      type: string
      enum: [name, createdAt, updatedAt]
```

**Why:**
- Consistency improves readability
- camelCase is common for OpenAPI
- Matches JSON property naming
- Best practice for APIs

---

### PATH-PARAM-REQUIRED: Path Parameters Required

**Issue:** Path parameters not marked as required.

**Problematic:**
```yaml
paths:
  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: false  # WRONG!
        schema:
          type: integer
```

**Recommended:**
```yaml
paths:
  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true  # Must always be true
        description: Unique identifier of the user
        schema:
          type: integer
          format: int64
          minimum: 1
    get:
      summary: Get user by ID
```

**Why:**
- Path parameters are always required
- Cannot be optional by definition
- OpenAPI Spec requirement
- Prevents invalid specifications

---

## 4. Schemas & Data Models

### SCHEMA-REQUIRED: Schema Definitions

**Issue:** Responses without schema definitions.

**Problematic:**
```yaml
responses:
  '200':
    description: Success
    content:
      application/json:
        # No schema defined
```

**Recommended:**
```yaml
responses:
  '200':
    description: User retrieved successfully
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
        examples:
          example1:
            summary: Example user
            value:
              id: 123
              name: John Doe
              email: john@example.com
```

**Why:**
- Defines response structure
- Enables validation and code generation
- Documents data format
- OpenAPI best practice

---

### SCHEMA-TYPES: Proper Type Definitions

**Issue:** Missing or incorrect type definitions.

**Problematic:**
```yaml
components:
  schemas:
    User:
      properties:
        id:
          # No type specified
        age:
          type: number  # Too generic
```

**Recommended:**
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          format: int64
          description: Unique identifier
        age:
          type: integer
          format: int32
          minimum: 0
          maximum: 150
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
```

**Why:**
- Type is required for all properties
- Use specific formats (int32, int64, email, date-time)
- Enables proper validation
- OpenAPI Spec requirement

---

### SCHEMA-PROPERTIES: Property Descriptions

**Issue:** Schema properties without descriptions.

**Problematic:**
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        status:
          type: string
        # No descriptions
```

**Recommended:**
```yaml
components:
  schemas:
    User:
      type: object
      description: Represents a user account in the system
      properties:
        id:
          type: integer
          format: int64
          description: Unique identifier assigned to the user
          readOnly: true
        status:
          type: string
          enum: [active, inactive, pending, suspended]
          description: Current status of the user account
          default: pending
        createdAt:
          type: string
          format: date-time
          description: Timestamp when the user account was created
          readOnly: true
      required:
        - id
        - status
```

**Why:**
- Documents property purpose
- Clarifies business meaning
- Improves code generation
- Best practice for maintainability

---

### SCHEMA-VALIDATION: Validation Constraints

**Issue:** Missing validation rules on schema properties.

**Problematic:**
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        email:
          type: string
        age:
          type: integer
        # No validation constraints
```

**Recommended:**
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        email:
          type: string
          format: email
          minLength: 5
          maxLength: 255
          pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        age:
          type: integer
          minimum: 18
          maximum: 120
          exclusiveMinimum: false
        username:
          type: string
          minLength: 3
          maxLength: 30
          pattern: '^[a-zA-Z0-9_-]+$'
        website:
          type: string
          format: uri
          maxLength: 2048
      required:
        - email
        - username
```

**Why:**
- Enforces data quality
- Prevents invalid data
- Documents constraints
- Enables client-side validation

---

### SCHEMA-EXAMPLES: Schema Examples

**Issue:** No examples provided for schemas.

**Problematic:**
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
      # No example
```

**Recommended:**
```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        email:
          type: string
          format: email
        role:
          type: string
          enum: [admin, user, guest]
      required:
        - id
        - name
        - email
      example:
        id: 12345
        name: John Doe
        email: john.doe@example.com
        role: user
```

**Why:**
- Clarifies expected data format
- Helps developers understand usage
- Used in generated documentation
- Best practice for clarity

---

### SCHEMA-REUSE: Component Schema Reuse

**Issue:** Duplicate schema definitions.

**Problematic:**
```yaml
paths:
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                name: {type: string}
                email: {type: string}
  /users/{id}:
    put:
      requestBody:
        content:
          application/json:
            schema:
              # Duplicated!
              type: object
              properties:
                name: {type: string}
                email: {type: string}
```

**Recommended:**
```yaml
paths:
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
  /users/{id}:
    put:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'

components:
  schemas:
    UserBase:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
    UserCreate:
      allOf:
        - $ref: '#/components/schemas/UserBase'
        - type: object
          required:
            - name
            - email
    UserUpdate:
      allOf:
        - $ref: '#/components/schemas/UserBase'
```

**Why:**
- DRY principle
- Easier maintenance
- Consistent schemas
- Best practice for large APIs

---

### ENUM-VALUES: Enumeration Definitions

**Issue:** String fields without enumeration when values are limited.

**Problematic:**
```yaml
components:
  schemas:
    User:
      properties:
        status:
          type: string
          # No enum, any string allowed
```

**Recommended:**
```yaml
components:
  schemas:
    User:
      properties:
        status:
          type: string
          enum:
            - active
            - inactive
            - pending
            - suspended
          description: Current status of the user account
          default: pending
        role:
          type: string
          enum:
            - admin
            - moderator
            - user
            - guest
          description: User's role in the system
```

**Why:**
- Restricts values to valid set
- Self-documenting
- Enables validation
- Prevents typos and invalid data

---

### DISCRIMINATOR: Polymorphism Support

**Issue:** No discriminator for polymorphic schemas.

**Problematic:**
```yaml
components:
  schemas:
    Pet:
      oneOf:
        - $ref: '#/components/schemas/Dog'
        - $ref: '#/components/schemas/Cat'
      # No discriminator
```

**Recommended:**
```yaml
components:
  schemas:
    Pet:
      type: object
      required:
        - petType
      properties:
        petType:
          type: string
      discriminator:
        propertyName: petType
        mapping:
          dog: '#/components/schemas/Dog'
          cat: '#/components/schemas/Cat'

    Dog:
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          properties:
            bark:
              type: boolean

    Cat:
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          properties:
            meow:
              type: boolean
```

**Why:**
- Efficient polymorphism handling
- Better code generation
- Clear type identification
- OpenAPI 3.x feature

---

## 5. Responses

### RESPONSE-REQUIRED: Required Responses

**Issue:** No response definitions.

**Problematic:**
```yaml
paths:
  /users:
    get:
      summary: List users
      # No responses defined
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'
```

**Why:**
- At least one response is required
- Documents API contract
- OpenAPI Spec requirement
- Essential for understanding API

---

### RESPONSE-DESC: Response Descriptions

**Issue:** Missing response descriptions.

**Problematic:**
```yaml
responses:
  '200':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  # No description
```

**Recommended:**
```yaml
responses:
  '200':
    description: User retrieved successfully
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
  '404':
    description: User not found with the specified ID
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
```

**Why:**
- Description is required for all responses
- Clarifies response meaning
- OpenAPI Spec requirement
- Improves documentation

---

### RESPONSE-SCHEMA: Response Schemas

**Issue:** Response content without schema.

**Problematic:**
```yaml
responses:
  '200':
    description: Success
    content:
      application/json:
        # No schema
```

**Recommended:**
```yaml
responses:
  '200':
    description: List of users retrieved successfully
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/User'
            pagination:
              $ref: '#/components/schemas/Pagination'
```

**Why:**
- Defines response structure
- Enables validation
- Improves code generation
- Best practice for typed APIs

---

### ERROR-RESPONSES: Error Response Definitions

**Issue:** Missing error response definitions.

**Problematic:**
```yaml
paths:
  /users/{id}:
    get:
      responses:
        '200':
          description: Success
        # No error responses
```

**Recommended:**
```yaml
paths:
  /users/{id}:
    get:
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid user ID format
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          description: User not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  responses:
    Unauthorized:
      description: Authentication credentials missing or invalid
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  schemas:
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: string
      required:
        - code
        - message
```

**Why:**
- Documents all possible errors
- Helps client error handling
- Complete API contract
- Best practice for production APIs

---

### SUCCESS-EXAMPLES: Success Response Examples

**Issue:** No examples for success responses.

**Problematic:**
```yaml
responses:
  '200':
    description: Success
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
    # No examples
```

**Recommended:**
```yaml
responses:
  '200':
    description: User retrieved successfully
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/User'
        examples:
          normalUser:
            summary: Example of a regular user
            value:
              id: 123
              name: John Doe
              email: john@example.com
              role: user
              status: active
          adminUser:
            summary: Example of an admin user
            value:
              id: 456
              name: Jane Admin
              email: jane@example.com
              role: admin
              status: active
```

**Why:**
- Shows expected response format
- Multiple examples for different scenarios
- Improves developer understanding
- Best practice for documentation

---

### ERROR-EXAMPLES: Error Response Examples

**Issue:** No examples for error responses.

**Problematic:**
```yaml
responses:
  '400':
    description: Bad request
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
    # No examples
```

**Recommended:**
```yaml
responses:
  '400':
    description: Invalid request parameters
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Error'
        examples:
          invalidEmail:
            summary: Invalid email format
            value:
              code: INVALID_EMAIL
              message: The provided email address is not valid
              details:
                - "Email must contain @ symbol"
          missingField:
            summary: Required field missing
            value:
              code: VALIDATION_ERROR
              message: Request validation failed
              details:
                - "Field 'email' is required"
                - "Field 'name' is required"
```

**Why:**
- Shows error response format
- Documents error codes
- Helps with error handling
- Best practice for robust APIs

---

## 6. Security

### SECURITY-SCHEMES: Security Scheme Definitions

**Issue:** No security schemes defined.

**Problematic:**
```yaml
openapi: 3.0.3
info:
  title: My API
paths:
  /users:
    get:
      summary: List users
# No security schemes
```

**Recommended:**
```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for service accounts
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes:
            read:users: Read user information
            write:users: Modify user information

security:
  - BearerAuth: []
```

**Why:**
- Documents authentication methods
- Required for secured APIs
- Enables auth code generation
- OpenAPI security best practice

---

### SECURITY-REQUIRED: Security Requirements

**Issue:** Endpoints without security requirements.

**Problematic:**
```yaml
paths:
  /users/{id}:
    delete:
      summary: Delete user
      # No security requirement!
```

**Recommended:**
```yaml
# Global security (applies to all endpoints unless overridden)
security:
  - BearerAuth: []

paths:
  /public/status:
    get:
      summary: API health status
      security: []  # Public endpoint
      responses:
        '200':
          description: API is healthy

  /users/{id}:
    delete:
      summary: Delete user
      security:
        - BearerAuth: []
        - OAuth2: [write:users]
      responses:
        '204':
          description: User deleted
        '401':
          description: Unauthorized
        '403':
          description: Forbidden
```

**Why:**
- Defines auth requirements per endpoint
- Documents which endpoints are public
- Critical for API security
- Best practice for secure APIs

---

### API-KEY-HEADER: API Key Header Naming

**Issue:** Non-standard API key header names.

**Problematic:**
```yaml
components:
  securitySchemes:
    ApiKey:
      type: apiKey
      in: header
      name: api_key  # Non-standard
```

**Recommended:**
```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key  # Standard convention
      description: API key for authentication
```

**Why:**
- Use standard conventions (X-API-Key)
- Consistent with HTTP header naming
- Easier integration
- Best practice

---

### OAUTH-SCOPES: OAuth Scope Definitions

**Issue:** OAuth without scope definitions.

**Problematic:**
```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          scopes: {}  # No scopes defined
```

**Recommended:**
```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      description: OAuth 2.0 authorization
      flows:
        authorizationCode:
          authorizationUrl: https://example.com/oauth/authorize
          tokenUrl: https://example.com/oauth/token
          refreshUrl: https://example.com/oauth/refresh
          scopes:
            read:users: Read user information
            write:users: Create and update users
            delete:users: Delete users
            read:admin: Read admin data
            write:admin: Modify admin settings

paths:
  /users:
    get:
      security:
        - OAuth2: [read:users]
    post:
      security:
        - OAuth2: [write:users]
```

**Why:**
- Documents permission scopes
- Enables fine-grained access control
- OAuth 2.0 best practice
- Required for OAuth flows

---

### SECURITY-DESC: Security Descriptions

**Issue:** Security schemes without descriptions.

**Problematic:**
```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
    # No description
```

**Recommended:**
```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT bearer token authentication.

        To obtain a token, call POST /auth/login with valid credentials.
        Include the token in the Authorization header as: `Bearer <token>`

        Tokens expire after 1 hour. Use the refresh token to obtain a new access token.
```

**Why:**
- Explains how to authenticate
- Documents token format and lifecycle
- Improves developer experience
- Best practice for documentation

---

### AUTH-ERRORS: Authentication Error Responses

**Issue:** Missing authentication error responses.

**Problematic:**
```yaml
paths:
  /users:
    get:
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Success
        # Missing 401, 403
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List users
      security:
        - BearerAuth: []
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '401':
          description: Authentication credentials missing or invalid
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                code: UNAUTHORIZED
                message: Bearer token is missing or invalid
        '403':
          description: Authenticated but insufficient permissions
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                code: FORBIDDEN
                message: Insufficient permissions to access this resource
```

**Why:**
- Documents auth failure scenarios
- Helps client error handling
- Complete security contract
- Best practice for secured endpoints

---

## 7. Documentation

### DESC-COMPLETE: Complete Descriptions

**Issue:** Missing descriptions throughout the spec.

**Problematic:**
```yaml
paths:
  /users:
    get:
      # No description
      responses:
        '200':
          # No description
```

**Recommended:**
```yaml
paths:
  /users:
    get:
      summary: List all users
      description: |
        Retrieves a paginated list of all users in the system.

        Supports filtering by status, role, and email.
        Results are sorted by creation date (newest first) by default.

        **Permissions:** Requires `read:users` scope.
      operationId: listUsers
      responses:
        '200':
          description: |
            A successful response containing an array of user objects
            and pagination metadata
```

**Why:**
- Comprehensive documentation
- Explains behavior and constraints
- Improves developer experience
- Best practice for all fields

---

### DESC-CLEAR: Clear, Concise Descriptions

**Issue:** Vague or overly complex descriptions.

**Problematic:**
```yaml
paths:
  /users/{id}:
    put:
      description: This endpoint updates stuff
```

**Recommended:**
```yaml
paths:
  /users/{id}:
    put:
      summary: Update user information
      description: |
        Updates the specified user's information.

        All fields are optional. Only provided fields will be updated.
        The user's ID and creation timestamp cannot be modified.

        Returns the updated user object on success.
```

**Why:**
- Clear and specific descriptions
- Explains what can/cannot be updated
- Sets correct expectations
- Best practice for quality docs

---

### EXAMPLES-PROVIDED: Examples for All Types

**Issue:** Missing examples for requests and responses.

**Problematic:**
```yaml
paths:
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      # No examples
```

**Recommended:**
```yaml
paths:
  /users:
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
            examples:
              basicUser:
                summary: Create a basic user
                value:
                  name: John Doe
                  email: john@example.com
                  role: user
              adminUser:
                summary: Create an admin user
                value:
                  name: Jane Admin
                  email: jane@example.com
                  role: admin
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
              example:
                id: 123
                name: John Doe
                email: john@example.com
                role: user
                status: active
                createdAt: '2024-01-15T10:30:00Z'
```

**Why:**
- Examples clarify usage
- Multiple examples show variations
- Improves developer onboarding
- Best practice for usability

---

### MARKDOWN-FORMAT: Markdown in Descriptions

**Issue:** Plain text descriptions without formatting.

**Problematic:**
```yaml
description: This endpoint returns users. You can filter by status (active, inactive) or role (admin, user). Results are paginated.
```

**Recommended:**
```yaml
description: |
  Returns a paginated list of users from the system.

  ## Filtering

  You can filter results using the following query parameters:
  - `status`: Filter by user status (`active`, `inactive`)
  - `role`: Filter by user role (`admin`, `user`, `guest`)

  ## Pagination

  Results are paginated with a default page size of 20.
  Use `limit` and `offset` parameters to control pagination.

  ## Sorting

  Default sort is by `createdAt` descending.
  Use `sortBy` parameter to change sorting.

  **Note:** Deleted users are not included unless `includeDeleted=true`.
```

**Why:**
- Markdown improves readability
- Structured documentation
- Supports headings, lists, bold, code
- OpenAPI supports CommonMark

---

### CONTACT-INFO: Contact Information

**Issue:** Missing contact information.

**Problematic:**
```yaml
info:
  title: My API
  version: 1.0.0
  # No contact info
```

**Recommended:**
```yaml
info:
  title: User Management API
  version: 1.0.0
  description: Comprehensive API for managing user accounts and profiles
  contact:
    name: API Support Team
    email: api-support@example.com
    url: https://support.example.com
  termsOfService: https://example.com/terms
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html
```

**Why:**
- Provides support contact
- Professional presentation
- Helps developers get help
- Best practice for production APIs

---

### LICENSE-INFO: License Information

**Issue:** Missing license information.

**Problematic:**
```yaml
info:
  title: My API
  version: 1.0.0
  # No license
```

**Recommended:**
```yaml
info:
  title: My API
  version: 1.0.0
  description: API description
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
  # Or for proprietary APIs:
  # license:
  #   name: Proprietary
  #   url: https://example.com/license
```

**Why:**
- Clarifies usage rights
- Legal requirement for many APIs
- Professional presentation
- Best practice

---

## Async Callbacks & Webhooks

### CALLBACKS-DEFINED: Describe Outbound Calls

**Anti-pattern:**
```yaml
paths:
  /payments:
    post:
      summary: Create payment
      # Missing callback documentation
```

**Improved:**
```yaml
paths:
  /payments:
    post:
      summary: Create payment
      callbacks:
        paymentStatus:
          '{$request.body#/callbackUrl}':
            post:
              summary: Notify payment status
              requestBody:
                required: true
                content:
                  application/json:
                    schema:
                      $ref: '#/components/schemas/PaymentStatus'
              responses:
                '200':
                  description: Acknowledge receipt
```

- Use runtime expressions (e.g., `$request.body#/callbackUrl`) for webhook targets.
- Callbacks inherit security requirements unless overridden—document API keys or MTLS expectations clearly.

### LINKS-DEFINED: Connect Related Operations

```yaml
responses:
  '201':
    description: Created
    links:
      GetOrder:
        operationId: getOrder
        parameters:
          orderId: '$response.body#/id'
```

- Helps SDK generators and API consumers discover follow-up calls.

## API Lifecycle & Versioning

### VERSION-STRATEGY
- Align `info.version` with semantic versioning and describe stability (beta/GA) in `x-api-stage` or tags.
- Document versioning approach (URI `/v1`, header `X-API-Version`, media type `application/vnd.example+json;version=1`).

### SUNSET-POLICY
- Deprecate operations with `deprecated: true` AND document timeline (`Sunset` header, `x-sunset-date` extension).
- Provide `externalDocs` or `x-changelog-url` references for migration guides.

### EXTENSIONS-VENDOR
- Explain any `x-*` extensions (gateway integrations, SDK hints) so reviewers understand automation hooks.

---

# Review Checklist

When reviewing OpenAPI specifications, systematically check:

## Structure Checklist
- [ ] OpenAPI version 3.x specified
- [ ] Info object complete (title, version, description)
- [ ] Servers defined for all environments
- [ ] Paths object present with endpoints
- [ ] Components defined for reusability
- [ ] Valid YAML syntax

## API Design Checklist
- [ ] RESTful path naming (nouns, plural)
- [ ] Appropriate HTTP methods
- [ ] Consistent naming conventions
- [ ] Path parameters properly defined
- [ ] Query parameters validated
- [ ] Operation IDs unique and descriptive

## Schema Checklist
- [ ] All schemas have types
- [ ] Required fields marked
- [ ] Validation constraints defined
- [ ] Examples provided
- [ ] Schemas reused via components
- [ ] Enums defined for limited values

## Response Checklist
- [ ] All operations have responses
- [ ] Success responses (2xx) defined
- [ ] Error responses (4xx, 5xx) defined
- [ ] Response schemas defined
- [ ] Examples provided
- [ ] Response descriptions clear

## Security Checklist
- [ ] Security schemes defined
- [ ] Security requirements per endpoint
- [ ] OAuth scopes defined
- [ ] Auth error responses (401, 403)
- [ ] Security descriptions complete

## Documentation Checklist
- [ ] All fields have descriptions
- [ ] Markdown formatting used
- [ ] Examples comprehensive
- [ ] Contact information provided
- [ ] License specified
- [ ] External docs linked

---

## Expected Good Patterns (Check for Absence)

> **Sources:** [OpenAPI Best Practices](https://learn.openapis.org/best-practices.html), [APImatic OpenAPI Guide](https://www.apimatic.io/blog/2022/11/14-best-practices-to-write-openapi-for-better-api-consumption), [Redocly Discriminator Guide](https://redocly.com/learn/openapi/discriminator)

This section identifies the **absence of good patterns** (not just presence of anti-patterns). Use `MISSING-*` IDs for tracking.

### 1. Component Reuse Patterns

**Mnemonic:** **"COMPONENTS-NOT-INLINE"**

| Expected Pattern | If Missing |
|------------------|------------|
| Schemas defined in `components/schemas` | 🔴 `MISSING-COMPONENT-SCHEMA` - Inline schemas with poor names |
| Parameters in `components/parameters` | ⚠️ `MISSING-COMPONENT-PARAM` - Duplicate parameter definitions |
| Responses in `components/responses` | ⚠️ `MISSING-COMPONENT-RESPONSE` - Inconsistent error responses |
| Request bodies in `components/requestBodies` | 💡 `MISSING-COMPONENT-BODY` - Repeated request definitions |

```yaml
# PRESENT: Proper component reuse
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
          description: Unique user identifier
        email:
          type: string
          format: email
          description: User's email address
        name:
          type: string
          description: User's display name

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Machine-readable error code
        message:
          type: string
          description: Human-readable error message

  parameters:
    PageParam:
      name: page
      in: query
      description: Page number for pagination
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: Number of items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: The requested resource was not found

paths:
  /users:
    get:
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'


# MISSING: Inline schemas (anti-pattern)
paths:
  /users:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object  # Inline! Will get auto-generated name like "inline_response_200"
                properties:
                  id:
                    type: string
                  email:
                    type: string
        '404':
          content:
            application/json:
              schema:
                type: object  # Another inline! Duplicated Error definition
                properties:
                  code:
                    type: string
                  message:
                    type: string
```

### 2. Example Patterns

**Mnemonic:** **"EXAMPLES-EVERYWHERE"**

| Expected Pattern | If Missing |
|------------------|------------|
| Examples for all schemas | 🔴 `MISSING-SCHEMA-EXAMPLE` - Unclear expected format |
| Examples for request bodies | ⚠️ `MISSING-REQUEST-EXAMPLE` - Hard to test API |
| Examples for responses | ⚠️ `MISSING-RESPONSE-EXAMPLE` - Unclear API output |
| Examples for parameters | 💡 `MISSING-PARAM-EXAMPLE` - Unclear parameter format |

```yaml
# PRESENT: Comprehensive examples
components:
  schemas:
    Order:
      type: object
      required:
        - id
        - items
        - total
      properties:
        id:
          type: string
          format: uuid
        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
        total:
          type: number
          format: decimal
      example:  # Schema-level example
        id: "550e8400-e29b-41d4-a716-446655440000"
        items:
          - productId: "prod-123"
            quantity: 2
            price: 29.99
        total: 59.98

paths:
  /orders:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrder'
            examples:  # Multiple named examples
              single_item:
                summary: Order with one item
                value:
                  items:
                    - productId: "prod-123"
                      quantity: 1
              multiple_items:
                summary: Order with multiple items
                value:
                  items:
                    - productId: "prod-123"
                      quantity: 2
                    - productId: "prod-456"
                      quantity: 1
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
              example:
                id: "550e8400-e29b-41d4-a716-446655440000"
                items:
                  - productId: "prod-123"
                    quantity: 2
                    price: 29.99
                total: 59.98


# MISSING: No examples
components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
        items:
          type: array
        total:
          type: number
      # No example! What does a real order look like?

paths:
  /orders:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrder'
            # No examples! How do I call this API?
```

### 3. Validation & Constraint Patterns

**Mnemonic:** **"CONSTRAIN-ALL-INPUTS"**

| Expected Pattern | If Missing |
|------------------|------------|
| `required` array for required properties | 🔴 `MISSING-REQUIRED` - Optional when should be mandatory |
| `format` for string types (email, uuid, etc.) | ⚠️ `MISSING-FORMAT` - No semantic validation |
| `minimum`/`maximum` for numbers | ⚠️ `MISSING-NUMERIC-BOUNDS` - Unbounded inputs |
| `minLength`/`maxLength` for strings | ⚠️ `MISSING-STRING-BOUNDS` - Unbounded strings |
| `pattern` for formatted strings | 💡 `MISSING-PATTERN` - No regex validation |
| `enum` for fixed value sets | ⚠️ `MISSING-ENUM` - Any value accepted |

```yaml
# PRESENT: Proper validation constraints
components:
  schemas:
    CreateUser:
      type: object
      required:           # Explicitly mark required fields
        - email
        - password
      properties:
        email:
          type: string
          format: email   # Semantic format
          maxLength: 255
          description: User's email address
        password:
          type: string
          format: password
          minLength: 8    # Minimum security requirement
          maxLength: 128
          pattern: '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$'  # Complexity
          description: Password (min 8 chars, upper, lower, digit)
        age:
          type: integer
          minimum: 13     # Business rule
          maximum: 150
          description: User's age (must be 13+)
        status:
          type: string
          enum:           # Fixed value set
            - active
            - inactive
            - pending
          default: pending
        username:
          type: string
          minLength: 3
          maxLength: 30
          pattern: '^[a-z0-9_]+$'  # Only lowercase, numbers, underscore
          description: Username (3-30 chars, lowercase alphanumeric)


# MISSING: No validation constraints
components:
  schemas:
    CreateUser:
      type: object
      properties:
        email:
          type: string    # Any string accepted! No format!
        password:
          type: string    # Empty password? 10MB password? All valid!
        age:
          type: integer   # Negative? 10000? All valid!
        status:
          type: string    # "banana"? "💩"? All valid!
      # No required array! Everything is optional!
```

### 4. Error Response Patterns

**Mnemonic:** **"ERRORS-DOCUMENTED"**

| Expected Pattern | If Missing |
|------------------|------------|
| Error schema in components | 🔴 `MISSING-ERROR-SCHEMA` - Inconsistent error format |
| 400 Bad Request documented | ⚠️ `MISSING-400` - Validation errors undocumented |
| 401 Unauthorized documented | 🔴 `MISSING-401` - Auth errors undocumented |
| 404 Not Found documented | ⚠️ `MISSING-404` - Missing resource errors |
| 500 Server Error documented | 💡 `MISSING-500` - Server errors undocumented |

```yaml
# PRESENT: Comprehensive error documentation
components:
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Machine-readable error code
          enum:
            - VALIDATION_ERROR
            - NOT_FOUND
            - UNAUTHORIZED
            - FORBIDDEN
            - INTERNAL_ERROR
        message:
          type: string
          description: Human-readable error message
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'
          description: Additional error details

    ErrorDetail:
      type: object
      properties:
        field:
          type: string
          description: Field that caused the error
        reason:
          type: string
          description: Why the field is invalid

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VALIDATION_ERROR
            message: Invalid request parameters
            details:
              - field: email
                reason: Invalid email format

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

paths:
  /orders/{id}:
    get:
      responses:
        '200':
          description: Order details
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'


# MISSING: No error responses
paths:
  /orders/{id}:
    get:
      responses:
        '200':
          description: Order details
      # What happens on error? 🤷‍♂️
```

### 5. Security Patterns

**Mnemonic:** **"SECURE-BY-DEFAULT"**

| Expected Pattern | If Missing |
|------------------|------------|
| `securitySchemes` in components | 🔴 `MISSING-SECURITY-SCHEMES` - No auth defined |
| Global `security` requirement | 🔴 `MISSING-GLOBAL-SECURITY` - API unprotected by default |
| Per-operation security (when different) | ⚠️ `MISSING-OPERATION-SECURITY` - Wrong auth applied |
| OAuth scopes defined | ⚠️ `MISSING-OAUTH-SCOPES` - No scope documentation |

```yaml
# PRESENT: Proper security configuration
openapi: 3.0.3
info:
  title: My Secure API
  version: 1.0.0

security:  # Global security - applies to all operations by default
  - BearerAuth: []

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from /auth/login

    ApiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for machine-to-machine access

    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          scopes:
            read:users: Read user information
            write:users: Create and update users
            admin: Full administrative access

paths:
  /public/health:
    get:
      security: []  # Override: No auth required (public endpoint)
      responses:
        '200':
          description: Health check

  /users:
    get:
      security:
        - OAuth2:
            - read:users  # Specific scope required
      responses:
        '200':
          description: List users

  /admin/settings:
    put:
      security:
        - OAuth2:
            - admin  # Admin scope required
      responses:
        '200':
          description: Settings updated


# MISSING: No security configuration
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

# No global security!
# No securitySchemes!

paths:
  /users:
    get:
      # No security specified - is this protected? 🤷‍♂️
      responses:
        '200':
          description: List users
```

### 6. Description & Documentation Patterns

**Mnemonic:** **"DESCRIBE-EVERYTHING"**

| Expected Pattern | If Missing |
|------------------|------------|
| `description` on all schemas | ⚠️ `MISSING-SCHEMA-DESC` - Unclear data models |
| `description` on all properties | ⚠️ `MISSING-PROPERTY-DESC` - Unclear field purpose |
| `description` on all operations | ⚠️ `MISSING-OPERATION-DESC` - Unclear endpoint purpose |
| `description` on all parameters | ⚠️ `MISSING-PARAM-DESC` - Unclear parameter usage |
| Markdown formatting for complex descriptions | 💡 `MISSING-MARKDOWN` - Poor documentation formatting |

```yaml
# PRESENT: Comprehensive descriptions
components:
  schemas:
    User:
      type: object
      description: |
        A registered user account in the system.

        ## Lifecycle
        Users are created via `/auth/register` and can be in one of several states:
        - `pending`: Email verification required
        - `active`: Fully verified and active
        - `suspended`: Temporarily disabled by admin

        ## Related Resources
        - Orders: `/users/{id}/orders`
        - Profile: `/users/{id}/profile`
      required:
        - id
        - email
        - status
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier for the user (UUID v4)
          readOnly: true
        email:
          type: string
          format: email
          description: |
            User's primary email address.
            - Must be unique across all users
            - Used for login and notifications
            - Cannot be changed after verification
        status:
          type: string
          enum: [pending, active, suspended]
          description: |
            Current account status:
            - `pending`: Awaiting email verification
            - `active`: Fully functional account
            - `suspended`: Disabled by administrator

paths:
  /users/{id}:
    get:
      summary: Get user by ID
      description: |
        Retrieves a single user by their unique identifier.

        ## Authorization
        - Own profile: Any authenticated user
        - Other profiles: Requires `admin` scope

        ## Response
        Returns full user object including profile data.
      parameters:
        - name: id
          in: path
          required: true
          description: The unique identifier (UUID) of the user to retrieve
          schema:
            type: string
            format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"


# MISSING: No descriptions
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        status:
          type: string
      # What is this? How do I use it? 🤷‍♂️

paths:
  /users/{id}:
    get:
      # No summary, no description
      parameters:
        - name: id
          in: path
          required: true
          # What format? What does it identify? 🤷‍♂️
```

### 7. Discriminator & Polymorphism Patterns

**Mnemonic:** **"DISCRIMINATE-UNIONS"**

| Expected Pattern | If Missing |
|------------------|------------|
| `discriminator` with `oneOf`/`anyOf` | 💡 `MISSING-DISCRIMINATOR` - No polymorphism hint |
| `mapping` in discriminator | 💡 `MISSING-DISCRIMINATOR-MAPPING` - Implicit mapping |
| Discriminator property as `required` | 🔴 `MISSING-DISCRIMINATOR-REQUIRED` - Optional discriminator |

```yaml
# PRESENT: Proper discriminator usage
components:
  schemas:
    Notification:
      oneOf:
        - $ref: '#/components/schemas/EmailNotification'
        - $ref: '#/components/schemas/SmsNotification'
        - $ref: '#/components/schemas/PushNotification'
      discriminator:
        propertyName: type
        mapping:
          email: '#/components/schemas/EmailNotification'
          sms: '#/components/schemas/SmsNotification'
          push: '#/components/schemas/PushNotification'

    NotificationBase:
      type: object
      required:
        - type  # Discriminator MUST be required!
        - recipient
      properties:
        type:
          type: string
          description: Type of notification
        recipient:
          type: string
          description: Recipient identifier

    EmailNotification:
      allOf:
        - $ref: '#/components/schemas/NotificationBase'
        - type: object
          required:
            - subject
          properties:
            type:
              type: string
              enum: [email]
            subject:
              type: string
            htmlBody:
              type: string

    SmsNotification:
      allOf:
        - $ref: '#/components/schemas/NotificationBase'
        - type: object
          properties:
            type:
              type: string
              enum: [sms]
            message:
              type: string
              maxLength: 160


# MISSING: No discriminator (harder for code generators)
components:
  schemas:
    Notification:
      oneOf:
        - $ref: '#/components/schemas/EmailNotification'
        - $ref: '#/components/schemas/SmsNotification'
      # No discriminator! Code generator doesn't know which type!
```

---

### Expected Patterns Summary Checklist

**When Reviewing, Verify Presence Of:**

🔴 **Critical (breaks code generation/validation if missing):**
- [ ] `MISSING-COMPONENT-SCHEMA` - Inline schemas instead of components
- [ ] `MISSING-SCHEMA-EXAMPLE` - No examples for schemas
- [ ] `MISSING-REQUIRED` - No required array on schemas
- [ ] `MISSING-ERROR-SCHEMA` - No standardized error format
- [ ] `MISSING-401` - Auth errors undocumented
- [ ] `MISSING-SECURITY-SCHEMES` - No security defined
- [ ] `MISSING-GLOBAL-SECURITY` - No default security
- [ ] `MISSING-DISCRIMINATOR-REQUIRED` - Optional discriminator property

⚠️ **Warning (significant impact):**
- [ ] `MISSING-COMPONENT-PARAM` - Duplicate parameter definitions
- [ ] `MISSING-COMPONENT-RESPONSE` - Inconsistent responses
- [ ] `MISSING-REQUEST-EXAMPLE` - No request examples
- [ ] `MISSING-RESPONSE-EXAMPLE` - No response examples
- [ ] `MISSING-FORMAT` - No semantic format on strings
- [ ] `MISSING-NUMERIC-BOUNDS` - Unbounded numbers
- [ ] `MISSING-STRING-BOUNDS` - Unbounded strings
- [ ] `MISSING-ENUM` - No enum for fixed values
- [ ] `MISSING-400` - Validation errors undocumented
- [ ] `MISSING-404` - Not found errors undocumented
- [ ] `MISSING-OPERATION-SECURITY` - Wrong auth assumptions
- [ ] `MISSING-OAUTH-SCOPES` - No scope documentation
- [ ] `MISSING-SCHEMA-DESC` - No schema descriptions
- [ ] `MISSING-PROPERTY-DESC` - No property descriptions
- [ ] `MISSING-OPERATION-DESC` - No operation descriptions
- [ ] `MISSING-PARAM-DESC` - No parameter descriptions

💡 **Recommendation (good practice):**
- [ ] `MISSING-COMPONENT-BODY` - Repeated request bodies
- [ ] `MISSING-PARAM-EXAMPLE` - No parameter examples
- [ ] `MISSING-PATTERN` - No regex for formatted strings
- [ ] `MISSING-500` - Server errors undocumented
- [ ] `MISSING-MARKDOWN` - No markdown in descriptions
- [ ] `MISSING-DISCRIMINATOR` - No polymorphism hint
- [ ] `MISSING-DISCRIMINATOR-MAPPING` - Implicit discriminator mapping

---

# Severity Levels

Categorize findings by severity:

**🔴 Critical (Must Fix)**
- Missing OpenAPI version
- Missing required fields (info.title, info.version)
- Invalid YAML syntax
- Missing response definitions
- Path parameters not marked required
- Security schemes missing for protected API

**⚠️ Warning (Should Fix)**
- Missing operation IDs
- No examples provided
- Missing error responses
- Inconsistent naming conventions
- Missing validation constraints
- No schema descriptions

**💡 Recommendation (Best Practice)**
- Add more examples
- Improve descriptions with Markdown
- Add external documentation links
- Use schema composition (allOf, oneOf)
- Add contact and license info
- Enhance error response details

---

# Your Review Style

- **Thorough**: Check all aspects of the OpenAPI specification
- **Practical**: Provide working YAML examples
- **Educational**: Explain the "why" behind each issue
- **Standards-focused**: Reference OpenAPI Specification, REST principles
- **Constructive**: Frame as improvements for better API design

Remember: A well-documented API specification is the foundation of a great API. Help teams build comprehensive, clear, and maintainable API documentation.
