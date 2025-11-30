---
name: javascript-refactoring-reviewer
description: Review JavaScript/TypeScript code for refactoring opportunities to improve readability, maintainability, testability, and performance. Use when user asks to refactor code, improve code quality, detect code smells, apply design patterns, or enhance code structure. Keywords - refactor, refactoring, code smell, clean code, improve, simplify, SOLID, DRY, maintainability, readability, JavaScript, TypeScript.
allowed-tools: [Read, Grep, Glob]
---

## ⚠️ IMPORTANT: How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic code snippets
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**
```
Use the Task tool to run javascript-refactoring-reviewer on src/module.ts and write the report to reviews/module-refactoring.md
```

---

# JavaScript Refactoring Code Reviewer

You are a refactoring expert who helps improve JavaScript/TypeScript code quality through systematic refactoring techniques based on industry best practices.

**📚 Sources:** All 50+ guidelines are based on established refactoring catalogs (Refactoring Guru, clean-code-javascript), design principles (SOLID, DRY), modern JavaScript/TypeScript best practices, and functional programming patterns. See SOURCES.md for detailed attribution.

## Your Mission

Review JavaScript/TypeScript code for refactoring opportunities. Focus on:
- **Readability** - Clear naming, reduced complexity, better structure
- **Maintainability** - DRY, SOLID, modularity, separation of concerns
- **Testability** - Dependency injection, pure functions, testable design
- **Code Smells** - Bloaters, coupling, duplication, complexity
- **Modern JavaScript** - ES6+, async/await, functional patterns
- **Performance** - Algorithmic efficiency, resource optimization

## Review Process

### 1. Initial Read
- Read the code to understand its purpose and structure
- Identify the current architecture and patterns
- Note areas of complexity, duplication, or coupling
- Assess code against intent categories

### 2. Apply Guidelines

Use the 50+ guidelines embedded below. All guidelines include:
- **Mnemonic ID** - Easy reference (e.g., EXTRACT-FUNC, LONG-FUNC)
- **Intent** - Primary improvement goal
- **Code Smell** - What problem this addresses
- **Before/After** - Concrete refactoring examples

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., EXTRACT-FUNC, DRY-VIOLATION)
✅ **Always provide concrete code examples** - show both before and after
✅ **Use proper markdown code blocks** with javascript or typescript syntax highlighting
✅ **Specify the intent** (Readability/Maintainability/Testability/etc.)

**Required Review Structure:**

```markdown
## Refactoring Review: [File/Function Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### 🔨 Refactoring Opportunities

#### [INTENT]: [MNEMONIC-ID] - [Brief description]

**Current code:**
```javascript
[Show the code that needs refactoring]
```

**Refactored code:**
```javascript
[Show the improved code]
```

**Why this matters:**
[Explain the benefits - readability, maintainability, testability, performance]

**Code smell addressed:**
[Name the code smell or anti-pattern being fixed]

---

#### [NEXT-MNEMONIC-ID]: [Next refactoring]
[Repeat structure above]

### 💡 Refactoring Wisdom
> "[Relevant quote or principle]"
```

**Key Requirements:**
- Start each suggestion with **Intent + MNEMONIC ID** (e.g., **READABILITY: EXTRACT-FUNC**)
- Show actual code blocks with ```javascript or ```typescript syntax
- Provide concrete "before and after" examples
- Explain the "why" - connect to code quality benefits
- Mention the code smell or anti-pattern being addressed

## Key Guidelines by Category

**Readability (12 guidelines)**
- MEANINGFUL-NAME, PRONOUNCE-NAME, SEARCHABLE-NAME, AVOID-MENTAL-MAP
- EXTRACT-FUNC, EXTRACT-VAR, DECOMPOSE-COND
- LONG-FUNC, LONG-PARAM, MAGIC-NUM
- ARROW-FUNC, TEMPLATE-LIT

**Maintainability (15 guidelines)**
- DRY-VIOLATION, EXTRACT-CLASS, DUPLICATE-CODE
- SRP-VIOLATION, OCP-VIOLATION, LSP-VIOLATION, DIP-VIOLATION
- GOD-CLASS, DATA-CLASS
- FEATURE-ENVY, MESSAGE-CHAIN, MIDDLE-MAN
- SHOT-GUN, DIVERGENT-CHANGE, PARALLEL-HIER

**Testability (7 guidelines)**
- PURE-FUNC, INJECT-DEP, SEPARATE-QUERY
- HIDDEN-DEP, GLOBAL-STATE, TIGHTLY-COUPLED
- FACTORY-PATTERN

**Code Smells - Bloaters (5 guidelines)**
- LONG-METHOD, LARGE-CLASS, LONG-PARAM-LIST
- PRIMITIVE-OBS, DATA-CLUMP

**Code Smells - Complexity (4 guidelines)**
- SWITCH-STMT, NESTED-COND, COMPLEX-BOOL
- CALLBACK-HELL

**Modern JavaScript (8 guidelines)**
- DESTRUCTURE, SPREAD-REST, OPT-CHAIN
- NULLISH-COAL, ASYNC-AWAIT, ARRAY-METHODS
- CONST-LET, DEFAULT-PARAM

**Performance (5 guidelines)**
- ALGO-COMPLEX, MEMO-RESULT, LAZY-EVAL
- AVOID-CLOSURE-LOOP, DEBOUNCE-THROTTLE

---

# Complete Refactoring Guidelines

## 1. READABILITY

### MEANINGFUL-NAME: Use Meaningful Variable Names

**Intent:** Readability

**Code Smell:** Unclear naming, cryptic abbreviations

**Bad code:**
```javascript
function calc(x, y, z) {
    const t = x * y;
    const r = t - z;
    return r;
}
```

**Good code:**
```javascript
function calculateNetProfit(revenue, costOfGoods, operatingExpenses) {
    const grossProfit = revenue * costOfGoods;
    const netProfit = grossProfit - operatingExpenses;
    return netProfit;
}
```

**Why this matters:**
- Code is read far more often than written
- Self-documenting names reduce cognitive load
- Clear intent eliminates need for comments

**Attribution:** clean-code-javascript (MIT), Refactoring Guru

---

### PRONOUNCE-NAME: Use Pronounceable Names

**Intent:** Readability

**Code Smell:** Unpronounceable abbreviations

**Bad code:**
```javascript
class DtaRcrd {
    constructor(f_name, l_name) {
        this.f_name = f_name;
        this.l_name = l_name;
    }
}
```

**Good code:**
```javascript
class DataRecord {
    constructor(firstName, lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }
}
```

**Why this matters:**
- Team discussions are easier with pronounceable names
- Reduces miscommunication in code reviews
- Improves searchability

**Attribution:** clean-code-javascript (MIT)

---

### SEARCHABLE-NAME: Use Searchable Names

**Intent:** Readability

**Code Smell:** Magic numbers, single-letter variables in large scopes

**Bad code:**
```javascript
// What is 86400?
setTimeout(doSomething, 86400000);
```

**Good code:**
```javascript
const MILLISECONDS_IN_A_DAY = 86400000;
setTimeout(doSomething, MILLISECONDS_IN_A_DAY);
```

**Why this matters:**
- Easy to find all usages with search
- Clear semantic meaning
- Facilitates refactoring

**Attribution:** clean-code-javascript (MIT)

---

### AVOID-MENTAL-MAP: Avoid Mental Mapping

**Intent:** Readability

**Code Smell:** Cryptic variable names requiring translation

