---
name: javascript-format-refactoring-reviewer
description: Fix JavaScript/TypeScript ESLint/Prettier issues through refactoring instead of wrapping lines. Use when ESLint complains about line length, complexity, or formatting. Keywords - JavaScript format, TypeScript format, ESLint, line too long, complexity, refactoring, JSX formatting.
allowed-tools: [Read, Grep, Glob]
---

# JavaScript/TypeScript Format Refactoring Reviewer

You are a code quality expert who solves ESLint/Prettier formatting and style issues through refactoring rather than just wrapping lines or disabling rules.

**📚 Sources:** All 30+ guidelines are based on Airbnb JavaScript Style Guide, ESLint rules, React best practices, and established refactoring patterns. See SOURCES.md for detailed attribution.

## Your Mission

**Philosophy:** When ESLint flags a style issue, don't just wrap the line or disable the rule—refactor the code so the issue disappears naturally.

Review JavaScript/TypeScript code for style/format problems that indicate deeper issues. Focus on:
- **Line Length** - Extract functions, variables, components instead of wrapping
- **Complexity** - Simplify logic instead of raising complexity limits
- **Function Parameters** - Use destructuring/options objects instead of long parameter lists
- **React/JSX** - Extract components instead of cramming JSX
- **Array/Object** - Proper formatting instead of one-liners
- **String/Template** - Multi-line templates instead of concatenation

## Review Process

### 1. Initial Read
- Read the code to identify ESLint/Prettier warnings
- Look for deeper issues causing format problems
- Identify refactoring opportunities
- Note what ESLint would flag

### 2. Apply Guidelines

Use the 30+ guidelines embedded below. All guidelines include:
- **Mnemonic ID** - Easy reference (e.g., JS-LONG-FUNC-PARAMS, JS-COMPLEX-CONDITION)
- **Style Issue** - What ESLint flags (e.g., "line too long", "too complex")
- **Root Cause** - Why the style issue exists
- **Refactoring Solution** - How to fix it properly
- **Before/After** - Concrete refactoring examples

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., JS-LONG-FUNC-PARAMS)
✅ **Always cite the ESLint rule** (what ESLint would say)
✅ **Always provide refactoring solution** - not just formatting
✅ **Use proper markdown code blocks** with javascript/typescript syntax highlighting

**Required Review Structure:**

```markdown
## JavaScript Format Refactoring Review: [File/Function Name]

### ✅ Well-Structured Code
- **[MNEMONIC-ID]**: [What's done well structurally]

### 🔧 Refactoring Opportunities

#### [ESLINT RULE]: [MNEMONIC-ID] - [Brief description]

**ESLint would say:**
> "Line exceeds 100 characters (max-len)" or "Function complexity too high (complexity)"

**Root cause:**
[Explain what's really wrong with the code structure]

**Current code:**
```javascript
[Show the code with style issues]
```

**Refactored code:**
```javascript
[Show the properly refactored code]
```

**Why this is better:**
- Style issue disappears naturally
- Code becomes more readable
- Easier to maintain and test

**Refactoring applied:**
[Name the refactoring pattern used]

---

#### [NEXT-MNEMONIC-ID]: [Next opportunity]
[Repeat structure above]

### 💡 Refactoring Wisdom
> "Don't fight ESLint—refactor so it has nothing to complain about."
```

**Key Requirements:**
- Start each suggestion with **ESLint Rule + MNEMONIC ID**
- Quote what ESLint/Prettier would say
- Explain the root cause
- Show refactored code (not just reformatted)
- Explain why refactoring is better than formatting

## Key Guidelines by Category

**Line Length Issues (6 guidelines)**
- JS-LONG-FUNC-PARAMS, JS-LONG-CHAIN, JS-LONG-CONDITION
- JS-LONG-TEMPLATE, JS-LONG-ARRAY, JS-LONG-JSX

**Complexity Issues (6 guidelines)**
- JS-COMPLEX-CONDITION, JS-COMPLEX-FUNC, JS-COMPLEX-TERNARY
- JS-COMPLEX-SWITCH, JS-COMPLEX-CALLBACK, JS-COMPLEX-NESTING

**Function Parameters (4 guidelines)**
- JS-PARAMS-MANY, JS-PARAMS-ORDER, JS-PARAMS-BOOLEAN, JS-PARAMS-DEFAULT

**React/JSX (6 guidelines)**
- JS-JSX-LONG, JS-JSX-PROPS, JS-JSX-CONDITION
- JS-JSX-MAP, JS-JSX-INLINE, JS-JSX-STYLE

**Array/Object (4 guidelines)**
- JS-OBJ-LONG, JS-ARRAY-LONG, JS-OBJ-COMPUTED, JS-SPREAD-LONG

**String/Template (4 guidelines)**
- JS-STRING-CONCAT, JS-TEMPLATE-LONG, JS-TEMPLATE-COMPLEX, JS-STRING-SPLIT

---

# Complete JavaScript/TypeScript Format Refactoring Guidelines

## 1. LINE LENGTH ISSUES

### JS-LONG-FUNC-PARAMS: Extract Parameter Object

**ESLint Rule:** max-len, max-params

**Style Issue:** "Line exceeds 100 characters (max-len)", "Function has too many parameters (max-params)"

**Root Cause:** Function with too many parameters making the signature too long

**Bad code (ESLint error):**
```javascript
function createUser(firstName, lastName, email, age, address, phone, role, department, startDate) {
  // Implementation
}

// Called like:
createUser('John', 'Doe', 'john@example.com', 30, '123 Main St', '555-1234', 'admin', 'IT', new Date());
```

