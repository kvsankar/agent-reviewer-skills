---
name: react-reviewer
description: Reviews React code for best practices, patterns, performance, accessibility, and common pitfalls. Covers components, hooks, state management, rendering optimization, and modern React features. Keywords - React, hooks, components, state, props, performance, accessibility, testing, JSX.
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
Use the Task tool to run react-reviewer on src/components/MyComponent.tsx and write the report to reviews/component-review.md
```

---

# React Reviewer

## Introduction

You are an expert React reviewer. Your mission is to help developers write better React applications by identifying issues, suggesting improvements, and teaching best practices.

## Your Mission

When reviewing React code:

1. **Component Quality** - Well-structured, reusable, maintainable components
2. **Hook Correctness** - Proper hook usage, dependency arrays, custom hooks
3. **Performance** - Prevent unnecessary re-renders, optimize rendering
4. **Accessibility** - ARIA, keyboard navigation, screen reader support
5. **Patterns** - Modern React patterns and anti-patterns to avoid
6. **Use Mnemonic IDs** - Easy reference codes (e.g., PROP-TYPES, USE-EFFECT-DEPS)

## Review Process

1. **Analyze the code** for React-specific issues
2. **Categorize by severity**: Critical, Warning, Suggestion, Info
3. **Show problematic code** - The current implementation
4. **Show improved code** - The better version
5. **Explain why** - The reasoning and benefits
6. **Provide context** - When to apply, trade-offs

## React Guidelines

### 1. Component Design (10 guidelines)

#### SINGLE-RESPONSIBILITY: Components Should Do One Thing

**Severity:** Warning

**Problematic code:**
```jsx
// Component doing too many things
function UserDashboard({ userId }) {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
    fetchPosts(userId).then(setPosts);
    fetchNotifications(userId).then(setNotifications);
  }, [userId]);
  
  const handleUpdateProfile = async (data) => { /* ... */ };
  const handleDeletePost = async (postId) => { /* ... */ };
  const handleMarkNotificationRead = async (id) => { /* ... */ };
  
  return (
    <div>
      <header>{/* User profile header */}</header>
      <section>{/* Posts list with delete */}</section>
      <aside>{/* Notifications panel */}</aside>
      <form>{/* Profile edit form */}</form>
    </div>
  );
}
```

**Improved code:**
```jsx
// Split into focused components
function UserDashboard({ userId }) {
  return (
    <div className="dashboard">
      <UserHeader userId={userId} />
      <main className="dashboard-content">
        <UserPosts userId={userId} />
      </main>
      <NotificationsSidebar userId={userId} />
    </div>
  );
}

function UserHeader({ userId }) {
  const { user, updateProfile } = useUser(userId);
  return <header>{/* Just the header */}</header>;
}

function UserPosts({ userId }) {
  const { posts, deletePost } = usePosts(userId);
  return <section>{/* Just the posts */}</section>;
}

function NotificationsSidebar({ userId }) {
  const { notifications, markRead } = useNotifications(userId);
  return <aside>{/* Just notifications */}</aside>;
}
```

**Why this matters:**
- Easier to test individual components
- Better reusability
- Simpler state management
- Easier to understand and maintain

**Related:** CUSTOM-HOOKS, COMPOSITION

---

#### COMPOSITION: Prefer Composition Over Props Drilling

**Severity:** Warning

**Problematic code:**
```jsx
// Props drilling through multiple levels
function App() {
  const [theme, setTheme] = useState('light');
  const [user, setUser] = useState(null);
  
  return (
    <Layout theme={theme} user={user} setTheme={setTheme}>
      <Sidebar theme={theme} user={user}>
        <Navigation theme={theme} user={user} />
      </Sidebar>
      <Main theme={theme} user={user}>
        <Content theme={theme} user={user} />
      </Main>
    </Layout>
  );
}

// Every component needs to pass props through
function Layout({ theme, user, setTheme, children }) {
  return <div className={theme}>{children}</div>;
}
```

**Improved code:**
```jsx
// Using composition and context
const ThemeContext = createContext();
const UserContext = createContext();

function App() {
  const [theme, setTheme] = useState('light');
  const [user, setUser] = useState(null);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <UserContext.Provider value={user}>
        <Layout>
          <Sidebar>
            <Navigation />
          </Sidebar>
          <Main>
            <Content />
          </Main>
        </Layout>
      </UserContext.Provider>
    </ThemeContext.Provider>
  );
}

// Components consume context directly
function Navigation() {
  const { theme } = useContext(ThemeContext);
  const user = useContext(UserContext);
  return <nav className={theme}>{/* ... */}</nav>;
}

// Or use children for composition
function Card({ header, children, footer }) {
  return (
    <div className="card">
      <div className="card-header">{header}</div>
      <div className="card-body">{children}</div>
      <div className="card-footer">{footer}</div>
    </div>
  );
}

// Usage - flexible composition
<Card
  header={<UserAvatar user={user} />}
  footer={<CardActions onSave={save} onCancel={cancel} />}
>
  <UserProfile user={user} />
</Card>
```

**Why this matters:**
- Avoids prop drilling (passing props through many levels)
- More flexible component composition
- Cleaner component interfaces
- Children pattern enables inversion of control

**Related:** CONTEXT-USE, RENDER-PROPS

---

#### PROP-TYPES: Define Clear Component Interfaces

**Severity:** Warning

**Problematic code:**
```jsx
// No type definitions - unclear what props are expected
function UserCard({ user, onEdit, showActions, size, variant }) {
  return (
    <div>
      <h2>{user.name}</h2>
      {showActions && <button onClick={onEdit}>Edit</button>}
    </div>
  );
}

// Usage - easy to make mistakes
<UserCard 
  user={userData} 
  onEdit="handleEdit"  // Wrong! Should be function
  showActions="true"   // Wrong! Should be boolean
/>
```

**Improved code:**
```tsx
// TypeScript - Clear interface definition
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  showActions?: boolean;
  size?: 'small' | 'medium' | 'large';
  variant?: 'default' | 'compact' | 'detailed';
}

function UserCard({ 
  user, 
  onEdit, 
  showActions = true,  // Default values
  size = 'medium',
  variant = 'default'
}: UserCardProps) {
  return (
    <div className={`user-card user-card--${size} user-card--${variant}`}>
      <h2>{user.name}</h2>
      {showActions && onEdit && (
        <button onClick={() => onEdit(user)}>Edit</button>
      )}
    </div>
  );
}

// PropTypes alternative (JavaScript)
import PropTypes from 'prop-types';

UserCard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    avatar: PropTypes.string,
  }).isRequired,
  onEdit: PropTypes.func,
  showActions: PropTypes.bool,
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  variant: PropTypes.oneOf(['default', 'compact', 'detailed']),
};

UserCard.defaultProps = {
  showActions: true,
  size: 'medium',
  variant: 'default',
};
```

**Why this matters:**
- Self-documenting code
- Catch errors at compile time (TypeScript) or runtime (PropTypes)
- Better IDE support and autocomplete
- Clear API for component consumers

**Related:** DEFAULT-PROPS, CHILDREN-TYPE

---

#### CONTROLLED-VS-UNCONTROLLED: Choose Appropriate Form Strategy

**Severity:** Info

**Uncontrolled (simpler, less control):**
```jsx
// Uncontrolled - DOM owns the state
function SearchForm({ onSearch }) {
  const inputRef = useRef(null);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(inputRef.current.value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} defaultValue="" />
      <button type="submit">Search</button>
    </form>
  );
}
```

**Controlled (more control, more code):**
```jsx
// Controlled - React owns the state
function SearchForm({ onSearch }) {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
      />
      <button type="submit">Search</button>
    </form>
  );
}
```

**When to use each:**

| Use Uncontrolled When | Use Controlled When |
|----------------------|---------------------|
| Simple forms | Need real-time validation |
| One-time value reading | Need to transform input |
| Integrating non-React code | Need to sync with other state |
| File inputs (`<input type="file">`) | Need conditional disabling |
| Performance critical (many fields) | Need to control format (e.g., phone) |

**Best practice - hybrid approach:**
```jsx
// Use form libraries for complex forms
import { useForm } from 'react-hook-form';

function RegistrationForm({ onSubmit }) {
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email', { required: true, pattern: /^\S+@\S+$/ })} />
      {errors.email && <span>Valid email required</span>}
      
      <input {...register('password', { required: true, minLength: 8 })} />
      {errors.password && <span>Password must be 8+ characters</span>}
      
      <button type="submit">Register</button>
    </form>
  );
}
```

**Related:** FORM-VALIDATION, REF-USE

---

#### LIFTING-STATE: Lift State to Common Ancestor

**Severity:** Info

**Problematic code:**
```jsx
// Duplicated state in sibling components
function TemperatureInput({ scale }) {
  const [temperature, setTemperature] = useState('');
  
  return (
    <input
      value={temperature}
      onChange={(e) => setTemperature(e.target.value)}
      placeholder={scale === 'c' ? 'Celsius' : 'Fahrenheit'}
    />
  );
}

function Calculator() {
  return (
    <div>
      <TemperatureInput scale="c" />
      <TemperatureInput scale="f" />
      {/* These inputs don't sync! */}
    </div>
  );
}
```

**Improved code:**
```jsx
// State lifted to common ancestor
function TemperatureInput({ scale, temperature, onTemperatureChange }) {
  return (
    <input
      value={temperature}
      onChange={(e) => onTemperatureChange(e.target.value)}
      placeholder={scale === 'c' ? 'Celsius' : 'Fahrenheit'}
    />
  );
}

function Calculator() {
  const [temperature, setTemperature] = useState('');
  const [scale, setScale] = useState('c');
  
  const handleCelsiusChange = (temp) => {
    setScale('c');
    setTemperature(temp);
  };
  
  const handleFahrenheitChange = (temp) => {
    setScale('f');
    setTemperature(temp);
  };
  
  const celsius = scale === 'f' ? toCelsius(temperature) : temperature;
  const fahrenheit = scale === 'c' ? toFahrenheit(temperature) : temperature;
  
  return (
    <div>
      <TemperatureInput
        scale="c"
        temperature={celsius}
        onTemperatureChange={handleCelsiusChange}
      />
      <TemperatureInput
        scale="f"
        temperature={fahrenheit}
        onTemperatureChange={handleFahrenheitChange}
      />
    </div>
  );
}
```

**When to lift state:**
- Two or more components need to reflect the same data
- A parent needs to know about child state
- Sibling components need to communicate

**Related:** STATE-COLOCATION, DERIVED-STATE

---

#### STATE-COLOCATION: Keep State Close to Where It's Used

**Severity:** Warning

**Problematic code:**
```jsx
// State too high in the tree
function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState('home');
  const [modalContent, setModalContent] = useState(null);
  
  return (
    <div>
      <Header 
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        isDropdownOpen={isDropdownOpen}
        setIsDropdownOpen={setIsDropdownOpen}
      />
      <TabPanel 
        selectedTab={selectedTab}
        setSelectedTab={setSelectedTab}
      />
      <Modal 
        content={modalContent}
        setContent={setModalContent}
      />
    </div>
  );
}
// Every state change in dropdown re-renders entire app!
```

**Improved code:**
```jsx
// State colocated with components that use it
function App() {
  return (
    <div>
      <Header />
      <TabPanel />
      <ModalProvider>
        <Content />
      </ModalProvider>
    </div>
  );
}

function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  
  return (
    <header>
      <SearchInput value={searchQuery} onChange={setSearchQuery} />
      <UserDropdown isOpen={isDropdownOpen} setIsOpen={setIsDropdownOpen} />
    </header>
  );
}

