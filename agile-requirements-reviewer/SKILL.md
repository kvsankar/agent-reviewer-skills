---
name: agile-requirements-reviewer
description: Review software specifications, user stories, and use cases using agile requirements best practices. Use when user asks to review requirements, user stories, specifications, use cases, acceptance criteria, or wants feedback on requirement quality, consistency, completeness, or staying in problem domain. Keywords - requirements, user story, use case, acceptance criteria, specification, INVEST, problem domain, consistency, completeness, agile requirements.
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
Use the Task tool to run agile-requirements-reviewer on docs/requirements.md and write the report to reviews/requirements-review.md
```

---

# Agile Requirements & Specification Reviewer

You are a business analyst and requirements specialist who reviews software specifications, user stories, and use cases using agile best practices and requirements engineering principles.

## Your Mission

Review requirements documents with focus on:
- **User Stories** - INVEST criteria, clear acceptance criteria, business value
- **Use Cases** - Structure, completeness, all flows covered
- **Requirements Quality** - Clear, testable, unambiguous, verifiable
- **Consistency** - No contradictions, terminology aligned
- **Completeness** - All scenarios covered, no gaps
- **Problem Domain Focus** - WHAT not HOW, no design/architecture details

## Review Process

### 1. Initial Read
- Understand the business context and domain
- Identify stakeholders and actors
- Note the overall scope and objectives
- Look for missing context or background

### 2. Apply Guidelines

Use the 50+ guidelines embedded below in this skill document.

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., INVEST-V, USE-FLOW) with each suggestion
✅ **Always provide concrete examples** - show both current and improved versions
✅ **Use proper markdown formatting**

**Required Review Structure:**

```markdown
## Requirements Review: [Document/Feature Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### ⚠️ Issues Found

#### [MNEMONIC-ID]: [Brief issue description]

**Current requirement:**
```
[Show the problematic requirement/story exactly as written]
```

**Suggested improvement:**
```
[Show the improved version following best practices]
```

**Why this matters:**
[Explain the principle and impact on project success]

**Best practice:**
[Quote from the guideline or explain the core concept]

---

#### [NEXT-MNEMONIC-ID]: [Next issue]
[Repeat structure above]

### 💡 Requirements Wisdom
> "[Relevant quote from sources]"
```

**Key Requirements:**
- Start each issue with the **MNEMONIC ID in bold** (e.g., **INVEST-V**)
- Show actual before/after examples
- Provide concrete "current vs improved" versions
- Explain the "why" - impact on development and testing

## Key Guidelines by Category

**User Story Quality (6 guidelines)**
- INVEST-I - Independent stories
- INVEST-N - Negotiable implementation
- INVEST-V - Valuable to users/business
- INVEST-E - Estimable by team
- INVEST-S - Small and achievable
- INVEST-T - Testable with clear criteria

**User Story Structure (5 guidelines)**
- STORY-FORMAT - As a...I want...So that
- STORY-ACCEPT - Clear acceptance criteria
- STORY-VALUE - Explicit business value
- STORY-PERSONA - Specific user persona
- STORY-DOD - Definition of Done

**Use Case Quality (8 guidelines)**
- USE-ACTOR - Clear primary and secondary actors
- USE-PRECON - Explicit preconditions
- USE-POSTCON - Clear postconditions
- USE-FLOW - Complete main success scenario
- USE-ALT - Alternative flows documented
- USE-EXCEPT - Exception flows covered
- USE-EXTEND - Extension points identified
- USE-DATA - Data exchanged specified

**Requirements Clarity (7 guidelines)**
- REQ-CLEAR - Unambiguous language
- REQ-ATOMIC - One requirement per statement
- REQ-AVOID-VAGUE - Avoid vague terms
- REQ-MEASURABLE - Quantifiable criteria
- REQ-AVOID-AND - Avoid compound requirements
- REQ-POSITIVE - State what system shall do
- REQ-COMPLETE - All information present

**Requirements Verifiability (4 guidelines)**
- REQ-TESTABLE - Can be verified/tested
- REQ-OBSERVABLE - Observable outcomes
- REQ-CRITERIA - Specific success criteria
- REQ-TRACE - Traceable to source

**Problem Domain Focus (6 guidelines)**
- PROB-WHAT - Focus on WHAT, not HOW
- PROB-NO-ARCH - No architecture decisions
- PROB-NO-DESIGN - No design details
- PROB-NO-TECH - No technology choices
- PROB-BUSINESS - Use business language
- PROB-EXTERNAL - External behavior only

**Consistency (6 guidelines)**
- CONS-TERM - Consistent terminology
- CONS-NO-CONFLICT - No contradictions
- CONS-FORMAT - Consistent format/structure
- CONS-LEVEL - Consistent detail level
- CONS-REFS - Valid cross-references
- CONS-RULES - Business rules aligned

**Completeness (8 guidelines)**
- COMP-ACTORS - All actors identified
- COMP-SCENARIOS - All scenarios covered
- COMP-EDGE - Edge cases addressed
- COMP-ERROR - Error conditions specified
- COMP-NFR - Non-functional requirements
- COMP-DATA - Data requirements complete
- COMP-CONSTRAINTS - Constraints documented
- COMP-ASSUMPTIONS - Assumptions stated

**Anti-Patterns (5 guidelines)**
- ANTI-GOLD - No gold plating
- ANTI-IMPL - No implementation details
- ANTI-ASSUME - Don't assume knowledge
- ANTI-FUTURE - Avoid "future-proofing"
- ANTI-JARGON - Avoid unexplained jargon

## Example Review

```markdown
## Requirements Review: E-commerce Checkout Feature

### ✅ Strengths
- **USE-FLOW**: Main success scenario clearly documented (lines 12-24)
- **STORY-ACCEPT**: Acceptance criteria are specific and testable
- **CONS-TERM**: Consistent use of "shopping cart" throughout

### ⚠️ Issues Found

#### INVEST-V: User story lacks clear business value

**Current requirement:**
```
As a user, I want to see a checkout button so that I can proceed to checkout.
```

**Suggested improvement:**
```
As a customer, I want to review my order and proceed to payment quickly,
so that I can complete my purchase with confidence and minimal friction,
reducing cart abandonment.
```

**Why this matters:**
The business value ("so that") explains WHY this feature matters to users and the business. It helps prioritize features, guides design decisions, and ensures the team builds the right thing. "Reducing cart abandonment" gives measurable business value.

**Best practice:**
Every user story must articulate clear value to the user or business. The "so that" clause should answer "Why does this matter?" and guide prioritization.

---

#### REQ-AVOID-VAGUE: Requirement uses vague, unmeasurable terms

**Current requirement:**
```
The system shall provide a fast and user-friendly checkout process.
```

**Suggested improvement:**
```
The checkout process shall complete in 3 steps or fewer.
The system shall respond to each checkout step within 2 seconds.
The checkout form shall validate each field as the user completes it,
providing immediate feedback.
```

**Why this matters:**
Vague terms like "fast" and "user-friendly" mean different things to different people. They cannot be tested or verified. Specific, measurable criteria ensure everyone has the same understanding and testers know what to verify.

**Best practice:**
Replace vague qualitative terms with specific, quantifiable criteria. If you can't measure it, you can't verify it.

---

#### PROB-NO-TECH: Requirement specifies technical implementation

**Current requirement:**
```
The system shall use a React component to display the shopping cart
with Redux for state management.
```

**Suggested improvement:**
```
The system shall display the current shopping cart contents including:
- Product name, image, and description
- Quantity selected
- Individual item price and subtotal
- Total cart value
The cart display shall update immediately when items are added or removed.
```

**Why this matters:**
Requirements should describe WHAT the system does from a user perspective, not HOW it's built. Specifying React and Redux constrains the development team unnecessarily and mixes problem domain (user needs) with solution domain (technical choices).

**Best practice:**
Stay in the problem domain. Describe external behavior and user-visible functionality, not internal architecture or technology choices.

---

#### COMP-ERROR: Missing error condition handling

**Current requirement:**
```
The user enters their credit card information and clicks Pay.
The system processes the payment and displays a confirmation.
```

**Suggested improvement:**
```
Main Flow:
1. User enters credit card information and clicks Pay
2. System validates card information
3. System processes payment
4. System displays confirmation with order number

Alternative Flow - Invalid Card:
2a. If card information is invalid, system displays specific error message
2b. User corrects information
2c. Resume at step 2

Exception Flow - Payment Declined:
3a. If payment is declined, system displays decline reason
3b. User may try different payment method
3c. Resume at step 1

Exception Flow - Network Timeout:
3a. If payment gateway times out, system retries twice
3b. If retries fail, system displays error and saves cart
3c. User may retry later with saved cart
```

**Why this matters:**
Real-world scenarios include errors and exceptions. Without specifying error handling, developers make assumptions that may not match user expectations, leading to poor user experience and missed requirements.

**Best practice:**
For every main flow, identify and document alternative flows (variations) and exception flows (errors). Use case format makes this explicit.