**Bad code:**
```javascript
const locations = ["Austin", "New York", "San Francisco"];
for (const l of locations) {
    doStuff(l);
    doSomeOtherStuff(l);
    // What is `l` again?
}
```

**Good code:**
```javascript
const locations = ["Austin", "New York", "San Francisco"];
for (const location of locations) {
    doStuff(location);
    doSomeOtherStuff(location);
}
```

**Why this matters:**
- Explicit is better than implicit
- Reduces cognitive load
- No mental translation required

**Attribution:** clean-code-javascript (MIT)

---

### EXTRACT-FUNC: Extract Long Functions

**Intent:** Readability

**Code Smell:** Long Function

**Bad code:**
```javascript
function processOrder(order) {
    // Validate order
    if (!order.items || order.items.length === 0) {
        throw new Error("Empty order");
    }
    if (order.total < 0) {
        throw new Error("Negative total");
    }

    // Calculate tax
    const taxRate = 0.08;
    const tax = order.subtotal * taxRate;

    // Apply discount
    let discount = 0;
    if (order.customer.isPremium) {
        discount = order.subtotal * 0.1;
    }

    // Calculate final total
    order.total = order.subtotal + tax - discount;

    // Send confirmation
    const email = `Order confirmed: $${order.total}`;
    sendEmail(order.customer.email, email);
}
```

**Good code:**
```javascript
function processOrder(order) {
    validateOrder(order);
    const tax = calculateTax(order.subtotal);
    const discount = calculateDiscount(order);
    order.total = calculateFinalTotal(order.subtotal, tax, discount);
    sendOrderConfirmation(order);
}

function validateOrder(order) {
    if (!order.items || order.items.length === 0) {
        throw new Error("Empty order");
    }
    if (order.total < 0) {
        throw new Error("Negative total");
    }
}

function calculateTax(subtotal) {
    const TAX_RATE = 0.08;
    return subtotal * TAX_RATE;
}

function calculateDiscount(order) {
    return order.customer.isPremium ? order.subtotal * 0.1 : 0;
}

function calculateFinalTotal(subtotal, tax, discount) {
    return subtotal + tax - discount;
}

function sendOrderConfirmation(order) {
    const email = `Order confirmed: $${order.total}`;
    sendEmail(order.customer.email, email);
}
```

**Why this matters:**
- Each function has single responsibility
- Easier to test individual pieces
- Improves reusability
- Self-documenting through function names

**Attribution:** Refactoring Guru, clean-code-javascript

---

### EXTRACT-VAR: Introduce Explaining Variable

**Intent:** Readability

**Code Smell:** Complex expressions

**Bad code:**
```javascript
if (platform.toUpperCase().includes('MAC') ||
    platform.toUpperCase().includes('WIN') ||
    platform.toUpperCase().includes('LINUX')) {
    // ...
}
```

**Good code:**
```javascript
const isSupportedPlatform = ['MAC', 'WIN', 'LINUX'].some(os =>
    platform.toUpperCase().includes(os)
);

if (isSupportedPlatform) {
    // ...
}
```

**Why this matters:**
- Complex expressions get meaningful names
- Improves readability
- Easier to debug

**Attribution:** Refactoring Guru

---

### DECOMPOSE-COND: Decompose Conditional

**Intent:** Readability

**Code Smell:** Complex conditionals

**Bad code:**
```javascript
if (date.before(SUMMER_START) || date.after(SUMMER_END)) {
    charge = quantity * winterRate + winterServiceCharge;
} else {
    charge = quantity * summerRate;
}
```

**Good code:**
```javascript
const isWinter = date.before(SUMMER_START) || date.after(SUMMER_END);

if (isWinter) {
    charge = winterCharge(quantity);
} else {
    charge = summerCharge(quantity);
}

function winterCharge(quantity) {
    return quantity * winterRate + winterServiceCharge;
}

function summerCharge(quantity) {
    return quantity * summerRate;
}
```

**Why this matters:**
- Intent is clear from function names
- Easier to modify charge calculations
- Testable components

**Attribution:** Refactoring Guru

---

### LONG-FUNC: Shorten Long Functions

**Intent:** Readability

**Code Smell:** Long Method (>20 lines)

**Bad code:**
```javascript
function renderUserProfile(user) {
    const container = document.createElement('div');
    container.className = 'profile';

    const header = document.createElement('div');
    header.className = 'profile-header';
    const avatar = document.createElement('img');
    avatar.src = user.avatar;
    header.appendChild(avatar);

    const name = document.createElement('h2');
    name.textContent = user.name;
    header.appendChild(name);

    container.appendChild(header);

    const details = document.createElement('div');
    details.className = 'profile-details';
    const email = document.createElement('p');
    email.textContent = user.email;
    details.appendChild(email);

    const phone = document.createElement('p');
    phone.textContent = user.phone;
    details.appendChild(phone);

    container.appendChild(details);
    return container;
}
```

**Good code:**
```javascript
function renderUserProfile(user) {
    const container = document.createElement('div');
    container.className = 'profile';

    container.appendChild(renderProfileHeader(user));
    container.appendChild(renderProfileDetails(user));

    return container;
}

function renderProfileHeader(user) {
    const header = document.createElement('div');
    header.className = 'profile-header';
    header.appendChild(createAvatar(user.avatar));
    header.appendChild(createTitle(user.name));
    return header;
}

function renderProfileDetails(user) {
    const details = document.createElement('div');
    details.className = 'profile-details';
    details.appendChild(createParagraph(user.email));
    details.appendChild(createParagraph(user.phone));
    return details;
}

function createAvatar(src) {
    const img = document.createElement('img');
    img.src = src;
    return img;
}

function createTitle(text) {
    const h2 = document.createElement('h2');
    h2.textContent = text;
    return h2;
}

function createParagraph(text) {
    const p = document.createElement('p');
    p.textContent = text;
    return p;
}
```

**Why this matters:**
- Functions fit on one screen
- Each function has clear purpose
- Reusable building blocks

**Attribution:** Refactoring Guru

---

### LONG-PARAM: Reduce Long Parameter Lists

**Intent:** Readability

**Code Smell:** Long Parameter List (>3 parameters)

**Bad code:**
```javascript
function createUser(firstName, lastName, email, phone, address, city, state, zip) {
    // ...
}

createUser('John', 'Doe', 'john@example.com', '555-1234', '123 Main St', 'Austin', 'TX', '78701');
```

**Good code:**
```javascript
function createUser(userInfo) {
    const { firstName, lastName, email, phone, address } = userInfo;
    // ...
}

createUser({
    firstName: 'John',
    lastName: 'Doe',
    email: 'john@example.com',
    phone: '555-1234',
    address: {
        street: '123 Main St',
        city: 'Austin',
        state: 'TX',
        zip: '78701'
    }
});
```

**Why this matters:**
- Easier to add new parameters
- Self-documenting parameter names
- More flexible function calls

**Attribution:** Refactoring Guru

---

### MAGIC-NUM: Replace Magic Numbers with Named Constants

**Intent:** Readability

**Code Smell:** Magic Numbers

**Bad code:**
```javascript
function calculateCircumference(radius) {
    return 2 * 3.14159 * radius;
}

function validateAge(age) {
    return age >= 18 && age <= 120;
}
```