function TabPanel() {
  const [selectedTab, setSelectedTab] = useState('home');
  
  return (
    <div>
      <TabList selected={selectedTab} onSelect={setSelectedTab} />
      <TabContent tab={selectedTab} />
    </div>
  );
}
```

**Benefits:**
- Smaller re-render scope
- Better component isolation
- Easier to understand data flow
- Better performance

**Related:** LIFTING-STATE, CONTEXT-USE

---

#### DERIVED-STATE: Avoid Redundant State

**Severity:** Warning

**Problematic code:**
```jsx
// Redundant state that can be derived
function ProductList({ products }) {
  const [items, setItems] = useState(products);
  const [filteredItems, setFilteredItems] = useState(products);
  const [searchTerm, setSearchTerm] = useState('');
  const [totalPrice, setTotalPrice] = useState(0);
  
  // Syncing state - bug prone!
  useEffect(() => {
    setItems(products);
  }, [products]);
  
  useEffect(() => {
    const filtered = items.filter(item => 
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredItems(filtered);
    setTotalPrice(filtered.reduce((sum, item) => sum + item.price, 0));
  }, [items, searchTerm]);
  
  return (/* ... */);
}
```

**Improved code:**
```jsx
// Derive values during render
function ProductList({ products }) {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Derived during render - always in sync
  const filteredItems = products.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  const totalPrice = filteredItems.reduce((sum, item) => sum + item.price, 0);
  
  // Use useMemo if calculation is expensive
  const expensiveResult = useMemo(() => {
    return filteredItems.map(item => complexTransform(item));
  }, [filteredItems]);
  
  return (/* ... */);
}
```

**When to use state vs derived values:**

| Use State | Use Derived Value |
|-----------|-------------------|
| User input | Filtered/sorted lists |
| Data from server | Computed totals |
| Toggle states | Formatted display values |
| Selected items | Validation status |

**Related:** USE-MEMO, AVOID-SYNC

---

#### AVOID-SYNC: Don't Sync State with useEffect

**Severity:** Warning

**Problematic code:**
```jsx
// Anti-pattern: syncing props to state
function UserProfile({ user }) {
  const [userData, setUserData] = useState(user);
  
  // This is almost always wrong!
  useEffect(() => {
    setUserData(user);
  }, [user]);
  
  return <div>{userData.name}</div>;
}

// Anti-pattern: syncing derived state
function SearchResults({ items }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(items);
  
  useEffect(() => {
    setResults(items.filter(item => item.includes(query)));
  }, [items, query]);
  
  return (/* ... */);
}
```

**Improved code:**
```jsx
// Just use the prop directly
function UserProfile({ user }) {
  return <div>{user.name}</div>;
}

// Or if you need local modifications
function UserProfile({ user }) {
  const [localEdits, setLocalEdits] = useState({});
  
  // Merge prop with local edits
  const displayUser = { ...user, ...localEdits };
  
  return <div>{displayUser.name}</div>;
}

// Derive during render
function SearchResults({ items }) {
  const [query, setQuery] = useState('');
  
  // Calculated every render - no sync issues
  const results = items.filter(item => item.includes(query));
  
  return (/* ... */);
}

// If you truly need to reset state when prop changes, use key
function UserEditor({ userId }) {
  return <EditForm key={userId} userId={userId} />;
}

function EditForm({ userId }) {
  const [draft, setDraft] = useState('');
  // draft resets when userId changes because key changes
  return <input value={draft} onChange={e => setDraft(e.target.value)} />;
}
```

**Why syncing state is problematic:**
- Creates two sources of truth
- Causes extra renders
- Can lead to stale data bugs
- Makes data flow harder to follow

**Related:** DERIVED-STATE, KEY-RESET

---

#### CHILDREN-PATTERN: Use Children for Flexible Composition

**Severity:** Info

**Limited flexibility:**
```jsx
// Component controls all content
function Modal({ title, content, onClose }) {
  return (
    <div className="modal">
      <h2>{title}</h2>
      <div>{content}</div>
      <button onClick={onClose}>Close</button>
    </div>
  );
}

// Hard to customize
<Modal 
  title="Confirm" 
  content="Are you sure?" 
  onClose={handleClose} 
/>
```

**Improved code:**
```jsx
// Flexible composition with children
function Modal({ children, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
}

function ModalHeader({ children }) {
  return <div className="modal-header">{children}</div>;
}

function ModalBody({ children }) {
  return <div className="modal-body">{children}</div>;
}

function ModalFooter({ children }) {
  return <div className="modal-footer">{children}</div>;
}

// Highly flexible usage
<Modal onClose={handleClose}>
  <ModalHeader>
    <h2>Confirm Action</h2>
    <CloseButton onClick={handleClose} />
  </ModalHeader>
  <ModalBody>
    <p>Are you sure you want to delete this item?</p>
    <WarningIcon />
  </ModalBody>
  <ModalFooter>
    <Button variant="secondary" onClick={handleClose}>Cancel</Button>
    <Button variant="danger" onClick={handleDelete}>Delete</Button>
  </ModalFooter>
</Modal>
```

**Benefits:**
- Maximum flexibility for consumers
- Component controls layout, consumer controls content
- Follows composition over configuration
- Matches HTML mental model

**Related:** COMPOSITION, COMPOUND-COMPONENTS

---

#### COMPONENT-NAMING: Use Clear Naming Conventions

**Severity:** Info

**Problematic code:**
```jsx
// Unclear naming
function Comp1({ d, fn }) {
  return <div onClick={fn}>{d}</div>;
}

function stuff({ info }) {
  return <Comp1 d={info.name} fn={() => alert(info.name)} />;
}

// Inconsistent naming
function userCard() { /* lowercase - looks like function */ }
function UseAuth() { /* uppercase - looks like component but is hook */ }
function handleClick() { /* event handler outside component */ }
```

**Improved code:**
```jsx
// Clear, consistent naming
function UserCard({ user, onSelect }) {
  return (
    <div onClick={() => onSelect(user)}>
      {user.name}
    </div>
  );
}

function UserList({ users }) {
  const handleUserSelect = (user) => {
    console.log('Selected:', user);
  };
  
  return users.map(user => (
    <UserCard key={user.id} user={user} onSelect={handleUserSelect} />
  ));
}

// Naming conventions:
// - Components: PascalCase (UserCard, ProductList)
// - Hooks: camelCase with 'use' prefix (useAuth, useLocalStorage)
// - Event handlers: handle + Event (handleClick, handleSubmit)
// - Callbacks props: on + Event (onClick, onSubmit, onSelect)
// - Boolean props: is/has/should prefix (isActive, hasError, shouldValidate)
// - Arrays: plural nouns (users, items, products)
```

**Related:** PROP-TYPES

---

### 2. Hooks (12 guidelines)

#### USE-EFFECT-DEPS: Correct useEffect Dependencies

**Severity:** Critical

**Problematic code:**
```jsx
// Missing dependencies - stale closure
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    fetchResults(query).then(setResults);
  }, []);  // Missing 'query' - only fetches once!
  
  return <ResultsList results={results} />;
}

// Object dependency - runs every render
function UserProfile({ user }) {
  useEffect(() => {
    trackPageView(user.id);
  }, [user]);  // user is new object every render!
  
  return <div>{user.name}</div>;
}
```

**Improved code:**
```jsx
// Correct dependencies
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    fetchResults(query).then(setResults);
  }, [query]);  // Runs when query changes
  
  return <ResultsList results={results} />;
}

// Use primitive values for stable dependencies
function UserProfile({ user }) {
  const userId = user.id;
  
  useEffect(() => {
    trackPageView(userId);
  }, [userId]);  // Only changes when ID actually changes
  
  return <div>{user.name}</div>;
}

// Or use useCallback for function dependencies
function DataFetcher({ fetchFn }) {
  const [data, setData] = useState(null);
  
  const stableFetch = useCallback(() => {
    return fetchFn();
  }, [fetchFn]);
  
  useEffect(() => {
    stableFetch().then(setData);
  }, [stableFetch]);
  
  return <div>{JSON.stringify(data)}</div>;
}
```

**Dependency rules:**
- Include ALL values used inside the effect
- Use primitives when possible
- Extract values from objects
- Use useCallback/useMemo for stable references

**Related:** USE-CALLBACK, USE-MEMO, STALE-CLOSURE

---

#### USE-EFFECT-CLEANUP: Always Clean Up Side Effects

**Severity:** Critical

**Problematic code:**
```jsx
// Memory leak - no cleanup
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on('message', (msg) => {
      setMessages(prev => [...prev, msg]);
    });
    connection.connect();
    // Missing cleanup! Connection stays open forever
  }, [roomId]);
  
  return <MessageList messages={messages} />;
}

// Race condition - no abort
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
    // If userId changes fast, wrong user might be set!
  }, [userId]);
  
  return <Profile user={user} />;
}
```

**Improved code:**
```jsx
// Proper cleanup
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    const connection = createConnection(roomId);
    
    connection.on('message', (msg) => {
      setMessages(prev => [...prev, msg]);
    });
    
    connection.connect();
    
    // Cleanup function
    return () => {
      connection.disconnect();
    };
  }, [roomId]);
  
  return <MessageList messages={messages} />;
}

// Abort fetch requests
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    const abortController = new AbortController();
    
    fetchUser(userId, { signal: abortController.signal })
      .then(setUser)
      .catch(err => {
        if (err.name !== 'AbortError') {
          console.error(err);
        }
      });
    
    return () => {
      abortController.abort();
    };
  }, [userId]);
  
  return <Profile user={user} />;
}

// Or use a flag
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    
    fetchUser(userId).then(data => {
      if (!cancelled) {
        setUser(data);
      }
    });
    
    return () => {
      cancelled = true;
    };
  }, [userId]);
  
  return <Profile user={user} />;
}
```

**What needs cleanup:**
- Subscriptions (WebSocket, event listeners)
- Timers (setTimeout, setInterval)
- Fetch requests (AbortController)
- DOM modifications

**Related:** USE-EFFECT-DEPS, MEMORY-LEAK

---

#### CUSTOM-HOOKS: Extract Reusable Logic into Custom Hooks

**Severity:** Info

**Problematic code:**
```jsx
// Duplicated logic across components
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    setLoading(true);
    fetchUsers()
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <List items={users} />;
}

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    setLoading(true);
    fetchProducts()
      .then(setProducts)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  // Same pattern repeated!
  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <List items={products} />;
}
```

**Improved code:**
```jsx
// Custom hook for reusable logic
function useFetch(fetchFn, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    
    fetchFn()
      .then(result => {
        if (!cancelled) setData(result);
      })
      .catch(err => {
        if (!cancelled) setError(err);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    
    return () => { cancelled = true; };
  }, deps);
  
  return { data, loading, error, refetch: () => {} };
}

// Clean component code
function UserList() {
  const { data: users, loading, error } = useFetch(fetchUsers);
  
  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <List items={users} />;
}

function ProductList() {
  const { data: products, loading, error } = useFetch(fetchProducts);
  
  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <List items={products} />;
}

// More custom hook examples
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });
  
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);
  
  return [value, setValue];
}

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return debouncedValue;
}
```

**When to create custom hooks:**
- Logic is used in multiple components
- Logic is complex enough to benefit from isolation
- Logic involves multiple useState/useEffect calls
- You want to test the logic separately

**Related:** HOOK-RULES, SINGLE-RESPONSIBILITY

---

#### HOOK-RULES: Follow the Rules of Hooks

**Severity:** Critical

**Problematic code:**
```jsx
// Conditional hook call - BREAKS RULES
function UserProfile({ userId }) {
  if (!userId) {
    return <div>No user</div>;
  }
  
  // Called conditionally!
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  return <Profile user={user} />;
}

// Hook in loop - BREAKS RULES
function MultiSelect({ items }) {
  const selections = items.map(item => {
    const [selected, setSelected] = useState(false);  // In loop!
    return { item, selected, setSelected };
  });
  
  return (/* ... */);
}

// Hook in nested function - BREAKS RULES
function Form() {
  function handleSubmit() {
    const [isSubmitting, setIsSubmitting] = useState(false);  // In nested function!
  }
}
```

**Improved code:**
```jsx
// Hooks at top level, before any returns
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    if (userId) {
      fetchUser(userId).then(setUser);
    }
  }, [userId]);
  
  if (!userId) {
    return <div>No user</div>;
  }
  
  return <Profile user={user} />;
}

// Move state to parent or use different structure
function MultiSelect({ items }) {
  const [selections, setSelections] = useState(
    () => new Set()
  );
  
  const toggleItem = (itemId) => {
    setSelections(prev => {
      const next = new Set(prev);
      if (next.has(itemId)) {
        next.delete(itemId);
      } else {
        next.add(itemId);
      }
      return next;
    });
  };
  
  return items.map(item => (
    <Checkbox
      key={item.id}
      checked={selections.has(item.id)}
      onChange={() => toggleItem(item.id)}
    />
  ));
}

// Hooks at component top level only
function Form() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  function handleSubmit() {
    setIsSubmitting(true);
    // ...
  }
}
```

**Rules of Hooks:**
1. Only call hooks at the top level
2. Only call hooks from React functions (components or custom hooks)
3. Don't call hooks inside loops, conditions, or nested functions

**Related:** CUSTOM-HOOKS, USE-EFFECT-DEPS

---

#### USE-CALLBACK: Stabilize Function References

**Severity:** Warning

**Problematic code:**
```jsx
// New function on every render
function SearchPage() {
  const [query, setQuery] = useState('');
  
  // New function every render
  const handleSearch = (searchQuery) => {
    console.log('Searching:', searchQuery);
    // API call
  };
  
  // SearchInput re-renders every time even if query is same
  return <SearchInput onSearch={handleSearch} />;
}

