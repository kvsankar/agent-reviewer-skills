# Sources and References

All guidelines in the Database Schema Reviewer are based on database theory, normalization principles, and official vendor documentation.

## Primary Sources

### Database Theory & Normalization

- **E.F. Codd's Work on Relational Databases**
  - "A Relational Model of Data for Large Shared Data Banks" (1970)
  - "Further Normalization of the Data Base Relational Model" (1971)
  - Publisher: ACM (Association for Computing Machinery)
  - Topics: 1NF, 2NF, 3NF, relational model fundamentals

- **C.J. Date - Database Systems**
  - "An Introduction to Database Systems" (8th Edition)
  - Publisher: Addison-Wesley
  - ISBN: 978-0321197849
  - Topics: Normalization, relational theory, database design

- **Ronald Fagin - Fourth & Fifth Normal Forms**
  - "Multivalued Dependencies and a New Normal Form" (1977)
  - "Normal Forms and Relational Database Operators" (1979)
  - Topics: 4NF, 5NF, join dependencies

- **Raymond F. Boyce & E.F. Codd - BCNF**
  - Boyce-Codd Normal Form
  - Topics: Refinement of 3NF, elimination of anomalies

### MySQL Documentation

- **MySQL 8.0 Reference Manual**
  - URL: https://dev.mysql.com/doc/refman/8.0/en/
  - Publisher: Oracle Corporation
  - Topics: InnoDB, indexing, data types, JSON, partitioning
  - License: GPL

- **MySQL Performance Blog (Percona)**
  - URL: https://www.percona.com/blog/
  - Topics: Index optimization, query performance, schema design

- **High Performance MySQL** (3rd Edition)
  - Authors: Baron Schwartz, Peter Zaitsev, Vadim Tkachenko
  - Publisher: O'Reilly Media
  - ISBN: 978-1449314286
  - Topics: Indexing strategies, schema optimization, InnoDB

### PostgreSQL Documentation

- **PostgreSQL 14 Documentation**
  - URL: https://www.postgresql.org/docs/14/
  - Publisher: PostgreSQL Global Development Group
  - Topics: Indexes (B-tree, GIN, GiST), JSONB, partitioning, constraints
  - License: PostgreSQL License

- **The Art of PostgreSQL**
  - Author: Dimitri Fontaine
  - Publisher: Self-published
  - Topics: Advanced features, performance, data types

### SQL Server Documentation

- **SQL Server 2019 Documentation**
  - URL: https://docs.microsoft.com/en-us/sql/sql-server/
  - Publisher: Microsoft Corporation
  - Topics: Clustered indexes, filtered indexes, temporal tables, columnstore

- **SQL Server Internals Series**
  - Author: Kalen Delaney
  - Publisher: Microsoft Press
  - Topics: Storage engine, indexing, query optimization

## Supporting References

### Indexing & Performance

- **Database Indexing Principles**
  - Markus Winand - "SQL Performance Explained"
  - URL: https://use-the-index-luke.com/
  - Topics: Index selection, composite indexes, covering indexes

- **Relational Database Index Design and the Optimizers**
  - Authors: Tapio Lahdenmaki, Michael Leach
  - Publisher: Wiley
  - ISBN: 978-0471719991
  - Topics: Index design patterns, optimizer behavior

### Data Modeling

- **Database Design for Mere Mortals** (3rd Edition)
  - Author: Michael J. Hernandez
  - Publisher: Addison-Wesley
  - ISBN: 978-0321884497
  - Topics: ER modeling, normalization, business rules

- **The Data Model Resource Book** (Revised Edition)
  - Author: Len Silverston
  - Publisher: Wiley
  - ISBN: 978-0471380238
  - Topics: Universal data models, industry patterns

### SQL Standards

- **ISO/IEC 9075:2016 (SQL:2016)**
  - International SQL Standard
  - Publisher: ISO/IEC
  - Topics: SQL syntax, data types, constraints

