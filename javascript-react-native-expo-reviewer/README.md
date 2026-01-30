# React Native Expo Reviewer Skill

A Claude Code skill that reviews React Native code developed with Expo for best practices, performance, and common pitfalls. **Comprehensive mobile analysis** - covers Expo configuration, components, performance, navigation, state management, platform handling, error handling, push notifications, and accessibility.

## What This Skill Does

This skill transforms Claude into a React Native and Expo expert who:

- **Identifies mobile anti-patterns** - ScrollView for long lists, missing memoization, JS thread blocking
- **Suggests Expo best practices** - Configuration, plugins, EAS Build, OTA updates
- **Optimizes performance** - Native driver animations, gesture handling, bundle size
- **Ensures proper navigation** - React Navigation structure, deep linking, type safety
- **Handles platform differences** - iOS/Android-specific code, safe areas, permissions
- **Improves accessibility** - Screen reader support, touch targets, font scaling
- **Categorizes by severity** - CRITICAL, HIGH, MEDIUM, LOW

## Philosophy

> **"Mobile is not just small web"** - Mobile has unique constraints: battery, memory, network, touch

> **"60fps or nothing"** - Users notice jank; keep the JS thread free

> **"Test on real devices"** - Simulators hide real-world performance issues

This skill emphasizes **mobile-first thinking** - optimizing for touch interactions, battery life, offline capability, and the constraints of mobile networks and hardware.

## Installation

### Personal Installation (Available in All Projects)

```bash
# Linux/Mac
cp -r javascript-react-native-expo-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "javascript-react-native-expo-reviewer" "$env:USERPROFILE\.claude\skills\"
```

### Project Installation (For Teams)

```bash
cp -r javascript-react-native-expo-reviewer /path/to/your-project/.claude/skills/
git add .claude/skills/javascript-react-native-expo-reviewer
git commit -m "Add React Native Expo Reviewer skill"
```

## How to Use

Simply ask Claude to review your React Native or Expo code:

```
"Review this React Native screen"
"Check my Expo configuration"
"Is this FlatList optimized?"
"Review my navigation setup"
"Check for performance issues in this component"
"Is this accessible for screen readers?"
"Review my push notification implementation"
```

## What You'll Get

A comprehensive React Native/Expo review with:

- **Severity Classification** - CRITICAL, HIGH, MEDIUM, LOW
- **Problematic Code** - Shows the issue
- **Improved Code** - Shows the fix with mobile-specific optimizations
- **Explanation** - Why it matters for mobile
- **Mnemonic IDs** - Easy reference (e.g., RN-FLATLIST, EXPO-CONFIG)

### Example Review

````markdown
## React Native Expo Review: ProductListScreen

### CRITICAL Issues

#### RN-FLATLIST: ScrollView Used for Long List

**Problematic code:**
```jsx
<ScrollView>
  {products.map(product => (
    <ProductCard key={product.id} product={product} />
  ))}
</ScrollView>
```

**Improved code:**
```jsx
const renderItem = useCallback(({ item }) => (
  <ProductCard product={item} />
), []);

<FlatList
  data={products}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  removeClippedSubviews={true}
/>
```

**Why:** ScrollView renders all items at once. With 500+ products, this causes multi-second load times and potential out-of-memory crashes on low-end devices. FlatList virtualizes rendering - only visible items exist in memory.
````

## The 38 React Native Expo Guidelines

### Expo Configuration (5 guidelines)

- **EXPO-CONFIG** - Use app.config.js for dynamic configuration
- **EXPO-SECRETS** - Never hardcode sensitive values
- **EXPO-PLUGINS** - Configure native modules correctly
- **EAS-BUILD** - Structure EAS build profiles properly
- **EAS-UPDATE** - Configure over-the-air updates properly

### React Native Components (6 guidelines)

- **RN-FLATLIST** - Use FlatList for long lists
- **RN-SECTIONLIST** - Use SectionList for grouped data
- **RN-IMAGE** - Optimize image loading and caching
- **RN-ASSETS** - Manage assets properly
- **RN-PRESSABLE** - Use Pressable for touch interactions
- **RN-STYLES** - Use StyleSheet.create for styles

### Performance (6 guidelines)

- **RN-MEMO** - Memoize components and callbacks
- **RN-JANK** - Avoid JavaScript thread blocking
- **RN-ANIMATION** - Use native driver for animations
- **RN-GESTURE** - Use React Native Gesture Handler
- **RN-BUNDLE** - Reduce bundle size
- **RN-HERMES** - Enable Hermes engine

### Navigation (5 guidelines)

- **NAV-STACK** - Structure navigation correctly
- **NAV-TYPES** - Type navigation with TypeScript
- **NAV-DEEPLINK** - Configure deep linking properly
- **NAV-PARAMS** - Pass navigation params correctly
- **NAV-HEADER** - Customize headers correctly

### Platform-Specific (4 guidelines)

- **RN-PLATFORM** - Handle platform differences
- **RN-SAFEAREA** - Handle safe areas correctly
- **RN-PERMISSIONS** - Request permissions properly
- **RN-STATUSBAR** - Configure status bar correctly