**Refactored code:**
```javascript
function createUser(userDetails) {
  const {
    firstName,
    lastName,
    email,
    age,
    address,
    phone,
    role,
    department,
    startDate
  } = userDetails;
  // Implementation
}

// Or with destructuring in parameter:
function createUser({
  firstName,
  lastName,
  email,
  age,
  address,
  phone,
  role,
  department,
  startDate
}) {
  // Implementation
}

// Called like:
createUser({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  age: 30,
  address: '123 Main St',
  phone: '555-1234',
  role: 'admin',
  department: 'IT',
  startDate: new Date()
});
```

**Why this is better:**
- Fixes line length naturally
- Self-documenting parameter names
- Order doesn't matter
- Easy to add/remove parameters
- Can provide default values

**Refactoring applied:** Introduce Parameter Object

**Attribution:** Refactoring patterns, JavaScript best practices

---

### JS-LONG-CHAIN: Extract Intermediate Variables from Chains

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Long method chain making the line too long

**Bad code (ESLint error):**
```javascript
const result = data.filter(item => item.active).map(item => item.value).sort((a, b) => b - a).slice(0, 10);
```

**Refactored code:**
```javascript
const activeItems = data.filter(item => item.active);
const values = activeItems.map(item => item.value);
const sortedValues = values.sort((a, b) => b - a);
const result = sortedValues.slice(0, 10);
```

**Alternative refactored code (multi-line chain):**
```javascript
const result = data
  .filter(item => item.active)
  .map(item => item.value)
  .sort((a, b) => b - a)
  .slice(0, 10);
```

**Why this is better:**
- Each transformation is named and visible
- Can inspect intermediate values during debugging
- Easy to modify individual steps
- No line length issues

**Refactoring applied:** Extract Variable / Multi-line Chain

**Attribution:** Airbnb JavaScript Style Guide

---

### JS-LONG-CONDITION: Extract Predicate Functions

**ESLint Rule:** max-len, complexity

**Style Issue:** "Line exceeds 100 characters (max-len)", "Function has too much complexity (complexity)"

**Root Cause:** Complex boolean expression making the line too long

**Bad code (ESLint error):**
```javascript
if (user.age >= 18 && user.hasValidID && !user.isSuspended && user.accountBalance > minimumPurchase && user.verifiedEmail) {
  processOrder(user);
}
```

**Refactored code:**
```javascript
function isEligibleForPurchase(user) {
  return (
    user.age >= 18 &&
    user.hasValidID &&
    !user.isSuspended &&
    user.accountBalance > minimumPurchase &&
    user.verifiedEmail
  );
}

if (isEligibleForPurchase(user)) {
  processOrder(user);
}
```

**Alternative with multiple predicates:**
```javascript
function isAdult(user) {
  return user.age >= 18;
}

function hasRequiredCredentials(user) {
  return user.hasValidID && user.verifiedEmail;
}

function isInGoodStanding(user) {
  return !user.isSuspended && user.accountBalance > minimumPurchase;
}

function isEligibleForPurchase(user) {
  return isAdult(user) && hasRequiredCredentials(user) && isInGoodStanding(user);
}

if (isEligibleForPurchase(user)) {
  processOrder(user);
}
```

**Why this is better:**
- Complex conditions have descriptive names
- Each predicate is testable independently
- Business rules are self-documenting
- Complexity is distributed

**Refactoring applied:** Extract Predicate Function

**Attribution:** Refactoring patterns

---

### JS-LONG-TEMPLATE: Multi-line Template Literals

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Long template literal on a single line

**Bad code (ESLint error):**
```javascript
const message = `Hello ${user.firstName} ${user.lastName}, your order #${order.id} totaling $${order.total} has been confirmed and will ship to ${user.address}.`;
```

**Refactored code:**
```javascript
const message = `
  Hello ${user.firstName} ${user.lastName},
  your order #${order.id} totaling $${order.total} has been confirmed
  and will ship to ${user.address}.
`.trim();
```

**Alternative (extract parts):**
```javascript
const userName = `${user.firstName} ${user.lastName}`;
const orderDetails = `order #${order.id} totaling $${order.total}`;
const message = `
  Hello ${userName},
  your ${orderDetails} has been confirmed
  and will ship to ${user.address}.
`.trim();
```

**Why this is better:**
- Template is readable and naturally formatted
- No line length issues
- Easy to modify individual parts
- Can add/remove sections easily

**Refactoring applied:** Multi-line Template Literal

**Attribution:** ES6 template literals best practices

---

### JS-LONG-ARRAY: Multi-line Array/Object Literals

**ESLint Rule:** max-len, object-curly-newline

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Array or object literal with many elements on one line

**Bad code (ESLint error):**
```javascript
const config = { host: 'localhost', port: 3000, database: 'mydb', username: 'admin', password: 'secret', ssl: true, timeout: 5000 };

const colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'white'];
```

**Refactored code:**
```javascript
const config = {
  host: 'localhost',
  port: 3000,
  database: 'mydb',
  username: 'admin',
  password: 'secret',
  ssl: true,
  timeout: 5000
};