- **ANSI SQL Standards**
  - American National Standards Institute
  - Topics: Standard SQL syntax and semantics

## Guideline Categories and Attribution

### Normalization (8 guidelines)
**Sources:**
- E.F. Codd (1NF, 2NF, 3NF)
- Raymond Boyce & E.F. Codd (BCNF)
- Ronald Fagin (4NF, 5NF)
- C.J. Date - Database normalization theory

**Referenced Concepts:**
- NORM-1NF: Codd's First Normal Form
- NORM-2NF: Codd's Second Normal Form
- NORM-3NF: Codd's Third Normal Form
- NORM-BCNF: Boyce-Codd Normal Form
- NORM-4NF: Fagin's Fourth Normal Form
- NORM-5NF: Fagin's Fifth Normal Form
- NORM-DENORM: Strategic denormalization patterns
- NORM-EAV: Entity-Attribute-Value anti-pattern

### Primary Keys & Identity (6 guidelines)
**Sources:**
- Relational database theory (Codd)
- MySQL InnoDB clustered indexes
- SQL Server clustered index best practices
- PostgreSQL sequences and SERIAL

**Referenced Concepts:**
- PK-REQUIRED: Fundamental relational theory
- PK-SURROGATE: Natural vs surrogate key trade-offs
- PK-UUID: UUID vs auto-increment patterns
- PK-COMPOSITE: Composite key usage
- PK-NAMING: Convention best practices
- PK-CLUSTERED: SQL Server / InnoDB specific

### Foreign Keys & Relationships (8 guidelines)
**Sources:**
- Relational integrity constraints (Codd, Date)
- MySQL InnoDB foreign keys
- PostgreSQL foreign key documentation
- SQL Server CASCADE rules

**Referenced Concepts:**
- FK-CONSTRAINT: Referential integrity (Codd)
- FK-CASCADE: CASCADE, RESTRICT, SET NULL options
- FK-INDEX: Index optimization for joins
- FK-POLYMORPHIC: Polymorphic association patterns

### Indexing (10 guidelines)
**Sources:**
- "SQL Performance Explained" (Markus Winand)
- "High Performance MySQL" (Schwartz et al.)
- Database vendor index documentation
- "Relational Database Index Design" (Lahdenmaki, Leach)

**Referenced Concepts:**
- IDX-STRATEGY: Index selection methodology
- IDX-SELECTIVE: Selectivity calculations
- IDX-COMPOSITE: Leftmost prefix rule
- IDX-COVERING: Index-only scans
- IDX-FULL-TEXT: Full-text search indexes
- IDX-PARTIAL: PostgreSQL partial indexes

### Data Types (10 guidelines)
**Sources:**
- MySQL 8.0 data types documentation
- PostgreSQL data types documentation
- SQL Server data types documentation
- SQL:2016 standard data types

**Referenced Concepts:**
- TYPE-APPROPRIATE: Proper type selection
- TYPE-NUMERIC: Integer vs decimal vs float
- TYPE-STRING: CHAR vs VARCHAR vs TEXT
- TYPE-DATE: DATE vs DATETIME vs TIMESTAMP
- TYPE-JSON: MySQL JSON, PostgreSQL JSONB

### Constraints & Validation (6 guidelines)
**Sources:**
- SQL standard constraints (SQL:2016)
- Database integrity constraints (Date)
- Vendor-specific constraint documentation

**Referenced Concepts:**
- CONST-NOT-NULL: NULL handling best practices
- CONST-CHECK: Domain constraints
- CONST-UNIQUE: Uniqueness constraints

### Naming Conventions (6 guidelines)
**Sources:**
- Industry best practices
- SQL style guides (Simon Holywell, Joe Celko)
- Database naming conventions research

**Referenced Resources:**
- SQL Style Guide: https://www.sqlstyle.guide/
- Joe Celko's SQL Programming Style

