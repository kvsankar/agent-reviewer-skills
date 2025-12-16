# Agile Requirements & Specification Reviewer

A comprehensive Claude Code skill for reviewing software specifications, user stories, and use cases using agile requirements best practices, business analysis principles, and requirements engineering standards.

## 🎯 What This Skill Reviews

This skill analyzes requirements documents, user stories, and use cases for:

### User Story Quality (INVEST Criteria)

- **I**ndependent - Stories can be developed in any order
- **N**egotiable - Details worked out through conversation
- **V**aluable - Clear business or user value
- **E**stimable - Team can estimate the work
- **S**mall - Fits in one iteration/sprint
- **T**estable - Clear acceptance criteria

### Use Case Completeness

- All actors identified (primary, secondary, stakeholders)
- Preconditions and postconditions specified
- Complete main success scenario
- Alternative flows documented
- Exception flows covered
- Data exchanged specified

### Requirements Quality

- Clear, unambiguous language
- Atomic (one requirement per statement)
- Measurable and verifiable
- Free from vague terms ("fast", "user-friendly")
- Testable with observable outcomes
- Traceable to business needs

### Problem Domain Focus

- Describes WHAT, not HOW
- No architecture or design details
- No technology choices
- Uses business language, not technical jargon
- Focuses on external behavior

### Consistency

- Consistent terminology throughout
- No contradicting requirements
- Consistent format and structure
- Business rules aligned
- Valid cross-references

### Completeness

- All actors and scenarios covered
- Edge cases addressed
- Error conditions specified
- Non-functional requirements included
- Data requirements complete
- Constraints and assumptions documented

## 📋 Example Review Output

````markdown
## Requirements Review: Checkout Flow Specification

### ✅ Strengths
- **USE-FLOW**: Main success scenario is detailed and clear (lines 15-35)
- **STORY-ACCEPT**: Acceptance criteria are specific and testable
- **CONS-TERM**: Consistent use of "customer" and "shopping cart" throughout

### ⚠️ Issues Found

#### INVEST-V: User story lacks clear business value

**Current requirement:**

```text
As a user, I want a checkout button so that I can check out.
```

**Suggested improvement:**

```text
As a customer, I want to review my order details and complete payment quickly,
so that I can finalize my purchase with confidence and minimal friction,
reducing cart abandonment and increasing conversion.
```

**Why this matters:**
The business value explains WHY this matters to users and the business. It helps
prioritize features and ensures the team builds the right thing. "Reducing cart
abandonment" provides measurable business value.

**Best practice:**
Every user story must articulate clear value. The "so that" clause should answer
"Why does this matter?" and guide prioritization decisions.

---

#### REQ-AVOID-VAGUE: Requirement uses unmeasurable terms

**Current requirement:**

```text
The checkout process shall be fast and user-friendly.
```

**Suggested improvement:**

```text
The checkout process shall:
- Complete in 3 steps or fewer from cart to confirmation
- Display each step within 2 seconds of user action
- Show progress indicator (Step 1 of 3, Step 2 of 3, etc.)
- Allow users to navigate back to previous steps without data loss
- Pre-fill known customer information (saved addresses, payment methods)
```

**Why this matters:**
Vague terms like "fast" and "user-friendly" mean different things to different
people and cannot be tested. Specific criteria ensure shared understanding and
enable verification.

**Best practice:**
Replace vague qualitative terms with specific, quantifiable criteria. If you
can't measure it, you can't verify it.

---

#### COMP-ERROR: Missing error condition handling

**Current requirement:**

```text
The user enters payment information and clicks Submit.
The system processes payment and displays confirmation.
```

**Suggested improvement:**