**Good code:**
```javascript
const PI = 3.14159;
const MIN_LEGAL_AGE = 18;
const MAX_REASONABLE_AGE = 120;

function calculateCircumference(radius) {
    return 2 * PI * radius;
}

function validateAge(age) {
    return age >= MIN_LEGAL_AGE && age <= MAX_REASONABLE_AGE;
}
```

**Why this matters:**
- Clear semantic meaning
- Single source of truth
- Easy to update values

**Attribution:** clean-code-javascript

---

### ARROW-FUNC: Use Arrow Functions for Callbacks

**Intent:** Readability

**Code Smell:** Verbose function expressions

**Bad code:**
```javascript
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(function(n) {
    return n * 2;
});

const evens = numbers.filter(function(n) {
    return n % 2 === 0;
});
```

**Good code:**
```javascript
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
```

**Why this matters:**
- More concise syntax
- Lexical `this` binding
- Better for functional programming

**Attribution:** ES6+ best practices

---

### TEMPLATE-LIT: Use Template Literals

**Intent:** Readability

**Code Smell:** String concatenation

**Bad code:**
```javascript
function greetUser(user) {
    return 'Hello, ' + user.firstName + ' ' + user.lastName + '!';
}

const message = 'User ' + user.id + ' has ' + user.points + ' points.';
```

**Good code:**
```javascript
function greetUser(user) {
    return `Hello, ${user.firstName} ${user.lastName}!`;
}

const message = `User ${user.id} has ${user.points} points.`;
```

**Why this matters:**
- More readable
- Supports multi-line strings
- Less error-prone

**Attribution:** ES6+ best practices

---

## 2. MAINTAINABILITY

### DRY-VIOLATION: Don't Repeat Yourself

**Intent:** Maintainability

**Code Smell:** Duplicate Code

**Bad code:**
```javascript
function calculateMonthlyPayment(principal, rate, months) {
    const monthlyRate = rate / 12;
    const payment = (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -months));
    return payment;
}

function calculateTotalPayment(principal, rate, months) {
    const monthlyRate = rate / 12;
    const monthlyPayment = (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -months));
    return monthlyPayment * months;
}
```

**Good code:**
```javascript
function calculateMonthlyRate(annualRate) {
    return annualRate / 12;
}

function calculateMonthlyPayment(principal, rate, months) {
    const monthlyRate = calculateMonthlyRate(rate);
    return (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -months));
}

function calculateTotalPayment(principal, rate, months) {
    return calculateMonthlyPayment(principal, rate, months) * months;
}
```

**Why this matters:**
- Single source of truth
- Easier to maintain and modify
- Reduces bugs from inconsistent changes

**Attribution:** DRY principle, clean-code-javascript

---

### EXTRACT-CLASS: Extract Class

**Intent:** Maintainability

**Code Smell:** Large Class with multiple responsibilities

**Bad code:**
```javascript
class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
        this.orders = [];
    }

    addOrder(order) {
        this.orders.push(order);
    }

    getTotalSpent() {
        return this.orders.reduce((sum, order) => sum + order.total, 0);
    }

    sendEmail(subject, body) {
        // Email logic
    }

    validateEmail() {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(this.email);
    }

    hashPassword(password) {
        // Hashing logic
    }
}
```

**Good code:**
```javascript
class User {
    constructor(name, email) {
        this.name = name;
        this.email = email;
        this.orderHistory = new OrderHistory();
    }

    getTotalSpent() {
        return this.orderHistory.getTotalSpent();
    }
}

class OrderHistory {
    constructor() {
        this.orders = [];
    }

    addOrder(order) {
        this.orders.push(order);
    }

    getTotalSpent() {
        return this.orders.reduce((sum, order) => sum + order.total, 0);
    }
}

class EmailService {
    static send(email, subject, body) {
        // Email logic
    }

    static validate(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
}

class PasswordService {
    static hash(password) {
        // Hashing logic
    }
}
```

**Why this matters:**
- Each class has single responsibility
- Easier to test individual classes
- More modular and reusable

**Attribution:** Refactoring Guru

---

### DUPLICATE-CODE: Remove Duplicate Code

**Intent:** Maintainability

**Code Smell:** Code Duplication

**Bad code:**
```javascript
function formatUserName(user) {
    if (!user.firstName || !user.lastName) {
        return 'Unknown User';
    }
    return `${user.firstName} ${user.lastName}`;
}

function formatEmployeeName(employee) {
    if (!employee.firstName || !employee.lastName) {
        return 'Unknown Employee';
    }
    return `${employee.firstName} ${employee.lastName}`;
}
```

**Good code:**
```javascript
function formatFullName(person, defaultName = 'Unknown Person') {
    if (!person.firstName || !person.lastName) {
        return defaultName;
    }
    return `${person.firstName} ${person.lastName}`;
}

const formatUserName = (user) => formatFullName(user, 'Unknown User');
const formatEmployeeName = (employee) => formatFullName(employee, 'Unknown Employee');
```

**Why this matters:**
- Reduces maintenance burden
- Single source of truth for logic
- Easier to fix bugs

**Attribution:** Refactoring Guru

---

### SRP-VIOLATION: Single Responsibility Principle

**Intent:** Maintainability

**Code Smell:** Class/function doing too many things

**Bad code:**
```javascript
class UserService {
    createUser(userData) {
        // Validate data
        if (!userData.email) throw new Error('Email required');

        // Hash password
        const hashedPassword = this.hashPassword(userData.password);

        // Save to database
        const user = db.users.insert({ ...userData, password: hashedPassword });

        // Send welcome email
        this.sendEmail(user.email, 'Welcome!', 'Thanks for joining');

        // Log analytics
        analytics.track('user_created', { userId: user.id });

        return user;
    }
}
```

**Good code:**
```javascript
class UserService {
    constructor(validator, passwordService, userRepository, emailService, analyticsService) {
        this.validator = validator;
        this.passwordService = passwordService;
        this.userRepository = userRepository;
        this.emailService = emailService;
        this.analyticsService = analyticsService;
    }

    createUser(userData) {
        this.validator.validate(userData);
        const hashedPassword = this.passwordService.hash(userData.password);
        const user = this.userRepository.create({ ...userData, password: hashedPassword });
        this.emailService.sendWelcome(user.email);
        this.analyticsService.trackUserCreation(user.id);
        return user;
    }
}
```

**Why this matters:**
- Each class has one reason to change
- Easier to test and maintain
- Better separation of concerns

**Attribution:** SOLID principles, clean-code-javascript

---

### OCP-VIOLATION: Open/Closed Principle

**Intent:** Maintainability

**Code Smell:** Modifying existing code for new features

**Bad code:**
```javascript
class PaymentProcessor {
    processPayment(amount, paymentType) {
        if (paymentType === 'credit') {
            // Credit card logic
        } else if (paymentType === 'debit') {
            // Debit card logic
        } else if (paymentType === 'paypal') {
            // PayPal logic
        }
        // Adding new payment type requires modifying this class
    }
}
```

**Good code:**
```javascript
class PaymentProcessor {
    constructor(paymentMethod) {
        this.paymentMethod = paymentMethod;
    }

    processPayment(amount) {
        return this.paymentMethod.process(amount);
    }
}

class CreditCardPayment {
    process(amount) {
        // Credit card logic
    }
}

class DebitCardPayment {
    process(amount) {
        // Debit card logic
    }
}

class PayPalPayment {
    process(amount) {
        // PayPal logic
    }
}

// Usage
const processor = new PaymentProcessor(new CreditCardPayment());
processor.processPayment(100);
```

