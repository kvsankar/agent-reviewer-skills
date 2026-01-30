# Sources and Attribution

This React Native Expo Reviewer skill is based on official documentation, community best practices, and authoritative sources from the React Native and Expo ecosystems.

## Primary Sources

### 1. React Native Official Documentation

**Source:** Meta (Facebook)
**URL:** https://reactnative.dev/
**Relevance:** Core React Native concepts, components, APIs, performance

**Key resources:**

- **Core Components** - https://reactnative.dev/docs/components-and-apis
- **Performance** - https://reactnative.dev/docs/performance
- **FlatList** - https://reactnative.dev/docs/flatlist
- **Animated API** - https://reactnative.dev/docs/animated
- **Platform Module** - https://reactnative.dev/docs/platform
- **Accessibility** - https://reactnative.dev/docs/accessibility

**Guidelines influenced:**

- RN-FLATLIST, RN-SECTIONLIST - List virtualization
- RN-ANIMATION - Animated API, native driver
- RN-PLATFORM - Platform-specific code
- RN-ACCESSIBILITY - Accessibility properties
- RN-STYLES - StyleSheet.create
- RN-PRESSABLE - Pressable component

---

### 2. Expo Documentation

**Source:** Expo Team
**URL:** https://docs.expo.dev/
**Relevance:** Expo SDK, configuration, build and deployment

**Key resources:**

- **Configuration** - https://docs.expo.dev/workflow/configuration/
- **app.config.js** - https://docs.expo.dev/workflow/configuration/#dynamic-configuration
- **EAS Build** - https://docs.expo.dev/build/introduction/
- **EAS Update** - https://docs.expo.dev/eas-update/introduction/
- **Expo Modules** - https://docs.expo.dev/modules/overview/
- **Push Notifications** - https://docs.expo.dev/push-notifications/overview/

**Guidelines influenced:**

- EXPO-CONFIG - Dynamic configuration
- EXPO-SECRETS - Secret management
- EXPO-PLUGINS - Config plugins
- EAS-BUILD - Build profiles
- EAS-UPDATE - Over-the-air updates
- NOTIF-SETUP, NOTIF-HANDLE - Push notifications

---

### 3. React Navigation Documentation

**Source:** React Navigation Team
**URL:** https://reactnavigation.org/
**Relevance:** Navigation patterns, deep linking, TypeScript

**Key resources:**

- **Getting Started** - https://reactnavigation.org/docs/getting-started
- **Stack Navigator** - https://reactnavigation.org/docs/stack-navigator
- **Tab Navigator** - https://reactnavigation.org/docs/bottom-tab-navigator
- **Deep Linking** - https://reactnavigation.org/docs/deep-linking
- **TypeScript** - https://reactnavigation.org/docs/typescript
- **Navigation Lifecycle** - https://reactnavigation.org/docs/navigation-lifecycle

**Guidelines influenced:**

- NAV-STACK - Navigator structure
- NAV-TYPES - TypeScript navigation types
- NAV-DEEPLINK - Deep linking configuration
- NAV-PARAMS - Parameter passing
- NAV-HEADER - Header customization

---

### 4. React Native Reanimated

**Source:** Software Mansion
**URL:** https://docs.swmansion.com/react-native-reanimated/
**Relevance:** High-performance animations

**Key resources:**

- **Fundamentals** - https://docs.swmansion.com/react-native-reanimated/docs/fundamentals/getting-started
- **Shared Values** - https://docs.swmansion.com/react-native-reanimated/docs/fundamentals/shared-values
- **Animations** - https://docs.swmansion.com/react-native-reanimated/docs/fundamentals/animations
- **Layout Animations** - https://docs.swmansion.com/react-native-reanimated/docs/layout-animations/entering-exiting-animations

**Guidelines influenced:**

- RN-ANIMATION - Native driver animations
- RN-GESTURE - Gesture integration with animations

---