### Performance Optimization (6 guidelines)
**Sources:**
- Database partitioning research
- Data warehousing best practices
- Temporal database patterns

**Referenced Concepts:**
- PERF-PARTITION: Range, list, hash partitioning
- PERF-ARCHIVE: Data lifecycle management
- PERF-MATERIALIZED: Materialized view patterns

### Database-Specific Guidelines
**Sources:**
- MySQL 8.0 / MariaDB specific features
- PostgreSQL 14+ specific features
- SQL Server 2019+ specific features

**Referenced Features:**
- MySQL: InnoDB storage engine, utf8mb4, JSON type
- PostgreSQL: SERIAL, ARRAY, JSONB, extensions (pg_trgm, uuid-ossp)
- SQL Server: IDENTITY, UNIQUEIDENTIFIER, temporal tables, FILESTREAM

## Industry Best Practices

### MySQL
- **Percona Database Performance Blog**
  - URL: https://www.percona.com/blog/
  - Topics: MySQL optimization, InnoDB tuning

- **Planet MySQL**
  - URL: https://planet.mysql.com/
  - Community best practices aggregator

### PostgreSQL
- **PostgreSQL Wiki**
  - URL: https://wiki.postgresql.org/
  - Topics: Performance tuning, best practices

- **2ndQuadrant Blog**
  - URL: https://www.2ndquadrant.com/en/blog/
  - PostgreSQL expertise and patterns

### SQL Server
- **SQL Server Central**
  - URL: https://www.sqlservercentral.com/
  - Community best practices

- **Brent Ozar Unlimited**
  - URL: https://www.brentozar.com/
  - SQL Server performance and design

## Tools and Validators

These tools implement and validate these principles:

- **MySQL Workbench** - Schema design and validation
- **pgAdmin** - PostgreSQL schema management
- **SQL Server Management Studio** - Schema design
- **dbdiagram.io** - Database schema visualization
- **SchemaSpy** - Schema documentation generator
- **pt-duplicate-key-checker** (Percona Toolkit) - Find redundant indexes
- **pg_stat_statements** - PostgreSQL query analysis

## Additional Reading

### Books
- "Database Design and Relational Theory" by C.J. Date
- "SQL Antipatterns" by Bill Karwin (Pragmatic Bookshelf, 2010)
- "Refactoring Databases" by Scott W. Ambler and Pramod J. Sadalage
- "SQL Performance Explained" by Markus Winand

### Research Papers
- "The Entity-Relationship Model" by Peter Chen (1976)
- "A Normal Form for Relational Databases" by Codd (1971)
- "Synthesizing Third Normal Form Relations from Functional Dependencies" by Bernstein (1976)

### Online Resources
- Database Administrators Stack Exchange: https://dba.stackexchange.com/
- Use The Index, Luke!: https://use-the-index-luke.com/
- SQL Style Guide: https://www.sqlstyle.guide/

## Vendor Documentation Links

- **MySQL**: https://dev.mysql.com/doc/
- **MariaDB**: https://mariadb.com/kb/en/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **SQL Server**: https://docs.microsoft.com/en-us/sql/
- **Oracle Database**: https://docs.oracle.com/en/database/

## License Information

This skill is based on publicly available database theory, standards, and vendor documentation:

- **Database Theory**: Academic research (public domain, ACM licensed)
- **SQL Standards**: ISO/IEC, ANSI standards
- **Vendor Documentation**: MySQL (GPL), PostgreSQL (PostgreSQL License), SQL Server (Microsoft documentation)
- **Books**: Fair use for educational reference purposes
- **Best Practices**: Community knowledge and industry patterns

All referenced materials are used in accordance with their respective licenses for educational and reference purposes.

---

**Note**: This skill provides guidance based on established database theory and vendor best practices. Always refer to official documentation for your specific database version.

**Last Updated**: November 2025
**Database Versions Covered**: MySQL 8.0+, PostgreSQL 14+, SQL Server 2019+