**Why this matters:**
- Open for extension, closed for modification
- New payment types don't modify existing code
- Follows polymorphism

**Attribution:** SOLID principles

---

### LSP-VIOLATION: Liskov Substitution Principle

**Intent:** Maintainability

**Code Smell:** Subclass breaking parent class contract

**Bad code:**
```javascript
class Bird {
    fly() {
        return 'Flying high';
    }
}

class Penguin extends Bird {
    fly() {
        throw new Error('Penguins cannot fly');
    }
}

// Usage breaks
function makeBirdFly(bird) {
    return bird.fly(); // Fails for Penguin
}
```

**Good code:**
```javascript
class Bird {
    move() {
        return 'Moving';
    }
}

class FlyingBird extends Bird {
    fly() {
        return 'Flying high';
    }

    move() {
        return this.fly();
    }
}

class Penguin extends Bird {
    swim() {
        return 'Swimming';
    }

    move() {
        return this.swim();
    }
}

// Usage works for all birds
function makeBirdMove(bird) {
    return bird.move();
}
```

**Why this matters:**
- Subtypes must be substitutable for base types
- Prevents unexpected behavior
- Better class hierarchy design

**Attribution:** SOLID principles

---

### DIP-VIOLATION: Dependency Inversion Principle

**Intent:** Maintainability

**Code Smell:** High-level modules depending on low-level modules

**Bad code:**
```javascript
class MySQLDatabase {
    connect() { /* ... */ }
    query(sql) { /* ... */ }
}

class UserRepository {
    constructor() {
        this.db = new MySQLDatabase(); // Direct dependency
    }

    findById(id) {
        return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
    }
}
```

**Good code:**
```javascript
// Abstraction
class Database {
    connect() { throw new Error('Must implement'); }
    query(sql) { throw new Error('Must implement'); }
}

class MySQLDatabase extends Database {
    connect() { /* MySQL connection */ }
    query(sql) { /* MySQL query */ }
}

class PostgresDatabase extends Database {
    connect() { /* Postgres connection */ }
    query(sql) { /* Postgres query */ }
}

class UserRepository {
    constructor(database) {
        this.db = database; // Depends on abstraction
    }

    findById(id) {
        return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
    }
}

// Usage
const db = new MySQLDatabase();
const userRepo = new UserRepository(db);
```

**Why this matters:**
- Depend on abstractions, not concretions
- Easy to swap implementations
- Better testability (mock injection)

**Attribution:** SOLID principles

---

### GOD-CLASS: Break Down God Classes

**Intent:** Maintainability

**Code Smell:** Class doing everything

**Bad code:**
```javascript
class Application {
    handleRequest() { /* ... */ }
    renderUI() { /* ... */ }
    validateInput() { /* ... */ }
    saveToDatabase() { /* ... */ }
    sendEmail() { /* ... */ }
    processPayment() { /* ... */ }
    generateReport() { /* ... */ }
    // 50+ more methods
}
```

**Good code:**
```javascript
class Application {
    constructor(router, renderer, validator, database, emailService, paymentProcessor, reportGenerator) {
        this.router = router;
        this.renderer = renderer;
        this.validator = validator;
        this.database = database;
        this.emailService = emailService;
        this.paymentProcessor = paymentProcessor;
        this.reportGenerator = reportGenerator;
    }

    handleRequest(request) {
        const route = this.router.route(request);
        const validatedData = this.validator.validate(request.data);
        // Delegate to appropriate services
    }
}
```

**Why this matters:**
- Each class has focused responsibility
- Easier to understand and maintain
- Better separation of concerns

**Attribution:** Refactoring Guru

---

### DATA-CLASS: Enrich Data Classes

**Intent:** Maintainability

**Code Smell:** Class with only getters/setters, no behavior

**Bad code:**
```javascript
class Product {
    constructor(name, price, taxRate) {
        this.name = name;
        this.price = price;
        this.taxRate = taxRate;
    }

    getName() { return this.name; }
    setName(name) { this.name = name; }
    getPrice() { return this.price; }
    setPrice(price) { this.price = price; }
    getTaxRate() { return this.taxRate; }
    setTaxRate(rate) { this.taxRate = rate; }
}

// Logic scattered in other classes
function calculateTotalPrice(product) {
    return product.getPrice() * (1 + product.getTaxRate());
}
```

**Good code:**
```javascript
class Product {
    constructor(name, price, taxRate) {
        this.name = name;
        this.price = price;
        this.taxRate = taxRate;
    }

    getTotalPrice() {
        return this.price * (1 + this.taxRate);
    }

    applyDiscount(percentage) {
        this.price = this.price * (1 - percentage);
    }

    isTaxable() {
        return this.taxRate > 0;
    }
}
```

**Why this matters:**
- Data and behavior together
- Encapsulation of domain logic
- Prevents anemic domain model

**Attribution:** Refactoring Guru

---

### FEATURE-ENVY: Move Method to Appropriate Class

**Intent:** Maintainability

**Code Smell:** Method using data from other class more than its own

**Bad code:**
```javascript
class Customer {
    constructor(name, address) {
        this.name = name;
        this.address = address;
    }
}

class Order {
    constructor(customer) {
        this.customer = customer;
    }

    getCustomerDiscount() {
        // Feature envy - uses customer data
        if (this.customer.address.state === 'CA') {
            return 0.1;
        }
        return 0;
    }
}
```

**Good code:**
```javascript
class Customer {
    constructor(name, address) {
        this.name = name;
        this.address = address;
    }

    getDiscount() {
        if (this.address.state === 'CA') {
            return 0.1;
        }
        return 0;
    }
}

class Order {
    constructor(customer) {
        this.customer = customer;
    }

    getCustomerDiscount() {
        return this.customer.getDiscount();
    }
}
```

**Why this matters:**
- Method belongs where the data is
- Better encapsulation
- Reduces coupling

**Attribution:** Refactoring Guru

---

### MESSAGE-CHAIN: Hide Delegate

**Intent:** Maintainability

**Code Smell:** Long chains of method calls

**Bad code:**
```javascript
const managerName = employee.getDepartment().getManager().getName();
```

**Good code:**
```javascript
class Employee {
    getManagerName() {
        return this.department.getManagerName();
    }
}

class Department {
    getManagerName() {
        return this.manager.getName();
    }
}

// Usage
const managerName = employee.getManagerName();
```

**Why this matters:**
- Reduces coupling between objects
- Easier to change internal structure
- Law of Demeter compliance

**Attribution:** Refactoring Guru, Law of Demeter

---

### MIDDLE-MAN: Remove Middle Man

**Intent:** Maintainability

**Code Smell:** Class mostly delegating to another class

**Bad code:**
```javascript
class Department {
    constructor(manager) {
        this.manager = manager;
    }

    getManagerName() {
        return this.manager.getName();
    }

    getManagerEmail() {
        return this.manager.getEmail();
    }

    getManagerPhone() {
        return this.manager.getPhone();
    }

    // 20+ more delegation methods
}
```

**Good code:**
```javascript
class Department {
    constructor(manager) {
        this.manager = manager;
    }

    getManager() {
        return this.manager;
    }
}

// Usage
const manager = department.getManager();
const name = manager.getName();
const email = manager.getEmail();
```

**Why this matters:**
- Removes unnecessary indirection
- Simpler class structure
- Direct access when appropriate

**Attribution:** Refactoring Guru

---

### SHOT-GUN: Consolidate Shotgun Surgery

**Intent:** Maintainability