### State Management (4 guidelines)

- **STATE-CONTEXT** - Use Context for global state
- **STATE-PERSIST** - Persist state correctly
- **STATE-QUERY** - Use React Query for server state
- **STATE-ZUSTAND** - Consider Zustand for complex state

### Error Handling (3 guidelines)

- **ERROR-BOUNDARY** - Use error boundaries
- **ERROR-CRASH** - Implement crash reporting
- **ERROR-NETWORK** - Handle network errors gracefully

### Push Notifications (2 guidelines)

- **NOTIF-SETUP** - Configure push notifications correctly
- **NOTIF-HANDLE** - Handle notification actions

### Accessibility (3 guidelines)

- **RN-ACCESSIBILITY** - Make components accessible
- **RN-TOUCH** - Ensure adequate touch targets
- **RN-FONT-SCALE** - Support dynamic font sizes

## Common Patterns This Skill Teaches

### Do This

```jsx
// FlatList with optimizations
<FlatList
  data={data}
  renderItem={renderItem}
  keyExtractor={(item) => item.id}
  getItemLayout={(data, index) => ({
    length: 80,
    offset: 80 * index,
    index,
  })}
  removeClippedSubviews={true}
/>

// Native driver animations
Animated.timing(opacity, {
  toValue: 1,
  duration: 300,
  useNativeDriver: true,
}).start();

// Environment-aware config
export default ({ config }) => ({
  ...config,
  extra: {
    apiUrl: process.env.API_URL,
  },
});

// Type-safe navigation
navigation.navigate('ProductDetail', { productId: '123' });

// Accessible components
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Add to cart"
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
>
```

### Not This

```jsx
// ScrollView for long lists (memory explosion)
<ScrollView>
  {items.map(item => <Item key={item.id} />)}
</ScrollView>

// JS-driven animations (jank)
Animated.timing(opacity, {
  toValue: 1,
  useNativeDriver: false,  // Runs on JS thread!
}).start();

// Hardcoded secrets (security risk)
const API_KEY = 'sk-live-abc123';

// Untyped navigation (runtime errors)
navigation.navigate('ProductDetial', { id: 123 });  // Typo!

// Missing accessibility
<TouchableOpacity onPress={onPress}>
  <Image source={icon} />
</TouchableOpacity>
```

## Benefits

- Find mobile-specific anti-patterns
- Optimize for 60fps performance
- Proper Expo SDK and EAS usage
- Type-safe navigation setup
- Platform-specific handling (iOS/Android)
- Accessibility compliance
- Push notification best practices
- Error handling and crash reporting
- Severity-based prioritization

## What Gets Checked

### Configuration

- Environment-based app.config.js
- Secure secret management
- Plugin configuration
- EAS Build profiles
- OTA update setup

### Performance

- List virtualization (FlatList/SectionList)
- Memoization (memo, useCallback, useMemo)
- Native driver animations
- Gesture handler usage
- Bundle size optimization
- Hermes engine

### Navigation

- Navigator structure and nesting
- TypeScript types for params
- Deep linking configuration
- Parameter serialization
- Header customization

### Platform Handling

- Platform.select usage
- Safe area insets
- Permission requests
- Status bar configuration

### State

- Context organization
- Secure vs async storage
- Server state (React Query)
- State persistence

### Errors

- Error boundaries
- Crash reporting integration
- Network error handling

### Notifications

- Permission handling
- Token registration
- Notification actions
- Deep link from notifications

### Accessibility

- Labels and roles
- Touch target sizes
- Font scaling support

## Supported Technologies

- **Expo SDK:** 48+
- **React Native:** 0.70+
- **React Navigation:** 6.x
- **TypeScript:** Full support
- **State:** Context, Zustand, React Query
- **Animation:** Reanimated 2/3, Animated API
- **Testing:** Jest, React Native Testing Library

## Sources and Attribution

All guidelines are based on:

- **React Native Documentation** - reactnative.dev
- **Expo Documentation** - docs.expo.dev
- **React Navigation Documentation** - reactnavigation.org
- **Apple Human Interface Guidelines** - Touch targets, accessibility
- **Material Design Guidelines** - Android patterns
- **Community Best Practices** - Performance optimization

See [SOURCES.md](./SOURCES.md) for detailed attribution.

## When to Use This Skill

**Use when:**

- Reviewing React Native components and screens
- Setting up a new Expo project
- Optimizing app performance
- Implementing navigation
- Adding push notifications
- Ensuring accessibility compliance
- Debugging platform-specific issues

**Not ideal for:**

- Web-only React applications (use react-reviewer instead)
- Native iOS/Android development (Swift/Kotlin)
- Backend/API development

## Tips for Best Results

1. **Provide context**: "This is the main product list with 1000+ items"
2. **Share related files**: Include navigation setup, context providers
3. **Mention issues**: "Users report the app crashes on Android"
4. **Ask specific questions**: "Is this FlatList optimized?" or "Is this accessible?"

## License

This skill is provided as-is for use with Claude Code. Based on official React Native, Expo, and React Navigation documentation.

---

**React Native is about building truly native apps with JavaScript - respect the platform.**
