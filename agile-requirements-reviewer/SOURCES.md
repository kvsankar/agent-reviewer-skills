# Sources and Attribution

This skill builds upon decades of requirements engineering, business analysis, and agile methodology best practices. All guidelines are derived from publicly available resources, standards, books, and community knowledge.

## Primary Sources

### 1. INVEST Criteria - Bill Wake

**Source:** XP123 / Bill Wake's work on user story quality
**Author:** Bill Wake
**Original Article:** "INVEST in Good Stories, and SMART Tasks" (2003)
**URL:** https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/

**Key Contributions:**
- INVEST acronym for user story quality
- Independent - stories can be developed in any order
- Negotiable - details are worked out through conversation
- Valuable - provides value to users or business
- Estimable - team can estimate the effort
- Small - fits within one iteration
- Testable - has clear acceptance criteria

**Guidelines Derived:**
- INVEST-I: Stories Should Be Independent
- INVEST-N: Stories Should Be Negotiable
- INVEST-V: Stories Must Provide Value
- INVEST-E: Stories Should Be Estimable
- INVEST-S: Stories Should Be Small
- INVEST-T: Stories Must Be Testable

---

### 2. User Stories Applied - Mike Cohn

**Source:** "User Stories Applied: For Agile Software Development" (2004)
**Author:** Mike Cohn
**Publisher:** Addison-Wesley Professional

**Key Contributions:**
- User story format: "As a [role], I want [feature], so that [benefit]"
- Acceptance criteria patterns
- Story splitting techniques
- Estimating and planning with user stories
- User personas in stories
- Definition of Done

**Guidelines Derived:**
- STORY-FORMAT: Use Standard User Story Format
- STORY-ACCEPT: Include Clear Acceptance Criteria
- STORY-VALUE: Explicitly State Business Value
- STORY-PERSONA: Use Specific User Personas
- STORY-DOD: Include Definition of Done
- INVEST-S: Stories Should Be Small (splitting techniques)

---

### 3. Writing Effective Use Cases - Alistair Cockburn

**Source:** "Writing Effective Use Cases" (2000)
**Author:** Alistair Cockburn
**Publisher:** Addison-Wesley Professional

**Key Contributions:**
- Use case structure and format
- Primary and secondary actors
- Main success scenario
- Extensions (alternative and exception flows)
- Preconditions and postconditions
- Use case levels and scope

**Guidelines Derived:**
- USE-ACTOR: Clearly Identify All Actors
- USE-PRECON: Specify Preconditions
- USE-POSTCON: Specify Postconditions
- USE-FLOW: Document Complete Main Success Scenario
- USE-ALT: Document Alternative Flows
- USE-EXCEPT: Document Exception Flows
- USE-EXTEND: Identify Extension Points
- USE-DATA: Specify Data Exchanged

---

### 4. Software Requirements - Karl Wiegers & Joy Beatty

**Source:** "Software Requirements" (3rd Edition, 2013)
**Authors:** Karl E. Wiegers, Joy Beatty
**Publisher:** Microsoft Press

**Key Contributions:**
- Requirements quality characteristics
- Requirements documentation practices
- Avoiding ambiguous terms
- Verifiable requirements
- Requirements traceability
- Managing requirements changes

**Guidelines Derived:**
- REQ-CLEAR: Use Clear, Unambiguous Language
- REQ-ATOMIC: One Requirement Per Statement
- REQ-AVOID-VAGUE: Avoid Vague Terms
- REQ-MEASURABLE: Make Requirements Measurable
- REQ-TESTABLE: Requirements Must Be Testable
- REQ-TRACE: Requirements Must Be Traceable
- CONS-NO-CONFLICT: Identify and Resolve Contradictions
- COMP-COMPLETE: Ensure Completeness

---

### 5. IEEE 830-1998 - Software Requirements Specifications

**Source:** IEEE Recommended Practice for Software Requirements Specifications
**Organization:** Institute of Electrical and Electronics Engineers
**Standard:** IEEE Std 830-1998 (superseded by ISO/IEC/IEEE 29148:2011)