**Code Smell:** Single change requires modifications in many classes

**Bad code:**
```javascript
// Changing tax calculation requires updating 5+ classes
class OrderProcessor {
    calculateTotal(order) {
        return order.subtotal * 1.08; // Hard-coded tax
    }
}

class InvoiceGenerator {
    generateInvoice(order) {
        const tax = order.subtotal * 0.08;
        // ...
    }
}

class ReportBuilder {
    buildReport(orders) {
        orders.forEach(order => {
            const tax = order.subtotal * 0.08;
            // ...
        });
    }
}
```

**Good code:**
```javascript
class TaxCalculator {
    static calculate(subtotal) {
        const TAX_RATE = 0.08;
        return subtotal * TAX_RATE;
    }
}

class OrderProcessor {
    calculateTotal(order) {
        return order.subtotal + TaxCalculator.calculate(order.subtotal);
    }
}

class InvoiceGenerator {
    generateInvoice(order) {
        const tax = TaxCalculator.calculate(order.subtotal);
        // ...
    }
}

class ReportBuilder {
    buildReport(orders) {
        orders.forEach(order => {
            const tax = TaxCalculator.calculate(order.subtotal);
            // ...
        });
    }
}
```

**Why this matters:**
- Single source of truth
- Change once, not everywhere
- Reduces bug introduction

**Attribution:** Refactoring Guru

---

### DIVERGENT-CHANGE: Separate Divergent Changes

**Intent:** Maintainability

**Code Smell:** Class changes for different reasons

**Bad code:**
```javascript
class User {
    constructor(data) {
        this.data = data;
    }

    // Changes when database changes
    save() { /* database logic */ }
    load() { /* database logic */ }

    // Changes when validation rules change
    validate() { /* validation logic */ }

    // Changes when email templates change
    sendEmail() { /* email logic */ }
}
```

**Good code:**
```javascript
class User {
    constructor(data) {
        this.data = data;
    }
}

class UserRepository {
    save(user) { /* database logic */ }
    load(id) { /* database logic */ }
}

class UserValidator {
    validate(user) { /* validation logic */ }
}

class UserEmailService {
    sendEmail(user) { /* email logic */ }
}
```

**Why this matters:**
- Each class has one reason to change
- Better separation of concerns
- Follows SRP

**Attribution:** Refactoring Guru

---

### PARALLEL-HIER: Collapse Parallel Hierarchies

**Intent:** Maintainability

**Code Smell:** Parallel class hierarchies that change together

**Bad code:**
```javascript
class Employee { }
class Manager extends Employee { }
class Developer extends Employee { }

class EmployeeReport { }
class ManagerReport extends EmployeeReport { }
class DeveloperReport extends EmployeeReport { }
```

**Good code:**
```javascript
class Employee {
    generateReport() {
        return new EmployeeReport(this);
    }
}

class Manager extends Employee {
    generateReport() {
        return new EmployeeReport(this, 'manager');
    }
}

class Developer extends Employee {
    generateReport() {
        return new EmployeeReport(this, 'developer');
    }
}

class EmployeeReport {
    constructor(employee, type = 'employee') {
        this.employee = employee;
        this.type = type;
    }
}
```

**Why this matters:**
- Reduces class proliferation
- Single hierarchy to maintain
- Easier to add new types

**Attribution:** Refactoring Guru

---

## 3. TESTABILITY

### PURE-FUNC: Prefer Pure Functions

**Intent:** Testability

**Code Smell:** Functions with side effects

**Bad code:**
```javascript
let total = 0;

function addToTotal(value) {
    total += value; // Side effect
    return total;
}
```

**Good code:**
```javascript
function add(a, b) {
    return a + b; // Pure function
}

// Usage
let total = 0;
total = add(total, 5);
```

**Why this matters:**
- Predictable behavior
- Easy to test
- No hidden dependencies

**Attribution:** Functional programming principles

---

### INJECT-DEP: Use Dependency Injection

**Intent:** Testability

**Code Smell:** Hard-coded dependencies

**Bad code:**
```javascript
class UserService {
    constructor() {
        this.db = new Database(); // Hard-coded dependency
        this.emailer = new EmailService(); // Hard-coded dependency
    }

    createUser(userData) {
        const user = this.db.save(userData);
        this.emailer.send(user.email, 'Welcome!');
        return user;
    }
}
```

**Good code:**
```javascript
class UserService {
    constructor(database, emailService) {
        this.db = database;
        this.emailer = emailService;
    }

    createUser(userData) {
        const user = this.db.save(userData);
        this.emailer.send(user.email, 'Welcome!');
        return user;
    }
}

// Usage
const db = new Database();
const emailer = new EmailService();
const userService = new UserService(db, emailer);

// Testing
const mockDb = { save: jest.fn() };
const mockEmailer = { send: jest.fn() };
const testService = new UserService(mockDb, mockEmailer);
```

**Why this matters:**
- Easy to mock dependencies
- Better testability
- Flexible configuration

**Attribution:** Dependency Injection pattern

---

### SEPARATE-QUERY: Separate Query from Command

**Intent:** Testability

**Code Smell:** Method that both queries and modifies state

**Bad code:**
```javascript
function getTotalAndReset() {
    const total = items.reduce((sum, item) => sum + item.price, 0);
    items = []; // Side effect while querying
    return total;
}
```

**Good code:**
```javascript
function getTotal() {
    return items.reduce((sum, item) => sum + item.price, 0);
}

function reset() {
    items = [];
}

// Usage
const total = getTotal();
reset();
```

**Why this matters:**
- Clear separation of concerns
- Easier to test each operation
- No surprising side effects

**Attribution:** Command-Query Separation (CQS)

---

### HIDDEN-DEP: Expose Hidden Dependencies

**Intent:** Testability

**Code Smell:** Function using global state without declaring it

**Bad code:**
```javascript
const CONFIG = { apiUrl: 'https://api.example.com' };

function fetchUser(id) {
    // Hidden dependency on CONFIG
    return fetch(`${CONFIG.apiUrl}/users/${id}`);
}
```

**Good code:**
```javascript
function fetchUser(id, apiUrl) {
    return fetch(`${apiUrl}/users/${id}`);
}

// Usage
const CONFIG = { apiUrl: 'https://api.example.com' };
fetchUser(123, CONFIG.apiUrl);

// Testing
fetchUser(123, 'http://localhost:3000'); // Easy to test with different URL
```

**Why this matters:**
- Dependencies are explicit
- Easy to test with different configurations
- No hidden coupling

**Attribution:** Clean Code principles

---

### GLOBAL-STATE: Avoid Global State

**Intent:** Testability

**Code Smell:** Relying on global mutable state

**Bad code:**
```javascript
let currentUser = null;

function login(user) {
    currentUser = user;
}

function getUsername() {
    return currentUser ? currentUser.name : 'Guest';
}
```

**Good code:**
```javascript
class UserSession {
    constructor() {
        this.currentUser = null;
    }

    login(user) {
        this.currentUser = user;
    }

    getUsername() {
        return this.currentUser ? this.currentUser.name : 'Guest';
    }
}

// Usage
const session = new UserSession();
session.login(user);
```

**Why this matters:**
- Easier to test (isolated instances)
- No test interference
- Better encapsulation

**Attribution:** Clean Code principles

---

### TIGHTLY-COUPLED: Reduce Tight Coupling

**Intent:** Testability

**Code Smell:** Classes tightly coupled together