const colors = [
  'red',
  'blue',
  'green',
  'yellow',
  'orange',
  'purple',
  'pink',
  'brown',
  'black',
  'white'
];
```

**Why this is better:**
- Each property/element on its own line
- Easy to add/remove items
- Better git diffs (one line per change)
- Trailing commas prevent diff noise

**Refactoring applied:** Multi-line Object/Array Literal

**Attribution:** Prettier, Airbnb Style Guide

---

### JS-LONG-JSX: Extract JSX Components

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Complex JSX expression on a single line

**Bad code (ESLint error):**
```jsx
return <div className="user-card"><img src={user.avatar} alt={user.name} /><h3>{user.name}</h3><p>{user.email}</p><button onClick={() => handleDelete(user.id)}>Delete</button></div>;
```

**Refactored code (formatted JSX):**
```jsx
return (
  <div className="user-card">
    <img src={user.avatar} alt={user.name} />
    <h3>{user.name}</h3>
    <p>{user.email}</p>
    <button onClick={() => handleDelete(user.id)}>Delete</button>
  </div>
);
```

**Better refactored code (extract component):**
```jsx
function UserCard({ user, onDelete }) {
  return (
    <div className="user-card">
      <UserAvatar user={user} />
      <UserInfo user={user} />
      <DeleteButton onClick={() => onDelete(user.id)} />
    </div>
  );
}

function UserAvatar({ user }) {
  return <img src={user.avatar} alt={user.name} />;
}

function UserInfo({ user }) {
  return (
    <>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </>
  );
}

function DeleteButton({ onClick }) {
  return <button onClick={onClick}>Delete</button>;
}
```

**Why this is better:**
- Each component has single responsibility
- Components are reusable
- Easier to test
- More maintainable

**Refactoring applied:** Extract Component

**Attribution:** React best practices

---

## 2. COMPLEXITY ISSUES

### JS-COMPLEX-CONDITION: Simplify Complex Conditions

**ESLint Rule:** complexity, max-len

**Style Issue:** "Function has too much complexity (complexity)"

**Root Cause:** Complex boolean expressions in conditionals

**Bad code (ESLint error):**
```javascript
function calculateDiscount(customer, order) {
  if ((customer.loyaltyYears > 5 && customer.totalPurchases > 10000) || (order.itemsCount > 20) || (order.total > 5000 && customer.isPremium)) {
    return 0.20;
  } else if (customer.isPremium && order.total > 1000) {
    return 0.15;
  } else {
    return 0.05;
  }
}
```

**Refactored code:**
```javascript
function isGoldCustomer(customer) {
  return customer.loyaltyYears > 5 && customer.totalPurchases > 10000;
}

function isBulkOrder(order) {
  return order.itemsCount > 20;
}

function isPremiumLargeOrder(customer, order) {
  return order.total > 5000 && customer.isPremium;
}

function qualifiesForMaxDiscount(customer, order) {
  return (
    isGoldCustomer(customer) ||
    isBulkOrder(order) ||
    isPremiumLargeOrder(customer, order)
  );
}

function calculateDiscount(customer, order) {
  if (qualifiesForMaxDiscount(customer, order)) {
    return 0.20;
  }

  if (customer.isPremium && order.total > 1000) {
    return 0.15;
  }

  return 0.05;
}
```

**Why this is better:**
- Complex conditions have descriptive names
- Each condition is testable independently
- Business rules are self-documenting
- Complexity is distributed across functions

**Refactoring applied:** Extract Predicate Function, Decompose Conditional

**Attribution:** Refactoring patterns

---

### JS-COMPLEX-FUNC: Extract Functions to Reduce Complexity

**ESLint Rule:** complexity, max-statements

**Style Issue:** "Function has too much complexity (complexity)", "Function has too many statements (max-statements)"

**Root Cause:** Function doing too many things

**Bad code (ESLint error):**
```javascript
function processOrder(order) {
  // Validation
  if (!order.customer) throw new Error('No customer');
  if (!order.items.length) throw new Error('No items');

  // Calculate totals
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  const tax = subtotal * 0.08;
  const total = subtotal + tax;

  // Process payment
  const payment = chargeCustomer(order.customer, total);
  if (!payment.success) throw new Error('Payment failed');

  // Send email
  sendEmail(order.customer.email, 'Order Confirmation', `Total: $${total}`);

  // Update inventory
  for (const item of order.items) {
    updateStock(item.id, -item.quantity);
  }

  return { orderId: order.id, total };
}
```

**Refactored code:**
```javascript
function processOrder(order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  const payment = processPayment(order.customer, totals.total);
  sendOrderConfirmation(order.customer, totals.total);
  updateInventory(order.items);

  return { orderId: order.id, total: totals.total };
}

function validateOrder(order) {
  if (!order.customer) {
    throw new Error('No customer');
  }
  if (!order.items.length) {
    throw new Error('No items');
  }
}

function calculateOrderTotals(order) {
  const subtotal = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const tax = subtotal * 0.08;
  const total = subtotal + tax;

  return { subtotal, tax, total };
}

function processPayment(customer, total) {
  const payment = chargeCustomer(customer, total);
  if (!payment.success) {
    throw new Error('Payment failed');
  }
  return payment;
}

function sendOrderConfirmation(customer, total) {
  sendEmail(customer.email, 'Order Confirmation', `Total: $${total}`);
}

function updateInventory(items) {
  for (const item of items) {
    updateStock(item.id, -item.quantity);
  }
}
```

**Why this is better:**
- Each function has single responsibility
- Main function reads like documentation
- Each step is testable independently
- No complexity warnings

**Refactoring applied:** Extract Function

**Attribution:** Clean Code, Refactoring patterns

---

### JS-COMPLEX-TERNARY: Replace Nested Ternaries

**ESLint Rule:** no-nested-ternary

**Style Issue:** "Do not nest ternary expressions (no-nested-ternary)"

**Root Cause:** Nested ternary operators are hard to read

**Bad code (ESLint error):**
```javascript
const status = user.isActive ? user.isPremium ? 'premium-active' : 'regular-active' : user.isPremium ? 'premium-inactive' : 'regular-inactive';
```

**Refactored code (if-else):**
```javascript
function getUserStatus(user) {
  if (user.isActive && user.isPremium) {
    return 'premium-active';
  }

  if (user.isActive) {
    return 'regular-active';
  }

  if (user.isPremium) {
    return 'premium-inactive';
  }

  return 'regular-inactive';
}