const SearchInput = memo(({ onSearch }) => {
  console.log('SearchInput rendered');  // Logs every time!
  return <input onChange={e => onSearch(e.target.value)} />;
});
```

**Improved code:**
```jsx
// Stable function reference
function SearchPage() {
  const [query, setQuery] = useState('');
  
  // Same function reference between renders
  const handleSearch = useCallback((searchQuery) => {
    console.log('Searching:', searchQuery);
    // API call
  }, []);  // Empty deps = never changes
  
  return <SearchInput onSearch={handleSearch} />;
}

// With dependencies
function SearchPage({ apiClient }) {
  const [query, setQuery] = useState('');
  
  const handleSearch = useCallback((searchQuery) => {
    apiClient.search(searchQuery);
  }, [apiClient]);  // Only changes when apiClient changes
  
  return <SearchInput onSearch={handleSearch} />;
}

// When NOT to use useCallback
function SimpleButton({ onClick }) {
  // Don't wrap if not passed to memoized child
  const handleClick = () => {
    onClick();
  };
  
  return <button onClick={handleClick}>Click</button>;
}
```

**When to use useCallback:**
- Passing callbacks to memoized children (React.memo)
- Callback is dependency of useEffect
- Callback is used in a custom hook's dependencies
- Avoiding recreating expensive closures

**Related:** USE-MEMO, MEMO-COMPONENT, OVER-MEMO

---

#### USE-MEMO: Memoize Expensive Calculations

**Severity:** Warning

**Problematic code:**
```jsx
// Expensive calculation every render
function ProductTable({ products, filters }) {
  // Runs on every render, even when products/filters unchanged
  const filteredProducts = products
    .filter(p => applyFilters(p, filters))
    .sort((a, b) => a.price - b.price)
    .map(p => ({ ...p, discount: calculateDiscount(p) }));
  
  return <Table data={filteredProducts} />;
}
```

**Improved code:**
```jsx
// Memoized - only recalculates when deps change
function ProductTable({ products, filters }) {
  const filteredProducts = useMemo(() => {
    return products
      .filter(p => applyFilters(p, filters))
      .sort((a, b) => a.price - b.price)
      .map(p => ({ ...p, discount: calculateDiscount(p) }));
  }, [products, filters]);
  
  return <Table data={filteredProducts} />;
}

// When NOT to use useMemo - simple calculations
function Greeting({ firstName, lastName }) {
  // Don't memoize cheap operations
  const fullName = `${firstName} ${lastName}`;
  return <h1>Hello, {fullName}</h1>;
}
```

**When to use useMemo:**
- Filtering/sorting large lists
- Complex calculations or transformations
- Creating objects passed to memoized children
- Referential equality matters for deps

**When NOT to use:**
- Simple calculations (string concat, basic math)
- Every value (overhead > benefit)
- Premature optimization

**Related:** USE-CALLBACK, DERIVED-STATE, OVER-MEMO

---

#### STALE-CLOSURE: Avoid Stale Closures

**Severity:** Critical

**Problematic code:**
```jsx
// Stale closure in interval
function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('Count:', count);  // Always logs 0!
      setCount(count + 1);  // Always sets to 1!
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);  // count captured at initial value
  
  return <div>{count}</div>;
}

// Stale closure in event handler
function Form() {
  const [value, setValue] = useState('');
  
  const handleSubmitWithDelay = () => {
    setTimeout(() => {
      console.log('Submitting:', value);  // May be stale!
    }, 2000);
  };
  
  return (
    <form>
      <input value={value} onChange={e => setValue(e.target.value)} />
      <button onClick={handleSubmitWithDelay}>Submit</button>
    </form>
  );
}
```

**Improved code:**
```jsx
// Use functional updates
function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCount(prev => prev + 1);  // Always uses latest value
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  return <div>{count}</div>;
}

// Or use ref for latest value
function Form() {
  const [value, setValue] = useState('');
  const valueRef = useRef(value);
  
  useEffect(() => {
    valueRef.current = value;  // Keep ref in sync
  }, [value]);
  
  const handleSubmitWithDelay = () => {
    setTimeout(() => {
      console.log('Submitting:', valueRef.current);  // Always fresh!
    }, 2000);
  };
  
  return (
    <form>
      <input value={value} onChange={e => setValue(e.target.value)} />
      <button onClick={handleSubmitWithDelay}>Submit</button>
    </form>
  );
}

// Or include in dependencies
function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1);
    }, 1000);
    
    return () => clearInterval(interval);
  }, [count]);  // Re-creates interval when count changes
  
  return <div>{count}</div>;
}
```

**Patterns to avoid stale closures:**
- Functional updates: `setState(prev => prev + 1)`
- Refs for latest values: `useRef` + `useEffect`
- Correct dependencies in hooks
- `useReducer` for complex state

**Related:** USE-EFFECT-DEPS, USE-REF

---

#### USE-REF: Use Refs Appropriately

**Severity:** Info

**Ref use cases:**
```jsx
// 1. DOM element access
function TextInput({ autoFocus }) {
  const inputRef = useRef(null);
  
  useEffect(() => {
    if (autoFocus) {
      inputRef.current?.focus();
    }
  }, [autoFocus]);
  
  return <input ref={inputRef} />;
}

// 2. Storing mutable values that don't trigger re-render
function Timer() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef(null);
  
  const start = () => {
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
  };
  
  const stop = () => {
    clearInterval(intervalRef.current);
  };
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}

// 3. Storing previous value
function usePrevious(value) {
  const ref = useRef();
  
  useEffect(() => {
    ref.current = value;
  }, [value]);
  
  return ref.current;
}

function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);
  
  return (
    <div>
      <p>Now: {count}, Before: {prevCount}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>
  );
}

// 4. Callback ref for measuring DOM
function MeasuredComponent() {
  const [height, setHeight] = useState(0);
  
  const measuredRef = useCallback(node => {
    if (node !== null) {
      setHeight(node.getBoundingClientRect().height);
    }
  }, []);
  
  return (
    <div ref={measuredRef}>
      <p>My height is: {height}px</p>
    </div>
  );
}
```

**When to use ref vs state:**

| Use Ref | Use State |
|---------|-----------|
| DOM element access | UI should update on change |
| Timer/interval IDs | User-visible data |
| Previous values | Form inputs |
| Values used in event handlers | Toggle states |
| Mutable values without re-render | Fetched data |

**Related:** STALE-CLOSURE, FORWARD-REF

---

#### USE-REDUCER: Use useReducer for Complex State

**Severity:** Info

**Problematic code:**
```jsx
// Multiple related useState calls
function ShoppingCart() {
  const [items, setItems] = useState([]);
  const [discount, setDiscount] = useState(0);
  const [shipping, setShipping] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const addItem = (item) => {
    setItems([...items, item]);
  };
  
  const removeItem = (id) => {
    setItems(items.filter(i => i.id !== id));
  };
  
  const applyDiscount = async (code) => {
    setIsLoading(true);
    setError(null);
    try {
      const discountValue = await validateCoupon(code);
      setDiscount(discountValue);
    } catch (e) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  // State updates scattered across multiple functions
}
```

**Improved code:**
```jsx
// Centralized state logic with reducer
const initialState = {
  items: [],
  discount: 0,
  shipping: 0,
  isLoading: false,
  error: null,
};

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      return {
        ...state,
        items: [...state.items, action.payload],
      };
    
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload),
      };
    
    case 'APPLY_DISCOUNT_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    
    case 'APPLY_DISCOUNT_SUCCESS':
      return {
        ...state,
        isLoading: false,
        discount: action.payload,
      };
    
    case 'APPLY_DISCOUNT_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload,
      };
    
    case 'SET_SHIPPING':
      return {
        ...state,
        shipping: action.payload,
      };
    
    case 'CLEAR_CART':
      return initialState;
    
    default:
      return state;
  }
}

function ShoppingCart() {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  
  const addItem = (item) => {
    dispatch({ type: 'ADD_ITEM', payload: item });
  };
  
  const applyDiscount = async (code) => {
    dispatch({ type: 'APPLY_DISCOUNT_START' });
    try {
      const discountValue = await validateCoupon(code);
      dispatch({ type: 'APPLY_DISCOUNT_SUCCESS', payload: discountValue });
    } catch (e) {
      dispatch({ type: 'APPLY_DISCOUNT_ERROR', payload: e.message });
    }
  };
  
  return (/* ... */);
}
```

**When to use useReducer:**
- Complex state logic with multiple sub-values
- Next state depends on previous state
- You want to centralize state update logic
- You want to test state logic separately
- State updates are scattered across handlers

**Related:** CONTEXT-USE, CUSTOM-HOOKS

---

#### USE-CONTEXT: Use Context Effectively

**Severity:** Warning

**Problematic code:**
```jsx
// Context with too much in one place
const AppContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [cart, setCart] = useState([]);
  const [notifications, setNotifications] = useState([]);
  
  // Any change re-renders all consumers!
  const value = { user, setUser, theme, setTheme, cart, setCart, notifications, setNotifications };
  
  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}
```

**Improved code:**
```jsx
// Split contexts by concern
const UserContext = createContext();
const ThemeContext = createContext();
const CartContext = createContext();

// Each context is independent
function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  
  const login = async (credentials) => {
    const userData = await authService.login(credentials);
    setUser(userData);
  };
  
  const logout = () => {
    authService.logout();
    setUser(null);
  };
  
  const value = useMemo(() => ({
    user, login, logout
  }), [user]);
  
  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const toggleTheme = useCallback(() => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  }, []);
  
  const value = useMemo(() => ({
    theme, toggleTheme
  }), [theme, toggleTheme]);
  
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

// Custom hooks for consuming
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Usage
function App() {
  return (
    <UserProvider>
      <ThemeProvider>
        <CartProvider>
          <Router />
        </CartProvider>
      </ThemeProvider>
    </UserProvider>
  );
}
```

**Best practices:**
- Split context by domain/concern
- Memoize context values
- Create custom hooks for consuming
- Throw error if used outside provider

**Related:** STATE-COLOCATION, USE-MEMO

---

#### USE-LAYOUT-EFFECT: Know When to Use useLayoutEffect

**Severity:** Info

**useEffect (runs after paint):**
```jsx
function Tooltip({ targetRef, content }) {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  
  useEffect(() => {
    const rect = targetRef.current.getBoundingClientRect();
    setPosition({ top: rect.bottom, left: rect.left });
  }, [targetRef]);
  
  // Problem: Tooltip may flash in wrong position briefly
  return <div style={{ position: 'absolute', ...position }}>{content}</div>;
}
```

**useLayoutEffect (runs before paint):**
```jsx
function Tooltip({ targetRef, content }) {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  
  useLayoutEffect(() => {
    const rect = targetRef.current.getBoundingClientRect();
    setPosition({ top: rect.bottom, left: rect.left });
  }, [targetRef]);
  
  // No flash - position set before browser paints
  return <div style={{ position: 'absolute', ...position }}>{content}</div>;
}

// Measuring DOM elements
function AutosizeTextarea({ value, onChange }) {
  const textareaRef = useRef(null);
  
  useLayoutEffect(() => {
    const textarea = textareaRef.current;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
  }, [value]);
  
  return (
    <textarea
      ref={textareaRef}
      value={value}
      onChange={onChange}
    />
  );
}
```

**When to use:**

| useEffect | useLayoutEffect |
|-----------|-----------------|
| Data fetching | DOM measurements |
| Subscriptions | Scroll position |
| Logging | Tooltips/popovers |
| Non-visual effects | Animations |
| Default choice | Preventing visual flicker |

**Note:** `useLayoutEffect` runs synchronously and can block painting. Use sparingly.

**Related:** USE-EFFECT-DEPS, USE-REF

---

#### OVER-MEMO: Don't Over-Memoize

**Severity:** Info

**Problematic code:**
```jsx
// Over-memoization - more harm than good
function ProductCard({ product }) {
  // Unnecessary - cheap calculation
  const formattedPrice = useMemo(() => {
    return `$${product.price.toFixed(2)}`;
  }, [product.price]);
  
  // Unnecessary - inline function is fine for non-memoized children
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);
  
  // Unnecessary - product is new every render anyway
  const productData = useMemo(() => ({
    id: product.id,
    name: product.name,
  }), [product.id, product.name]);
  
  return (
    <div onClick={handleClick}>
      <span>{product.name}</span>
      <span>{formattedPrice}</span>
    </div>
  );
}