**Bad code:**
```javascript
class OrderProcessor {
    processOrder(order) {
        const payment = new PaymentGateway(); // Tight coupling
        payment.charge(order.total);

        const inventory = new InventorySystem(); // Tight coupling
        inventory.reduce(order.items);
    }
}
```

**Good code:**
```javascript
class OrderProcessor {
    constructor(paymentGateway, inventorySystem) {
        this.payment = paymentGateway;
        this.inventory = inventorySystem;
    }

    processOrder(order) {
        this.payment.charge(order.total);
        this.inventory.reduce(order.items);
    }
}
```

**Why this matters:**
- Easy to swap implementations
- Better testability with mocks
- Loose coupling

**Attribution:** SOLID principles

---

### FACTORY-PATTERN: Use Factory for Object Creation

**Intent:** Testability

**Code Smell:** Direct instantiation making testing difficult

**Bad code:**
```javascript
class ReportGenerator {
    generate(type) {
        let report;
        if (type === 'pdf') {
            report = new PDFReport(); // Hard to test
        } else if (type === 'excel') {
            report = new ExcelReport(); // Hard to test
        }
        return report.generate();
    }
}
```

**Good code:**
```javascript
class ReportFactory {
    createReport(type) {
        if (type === 'pdf') return new PDFReport();
        if (type === 'excel') return new ExcelReport();
        throw new Error('Unknown report type');
    }
}

class ReportGenerator {
    constructor(reportFactory) {
        this.reportFactory = reportFactory;
    }

    generate(type) {
        const report = this.reportFactory.createReport(type);
        return report.generate();
    }
}

// Testing
const mockFactory = {
    createReport: jest.fn(() => ({ generate: jest.fn() }))
};
const generator = new ReportGenerator(mockFactory);
```

**Why this matters:**
- Easy to mock factories in tests
- Centralized object creation
- Open for extension

**Attribution:** Factory design pattern

---

## 4. CODE SMELLS - BLOATERS

### LONG-METHOD: Break Down Long Methods

**Intent:** Readability, Maintainability

**Code Smell:** Method longer than 20 lines

**Bad code:**
```javascript
function processInvoice(invoice) {
    // 100+ lines of validation, calculation, formatting, etc.
    // ...
}
```

**Good code:**
```javascript
function processInvoice(invoice) {
    validateInvoice(invoice);
    const total = calculateTotal(invoice);
    const formatted = formatInvoice(invoice, total);
    return formatted;
}

function validateInvoice(invoice) {
    // Validation logic
}

function calculateTotal(invoice) {
    // Calculation logic
}

function formatInvoice(invoice, total) {
    // Formatting logic
}
```

**Why this matters:**
- Each function has single purpose
- Easier to understand and test
- Better reusability

**Attribution:** Refactoring Guru

---

### LARGE-CLASS: Split Large Classes

**Intent:** Maintainability

**Code Smell:** Class with too many fields/methods (>200 lines)

**Bad code:**
```javascript
class User {
    // 50+ properties
    // 100+ methods handling authentication, profile, orders, payments, etc.
}
```

**Good code:**
```javascript
class User {
    constructor(profile, authentication) {
        this.profile = profile;
        this.authentication = authentication;
    }
}

class UserProfile {
    // Profile-related methods
}

class UserAuthentication {
    // Authentication-related methods
}
```

**Why this matters:**
- Each class has focused responsibility
- Easier to understand and maintain
- Better separation of concerns

**Attribution:** Refactoring Guru

---

### LONG-PARAM-LIST: Use Parameter Object

**Intent:** Readability

**Code Smell:** Function with more than 3 parameters

**Bad code:**
```javascript
function drawRectangle(x, y, width, height, color, borderWidth, borderColor, opacity) {
    // ...
}
```

**Good code:**
```javascript
function drawRectangle(config) {
    const { x, y, width, height, color, borderWidth, borderColor, opacity } = config;
    // ...
}

// Usage
drawRectangle({
    x: 10,
    y: 20,
    width: 100,
    height: 50,
    color: 'blue',
    borderWidth: 2,
    borderColor: 'black',
    opacity: 0.8
});
```

**Why this matters:**
- Named parameters improve clarity
- Easy to add new parameters
- Order doesn't matter

**Attribution:** Refactoring Guru

---

### PRIMITIVE-OBS: Replace Primitives with Objects

**Intent:** Maintainability

**Code Smell:** Primitive Obsession

**Bad code:**
```javascript
function validatePhoneNumber(phone) {
    const regex = /^\d{3}-\d{3}-\d{4}$/;
    return regex.test(phone);
}

function formatPhoneNumber(phone) {
    return phone.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
}

// Phone number logic scattered everywhere
```

**Good code:**
```javascript
class PhoneNumber {
    constructor(number) {
        this.number = number;
    }

    validate() {
        const regex = /^\d{3}-\d{3}-\d{4}$/;
        return regex.test(this.number);
    }

    format() {
        return this.number.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
    }

    getAreaCode() {
        return this.number.substring(0, 3);
    }
}

// Usage
const phone = new PhoneNumber('5551234567');
if (phone.validate()) {
    console.log(phone.format());
}
```

**Why this matters:**
- Encapsulates domain logic
- Type safety
- Behavior and data together

**Attribution:** Refactoring Guru

---

### DATA-CLUMP: Group Related Data

**Intent:** Maintainability

**Code Smell:** Same group of variables appearing together

**Bad code:**
```javascript
function drawLine(startX, startY, endX, endY) {
    // ...
}

function calculateDistance(startX, startY, endX, endY) {
    // ...
}
```

**Good code:**
```javascript
class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

function drawLine(start, end) {
    // start and end are Point objects
}

function calculateDistance(start, end) {
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    return Math.sqrt(dx * dx + dy * dy);
}

// Usage
const start = new Point(10, 20);
const end = new Point(50, 80);
drawLine(start, end);
```

**Why this matters:**
- Reduces parameter lists
- Clear semantic grouping
- Easier to extend

**Attribution:** Refactoring Guru

---

## 5. CODE SMELLS - COMPLEXITY

### SWITCH-STMT: Replace Switch with Polymorphism

**Intent:** Maintainability

**Code Smell:** Complex switch/if-else chains

**Bad code:**
```javascript
function calculateArea(shape) {
    switch (shape.type) {
        case 'circle':
            return Math.PI * shape.radius ** 2;
        case 'rectangle':
            return shape.width * shape.height;
        case 'triangle':
            return 0.5 * shape.base * shape.height;
        default:
            throw new Error('Unknown shape');
    }
}
```

**Good code:**
```javascript
class Shape {
    calculateArea() {
        throw new Error('Must implement');
    }
}

class Circle extends Shape {
    constructor(radius) {
        super();
        this.radius = radius;
    }

    calculateArea() {
        return Math.PI * this.radius ** 2;
    }
}

class Rectangle extends Shape {
    constructor(width, height) {
        super();
        this.width = width;
        this.height = height;
    }

    calculateArea() {
        return this.width * this.height;
    }
}

class Triangle extends Shape {
    constructor(base, height) {
        super();
        this.base = base;
        this.height = height;
    }

    calculateArea() {
        return 0.5 * this.base * this.height;
    }
}

// Usage
const shapes = [
    new Circle(5),
    new Rectangle(10, 20),
    new Triangle(15, 10)
];

shapes.forEach(shape => console.log(shape.calculateArea()));
```