**Key Contributions:**
- SRS document structure
- Requirements characteristics (unambiguous, complete, verifiable, etc.)
- Functional and non-functional requirements
- Problem domain vs. solution domain
- Requirements organization

**Guidelines Derived:**
- REQ-CLEAR: Unambiguous requirements
- REQ-COMPLETE: Complete information
- REQ-TESTABLE: Verifiable requirements
- REQ-OBSERVABLE: Observable outcomes
- PROB-WHAT: Focus on WHAT, not HOW
- COMP-NFR: Include Non-Functional Requirements

---

### 6. BABOK - Business Analysis Body of Knowledge

**Source:** "A Guide to the Business Analysis Body of Knowledge" (BABOK Guide)
**Organization:** International Institute of Business Analysis (IIBA)
**Latest Version:** BABOK v3 (2015)

**Key Contributions:**
- Requirements elicitation techniques
- Requirements analysis and documentation
- Solution evaluation
- Stakeholder analysis
- Business analysis planning
- Requirements management and communication

**Guidelines Derived:**
- COMP-ACTORS: Identify All Actors (stakeholder analysis)
- CONS-TERM: Use Consistent Terminology (business vocabulary)
- PROB-BUSINESS: Use Business Language
- COMP-CONSTRAINTS: Document Constraints
- COMP-ASSUMPTIONS: State All Assumptions
- REQ-TRACE: Requirements traceability

---

### 7. Agile Extension to BABOK Guide

**Source:** "Agile Extension to the BABOK Guide" (2013)
**Organization:** International Institute of Business Analysis (IIBA)

**Key Contributions:**
- Agile business analysis practices
- User stories in agile context
- Acceptance criteria
- Product backlog refinement
- Definition of Ready and Done

**Guidelines Derived:**
- STORY-FORMAT: User story structure in agile
- STORY-ACCEPT: Acceptance criteria for stories
- STORY-DOD: Definition of Done
- INVEST criteria application in agile context

---

### 8. Scaled Agile Framework (SAFe) - Dean Leffingwell

**Source:** Scaled Agile Framework methodology
**Author:** Dean Leffingwell
**Website:** https://scaledagileframework.com/

**Key Contributions:**
- Requirements at scale (epics, features, stories)
- Acceptance criteria patterns
- Non-functional requirements in agile
- Architectural runway
- Solution intent

**Guidelines Derived:**
- CONS-LEVEL: Maintain Consistent Level of Detail (epic/feature/story hierarchy)
- COMP-NFR: Non-functional requirements in agile
- STORY-VALUE: Business value articulation

---

### 9. Use Case 2.0 - Ivar Jacobson

**Source:** "Use Case 2.0: The Guide" (2011)
**Author:** Ivar Jacobson
**Organization:** Ivar Jacobson International

**Key Contributions:**
- Lightweight use case approach
- Use case slices
- Integration with agile
- Use case-driven development

**Guidelines Derived:**
- USE-FLOW: Main success scenario
- USE-ALT: Alternative flows
- USE-EXCEPT: Exception handling
- Integration of use cases with user stories

---

## Concept Sources

### Problem Domain vs. Solution Domain

**Principle:** Requirements describe the problem (what's needed), not the solution (how it's built).

**Sources:**
- **Michael Jackson** - "Problem Frames" (2001)
- **Pamela Zave & Michael Jackson** - "Four Dark Corners of Requirements Engineering" (1997)
- **IEEE 830** - Distinguishing functional requirements from design constraints

**Guidelines Derived:**
- PROB-WHAT: Focus on WHAT, Not HOW
- PROB-NO-ARCH: No Architecture Decisions
- PROB-NO-DESIGN: No Design Details
- PROB-NO-TECH: No Technology Choices
- PROB-EXTERNAL: Focus on External Behavior

---

### Requirements Quality Attributes

**Principle:** Good requirements are clear, complete, consistent, verifiable, traceable, etc.