const status = getUserStatus(user);
```

**Alternative (lookup object):**
```javascript
const statusMap = {
  'true-true': 'premium-active',
  'true-false': 'regular-active',
  'false-true': 'premium-inactive',
  'false-false': 'regular-inactive'
};

const status = statusMap[`${user.isActive}-${user.isPremium}`];
```

**Why this is better:**
- Clear logic flow
- Easy to understand
- Can add more conditions easily
- No cognitive load from nested ternaries

**Refactoring applied:** Replace Nested Ternary with If-Else or Lookup

**Attribution:** Airbnb JavaScript Style Guide

---

### JS-COMPLEX-SWITCH: Use Lookup Objects or Maps

**ESLint Rule:** complexity

**Style Issue:** "Function has too much complexity (complexity)"

**Root Cause:** Long switch statement with many cases

**Bad code (ESLint error):**
```javascript
function getDiscount(customerType) {
  switch (customerType) {
    case 'gold':
      return 0.20;
    case 'silver':
      return 0.15;
    case 'bronze':
      return 0.10;
    case 'new':
      return 0.05;
    case 'student':
      return 0.25;
    case 'senior':
      return 0.30;
    case 'employee':
      return 0.50;
    default:
      return 0.00;
  }
}
```

**Refactored code (object lookup):**
```javascript
const CUSTOMER_DISCOUNTS = {
  gold: 0.20,
  silver: 0.15,
  bronze: 0.10,
  new: 0.05,
  student: 0.25,
  senior: 0.30,
  employee: 0.50
};

function getDiscount(customerType) {
  return CUSTOMER_DISCOUNTS[customerType] ?? 0.00;
}
```

**Alternative (Map for complex logic):**
```javascript
const discountCalculators = new Map([
  ['gold', () => 0.20],
  ['silver', () => 0.15],
  ['bronze', () => 0.10],
  ['new', () => 0.05],
  ['student', (age) => age < 25 ? 0.30 : 0.25],
  ['senior', (age) => age >= 65 ? 0.35 : 0.30],
  ['employee', () => 0.50]
]);

function getDiscount(customerType, age) {
  const calculator = discountCalculators.get(customerType);
  return calculator ? calculator(age) : 0.00;
}
```

**Why this is better:**
- No branching - O(1) lookup
- Easy to add new customer types
- Data separated from logic
- Complexity score minimal

**Refactoring applied:** Replace Switch with Object/Map Lookup

**Attribution:** JavaScript patterns

---

### JS-COMPLEX-CALLBACK: Use Async/Await Instead of Callbacks

**ESLint Rule:** complexity, max-nested-callbacks

**Style Issue:** "Function has too much complexity (complexity)", "Too many nested callbacks (max-nested-callbacks)"

**Root Cause:** Callback hell with nested callbacks

**Bad code (ESLint error):**
```javascript
function processUser(userId, callback) {
  getUser(userId, (err, user) => {
    if (err) return callback(err);

    getOrders(user.id, (err, orders) => {
      if (err) return callback(err);

      processOrders(orders, (err, result) => {
        if (err) return callback(err);

        sendNotification(user.email, result, (err) => {
          if (err) return callback(err);
          callback(null, result);
        });
      });
    });
  });
}
```

**Refactored code (async/await):**
```javascript
async function processUser(userId) {
  const user = await getUser(userId);
  const orders = await getOrders(user.id);
  const result = await processOrders(orders);
  await sendNotification(user.email, result);

  return result;
}
```

**With error handling:**
```javascript
async function processUser(userId) {
  try {
    const user = await getUser(userId);
    const orders = await getOrders(user.id);
    const result = await processOrders(orders);
    await sendNotification(user.email, result);

    return result;
  } catch (error) {
    console.error('Failed to process user:', error);
    throw error;
  }
}
```

**Why this is better:**
- Linear, easy-to-read flow
- No callback nesting
- Standard try/catch error handling
- Complexity greatly reduced

**Refactoring applied:** Convert Callbacks to Async/Await

**Attribution:** Modern JavaScript async patterns

---

### JS-COMPLEX-NESTING: Reduce Nesting Levels

**ESLint Rule:** max-depth

**Style Issue:** "Blocks are nested too deeply (max-depth)"

**Root Cause:** Deep nesting making code hard to read

**Bad code (ESLint error):**
```javascript
function processData(data) {
  if (data) {
    if (data.items) {
      for (const item of data.items) {
        if (item.valid) {
          if (item.value > 0) {
            if (item.category === 'priority') {
              processItem(item);
            }
          }
        }
      }
    }
  }
}
```

**Refactored code (guard clauses + early returns):**
```javascript
function processData(data) {
  if (!data?.items) {
    return;
  }

  for (const item of data.items) {
    if (shouldProcessItem(item)) {
      processItem(item);
    }
  }
}

function shouldProcessItem(item) {
  return item.valid && item.value > 0 && item.category === 'priority';
}
```

**Alternative (filter + forEach):**
```javascript
function processData(data) {
  if (!data?.items) {
    return;
  }

  const priorityItems = data.items.filter(isPriorityItem);
  priorityItems.forEach(processItem);
}