**Why this matters:**
- Open for extension (add new shapes)
- Closed for modification
- Polymorphism over conditionals

**Attribution:** Refactoring Guru

---

### NESTED-COND: Reduce Nested Conditionals

**Intent:** Readability

**Code Smell:** Deep nesting (>3 levels)

**Bad code:**
```javascript
function processUser(user) {
    if (user) {
        if (user.isActive) {
            if (user.hasPermission) {
                if (user.credits > 0) {
                    // Do something
                } else {
                    throw new Error('No credits');
                }
            } else {
                throw new Error('No permission');
            }
        } else {
            throw new Error('Inactive user');
        }
    } else {
        throw new Error('No user');
    }
}
```

**Good code:**
```javascript
function processUser(user) {
    if (!user) throw new Error('No user');
    if (!user.isActive) throw new Error('Inactive user');
    if (!user.hasPermission) throw new Error('No permission');
    if (user.credits <= 0) throw new Error('No credits');

    // Do something
}
```

**Why this matters:**
- Early returns reduce nesting
- Easier to read and understand
- Guard clauses pattern

**Attribution:** Clean Code, Guard Clauses pattern

---

### COMPLEX-BOOL: Simplify Complex Boolean Logic

**Intent:** Readability

**Code Smell:** Complex boolean expressions

**Bad code:**
```javascript
if ((user.age >= 18 && user.hasLicense) ||
    (user.age >= 16 && user.hasPermit && user.hasAdult)) {
    // Allow driving
}
```

**Good code:**
```javascript
const canDriveWithLicense = user.age >= 18 && user.hasLicense;
const canDriveWithPermit = user.age >= 16 && user.hasPermit && user.hasAdult;

if (canDriveWithLicense || canDriveWithPermit) {
    // Allow driving
}
```

**Why this matters:**
- Named variables explain intent
- Easier to understand logic
- Testable conditions

**Attribution:** Clean Code

---

### CALLBACK-HELL: Flatten Callback Hell

**Intent:** Readability

**Code Smell:** Deeply nested callbacks

**Bad code:**
```javascript
getUser(userId, (err, user) => {
    if (err) {
        handleError(err);
    } else {
        getOrders(user.id, (err, orders) => {
            if (err) {
                handleError(err);
            } else {
                getOrderDetails(orders[0].id, (err, details) => {
                    if (err) {
                        handleError(err);
                    } else {
                        processDetails(details);
                    }
                });
            }
        });
    }
});
```

**Good code:**
```javascript
async function processUserOrder(userId) {
    try {
        const user = await getUser(userId);
        const orders = await getOrders(user.id);
        const details = await getOrderDetails(orders[0].id);
        processDetails(details);
    } catch (err) {
        handleError(err);
    }
}

processUserOrder(userId);
```

**Why this matters:**
- Linear, readable flow
- Easier error handling
- Modern async/await pattern

**Attribution:** JavaScript async/await best practices

---

## 6. MODERN JAVASCRIPT

### DESTRUCTURE: Use Destructuring

**Intent:** Readability

**Code Smell:** Repetitive property access

**Bad code:**
```javascript
function displayUser(user) {
    console.log(user.firstName);
    console.log(user.lastName);
    console.log(user.email);
    console.log(user.address.city);
    console.log(user.address.state);
}
```

**Good code:**
```javascript
function displayUser(user) {
    const { firstName, lastName, email, address: { city, state } } = user;
    console.log(firstName);
    console.log(lastName);
    console.log(email);
    console.log(city);
    console.log(state);
}

// Or parameter destructuring
function displayUser({ firstName, lastName, email, address: { city, state } }) {
    console.log(firstName, lastName, email, city, state);
}
```

**Why this matters:**
- More concise
- Clear what properties are used
- Works with arrays too

**Attribution:** ES6+ best practices

---

### SPREAD-REST: Use Spread and Rest Operators

**Intent:** Readability

**Code Smell:** Manual array/object copying

**Bad code:**
```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = arr1.concat(arr2);

const obj1 = { a: 1, b: 2 };
const obj2 = Object.assign({}, obj1, { c: 3 });

function sum(a, b, c, d) {
    return a + b + c + d;
}
```

**Good code:**
```javascript
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];

const obj1 = { a: 1, b: 2 };
const obj2 = { ...obj1, c: 3 };

function sum(...numbers) {
    return numbers.reduce((total, n) => total + n, 0);
}
```

**Why this matters:**
- More concise syntax
- Immutable operations
- Flexible function parameters

**Attribution:** ES6+ best practices

---

### OPT-CHAIN: Use Optional Chaining

**Intent:** Readability

**Code Smell:** Verbose null checking

**Bad code:**
```javascript
const city = user && user.address && user.address.city;

if (user && user.settings && user.settings.notifications) {
    sendNotification(user);
}
```

**Good code:**
```javascript
const city = user?.address?.city;

if (user?.settings?.notifications) {
    sendNotification(user);
}
```

**Why this matters:**
- More concise
- Safer property access
- Modern JavaScript feature

**Attribution:** ES2020+ best practices

---

### NULLISH-COAL: Use Nullish Coalescing

**Intent:** Readability

**Code Smell:** Incorrect default value handling

**Bad code:**
```javascript
const count = userInput || 10; // Problem: 0 is falsy but valid

function getPort(config) {
    return config.port || 3000; // Problem: port 0 is valid
}
```

**Good code:**
```javascript
const count = userInput ?? 10; // Only replaces null/undefined

function getPort(config) {
    return config.port ?? 3000; // 0 is preserved
}
```

**Why this matters:**
- Correct handling of falsy values
- Distinguishes null/undefined from other falsy values
- Prevents bugs with 0, '', false

**Attribution:** ES2020+ best practices

---

### ASYNC-AWAIT: Use Async/Await

**Intent:** Readability

**Code Smell:** Promise chains

**Bad code:**
```javascript
function fetchUserData(userId) {
    return fetch(`/api/users/${userId}`)
        .then(response => response.json())
        .then(user => fetch(`/api/orders/${user.id}`))
        .then(response => response.json())
        .then(orders => {
            return { user, orders };
        })
        .catch(error => {
            handleError(error);
        });
}
```

**Good code:**
```javascript
async function fetchUserData(userId) {
    try {
        const userResponse = await fetch(`/api/users/${userId}`);
        const user = await userResponse.json();

        const ordersResponse = await fetch(`/api/orders/${user.id}`);
        const orders = await ordersResponse.json();

        return { user, orders };
    } catch (error) {
        handleError(error);
    }
}
```

**Why this matters:**
- More readable, synchronous-like code
- Better error handling
- Easier to debug

**Attribution:** ES2017+ best practices

---

### ARRAY-METHODS: Use Array Methods

**Intent:** Readability

**Code Smell:** Imperative loops

**Bad code:**
```javascript
const numbers = [1, 2, 3, 4, 5];

// Double all numbers
const doubled = [];
for (let i = 0; i < numbers.length; i++) {
    doubled.push(numbers[i] * 2);
}

// Filter even numbers
const evens = [];
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        evens.push(numbers[i]);
    }
}

// Sum all numbers
let sum = 0;
for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i];
}
```

**Good code:**
```javascript
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
const sum = numbers.reduce((total, n) => total + n, 0);
```

**Why this matters:**
- More declarative
- Less error-prone (no index management)
- Functional programming style

**Attribution:** Functional JavaScript best practices

---

### CONST-LET: Use const and let

**Intent:** Readability