```text
Main Success Scenario:
1. User enters payment information
2. System validates payment information format
3. System processes payment via payment gateway
4. System displays order confirmation with order number

Exception Flow - Invalid Payment Information:
2a. If payment information invalid, display specific error
2b. Highlight invalid fields
2c. Return to step 1

Exception Flow - Payment Declined:
3a. If payment declined, display decline reason
3b. Offer alternative payment method
3c. Return to step 1

Exception Flow - Payment Gateway Timeout:
3a. If payment gateway timeout (>30 seconds), retry up to 2 times
3b. If retries fail, save cart and display error message
3c. Send notification to customer service team
```

**Why this matters:**
Real-world systems must handle errors gracefully. Without specified error handling,
developers make assumptions that may not match user expectations, leading to poor
user experience.

**Best practice:**
For every main flow, identify and document alternative flows (variations) and
exception flows (errors). Use case format makes this explicit.

### 💡 Requirements Wisdom
> "Requirements should focus on WHAT the system must do or a quality it must have,
> not HOW it's built. Stay in the problem domain."
````

## 🚀 Installation

### Personal Installation (Available in All Projects)

Copy the skill to your personal Claude directory:

```bash
# Linux/Mac
cp -r agile-requirements-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "agile-requirements-reviewer" "$env:USERPROFILE\.claude\skills\"
```

### Project Installation (For Teams)

Copy to your project's `.claude/skills/` directory:

```bash
cd your-project
mkdir -p .claude/skills
cp -r /path/to/agile-requirements-reviewer .claude/skills/
```

Then update your project's `.claude/settings.json`:

```json
{
  "skills": [
    {
      "name": "agile-requirements-reviewer",
      "path": "./.claude/skills/agile-requirements-reviewer"
    }
  ]
}
```

## 💡 How to Use

Once installed, the skill activates automatically when you request requirements reviews:

```
"Review these user stories for quality"
"Check this specification for completeness"
"Analyze these requirements for consistency"
"Review this use case for missing scenarios"
"Check if these requirements stay in the problem domain"
"Validate these acceptance criteria"
```

Or invoke directly:

```
"Use the agile requirements reviewer on this specification"
"Apply INVEST criteria to these user stories"
```

## 📚 What You'll Learn

This skill is educational - it doesn't just point out issues, it teaches:

✅ **Why quality matters** - Impact on development and project success
✅ **Concrete examples** - Before/after improvements
✅ **Best practices** - INVEST criteria, use case patterns, clarity guidelines
✅ **Trade-offs** - When to apply rules and when context matters
✅ **Problem vs solution** - Staying in problem domain, avoiding design

## 🎓 Skill Coverage

### 50+ Guidelines Organized by Category

1. **User Story Quality (6)** - INVEST-I, INVEST-N, INVEST-V, INVEST-E, INVEST-S, INVEST-T
2. **User Story Structure (5)** - STORY-FORMAT, STORY-ACCEPT, STORY-VALUE, STORY-PERSONA, STORY-DOD
3. **Use Case Quality (8)** - USE-ACTOR, USE-PRECON, USE-POSTCON, USE-FLOW, USE-ALT, USE-EXCEPT, USE-EXTEND, USE-DATA
4. **Requirements Clarity (7)** - REQ-CLEAR, REQ-ATOMIC, REQ-AVOID-VAGUE, REQ-MEASURABLE, REQ-AVOID-AND, REQ-POSITIVE, REQ-COMPLETE
5. **Requirements Verifiability (4)** - REQ-TESTABLE, REQ-OBSERVABLE, REQ-CRITERIA, REQ-TRACE
6. **Problem Domain Focus (6)** - PROB-WHAT, PROB-NO-ARCH, PROB-NO-DESIGN, PROB-NO-TECH, PROB-BUSINESS, PROB-EXTERNAL
7. **Consistency (6)** - CONS-TERM, CONS-NO-CONFLICT, CONS-FORMAT, CONS-LEVEL, CONS-REFS, CONS-RULES
8. **Completeness (8)** - COMP-ACTORS, COMP-SCENARIOS, COMP-EDGE, COMP-ERROR, COMP-NFR, COMP-DATA, COMP-CONSTRAINTS, COMP-ASSUMPTIONS
9. **Anti-Patterns (5)** - ANTI-GOLD, ANTI-IMPL, ANTI-ASSUME, ANTI-FUTURE, ANTI-JARGON