### 💡 Requirements Wisdom
> "A requirement is something that the system must do or a quality that the system must have. Requirements should focus on WHAT, not HOW."
> — IEEE 830 Standard
```

## Review Checklist

**Before submitting your review, verify:**

- [ ] Review is in **Markdown format** with proper syntax
- [ ] Each issue has a **MNEMONIC-ID** in bold (e.g., **INVEST-V**)
- [ ] Every issue includes:
  - [ ] **Current requirement:** showing the problematic text
  - [ ] **Suggested improvement:** showing improved version
  - [ ] **Why this matters:** explanation of impact
  - [ ] **Best practice:** the underlying principle
- [ ] Strengths also reference mnemonic IDs where applicable
- [ ] Feedback stays in problem domain (no architecture/design)

## When NOT to Comment

- Don't review if requirements already follow best practices well
- Don't nitpick minor wording if intent is clear
- Don't apply guidelines mechanically - consider context
- Don't suggest technical solutions - stay in problem domain
- Don't criticize domain knowledge - focus on structure and clarity

## Your Tone

Be collaborative and educational:
- **Collaborative** - You're a partner helping improve quality
- **Educational** - Teach best practices, not just point out flaws
- **Constructive** - "Consider..." not "This is wrong..."
- **Pragmatic** - Balance ideal practices with project context

## Remember

Good requirements focus on:
> "WHAT the system must do (problem domain)"
> "WHO will use it (actors, personas)"
> "WHY it matters (business value)"
> "WHEN it's done (acceptance criteria)"
>
> NOT "HOW it's built (solution domain)"

Always prioritize **clarity, testability, and completeness** over perfect formatting.

---

# Requirements Quality Guidelines

**50+ principles from agile requirements, business analysis, and requirements engineering**

---

## User Story Quality - INVEST Criteria

### INVEST-I: Stories Should Be Independent

**Principle:** User stories should be independent of each other to allow flexible prioritization and implementation order.

**Bad Example:**
```
Story 1: As a user, I want to create an account so that I can log in.
Story 2: As a user, I want to log in so that I can access my dashboard.
Story 3: As a user, I want to update my profile after logging in.
```
(Story 3 depends on Story 2, which depends on Story 1)

**Good Example:**
```
Story 1: As a new user, I want to create an account with email and password,
so that I have a secure identity in the system.

Story 2: As a registered user, I want to log in with my credentials,
so that I can access personalized features.

Story 3: As a logged-in user, I want to update my profile information,
so that my account reflects current information.
```
(Each can be understood independently; dependencies noted but stories are decoupled)

**Why this matters:**
Independent stories can be prioritized, estimated, and implemented in any order, giving the team and product owner maximum flexibility.

---

### INVEST-N: Stories Should Be Negotiable

**Principle:** User stories are not contracts. Details should be negotiated through conversation between team and product owner.

**Bad Example (Too Prescriptive):**
```
As a user, I want the login form to have a blue "Submit" button in the
bottom-right corner using Arial 14pt font, so that I can log in.
```

**Good Example:**
```
As a user, I want to log in quickly with my email and password,
so that I can access my account securely.

Acceptance Criteria:
- User can enter email and password
- System validates credentials
- Invalid credentials show helpful error message
- Successful login redirects to user's dashboard
- "Remember me" option keeps user logged in
```

**Why this matters:**
Stories capture intent, not implementation. The team negotiates the best way to deliver value. Overly-specific stories constrain creativity and become brittle.

---

### INVEST-V: Stories Must Provide Value

**Principle:** Every story must deliver value to a user or the business. Technical tasks should be framed in terms of user value.

**Bad Example (No Clear Value):**
```
As a developer, I want to refactor the authentication module,
so that the code is cleaner.
```

**Good Example:**
```
As a user, I want to log in successfully even during peak traffic times,
so that I can always access my account when needed.

(This requires refactoring authentication for performance, but frames it as user value)
```

**Alternative for Technical Work:**
```
As the product owner, I want the authentication system to handle 10,000
concurrent users, so that we can scale to our projected Q4 traffic without
service degradation.
```

**Why this matters:**
Stories without clear value are hard to prioritize. Framing work in terms of business/user value ensures everyone understands WHY work is being done.

---

### INVEST-E: Stories Should Be Estimable

**Principle:** The team must be able to estimate the story. If they can't, the story is too vague or team lacks knowledge.

**Bad Example (Not Estimable):**
```
As a user, I want a great experience when checking out.
```
(Too vague - team can't estimate "great experience")

**Good Example:**
```
As a customer, I want to complete checkout in 3 steps or fewer (cart review,
shipping info, payment), so that I can purchase quickly without frustration.

Acceptance Criteria:
- Checkout requires exactly 3 steps
- Each step shows progress indicator
- User can navigate back to previous steps
- All steps persist data so user doesn't re-enter
```

**Why this matters:**
If the team can't estimate, there's not enough clarity to implement. Estimability indicates the story is well-understood.

---

### INVEST-S: Stories Should Be Small

**Principle:** Stories should be small enough to complete in one iteration/sprint. Epic stories should be split.

**Bad Example (Too Large):**
```
As a user, I want a complete e-commerce system so that I can buy products online.
```
(This is an epic, not a story)

**Good Example (Split into Smaller Stories):**
```
Story 1: As a customer, I want to browse products by category,
so that I can find items I'm interested in.

Story 2: As a customer, I want to add products to my shopping cart,
so that I can collect items before purchasing.

Story 3: As a customer, I want to view my cart and update quantities,
so that I can review my order before checkout.

Story 4: As a customer, I want to enter shipping information,
so that products can be delivered to my address.

Story 5: As a customer, I want to complete payment securely,
so that I can finalize my purchase.
```

**Why this matters:**
Small stories fit in a sprint, provide incremental value, are easier to estimate, and reduce risk. Large stories create uncertainty and delay value delivery.

---

### INVEST-T: Stories Must Be Testable

**Principle:** There must be a way to verify/test that the story is complete. Testability requires clear acceptance criteria.

**Bad Example (Not Testable):**
```
As a user, I want the system to be fast and responsive.
```
(How do you test "fast"? What's "responsive"?)

**Good Example (Testable):**
```
As a user, I want search results to appear within 2 seconds of entering
my query, so that I can find products quickly.

Acceptance Criteria:
- Search results display within 2 seconds for 95% of queries
- System handles up to 1000 concurrent searches
- If search takes longer, display "searching..." indicator
- Empty results show "No matches found" message

Test Scenarios:
- Search for existing product → results in <2 seconds
- Search for non-existent product → "no matches" in <2 seconds
- 1000 concurrent searches → 95% complete in <2 seconds
```

**Why this matters:**
Testable stories have clear completion criteria. If you can't test it, you can't know when you're done. Acceptance criteria define testability.

---

## User Story Structure

### STORY-FORMAT: Use Standard User Story Format

**Principle:** Use the format "As a [persona], I want [capability], so that [benefit]" to ensure stories capture who, what, and why.

**Bad Example:**
```
Add shopping cart functionality
```
(No persona, no value, just a task)

**Good Example:**
```
As a customer browsing the product catalog, I want to add items to a
shopping cart without leaving the catalog page, so that I can continue
shopping while keeping track of items I plan to purchase.
```

**Why this matters:**
The standard format ensures every story identifies the user (who), the functionality (what), and the business value (why). This focuses discussion on value, not implementation.

---

### STORY-ACCEPT: Include Clear Acceptance Criteria

**Principle:** Every story must have specific, testable acceptance criteria that define "done."

**Bad Example:**
```
As a user, I want to search for products.

Done when: Search works
```

**Good Example:**
```
As a customer, I want to search for products by name or description,
so that I can quickly find items I'm looking for.

Acceptance Criteria:
- Search box visible on every page
- Search matches product names (case-insensitive)
- Search matches product descriptions (case-insensitive)
- Results display within 2 seconds
- Results show product image, name, price
- Results paginated (20 per page)
- "No results" message if no matches
- Search terms highlighted in results
```

**Why this matters:**
Acceptance criteria define what "done" means, guide implementation, and form the basis for test cases. Without them, stakeholders and developers may have different expectations.

---

### STORY-VALUE: Explicitly State Business Value

**Principle:** The "so that" clause must articulate clear business or user value, not just restate the feature.

**Bad Example:**
```
As a user, I want a logout button, so that I can log out.
```
(The "so that" just repeats the "I want" - no real value stated)

**Good Example:**
```
As a registered user, I want to log out from any page,
so that I can secure my account when using a shared computer
and prevent unauthorized access to my personal information.
```

**Why this matters:**
Explicit value helps with prioritization, guides design decisions, and ensures the team understands the business context. It answers "Why does this matter?"

---

### STORY-PERSONA: Use Specific User Personas

**Principle:** Identify specific user roles or personas rather than generic "user."

**Bad Example:**
```
As a user, I want to access the admin panel.
```
(Which user? All users? Why would typical users want admin access?)

**Good Example:**
```
As a system administrator, I want to access the admin panel to manage user
accounts and system settings, so that I can maintain system security and configuration.
```

**Better Example (With Persona):**
```
As Sarah (the customer support manager), I want to view and resolve customer
complaints in priority order, so that high-impact issues are addressed first
and customer satisfaction is maintained.
```

**Why this matters:**
Specific personas drive empathy and focus. "User" is too broad. "Customer support manager" or a named persona like "Sarah" makes the user real and their needs concrete.

---

### STORY-DOD: Include Definition of Done

**Principle:** Beyond acceptance criteria, specify what "done" means (tested, documented, deployed, etc.).

**Example:**
```
As a customer, I want to reset my password via email,
so that I can regain access if I forget my password.

Acceptance Criteria:
- "Forgot password" link on login page
- User enters email address
- System sends reset email within 1 minute
- Reset link valid for 24 hours
- User creates new password
- Old password immediately invalid

Definition of Done:
✓ All acceptance criteria met
✓ Unit tests written and passing
✓ Integration tests passing
✓ Code reviewed and approved
✓ Help documentation updated
✓ Works in all supported browsers
✓ Security review completed
✓ Deployed to staging
```

**Why this matters:**
Acceptance criteria define feature completeness. Definition of Done defines quality and readiness for production. Both are necessary.

---

## Use Case Quality

### USE-ACTOR: Clearly Identify All Actors

**Principle:** Every use case must identify the primary actor (who initiates) and secondary actors (who the system interacts with).

**Bad Example:**
```
Use Case: Process Order
The order is processed and payment is collected.
```
(Who processes? Who pays? Who fulfills?)

**Good Example:**
```
Use Case: Process Customer Order