### 5. React Native Gesture Handler

**Source:** Software Mansion
**URL:** https://docs.swmansion.com/react-native-gesture-handler/
**Relevance:** Native gesture handling

**Key resources:**

- **Gesture Handlers** - https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/about-handlers
- **Gesture Composition** - https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/gesture-composition
- **Manual Gestures** - https://docs.swmansion.com/react-native-gesture-handler/docs/gestures/manual-gestures

**Guidelines influenced:**

- RN-GESTURE - Gesture Handler usage

---

### 6. Expo Image

**Source:** Expo Team
**URL:** https://docs.expo.dev/versions/latest/sdk/image/
**Relevance:** High-performance image component

**Guidelines influenced:**

- RN-IMAGE - Image optimization and caching

---

### 7. Safe Area Context

**Source:** React Native Community
**URL:** https://github.com/th3rdwave/react-native-safe-area-context
**Relevance:** Safe area handling for notches and home indicators

**Guidelines influenced:**

- RN-SAFEAREA - Safe area handling

---

### 8. React Query (TanStack Query)

**Source:** TanStack
**URL:** https://tanstack.com/query/latest
**Relevance:** Server state management

**Key resources:**

- **React Query Documentation** - https://tanstack.com/query/latest/docs/react/overview
- **Queries** - https://tanstack.com/query/latest/docs/react/guides/queries
- **Mutations** - https://tanstack.com/query/latest/docs/react/guides/mutations
- **Caching** - https://tanstack.com/query/latest/docs/react/guides/caching

**Guidelines influenced:**

- STATE-QUERY - React Query for server state

---

### 9. Zustand

**Source:** Poimandres
**URL:** https://github.com/pmndrs/zustand
**Relevance:** Lightweight state management

**Key resources:**

- **Documentation** - https://docs.pmnd.rs/zustand/getting-started/introduction
- **Persist Middleware** - https://docs.pmnd.rs/zustand/integrations/persisting-store-data

**Guidelines influenced:**

- STATE-ZUSTAND - Zustand for complex state
- STATE-PERSIST - State persistence

---

### 10. Sentry React Native

**Source:** Sentry
**URL:** https://docs.sentry.io/platforms/react-native/
**Relevance:** Error tracking and crash reporting

**Guidelines influenced:**

- ERROR-CRASH - Crash reporting implementation

---

### 11. Apple Human Interface Guidelines

**Source:** Apple
**URL:** https://developer.apple.com/design/human-interface-guidelines/
**Relevance:** iOS design patterns, accessibility, touch targets

**Key sections:**

- **Touch Targets** - Minimum 44x44 points
- **Accessibility** - VoiceOver, Dynamic Type
- **Safe Areas** - Notch, home indicator handling

**Guidelines influenced:**

- RN-TOUCH - Touch target sizes
- RN-ACCESSIBILITY - iOS accessibility
- RN-FONT-SCALE - Dynamic Type support
- RN-SAFEAREA - Safe area handling

---

### 12. Material Design Guidelines

**Source:** Google
**URL:** https://material.io/design
**Relevance:** Android design patterns, accessibility

**Key sections:**

- **Touch Targets** - Minimum 48x48 dp
- **Accessibility** - TalkBack, font scaling
- **Components** - Android-specific patterns

**Guidelines influenced:**

- RN-TOUCH - Android touch targets
- RN-ACCESSIBILITY - Android accessibility
- RN-PLATFORM - Android-specific patterns

---

### 13. Web Content Accessibility Guidelines (WCAG)

**Source:** W3C
**URL:** https://www.w3.org/WAI/standards-guidelines/wcag/
**Relevance:** Accessibility standards applicable to mobile

**Guidelines influenced:**

- RN-ACCESSIBILITY - Accessibility labels, roles
- RN-TOUCH - Touch target sizes
- RN-FONT-SCALE - Text resizing

---

### 14. Hermes Engine