**Sources:**
- **IEEE 830** - Characteristics of good SRS
- **Karl Wiegers** - Requirements quality attributes
- **ISO/IEC/IEEE 29148:2011** - Systems and software engineering requirements

**Quality Attributes:**
- **Unambiguous** - Only one interpretation
- **Complete** - All necessary information present
- **Consistent** - No contradictions
- **Verifiable** - Can be tested/verified
- **Traceable** - Linked to source and design
- **Modifiable** - Easy to change
- **Prioritized** - Importance indicated

**Guidelines Derived:**
- REQ-CLEAR: Clear, unambiguous language
- REQ-COMPLETE: Complete information
- CONS-NO-CONFLICT: No contradictions
- REQ-TESTABLE: Verifiable requirements
- REQ-TRACE: Traceability

---

### Avoiding Ambiguity in Requirements

**Principle:** Eliminate words and phrases that have multiple interpretations.

**Sources:**
- **Donald Firesmith** - "Common Requirements Problems" (2007)
- **Karl Wiegers** - Ambiguous terms to avoid
- **NASA** - Requirements writing guidelines

**Common Ambiguous Terms:**
- "Fast", "quick", "rapid" - How fast?
- "User-friendly", "easy to use" - According to whom?
- "Etc.", "and so on" - What else is included?
- "Appropriate", "suitable" - What criteria?
- "Flexible", "adaptable" - In what ways?

**Guidelines Derived:**
- REQ-AVOID-VAGUE: Avoid Vague Terms
- REQ-MEASURABLE: Make Requirements Measurable
- REQ-CLEAR: Unambiguous language

---

### Functional vs. Non-Functional Requirements

**Principle:** Systems have both functional requirements (what they do) and non-functional requirements (how well they do it).

**Sources:**
- **Lawrence Chung et al.** - "Non-Functional Requirements in Software Engineering" (1999)
- **ISO/IEC 25010** - System and software quality models
- **Martin Glinz** - "On Non-Functional Requirements" (2007)

**Non-Functional Categories:**
- Performance (speed, throughput, response time)
- Scalability (growth capacity)
- Security (protection, authentication)
- Reliability (uptime, MTBF)
- Usability (ease of use, learnability)
- Maintainability (modifiability, testability)
- Portability (adaptability, installability)

**Guidelines Derived:**
- COMP-NFR: Include Non-Functional Requirements

---

## Anti-Pattern Sources

### Gold Plating

**Principle:** Don't add features beyond what's needed or requested.

**Sources:**
- **Steve McConnell** - "Code Complete" (2004) - discusses gold plating in development
- **Project Management Institute** - PMBOK Guide - scope creep and gold plating
- **Agile Manifesto** - Principles of simplicity

**Guidelines Derived:**
- ANTI-GOLD: Avoid Gold Plating

---

### Requirements Creep and Scope Creep

**Principle:** Manage scope and avoid uncontrolled growth of requirements.

**Sources:**
- **Project Management Body of Knowledge** (PMBOK)
- **Agile practices** - time-boxing and product backlog management

**Guidelines Derived:**
- ANTI-GOLD: Focus on requested needs
- ANTI-FUTURE: Avoid premature future-proofing

---

### Mixing Requirements with Design

**Principle:** Requirements state needs; design specifies solutions. Keep them separate.

**Sources:**
- **IEEE 830** - SRS should not include design
- **Karl Wiegers** - Requirements vs. design
- **Alistair Cockburn** - Use cases describe external behavior

**Guidelines Derived:**
- PROB-NO-DESIGN: No Design Details
- PROB-NO-ARCH: No Architecture Decisions
- PROB-NO-TECH: No Technology Choices
- ANTI-IMPL: Don't Sneak Implementation into Requirements

---

## Guideline Mapping

Each guideline in this skill can be traced to one or more sources:

### User Story Quality (INVEST)
- All INVEST guidelines → **Bill Wake** (INVEST criteria)
- User story format → **Mike Cohn** (User Stories Applied)
- Acceptance criteria → **Mike Cohn**, **Agile Extension to BABOK**