Each guideline includes:
- Clear principle statement
- Bad/good examples
- Explanation of impact
- Real-world context

## 🔍 When to Use This Skill

**Perfect for:**
- ✅ Reviewing user stories before sprint planning
- ✅ Validating use cases for completeness
- ✅ Checking specifications for clarity and testability
- ✅ Ensuring requirements stay in problem domain
- ✅ Finding inconsistencies and contradictions
- ✅ Identifying missing scenarios and edge cases
- ✅ Improving requirement quality before development
- ✅ Training teams on requirements best practices

**Not ideal for:**
- ❌ Reviewing architectural designs (use architecture skill)
- ❌ Reviewing code (use code review skills)
- ❌ Testing specifications (different from requirements)
- ❌ Requirements that are already high quality

## 🎯 Philosophy

This skill focuses on requirements quality fundamentals:

> **Problem domain, not solution domain** - WHAT not HOW
>
> **Clarity over cleverness** - Simple, unambiguous language
>
> **Testability over completeness** - Better to verify than to be comprehensive
>
> **Value over features** - Why it matters, not just what it does
>
> **Pragmatic, not dogmatic** - Apply guidelines with context

## 🤝 Works Great With

Use alongside other skills for comprehensive quality:
- **Security reviewer** - Security requirements validation
- **Code reviewers** - Ensure implementation matches requirements
- **Functional reviewers** - Check code against specifications

## 📖 Based On

This skill is based on established requirements engineering and agile practices:

- **INVEST Criteria** - Bill Wake's user story quality framework
- **IEEE 830** - Software Requirements Specification standard
- **BABOK** - Business Analysis Body of Knowledge
- **Use Case 2.0** - Ivar Jacobson's use case methodology
- **Mike Cohn** - User story and agile estimation practices
- **Alistair Cockburn** - Use case writing guidance
- **Karl Wiegers** - Software requirements best practices
- **Dean Leffingwell** - SAFe and agile requirements
- **Agile Alliance** - Agile requirements patterns

## 🔧 Customization

The skill uses these tools (configurable in SKILL.md frontmatter):
- `Read` - Reads specification documents
- `Grep` - Searches for patterns
- `Glob` - Finds specification files

## 📊 Review Quality

Each review provides:
- **Mnemonic IDs** - Easy reference (e.g., INVEST-V, USE-FLOW)
- **Structured format** - Strengths, issues, wisdom
- **Examples** - Current vs. suggested requirements
- **Explanations** - Why it matters and impact
- **Actionable feedback** - Clear steps to improve

## 🎓 Common Issues Found

The skill commonly identifies:

**User Story Issues:**
- Missing or weak business value statements
- Stories too large or too vague to estimate
- Missing acceptance criteria
- Generic "user" instead of specific persona

**Use Case Issues:**
- Missing exception flows and error handling
- Incomplete actor identification
- Alternative flows not documented
- Missing preconditions or postconditions

**Requirements Issues:**
- Vague terms ("fast", "user-friendly", "robust")
- Mixing multiple requirements in one statement
- Technology or design details in requirements
- Untestable or unverifiable requirements

**Consistency Issues:**
- Inconsistent terminology (user/customer/client)
- Contradicting requirements
- Different detail levels
- Broken cross-references

**Completeness Issues:**
- Missing error conditions
- Edge cases not addressed
- Non-functional requirements missing
- Assumptions not documented

## 💬 Feedback & Contributions

Found an issue or have a suggestion?
- Open an issue on the repository
- Suggest new guidelines or patterns
- Share your requirements review experiences

## 📄 License

This skill is provided as-is for use with Claude Code. See SOURCES.md for detailed attribution to requirements engineering and agile methodology sources.

---

**Build better software by starting with better requirements.**
