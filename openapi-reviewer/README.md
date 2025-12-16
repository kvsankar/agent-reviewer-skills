# OpenAPI Specification Reviewer

A Claude Code skill for reviewing OpenAPI/Swagger specifications using industry best practices.

## What It Does

This skill reviews OpenAPI (Swagger) specification files for:
- **Structure & Format** - OpenAPI version, required fields, valid YAML
- **API Design** - RESTful naming, HTTP methods, consistency
- **Data Models** - Schema definitions, validation, reusability
- **Documentation** - Descriptions, examples, completeness
- **Security** - Authentication schemes, requirements, error handling
- **Responses** - Success and error responses, schemas, examples

## When to Use

Use this skill when you need to:
- Review OpenAPI/Swagger YAML or JSON files
- Validate API specification quality
- Check REST API design best practices
- Ensure complete API documentation
- Verify security definitions
- Get feedback on API improvements

## How to Use

### In Claude Code

```
Please review this OpenAPI specification:
[paste OpenAPI YAML content]
```

Or reference a file:
```
Review the OpenAPI spec at ./api/openapi.yaml
```

### Keywords That Trigger This Skill

- OpenAPI
- Swagger
- API specification
- API spec
- REST API design
- API definition
- YAML API
- API documentation review

## What You'll Get

A structured review with:

### ✅ Strengths
Things done well in the specification

### 🔴 Critical Issues
Problems that must be fixed:
- Missing required fields
- Invalid structure
- Security gaps

### ⚠️ Warnings
Issues that should be addressed:
- Missing examples
- Incomplete documentation
- Inconsistent naming

### 💡 Recommendations
Best practices to improve the API:
- Better organization
- Enhanced documentation
- Improved schema design

## Example Review Output

````markdown
## OpenAPI Specification Review: User Management API

### ✅ Strengths
- **API-VERSION**: OpenAPI 3.0.3 properly specified
- **COMPONENTS-REUSE**: Good use of reusable schemas
- **SECURITY-SCHEMES**: Well-defined JWT authentication

### 🔴 Critical Issues

#### PATH-PARAM-REQUIRED: Path Parameters Not Marked Required

**Current specification:**
```yaml
paths:
  /users/{id}:
    parameters:
      - name: id
        in: path
        schema:
          type: integer
```

**Recommended specification:**
```yaml
paths:
  /users/{id}:
    parameters:
      - name: id
        in: path
        required: true
        description: Unique identifier of the user
        schema:
          type: integer
          format: int64
```
````

## Guidelines Covered

### Structure (8 guidelines)
- OpenAPI version
- Required info fields
- Server definitions
- Paths object
- Components reuse
- Tags organization
- External docs
- Valid YAML

### Path & Operations (10 guidelines)
- RESTful path naming
- Path parameters
- Operation IDs
- Summaries and descriptions
- HTTP methods
- Tags
- Deprecation
- Response codes
- Request bodies

### Parameters (6 guidelines)
- Required markers
- Descriptions
- Examples
- Validation rules
- Naming conventions
- Path parameter requirements

### Schemas (8 guidelines)
- Schema definitions
- Type specifications
- Property descriptions
- Validation constraints
- Examples
- Reusability
- Enumerations
- Discriminators

### Responses (6 guidelines)
- Required responses
- Response descriptions
- Response schemas
- Error responses
- Success examples
- Error examples

### Security (6 guidelines)
- Security schemes
- Security requirements
- API key conventions
- OAuth scopes
- Security descriptions
- Auth error responses

### Documentation (6 guidelines)
- Complete descriptions
- Clear writing
- Examples everywhere
- Markdown formatting
- Contact information
- License information

## Sources

All guidelines are based on:
- OpenAPI Specification 3.0.x and 3.1.x
- REST API design principles
- Industry best practices
- API documentation standards

See [SOURCES.md](SOURCES.md) for detailed references.

## Tips

1. **Provide the full spec**: Include the complete OpenAPI file for comprehensive review
2. **Specify concerns**: Mention specific areas you're concerned about
3. **Ask questions**: Request clarification on any recommendations
4. **Iterate**: Apply suggestions and ask for re-review

## Examples of Good Use

✅ "Review this OpenAPI spec for completeness"
✅ "Check if this API follows REST best practices"
✅ "Validate the security definitions in this spec"
✅ "Review the error handling in this OpenAPI file"

## Related Skills

- `security-privacy-reviewer` - For reviewing API implementation security
- `refactoring-reviewer` - For reviewing API implementation code
- `python-test-reviewer` - For reviewing API tests

---

**Note**: This skill reviews the API specification (OpenAPI/Swagger files), not the implementation code. For code review, use the appropriate language-specific reviewer skill.