function isPriorityItem(item) {
  return item.valid && item.value > 0 && item.category === 'priority';
}
```

**Why this is better:**
- Guard clauses eliminate nesting
- Filter logic extracted and named
- Happy path is clear
- No deep nesting

**Refactoring applied:** Guard Clauses, Extract Predicate

**Attribution:** Clean Code principles

---

## 3. FUNCTION PARAMETERS

### JS-PARAMS-MANY: Use Destructuring or Options Object

**ESLint Rule:** max-params

**Style Issue:** "Function has too many parameters (max-params)"

**Root Cause:** Too many individual parameters

**Bad code (ESLint error):**
```javascript
function createReport(title, author, date, format, includeCharts, includeSummary, pageSize, orientation) {
  // Implementation
}
```

**Refactored code (options object):**
```javascript
function createReport(options) {
  const {
    title,
    author,
    date,
    format = 'pdf',
    includeCharts = true,
    includeSummary = true,
    pageSize = 'A4',
    orientation = 'portrait'
  } = options;

  // Implementation
}

// Usage:
createReport({
  title: 'Q4 Report',
  author: 'John Doe',
  date: new Date(),
  format: 'pdf',
  includeCharts: false
});
```

**Alternative (separate required and optional):**
```javascript
function createReport(title, author, date, options = {}) {
  const {
    format = 'pdf',
    includeCharts = true,
    includeSummary = true,
    pageSize = 'A4',
    orientation = 'portrait'
  } = options;

  // Implementation
}

// Usage:
createReport('Q4 Report', 'John Doe', new Date(), {
  includeCharts: false
});
```

**Why this is better:**
- Required parameters explicit
- Optional parameters in object
- Self-documenting
- Easy to add new options

**Refactoring applied:** Introduce Options Object

**Attribution:** JavaScript best practices

---

### JS-PARAMS-ORDER: Logical Parameter Order

**ESLint Rule:** N/A (best practice)

**Style Issue:** Confusing parameter order

**Root Cause:** Parameters not in logical order

**Bad code (confusing):**
```javascript
function sendEmail(subject, template, to, from, cc, bcc, attachments, priority) {
  // Implementation
}

// Hard to remember order
sendEmail('Hello', 'welcome.html', 'user@example.com', 'no-reply@example.com', null, null, [], 'high');
```

**Refactored code:**
```javascript
function sendEmail({ to, from, subject, template, cc, bcc, attachments = [], priority = 'normal' }) {
  // Implementation
}

// Self-documenting call
sendEmail({
  to: 'user@example.com',
  from: 'no-reply@example.com',
  subject: 'Hello',
  template: 'welcome.html',
  priority: 'high'
});
```

**Why this is better:**
- Order doesn't matter
- Named parameters are self-documenting
- Can't accidentally mix up parameters
- Optional parameters have defaults

**Refactoring applied:** Use Named Parameters (Object Destructuring)

**Attribution:** JavaScript patterns

---

### JS-PARAMS-BOOLEAN: Avoid Boolean Parameters

**ESLint Rule:** N/A (best practice)

**Style Issue:** Boolean parameter makes intent unclear

**Root Cause:** Boolean flag controlling behavior

**Bad code (unclear intent):**
```javascript
function saveUser(user, sendEmail) {
  // Save user
  if (sendEmail) {
    // Send email
  }
}

// What does true mean?
saveUser(user, true);
```

**Refactored code (options object):**
```javascript
function saveUser(user, options = {}) {
  const { sendEmail = false } = options;

  // Save user
  if (sendEmail) {
    // Send email
  }
}

// Clear intent
saveUser(user, { sendEmail: true });
```

**Alternative (separate functions):**
```javascript
function saveUser(user) {
  // Save user logic
}

function saveUserAndSendEmail(user) {
  saveUser(user);
  sendWelcomeEmail(user);
}

// Intent is clear from function name
saveUserAndSendEmail(user);
```

**Why this is better:**
- Intent is clear at call site
- Named parameters self-document
- Or separate functions for different behaviors
- No boolean confusion

**Refactoring applied:** Replace Boolean Parameter with Options or Separate Functions

**Attribution:** Clean Code

---

### JS-PARAMS-DEFAULT: Use Default Parameters

**ESLint Rule:** default-param-last

**Style Issue:** Default values not using default parameter syntax

**Root Cause:** Manual default value assignment

**Bad code (old style):**
```javascript
function createUser(name, role, status) {
  role = role || 'user';
  status = status || 'active';

  return { name, role, status };
}
```

**Refactored code:**
```javascript
function createUser(name, role = 'user', status = 'active') {
  return { name, role, status };
}
```

**With object destructuring:**
```javascript
function createUser({ name, role = 'user', status = 'active' } = {}) {
  return { name, role, status };
}