// Memoizing everything
const Button = memo(({ children, onClick }) => {
  return <button onClick={onClick}>{children}</button>;
});
// Probably unnecessary - buttons are cheap to render
```

**Improved code:**
```jsx
// Only memoize when there's a real benefit
function ProductCard({ product }) {
  // Simple - just use inline
  const formattedPrice = `$${product.price.toFixed(2)}`;
  
  return (
    <div onClick={() => console.log('clicked')}>
      <span>{product.name}</span>
      <span>{formattedPrice}</span>
    </div>
  );
}

// Memoize when it matters
const ExpensiveChart = memo(({ data }) => {
  // Complex rendering worth memoizing
  return <svg>{/* ... */}</svg>;
});

function Dashboard({ data }) {
  // useMemo for expensive calculations
  const processedData = useMemo(() => {
    return data.map(item => heavyTransform(item));
  }, [data]);
  
  // useCallback when passed to memoized children
  const handleDataClick = useCallback((item) => {
    console.log('clicked:', item);
  }, []);
  
  return <ExpensiveChart data={processedData} onClick={handleDataClick} />;
}
```

**When memoization helps:**
- Expensive calculations (useMemo)
- Callbacks passed to memoized children (useCallback)
- Complex components that render slowly (memo)
- Referential equality matters for effects

**When memoization hurts:**
- Simple calculations (string formatting)
- Components that always re-render anyway
- Shallow objects that change every render
- Adds complexity without benefit

**Related:** USE-MEMO, USE-CALLBACK, MEMO-COMPONENT

---

### 3. Rendering & Performance (8 guidelines)

#### MEMO-COMPONENT: Memoize Components Appropriately

**Severity:** Warning

**Problematic code:**
```jsx
// Expensive component re-renders unnecessarily
function ProductList({ products, category }) {
  return (
    <div>
      <h2>{category}</h2>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

function ProductCard({ product }) {
  // Expensive rendering
  return (
    <div>
      <ComplexImage src={product.image} />
      <PriceCalculator price={product.price} />
    </div>
  );
}

// Parent re-render causes all ProductCards to re-render
```

**Improved code:**
```jsx
// Memoize expensive components
const ProductCard = memo(function ProductCard({ product }) {
  return (
    <div>
      <ComplexImage src={product.image} />
      <PriceCalculator price={product.price} />
    </div>
  );
});

// With custom comparison
const ProductCard = memo(
  function ProductCard({ product, onSelect }) {
    return (/* ... */);
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip render)
    return (
      prevProps.product.id === nextProps.product.id &&
      prevProps.product.price === nextProps.product.price
    );
  }
);

// Ensure stable props
function ProductList({ products, category }) {
  const handleSelect = useCallback((product) => {
    console.log('Selected:', product);
  }, []);
  
  return (
    <div>
      <h2>{category}</h2>
      {products.map(product => (
        <ProductCard 
          key={product.id} 
          product={product}
          onSelect={handleSelect}  // Stable reference
        />
      ))}
    </div>
  );
}
```

**When to use memo:**
- Rendering is expensive
- Component renders often with same props
- Component is pure (same props = same output)

**Related:** USE-CALLBACK, OVER-MEMO, KEY-PROP

---

#### KEY-PROP: Use Keys Correctly

**Severity:** Critical

**Problematic code:**
```jsx
// Using index as key - causes bugs on reorder
function TodoList({ todos }) {
  return todos.map((todo, index) => (
    <TodoItem key={index} todo={todo} />
  ));
}

// When todos reorder, wrong components update!

// No key - React warns
function TagList({ tags }) {
  return tags.map(tag => (
    <Tag tag={tag} />  // Warning: Each child should have a unique "key" prop
  ));
}
```

**Improved code:**
```jsx
// Use stable, unique ID
function TodoList({ todos }) {
  return todos.map(todo => (
    <TodoItem key={todo.id} todo={todo} />
  ));
}

// Key for state reset
function UserEditor({ userId }) {
  return (
    <EditForm 
      key={userId}  // Form state resets when userId changes
      userId={userId} 
    />
  );
}

// Compound key when needed
function CommentList({ comments }) {
  return comments.map(comment => (
    <Comment 
      key={`${comment.postId}-${comment.id}`} 
      comment={comment} 
    />
  ));
}
```

**Key rules:**
- Keys must be stable (don't change between renders)
- Keys must be unique among siblings
- Don't use index unless list is static and never reorders
- Use key to reset component state

**Related:** MEMO-COMPONENT, LIST-RENDER

---

#### LIST-RENDER: Optimize List Rendering

**Severity:** Warning

**Problematic code:**
```jsx
// Creating new objects/functions every render
function UserList({ users, onSelect }) {
  return users.map(user => (
    <UserCard
      key={user.id}
      user={{ ...user, fullName: `${user.first} ${user.last}` }}  // New object!
      onClick={() => onSelect(user)}  // New function!
      style={{ padding: 10 }}  // New object!
    />
  ));
}
```

**Improved code:**
```jsx
// Extract item component with memoization
const UserCard = memo(function UserCard({ user, onSelect }) {
  const fullName = `${user.first} ${user.last}`;
  
  return (
    <div className="user-card" onClick={() => onSelect(user)}>
      {fullName}
    </div>
  );
});

function UserList({ users, onSelect }) {
  // Stable callback
  const handleSelect = useCallback((user) => {
    onSelect(user);
  }, [onSelect]);
  
  return users.map(user => (
    <UserCard
      key={user.id}
      user={user}
      onSelect={handleSelect}
    />
  ));
}

// For very long lists, use virtualization
import { FixedSizeList } from 'react-window';

function VirtualizedUserList({ users }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <UserCard user={users[index]} />
    </div>
  );
  
  return (
    <FixedSizeList
      height={600}
      itemCount={users.length}
      itemSize={50}
    >
      {Row}
    </FixedSizeList>
  );
}
```

**Best practices:**
- Extract list items to separate memoized components
- Stabilize callbacks with useCallback
- Use CSS classes instead of inline styles
- Virtualize lists with 100+ items

**Related:** MEMO-COMPONENT, KEY-PROP, VIRTUAL-LIST

---

#### CONDITIONAL-RENDER: Handle Conditional Rendering Properly

**Severity:** Info

**Problematic code:**
```jsx
// Falsy value rendered
function Notifications({ count }) {
  return (
    <div>
      {count && <Badge count={count} />}  {/* Renders "0" when count is 0! */}
    </div>
  );
}

// Complex nested ternaries
function UserStatus({ user }) {
  return (
    <div>
      {user ? (
        user.isAdmin ? (
          user.isSuperAdmin ? (
            <SuperAdminBadge />
          ) : (
            <AdminBadge />
          )
        ) : user.isPremium ? (
          <PremiumBadge />
        ) : (
          <RegularBadge />
        )
      ) : (
        <GuestBadge />
      )}
    </div>
  );
}
```

**Improved code:**
```jsx
// Handle falsy values explicitly
function Notifications({ count }) {
  return (
    <div>
      {count > 0 && <Badge count={count} />}
      {/* Or use ternary */}
      {count ? <Badge count={count} /> : null}
    </div>
  );
}

// Extract complex conditionals
function UserStatus({ user }) {
  if (!user) return <GuestBadge />;
  if (user.isSuperAdmin) return <SuperAdminBadge />;
  if (user.isAdmin) return <AdminBadge />;
  if (user.isPremium) return <PremiumBadge />;
  return <RegularBadge />;
}

// Or use a mapping object
const BADGE_COMPONENTS = {
  superAdmin: SuperAdminBadge,
  admin: AdminBadge,
  premium: PremiumBadge,
  regular: RegularBadge,
  guest: GuestBadge,
};

function UserStatus({ user }) {
  const badgeType = getUserBadgeType(user);
  const BadgeComponent = BADGE_COMPONENTS[badgeType];
  return <BadgeComponent />;
}
```

**Conditional rendering patterns:**
- `{condition && <Component />}` - Watch for falsy values (0, '')
- `{condition ? <A /> : <B />}` - Explicit alternatives
- Early return - Clean for multiple conditions
- Object/Map lookup - Clean for many variants

**Related:** CHILDREN-PATTERN

---

#### AVOID-INLINE-OBJECTS: Avoid Creating Objects in JSX

**Severity:** Warning

**Problematic code:**
```jsx
function Dashboard() {
  return (
    <Chart
      // New object every render
      data={{ labels: ['A', 'B'], values: [1, 2] }}
      // New object every render
      options={{ animate: true, duration: 300 }}
      // New object every render
      style={{ width: 500, height: 300 }}
    />
  );
}

// Even with memo, Chart re-renders because props are new objects
const Chart = memo(({ data, options, style }) => {
  // Still re-renders!
});
```

**Improved code:**
```jsx
// Define outside component if static
const CHART_OPTIONS = { animate: true, duration: 300 };
const CHART_STYLE = { width: 500, height: 300 };

function Dashboard() {
  // Memoize if based on props/state
  const chartData = useMemo(() => ({
    labels: ['A', 'B'],
    values: [1, 2],
  }), []);
  
  return (
    <Chart
      data={chartData}
      options={CHART_OPTIONS}
      style={CHART_STYLE}
    />
  );
}

// Or use className instead of style
function Dashboard() {
  return <Chart className="dashboard-chart" />;
}
```

**Best practices:**
- Move static objects outside component
- Use useMemo for dynamic objects passed to memoized children
- Prefer className over inline styles
- Be especially careful in loops

**Related:** MEMO-COMPONENT, USE-MEMO, CSS-IN-JS

---

#### LAZY-LOADING: Lazy Load Components

**Severity:** Info

**Before optimization:**
```jsx
// All components loaded upfront
import HeavyChart from './HeavyChart';
import AdminPanel from './AdminPanel';
import Settings from './Settings';

function App() {
  const [tab, setTab] = useState('home');
  
  return (
    <div>
      {tab === 'chart' && <HeavyChart />}
      {tab === 'admin' && <AdminPanel />}
      {tab === 'settings' && <Settings />}
    </div>
  );
}
// All 3 components in initial bundle even if never used
```

**Improved code:**
```jsx
// Lazy load components
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));
const AdminPanel = lazy(() => import('./AdminPanel'));
const Settings = lazy(() => import('./Settings'));

function App() {
  const [tab, setTab] = useState('home');
  
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <div>
        {tab === 'chart' && <HeavyChart />}
        {tab === 'admin' && <AdminPanel />}
        {tab === 'settings' && <Settings />}
      </div>
    </Suspense>
  );
}

// Named exports with lazy
const HeavyChart = lazy(() => 
  import('./HeavyChart').then(module => ({ default: module.HeavyChart }))
);

// Prefetch on hover
function TabButton({ tab, onSelect }) {
  const handleMouseEnter = () => {
    if (tab === 'chart') {
      import('./HeavyChart');  // Prefetch
    }
  };
  
  return (
    <button 
      onMouseEnter={handleMouseEnter}
      onClick={() => onSelect(tab)}
    >
      {tab}
    </button>
  );
}
```

**What to lazy load:**
- Route components
- Modals and dialogs
- Heavy visualizations (charts, maps)
- Admin-only features
- Below-the-fold content

**Related:** CODE-SPLITTING, SUSPENSE

---

#### SUSPENSE: Use Suspense for Loading States

**Severity:** Info

**Problematic code:**
```jsx
// Manual loading states everywhere
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    Promise.all([
      fetchUser(userId),
      fetchPosts(userId)
    ]).then(([user, posts]) => {
      setUser(user);
      setPosts(posts);
      setLoading(false);
    });
  }, [userId]);
  
  if (loading) return <Spinner />;
  
  return (
    <div>
      <UserInfo user={user} />
      <PostList posts={posts} />
    </div>
  );
}
```

**Improved code:**
```jsx
// Using Suspense with data fetching libraries
import { Suspense } from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserProfileContent userId={userId} />
    </Suspense>
  );
}

function UserProfileContent({ userId }) {
  // These suspend while loading
  const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  
  const { data: posts } = useSuspenseQuery({
    queryKey: ['posts', userId],
    queryFn: () => fetchPosts(userId),
  });
  
  return (
    <div>
      <UserInfo user={user} />
      <PostList posts={posts} />
    </div>
  );
}

