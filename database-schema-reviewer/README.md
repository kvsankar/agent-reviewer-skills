# Database Schema Reviewer

A Claude Code skill for reviewing relational database schemas using industry best practices for normalization, performance, and data integrity.

## What It Does

This skill reviews database schemas (DDL scripts, migrations, ORM models) for:
- **Normalization** - 1NF through 5NF, denormalization strategies
- **Performance** - Indexing, partitioning, query optimization
- **Data Integrity** - Primary keys, foreign keys, constraints
- **Data Types** - Appropriate column types and sizes
- **Database-Specific** - MySQL, PostgreSQL, MS SQL Server best practices
- **Naming Conventions** - Consistent, clear naming standards

## When to Use

Use this skill when you need to:
- Review database schema designs
- Validate DDL scripts before deployment
- Optimize database performance
- Check normalization compliance
- Review database migrations
- Audit existing schemas for improvements

## How to Use

### In Claude Code

```
Please review this database schema:
[paste DDL/migration script]
```

Or reference a file:
```
Review the schema in ./migrations/001_initial_schema.sql
```

### Keywords That Trigger This Skill

- Database schema
- DDL script
- Database design
- Normalization
- Foreign keys
- Database migration
- MySQL schema
- PostgreSQL schema
- SQL Server schema
- Table design
- Index optimization

## What You'll Get

A structured review with:

### ✅ Strengths
Things done well in the schema

### 🔴 Critical Issues
Problems that must be fixed:
- Missing primary keys
- Missing foreign key constraints
- Normalization violations
- Data integrity risks

### ⚠️ Warnings
Issues that should be addressed:
- Missing indexes
- Inefficient data types
- Performance concerns
- Naming inconsistencies

### 💡 Recommendations
Best practices to improve the schema:
- Indexing strategies
- Partitioning suggestions
- Type optimizations
- Platform-specific features

## Example Review Output

```markdown
## Database Schema Review: E-commerce Database

### ✅ Strengths
- **PK-REQUIRED**: All tables have primary keys
- **FK-CONSTRAINT**: Foreign keys properly defined with CASCADE rules
- **IDX-STRATEGY**: Good use of composite indexes

### 🔴 Critical Issues

#### NORM-3NF: Third Normal Form Violation

**Current schema:**
```sql
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_email VARCHAR(255),  -- Transitive dependency
  customer_address TEXT  -- Transitive dependency
);
```

**Recommended schema:**
```sql
CREATE TABLE customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  address TEXT
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

**Impact:**
Violates 3NF due to transitive dependencies. Customer data duplicated across orders, leading to update anomalies and data inconsistency.
```

## Guidelines Covered

### Normalization (8 guidelines)
- First normal form (1NF)
- Second normal form (2NF)
- Third normal form (3NF)
- Boyce-Codd normal form (BCNF)
- Fourth normal form (4NF)
- Fifth normal form (5NF)
- Strategic denormalization
- Avoid EAV anti-pattern

### Primary Keys & Identity (6 guidelines)
- Primary key requirements
- Surrogate vs natural keys
- UUID vs auto-increment
- Composite key usage
- Naming conventions
- Clustered index considerations

### Foreign Keys & Relationships (8 guidelines)
- Foreign key constraints
- CASCADE delete/update rules
- Indexing foreign keys
- Naming conventions
- Nullable foreign keys
- Orphan prevention
- Circular reference avoidance
- Polymorphic associations

### Indexing (10 guidelines)
- Index strategy
- Index selectivity
- Composite index column order
- Covering indexes
- Unique constraints
- Redundant index avoidance
- Prefix indexes
- Full-text search indexes
- Partial/filtered indexes
- Index maintenance overhead

### Data Types (10 guidelines)
- Appropriate type selection
- Column sizing
- Numeric types (INT, BIGINT, DECIMAL, FLOAT)
- String types (CHAR, VARCHAR, TEXT)
- Date/time types (DATE, TIMESTAMP, DATETIME)
- Boolean representation
- ENUM vs lookup tables
- JSON column usage
- BLOB/TEXT usage
- DECIMAL vs FLOAT for money

### Constraints & Validation (6 guidelines)
- NOT NULL constraints
- DEFAULT values
- CHECK constraints
- UNIQUE constraints
- Data validation rules
- Trigger usage

### Naming Conventions (6 guidelines)
- Table naming
- Column naming
- Consistency standards
- Reserved word avoidance
- Abbreviation standards
- Singular vs plural

### Performance Optimization (6 guidelines)
- Table partitioning
- Archival strategies
- Soft delete patterns
- Counter cache tables
- Materialized views
- Sharding considerations

### Database-Specific (MySQL - 4 guidelines)
- Storage engine selection (InnoDB)
- Character set and collation
- Full-text search
- JSON column type

### Database-Specific (PostgreSQL - 4 guidelines)
- SERIAL types vs sequences
- Array column usage
- JSONB vs JSON
- Extension usage

### Database-Specific (MS SQL Server - 4 guidelines)
- IDENTITY columns
- UNIQUEIDENTIFIER usage
- FILESTREAM usage
- Temporal tables

## Supported Platforms

- **MySQL** / MariaDB (5.7+, 8.0+)
- **PostgreSQL** (10+, 14+)
- **Microsoft SQL Server** (2016+, 2019+)
- **Generic SQL** (ANSI SQL standards)

Platform-specific recommendations provided when applicable.

## Sources

All guidelines are based on:
- Database normalization theory (Codd, Date, Fagin)
- MySQL documentation and best practices
- PostgreSQL documentation and best practices
- SQL Server documentation and best practices
- Industry standards (SQL:2016, ANSI SQL)
- Performance optimization research

See [SOURCES.md](SOURCES.md) for detailed references.

## Tips

1. **Specify the database**: Mention MySQL, PostgreSQL, or SQL Server for platform-specific advice
2. **Provide context**: Share performance requirements, data volume expectations
3. **Include migrations**: Review migration scripts before applying to production
4. **Ask questions**: Request clarification on normalization or indexing recommendations

## Examples of Good Use

✅ "Review this MySQL schema for normalization and performance"
✅ "Check this PostgreSQL migration for indexing best practices"
✅ "Validate this SQL Server schema against normalization principles"
✅ "Review these Django ORM models for database efficiency"
✅ "Check if this schema needs denormalization for performance"

## Related Skills

- `django-reviewer` - For reviewing Django ORM models and queries
- `security-privacy-reviewer` - For database security and PII handling
- `refactoring-reviewer` - For refactoring database access code
- `python-test-reviewer` - For reviewing database tests

---

**Note**: This skill reviews database schema definitions (DDL, migrations, models), not query optimization or application code. For query performance review, analyze queries alongside schema design.