### User Story Structure
- STORY-FORMAT → **Mike Cohn**
- STORY-ACCEPT → **Mike Cohn**, **Agile Extension to BABOK**
- STORY-VALUE → **Mike Cohn**, **SAFe**
- STORY-PERSONA → **Mike Cohn**, **Alan Cooper** (About Face)
- STORY-DOD → **Agile Extension to BABOK**, **Scrum Guide**

### Use Case Quality
- All USE- guidelines → **Alistair Cockburn** (Writing Effective Use Cases)
- USE-ACTOR → **Alistair Cockburn**, **Ivar Jacobson**
- USE-FLOW → **Alistair Cockburn**, **Use Case 2.0**

### Requirements Clarity
- REQ-CLEAR → **IEEE 830**, **Karl Wiegers**
- REQ-ATOMIC → **Karl Wiegers**
- REQ-AVOID-VAGUE → **Karl Wiegers**, **NASA Guidelines**
- REQ-MEASURABLE → **Tom Gilb** (Planguage), **Karl Wiegers**
- REQ-AVOID-AND → **Karl Wiegers**
- REQ-POSITIVE → **Requirements Engineering** best practices
- REQ-COMPLETE → **IEEE 830**, **Karl Wiegers**

### Requirements Verifiability
- REQ-TESTABLE → **IEEE 830**, **Karl Wiegers**
- REQ-OBSERVABLE → **IEEE 830**, **Pamela Zave**
- REQ-CRITERIA → **Tom Gilb**, **Mike Cohn** (acceptance criteria)
- REQ-TRACE → **BABOK**, **IEEE 830**

### Problem Domain Focus
- PROB-WHAT → **Michael Jackson** (Problem Frames), **IEEE 830**
- PROB-NO-ARCH → **IEEE 830**, **Separation of Concerns**
- PROB-NO-DESIGN → **IEEE 830**, **Requirements Engineering**
- PROB-NO-TECH → **Requirements best practices**
- PROB-BUSINESS → **BABOK**, **Domain-Driven Design**
- PROB-EXTERNAL → **IEEE 830**, **Alistair Cockburn**

### Consistency
- CONS-TERM → **BABOK** (business vocabulary), **Karl Wiegers**
- CONS-NO-CONFLICT → **IEEE 830**, **Karl Wiegers**
- CONS-FORMAT → **IEEE 830**, **Requirements templates**
- CONS-LEVEL → **Mike Cohn** (story splitting), **SAFe** (epic/feature/story)
- CONS-REFS → **Traceability practices**, **BABOK**
- CONS-RULES → **Business Rules approach**, **BABOK**

### Completeness
- COMP-ACTORS → **Alistair Cockburn**, **BABOK** (stakeholder analysis)
- COMP-SCENARIOS → **Alistair Cockburn**, **Use case best practices**
- COMP-EDGE → **Software testing** literature, **Karl Wiegers**
- COMP-ERROR → **Exception handling** in use cases, **Alistair Cockburn**
- COMP-NFR → **ISO/IEC 25010**, **Lawrence Chung**
- COMP-DATA → **Data modeling**, **Karl Wiegers**
- COMP-CONSTRAINTS → **Karl Wiegers**, **BABOK**
- COMP-ASSUMPTIONS → **Risk management**, **BABOK**

### Anti-Patterns
- ANTI-GOLD → **Steve McConnell**, **PMBOK**
- ANTI-IMPL → **IEEE 830**, **Requirements engineering**
- ANTI-ASSUME → **Technical writing** best practices
- ANTI-FUTURE → **YAGNI principle**, **Agile principles**
- ANTI-JARGON → **Technical writing**, **Plain language**

---

## Additional References

### Books

1. **"User Stories Applied"** by Mike Cohn (2004)
   - User story writing and management

2. **"Writing Effective Use Cases"** by Alistair Cockburn (2000)
   - Use case methodology and best practices

3. **"Software Requirements"** by Karl Wiegers & Joy Beatty (3rd ed., 2013)
   - Comprehensive requirements engineering