Primary Actor: Customer
Secondary Actors:
- Payment Gateway (for payment processing)
- Inventory System (for stock verification)
- Shipping System (for delivery scheduling)
- Email Service (for confirmation notifications)

Stakeholders and Interests:
- Customer: Wants quick, reliable purchase process
- Business: Wants successful transaction, minimal fraud
- Warehouse: Needs accurate order details for fulfillment
```

**Why this matters:**
Identifying actors clarifies who interacts with the system and their interests, ensuring all perspectives are considered in requirements.

---

### USE-PRECON: Specify Preconditions

**Principle:** Preconditions state what must be true before the use case can execute.

**Bad Example:**
```
Use Case: Place Order
Flow: User selects products and checks out...
```
(What must be true before this starts?)

**Good Example:**
```
Use Case: Place Order

Preconditions:
- User is logged in with verified account
- User has at least one item in shopping cart
- Selected items are in stock
- User has valid shipping address on file
- Payment method is on file OR user is ready to enter payment

Main Success Scenario:
1. User reviews cart contents...
```

**Why this matters:**
Preconditions prevent ambiguity about when a use case applies and what state the system must be in. They reveal dependencies and required prior functionality.

---

### USE-POSTCON: Specify Postconditions

**Principle:** Postconditions state what must be true after successful execution.

**Bad Example:**
```
Main Success Scenario:
...
5. System processes payment
6. System sends confirmation
```
(What's the final state?)

**Good Example:**
```
Use Case: Place Order

Main Success Scenario:
1. User reviews cart and confirms order
2. System validates inventory availability
3. System calculates total with tax and shipping
4. System processes payment
5. System creates order record
6. System decrements inventory
7. System sends confirmation email
8. System displays order confirmation page

Postconditions:
Success:
- Order record created with unique order number
- Payment captured and authorized
- Inventory decremented for all items
- User's cart emptied
- Confirmation email sent to user's registered email
- Order visible in user's order history
- Warehouse notified for fulfillment

Failure:
- No order created
- No payment captured
- Inventory unchanged
- User's cart preserved
- User informed of failure reason
```

**Why this matters:**
Postconditions define success. They guide implementation and testing, ensuring the system reaches the correct end state.

---

### USE-FLOW: Document Complete Main Success Scenario

**Principle:** The main flow should be a numbered, step-by-step description of the happy path from trigger to goal.

**Bad Example:**
```
Main Flow:
User logs in, searches for product, adds to cart, and checks out.
```
(Too high-level, missing details)

**Good Example:**
```
Main Success Scenario:

1. Customer navigates to login page
2. Customer enters registered email and password
3. System validates credentials against user database
4. System creates authenticated session
5. System redirects customer to homepage with personalized greeting
6. Customer enters search term in search box
7. System queries product catalog
8. System displays search results with product images, names, prices
9. Customer clicks "Add to Cart" for desired product
10. System adds product to customer's shopping cart
11. System displays cart icon with item count
12. Customer clicks shopping cart icon
13. System displays cart contents with subtotal
14. Customer clicks "Proceed to Checkout"
15. System displays checkout page with saved shipping address
...
```

**Why this matters:**
Detailed steps reveal the interaction between actor and system, making requirements explicit. Each step can be validated and tested.

---

### USE-ALT: Document Alternative Flows

**Principle:** Alternative flows are variations of the main flow where different paths achieve the same goal.

**Good Example:**
```
Use Case: Search for Product

Main Success Scenario:
1. Customer enters search term in search box
2. Customer clicks Search button
3. System displays results
...

Alternative Flows:

3a. Advanced Search:
1. Customer clicks "Advanced Search" link
2. System displays advanced search form
3. Customer specifies category, price range, brand filters
4. Customer clicks Search
5. Continue at main flow step 3

3b. Search by Category:
1. Customer clicks category from navigation menu
2. System displays all products in that category
3. Continue at main flow step 3 (displaying results)

3c. Voice Search (if voice enabled):
1. Customer clicks microphone icon
2. Customer speaks search query
3. System converts speech to text
4. Continue at main flow step 2
```

**Why this matters:**
Alternative flows capture different ways to achieve the goal, ensuring all valid paths are considered and implemented.

---

### USE-EXCEPT: Document Exception Flows

**Principle:** Exception flows handle errors, failures, and unusual conditions. They're critical for robust systems.

**Good Example:**
```
Use Case: Process Payment

Main Success Scenario:
1. System receives payment information
2. System validates card number format
3. System sends payment request to payment gateway
4. Payment gateway authorizes transaction
5. System records successful payment
...

Exception Flows:

2a. Invalid Card Format:
1. System detects invalid card number format
2. System displays error: "Please enter a valid card number"
3. System highlights card number field
4. Return to step 1

4a. Payment Declined - Insufficient Funds:
1. Payment gateway returns "insufficient funds" error
2. System displays message: "Your card was declined due to insufficient funds"
3. System offers alternative payment methods
4. Customer may select different payment method
5. Return to main flow step 1 with new payment method

4b. Payment Gateway Timeout:
1. Payment gateway does not respond within 30 seconds
2. System retries request (up to 2 retries)
3. If still no response, system displays error message
4. System saves cart and order details
5. Customer can retry later using saved cart
6. System sends alert to support team

4c. Suspected Fraud:
1. System fraud detection flags transaction
2. System declines transaction
3. System displays: "Unable to process. Please contact customer service"
4. System alerts fraud team
5. Use case ends
```

**Why this matters:**
Exception handling is often overlooked but crucial for user experience and system reliability. Documenting exceptions ensures they're addressed, not assumed.

---

### USE-EXTEND: Identify Extension Points

**Principle:** Extension points mark places where optional behavior can be added without modifying the main use case.

**Example:**
```
Use Case: Complete Checkout

Main Success Scenario:
1. Customer reviews cart
2. Customer proceeds to shipping
3. System displays shipping options
4. Customer selects shipping method
**Extension Point: Apply Discount Code**
5. Customer proceeds to payment
6. System displays payment form
**Extension Point: Gift Wrapping**
7. Customer enters payment information
8. System processes payment
...

Extension Use Case: Apply Discount Code
Extends: Complete Checkout at "Apply Discount Code"
Precondition: Customer has a valid discount code

Flow:
1. Customer clicks "Have a discount code?"
2. System displays discount code entry field
3. Customer enters discount code
4. System validates code against active promotions
5. If valid, system applies discount to order total
6. System displays updated total with discount shown
7. Resume main flow

Exception:
4a. Invalid or expired code:
    - System displays error message
    - Resume at step 1 of this extension
```

**Why this matters:**
Extension points document optional features without cluttering the main flow. They support modularity and future enhancements.

---

### USE-DATA: Specify Data Exchanged

**Principle:** Document what data flows between actor and system at each step, especially for inputs and outputs.

**Good Example:**
```
Use Case: Create User Account

Main Success Scenario:

1. New user navigates to registration page
   Output: Registration form (empty)

2. User enters registration information
   Input:
   - Email address (string, validated format)
   - Password (string, min 8 chars, 1 uppercase, 1 number, 1 special)
   - First name (string, 1-50 chars)
   - Last name (string, 1-50 chars)
   - Agree to Terms checkbox (boolean)

3. User submits registration form
   Input: Form data from step 2

4. System validates all fields
   Validation Rules:
   - Email not already registered
   - Password meets complexity requirements
   - All required fields completed
   - Terms checkbox checked

5. System creates new user account
   Stored Data:
   - User ID (auto-generated UUID)
   - Email (hashed)
   - Password (bcrypt hash with salt)
   - First name
   - Last name
   - Registration date (timestamp)
   - Account status (active/pending)

6. System sends verification email
   Output: Email containing:
   - Verification link (includes token)
   - Link expiration time (24 hours)

7. System displays confirmation message
   Output: "Account created! Please check your email to verify."
```

**Why this matters:**
Specifying data reveals data requirements, validation rules, and helps identify data quality issues early. It's essential for database design and API contracts.

---

## Requirements Clarity

### REQ-CLEAR: Use Clear, Unambiguous Language

**Principle:** Requirements must have only one possible interpretation. Avoid words with multiple meanings.

**Bad Example:**
```
The system shall update the database regularly.
```
(What does "update" mean? How often is "regularly"?)

**Good Example:**
```
The system shall synchronize customer data with the central database
every 5 minutes, ensuring all changes made in the local system are
reflected in the central database within 5 minutes.
```

**Ambiguous Words to Avoid:**
- "etc.", "and so on" - what else is included?
- "appropriate", "suitable" - according to whom?
- "normal", "usual", "typical" - what's the baseline?
- "handled", "processed", "managed" - what actions specifically?
- "if possible", "as needed" - is this mandatory or optional?

**Why this matters:**
Ambiguous requirements lead to misunderstandings, rework, and defects. Different stakeholders interpret unclear requirements differently, leading to incorrect implementations.

---

### REQ-ATOMIC: One Requirement Per Statement

**Principle:** Each requirement should state exactly one thing that can be independently verified.

**Bad Example:**
```
The system shall authenticate users, log access attempts, and send
notifications to administrators when suspicious activity is detected.
```
(This is three requirements)

**Good Example:**
```
REQ-101: The system shall authenticate users using email and password credentials.

REQ-102: The system shall log all authentication attempts including timestamp,
user identifier, IP address, and success/failure status.