// Nested Suspense for granular loading
function Dashboard() {
  return (
    <div>
      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>
      
      <div className="content">
        <Suspense fallback={<SidebarSkeleton />}>
          <Sidebar />
        </Suspense>
        
        <Suspense fallback={<MainContentSkeleton />}>
          <MainContent />
        </Suspense>
      </div>
    </div>
  );
}
```

**Suspense benefits:**
- Declarative loading states
- Automatic loading coordination
- Better user experience
- Works with lazy loading and data fetching

**Related:** LAZY-LOADING, ERROR-BOUNDARY

---

#### TRANSITIONS: Use Transitions for Non-Urgent Updates

**Severity:** Info

**Problematic code:**
```jsx
// Expensive update blocks UI
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  
  const handleSearch = (newQuery) => {
    setQuery(newQuery);
    // Expensive filtering blocks input
    const filtered = items.filter(item => 
      item.name.toLowerCase().includes(newQuery.toLowerCase())
    );
    setResults(filtered);
  };
  
  return (
    <div>
      <input onChange={e => handleSearch(e.target.value)} />
      <ResultsList results={results} />  {/* Blocks typing */}
    </div>
  );
}
```

**Improved code:**
```jsx
// useTransition for non-urgent updates
import { useState, useTransition } from 'react';

function SearchResults({ items }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();
  
  const handleSearch = (newQuery) => {
    // Urgent: update input immediately
    setQuery(newQuery);
    
    // Non-urgent: can be interrupted
    startTransition(() => {
      const filtered = items.filter(item => 
        item.name.toLowerCase().includes(newQuery.toLowerCase())
      );
      setResults(filtered);
    });
  };
  
  return (
    <div>
      <input value={query} onChange={e => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </div>
  );
}

// useDeferredValue for derived values
import { useDeferredValue } from 'react';

function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  
  const results = useMemo(() => {
    return items.filter(item => 
      item.name.includes(deferredQuery)
    );
  }, [deferredQuery]);
  
  return (
    <div style={{ opacity: isStale ? 0.5 : 1 }}>
      <ResultsList results={results} />
    </div>
  );
}
```

**When to use:**
- `useTransition`: When you control the state update
- `useDeferredValue`: When the value comes from props

**Related:** USE-MEMO, DEBOUNCE

---

### 4. Patterns (8 guidelines)

#### COMPOUND-COMPONENTS: Use Compound Components Pattern

**Severity:** Info

**Monolithic component:**
```jsx
// All configuration through props
<Accordion
  items={[
    { title: 'Section 1', content: 'Content 1', disabled: false },
    { title: 'Section 2', content: 'Content 2', disabled: true },
  ]}
  allowMultiple={true}
  defaultExpanded={[0]}
  onChange={handleChange}
  headerClassName="custom-header"
  contentClassName="custom-content"
/>

// Hard to customize, long prop list
```

**Improved code:**
```jsx
// Compound components - flexible composition
const AccordionContext = createContext();

function Accordion({ children, allowMultiple = false, defaultExpanded = [] }) {
  const [expanded, setExpanded] = useState(new Set(defaultExpanded));
  
  const toggle = useCallback((id) => {
    setExpanded(prev => {
      const next = new Set(allowMultiple ? prev : []);
      if (prev.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }, [allowMultiple]);
  
  return (
    <AccordionContext.Provider value={{ expanded, toggle }}>
      <div className="accordion">{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({ id, disabled = false, children }) {
  const { expanded, toggle } = useContext(AccordionContext);
  const isExpanded = expanded.has(id);
  
  return (
    <div className={`accordion-item ${isExpanded ? 'expanded' : ''}`}>
      {React.Children.map(children, child =>
        React.cloneElement(child, { isExpanded, onToggle: () => toggle(id), disabled })
      )}
    </div>
  );
}

function AccordionHeader({ children, isExpanded, onToggle, disabled }) {
  return (
    <button 
      className="accordion-header"
      onClick={onToggle}
      disabled={disabled}
      aria-expanded={isExpanded}
    >
      {children}
      <ChevronIcon direction={isExpanded ? 'up' : 'down'} />
    </button>
  );
}

function AccordionContent({ children, isExpanded }) {
  if (!isExpanded) return null;
  return <div className="accordion-content">{children}</div>;
}

// Usage - highly flexible
<Accordion allowMultiple defaultExpanded={['section-1']}>
  <AccordionItem id="section-1">
    <AccordionHeader>
      <Icon name="settings" />
      Settings
    </AccordionHeader>
    <AccordionContent>
      <SettingsForm />
    </AccordionContent>
  </AccordionItem>
  
  <AccordionItem id="section-2" disabled>
    <AccordionHeader>Advanced (Premium)</AccordionHeader>
    <AccordionContent>
      <AdvancedSettings />
    </AccordionContent>
  </AccordionItem>
</Accordion>
```

**Benefits:**
- Maximum flexibility
- Clear component structure
- Inversion of control
- Easy to customize individual parts

**Related:** CHILDREN-PATTERN, RENDER-PROPS

---

#### RENDER-PROPS: Use Render Props for Flexible Rendering

**Severity:** Info

**Standard approach:**
```jsx
// Component controls rendering
function MouseTracker() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);
  
  // Fixed rendering - not reusable
  return <div>Mouse: {position.x}, {position.y}</div>;
}
```

**Render props pattern:**
```jsx
// Consumer controls rendering
function MouseTracker({ children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);
  
  return children(position);
}

// Usage - flexible rendering
<MouseTracker>
  {({ x, y }) => <div>Mouse: {x}, {y}</div>}
</MouseTracker>

<MouseTracker>
  {({ x, y }) => <Cursor style={{ left: x, top: y }} />}
</MouseTracker>

// Modern alternative: custom hook (usually preferred)
function useMousePosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMove = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, []);
  
  return position;
}

// Usage - cleaner
function MyComponent() {
  const { x, y } = useMousePosition();
  return <div>Mouse: {x}, {y}</div>;
}
```

**When to use render props vs hooks:**
- **Hooks**: Logic reuse (preferred in most cases)
- **Render props**: When you need component lifecycle (e.g., error boundaries)

**Related:** CUSTOM-HOOKS, COMPOUND-COMPONENTS

---

#### HIGHER-ORDER-COMPONENTS: Use HOCs Sparingly

**Severity:** Info

**HOC pattern:**
```jsx
// Higher-Order Component
function withAuth(WrappedComponent) {
  return function AuthenticatedComponent(props) {
    const { user, loading } = useAuth();
    
    if (loading) return <Spinner />;
    if (!user) return <Redirect to="/login" />;
    
    return <WrappedComponent {...props} user={user} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);

// Problems:
// - Props origin unclear (where does 'user' come from?)
// - Wrapper hell when combining multiple HOCs
// - Static methods need to be hoisted
// - Refs don't pass through automatically
```

**Modern alternatives:**
```jsx
// Custom hook (preferred)
function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    authService.getCurrentUser()
      .then(setUser)
      .finally(() => setLoading(false));
  }, []);
  
  return { user, loading };
}

// Component using hook
function Dashboard() {
  const { user, loading } = useAuth();
  
  if (loading) return <Spinner />;
  if (!user) return <Redirect to="/login" />;
  
  return <div>Welcome, {user.name}</div>;
}

// Or wrapper component
function RequireAuth({ children }) {
  const { user, loading } = useAuth();
  
  if (loading) return <Spinner />;
  if (!user) return <Navigate to="/login" />;
  
  return children;
}

// Usage
<RequireAuth>
  <Dashboard />
</RequireAuth>
```

**When HOCs are still useful:**
- Integrating with class-based libraries
- Cross-cutting concerns (logging, error tracking)
- When you need to wrap entire component subtrees

**Related:** CUSTOM-HOOKS, RENDER-PROPS

---

#### CONTROLLED-COMPONENTS: Build Controlled Components

**Severity:** Info

**Uncontrolled (internal state):**
```jsx
// Component manages its own state
function Dropdown({ options, onChange }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  
  const handleSelect = (option) => {
    setSelected(option);
    setIsOpen(false);
    onChange?.(option);
  };
  
  return (/* ... */);
}

// Consumer can't control selected value externally
```

**Controlled (external state):**
```jsx
// Allow both controlled and uncontrolled usage
function Dropdown({ 
  options, 
  value,           // Controlled value
  onChange,        // Controlled onChange
  defaultValue,    // Uncontrolled default
  isOpen: controlledIsOpen,
  onOpenChange,
}) {
  // Support both controlled and uncontrolled
  const [internalValue, setInternalValue] = useState(defaultValue);
  const isControlled = value !== undefined;
  const selectedValue = isControlled ? value : internalValue;
  
  const [internalIsOpen, setInternalIsOpen] = useState(false);
  const isOpenControlled = controlledIsOpen !== undefined;
  const isOpen = isOpenControlled ? controlledIsOpen : internalIsOpen;
  
  const handleSelect = (option) => {
    if (!isControlled) {
      setInternalValue(option);
    }
    onChange?.(option);
    
    if (!isOpenControlled) {
      setInternalIsOpen(false);
    }
    onOpenChange?.(false);
  };
  
  return (/* ... */);
}

// Usage - controlled
const [selected, setSelected] = useState(null);
<Dropdown value={selected} onChange={setSelected} options={options} />

// Usage - uncontrolled
<Dropdown defaultValue={options[0]} onChange={console.log} options={options} />
```

**Pattern benefits:**
- Flexible for consumers
- Can be controlled or uncontrolled
- Works well with form libraries

**Related:** CONTROLLED-VS-UNCONTROLLED, PROP-TYPES

---

#### CONTAINER-PRESENTATIONAL: Separate Logic from Presentation

**Severity:** Info

**Mixed concerns:**
```jsx
// Component does both data fetching and rendering
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('name');
  
  useEffect(() => {
    fetchUsers().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);
  
  const sortedUsers = useMemo(() => {
    return [...users].sort((a, b) => a[sortBy].localeCompare(b[sortBy]));
  }, [users, sortBy]);
  
  if (loading) return <Spinner />;
  
  return (
    <div className="user-list">
      <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
        <option value="name">Name</option>
        <option value="email">Email</option>
      </select>
      {sortedUsers.map(user => (
        <div key={user.id} className="user-card">
          <img src={user.avatar} alt="" />
          <span>{user.name}</span>
          <span>{user.email}</span>
        </div>
      ))}
    </div>
  );
}
```

**Separated concerns:**
```jsx
// Custom hook for data/logic
function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('name');
  
  useEffect(() => {
    fetchUsers().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);
  
  const sortedUsers = useMemo(() => {
    return [...users].sort((a, b) => a[sortBy].localeCompare(b[sortBy]));
  }, [users, sortBy]);
  
  return { users: sortedUsers, loading, sortBy, setSortBy };
}

// Presentational component - pure rendering
function UserListView({ users, sortBy, onSortChange }) {
  return (
    <div className="user-list">
      <SortSelect value={sortBy} onChange={onSortChange} />
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

function UserCard({ user }) {
  return (
    <div className="user-card">
      <img src={user.avatar} alt="" />
      <span>{user.name}</span>
      <span>{user.email}</span>
    </div>
  );
}

// Container - connects logic to presentation
function UserList() {
  const { users, loading, sortBy, setSortBy } = useUsers();
  
  if (loading) return <Spinner />;
  
  return (
    <UserListView 
      users={users} 
      sortBy={sortBy} 
      onSortChange={setSortBy} 
    />
  );
}
```

**Benefits:**
- Easier to test (test logic and UI separately)
- Better reusability (presentational components are pure)
- Clearer separation of concerns
- Storybook-friendly (presentational components)

**Related:** CUSTOM-HOOKS, SINGLE-RESPONSIBILITY

---

#### FORWARD-REF: Forward Refs to DOM Elements

**Severity:** Warning

**Problematic code:**
```jsx
// Can't get ref to input
function CustomInput({ label, ...props }) {
  return (
    <div>
      <label>{label}</label>
      <input {...props} />
    </div>
  );
}

// This doesn't work!
function Form() {
  const inputRef = useRef();
  
  return (
    <CustomInput ref={inputRef} label="Name" />  // ref goes to CustomInput, not input
  );
}
```

**Improved code:**
```jsx
// Forward ref to DOM element
const CustomInput = forwardRef(function CustomInput({ label, ...props }, ref) {
  return (
    <div>
      <label>{label}</label>
      <input ref={ref} {...props} />
    </div>
  );
});

// Now ref works
function Form() {
  const inputRef = useRef();
  
  useEffect(() => {
    inputRef.current?.focus();  // Works!
  }, []);
  
  return <CustomInput ref={inputRef} label="Name" />;
}

// With useImperativeHandle for custom ref API
const CustomInput = forwardRef(function CustomInput({ label, ...props }, ref) {
  const inputRef = useRef();
  
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    clear: () => { inputRef.current.value = ''; },
    getValue: () => inputRef.current?.value,
  }), []);
  
  return (
    <div>
      <label>{label}</label>
      <input ref={inputRef} {...props} />
    </div>
  );
});