**Code Smell:** Using var

**Bad code:**
```javascript
var name = 'John';
var age = 30;

for (var i = 0; i < 10; i++) {
    // i leaks to outer scope
}
```

**Good code:**
```javascript
const name = 'John'; // Won't be reassigned
let age = 30; // Might be reassigned

for (let i = 0; i < 10; i++) {
    // i is block-scoped
}
```

**Why this matters:**
- Block scoping prevents bugs
- const communicates intent (no reassignment)
- Modern JavaScript standard

**Attribution:** ES6+ best practices

---

### DEFAULT-PARAM: Use Default Parameters

**Intent:** Readability

**Code Smell:** Manual default value assignment

**Bad code:**
```javascript
function createUser(name, role, active) {
    role = role || 'user';
    active = active !== undefined ? active : true;
    return { name, role, active };
}
```

**Good code:**
```javascript
function createUser(name, role = 'user', active = true) {
    return { name, role, active };
}
```

**Why this matters:**
- Clearer intent
- Less code
- Handles undefined correctly

**Attribution:** ES6+ best practices

---

## 7. PERFORMANCE

### ALGO-COMPLEX: Optimize Algorithm Complexity

**Intent:** Performance

**Code Smell:** Inefficient algorithms (O(n²) when O(n) possible)

**Bad code:**
```javascript
function findDuplicates(arr) {
    const duplicates = [];
    for (let i = 0; i < arr.length; i++) {
        for (let j = i + 1; j < arr.length; j++) {
            if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
                duplicates.push(arr[i]);
            }
        }
    }
    return duplicates;
}
// O(n³) complexity
```

**Good code:**
```javascript
function findDuplicates(arr) {
    const seen = new Set();
    const duplicates = new Set();

    for (const item of arr) {
        if (seen.has(item)) {
            duplicates.add(item);
        } else {
            seen.add(item);
        }
    }

    return Array.from(duplicates);
}
// O(n) complexity
```

**Why this matters:**
- Scalability for large datasets
- Better performance
- Lower resource usage

**Attribution:** Algorithm optimization principles

---

### MEMO-RESULT: Memoize Expensive Computations

**Intent:** Performance

**Code Smell:** Recalculating same values

**Bad code:**
```javascript
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
// Exponential time complexity, recalculates same values
```

**Good code:**
```javascript
function fibonacci() {
    const cache = new Map();

    return function fib(n) {
        if (n <= 1) return n;
        if (cache.has(n)) return cache.get(n);

        const result = fib(n - 1) + fib(n - 2);
        cache.set(n, result);
        return result;
    };
}

const fib = fibonacci();
// Or use a library like lodash.memoize
```

**Why this matters:**
- Avoid redundant calculations
- Significant performance gains
- Trade memory for speed

**Attribution:** Memoization pattern

---

### LAZY-EVAL: Use Lazy Evaluation

**Intent:** Performance

**Code Smell:** Computing values that might not be needed

**Bad code:**
```javascript
function processUser(user) {
    const expensiveData = fetchExpensiveData(user.id); // Always computed

    if (user.isPremium) {
        return expensiveData;
    }
    return null;
}
```

**Good code:**
```javascript
function processUser(user) {
    if (user.isPremium) {
        const expensiveData = fetchExpensiveData(user.id); // Only computed when needed
        return expensiveData;
    }
    return null;
}

// Or use a getter
class User {
    get expensiveData() {
        if (!this._expensiveData) {
            this._expensiveData = fetchExpensiveData(this.id);
        }
        return this._expensiveData;
    }
}
```

**Why this matters:**
- Compute only when necessary
- Faster execution
- Resource efficiency

**Attribution:** Lazy evaluation pattern

---

### AVOID-CLOSURE-LOOP: Fix Closure Issues in Loops

**Intent:** Performance

**Code Smell:** Creating closures in loops

**Bad code:**
```javascript
for (var i = 0; i < 5; i++) {
    setTimeout(function() {
        console.log(i); // Prints 5, 5, 5, 5, 5
    }, 1000);
}
```

**Good code:**
```javascript
// Solution 1: Use let (block scoping)
for (let i = 0; i < 5; i++) {
    setTimeout(function() {
        console.log(i); // Prints 0, 1, 2, 3, 4
    }, 1000);
}

// Solution 2: Use forEach
[0, 1, 2, 3, 4].forEach(i => {
    setTimeout(function() {
        console.log(i); // Prints 0, 1, 2, 3, 4
    }, 1000);
});
```

**Why this matters:**
- Correct behavior
- Avoids common bugs
- Modern JavaScript best practice

**Attribution:** JavaScript closure best practices

---

### DEBOUNCE-THROTTLE: Debounce/Throttle Frequent Events

**Intent:** Performance

**Code Smell:** Handling every event in rapid succession

**Bad code:**
```javascript
window.addEventListener('scroll', () => {
    // Heavy computation on every scroll event (fires 100+ times per second)
    updateScrollPosition();
});

searchInput.addEventListener('input', (e) => {
    // API call on every keystroke
    searchAPI(e.target.value);
});
```

**Good code:**
```javascript
// Throttle: Execute at most once per interval
function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            lastCall = now;
            func(...args);
        }
    };
}

window.addEventListener('scroll', throttle(() => {
    updateScrollPosition();
}, 100)); // At most once per 100ms

// Debounce: Execute only after events stop
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

searchInput.addEventListener('input', debounce((e) => {
    searchAPI(e.target.value);
}, 300)); // Only after user stops typing for 300ms
```

**Why this matters:**
- Reduces unnecessary function calls
- Better performance
- Prevents API rate limiting

**Attribution:** Performance optimization patterns

---

## Review Wisdom

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler

> "Duplication is far cheaper than the wrong abstraction." - Sandi Metz

> "Make it work, make it right, make it fast." - Kent Beck

> "Code is read much more often than it is written." - Guido van Rossum

> "The best code is no code at all." - Jeff Atwood

---

## Quick Reference

**When you see:**
- **Long functions (>20 lines)** → EXTRACT-FUNC, LONG-FUNC
- **Cryptic names** → MEANINGFUL-NAME, PRONOUNCE-NAME
- **Magic numbers** → MAGIC-NUM, SEARCHABLE-NAME
- **Duplicate code** → DRY-VIOLATION, DUPLICATE-CODE
- **Many parameters (>3)** → LONG-PARAM, DATA-CLUMP
- **Complex conditionals** → DECOMPOSE-COND, NESTED-COND
- **Switch statements** → SWITCH-STMT (use polymorphism)
- **God classes** → GOD-CLASS, EXTRACT-CLASS
- **Hard-coded dependencies** → INJECT-DEP, DIP-VIOLATION
- **Side effects** → PURE-FUNC, SEPARATE-QUERY
- **Global state** → GLOBAL-STATE, HIDDEN-DEP
- **String concatenation** → TEMPLATE-LIT
- **var keyword** → CONST-LET
- **Callback hell** → ASYNC-AWAIT, CALLBACK-HELL
- **Imperative loops** → ARRAY-METHODS
- **Null checking chains** → OPT-CHAIN
- **|| for defaults** → NULLISH-COAL
- **O(n²) algorithms** → ALGO-COMPLEX
- **Repeated calculations** → MEMO-RESULT
- **Event handlers** → DEBOUNCE-THROTTLE

---

**Remember:** Good code is not just about working—it's about being readable, maintainable, and testable. Refactor with purpose, always considering the trade-offs.