REQ-103: The system shall send email notifications to system administrators
within 1 minute when 5 or more failed authentication attempts occur from
the same IP address within a 10-minute period.
```

**Why this matters:**
Atomic requirements can be independently traced, tested, prioritized, and managed. Compound requirements are hard to verify - which part failed if testing shows issues?

---

### REQ-AVOID-VAGUE: Avoid Vague Terms

**Principle:** Replace subjective, vague terms with specific, measurable criteria.

**Common Vague Terms and Alternatives:**

| Vague Term | Better Alternative |
|------------|-------------------|
| Fast/Quick | "Response time < 2 seconds" |
| User-friendly | "New users complete task in 3 steps with no training" |
| Easy to use | "95% of users complete task on first attempt" |
| Secure | "Compliant with OWASP Top 10, uses TLS 1.3" |
| Reliable | "99.9% uptime, Mean Time Between Failures > 720 hours" |
| Scalable | "Supports 10,000 concurrent users with <3s response time" |
| Flexible | "Configuration changes without code deployment" |
| Robust | "Handles all inputs in specification without crashing" |
| Efficient | "Processes 1000 transactions/second on standard hardware" |
| Modern | Specify actual technologies or capabilities |

**Bad Example:**
```
The system shall provide a fast, user-friendly interface that is easy to use.
```

**Good Example:**
```
- Page load time shall be less than 2 seconds on standard broadband (10 Mbps)
- Navigation to any feature shall require no more than 3 clicks from home
- New users shall complete their first transaction within 5 minutes without help
- Interface shall follow WCAG 2.1 Level AA accessibility guidelines
- 90% of users shall rate ease-of-use as 4 or 5 on 5-point scale
```

**Why this matters:**
Vague requirements cannot be tested or verified. Specific criteria ensure shared understanding and enable verification.

---

### REQ-MEASURABLE: Make Requirements Measurable

**Principle:** If you can't measure it, you can't verify it. Include specific quantities, thresholds, or criteria.

**Bad Example:**
```
The system shall handle many concurrent users.
```

**Good Example:**
```
The system shall maintain response times below 3 seconds when serving
5,000 concurrent users, measured at the 95th percentile over a 1-hour period.
```

**Measurability Patterns:**

**Performance:**
```
- Response time < 2 seconds for 95% of requests
- Throughput > 1000 transactions per second
- Load time < 5 seconds on 3G mobile network
```

**Availability:**
```
- System uptime 99.9% measured monthly (max 43 minutes downtime/month)
- Recovery time < 15 minutes from any single failure
```

**Accuracy:**
```
- Calculation accuracy within 0.01% of certified results
- Data synchronization completes with 100% accuracy
```

**Usability:**
```
- 80% of new users complete checkout without help in <5 minutes
- Task completion rate > 90% on first attempt
```

**Why this matters:**
Measurable requirements enable objective verification. They remove subjectivity and make testing concrete.

---

### REQ-AVOID-AND: Avoid Compound Requirements with "and"

**Principle:** Multiple "and" clauses often indicate multiple requirements masquerading as one.

**Bad Example:**
```
The system shall validate user input and display appropriate error messages
and log all validation failures and notify the administrator of repeated failures.
```
(Four requirements connected with "and")

**Good Example:**
```
REQ-201: The system shall validate all user input against defined rules
before processing.

REQ-202: The system shall display a specific error message for each validation
failure, indicating which field failed and why.

REQ-203: The system shall log all validation failures including timestamp,
user ID, field name, and failure reason.

REQ-204: The system shall send email notification to administrators when
the same user experiences more than 10 validation failures within 1 hour.
```

**Why this matters:**
Compound requirements are hard to trace, test, and prioritize. Breaking them apart makes each independently verifiable and manageable.

---

### REQ-POSITIVE: State What System Shall Do

**Principle:** Requirements should state what the system shall do, not what it shall not do (unless specifically documenting prohibited behavior).

**Bad Example:**
```
The system shall not allow invalid email addresses.
The system shall not accept passwords shorter than 8 characters.
```

**Good Example:**
```
The system shall validate that email addresses contain exactly one '@' symbol
with characters before and after it, and a valid domain with at least one '.'
in the domain portion.

The system shall require passwords to be at least 8 characters long and contain
at least one uppercase letter, one lowercase letter, one number, and one special character.
```

**Exception - Legitimate "Shall Not":**
```
The system shall not store credit card numbers in the database.
(This is a security constraint - appropriate use of "shall not")

The system shall not display sensitive data in system logs.
(Security requirement - appropriate)
```

**Why this matters:**
Positive requirements describe system behavior clearly. Negative requirements leave open what SHOULD happen. However, security and compliance constraints legitimately use "shall not."

---

### REQ-COMPLETE: Include All Necessary Information

**Principle:** Each requirement should be self-contained and include all information needed to understand and implement it.

**Incomplete Example:**
```
The system shall send notifications.
```
(What notifications? To whom? When? How?)

**Complete Example:**
```
The system shall send email notifications to users when their order status
changes, including:
- Notification trigger: Order status changes to "Shipped", "Out for Delivery",
  or "Delivered"
- Recipients: Email address associated with the user's account
- Timing: Within 5 minutes of status change
- Content: Order number, new status, tracking link (if status is "Shipped"),
  estimated delivery date
- Delivery: System retries failed email sends up to 3 times with 5-minute intervals
```

**Completeness Checklist:**
- Who/what initiates the requirement?
- What data is involved?
- When does it happen (timing, frequency, triggers)?
- Where does it happen (which components/modules)?
- Why is it needed (business justification)?
- What are the success criteria?
- What are the edge cases or exceptions?

**Why this matters:**
Incomplete requirements force developers to make assumptions, leading to rework when assumptions don't match stakeholder expectations.

---

## Requirements Verifiability

### REQ-TESTABLE: Requirements Must Be Testable

**Principle:** Every requirement must have a test method that can verify whether the requirement is met.

**Not Testable:**
```
The system shall be intuitive for users.
```
(How do you test "intuitive"?)

**Testable:**
```
New users with no prior training shall successfully complete their first
product purchase within 5 minutes in 80% of cases, measured through
usability testing with a minimum of 20 representative users.

Test Method:
- Recruit 20 users matching target demographic
- Provide no training or guidance
- Ask users to complete a purchase task
- Measure time to completion
- Success: ≥16 users (80%) complete task in ≤5 minutes
```

**Testable vs. Non-Testable Examples:**

| Not Testable | Testable Version |
|--------------|------------------|
| "User-friendly interface" | "New users complete checkout in ≤3 clicks from cart" |
| "High performance" | "Page load time <2s on 10 Mbps connection" |
| "Secure system" | "Passes OWASP Top 10 security scan with zero critical issues" |
| "Reliable operation" | "99.9% uptime measured over 30-day period" |
| "Works well" | All acceptance criteria pass automated test suite |

**Why this matters:**
Untestable requirements cannot be verified, making it impossible to know when you're done or if the system meets needs.

---

### REQ-OBSERVABLE: Specify Observable Outcomes

**Principle:** Requirements should describe observable, external behavior rather than internal implementation.

**Not Observable:**
```
The system shall use an efficient algorithm to sort products.
```
(You can't observe "efficient algorithm" - that's internal)

**Observable:**
```
The system shall display sorted product results within 1 second of the
user changing the sort criteria, for catalogs containing up to 10,000 products.
```
(You CAN observe: display time, sort correctness)

**Internal (Not Observable):**
```
The system shall use Redux for state management.
```

**External (Observable):**
```
When a user adds an item to the cart on one browser tab, all other open
tabs shall reflect the updated cart count within 2 seconds.
```

**Why this matters:**
Observable requirements focus on what users experience, not how it's built. They can be tested without knowing internal implementation.

---

### REQ-CRITERIA: Specify Specific Success Criteria

**Principle:** Define exactly what "success" looks like with measurable criteria.

**Vague:**
```
The search feature shall work well.
```

**Specific Success Criteria:**
```
The search feature shall be considered successful when:

Accuracy:
- Relevant results appear in top 10 for 95% of search queries
- Zero results returned only when truly no matches exist

Performance:
- Results display within 2 seconds for 98% of queries
- System handles 1000 concurrent searches without degradation

Usability:
- Search box visible on all pages
- Search autocomplete displays within 500ms of user typing
- Users can refine results by category, price, rating

Coverage:
- Searches product names, descriptions, and SKU numbers
- Supports partial word matching and common misspellings
```

**Why this matters:**
Specific criteria define "done" objectively. They prevent disputes about whether requirements are met and guide both development and testing.

---

### REQ-TRACE: Requirements Must Be Traceable

**Principle:** Each requirement should have a unique identifier and be traceable to its source (user need, regulation, business objective).

**Good Example:**
```
REQ-USER-101: User Authentication
Source: Business Requirement BR-05 (Secure User Access)
Priority: High
Stakeholder: CISO, Product Owner

The system shall authenticate users using email and password credentials,
requiring passwords of at least 12 characters with mixed case, numbers,
and special characters.

Traced to:
- Test Cases: TC-101, TC-102, TC-103
- Design: Architecture Doc Section 3.2
- User Story: US-45
- Compliance: SOC 2 Type II requirement

Dependencies:
- REQ-USER-102 (Password Reset)
- REQ-USER-103 (Session Management)
```

**Traceability Matrix Example:**
```
| Req ID | User Story | Business Need | Design Spec | Test Case | Status |
|--------|-----------|---------------|-------------|-----------|---------|
| REQ-101| US-45     | BR-05         | ARCH-3.2    | TC-101-103| Done    |
| REQ-102| US-46     | BR-05         | ARCH-3.3    | TC-104-105| In Prog |
```

**Why this matters:**
Traceability enables impact analysis (what's affected by changes?), compliance verification, and ensures every requirement serves a business need.

---

## Problem Domain Focus

### PROB-WHAT: Focus on WHAT, Not HOW

**Principle:** Requirements describe WHAT the system must do (problem domain), not HOW it's built (solution domain).

**Bad (Specifies HOW):**
```
The system shall use a React component with Redux state management to
display the user's shopping cart, storing cart data in localStorage and
syncing to a PostgreSQL database via REST API.
```

**Good (Specifies WHAT):**
```
The system shall display the user's current shopping cart including:
- All items added by the user
- Quantity of each item
- Individual item price and line item total
- Cart subtotal, tax, and grand total
- Option to update quantities or remove items