4. **"Mastering the Requirements Process"** by Suzanne Robertson & James Robertson (3rd ed., 2012)
   - Requirements discovery and specification

5. **"Agile Software Requirements"** by Dean Leffingwell (2010)
   - Requirements in agile and SAFe

6. **"Succeeding with Agile"** by Mike Cohn (2009)
   - Agile adoption and user stories

7. **"The Persona Lifecycle"** by John Pruitt & Tamara Adlin (2006)
   - Creating and using personas

8. **"Requirements Engineering Fundamentals"** by Klaus Pohl & Chris Rupp (2011)
   - Requirements engineering principles

9. **"Discover to Deliver"** by Ellen Gottesdiener & Mary Gorman (2012)
   - Agile product planning

---

### Standards and Guides

1. **IEEE 830-1998** - Recommended Practice for Software Requirements Specifications
   - Superseded by ISO/IEC/IEEE 29148:2011

2. **ISO/IEC/IEEE 29148:2011** - Systems and software engineering — Life cycle processes — Requirements engineering

3. **BABOK Guide v3** (2015) - Business Analysis Body of Knowledge
   - Published by IIBA (International Institute of Business Analysis)

4. **Agile Extension to BABOK Guide** (2013)
   - Published by IIBA

5. **ISO/IEC 25010:2011** - Systems and software quality requirements and evaluation (SQuaRE)
   - Quality model

---

### Articles and Papers

1. **"INVEST in Good Stories, and SMART Tasks"** by Bill Wake (2003)
   - Original INVEST criteria

2. **"Four Dark Corners of Requirements Engineering"** by Pamela Zave & Michael Jackson (1997)
   - Requirements vs. specifications

3. **"On Non-Functional Requirements"** by Martin Glinz (2007)
   - NFR classification

4. **"Common Requirements Problems, Their Negative Consequences, and Industry Best Practices to Help Solve Them"** by Donald Firesmith (2007)
   - Requirements anti-patterns

---

### Online Resources

1. **Agile Alliance** - https://www.agilealliance.org/
   - User stories, acceptance criteria, agile requirements practices

2. **IIBA (International Institute of Business Analysis)** - https://www.iiba.org/
   - BABOK and business analysis standards

3. **Scaled Agile Framework (SAFe)** - https://scaledagileframework.com/
   - Requirements at scale

4. **IEEE Computer Society** - https://www.computer.org/
   - Standards and requirements engineering resources

---

## Acknowledgments

This skill exists thanks to the requirements engineering and agile communities:

- **Bill Wake** - For INVEST criteria that improved user story quality
- **Mike Cohn** - For making user stories practical and accessible
- **Alistair Cockburn** - For effective use case methodology
- **Karl Wiegers & Joy Beatty** - For comprehensive requirements engineering guidance
- **Dean Leffingwell** - For scaling agile requirements practices
- **Ivar Jacobson** - For use case-driven development
- **IIBA** - For professionalizing business analysis with BABOK
- **IEEE** - For requirements engineering standards
- **Agile Manifesto Authors** - For revolutionizing software development
- **Requirements Engineering Community** - For decades of research and practice

---

## Usage and Attribution

This skill compiles and synthesizes information from the sources listed above. When using insights from this skill:

1. **Credit original authors** when sharing specific concepts (e.g., "INVEST criteria by Bill Wake")
2. **Link to source materials** for deeper learning
3. **Respect licenses** of original works
4. **Cite standards appropriately** (IEEE, ISO, BABOK)
5. **Contribute back** improvements to the requirements community

---

## Disclaimer

This skill is an educational tool based on publicly available resources, standards, and community best practices. It represents established requirements engineering knowledge as of its creation date.

For authoritative information, always refer to:
- **Official standards** (IEEE, ISO/IEC)
- **Original books and papers** by cited authors
- **BABOK Guide** for business analysis
- **Your organization's** requirements standards and templates

Requirements practices continue to evolve with technology and methodology advancements.

---

**Last Updated:** 2024
**Skill Version:** 1.0

*This skill stands on the shoulders of giants in requirements engineering, business analysis, and agile methodology.*