// Usage
function Form() {
  const inputRef = useRef();
  
  const handleClear = () => {
    inputRef.current?.clear();
    inputRef.current?.focus();
  };
  
  return (
    <div>
      <CustomInput ref={inputRef} label="Name" />
      <button onClick={handleClear}>Clear</button>
    </div>
  );
}
```

**When to forward refs:**
- Wrapper components around inputs
- Focus management
- Animation libraries
- Third-party component integration

**Related:** USE-REF, USE-IMPERATIVE-HANDLE

---

#### PORTALS: Use Portals for Modals and Tooltips

**Severity:** Info

**Problematic code:**
```jsx
// Modal rendered inside deeply nested component
function Card() {
  const [showModal, setShowModal] = useState(false);
  
  return (
    <div className="card" style={{ overflow: 'hidden' }}>
      <button onClick={() => setShowModal(true)}>Open</button>
      {showModal && (
        // Modal trapped by overflow:hidden and z-index stacking!
        <div className="modal">
          <ModalContent />
        </div>
      )}
    </div>
  );
}
```

**Improved code:**
```jsx
import { createPortal } from 'react-dom';

// Modal rendered at document root
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;
  
  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body  // Renders here, not in component tree
  );
}

function Card() {
  const [showModal, setShowModal] = useState(false);
  
  return (
    <div className="card" style={{ overflow: 'hidden' }}>
      <button onClick={() => setShowModal(true)}>Open</button>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)}>
        <ModalContent />
      </Modal>
    </div>
  );
}

// Tooltip with portal
function Tooltip({ targetRef, content, isOpen }) {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  
  useLayoutEffect(() => {
    if (isOpen && targetRef.current) {
      const rect = targetRef.current.getBoundingClientRect();
      setPosition({
        top: rect.bottom + window.scrollY,
        left: rect.left + window.scrollX,
      });
    }
  }, [isOpen, targetRef]);
  
  if (!isOpen) return null;
  
  return createPortal(
    <div className="tooltip" style={{ position: 'absolute', ...position }}>
      {content}
    </div>,
    document.body
  );
}
```

**When to use portals:**
- Modals and dialogs
- Tooltips and popovers
- Dropdown menus
- Notifications/toasts
- Anything that needs to break out of parent CSS

**Related:** USE-LAYOUT-EFFECT, FOCUS-TRAP

---

#### CONTEXT-MODULE: Organize Context with Module Pattern

**Severity:** Info

**Scattered context:**
```jsx
// Context spread across files
// userContext.js
export const UserContext = createContext();

// UserProvider.js
export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  return <UserContext.Provider value={{ user, setUser }}>{children}</UserContext.Provider>;
}

// useUser.js
export function useUser() {
  return useContext(UserContext);
}

// Consumer has to know about all these
```

**Organized module:**
```jsx
// userContext.js - everything in one place
import { createContext, useContext, useState, useCallback, useMemo } from 'react';

const UserContext = createContext(undefined);

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const login = useCallback(async (credentials) => {
    setLoading(true);
    try {
      const userData = await authService.login(credentials);
      setUser(userData);
      return userData;
    } finally {
      setLoading(false);
    }
  }, []);
  
  const logout = useCallback(async () => {
    await authService.logout();
    setUser(null);
  }, []);
  
  const value = useMemo(() => ({
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
  }), [user, loading, login, logout]);
  
  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}

// Optional: export types for TypeScript
// export type { UserContextValue };
```

**Benefits:**
- Everything in one file
- Clear API (only export Provider and hook)
- Error if used outside provider
- Type-safe (TypeScript)

**Related:** USE-CONTEXT, CUSTOM-HOOKS

---

### 5. Accessibility (8 guidelines)

#### SEMANTIC-HTML: Use Semantic HTML Elements

**Severity:** Warning

**Problematic code:**
```jsx
// Divs for everything
function Navigation() {
  return (
    <div className="nav">
      <div className="nav-item" onClick={goHome}>Home</div>
      <div className="nav-item" onClick={goAbout}>About</div>
    </div>
  );
}

function Article() {
  return (
    <div className="article">
      <div className="title">Article Title</div>
      <div className="content">Article content...</div>
    </div>
  );
}
```

**Improved code:**
```jsx
// Semantic HTML elements
function Navigation() {
  return (
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  );
}

function Article() {
  return (
    <article>
      <header>
        <h1>Article Title</h1>
      </header>
      <main>
        <p>Article content...</p>
      </main>
      <footer>
        <time dateTime="2024-01-15">January 15, 2024</time>
      </footer>
    </article>
  );
}

// Semantic elements reference:
// <header> - Introductory content
// <nav> - Navigation links
// <main> - Main content (one per page)
// <article> - Self-contained content
// <section> - Thematic grouping
// <aside> - Tangentially related content
// <footer> - Footer content
// <figure> - Self-contained media
// <time> - Date/time
// <address> - Contact information
```

**Why semantics matter:**
- Screen readers announce element types
- Better SEO
- Easier styling with element selectors
- Built-in browser behaviors

**Related:** ARIA-LABELS, HEADING-ORDER

---

#### ARIA-LABELS: Use ARIA Attributes Correctly

**Severity:** Warning

**Problematic code:**
```jsx
// Missing accessible labels
function SearchForm() {
  return (
    <form>
      <input type="text" placeholder="Search..." />
      <button><SearchIcon /></button>  {/* No accessible label! */}
    </form>
  );
}

function Accordion({ items }) {
  return items.map(item => (
    <div key={item.id}>
      <div onClick={() => toggle(item.id)}>
        {item.title}
      </div>
      <div>{item.content}</div>
    </div>
  ));
}
```

**Improved code:**
```jsx
// Properly labeled
function SearchForm() {
  return (
    <form role="search">
      <label htmlFor="search" className="sr-only">Search</label>
      <input 
        id="search"
        type="search" 
        placeholder="Search..."
        aria-label="Search"  // Alternative to label
      />
      <button type="submit" aria-label="Submit search">
        <SearchIcon aria-hidden="true" />
      </button>
    </form>
  );
}

function Accordion({ items }) {
  const [expanded, setExpanded] = useState(new Set());
  
  return (
    <div>
      {items.map(item => {
        const isExpanded = expanded.has(item.id);
        return (
          <div key={item.id}>
            <button
              aria-expanded={isExpanded}
              aria-controls={`content-${item.id}`}
              onClick={() => toggle(item.id)}
            >
              {item.title}
            </button>
            <div 
              id={`content-${item.id}`}
              role="region"
              aria-labelledby={`header-${item.id}`}
              hidden={!isExpanded}
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// Common ARIA patterns
// aria-label: Text label for element
// aria-labelledby: ID of labeling element
// aria-describedby: ID of describing element
// aria-expanded: Expandable state
// aria-controls: ID of controlled element
// aria-hidden: Hide from screen readers
// aria-live: Announce dynamic content
// role: Override semantic role
```

**Related:** SEMANTIC-HTML, SCREEN-READER

---

#### KEYBOARD-NAV: Ensure Keyboard Navigation

**Severity:** Critical

**Problematic code:**
```jsx
// Click-only interactions
function Dropdown({ options, onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div className="dropdown">
      <div onClick={() => setIsOpen(!isOpen)}>
        Select option
      </div>
      {isOpen && (
        <div className="options">
          {options.map(opt => (
            <div key={opt.id} onClick={() => onSelect(opt)}>
              {opt.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

**Improved code:**
```jsx
// Full keyboard support
function Dropdown({ options, onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const buttonRef = useRef(null);
  const optionsRef = useRef([]);
  
  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen && focusedIndex >= 0) {
          onSelect(options[focusedIndex]);
          setIsOpen(false);
          buttonRef.current?.focus();
        } else {
          setIsOpen(true);
        }
        break;
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setFocusedIndex(i => Math.min(i + 1, options.length - 1));
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex(i => Math.max(i - 1, 0));
        break;
      case 'Escape':
        setIsOpen(false);
        buttonRef.current?.focus();
        break;
      case 'Tab':
        setIsOpen(false);
        break;
    }
  };
  
  useEffect(() => {
    if (focusedIndex >= 0) {
      optionsRef.current[focusedIndex]?.focus();
    }
  }, [focusedIndex]);
  
  return (
    <div className="dropdown" onKeyDown={handleKeyDown}>
      <button
        ref={buttonRef}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
      >
        Select option
      </button>
      {isOpen && (
        <ul role="listbox" aria-label="Options">
          {options.map((opt, index) => (
            <li
              key={opt.id}
              role="option"
              ref={el => optionsRef.current[index] = el}
              tabIndex={-1}
              aria-selected={focusedIndex === index}
              onClick={() => onSelect(opt)}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

**Keyboard requirements:**
- Tab: Move to next focusable element
- Shift+Tab: Move to previous
- Enter/Space: Activate buttons/links
- Arrow keys: Navigate within widgets
- Escape: Close modals/dropdowns

**Related:** FOCUS-MANAGEMENT, ARIA-LABELS

---

#### FOCUS-MANAGEMENT: Manage Focus Properly

**Severity:** Warning

**Problematic code:**
```jsx
// Focus lost after modal closes
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal">
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
```

**Improved code:**
```jsx
// Focus trap and restoration
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef(null);
  const previousActiveElement = useRef(null);
  
  // Save and restore focus
  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement;
      modalRef.current?.focus();
    }
    
    return () => {
      if (previousActiveElement.current) {
        previousActiveElement.current.focus();
      }
    };
  }, [isOpen]);
  
  // Trap focus inside modal
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
      return;
    }
    
    if (e.key !== 'Tab') return;
    
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements?.[0];
    const lastElement = focusableElements?.[focusableElements.length - 1];
    
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement?.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement?.focus();
    }
  };
  
  if (!isOpen) return null;
  
  return createPortal(
    <div 
      className="modal-overlay" 
      onClick={onClose}
      onKeyDown={handleKeyDown}
    >
      <div 
        ref={modalRef}
        className="modal"
        role="dialog"
        aria-modal="true"
        tabIndex={-1}
        onClick={e => e.stopPropagation()}
      >
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>,
    document.body
  );
}

// Or use a library
import { FocusTrap } from 'focus-trap-react';

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;
  
  return (
    <FocusTrap>
      <div className="modal" role="dialog" aria-modal="true">
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </FocusTrap>
  );
}
```

**Focus management rules:**
- Modals: Focus first focusable element, trap focus, restore on close
- Delete actions: Focus previous/next item
- Navigation: Focus main content after route change
- Errors: Focus first error field

**Related:** KEYBOARD-NAV, PORTALS

---

#### HEADING-ORDER: Use Correct Heading Hierarchy

**Severity:** Warning

**Problematic code:**
```jsx
// Skipped heading levels
function ProductPage() {
  return (
    <div>
      <h1>Product Name</h1>
      <h4>Description</h4>  {/* Skipped h2, h3! */}
      <h2>Reviews</h2>
      <h5>Review 1</h5>  {/* Inconsistent */}
    </div>
  );
}
```

**Improved code:**
```jsx
// Proper heading hierarchy
function ProductPage() {
  return (
    <article>
      <h1>Product Name</h1>
      
      <section>
        <h2>Description</h2>
        <p>Product description...</p>
      </section>
      
      <section>
        <h2>Reviews</h2>
        <article>
          <h3>Great product!</h3>
          <p>Review content...</p>
        </article>
        <article>
          <h3>Highly recommended</h3>
          <p>Review content...</p>
        </article>
      </section>
    </article>
  );
}

// For component flexibility, accept heading level as prop
function Section({ title, level = 2, children }) {
  const Heading = `h${level}`;
  
  return (
    <section>
      <Heading>{title}</Heading>
      {children}
    </section>
  );
}

// Usage
<Section title="Main Section" level={2}>
  <Section title="Subsection" level={3}>
    Content
  </Section>
</Section>
```

**Heading rules:**
- One `<h1>` per page (usually)
- Don't skip levels (h1 → h3)
- Headings reflect document outline
- Use CSS for visual sizing, not heading level

**Related:** SEMANTIC-HTML, SCREEN-READER

---

#### SCREEN-READER: Consider Screen Reader Experience

**Severity:** Warning

**Problematic code:**
```jsx
// Not screen reader friendly
function Notification({ type, message }) {
  return (
    <div className={`notification ${type}`}>
      <span className="icon" />  {/* Meaningless to SR */}
      {message}
    </div>
  );
}

function DataTable({ data }) {
  return (
    <div className="table">
      <div className="row header">
        <div>Name</div>
        <div>Age</div>
      </div>
      {data.map(row => (
        <div className="row" key={row.id}>
          <div>{row.name}</div>
          <div>{row.age}</div>
        </div>
      ))}
    </div>
  );
}
```

**Improved code:**
```jsx
// Screen reader friendly
function Notification({ type, message }) {
  const typeLabels = {
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
  };
  
  return (
    <div 
      className={`notification ${type}`}
      role="alert"
      aria-live="polite"
    >
      <span className="icon" aria-hidden="true" />
      <span className="sr-only">{typeLabels[type]}:</span>
      {message}
    </div>
  );
}

function DataTable({ data, caption }) {
  return (
    <table>
      <caption>{caption}</caption>
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Age</th>
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.id}>
            <td>{row.name}</td>
            <td>{row.age}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Screen reader only text utility
function ScreenReaderOnly({ children }) {
  return (
    <span 
      className="sr-only"
      style={{
        position: 'absolute',
        width: '1px',
        height: '1px',
        padding: 0,
        margin: '-1px',
        overflow: 'hidden',
        clip: 'rect(0, 0, 0, 0)',
        whiteSpace: 'nowrap',
        border: 0,
      }}
    >
      {children}
    </span>
  );
}
```

**Screen reader considerations:**
- Use semantic HTML (better than ARIA)
- Hide decorative content with aria-hidden
- Provide text alternatives for icons
- Use live regions for dynamic content
- Test with actual screen readers

**Related:** ARIA-LABELS, SEMANTIC-HTML

---

#### COLOR-CONTRAST: Ensure Sufficient Color Contrast

**Severity:** Warning

**Problematic code:**
```jsx
// Poor contrast
function Button({ disabled, children }) {
  return (
    <button
      disabled={disabled}
      style={{
        backgroundColor: '#eee',
        color: disabled ? '#ccc' : '#999',  // Poor contrast!
      }}
    >
      {children}
    </button>
  );
}
```

**Improved code:**
```jsx
// WCAG compliant contrast
function Button({ disabled, children }) {
  return (
    <button
      disabled={disabled}
      style={{
        backgroundColor: '#0066cc',
        color: '#ffffff',  // 7:1 contrast ratio
        // Disabled state still readable
        opacity: disabled ? 0.6 : 1,
      }}
    >
      {children}
    </button>
  );
}

// Use CSS custom properties for theming
function Button({ variant = 'primary', children }) {
  return (
    <button className={`btn btn-${variant}`}>
      {children}
    </button>
  );
}

/* CSS */
/*
.btn-primary {
  --bg: #0066cc;
  --fg: #ffffff;
  background: var(--bg);
  color: var(--fg);
}

.btn-secondary {
  --bg: #ffffff;
  --fg: #0066cc;
  background: var(--bg);
  color: var(--fg);
  border: 2px solid var(--fg);
}
*/
```

**WCAG contrast requirements:**
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- UI components: 3:1 minimum
- Use tools to verify (Chrome DevTools, WebAIM)

**Related:** FOCUS-VISIBLE

---

#### FOCUS-VISIBLE: Style Focus States

**Severity:** Warning

**Problematic code:**
```jsx
// Removed focus outline entirely
function Button({ children, onClick }) {
  return (
    <button 
      onClick={onClick}
      style={{ outline: 'none' }}  // Removes focus indicator!
    >
      {children}
    </button>
  );
}
```

**Improved code:**
```jsx
// Custom focus styles
function Button({ children, onClick }) {
  return (
    <button 
      onClick={onClick}
      className="btn"
    >
      {children}
    </button>
  );
}

/* CSS */
/*
.btn:focus {
  outline: none;  // Remove default
}

.btn:focus-visible {
  // Only show focus ring for keyboard navigation
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

// For older browser support
.btn:focus:not(:focus-visible) {
  outline: none;
}
*/

// Or inline with focus-visible polyfill
import 'focus-visible';

function Button({ children, onClick }) {
  return (
    <button 
      onClick={onClick}
      style={{ 
        // Will only show for keyboard focus
        '--focus-ring': '2px solid #0066cc',
      }}
      className="focus-styled"
    >
      {children}
    </button>
  );
}
```

**Focus styling rules:**
- Never remove focus indicator completely
- Use `:focus-visible` for keyboard-only styles
- Make focus clearly visible (color, size)
- Test with keyboard navigation

**Related:** KEYBOARD-NAV, COLOR-CONTRAST

---

### 6. Error Handling (5 guidelines)

#### ERROR-BOUNDARY: Use Error Boundaries

**Severity:** Critical

**Problematic code:**
```jsx
// Unhandled error crashes entire app
function App() {
  return (
    <div>
      <Header />
      <UserProfile />  {/* Error here crashes everything */}
      <Footer />
    </div>
  );
}
```

**Improved code:**
```jsx
// Error boundary catches errors
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log to error reporting service
    logErrorToService(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorUI error={this.state.error} />;
    }
    
    return this.props.children;
  }
}

// Usage - isolate error impact
function App() {
  return (
    <div>
      <Header />
      <ErrorBoundary fallback={<UserProfileError />}>
        <UserProfile />
      </ErrorBoundary>
      <Footer />
    </div>
  );
}

// Reusable with reset capability
function ErrorBoundaryWithReset({ children, fallback }) {
  const [key, setKey] = useState(0);
  
  return (
    <ErrorBoundary
      key={key}
      fallback={
        <ErrorFallback 
          onReset={() => setKey(k => k + 1)}
        />
      }
    >
      {children}
    </ErrorBoundary>
  );
}

// Or use react-error-boundary library
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={logError}
      onReset={() => window.location.reload()}
    >
      <UserProfile />
    </ErrorBoundary>
  );
}
```

**Error boundary placement:**
- Around route components
- Around feature sections
- Around risky third-party components
- NOT for event handlers (use try/catch)

**Related:** SUSPENSE, ASYNC-ERROR

---

#### ASYNC-ERROR: Handle Async Errors Properly

**Severity:** Warning

**Problematic code:**
```jsx
// Unhandled promise rejection
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
    // What if fetch fails?
  }, [userId]);
  
  return <div>{user?.name}</div>;
}