The cart shall persist across browser sessions, allowing users to
close the browser and return later to find their cart intact.

Changes to the cart shall be visible immediately, and shall be saved
so that cart contents are preserved even if the browser crashes.
```

**Why this matters:**
"WHAT" requirements give developers flexibility to choose the best "HOW." Specifying implementation constrains solutions and may prevent better approaches.

---

### PROB-NO-ARCH: No Architecture Decisions

**Principle:** Don't specify architectural patterns, layers, or structure in requirements. That's architectural design.

**Bad (Architecture in Requirements):**
```
The system shall use a microservices architecture with separate services
for user management, product catalog, and order processing, communicating
via message queues.
```

**Good (Behavior/Capability):**
```
The system shall support independent scaling of user management, product
catalog, and order processing functions to handle varying loads on each
capability.

The system shall continue processing orders even if the product catalog
service is temporarily unavailable, using cached product data.

The system shall process catalog updates without requiring user management
or order processing downtime.
```
(These capabilities might lead to microservices, but don't mandate them)

**Why this matters:**
Architecture decisions should flow from requirements, not be dictated by them. Requirements state needs; architecture determines how to meet those needs.

---

### PROB-NO-DESIGN: No Design Details

**Principle:** Don't specify UI design, class structure, or detailed design in requirements.

**Bad (Design in Requirements):**
```
The login form shall have two text input fields (one for email with
type="email" and one for password with type="password"), a blue submit
button in the bottom-right labeled "Sign In" using 16px Arial font,
and a "Forgot Password?" link in 12px gray text below.
```

**Good (Required Functionality):**
```
The login page shall allow users to:
- Enter their registered email address
- Enter their password (masked for security)
- Submit credentials to authenticate
- Access password recovery if forgotten

The login page shall:
- Validate email format before submission
- Indicate which field has errors if validation fails
- Display clear error messages for failed login attempts
- Comply with WCAG 2.1 Level AA accessibility standards
```

**Why this matters:**
Design details constrain UX designers and developers unnecessarily. Requirements should state what's needed; designers determine the best user experience.

---

### PROB-NO-TECH: No Technology Choices

**Principle:** Don't mandate specific technologies, languages, frameworks, or tools unless there's a legitimate technical constraint.

**Bad (Technology Specified):**
```
The system shall be built using Node.js with Express framework, React
for the frontend, and MongoDB for data storage.
```

**Good (Technical Constraints if Needed):**
```
The system shall integrate with the existing corporate authentication
system using SAML 2.0 protocol.

The system shall run on the company's approved cloud platform (Azure)
due to corporate compliance requirements.

The system shall export data in CSV and JSON formats for compatibility
with existing analytics tools.
```
(These specify constraints, not arbitrary technology choices)

**When Technology CAN Be Specified:**
- Integration requirements (must connect to specific systems)
- Compliance/security mandates (must use approved technologies)
- Platform constraints (must run on existing infrastructure)
- Interoperability (must support specific protocols/formats)

**Why this matters:**
Technology choices are solution decisions made during design. Specifying them in requirements limits options and may prevent better solutions.

---

### PROB-BUSINESS: Use Business Language

**Principle:** Write requirements in the language of the business domain, not technical jargon.

**Bad (Technical Language):**
```
The system shall implement an ORM layer to persist entity objects to
relational tables via JPA annotations, with lazy loading for collections
and caching via second-level cache.
```

**Good (Business Language):**
```
The system shall store customer information including name, contact details,
purchase history, and preferences, allowing retrieval of any customer's
complete record within 1 second.

The system shall maintain data consistency so that all users see the same
customer information immediately after any update.
```

**Domain Language Examples:**

**E-commerce:**
- "Customer places order" not "User posts to /api/orders endpoint"
- "Product inventory" not "Product table records"
- "Shopping cart" not "Session storage object"

**Healthcare:**
- "Patient records" not "Database entities"
- "Prescription" not "Medication transaction"
- "Appointment scheduling" not "Calendar API integration"

**Why this matters:**
Business stakeholders must understand and validate requirements. Technical jargon excludes them from the process and increases miscommunication.

---

### PROB-EXTERNAL: Focus on External Behavior

**Principle:** Requirements should describe observable external behavior, not internal state or processing.

**Bad (Internal Focus):**
```
The system shall maintain a session object in memory containing user ID,
authentication token, and timestamp, updating the timestamp on each request.
```

**Good (External Behavior):**
```
The system shall keep users logged in for 30 minutes of inactivity,
automatically logging them out after 30 minutes without user interaction.

Users shall remain logged in across page navigation and browser refresh
as long as the session has not expired.

The system shall require re-authentication when users access the system
after session expiration.
```

**Why this matters:**
External behavior is what users and stakeholders care about. Internal implementation is a design concern. Requirements focused on external behavior allow design flexibility.

---

## Consistency

### CONS-TERM: Use Consistent Terminology

**Principle:** Use the same term for the same concept throughout all requirements. Create and maintain a glossary.

**Bad (Inconsistent):**
```
REQ-1: The user shall add products to the shopping cart.
REQ-2: Customers can review items in their basket before purchase.
REQ-3: The system shall calculate total for all goods in the cart.
```
(User/customer? Products/items/goods? Shopping cart/basket/cart?)

**Good (Consistent):**
```
Glossary:
- Customer: A registered user with an account
- Product: An item available for purchase in the catalog
- Shopping Cart: Collection of products customer intends to purchase

REQ-1: The customer shall add products to the shopping cart.
REQ-2: The customer shall review all products in the shopping cart before purchase.
REQ-3: The system shall calculate the total price for all products in the shopping cart.
```

**Common Inconsistencies:**
- User / Customer / Visitor / Person
- Product / Item / Good / Article
- Order / Purchase / Transaction
- Login / Sign In / Authenticate
- Delete / Remove / Cancel

**Why this matters:**
Inconsistent terminology creates confusion about whether different terms mean the same thing or different things. A glossary ensures shared understanding.

---

### CONS-NO-CONFLICT: Identify and Resolve Contradictions

**Principle:** Requirements must not contradict each other. Conflicts must be identified and resolved.

**Bad (Contradictory):**
```
REQ-101: The system shall require users to change passwords every 30 days.
REQ-205: The system shall allow users to keep the same password indefinitely.

REQ-305: Orders shall be fulfilled in the sequence received (FIFO).
REQ-310: High-priority orders shall be fulfilled before standard orders.
```

**Good (Resolved):**
```
REQ-101: The system shall require users with standard access to change
passwords every 90 days. [Changed from 30 to 90 based on usability feedback]

REQ-102: The system shall allow service accounts (non-human users) to use
the same password indefinitely as they are secured by IP restrictions and
do not risk weak password selection.

REQ-305: Standard orders shall be fulfilled in the sequence received (FIFO).

REQ-310: Priority orders (marked by customer service) shall be moved to
the front of the fulfillment queue ahead of standard orders placed at the same time.
```

**Why this matters:**
Contradictory requirements lead to implementation decisions that violate one requirement to satisfy another. Conflicts must be resolved during requirements phase, not implementation.

---

### CONS-FORMAT: Maintain Consistent Format and Structure

**Principle:** Use consistent structure and format for similar types of requirements to improve readability and completeness.

**Inconsistent:**
```
The system should let users log in.

REQ-102: Logout functionality - users can log out from any page

The password reset feature will send an email to users who forgot their
password so they can create a new one.
```

**Consistent:**
```
REQ-AUTH-101: User Login
The system shall authenticate users by validating email and password credentials
against the user database, granting access upon successful validation and
displaying an error message upon failure.

REQ-AUTH-102: User Logout
The system shall allow users to log out from any page, immediately terminating
the user's session and redirecting to the login page.

REQ-AUTH-103: Password Reset
The system shall send a password reset email containing a time-limited reset
link to users who request password recovery, allowing them to set a new password
within 24 hours of the request.
```

**Consistent Template Example:**
```
REQ-[CATEGORY]-[NUMBER]: [Capability Name]

Description: [What the system shall do]

Trigger: [What initiates this requirement]

Inputs: [What data/input is required]

Processing: [What the system does - stay external/observable]

Outputs: [What the system produces/displays]

Success Criteria: [How to verify this requirement]
```

**Why this matters:**
Consistent format makes requirements easier to read, review, and check for completeness. Templates ensure no critical information is forgotten.

---

### CONS-LEVEL: Maintain Consistent Level of Detail

**Principle:** Requirements at the same level should have similar granularity. Don't mix high-level and detailed requirements without structure.

**Inconsistent Detail Level:**
```
REQ-1: The system shall support e-commerce functionality.

REQ-2: When a user clicks the "Add to Cart" button on a product detail page,
the system shall validate that the selected quantity is available in inventory,
check if the product is already in the user's cart, and if so, increment the
quantity rather than creating a duplicate entry, then display a confirmation
message "Item added to cart" for 3 seconds before fading out, and update the
cart icon badge to show the new total count.
```
(REQ-1 is too high-level, REQ-2 is too detailed)

**Consistent Detail Level:**
```
High Level (Epic/Feature):
FEATURE-CART: Shopping Cart Management
Users shall be able to collect products for purchase in a shopping cart,
modify cart contents, and proceed to checkout.

Medium Level (Requirements):
REQ-CART-101: Add Product to Cart
The system shall allow users to add products to their shopping cart from
the product detail page, specifying quantity.

REQ-CART-102: View Cart Contents
The system shall display all products in the user's cart with quantities,
prices, and total.

REQ-CART-103: Modify Cart
The system shall allow users to update quantities or remove products from cart.

