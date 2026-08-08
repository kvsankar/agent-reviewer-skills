## Expected Good Patterns (Check for Absence)

> **Sources:** [Agile Alliance INVEST](https://www.agilealliance.org/glossary/invest/), [LogRocket INVEST Guide](https://blog.logrocket.com/product-management/writing-meaningful-user-stories-invest-principle/), [AltexSoft Acceptance Criteria Guide](https://www.altexsoft.com/blog/acceptance-criteria-purposes-formats-and-best-practices/)

This section identifies the **absence of good patterns** (not just presence of anti-patterns). Use `MISSING-*` IDs for tracking.

### 1. User Story Structure Patterns

**Mnemonic:** **"WHO-WHAT-WHY"**

| Expected Pattern | If Missing |
|------------------|------------|
| Complete "As a/I want/So that" format | 🔴 `MISSING-STORY-FORMAT` - Incomplete story |
| Specific user persona (not "user") | ⚠️ `MISSING-PERSONA` - Generic actor |
| Clear business value statement | 🔴 `MISSING-VALUE-STATEMENT` - No justification |
| Acceptance criteria attached | 🔴 `MISSING-ACCEPTANCE-CRITERIA` - Undefined "done" |

```markdown
# PRESENT: Complete user story with structure

**User Story: Order History Access**

As a **registered customer** (specific persona)
I want to **view my order history from the last 12 months** (specific action)
So that I can **track my spending and reorder frequently purchased items** (clear value)

**Acceptance Criteria:**

Given I am logged in as a registered customer
When I navigate to "My Orders"
Then I see a list of all orders from the last 12 months
And each order shows: order date, total amount, status, order number
And orders are sorted by date (newest first)
And I can click any order to see full details

**Business Value:** Reduces customer support calls by 30% for order status inquiries


# MISSING: Incomplete user story

User Story: Order History

As a user (too generic - which user?)
I want to see my orders (what orders? how many? what info?)
(missing "So that" - why is this valuable?)

(no acceptance criteria - when is this "done"?)
```

### 2. INVEST Criteria Patterns

**Mnemonic:** **"INVEST-IN-STORIES"**

| Expected Pattern | If Missing |
|------------------|------------|
| Independent (no dependencies) | ⚠️ `MISSING-INDEPENDENCE` - Coupled stories |
| Negotiable (not contract) | 💡 `MISSING-NEGOTIABLE` - Over-specified |
| Valuable (clear benefit) | 🔴 `MISSING-VALUE` - No business value |
| Estimable (enough detail) | ⚠️ `MISSING-ESTIMABLE` - Can't size |
| Small (fits in sprint) | ⚠️ `MISSING-SMALL` - Too large |
| Testable (pass/fail criteria) | 🔴 `MISSING-TESTABLE` - Can't verify |

```markdown
# PRESENT: Stories meeting INVEST criteria

## Story 1: Independent & Small
As a checkout user
I want to apply a discount code to my cart
So that I receive the advertised discount

Acceptance Criteria:
- Valid code reduces total by specified percentage
- Invalid code shows error message
- Only one code can be applied per order

(Independent: Can be built/tested without other stories)
(Small: Can be completed in one sprint)

## Story 2: Valuable & Testable
As a warehouse manager
I want to receive low-stock alerts when inventory drops below threshold
So that I can reorder before stockouts occur

Acceptance Criteria:
- Alert triggers when stock < reorder_point
- Alert includes: product name, current stock, reorder quantity
- Alert sent via email within 5 minutes of threshold breach

Business Value: Reduces stockouts by 40%, preventing $50K monthly lost sales
Test: Set product threshold=10, reduce stock to 9, verify alert received


# MISSING: Stories violating INVEST

## Violates Independent
As a user, I want to complete checkout
(Depends on: login, cart, payment, shipping - too coupled!)

## Violates Valuable
As a developer, I want to refactor the database schema
(No user value! This is technical debt, not a user story)

## Violates Estimable
As a user, I want the system to be fast
(How fast? What operations? Can't estimate without specifics)

## Violates Small
As a user, I want to manage my entire account
(Too big! Break into: update profile, change password, manage addresses, etc.)

## Violates Testable
As a user, I want a modern, intuitive interface
(What is "modern"? What is "intuitive"? Can't objectively test)
```

### 3. Acceptance Criteria Patterns

**Mnemonic:** **"GIVEN-WHEN-THEN"**

| Expected Pattern | If Missing |
|------------------|------------|
| Given/When/Then format | 💡 `MISSING-GWT-FORMAT` - Unclear scenarios |
| Specific, measurable criteria | 🔴 `MISSING-MEASURABLE-AC` - Vague "done" |
| Edge cases covered | ⚠️ `MISSING-EDGE-CASES` - Incomplete coverage |
| Error scenarios included | ⚠️ `MISSING-ERROR-AC` - Happy path only |
| Testable assertions | 🔴 `MISSING-TESTABLE-AC` - Subjective criteria |

```markdown
# PRESENT: Complete acceptance criteria with GWT format

**Story: User Login**

**Happy Path:**
Given I am a registered user with valid credentials
When I enter my email and password and click "Login"
Then I am redirected to my dashboard
And I see "Welcome back, [name]" message
And my session expires after 30 minutes of inactivity

**Edge Cases:**
Given I have caps lock enabled
When I enter my password
Then I see a warning "Caps Lock is on"

Given I am already logged in on another device
When I log in from a new device
Then I see "You're logged in on 2 devices"

**Error Scenarios:**
Given I enter an incorrect password
When I click "Login"
Then I see "Invalid email or password"
And the password field is cleared
And I remain on the login page

Given I have failed login 5 times
When I attempt a 6th login
Then my account is locked for 15 minutes
And I see "Account temporarily locked. Try again in 15 minutes."
And I receive an email about the failed attempts


# MISSING: Vague acceptance criteria

**Story: User Login**

Acceptance Criteria:
- User can log in (what does "can" mean?)
- Error handling for invalid credentials (what error? what message?)
- Security should be maintained (how? measured how?)

(Missing: edge cases, specific error messages, measurable criteria)
```

### 4. Use Case Completeness Patterns

**Mnemonic:** **"MAIN-ALT-EXCEPTION"**

| Expected Pattern | If Missing |
|------------------|------------|
| Main success scenario documented | 🔴 `MISSING-MAIN-FLOW` - No happy path |
| Alternative flows documented | ⚠️ `MISSING-ALT-FLOWS` - Only one path |
| Exception/error flows documented | ⚠️ `MISSING-EXCEPTION-FLOWS` - No error handling |
| Preconditions stated | ⚠️ `MISSING-PRECONDITIONS` - Assumed context |
| Postconditions stated | 💡 `MISSING-POSTCONDITIONS` - Unclear end state |

```markdown
# PRESENT: Complete use case

**Use Case: Place Order**

**Actors:** Customer, Payment Gateway, Inventory System

**Preconditions:**
- Customer is logged in
- Cart contains at least one item
- All items are in stock

**Main Success Scenario:**
1. Customer clicks "Checkout"
2. System displays order summary with items and totals
3. Customer enters or selects shipping address
4. Customer selects shipping method
5. System calculates final total including shipping
6. Customer enters payment information
7. System validates payment with Payment Gateway
8. Payment Gateway confirms payment
9. System creates order record
10. System updates Inventory System (reduce stock)
11. System displays order confirmation with order number
12. System sends confirmation email to customer

**Alternative Flows:**
3a. Customer wants new address:
    1. Customer clicks "Add new address"
    2. Customer enters address details
    3. System validates address
    4. Return to step 4

6a. Customer uses saved payment method:
    1. Customer selects saved payment method
    2. Skip to step 7

**Exception Flows:**
7a. Payment validation fails:
    1. System displays "Payment declined: [reason]"
    2. Customer updates payment information
    3. Return to step 7

10a. Inventory update fails (item out of stock):
    1. System reverses payment
    2. System displays "Sorry, [item] is now out of stock"
    3. System offers to remove item and continue

**Postconditions:**
- Order exists with status "Confirmed"
- Payment captured
- Inventory reduced
- Confirmation email sent


# MISSING: Incomplete use case

**Use Case: Place Order**

1. User checks out
2. User pays
3. Order is placed

(Missing: actors, preconditions, alternative paths, error handling, postconditions)
```

### 5. Non-Functional Requirements Patterns

**Mnemonic:** **"PERFORMANCE-SECURITY-SCALE"**

| Expected Pattern | If Missing |
|------------------|------------|
| Performance requirements with numbers | ⚠️ `MISSING-PERFORMANCE-NFR` - "Fast" without metrics |
| Security requirements specified | ⚠️ `MISSING-SECURITY-NFR` - Assumed security |
| Scalability targets defined | 💡 `MISSING-SCALABILITY-NFR` - Unknown limits |
| Availability/uptime requirements | 💡 `MISSING-AVAILABILITY-NFR` - No SLA |
| Accessibility requirements | 💡 `MISSING-ACCESSIBILITY-NFR` - Excluded users |

```markdown
# PRESENT: Specific, measurable NFRs

## Performance
- Page load time: < 2 seconds at 95th percentile
- API response time: < 200ms for 99% of requests
- Search results: < 500ms for queries up to 10,000 results
- Checkout completion: < 5 seconds end-to-end

## Scalability
- Support 10,000 concurrent users
- Handle 1,000 orders per minute during peak
- Database: support 100 million product records
- File storage: 10TB with 50% annual growth

## Availability
- 99.9% uptime (< 8.76 hours downtime per year)
- Planned maintenance: max 4 hours monthly, outside peak hours
- Recovery Time Objective (RTO): 1 hour
- Recovery Point Objective (RPO): 5 minutes

## Security
- All data encrypted in transit (TLS 1.3)
- Passwords: bcrypt with cost factor 12
- Session timeout: 30 minutes of inactivity
- OWASP Top 10 vulnerabilities addressed
- PCI-DSS compliance for payment data

## Accessibility
- WCAG 2.1 AA compliance
- Screen reader compatible
- Keyboard navigation for all functions
- Color contrast ratio: minimum 4.5:1


# MISSING: Vague NFRs

## Performance
- The system should be fast
- Pages should load quickly

## Security
- The system should be secure
- User data should be protected

(No numbers, no specific criteria, can't test or verify)
```

### 6. Problem Domain Patterns

**Mnemonic:** **"WHAT-NOT-HOW"**

| Expected Pattern | If Missing |
|------------------|------------|
| Business language (not technical) | ⚠️ `MISSING-BUSINESS-LANG` - Technical jargon |
| Behavior description (not implementation) | 🔴 `MISSING-BEHAVIOR-FOCUS` - Design in requirements |
| User goals (not system internals) | ⚠️ `MISSING-USER-GOALS` - System-centric |
| Outcomes (not mechanisms) | 💡 `MISSING-OUTCOMES` - Process-focused |

```markdown
# PRESENT: Problem domain focus

**Requirement: Order Notifications**

The system shall notify customers when their order status changes.

Notifications include:
- Order confirmed (immediately after payment)
- Order shipped (include tracking number)
- Order delivered (based on carrier confirmation)
- Order delayed (if shipping estimate changes)

Customers can configure notification preferences:
- Email (default: enabled)
- SMS (default: disabled)
- Push notification (if app installed)


# MISSING: Implementation leaking into requirements

**Requirement: Order Notifications**

The system shall use a PostgreSQL database to store notification preferences
in a `user_preferences` table with columns `user_id`, `email_enabled`,
`sms_enabled`. When order status changes, a Kafka message shall be published
to the `order-events` topic. A Lambda function shall consume events and
send emails via SendGrid API, SMS via Twilio API...

(This is design/implementation, not requirements!
Requirements say WHAT happens, not HOW it's implemented.)
```

---

### Expected Patterns Summary Checklist

**When Reviewing, Verify Presence Of:**

🔴 **Critical (incomplete requirements if missing):**
- [ ] `MISSING-STORY-FORMAT` - No As a/I want/So that structure
- [ ] `MISSING-VALUE-STATEMENT` - No business value in story
- [ ] `MISSING-ACCEPTANCE-CRITERIA` - No criteria for "done"
- [ ] `MISSING-VALUE` - INVEST: Story provides no clear value
- [ ] `MISSING-TESTABLE` - INVEST: Can't objectively verify
- [ ] `MISSING-MEASURABLE-AC` - Vague acceptance criteria
- [ ] `MISSING-TESTABLE-AC` - Subjective/untestable criteria
- [ ] `MISSING-MAIN-FLOW` - No main success scenario
- [ ] `MISSING-BEHAVIOR-FOCUS` - Implementation in requirements

⚠️ **Warning (significant gaps):**
- [ ] `MISSING-PERSONA` - Generic "user" instead of persona
- [ ] `MISSING-INDEPENDENCE` - INVEST: Stories too coupled
- [ ] `MISSING-ESTIMABLE` - INVEST: Can't size story
- [ ] `MISSING-SMALL` - INVEST: Story too large for sprint
- [ ] `MISSING-EDGE-CASES` - Only happy path covered
- [ ] `MISSING-ERROR-AC` - No error scenario criteria
- [ ] `MISSING-ALT-FLOWS` - Only one path through use case
- [ ] `MISSING-EXCEPTION-FLOWS` - No error handling in use case
- [ ] `MISSING-PRECONDITIONS` - Assumed starting context
- [ ] `MISSING-PERFORMANCE-NFR` - No performance requirements
- [ ] `MISSING-SECURITY-NFR` - No security requirements
- [ ] `MISSING-BUSINESS-LANG` - Technical jargon in requirements
- [ ] `MISSING-USER-GOALS` - System-centric not user-centric

💡 **Recommendation (good practice):**
- [ ] `MISSING-NEGOTIABLE` - INVEST: Over-specified story
- [ ] `MISSING-GWT-FORMAT` - No Given/When/Then format
- [ ] `MISSING-POSTCONDITIONS` - Unclear end state
- [ ] `MISSING-SCALABILITY-NFR` - No scalability targets
- [ ] `MISSING-AVAILABILITY-NFR` - No uptime requirements
- [ ] `MISSING-ACCESSIBILITY-NFR` - No accessibility requirements
- [ ] `MISSING-OUTCOMES` - Process-focused not outcome-focused