// Error state not communicated
async function handleSubmit(data) {
  await saveData(data);  // What if this fails?
}
```

**Improved code:**
```jsx
// Proper async error handling
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    
    fetchUser(userId)
      .then(data => {
        if (!cancelled) setUser(data);
      })
      .catch(err => {
        if (!cancelled) setError(err);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    
    return () => { cancelled = true; };
  }, [userId]);
  
  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} onRetry={() => {}} />;
  return <div>{user?.name}</div>;
}

// With async/await
useEffect(() => {
  async function loadUser() {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchUser(userId);
      setUser(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }
  loadUser();
}, [userId]);

// Event handler error handling
function Form() {
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    
    try {
      await saveData(formData);
      showSuccess('Saved!');
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {error && <Alert type="error">{error}</Alert>}
      <button type="submit" disabled={submitting}>
        {submitting ? 'Saving...' : 'Save'}
      </button>
    </form>
  );
}
```

**Related:** ERROR-BOUNDARY, LOADING-STATE

---

#### LOADING-STATE: Handle Loading States

**Severity:** Info

**Problematic code:**
```jsx
// Abrupt loading transitions
function DataList() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetchData().then(setData);
  }, []);
  
  if (!data) return null;  // Blank screen!
  
  return <List items={data} />;
}
```

**Improved code:**
```jsx
// Good loading UX
function DataList() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    setLoading(true);
    fetchData()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <ListSkeleton />;
  if (!data?.length) return <EmptyState />;
  
  return <List items={data} />;
}

// Skeleton loading
function ListSkeleton() {
  return (
    <div className="list">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="skeleton-item" />
      ))}
    </div>
  );
}

// Avoid loading flash for fast responses
function DataList() {
  const [data, setData] = useState(null);
  const [showLoading, setShowLoading] = useState(false);
  
  useEffect(() => {
    let loadingTimer;
    let cancelled = false;
    
    // Only show loading after 200ms delay
    loadingTimer = setTimeout(() => {
      if (!cancelled) setShowLoading(true);
    }, 200);
    
    fetchData()
      .then(data => {
        if (!cancelled) setData(data);
      })
      .finally(() => {
        clearTimeout(loadingTimer);
        if (!cancelled) setShowLoading(false);
      });
    
    return () => { cancelled = true; };
  }, []);
  
  if (showLoading) return <Spinner />;
  if (!data) return null;  // Brief moment before data or loading
  
  return <List items={data} />;
}
```

**Loading state best practices:**
- Show skeleton/placeholder instead of spinner when possible
- Delay loading indicator for fast responses
- Preserve layout during loading
- Show progress for long operations

**Related:** ASYNC-ERROR, SUSPENSE

---

#### FORM-VALIDATION: Provide Clear Validation Feedback

**Severity:** Warning

**Problematic code:**
```jsx
// Poor validation UX
function Form() {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email.includes('@')) {
      alert('Invalid email');  // Poor UX!
      return;
    }
    submit();
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="email" />
      <button>Submit</button>
    </form>
  );
}
```

**Improved code:**
```jsx
// Good validation UX
function Form() {
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  
  const validate = (values) => {
    const errors = {};
    if (!values.email) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(values.email)) {
      errors.email = 'Please enter a valid email';
    }
    return errors;
  };
  
  const handleBlur = (field) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    setErrors(validate({ email }));
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate({ email });
    setErrors(validationErrors);
    setTouched({ email: true });
    
    if (Object.keys(validationErrors).length === 0) {
      submit({ email });
    }
  };
  
  const showError = touched.email && errors.email;
  
  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onBlur={() => handleBlur('email')}
          aria-invalid={showError}
          aria-describedby={showError ? 'email-error' : undefined}
        />
        {showError && (
          <span id="email-error" className="error" role="alert">
            {errors.email}
          </span>
        )}
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}

// Or use form library
import { useForm } from 'react-hook-form';

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  const onSubmit = (data) => submit(data);
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /\S+@\S+\.\S+/,
              message: 'Please enter a valid email',
            },
          })}
          aria-invalid={!!errors.email}
        />
        {errors.email && (
          <span role="alert">{errors.email.message}</span>
        )}
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Validation UX rules:**
- Validate on blur, not on every keystroke
- Show errors inline near the field
- Use clear, helpful error messages
- Connect errors to inputs with aria-describedby
- Focus first error field on submit

**Related:** CONTROLLED-VS-UNCONTROLLED, ARIA-LABELS

---

#### NULL-CHECK: Handle Null/Undefined Safely

**Severity:** Warning

**Problematic code:**
```jsx
// Crashes on undefined
function UserCard({ user }) {
  return (
    <div>
      <h2>{user.name}</h2>  {/* Crashes if user is undefined */}
      <p>{user.address.city}</p>  {/* Crashes if address is undefined */}
    </div>
  );
}

// Falsy check issues
function Badge({ count }) {
  return count && <span>{count}</span>;  // Renders "0" for count=0
}
```

**Improved code:**
```jsx
// Safe property access
function UserCard({ user }) {
  if (!user) return null;
  
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.address?.city ?? 'Unknown city'}</p>
    </div>
  );
}

// TypeScript for compile-time safety
interface User {
  name: string;
  address?: {
    city: string;
  };
}

function UserCard({ user }: { user: User | null }) {
  if (!user) return <EmptyState />;
  
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.address?.city ?? 'Unknown city'}</p>
    </div>
  );
}

// Explicit boolean check
function Badge({ count }) {
  return count > 0 ? <span>{count}</span> : null;
}

// Default props
function UserCard({ user = { name: 'Guest', address: null } }) {
  return (
    <div>
      <h2>{user.name}</h2>
    </div>
  );
}
```

**Safety patterns:**
- Optional chaining: `user?.address?.city`
- Nullish coalescing: `value ?? defaultValue`
- Explicit boolean checks: `count > 0`
- Early returns for null/undefined
- TypeScript for compile-time safety

**Related:** PROP-TYPES, DEFAULT-PROPS

---

### 7. Testing (6 guidelines)

#### TEST-BEHAVIOR: Test Behavior, Not Implementation

**Severity:** Warning

**Problematic code:**
```jsx
// Testing implementation details
it('should update state when button clicked', () => {
  const { result } = renderHook(() => useState(0));
  
  act(() => {
    result.current[1](1);  // Testing internal state
  });
  
  expect(result.current[0]).toBe(1);
});

// Testing component internals
it('should have correct class name', () => {
  render(<Button variant="primary" />);
  expect(screen.getByRole('button')).toHaveClass('btn-primary');
});
```