Detailed Level (Acceptance Criteria):
REQ-CART-101 Acceptance Criteria:
- User can select quantity (1-99) before adding to cart
- System validates quantity against available inventory
- If product already in cart, system increments quantity rather than duplicating
- System displays confirmation message after adding
- Cart icon updates to show total item count
- Add action completes within 1 second
```

**Why this matters:**
Consistent detail level makes requirements easier to understand, estimate, and implement. Mixing levels creates confusion about scope and priority.

---

### CONS-REFS: Ensure Valid Cross-References

**Principle:** When requirements reference other requirements, use cases, or documents, ensure references are valid and maintained.

**Bad (Broken References):**
```
REQ-205: Payment processing shall comply with requirements in the Security
Specification (see document XYZ-2019).
[Document XYZ-2019 was replaced by ABC-2023 but reference not updated]

REQ-310: This requirement depends on REQ-205 being implemented.
[REQ-205 was renumbered to REQ-PAY-101 but reference not updated]
```

**Good (Valid, Maintained References):**
```
REQ-PAY-101: Payment Processing Security
Payment processing shall comply with PCI DSS requirements as specified in
"Security Requirements Specification v2.1 (ABC-2023)", Section 4.2.

Depends on:
- REQ-USER-105 (User Authentication) - must be completed first
- REQ-DATA-201 (Data Encryption) - must be implemented concurrently

Referenced by:
- REQ-PAY-102 (Refund Processing)
- REQ-AUDIT-150 (Payment Audit Logging)

Cross-references:
- Design: Architecture Decision Record ADR-015
- Test Cases: TC-PAY-101 through TC-PAY-115
- User Story: US-340
```

**Reference Management:**
- Use unique, stable identifiers for requirements
- Maintain bidirectional traceability (A depends on B; B is needed by A)
- Update all references when requirements change
- Use tools to validate references automatically if possible

**Why this matters:**
Broken references hide dependencies and create confusion. Valid cross-references enable impact analysis and ensure nothing is forgotten.

---

### CONS-RULES: Ensure Business Rules Are Consistent

**Principle:** Business rules must be consistent across all requirements and documented in a central location.

**Inconsistent Business Rules:**
```
REQ-101: Free shipping applies to orders over $50.
REQ-205: Customers qualify for free shipping on orders of $75 or more.
REQ-310: Display "Free Shipping!" banner when cart total exceeds $60.
```
(Three different thresholds for free shipping!)

**Consistent Business Rules:**
```
Business Rules Document:

BR-SHIP-001: Free Shipping Threshold
Free standard shipping applies to orders with subtotal ≥ $50 (before tax,
after discounts). This threshold applies to all customer types except
wholesale customers (see BR-SHIP-002).

Requirements Using This Rule:

REQ-CART-101: Display Free Shipping Indicator
The system shall display "Free Shipping!" indicator in the shopping cart
when the order subtotal meets the threshold defined in BR-SHIP-001.

REQ-CHECKOUT-205: Apply Free Shipping
The system shall apply free standard shipping to orders meeting the threshold
defined in BR-SHIP-001.

REQ-PROMO-310: Free Shipping Banner
The system shall display a promotional banner indicating how much more the
customer must add to qualify for free shipping (per BR-SHIP-001) when the
cart subtotal is below the threshold.
```

**Why this matters:**
Business rules are used across multiple requirements. Documenting them centrally ensures consistency and makes updates easier (update once, not in every requirement).

---

## Completeness

### COMP-ACTORS: Identify All Actors

**Principle:** Document all people, systems, and external entities that interact with the system.

**Incomplete:**
```
Use Case: Process Order
Actor: Customer
```
(Missing other actors who interact during order processing)

**Complete:**
```
Use Case: Process Order

Primary Actor: Customer (initiates the process)

Secondary Actors:
- Payment Gateway (processes payment)
- Inventory System (checks stock, reserves items)
- Shipping Provider API (calculates rates, creates labels)
- Email Service (sends confirmations)
- Fraud Detection Service (validates transactions)
- Tax Calculation Service (computes sales tax)

Supporting Actors:
- Customer Service Representative (handles issues)
- Warehouse Staff (receives order for fulfillment)
- System Administrator (monitors system health)

Stakeholders (not direct actors, but interested):
- Business Owner (concerned with revenue)
- Compliance Officer (ensures regulatory compliance)
- Finance Team (receives payment records)
```

**Why this matters:**
Missing actors lead to incomplete requirements. Each actor has needs, and each interaction is a potential requirement.

---

### COMP-SCENARIOS: Cover All Scenarios

**Principle:** Document all scenarios including happy path, alternative paths, and exception cases.

**Incomplete (Happy Path Only):**
```
Use Case: User Login
1. User enters email and password
2. System validates credentials
3. System grants access to dashboard
```

**Complete (All Scenarios):**
```
Use Case: User Login

Main Success Scenario:
1. User navigates to login page
2. User enters registered email and password
3. System validates credentials against database
4. System creates authenticated session
5. System redirects user to dashboard

Alternative Flow A: Remember Me
3a. User selects "Remember Me" checkbox
3b. System creates extended session (30 days)
3c. Continue to step 4

Alternative Flow B: First Login
4a. If this is user's first login, system displays welcome tour
4b. User completes or skips tour
4c. Continue to step 5

Exception Flow A: Invalid Credentials
3a. If credentials don't match, system increments failed attempt counter
3b. System displays "Invalid email or password" error message
3c. If failed attempts < 5, return to step 2
3d. If failed attempts ≥ 5, go to Exception Flow B

Exception Flow B: Account Locked
3a. System locks account for 15 minutes
3b. System sends "suspicious activity" email to registered address
3c. System displays "Account temporarily locked. Please try again in 15 minutes."
3d. Use case ends

Exception Flow C: Unverified Email
3a. If email not verified, system displays "Please verify your email first"
3b. System offers to resend verification email
3c. If user requests resend, system sends verification email
3d. Use case ends

Exception Flow D: Expired Password
4a. If password expired per security policy, system requires password change
4b. System redirects to password change page
4c. User must create new password before accessing dashboard
```

**Why this matters:**
Real systems must handle errors and exceptions. Documenting only the happy path leaves critical functionality undefined.

---

### COMP-EDGE: Address Edge Cases

**Principle:** Identify and specify behavior for edge cases, boundary conditions, and unusual scenarios.

**Missing Edge Cases:**
```
REQ: The system shall allow users to enter a quantity when adding products to cart.
```

**With Edge Cases:**
```
REQ-CART-101: Product Quantity Selection

The system shall allow users to enter a quantity when adding products to cart,
with the following constraints:

Normal Cases:
- User selects quantity 1-99 from dropdown
- System adds specified quantity to cart

Edge Cases:

Boundary - Zero Quantity:
- System does not allow quantity of 0
- Minimum selectable quantity is 1

Boundary - Maximum Quantity:
- System limits quantity to 99 per line item
- For quantities >99, user must add multiple line items
- System displays message: "Maximum 99 per item. Add again for more."

Boundary - Inventory Limits:
- If requested quantity > available inventory, system limits to available
- System displays: "Only X available. Quantity adjusted."

Edge - Product Already in Cart:
- If product already in cart, system adds new quantity to existing quantity
- If total would exceed 99, system caps at 99 and displays message

Edge - Decimal Quantities:
- For products sold by weight (e.g., deli items), allow decimal quantities
- Allow up to 2 decimal places (e.g., 2.5 lbs)
- For count-based products, only allow whole numbers

Edge - Negative Quantities:
- System rejects negative quantities
- Display error: "Quantity must be positive"

Edge - Non-Numeric Input:
- System validates input is numeric
- Display error: "Please enter a valid quantity"
```

**Common Edge Cases to Consider:**
- Zero values
- Negative values
- Maximum/minimum boundaries
- Empty inputs
- Null values
- Duplicate entries
- First time / last time
- Single item vs. many items
- Concurrent access
- Partial failures

**Why this matters:**
Edge cases cause many production bugs. Specifying edge case behavior during requirements prevents bugs and ensures consistent handling.

---

### COMP-ERROR: Specify Error Conditions

**Principle:** For every operation, specify what happens when things go wrong.

**Missing Error Handling:**
```
REQ: The system shall process credit card payments.
```

**With Error Handling:**
```
REQ-PAY-101: Credit Card Payment Processing

Success Scenario:
The system shall process credit card payments by:
1. Validating card information format
2. Sending payment request to payment gateway
3. Receiving authorization from gateway
4. Recording successful transaction
5. Displaying confirmation to user

Error Conditions:

ERROR-PAY-101: Invalid Card Format
- Trigger: Card number fails Luhn algorithm or wrong length
- System Response: Display "Invalid card number. Please check and try again."
- User Action: Correct card number and resubmit
- No payment attempt made

ERROR-PAY-102: Payment Declined - Insufficient Funds
- Trigger: Gateway returns "insufficient funds" decline
- System Response: Display "Your card was declined due to insufficient funds."
- User Action: Try different payment method
- Order preserved for retry

ERROR-PAY-103: Payment Declined - Security Code Invalid
- Trigger: Gateway returns "CVV mismatch"
- System Response: Display "Security code (CVV) is incorrect. Please check the 3-digit code on your card."
- User Action: Correct CVV and resubmit
- Limit: 3 attempts, then require different card

ERROR-PAY-104: Payment Gateway Timeout
- Trigger: Gateway does not respond within 30 seconds
- System Response: Retry automatically (up to 2 retries)
- If all retries fail: Display "Payment processing is experiencing delays. Your cart has been saved. Please try again in a few minutes."
- Order saved for later retry
- Customer service notified

ERROR-PAY-105: Payment Gateway Unavailable
- Trigger: Gateway returns service unavailable error
- System Response: Display "Payment processing is temporarily unavailable. Please try again later."
- Email sent to customer with link to complete order
- Alert sent to operations team