**Source:** Meta (Facebook)
**URL:** https://hermesengine.dev/
**Relevance:** JavaScript engine for React Native

**Guidelines influenced:**

- RN-HERMES - Hermes engine benefits

---

### 15. Expo SecureStore

**Source:** Expo Team
**URL:** https://docs.expo.dev/versions/latest/sdk/securestore/
**Relevance:** Secure storage for sensitive data

**Guidelines influenced:**

- STATE-PERSIST - Secure vs async storage
- EXPO-SECRETS - Secret storage

---

### 16. NetInfo

**Source:** React Native Community
**URL:** https://github.com/react-native-netinfo/react-native-netinfo
**Relevance:** Network connectivity detection

**Guidelines influenced:**

- ERROR-NETWORK - Network status handling

---

### 17. React Error Boundary

**Source:** Brian Vaughn
**URL:** https://github.com/bvaughn/react-error-boundary
**Relevance:** Error boundary component for React

**Guidelines influenced:**

- ERROR-BOUNDARY - Error boundary implementation

---

## Community Resources

### Performance Optimization

- **Callstack Blog** - https://blog.callstack.io/ - React Native performance articles
- **Software Mansion Blog** - https://blog.swmansion.com/ - Reanimated, Gesture Handler insights
- **Expo Blog** - https://blog.expo.dev/ - Expo best practices

### Books and Courses

- **React Native in Action** by Nader Dabit
- **Fullstack React Native** by Devin Abbott
- **Expo documentation tutorials** - https://docs.expo.dev/tutorial/introduction/

### Tools

- **Flipper** - https://fbflipper.com/ - React Native debugging
- **React DevTools** - Component inspection
- **Expo DevTools** - Development and debugging

---

## Research Methodology

The guidelines in this skill were developed through:

1. **Documentation Review**
   - React Native official documentation
   - Expo SDK documentation
   - React Navigation documentation
   - Third-party library documentation

2. **Performance Testing**
   - FlatList vs ScrollView benchmarks
   - Native driver vs JS-driven animation comparisons
   - Bundle size analysis

3. **Platform Guidelines**
   - Apple Human Interface Guidelines
   - Material Design Guidelines
   - WCAG accessibility standards

4. **Community Best Practices**
   - Expo community forums
   - React Native GitHub issues and discussions
   - Conference talks and blog posts

5. **Real-World Validation**
   - Production app patterns
   - App Store and Play Store requirements
   - User experience research

---

## Additional Resources

### Documentation

- React Native - https://reactnative.dev/
- Expo - https://docs.expo.dev/
- React Navigation - https://reactnavigation.org/

### Community

- Expo Forums - https://forums.expo.dev/
- React Native GitHub - https://github.com/facebook/react-native
- Discord communities

### Tools

- Expo CLI - https://docs.expo.dev/workflow/expo-cli/
- EAS CLI - https://docs.expo.dev/build/setup/
- React Native Debugger - https://github.com/jhen0409/react-native-debugger

---

## Attribution Note

This skill synthesizes knowledge from official documentation and respected community sources. All recommendations align with:

- React Native team's official guidance
- Expo team's best practices
- React Navigation patterns
- Platform-specific guidelines (iOS/Android)
- Accessibility standards (WCAG)

The examples are original implementations demonstrating principles from these sources, adapted for practical use with Claude Code.

## Version History

- **v1.0** (2026-01-31) - Initial release with 38 React Native Expo guidelines
  - Expo Configuration (5 guidelines)
  - React Native Components (6 guidelines)
  - Performance (6 guidelines)
  - Navigation (5 guidelines)
  - Platform-Specific (4 guidelines)
  - State Management (4 guidelines)
  - Error Handling (3 guidelines)
  - Push Notifications (2 guidelines)
  - Accessibility (3 guidelines)

---

**All sources are publicly available and represent industry-standard best practices for React Native and Expo development.**