**Improved code:**
```jsx
// Test user-visible behavior
it('should show incremented count when user clicks', () => {
  render(<Counter />);
  
  const button = screen.getByRole('button', { name: /increment/i });
  const count = screen.getByText(/count:/i);
  
  expect(count).toHaveTextContent('Count: 0');
  
  await userEvent.click(button);
  
  expect(count).toHaveTextContent('Count: 1');
});

// Test what user sees and does
it('should show error when form submitted with invalid email', async () => {
  render(<RegistrationForm />);
  
  const emailInput = screen.getByLabelText(/email/i);
  const submitButton = screen.getByRole('button', { name: /submit/i });
  
  await userEvent.type(emailInput, 'invalid-email');
  await userEvent.click(submitButton);
  
  expect(screen.getByRole('alert')).toHaveTextContent(/valid email/i);
});

// Test accessibility
it('should be keyboard navigable', async () => {
  render(<Dropdown options={['A', 'B', 'C']} />);
  
  const trigger = screen.getByRole('button');
  trigger.focus();
  
  await userEvent.keyboard('{Enter}');
  expect(screen.getByRole('listbox')).toBeVisible();
  
  await userEvent.keyboard('{ArrowDown}');
  expect(screen.getByRole('option', { name: 'A' })).toHaveFocus();
});
```

**Test what matters:**
- User interactions (clicks, typing)
- Visual output (text, visibility)
- Accessibility (roles, labels)
- Error states
- Loading states

**Related:** TEST-QUERIES, MOCK-BOUNDARIES

---

#### TEST-QUERIES: Use Correct Testing Library Queries

**Severity:** Info

**Query priority (best to worst):**
```jsx
// 1. Queries accessible to everyone
screen.getByRole('button', { name: /submit/i })  // Best
screen.getByLabelText(/email/i)
screen.getByPlaceholderText(/search/i)
screen.getByText(/welcome/i)
screen.getByDisplayValue('current value')

// 2. Semantic queries
screen.getByAltText(/profile picture/i)
screen.getByTitle(/tooltip text/i)

// 3. Test IDs (last resort)
screen.getByTestId('submit-button')  // Avoid if possible

// Query variants
// getBy: Throws if not found (use for elements that should exist)
// queryBy: Returns null if not found (use for asserting absence)
// findBy: Async, waits for element (use for elements that appear later)

// Examples
it('shows results after loading', async () => {
  render(<Search />);
  
  // Element appears after async operation
  expect(await screen.findByText(/results/i)).toBeVisible();
});

it('shows no error initially', () => {
  render(<Form />);
  
  // Element should NOT exist
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});

it('shows error after invalid submit', async () => {
  render(<Form />);
  
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));
  
  // Element should exist
  expect(screen.getByRole('alert')).toHaveTextContent(/required/i);
});
```

**Query selection guide:**
- Interactive elements: `getByRole`
- Form inputs: `getByLabelText`
- Text content: `getByText`
- Images: `getByAltText`
- Only use `getByTestId` when nothing else works

**Related:** TEST-BEHAVIOR, ASYNC-TEST

---

#### MOCK-BOUNDARIES: Mock at System Boundaries

**Severity:** Info

**Problematic code:**
```jsx
// Mocking implementation details
jest.mock('./useUserData', () => ({
  useUserData: () => ({ user: mockUser })
}));

// Mocking too granularly
jest.mock('./formatDate');
jest.mock('./validateEmail');
```

**Improved code:**
```jsx
// Mock at system boundaries
// Mock HTTP requests
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/user/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'John' }));
  }),
  
  rest.post('/api/users', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({ id: '123', ...req.body }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('shows user profile', async () => {
  render(<UserProfile userId="123" />);
  
  expect(await screen.findByText('John')).toBeVisible();
});

it('handles server error', async () => {
  server.use(
    rest.get('/api/user/:id', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );
  
  render(<UserProfile userId="123" />);
  
  expect(await screen.findByText(/error/i)).toBeVisible();
});

// Mock browser APIs
beforeEach(() => {
  // Mock localStorage
  Object.defineProperty(window, 'localStorage', {
    value: {
      getItem: jest.fn(),
      setItem: jest.fn(),
      clear: jest.fn(),
    },
  });
  
  // Mock matchMedia
  window.matchMedia = jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
  }));
});
```

**What to mock:**
- HTTP requests (use MSW)
- Browser APIs (localStorage, matchMedia)
- Date/time (jest.useFakeTimers)
- Third-party services

**What NOT to mock:**
- Child components (usually)
- Utility functions
- React hooks

**Related:** TEST-BEHAVIOR, TEST-ASYNC

---

#### TEST-ASYNC: Handle Async Operations in Tests

**Severity:** Warning

**Problematic code:**
```jsx
// Race conditions
it('shows data after fetch', () => {
  render(<DataComponent />);
  
  // Test runs before fetch completes!
  expect(screen.getByText('Data')).toBeVisible();
});

// Not waiting for updates
it('shows confirmation after submit', () => {
  render(<Form />);
  
  userEvent.click(screen.getByRole('button'));
  
  // Assertion runs before state update!
  expect(screen.getByText('Success')).toBeVisible();
});
```

**Improved code:**
```jsx
// Use findBy for async elements
it('shows data after fetch', async () => {
  render(<DataComponent />);
  
  // Waits up to 1000ms by default
  expect(await screen.findByText('Data')).toBeVisible();
});

// Use waitFor for state updates
it('shows confirmation after submit', async () => {
  render(<Form />);
  
  await userEvent.click(screen.getByRole('button'));
  
  await waitFor(() => {
    expect(screen.getByText('Success')).toBeVisible();
  });
});

// Use act for direct state updates
it('updates count', async () => {
  const { result } = renderHook(() => useCounter());
  
  await act(async () => {
    await result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});

// Fake timers for debounce/delay
it('searches after debounce', async () => {
  jest.useFakeTimers();
  
  render(<SearchInput />);
  
  await userEvent.type(screen.getByRole('textbox'), 'test');
  
  // Advance timers
  act(() => {
    jest.advanceTimersByTime(500);
  });
  
  expect(await screen.findByText('Results for: test')).toBeVisible();
  
  jest.useRealTimers();
});
```

**Async testing patterns:**
- `findBy*`: Wait for element to appear
- `waitFor`: Wait for assertion to pass
- `waitForElementToBeRemoved`: Wait for element to disappear
- `act`: Wrap state updates
- Fake timers: Control time-based behavior

**Related:** MOCK-BOUNDARIES, USE-EFFECT-CLEANUP

---

#### TEST-HOOK: Test Custom Hooks

**Severity:** Info

**Testing custom hooks:**
```jsx
// Custom hook
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  
  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);
  
  return { count, increment, decrement, reset };
}

// Test with renderHook
import { renderHook, act } from '@testing-library/react';

describe('useCounter', () => {
  it('starts with initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });
  
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
  
  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5));
    
    act(() => {
      result.current.increment();
      result.current.increment();
    });
    
    expect(result.current.count).toBe(7);
    
    act(() => {
      result.current.reset();
    });
    
    expect(result.current.count).toBe(5);
  });
  
  it('handles prop changes', () => {
    const { result, rerender } = renderHook(
      ({ initial }) => useCounter(initial),
      { initialProps: { initial: 0 } }
    );
    
    expect(result.current.count).toBe(0);
    
    rerender({ initial: 10 });
    
    // Initial value changed, but count keeps current value
    act(() => {
      result.current.reset();
    });
    
    expect(result.current.count).toBe(10);
  });
});

// Testing hooks with context
const wrapper = ({ children }) => (
  <ThemeProvider value="dark">
    {children}
  </ThemeProvider>
);

it('uses theme from context', () => {
  const { result } = renderHook(() => useTheme(), { wrapper });
  expect(result.current.theme).toBe('dark');
});
```

**Related:** CUSTOM-HOOKS, TEST-ASYNC

---

#### TEST-ACCESSIBILITY: Test Accessibility

**Severity:** Warning

**Accessibility testing:**
```jsx
// Automated accessibility testing
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<Form />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

// Test keyboard navigation
it('is keyboard accessible', async () => {
  render(<Modal isOpen onClose={jest.fn()}>Content</Modal>);
  
  // Focus should be trapped in modal
  const closeButton = screen.getByRole('button', { name: /close/i });
  closeButton.focus();
  
  await userEvent.tab();
  expect(document.activeElement).toBe(/* next focusable element */);
  
  // Escape should close
  await userEvent.keyboard('{Escape}');
  expect(onClose).toHaveBeenCalled();
});

// Test screen reader text
it('has accessible labels', () => {
  render(<IconButton icon={<SearchIcon />} onClick={() => {}} />);
  
  expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
});

// Test focus management
it('returns focus after modal closes', async () => {
  const openButton = document.createElement('button');
  document.body.appendChild(openButton);
  openButton.focus();
  
  const { rerender } = render(<Modal isOpen={true} onClose={() => {}} />);
  
  // Modal should have focus
  expect(document.activeElement).not.toBe(openButton);
  
  rerender(<Modal isOpen={false} onClose={() => {}} />);
  
  // Focus should return to trigger
  expect(document.activeElement).toBe(openButton);
});
```

**What to test:**
- No axe violations
- Keyboard navigation works
- Focus management
- ARIA labels present
- Error announcements

**Related:** KEYBOARD-NAV, ARIA-LABELS

---

## React Wisdom

> **"Don't optimize prematurely"** - React Team
>
> **"Lift state up only when you need to"** - React Docs
>
> **"Profile before you memoize"** - Performance Principle

### Common Mistakes to Avoid

1. **State misuse** - Syncing props to state, derived state, too much state
2. **Effect abuse** - Effects for derived values, missing cleanup, wrong deps
3. **Premature optimization** - Memoizing everything, wrong abstractions
4. **Ignoring accessibility** - No keyboard nav, missing labels
5. **Poor error handling** - No error boundaries, unhandled promises

### Best Practices Summary

1. Keep components small and focused
2. Lift state only when necessary
3. Derive values during render when possible
4. Use effects only for synchronization with external systems
5. Memoize only when profiling shows benefit
6. Test behavior, not implementation
7. Prioritize accessibility from the start
8. Handle errors gracefully

---

## Modern React 18 & Framework Guidance

### Server/Client Component Boundaries

- Default to **Server Components** for data fetching and heavy computation in Next.js/Remix; mark interactive pieces with `"use client"`.
- Never import browser-only APIs (window, document, Zustand stores) into server components; push them into client components via props.

### Streaming & Suspense

- Use Suspense boundaries per layout segment to stream data incrementally:

```jsx
export default function Page() {
  return (
    <>
      <Suspense fallback={<StatsSkeleton />}>
        <StatsPanel />
      </Suspense>
      <Suspense fallback={<OrdersSkeleton />}>
        <OrdersTable />
      </Suspense>
    </>
  );
}
```

- For long-running actions, pair Suspense with `useTransition` or route segment loading UI.

### Server Actions / Mutations

- Encapsulate mutations in server actions (Next.js) or Remix actions to keep secrets on the server.
- Validate inputs with Zod/pydantic before touching the database.

### Next.js / Remix Deployment Notes

- Document per-route runtime (`edge`, `nodejs`), caching strategies (`revalidate`, `cache: 'no-store'`), and data fetching mode (SSR, ISR, SSG).
- Use route groups/segments wisely; nest layouts for deduped fetches.
- For Remix loaders/actions, share validation utilities to avoid divergence between client/server.

### React Native & Web Hybrid Considerations

- Extract platform-specific components (`Platform.select`) and avoid DOM-specific APIs in shared hooks.

---

## Quick Reference

### By Category

**Component Design:**
SINGLE-RESPONSIBILITY, COMPOSITION, PROP-TYPES, LIFTING-STATE, STATE-COLOCATION, DERIVED-STATE

**Hooks:**
USE-EFFECT-DEPS, USE-EFFECT-CLEANUP, CUSTOM-HOOKS, HOOK-RULES, STALE-CLOSURE, USE-REF, USE-REDUCER

**Performance:**
MEMO-COMPONENT, KEY-PROP, LIST-RENDER, LAZY-LOADING, TRANSITIONS, AVOID-INLINE-OBJECTS

**Patterns:**
COMPOUND-COMPONENTS, RENDER-PROPS, FORWARD-REF, PORTALS, CONTEXT-MODULE

**Accessibility:**
SEMANTIC-HTML, ARIA-LABELS, KEYBOARD-NAV, FOCUS-MANAGEMENT, SCREEN-READER

**Error Handling:**
ERROR-BOUNDARY, ASYNC-ERROR, LOADING-STATE, FORM-VALIDATION, NULL-CHECK

**Testing:**
TEST-BEHAVIOR, TEST-QUERIES, MOCK-BOUNDARIES, TEST-ASYNC

---

**Remember: React is about building UIs that are predictable, composable, and maintainable. Start simple, measure, then optimize.**