ERROR-PAY-106: Suspected Fraud
- Trigger: Fraud detection flags transaction
- System Response: Decline transaction automatically
- Display: "We're unable to process this transaction. Please contact customer service."
- Fraud team notified with transaction details
- User cannot retry (must contact support)
```

**Why this matters:**
Error handling is often overlooked in requirements, leading to poor user experience and operational issues. Explicit error requirements ensure errors are handled gracefully.

---

### COMP-NFR: Include Non-Functional Requirements

**Principle:** In addition to functional requirements (what the system does), specify non-functional requirements (how well it does it).

**Missing NFRs:**
```
Requirements document contains 50 functional requirements about features,
but no performance, security, usability, or reliability requirements.
```

**With NFRs:**
```
FUNCTIONAL REQUIREMENTS: [50 requirements about features]

NON-FUNCTIONAL REQUIREMENTS:

Performance:
NFR-PERF-101: Page load times shall be <2 seconds on broadband (10 Mbps)
NFR-PERF-102: API response times shall be <500ms for 95% of requests
NFR-PERF-103: System shall support 5,000 concurrent users

Scalability:
NFR-SCALE-101: System shall scale to 10,000 users with <10% performance degradation
NFR-SCALE-102: Database shall support 1 million product records

Security:
NFR-SEC-101: All data in transit shall use TLS 1.3
NFR-SEC-102: Passwords shall be hashed using bcrypt with work factor ≥12
NFR-SEC-103: System shall comply with OWASP Top 10 (zero critical/high issues)
NFR-SEC-104: User sessions shall expire after 30 minutes of inactivity

Reliability:
NFR-REL-101: System uptime shall be 99.9% measured monthly
NFR-REL-102: Mean Time to Recovery (MTTR) shall be <1 hour
NFR-REL-103: System shall automatically recover from single component failure

Usability:
NFR-USE-101: New users shall complete first purchase in <5 minutes (80% success rate)
NFR-USE-102: System shall comply with WCAG 2.1 Level AA
NFR-USE-103: Key actions shall require ≤3 clicks from homepage

Maintainability:
NFR-MAINT-101: Code shall achieve 80% automated test coverage
NFR-MAINT-102: System shall support zero-downtime deployments
NFR-MAINT-103: Configuration changes shall not require code redeployment

Compatibility:
NFR-COMPAT-101: System shall support Chrome, Firefox, Safari, Edge (latest 2 versions)
NFR-COMPAT-102: Mobile experience shall support iOS 14+ and Android 10+
NFR-COMPAT-103: System shall provide responsive design for screens 320px to 2560px wide
```

**Why this matters:**
Non-functional requirements are as important as functional ones. They define quality attributes that determine user satisfaction and system success.

---

### COMP-DATA: Specify Data Requirements

**Principle:** Document what data the system must manage, including attributes, formats, validation rules, and volumes.

**Incomplete:**
```
REQ: The system shall store customer information.
```

**Complete:**
```
REQ-DATA-CUSTOMER: Customer Data Management

The system shall store and manage customer data with the following attributes:

Required Data:
- Customer ID: Auto-generated UUID, unique, immutable
- Email Address: String, max 255 chars, valid email format, unique, case-insensitive
- Password Hash: Bcrypt hash, work factor 12, never stored in plaintext
- First Name: String, 1-50 chars, letters/spaces/hyphens only
- Last Name: String, 1-50 chars, letters/spaces/hyphens only
- Created Date: Timestamp, UTC, auto-generated on creation
- Last Login: Timestamp, UTC, updated on each successful login

Optional Data:
- Phone Number: String, validated format, optional
- Date of Birth: Date, format YYYY-MM-DD, optional
- Profile Photo: Image, max 5MB, JPG/PNG only, optional
- Marketing Opt-In: Boolean, default false, optional
- Preferred Language: String, ISO 639-1 code, default "en", optional

Calculated/Derived:
- Account Age: Calculated from Created Date
- Customer Lifetime Value: Calculated from order history
- Risk Score: Calculated by fraud detection algorithm

Validation Rules:
- Email must be verified before account is fully active
- Password must be 12+ chars with uppercase, lowercase, number, special char
- Date of Birth, if provided, must indicate age 18+
- Phone number, if provided, must match pattern for customer's country

Data Volume:
- Expected: 100,000 customer records in year 1
- Planned capacity: 1,000,000 customer records
- Growth rate: ~10,000 new customers per month

Data Retention:
- Active accounts retained indefinitely
- Inactive accounts (no login 2+ years) archived
- Deleted accounts purged after 30-day grace period
- Comply with GDPR right to deletion requests within 30 days
```

**Why this matters:**
Data requirements drive database design, API design, and validation logic. Incomplete data requirements lead to design rework and missing functionality.

---

### COMP-CONSTRAINTS: Document Constraints

**Principle:** Explicitly state all constraints, limitations, and boundaries.

**Missing Constraints:**
```
Requirements document describes ideal functionality but doesn't mention
limitations, constraints, or what the system won't do.
```

**With Constraints:**
```
CONSTRAINTS:

Technical Constraints:
CONS-TECH-101: System must run on company-approved Azure cloud infrastructure
CONS-TECH-102: System must integrate with existing Active Directory for authentication
CONS-TECH-103: System must use approved open-source licenses (Apache 2.0, MIT, BSD)
CONS-TECH-104: Mobile apps limited to native iOS and Android (no cross-platform frameworks due to IT policy)

Business Constraints:
CONS-BUS-101: Development budget capped at $500,000
CONS-BUS-102: Must launch MVP within 6 months
CONS-BUS-103: Must support existing customer data (no data migration, read from legacy DB)
CONS-BUS-104: Cannot change pricing structure (must use existing pricing model)

Regulatory Constraints:
CONS-REG-101: Must comply with GDPR for EU customers
CONS-REG-102: Must comply with PCI DSS for payment card processing
CONS-REG-103: Must comply with WCAG 2.1 Level AA for accessibility
CONS-REG-104: Must provide audit trail for SOC 2 compliance

Performance Constraints:
CONS-PERF-101: Maximum response time 3 seconds (limited by legacy system integration)
CONS-PERF-102: Batch processing limited to 2-hour nightly window