// Usage:
createUser({ name: 'John' }); // Uses defaults for role and status
createUser({ name: 'Jane', role: 'admin' }); // Uses default for status
```

**Why this is better:**
- Default parameters are explicit
- Works correctly with falsy values (0, false, '')
- Self-documenting
- Standard ES6+ syntax

**Refactoring applied:** Use Default Parameters

**Attribution:** ES6+ features

---

## 4. REACT/JSX

### JS-JSX-LONG: Extract JSX Components

**ESLint Rule:** max-len, react/jsx-max-depth

**Style Issue:** "Line exceeds 100 characters (max-len)", "JSX is nested too deeply (react/jsx-max-depth)"

**Root Cause:** Complex JSX in a single component

**Bad code (ESLint error):**
```jsx
function UserDashboard({ user, orders, notifications }) {
  return (
    <div className="dashboard">
      <div className="header">
        <img src={user.avatar} alt={user.name} />
        <div className="user-info">
          <h1>{user.name}</h1>
          <p>{user.email}</p>
          <span className="badge">{user.role}</span>
        </div>
      </div>
      <div className="content">
        <div className="orders">
          <h2>Recent Orders</h2>
          {orders.map(order => (
            <div key={order.id} className="order">
              <span>#{order.id}</span>
              <span>${order.total}</span>
              <span>{order.status}</span>
              <button onClick={() => viewOrder(order.id)}>View</button>
            </div>
          ))}
        </div>
        <div className="notifications">
          <h2>Notifications</h2>
          {notifications.map(notification => (
            <div key={notification.id} className="notification">
              <span>{notification.message}</span>
              <span>{notification.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

**Refactored code:**
```jsx
function UserDashboard({ user, orders, notifications }) {
  return (
    <div className="dashboard">
      <DashboardHeader user={user} />
      <DashboardContent orders={orders} notifications={notifications} />
    </div>
  );
}

function DashboardHeader({ user }) {
  return (
    <div className="header">
      <UserAvatar user={user} />
      <UserInfo user={user} />
    </div>
  );
}

function UserAvatar({ user }) {
  return <img src={user.avatar} alt={user.name} />;
}

function UserInfo({ user }) {
  return (
    <div className="user-info">
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <span className="badge">{user.role}</span>
    </div>
  );
}

function DashboardContent({ orders, notifications }) {
  return (
    <div className="content">
      <OrdersList orders={orders} />
      <NotificationsList notifications={notifications} />
    </div>
  );
}

function OrdersList({ orders }) {
  return (
    <div className="orders">
      <h2>Recent Orders</h2>
      {orders.map(order => (
        <OrderItem key={order.id} order={order} />
      ))}
    </div>
  );
}

function OrderItem({ order }) {
  return (
    <div className="order">
      <span>#{order.id}</span>
      <span>${order.total}</span>
      <span>{order.status}</span>
      <button onClick={() => viewOrder(order.id)}>View</button>
    </div>
  );
}

function NotificationsList({ notifications }) {
  return (
    <div className="notifications">
      <h2>Notifications</h2>
      {notifications.map(notification => (
        <NotificationItem key={notification.id} notification={notification} />
      ))}
    </div>
  );
}

function NotificationItem({ notification }) {
  return (
    <div className="notification">
      <span>{notification.message}</span>
      <span>{notification.date}</span>
    </div>
  );
}
```

**Why this is better:**
- Each component has single responsibility
- Components are reusable
- Easy to test individually
- Shallow JSX nesting
- More maintainable

**Refactoring applied:** Extract Component

**Attribution:** React best practices

---

### JS-JSX-PROPS: Extract Props Object

**ESLint Rule:** react/jsx-max-props-per-line

**Style Issue:** "Too many props on a single line (react/jsx-max-props-per-line)"

**Root Cause:** Component with many props

**Bad code (ESLint error):**
```jsx
<UserCard id={user.id} name={user.name} email={user.email} avatar={user.avatar} role={user.role} status={user.status} createdAt={user.createdAt} lastLogin={user.lastLogin} />
```

**Refactored code (multi-line props):**
```jsx
<UserCard
  id={user.id}
  name={user.name}
  email={user.email}
  avatar={user.avatar}
  role={user.role}
  status={user.status}
  createdAt={user.createdAt}
  lastLogin={user.lastLogin}
/>
```

**Better refactored code (pass object):**
```jsx
<UserCard user={user} />

// Component definition:
function UserCard({ user }) {
  const { id, name, email, avatar, role, status, createdAt, lastLogin } = user;

  return (
    <div className="user-card">
      {/* Use destructured values */}
    </div>
  );
}
```

**Alternative (spread if appropriate):**
```jsx
<UserCard {...user} />

// Only if UserCard explicitly expects these props
function UserCard({ id, name, email, avatar, role, status, createdAt, lastLogin }) {
  return (
    <div className="user-card">
      {/* Use props */}
    </div>
  );
}
```

**Why this is better:**
- Cleaner JSX
- Less prop drilling
- Easier to pass all related data
- Fewer lines

**Refactoring applied:** Pass Object Instead of Individual Props

**Attribution:** React patterns

---

### JS-JSX-CONDITION: Extract Conditional Logic

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Complex conditional rendering inline

**Bad code (ESLint error):**
```jsx
function UserStatus({ user }) {
  return (
    <div>
      {user.isActive && user.isPremium && !user.isSuspended && user.emailVerified ? <PremiumBadge /> : user.isActive && !user.isSuspended ? <ActiveBadge /> : <InactiveBadge />}
    </div>
  );
}
```

**Refactored code (extract function):**
```jsx
function UserStatus({ user }) {
  const getBadge = () => {
    if (isPremiumActive(user)) {
      return <PremiumBadge />;
    }

    if (isActive(user)) {
      return <ActiveBadge />;
    }

    return <InactiveBadge />;
  };

  return <div>{getBadge()}</div>;
}

function isPremiumActive(user) {
  return user.isActive && user.isPremium && !user.isSuspended && user.emailVerified;
}

function isActive(user) {
  return user.isActive && !user.isSuspended;
}
```

**Alternative (separate component):**
```jsx
function UserStatus({ user }) {
  return (
    <div>
      <StatusBadge user={user} />
    </div>
  );
}

function StatusBadge({ user }) {
  if (isPremiumActive(user)) {
    return <PremiumBadge />;
  }

  if (isActive(user)) {
    return <ActiveBadge />;
  }

  return <InactiveBadge />;
}
```

**Why this is better:**
- Conditional logic is clear
- Each condition is named
- Easy to test
- JSX is clean

**Refactoring applied:** Extract Conditional Logic

**Attribution:** React patterns

---

### JS-JSX-MAP: Extract Map Callbacks

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Complex callback inside map

**Bad code (ESLint error):**
```jsx
function OrdersList({ orders }) {
  return (
    <div>
      {orders.map(order => <div key={order.id} className="order"><span>#{order.id}</span><span>${order.total}</span><span>{order.status}</span><button onClick={() => viewOrder(order.id)}>View</button></div>)}
    </div>
  );
}
```

**Refactored code (extract component):**
```jsx
function OrdersList({ orders }) {
  return (
    <div>
      {orders.map(order => (
        <OrderItem key={order.id} order={order} />
      ))}
    </div>
  );
}

function OrderItem({ order }) {
  return (
    <div className="order">
      <span>#{order.id}</span>
      <span>${order.total}</span>
      <span>{order.status}</span>
      <button onClick={() => viewOrder(order.id)}>View</button>
    </div>
  );
}
```

**Why this is better:**
- Map callback is simple
- OrderItem component is reusable
- Easy to test
- Cleaner JSX

**Refactoring applied:** Extract Component from Map

**Attribution:** React best practices

---

### JS-JSX-INLINE: Avoid Inline Functions (When Needed)

**ESLint Rule:** react/jsx-no-bind

**Style Issue:** "JSX props should not use arrow functions (react/jsx-no-bind)"

**Root Cause:** Creating new function on every render

**Bad code (ESLint warning):**
```jsx
function UserList({ users }) {
  return (
    <div>
      {users.map(user => (
        <button key={user.id} onClick={() => handleDelete(user.id)}>
          Delete {user.name}
        </button>
      ))}
    </div>
  );
}
```

**Refactored code (useCallback for performance):**
```jsx
function UserList({ users, onDelete }) {
  const handleDelete = useCallback((userId) => {
    onDelete(userId);
  }, [onDelete]);

  return (
    <div>
      {users.map(user => (
        <UserDeleteButton
          key={user.id}
          user={user}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}

function UserDeleteButton({ user, onDelete }) {
  const handleClick = () => onDelete(user.id);

  return (
    <button onClick={handleClick}>
      Delete {user.name}
    </button>
  );
}
```

**Note:** In modern React, inline functions are often fine. Only optimize when you have performance issues.

**Why this is better (when needed):**
- Avoids creating new functions on every render
- Better performance for large lists
- Memoization works better

**Refactoring applied:** Extract Event Handler, Use useCallback

**Attribution:** React performance patterns

---

### JS-JSX-STYLE: Extract Style Objects

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Long inline style object

**Bad code (ESLint error):**
```jsx
function Card({ title }) {
  return (
    <div style={{ padding: '20px', margin: '10px', backgroundColor: '#f0f0f0', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
      <h2>{title}</h2>
    </div>
  );
}
```

**Refactored code (extract style object):**
```jsx
const cardStyle = {
  padding: '20px',
  margin: '10px',
  backgroundColor: '#f0f0f0',
  borderRadius: '8px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
};

function Card({ title }) {
  return (
    <div style={cardStyle}>
      <h2>{title}</h2>
    </div>
  );
}
```

**Better refactored code (CSS module or styled component):**
```jsx
// Using CSS module
import styles from './Card.module.css';

function Card({ title }) {
  return (
    <div className={styles.card}>
      <h2>{title}</h2>
    </div>
  );
}

// Or using styled-components
import styled from 'styled-components';

const StyledCard = styled.div`
  padding: 20px;
  margin: 10px;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

function Card({ title }) {
  return (
    <StyledCard>
      <h2>{title}</h2>
    </StyledCard>
  );
}
```

**Why this is better:**
- Styles are reusable
- JSX is cleaner
- Easier to maintain styles
- Better separation of concerns

**Refactoring applied:** Extract Style Object or Use CSS-in-JS

**Attribution:** React styling best practices

---

## 5. ARRAY/OBJECT

### JS-OBJ-LONG: Multi-line Objects

**ESLint Rule:** object-curly-newline, object-property-newline

**Style Issue:** "Object literal should have line breaks (object-curly-newline)"

**Root Cause:** Object with many properties on one line

**Bad code (ESLint error):**
```javascript
const user = { id: 1, name: 'John Doe', email: 'john@example.com', role: 'admin', status: 'active', createdAt: new Date(), lastLogin: new Date() };
```

**Refactored code:**
```javascript
const user = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  role: 'admin',
  status: 'active',
  createdAt: new Date(),
  lastLogin: new Date()
};
```

**Why this is better:**
- Each property on its own line
- Easy to add/remove properties
- Better git diffs
- More readable

**Refactoring applied:** Multi-line Object Literal

**Attribution:** Prettier, Airbnb Style Guide

---

### JS-ARRAY-LONG: Multi-line Arrays

**ESLint Rule:** array-element-newline

**Style Issue:** "Array elements should have line breaks (array-element-newline)"

**Root Cause:** Array with many elements on one line

**Bad code (ESLint error):**
```javascript
const colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'white'];

const users = [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }, { id: 3, name: 'Bob' }, { id: 4, name: 'Alice' }];
```

**Refactored code:**
```javascript
const colors = [
  'red',
  'blue',
  'green',
  'yellow',
  'orange',
  'purple',
  'pink',
  'brown',
  'black',
  'white'
];

const users = [
  { id: 1, name: 'John' },
  { id: 2, name: 'Jane' },
  { id: 3, name: 'Bob' },
  { id: 4, name: 'Alice' }
];
```

**Why this is better:**
- Each element on its own line
- Easy to add/remove elements
- Better git diffs
- Trailing commas prevent diff noise

**Refactoring applied:** Multi-line Array Literal

**Attribution:** Prettier, Airbnb Style Guide

---

### JS-OBJ-COMPUTED: Extract Computed Properties

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Complex computed property names or values

**Bad code (ESLint error):**
```javascript
const config = {
  [getUserRole(user) + '_' + getEnvironment()]: getConfigValue(user, environment, 'permission'),
  [getNamespace() + '_' + getVersion()]: getFeatureFlags(namespace, version)
};
```

**Refactored code:**
```javascript
const roleEnvKey = `${getUserRole(user)}_${getEnvironment()}`;
const roleEnvValue = getConfigValue(user, environment, 'permission');

const namespaceVersionKey = `${getNamespace()}_${getVersion()}`;
const namespaceVersionValue = getFeatureFlags(namespace, version);

const config = {
  [roleEnvKey]: roleEnvValue,
  [namespaceVersionKey]: namespaceVersionValue
};
```

**Why this is better:**
- Complex computations are named
- Easy to debug intermediate values
- No line length issues
- Self-documenting

**Refactoring applied:** Extract Variable for Computed Properties

**Attribution:** JavaScript patterns

---

### JS-SPREAD-LONG: Multi-line Spreads

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Multiple spread operations on one line

**Bad code (ESLint error):**
```javascript
const merged = { ...defaultConfig, ...userConfig, ...environmentConfig, ...featureFlags, timestamp: Date.now() };
```

**Refactored code:**
```javascript
const merged = {
  ...defaultConfig,
  ...userConfig,
  ...environmentConfig,
  ...featureFlags,
  timestamp: Date.now()
};
```

**Alternative (explicit merge for clarity):**
```javascript
const baseConfig = { ...defaultConfig, ...userConfig };
const fullConfig = { ...baseConfig, ...environmentConfig };
const merged = {
  ...fullConfig,
  ...featureFlags,
  timestamp: Date.now()
};
```

**Why this is better:**
- Each spread on its own line
- Merge order is clear
- Easy to add/remove spreads
- Better for git diffs

**Refactoring applied:** Multi-line Spread Syntax

**Attribution:** JavaScript patterns

---

## 6. STRING/TEMPLATE

### JS-STRING-CONCAT: Use Template Literals

**ESLint Rule:** prefer-template

**Style Issue:** "Use template literals instead of string concatenation (prefer-template)"

**Root Cause:** Using + for string concatenation

**Bad code (ESLint error):**
```javascript
const message = 'Hello ' + user.firstName + ' ' + user.lastName + ', your order #' + order.id + ' totals $' + order.total + '.';
```

**Refactored code:**
```javascript
const message = `Hello ${user.firstName} ${user.lastName}, your order #${order.id} totals $${order.total}.`;
```

**Why this is better:**
- More readable
- No string concatenation
- Easier to add/modify parts
- Standard ES6+ syntax

**Refactoring applied:** Use Template Literals

**Attribution:** ES6+ features, ESLint prefer-template

---

### JS-TEMPLATE-LONG: Multi-line Templates

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Long template literal on single line

**Bad code (ESLint error):**
```javascript
const html = `<div class="card"><h1>${title}</h1><p>${description}</p><button onclick="action('${id}')">Click</button></div>`;
```

**Refactored code:**
```javascript
const html = `
  <div class="card">
    <h1>${title}</h1>
    <p>${description}</p>
    <button onclick="action('${id}')">Click</button>
  </div>
`.trim();
```

**Why this is better:**
- Template is readable
- Proper HTML/markup formatting
- Easy to modify structure
- No line length issues

**Refactoring applied:** Multi-line Template Literal

**Attribution:** ES6+ template literals

---

### JS-TEMPLATE-COMPLEX: Extract Template Parts

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Complex expressions in template

**Bad code (ESLint error):**
```javascript
const message = `User ${user.firstName} ${user.lastName} (${user.role.toUpperCase()}) ordered ${order.items.length} items totaling $${order.items.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2)} on ${new Date(order.date).toLocaleDateString()}.`;
```

**Refactored code:**
```javascript
const userName = `${user.firstName} ${user.lastName}`;
const userRole = user.role.toUpperCase();
const itemCount = order.items.length;
const orderTotal = order.items
  .reduce((sum, item) => sum + item.price * item.quantity, 0)
  .toFixed(2);
const orderDate = new Date(order.date).toLocaleDateString();

const message = `User ${userName} (${userRole}) ordered ${itemCount} items totaling $${orderTotal} on ${orderDate}.`;
```

**Why this is better:**
- Complex calculations extracted and named
- Template is readable
- Easy to debug individual parts
- Can reuse extracted values

**Refactoring applied:** Extract Variable for Template Parts

**Attribution:** JavaScript patterns

---

### JS-STRING-SPLIT: Split Long Strings

**ESLint Rule:** max-len

**Style Issue:** "Line exceeds 100 characters (max-len)"

**Root Cause:** Long string literal

**Bad code (ESLint error):**
```javascript
const error = 'An unexpected error occurred while processing your request. Please try again later or contact support if the problem persists.';
```

**Refactored code (multi-line template):**
```javascript
const error = `
  An unexpected error occurred while processing your request.
  Please try again later or contact support if the problem persists.
`.trim();
```

**Alternative (join array):**
```javascript
const error = [
  'An unexpected error occurred while processing your request.',
  'Please try again later or contact support if the problem persists.'
].join(' ');
```

**Why this is better:**
- String is readable
- Easy to modify parts
- No line length issues
- Natural line breaks

**Refactoring applied:** Multi-line String

**Attribution:** JavaScript patterns

---

# End of Guidelines

Remember: When ESLint complains, don't just wrap the line or disable the rule—refactor the code so the issue disappears naturally. Good structure leads to good style automatically.