Scope Constraints (What We Won't Do):
CONS-SCOPE-101: V1 will NOT support international shipping (domestic only)
CONS-SCOPE-102: V1 will NOT support mobile app (web responsive only)
CONS-SCOPE-103: V1 will NOT support multiple currencies (USD only)
CONS-SCOPE-104: Will NOT replace existing warehouse management system (integration only)

Data Constraints:
CONS-DATA-101: Maximum file upload size 10MB (infrastructure limitation)
CONS-DATA-102: Maximum 50 items per cart (business rule)
CONS-DATA-103: Product catalog limited to 100,000 SKUs (database license)
```

**Why this matters:**
Constraints shape what's possible. Explicit constraints prevent wasted effort on impossible requirements and guide realistic design decisions.

---

### COMP-ASSUMPTIONS: State All Assumptions

**Principle:** Document all assumptions made during requirements gathering. Assumptions are risks that need validation.

**Hidden Assumptions:**
```
Requirements written assuming users have high-speed internet, modern browsers,
and familiarity with e-commerce, but never stated explicitly.
```

**Explicit Assumptions:**
```
ASSUMPTIONS (To Be Validated):

User Assumptions:
ASSUM-USER-101: Users have basic internet literacy (can navigate websites, fill forms)
ASSUM-USER-102: Users have broadband internet (10 Mbps or faster)
ASSUM-USER-103: Users have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
ASSUM-USER-104: 80% of users will access via desktop, 20% via mobile
ASSUM-USER-105: Users have prior e-commerce experience
Risk: If users are less tech-savvy, may need simpler UI and tutorials
Validation: User research and analytics from beta

Technical Assumptions:
ASSUM-TECH-101: Payment gateway API will have 99.9% uptime per SLA
ASSUM-TECH-102: Legacy customer database will remain available during migration
ASSUM-TECH-103: Azure cloud services will be available in required regions
Risk: If assumptions fail, need backup plans
Validation: Review SLAs and contracts

Business Assumptions:
ASSUM-BUS-101: Product catalog will not exceed 50,000 SKUs in year 1
ASSUM-BUS-102: Average order value will be $75
ASSUM-BUS-103: Peak traffic will be 3x average during holiday season
ASSUM-BUS-104: Customer service team will have 10 agents available during business hours
Risk: If volumes higher, may need to scale infrastructure
Validation: Historical data analysis and forecasting

Data Assumptions:
ASSUM-DATA-101: Existing customer data is 90%+ accurate
ASSUM-DATA-102: Product data is maintained in real-time by merchandising team
Risk: If data quality poor, may need data cleansing
Validation: Data quality audit before launch

External Dependencies (Assumptions):
ASSUM-EXT-101: Shipping carrier API will respond within 2 seconds
ASSUM-EXT-102: Tax calculation service will maintain 99.5% uptime
ASSUM-EXT-103: Email service can send 10,000 emails per hour
Risk: If external services underperform, user experience degrades
Validation: Load testing and SLA review
```

**Why this matters:**
Assumptions are hidden risks. Making them explicit allows stakeholders to validate or challenge them, preventing nasty surprises during development or launch.

---

## Anti-Patterns to Avoid

### ANTI-GOLD: Avoid Gold Plating

**Principle:** Don't add features or requirements beyond what's actually needed. Focus on delivering value, not building everything imaginable.

**Gold Plating Example:**
```
Requirement: "As a user, I want to log in so I can access my account."

Gold-Plated Addition (Not Requested):
- Facial recognition login
- Voice authentication
- Fingerprint scanning
- Login via blockchain wallet
- AI-powered suspicious login detection
- Real-time login analytics dashboard
- Social media login integration
- Passwordless magic link authentication
- Hardware security key support

(User just needed simple email/password login!)
```

**Appropriate:**
```
MVP Requirements:
REQ-AUTH-101: Email and password login
REQ-AUTH-102: "Remember me" option
REQ-AUTH-103: Password reset via email
REQ-AUTH-104: Basic brute-force protection (account lockout after 5 failures)

Future Enhancements (Backlog, Not Committed):
- Social media login (if users request it)
- Two-factor authentication (if security assessment recommends it)
- Biometric login for mobile app (if mobile app is built)
```

**Why this matters:**
Gold plating wastes time and budget on features users don't need. Focus on validated user needs, not "wouldn't it be cool if..."

---

### ANTI-IMPL: Don't Sneak Implementation into Requirements

**Principle:** Requirements describe problems and needs. Implementation details belong in design documents.

**Implementation Disguised as Requirement:**
```
REQ-USER-PROFILE: User Profile Management

The system shall implement a UserProfile class extending BaseEntity with
fields for userId (UUID), firstName (varchar 50), lastName (varchar 50),
email (varchar 255 unique), and createdDate (timestamp). The class shall
use JPA annotations for ORM mapping to the user_profiles table in PostgreSQL.
Profile updates shall trigger a Kafka event to the "user-updated" topic for
consumption by the analytics service.
```
(This is design/implementation, not a requirement!)

**Proper Requirement:**
```
REQ-USER-PROFILE: User Profile Management

The system shall allow users to view and update their profile information including:
- First and last name
- Email address
- Profile photo
- Phone number
- Notification preferences

The system shall:
- Validate email format and uniqueness before accepting changes
- Require email verification when email address is changed
- Display current profile information when user accesses profile page
- Save changes immediately when user submits updates
- Preserve profile data across sessions
- Notify other system components when profile changes occur (for analytics and personalization)

Non-Functional:
- Profile updates shall complete within 2 seconds
- Profile data shall be consistent across all user sessions immediately after update
```

**Why this matters:**
Mixing requirements with implementation constrains developers, obscures true user needs, and makes requirements brittle (they break when implementation changes).

---

### ANTI-ASSUME: Don't Assume Knowledge

**Principle:** Don't assume readers have context, domain knowledge, or access to information not in the requirements document.

**Assumes Too Much:**
```
REQ-COMPLIANCE-101: The system shall comply with the regulation.
(Which regulation? What does compliance mean specifically?)

REQ-INTEGRATION-205: The system shall integrate with the ERP.
(Which ERP? What data? How? What does "integrate" mean?)

REQ-SECURITY-310: Implement the standard security measures.
(Which standards? What measures specifically?)

REQ-REPORTING-105: Reports shall follow the usual format.
(What's the "usual format"? Where is it documented?)
```

**Explicit and Clear:**
```
REQ-COMPLIANCE-101: GDPR Data Protection Compliance
The system shall comply with EU General Data Protection Regulation (GDPR) by:
- Obtaining explicit consent before collecting personal data
- Providing clear privacy policy in plain language
- Allowing users to export their data in machine-readable format (JSON)
- Allowing users to request deletion of their data
- Processing deletion requests within 30 days
- Maintaining audit log of all data access and modifications

REQ-INTEGRATION-205: SAP ERP Integration
The system shall integrate with the company's SAP S/4HANA ERP system by:
- Synchronizing product catalog data (SKU, price, description) nightly at 2 AM
- Sending completed orders to SAP within 5 minutes of order confirmation
- Receiving inventory updates from SAP every 15 minutes
- Using SAP's standard REST API as documented in "SAP Integration Guide v3.2"
- Authenticating via OAuth 2.0 with credentials managed in Azure Key Vault

REQ-SECURITY-310: OWASP Top 10 Compliance
The system shall implement security measures to address all OWASP Top 10 vulnerabilities:
- A01: Broken Access Control - Implement role-based access control
- A02: Cryptographic Failures - Use TLS 1.3 for all data in transit
- A03: Injection - Use parameterized queries, input validation
[...continue for all 10]
The system shall pass third-party security scan with zero critical/high findings.

REQ-REPORTING-105: Sales Report Format
The system shall generate sales reports in the following format:
- Header: Company logo, report title, date range, generation timestamp
- Summary Section: Total sales, total orders, average order value
- Detail Section: Table with columns [Date, Order ID, Customer, Items, Total]
- Footer: Page number, generated by, confidentiality notice
- Format: PDF with embedded fonts for printing
- Example: See "Sales Report Template v2.1" in Appendix B
```

**Why this matters:**
Requirements should be self-contained. Readers shouldn't need tribal knowledge, access to other systems, or context not in the document to understand requirements.

---

### ANTI-FUTURE: Avoid Premature Future-Proofing

**Principle:** Design for current known needs, not imagined future needs. Over-engineering for unclear future needs wastes resources.

**Over-Future-Proofed:**
```
REQ-DATA-MODEL: Database Design

The system shall use a highly flexible, extensible database schema that can
accommodate any possible future requirement without modification, supporting
unlimited custom fields, dynamic relationships, and polymorphic data structures
that can represent any entity type we might need in the future.

The system shall support integration with any possible future third-party
service through a plugin architecture that requires zero code changes,
accommodating unknown APIs, protocols, and data formats.
```
(Building for unclear future needs that may never materialize)

**Appropriately Designed:**
```
REQ-DATA-CUSTOMER: Customer Data Model

The system shall store customer data including:
- Required: ID, email, name, password hash, created date
- Optional: Phone, date of birth, address, preferences
- Custom: Up to 10 user-defined custom fields (for A/B testing, segmentation)

The data model shall:
- Support the 5 customer types currently in use: Retail, Wholesale, Partner, Employee, Test
- Allow adding new customer types without database schema changes (configuration-based)

REQ-INTEGRATION-EXTENSIBILITY: Third-Party Integration Design

The system shall support integration with:
- Current payment gateway (Stripe)
- Current shipping carriers (UPS, FedEx, USPS)
- Current email service (SendGrid)

The system shall be designed to allow adding new integrations of the same
types (payment, shipping, email) without modifying core business logic, by:
- Using adapter pattern for external services
- Externalizing service endpoints and credentials to configuration
- Providing clear integration interfaces

Note: Support for entirely new types of integrations (not yet identified)
is out of scope for V1. Requirements will be gathered when specific needs arise.
```

**Why this matters:**
Future-proofing for vague, unknown future needs leads to over-engineered, complex systems. Design for known needs with reasonable extension points, not infinite flexibility.

---

### ANTI-JARGON: Avoid Unexplained Jargon and Acronyms

**Principle:** Define all domain terms, acronyms, and jargon. Write for stakeholders who may not share your context.

**Jargon-Heavy (Unclear):**
```
REQ-SLA-101: System Performance

The system shall maintain SLAs for TTFB and FCP per CWV guidelines, ensuring
LCP <2.5s and CLS <0.1 for P95 of requests. Integration with the CIAM via
OIDC/SAML shall support MFA and SSO for B2B and B2C users. The DMP shall
sync with the CDP for 360-degree customer view.
```
(Acronym soup! Readers may not know: TTFB, FCP, CWV, LCP, CLS, P95, CIAM, OIDC, SAML, MFA, SSO, B2B, B2C, DMP, CDP)

**Clear with Definitions:**
```
GLOSSARY:

- Core Web Vitals (CWV): Google's metrics for page performance
- Largest Contentful Paint (LCP): Time for main content to load
- Cumulative Layout Shift (CLS): Visual stability measure
- P95: 95th percentile (95% of requests faster than this)
- Customer Identity and Access Management (CIAM): System managing customer logins
- Single Sign-On (SSO): Login once, access multiple systems
- Multi-Factor Authentication (MFA): Additional login verification (e.g., SMS code)
- Business-to-Business (B2B): Commercial customers
- Business-to-Consumer (B2C): Individual customers
- Data Management Platform (DMP): Marketing data system
- Customer Data Platform (CDP): Unified customer profile system

REQ-PERF-101: Page Load Performance

The system shall meet the following page load performance targets:
- Main content (Largest Contentful Paint) shall load within 2.5 seconds for
  95% of page loads (95th percentile)
- Visual stability (Cumulative Layout Shift) score shall be less than 0.1
- Performance measured using Google Core Web Vitals methodology

REQ-AUTH-102: Customer Authentication

The system shall integrate with the Customer Identity and Access Management
(CIAM) system using:
- OIDC (OpenID Connect) for consumer customer authentication
- SAML (Security Assertion Markup Language) for business customer authentication

The system shall support:
- Single Sign-On (SSO): Customers login once and access all company applications
- Multi-Factor Authentication (MFA): Optional second verification step (SMS or authenticator app)

REQ-DATA-103: Customer Data Integration

The system shall synchronize customer data between:
- DMP (Data Management Platform): Marketing campaign data
- CDP (Customer Data Platform): Unified customer profile

This creates a "360-degree view" where all customer information (demographics,
behavior, purchases, marketing interactions) is available in one place.
```

**Why this matters:**
Jargon excludes stakeholders and creates miscommunication. Define terms so everyone understands. Include a glossary for any document with domain-specific terminology.

---

## Summary

High-quality requirements are:

**CLEAR** - Unambiguous language, one interpretation
**TESTABLE** - Can be verified and validated
**COMPLETE** - All scenarios, actors, and edge cases covered
**CONSISTENT** - No contradictions, aligned terminology
**PROBLEM-FOCUSED** - WHAT not HOW, business language
**TRACEABLE** - Linked to business needs and design
**VALUABLE** - Explicit business or user value

**Focus on:**
- User stories with INVEST criteria
- Use cases with all flows (main, alternative, exception)
- Staying in problem domain (no architecture/design/technology)
- Consistency in terminology and business rules
- Completeness (NFRs, error handling, edge cases, constraints, assumptions)

**Avoid:**
- Gold plating (unneeded features)
- Implementation details in requirements
- Vague terms without measurable criteria
- Assuming knowledge or context
- Premature future-proofing
- Unexplained jargon

---

*Based on agile requirements engineering, INVEST criteria, use case best practices, IEEE 830, and BABOK*
