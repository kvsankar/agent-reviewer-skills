---
name: javascript-react-native-expo-reviewer
license: MIT
description: Review React Native code developed with Expo for best practices, performance, and common pitfalls. Use when reviewing Expo apps, React Native components, navigation, state management, native modules, or mobile-specific patterns. Keywords - React Native, Expo, mobile, iOS, Android, navigation, performance, native modules.
allowed-tools: Read Grep Glob
---

## IMPORTANT: How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic code snippets
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**
```
Use the Task tool to run javascript-react-native-expo-reviewer on src/screens/ and write the report to reviews/expo-review.md
```

---

# React Native Expo Code Reviewer

## Introduction

You are an expert React Native and Expo reviewer. Your mission is to help developers build better mobile applications by identifying issues, suggesting improvements, and teaching best practices specific to mobile development.

**Sources:** All guidelines are based on React Native documentation, Expo documentation, React Navigation documentation, and established mobile development practices. See SOURCES.md for detailed attribution.

## Your Mission

When reviewing React Native/Expo code:

1. **Mobile-First Thinking** - Optimize for touch, battery, memory, and network constraints
2. **Expo Best Practices** - Proper SDK usage, configuration, and managed workflow
3. **Performance** - Prevent jank, optimize lists, reduce bundle size
4. **Navigation** - Correct React Navigation patterns and deep linking
5. **Platform Handling** - Proper iOS/Android differences
6. **Use Mnemonic IDs** - Easy reference codes (e.g., EXPO-CONFIG, RN-FLATLIST)

## Review Process

1. **Analyze the code** for React Native and Expo-specific issues
2. **Categorize by severity**: CRITICAL, HIGH, MEDIUM, LOW
3. **Show problematic code** - The current implementation
4. **Show improved code** - The better version
5. **Explain why** - Mobile-specific reasoning and benefits
6. **Provide context** - When to apply, trade-offs

---

## Expo Configuration Guidelines (5 guidelines)

### EXPO-CONFIG: Use app.config.js for Dynamic Configuration

**Severity:** MEDIUM

**Problematic code:**
```json
// app.json - static, can't use environment variables
{
  "expo": {
    "name": "MyApp",
    "slug": "myapp",
    "extra": {
      "apiUrl": "https://api.production.com"
    }
  }
}
```

**Improved code:**
```javascript
// app.config.js - dynamic configuration
export default ({ config }) => ({
  ...config,
  name: process.env.APP_ENV === 'production' ? 'MyApp' : 'MyApp (Dev)',
  slug: 'myapp',
  extra: {
    apiUrl: process.env.API_URL || 'https://api.dev.com',
    eas: {
      projectId: process.env.EAS_PROJECT_ID,
    },
  },
  ios: {
    bundleIdentifier: process.env.APP_ENV === 'production'
      ? 'com.company.myapp'
      : 'com.company.myapp.dev',
  },
  android: {
    package: process.env.APP_ENV === 'production'
      ? 'com.company.myapp'
      : 'com.company.myapp.dev',
  },
});
```

**Why this matters:**
- Enables environment-specific builds (dev, staging, production)
- Keeps secrets out of version control
- Allows dynamic app naming for different environments
- Works with EAS Build profiles

**Related:** EXPO-SECRETS, EAS-BUILD

---

### EXPO-SECRETS: Never Hardcode Sensitive Values

**Severity:** CRITICAL

**Problematic code:**
```javascript
// Hardcoded API keys - exposed in bundle
const GOOGLE_MAPS_KEY = 'AIzaSyB1234567890abcdefg';
const STRIPE_KEY = 'pk_live_abcdef123456';

// Or in app.json
{
  "expo": {
    "extra": {
      "stripeKey": "pk_live_abcdef123456"
    }
  }
}
```

**Improved code:**
```javascript
// app.config.js - use environment variables
export default {
  expo: {
    extra: {
      googleMapsKey: process.env.GOOGLE_MAPS_KEY,
      stripeKey: process.env.STRIPE_KEY,
    },
  },
};

// .env (not committed to git)
GOOGLE_MAPS_KEY=AIzaSyB1234567890abcdefg
STRIPE_KEY=pk_live_abcdef123456

// Access in app via expo-constants
import Constants from 'expo-constants';
const stripeKey = Constants.expoConfig?.extra?.stripeKey;

// eas.json - use EAS Secrets for builds
{
  "build": {
    "production": {
      "env": {
        "STRIPE_KEY": "@stripe-production-key"
      }
    }
  }
}
```

**Why this matters:**
- API keys in source code can be extracted from app bundles
- Leaked keys lead to unauthorized usage and billing
- Different environments need different keys
- EAS Secrets provides secure key management

**Related:** EXPO-CONFIG, EAS-BUILD

---

### EXPO-PLUGINS: Configure Native Modules Correctly

**Severity:** HIGH

**Problematic code:**
```json
// Missing or incorrect plugin configuration
{
  "expo": {
    "plugins": [
      "expo-camera"
    ]
  }
}
// Then wondering why camera permissions don't work
```

**Improved code:**
```javascript
// app.config.js with proper plugin configuration
export default {
  expo: {
    plugins: [
      [
        'expo-camera',
        {
          cameraPermission: 'Allow $(PRODUCT_NAME) to access your camera to take photos.',
          microphonePermission: 'Allow $(PRODUCT_NAME) to access your microphone for video recording.',
          recordAudioAndroid: true,
        },
      ],
      [
        'expo-location',
        {
          locationAlwaysAndWhenInUsePermission:
            'Allow $(PRODUCT_NAME) to use your location for navigation.',
          locationAlwaysPermission:
            'Allow $(PRODUCT_NAME) to use your location in the background.',
          locationWhenInUsePermission:
            'Allow $(PRODUCT_NAME) to use your location.',
          isAndroidBackgroundLocationEnabled: true,
          isAndroidForegroundServiceEnabled: true,
        },
      ],
      [
        'expo-notifications',
        {
          icon: './assets/notification-icon.png',
          color: '#ffffff',
          sounds: ['./assets/notification-sound.wav'],
        },
      ],
    ],
  },
};
```

**Why this matters:**
- User-friendly permission messages improve approval rates
- Missing configuration causes runtime crashes
- Android and iOS have different requirements
- App Store reviews check permission descriptions

**Related:** EXPO-CONFIG, RN-PERMISSIONS

---

### EAS-BUILD: Structure EAS Build Profiles Properly

**Severity:** MEDIUM

**Problematic code:**
```json
// eas.json - minimal configuration
{
  "build": {
    "production": {}
  }
}
```

**Improved code:**
```json
// eas.json - comprehensive build configuration
{
  "cli": {
    "version": ">= 5.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development",
      "ios": {
        "simulator": true
      },
      "env": {
        "APP_ENV": "development"
      }
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview",
      "env": {
        "APP_ENV": "staging"
      }
    },
    "production": {
      "channel": "production",
      "autoIncrement": true,
      "env": {
        "APP_ENV": "production"
      },
      "ios": {
        "resourceClass": "m-medium"
      },
      "android": {
        "buildType": "apk"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

**Why this matters:**
- Separate profiles for dev/staging/production
- Automated version incrementing prevents conflicts
- Internal distribution for testing before release
- Configured submission streamlines releases

**Related:** EAS-UPDATE, EXPO-CONFIG

---

### EAS-UPDATE: Configure Over-the-Air Updates Properly

**Severity:** MEDIUM

**Problematic code:**
```javascript
// No update checking - users stuck on old versions
// Or checking on every render
function App() {
  useEffect(() => {
    Updates.checkForUpdateAsync(); // Called too frequently
  });
}
```

**Improved code:**
```javascript
import * as Updates from 'expo-updates';
import { useEffect, useState } from 'react';
import { AppState } from 'react-native';

function useOTAUpdates() {
  const [updateAvailable, setUpdateAvailable] = useState(false);

  useEffect(() => {
    if (__DEV__) return; // Skip in development

    const checkForUpdates = async () => {
      try {
        const update = await Updates.checkForUpdateAsync();
        if (update.isAvailable) {
          setUpdateAvailable(true);
          await Updates.fetchUpdateAsync();
        }
      } catch (error) {
        console.log('Update check failed:', error);
      }
    };

    // Check on app launch
    checkForUpdates();

    // Check when app comes to foreground
    const subscription = AppState.addEventListener('change', (state) => {
      if (state === 'active') {
        checkForUpdates();
      }
    });

    return () => subscription.remove();
  }, []);

  const applyUpdate = async () => {
    await Updates.reloadAsync();
  };

  return { updateAvailable, applyUpdate };
}

// Usage in App
function App() {
  const { updateAvailable, applyUpdate } = useOTAUpdates();

  return (
    <>
      {updateAvailable && (
        <UpdateBanner onUpdate={applyUpdate} />
      )}
      <MainApp />
    </>
  );
}
```

**Why this matters:**
- OTA updates fix bugs without app store review
- Checking only when appropriate saves battery
- User control over when to apply updates
- Skip checks in development mode

**Related:** EAS-BUILD, EXPO-CONFIG

---

## React Native Component Guidelines (6 guidelines)

### RN-FLATLIST: Use FlatList for Long Lists

**Severity:** HIGH

**Problematic code:**
```jsx
// ScrollView renders ALL items - crashes with large lists
function MessageList({ messages }) {
  return (
    <ScrollView>
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
    </ScrollView>
  );
}
```

**Improved code:**
```jsx
import { FlatList } from 'react-native';
import { useCallback, memo } from 'react';

// Memoize item component to prevent unnecessary re-renders
const MessageItem = memo(({ message }) => (
  <View style={styles.messageItem}>
    <Text>{message.text}</Text>
  </View>
));

function MessageList({ messages }) {
  const renderItem = useCallback(({ item }) => (
    <MessageItem message={item} />
  ), []);

  const keyExtractor = useCallback((item) => item.id, []);

  return (
    <FlatList
      data={messages}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      initialNumToRender={10}
      maxToRenderPerBatch={10}
      windowSize={5}
      removeClippedSubviews={true}
      getItemLayout={(data, index) => ({
        length: 80, // Fixed height items
        offset: 80 * index,
        index,
      })}
    />
  );
}
```

**Why this matters:**
- ScrollView renders all items immediately (memory explosion)
- FlatList virtualizes - only renders visible items
- getItemLayout enables instant scroll-to-index
- removeClippedSubviews reduces memory on Android

**Related:** RN-SECTIONLIST, RN-MEMO

---

### RN-SECTIONLIST: Use SectionList for Grouped Data

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Manual section handling - error-prone and verbose
function ContactList({ contacts }) {
  const grouped = groupByFirstLetter(contacts);

  return (
    <ScrollView>
      {Object.entries(grouped).map(([letter, items]) => (
        <View key={letter}>
          <Text style={styles.header}>{letter}</Text>
          {items.map(contact => (
            <ContactItem key={contact.id} contact={contact} />
          ))}
        </View>
      ))}
    </ScrollView>
  );
}
```

**Improved code:**
```jsx
import { SectionList } from 'react-native';

function ContactList({ contacts }) {
  const sections = useMemo(() => {
    const grouped = contacts.reduce((acc, contact) => {
      const letter = contact.name[0].toUpperCase();
      if (!acc[letter]) acc[letter] = [];
      acc[letter].push(contact);
      return acc;
    }, {});

    return Object.entries(grouped)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([letter, data]) => ({ title: letter, data }));
  }, [contacts]);

  return (
    <SectionList
      sections={sections}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ContactItem contact={item} />}
      renderSectionHeader={({ section: { title } }) => (
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>{title}</Text>
        </View>
      )}
      stickySectionHeadersEnabled={true}
      initialNumToRender={20}
    />
  );
}
```

**Why this matters:**
- Built-in section header support with sticky headers
- Virtualization for performance
- Cleaner API for grouped data
- Better scroll-to-section support

**Related:** RN-FLATLIST, RN-MEMO

---

### RN-IMAGE: Optimize Image Loading and Caching

**Severity:** HIGH

**Problematic code:**
```jsx
// No optimization - slow loading, no caching
function ProductCard({ product }) {
  return (
    <View>
      <Image
        source={{ uri: product.imageUrl }}
        style={{ width: 200, height: 200 }}
      />
    </View>
  );
}
```

**Improved code:**
```jsx
import { Image } from 'expo-image';

function ProductCard({ product }) {
  return (
    <View>
      <Image
        source={{ uri: product.imageUrl }}
        style={{ width: 200, height: 200 }}
        contentFit="cover"
        placeholder={product.blurhash}
        transition={200}
        cachePolicy="memory-disk"
        recyclingKey={product.id}
      />
    </View>
  );
}

// For local assets, use require with proper sizing
function Logo() {
  return (
    <Image
      source={require('../assets/logo.png')}
      style={{ width: 100, height: 50 }}
      contentFit="contain"
    />
  );
}

// Preload critical images
import { Image } from 'expo-image';

async function preloadImages(urls) {
  await Image.prefetch(urls);
}
```

**Why this matters:**
- expo-image is significantly faster than RN Image
- Blurhash placeholders improve perceived performance
- Caching reduces network requests and load times
- recyclingKey helps with list performance

**Related:** RN-FLATLIST, RN-ASSETS

---

### RN-ASSETS: Manage Assets Properly

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Inconsistent asset loading
<Image source={{ uri: '../assets/logo.png' }} /> // Won't work
<Image source={require('./assets/icon')} /> // Missing extension
```

**Improved code:**
```javascript
// assets/index.js - centralized asset management
export const images = {
  logo: require('./images/logo.png'),
  placeholder: require('./images/placeholder.png'),
  icons: {
    home: require('./icons/home.png'),
    profile: require('./icons/profile.png'),
  },
};

export const fonts = {
  regular: require('./fonts/Inter-Regular.ttf'),
  bold: require('./fonts/Inter-Bold.ttf'),
};

// Load fonts with expo-font
import { useFonts } from 'expo-font';
import { fonts } from './assets';

function App() {
  const [fontsLoaded] = useFonts({
    'Inter-Regular': fonts.regular,
    'Inter-Bold': fonts.bold,
  });

  if (!fontsLoaded) {
    return <SplashScreen />;
  }

  return <MainApp />;
}

// app.json - preload assets
{
  "expo": {
    "assetBundlePatterns": ["**/*"],
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    }
  }
}
```

**Why this matters:**
- Centralized assets are easier to maintain
- Proper loading prevents runtime errors
- Font loading must complete before use
- Asset bundling improves startup time

**Related:** RN-IMAGE, EXPO-CONFIG

---

### RN-PRESSABLE: Use Pressable for Touch Interactions

**Severity:** MEDIUM

**Problematic code:**
```jsx
// TouchableOpacity has limited customization
<TouchableOpacity onPress={handlePress}>
  <Text>Press me</Text>
</TouchableOpacity>

// TouchableWithoutFeedback gives no visual feedback
<TouchableWithoutFeedback onPress={handlePress}>
  <View><Text>Press me</Text></View>
</TouchableWithoutFeedback>
```

**Improved code:**
```jsx
import { Pressable, StyleSheet } from 'react-native';

function Button({ onPress, title, disabled }) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        pressed && styles.buttonPressed,
        disabled && styles.buttonDisabled,
      ]}
      android_ripple={{ color: 'rgba(0, 0, 0, 0.1)' }}
      hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
    >
      {({ pressed }) => (
        <Text style={[
          styles.buttonText,
          pressed && styles.buttonTextPressed,
        ]}>
          {title}
        </Text>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    padding: 16,
    borderRadius: 8,
    backgroundColor: '#007AFF',
  },
  buttonPressed: {
    backgroundColor: '#0056b3',
    transform: [{ scale: 0.98 }],
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: '600',
  },
  buttonTextPressed: {
    opacity: 0.8,
  },
});
```

**Why this matters:**
- Pressable offers fine-grained press state control
- hitSlop improves touch targets for accessibility
- android_ripple provides native Android feedback
- Render props enable dynamic styling

**Related:** RN-ACCESSIBILITY, RN-STYLES

---

### RN-STYLES: Use StyleSheet.create for Styles

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Inline styles - recreated every render
function Card({ title }) {
  return (
    <View style={{
      padding: 16,
      margin: 8,
      backgroundColor: 'white',
      borderRadius: 8,
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>{title}</Text>
    </View>
  );
}
```

**Improved code:**
```jsx
import { StyleSheet, View, Text } from 'react-native';

function Card({ title, variant = 'default' }) {
  return (
    <View style={[styles.card, styles[variant]]}>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    margin: 8,
    backgroundColor: 'white',
    borderRadius: 8,
    ...shadowStyle,
  },
  default: {},
  highlighted: {
    borderColor: '#007AFF',
    borderWidth: 2,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
  },
});

// Shared shadow styles
const shadowStyle = {
  shadowColor: '#000',
  shadowOffset: { width: 0, height: 2 },
  shadowOpacity: 0.1,
  shadowRadius: 4,
  elevation: 3, // Android
};
```

**Why this matters:**
- StyleSheet.create validates styles at creation time
- Styles are created once, not every render
- Array syntax enables conditional styling
- Shared styles reduce duplication

**Related:** RN-MEMO, RN-PLATFORM

---

## Performance Guidelines (6 guidelines)

### RN-MEMO: Memoize Components and Callbacks

**Severity:** HIGH

**Problematic code:**
```jsx
// Re-renders on every parent render
function ParentScreen() {
  const [count, setCount] = useState(0);

  // New function created every render
  const handleItemPress = (id) => {
    console.log('Pressed:', id);
  };

  return (
    <View>
      <Text>Count: {count}</Text>
      <Button onPress={() => setCount(c => c + 1)} title="Increment" />
      <ExpensiveList onItemPress={handleItemPress} />
    </View>
  );
}

function ExpensiveList({ onItemPress }) {
  // Re-renders when parent count changes (unnecessary!)
  return <FlatList ... />;
}
```

**Improved code:**
```jsx
import { memo, useCallback, useMemo } from 'react';

function ParentScreen() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([]);

  // Stable callback reference
  const handleItemPress = useCallback((id) => {
    console.log('Pressed:', id);
  }, []);

  // Memoize expensive computations
  const sortedItems = useMemo(() =>
    [...items].sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  );

  return (
    <View>
      <Text>Count: {count}</Text>
      <Button onPress={() => setCount(c => c + 1)} title="Increment" />
      <ExpensiveList items={sortedItems} onItemPress={handleItemPress} />
    </View>
  );
}

// Memoized component - only re-renders when props change
const ExpensiveList = memo(function ExpensiveList({ items, onItemPress }) {
  const renderItem = useCallback(({ item }) => (
    <ListItem item={item} onPress={onItemPress} />
  ), [onItemPress]);

  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={item => item.id}
    />
  );
});
```

**Why this matters:**
- Mobile devices have limited CPU - avoid wasted renders
- memo() prevents re-renders when props unchanged
- useCallback stabilizes function references
- useMemo prevents expensive recomputation

**Related:** RN-FLATLIST, RN-JANK

---

### RN-JANK: Avoid JavaScript Thread Blocking

**Severity:** CRITICAL

**Problematic code:**
```jsx
// Blocks JS thread - causes UI jank
function SearchScreen() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = (text) => {
    setQuery(text);
    // Synchronous filtering blocks the thread
    const filtered = allItems.filter(item =>
      item.name.toLowerCase().includes(text.toLowerCase()) &&
      item.tags.some(tag => tag.includes(text))
    );
    setResults(filtered);
  };

  return (
    <TextInput
      value={query}
      onChangeText={handleSearch}
      placeholder="Search..."
    />
  );
}
```

**Improved code:**
```jsx
import { InteractionManager } from 'react-native';
import { useDeferredValue, useMemo, useTransition } from 'react';

function SearchScreen() {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  // Deferred value for non-urgent updates
  const deferredQuery = useDeferredValue(query);

  const results = useMemo(() => {
    if (!deferredQuery) return [];
    return allItems.filter(item =>
      item.name.toLowerCase().includes(deferredQuery.toLowerCase())
    );
  }, [deferredQuery]);

  const handleSearch = (text) => {
    setQuery(text);
  };

  return (
    <View>
      <TextInput
        value={query}
        onChangeText={handleSearch}
        placeholder="Search..."
      />
      {isPending && <ActivityIndicator />}
      <SearchResults results={results} />
    </View>
  );
}

// For heavy operations, use InteractionManager
async function loadDataAfterAnimation() {
  await InteractionManager.runAfterInteractions(async () => {
    // Heavy work here - runs after animations complete
    const data = await fetchLargeDataset();
    processData(data);
  });
}
```

**Why this matters:**
- JS thread blocking causes dropped frames (jank)
- Users notice stuttering during scroll/animations
- useDeferredValue keeps input responsive
- InteractionManager ensures smooth transitions

**Related:** RN-MEMO, RN-ANIMATION

---

### RN-ANIMATION: Use Native Driver for Animations

**Severity:** HIGH

**Problematic code:**
```jsx
// JS-driven animation - choppy on low-end devices
function FadeInView({ children }) {
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 300,
      useNativeDriver: false, // Runs on JS thread!
    }).start();
  }, []);

  return (
    <Animated.View style={{ opacity, backgroundColor: 'red' }}>
      {children}
    </Animated.View>
  );
}
```

**Improved code:**
```jsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  FadeIn,
  FadeOut,
} from 'react-native-reanimated';

// Option 1: Reanimated (recommended)
function FadeInView({ children }) {
  return (
    <Animated.View entering={FadeIn.duration(300)} exiting={FadeOut}>
      {children}
    </Animated.View>
  );
}

// Option 2: Reanimated with custom animation
function SlideInCard({ children }) {
  const translateY = useSharedValue(100);
  const opacity = useSharedValue(0);

  useEffect(() => {
    translateY.value = withSpring(0, { damping: 15 });
    opacity.value = withTiming(1, { duration: 300 });
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
}

// Option 3: Animated API with native driver (limited properties)
function NativeAnimatedView({ children }) {
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true, // Only works with transform and opacity
    }).start();
  }, []);

  return (
    <Animated.View style={{ opacity }}>
      {children}
    </Animated.View>
  );
}
```

**Why this matters:**
- Native driver runs animations on UI thread (60fps)
- JS-driven animations compete with business logic
- Reanimated 2+ offers best performance and flexibility
- Native driver only supports transform and opacity

**Related:** RN-JANK, RN-GESTURE

---

### RN-GESTURE: Use React Native Gesture Handler

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Built-in gestures have limitations
import { PanResponder, View } from 'react-native';

function DraggableCard() {
  const pan = useRef(new Animated.ValueXY()).current;

  const panResponder = PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onPanResponderMove: Animated.event([
      null,
      { dx: pan.x, dy: pan.y }
    ], { useNativeDriver: false }), // Can't use native driver!
    onPanResponderRelease: () => {
      Animated.spring(pan, {
        toValue: { x: 0, y: 0 },
        useNativeDriver: false,
      }).start();
    },
  });

  return (
    <Animated.View {...panResponder.panHandlers} style={pan.getLayout()}>
      <Card />
    </Animated.View>
  );
}
```

**Improved code:**
```jsx
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

function DraggableCard() {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  const context = useSharedValue({ x: 0, y: 0 });

  const gesture = Gesture.Pan()
    .onStart(() => {
      context.value = { x: translateX.value, y: translateY.value };
    })
    .onUpdate((event) => {
      translateX.value = context.value.x + event.translationX;
      translateY.value = context.value.y + event.translationY;
    })
    .onEnd(() => {
      translateX.value = withSpring(0);
      translateY.value = withSpring(0);
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={animatedStyle}>
        <Card />
      </Animated.View>
    </GestureDetector>
  );
}
```

**Why this matters:**
- Gesture Handler runs on native thread
- Smoother gestures, especially during scroll
- Composable gesture API (tap + pan, etc.)
- Better integration with Reanimated

**Related:** RN-ANIMATION, RN-JANK

---

### RN-BUNDLE: Reduce Bundle Size

**Severity:** MEDIUM

**Problematic code:**
```javascript
// Importing entire libraries
import _ from 'lodash';
import moment from 'moment';
import { View } from 'react-native';

const formatted = moment().format('YYYY-MM-DD');
const sorted = _.sortBy(items, 'name');
```

**Improved code:**
```javascript
// Import only what you need
import sortBy from 'lodash/sortBy';
import { format } from 'date-fns';

const formatted = format(new Date(), 'yyyy-MM-dd');
const sorted = sortBy(items, 'name');

// Or use native alternatives
const sorted = [...items].sort((a, b) => a.name.localeCompare(b.name));
const formatted = new Date().toISOString().split('T')[0];

// Analyze bundle size
// npx expo-optimize
// npx react-native-bundle-visualizer

// Lazy load heavy screens
const HeavyScreen = React.lazy(() => import('./HeavyScreen'));

function App() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <HeavyScreen />
    </Suspense>
  );
}
```

**Why this matters:**
- Smaller bundles = faster app startup
- Mobile networks may be slow
- moment.js is 300kb+, date-fns tree-shakes
- lodash full import adds unnecessary code

**Related:** EAS-BUILD, RN-JANK

---

### RN-HERMES: Enable Hermes Engine

**Severity:** HIGH

**Problematic code:**
```json
// app.json - Hermes disabled (slower startup)
{
  "expo": {
    "jsEngine": "jsc"
  }
}
```

**Improved code:**
```json
// app.json - Hermes enabled (default in SDK 48+)
{
  "expo": {
    "jsEngine": "hermes"
  }
}

// Verify Hermes is running
// In your app:
const isHermes = () => !!global.HermesInternal;
console.log('Hermes enabled:', isHermes());
```

**Why this matters:**
- Hermes reduces app startup time by 50%+
- Lower memory usage
- Smaller app size (bytecode vs plain JS)
- Default in Expo SDK 48+ and React Native 0.70+

**Related:** RN-BUNDLE, EAS-BUILD

---

## Navigation Guidelines (5 guidelines)

### NAV-STACK: Structure Navigation Correctly

**Severity:** HIGH

**Problematic code:**
```jsx
// Flat navigation - no clear hierarchy
function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
        <Stack.Screen name="ProductList" component={ProductListScreen} />
        <Stack.Screen name="ProductDetail" component={ProductDetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Improved code:**
```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Auth flow - separate stack
function AuthStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
    </Stack.Navigator>
  );
}

// Main tabs after login
function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="HomeTab" component={HomeStack} />
      <Tab.Screen name="ProfileTab" component={ProfileStack} />
      <Tab.Screen name="SettingsTab" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

// Nested stack for Home tab
function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="ProductList" component={ProductListScreen} />
      <Stack.Screen name="ProductDetail" component={ProductDetailScreen} />
    </Stack.Navigator>
  );
}

// Root navigator
function App() {
  const { isLoggedIn } = useAuth();

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isLoggedIn ? (
          <Stack.Screen name="Main" component={MainTabs} />
        ) : (
          <Stack.Screen name="Auth" component={AuthStack} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Why this matters:**
- Clear separation of auth and main flows
- Nested navigators match user mental model
- Tab-based navigation for main sections
- Conditional rendering based on auth state

**Related:** NAV-TYPES, NAV-DEEPLINK

---

### NAV-TYPES: Type Navigation with TypeScript

**Severity:** MEDIUM

**Problematic code:**
```tsx
// No type safety - runtime errors
function ProductScreen({ navigation, route }) {
  const productId = route.params.productId; // Could be undefined!

  const goToReviews = () => {
    navigation.navigate('Reviews', { id: productId }); // Typo in screen name?
  };
}
```

**Improved code:**
```tsx
// types/navigation.ts
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { CompositeScreenProps } from '@react-navigation/native';
import { BottomTabScreenProps } from '@react-navigation/bottom-tabs';

// Define param lists for each navigator
export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
};

export type AuthStackParamList = {
  Login: undefined;
  Register: { referralCode?: string };
};

export type MainTabParamList = {
  HomeTab: undefined;
  ProfileTab: undefined;
  SettingsTab: undefined;
};

export type HomeStackParamList = {
  Home: undefined;
  ProductList: { category: string };
  ProductDetail: { productId: string; productName: string };
  Reviews: { productId: string };
};

// Screen props types
export type ProductDetailScreenProps = CompositeScreenProps<
  NativeStackScreenProps<HomeStackParamList, 'ProductDetail'>,
  BottomTabScreenProps<MainTabParamList>
>;

// Usage with full type safety
function ProductDetailScreen({ navigation, route }: ProductDetailScreenProps) {
  const { productId, productName } = route.params; // Typed!

  const goToReviews = () => {
    navigation.navigate('Reviews', { productId }); // Autocomplete works!
  };

  return (
    <View>
      <Text>{productName}</Text>
      <Button title="Reviews" onPress={goToReviews} />
    </View>
  );
}

// Typed navigation hook
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

type HomeNavigation = NativeStackNavigationProp<HomeStackParamList>;

function useHomeNavigation() {
  return useNavigation<HomeNavigation>();
}
```

**Why this matters:**
- Catch navigation errors at compile time
- Autocomplete for screen names and params
- Required params enforced
- Refactoring is safer

**Related:** NAV-STACK, NAV-PARAMS

---

### NAV-DEEPLINK: Configure Deep Linking Properly

**Severity:** MEDIUM

**Problematic code:**
```jsx
// No deep linking - can't share or open specific screens
function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {/* ... */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Improved code:**
```jsx
import { NavigationContainer } from '@react-navigation/native';
import * as Linking from 'expo-linking';

// Define linking configuration
const linking = {
  prefixes: [
    Linking.createURL('/'),
    'https://myapp.com',
    'myapp://',
  ],
  config: {
    screens: {
      Auth: {
        screens: {
          Login: 'login',
          Register: 'register/:referralCode?',
        },
      },
      Main: {
        screens: {
          HomeTab: {
            screens: {
              Home: 'home',
              ProductList: 'products/:category',
              ProductDetail: 'product/:productId',
            },
          },
          ProfileTab: 'profile',
          SettingsTab: 'settings',
        },
      },
      NotFound: '*',
    },
  },
};

function App() {
  return (
    <NavigationContainer
      linking={linking}
      fallback={<LoadingScreen />}
    >
      <Stack.Navigator>
        {/* ... */}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// app.json - configure URL schemes
{
  "expo": {
    "scheme": "myapp",
    "ios": {
      "associatedDomains": ["applinks:myapp.com"]
    },
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [
            { "scheme": "https", "host": "myapp.com", "pathPrefix": "/" }
          ],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

**Why this matters:**
- Users can share links to specific content
- Marketing campaigns can link to app
- Universal links improve user experience
- Required for some features (email verification, etc.)

**Related:** NAV-STACK, EXPO-CONFIG

---

### NAV-PARAMS: Pass Navigation Params Correctly

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Passing entire objects - serialization issues
navigation.navigate('ProductDetail', {
  product: { id: 1, name: 'Item', data: complexObject }
});

// Passing functions - won't work
navigation.navigate('EditScreen', {
  onSave: (data) => saveData(data)
});
```

**Improved code:**
```jsx
// Pass only IDs, fetch data in target screen
navigation.navigate('ProductDetail', { productId: '123' });

function ProductDetailScreen({ route }) {
  const { productId } = route.params;
  const { data: product, isLoading } = useProduct(productId);

  if (isLoading) return <LoadingScreen />;
  return <ProductView product={product} />;
}

// For callbacks, use events or global state
import { DeviceEventEmitter } from 'react-native';

// Screen A - navigate and listen for result
function ScreenA() {
  useEffect(() => {
    const subscription = DeviceEventEmitter.addListener(
      'productEdited',
      (data) => {
        console.log('Product edited:', data);
      }
    );
    return () => subscription.remove();
  }, []);

  return (
    <Button
      title="Edit"
      onPress={() => navigation.navigate('EditScreen', { productId })}
    />
  );
}

// Screen B - emit event when done
function EditScreen({ route, navigation }) {
  const handleSave = async (data) => {
    await saveProduct(data);
    DeviceEventEmitter.emit('productEdited', data);
    navigation.goBack();
  };
}

// Or use React Navigation's event system
navigation.navigate('EditScreen', { productId });
// In EditScreen:
navigation.navigate({
  name: 'ScreenA',
  params: { editedProduct: data },
  merge: true,
});
```

**Why this matters:**
- Params are serialized - complex objects fail
- Functions can't be serialized
- IDs enable proper data fetching and caching
- Deep linking requires serializable params

**Related:** NAV-TYPES, NAV-STACK

---

### NAV-HEADER: Customize Headers Correctly

**Severity:** LOW

**Problematic code:**
```jsx
// Header customization scattered across screens
function ProductScreen({ navigation }) {
  useLayoutEffect(() => {
    navigation.setOptions({
      headerTitle: 'Product',
      headerRight: () => <CartButton />,
      headerStyle: { backgroundColor: 'white' },
      // Repeated in every screen...
    });
  }, []);
}
```

**Improved code:**
```jsx
// Centralized header configuration
const screenOptions = {
  headerStyle: {
    backgroundColor: '#ffffff',
  },
  headerTintColor: '#000000',
  headerTitleStyle: {
    fontWeight: '600',
  },
  headerShadowVisible: false,
  headerBackTitleVisible: false,
};

function HomeStack() {
  return (
    <Stack.Navigator screenOptions={screenOptions}>
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="ProductDetail"
        component={ProductDetailScreen}
        options={({ route }) => ({
          title: route.params.productName,
          headerRight: () => <ShareButton />,
        })}
      />
    </Stack.Navigator>
  );
}

// Custom header component for complex cases
function CustomHeader({ title, onBack, rightComponent }) {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.header, { paddingTop: insets.top }]}>
      <Pressable onPress={onBack} style={styles.backButton}>
        <Icon name="arrow-left" size={24} />
      </Pressable>
      <Text style={styles.title}>{title}</Text>
      {rightComponent}
    </View>
  );
}

// Use in screen
<Stack.Screen
  name="CustomScreen"
  component={CustomScreen}
  options={{
    header: (props) => (
      <CustomHeader
        title="Custom"
        onBack={() => props.navigation.goBack()}
        rightComponent={<SettingsButton />}
      />
    ),
  }}
/>
```

**Why this matters:**
- Centralized options reduce duplication
- Consistent header styling across app
- Custom headers for special cases
- Safe area handling for notches

**Related:** NAV-STACK, RN-SAFEAREA

---

## Platform-Specific Guidelines (4 guidelines)

### RN-PLATFORM: Handle Platform Differences

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Platform check everywhere
function Card() {
  return (
    <View style={{
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 3,
    }}>
      {Platform.OS === 'ios' ? <IOSComponent /> : <AndroidComponent />}
    </View>
  );
}
```

**Improved code:**
```jsx
import { Platform, StyleSheet } from 'react-native';

// Platform-specific styles
const styles = StyleSheet.create({
  card: {
    backgroundColor: 'white',
    borderRadius: 8,
    padding: 16,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
      },
      android: {
        elevation: 3,
      },
    }),
  },
  text: {
    fontFamily: Platform.select({
      ios: 'System',
      android: 'Roboto',
    }),
  },
});

// Platform-specific components via file extensions
// Button.ios.tsx
export function Button({ title, onPress }) {
  return <IOSButton title={title} onPress={onPress} />;
}

// Button.android.tsx
export function Button({ title, onPress }) {
  return <AndroidButton title={title} onPress={onPress} />;
}

// Usage - automatically picks correct file
import { Button } from './Button';

// Platform-specific logic
const statusBarHeight = Platform.select({
  ios: 44,
  android: StatusBar.currentHeight || 0,
});

// Check for specific OS version
if (Platform.OS === 'ios' && parseInt(Platform.Version, 10) >= 14) {
  // iOS 14+ specific code
}
```

**Why this matters:**
- iOS and Android have different design languages
- Shadow implementation differs between platforms
- File extensions enable clean platform separation
- Platform.select is cleaner than ternaries

**Related:** RN-STYLES, RN-SAFEAREA

---

### RN-SAFEAREA: Handle Safe Areas Correctly

**Severity:** HIGH

**Problematic code:**
```jsx
// Content hidden behind notch/home indicator
function Screen() {
  return (
    <View style={{ flex: 1 }}>
      <Header /> {/* May be behind notch */}
      <Content />
      <TabBar /> {/* May be behind home indicator */}
    </View>
  );
}
```

**Improved code:**
```jsx
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';
import { SafeAreaView } from 'react-native-safe-area-context';

// Wrap app in provider
function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        {/* ... */}
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

// Option 1: SafeAreaView for simple screens
function SimpleScreen() {
  return (
    <SafeAreaView style={{ flex: 1 }} edges={['top', 'bottom']}>
      <Content />
    </SafeAreaView>
  );
}

// Option 2: useSafeAreaInsets for fine control
function CustomScreen() {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ flex: 1 }}>
      <View style={{ paddingTop: insets.top }}>
        <Header />
      </View>
      <ScrollView contentContainerStyle={{ paddingBottom: insets.bottom }}>
        <Content />
      </ScrollView>
    </View>
  );
}

// Option 3: Edge-specific with tabs (bottom handled by tab bar)
function TabScreen() {
  return (
    <SafeAreaView style={{ flex: 1 }} edges={['top']}>
      <Content />
    </SafeAreaView>
  );
}

// Handle keyboard with KeyboardAvoidingView
import { KeyboardAvoidingView, Platform } from 'react-native';

function FormScreen() {
  const insets = useSafeAreaInsets();

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={insets.top}
    >
      <Form />
    </KeyboardAvoidingView>
  );
}
```

**Why this matters:**
- Modern phones have notches, Dynamic Island, home indicators
- Content must not be obscured by hardware
- Different edges need handling for different screens
- Tab bars usually handle bottom safe area

**Related:** RN-PLATFORM, NAV-HEADER

---

### RN-PERMISSIONS: Request Permissions Properly

**Severity:** HIGH

**Problematic code:**
```jsx
// Requesting permission without context
async function takePicture() {
  const { status } = await Camera.requestCameraPermissionsAsync();
  if (status === 'granted') {
    // Take picture
  }
}

// Called immediately on mount - bad UX
useEffect(() => {
  Camera.requestCameraPermissionsAsync();
  Location.requestForegroundPermissionsAsync();
  Notifications.requestPermissionsAsync();
}, []);
```

**Improved code:**
```jsx
import * as Camera from 'expo-camera';
import * as Location from 'expo-location';

// Check before requesting
async function checkCameraPermission() {
  const { status: existingStatus } = await Camera.getCameraPermissionsAsync();

  if (existingStatus === 'granted') {
    return true;
  }

  if (existingStatus === 'denied') {
    // Show settings prompt
    Alert.alert(
      'Camera Permission Required',
      'Please enable camera access in Settings to take photos.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Open Settings', onPress: () => Linking.openSettings() },
      ]
    );
    return false;
  }

  // First time - show rationale then request
  const { status } = await Camera.requestCameraPermissionsAsync();
  return status === 'granted';
}

// Request in context when user takes action
function CameraButton() {
  const handlePress = async () => {
    const hasPermission = await checkCameraPermission();
    if (hasPermission) {
      navigation.navigate('Camera');
    }
  };

  return <Button title="Take Photo" onPress={handlePress} />;
}

// Custom hook for permission management
function usePermission(permissionFn, requestFn) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    permissionFn().then(({ status }) => setStatus(status));
  }, []);

  const request = async () => {
    if (status === 'granted') return true;
    if (status === 'denied') {
      // Show settings alert
      return false;
    }
    const { status: newStatus } = await requestFn();
    setStatus(newStatus);
    return newStatus === 'granted';
  };

  return { status, request };
}

// Usage
const camera = usePermission(
  Camera.getCameraPermissionsAsync,
  Camera.requestCameraPermissionsAsync
);
```

**Why this matters:**
- Users grant permissions more often with context
- Requesting all permissions at startup is overwhelming
- Denied permissions need Settings redirect
- iOS requires specific usage descriptions

**Related:** EXPO-PLUGINS, RN-PLATFORM

---

### RN-STATUSBAR: Configure Status Bar Correctly

**Severity:** LOW

**Problematic code:**
```jsx
// Inconsistent status bar across screens
function LightScreen() {
  return <View style={{ backgroundColor: 'white' }}>{/* ... */}</View>;
}

function DarkScreen() {
  return <View style={{ backgroundColor: '#1a1a1a' }}>{/* ... */}</View>;
  // Status bar text is black - invisible!
}
```

**Improved code:**
```jsx
import { StatusBar } from 'expo-status-bar';
import { useIsFocused } from '@react-navigation/native';

// Global status bar in App
function App() {
  return (
    <>
      <StatusBar style="auto" />
      <NavigationContainer>
        {/* ... */}
      </NavigationContainer>
    </>
  );
}

// Screen-specific status bar
function DarkScreen() {
  const isFocused = useIsFocused();

  return (
    <View style={styles.darkContainer}>
      {isFocused && <StatusBar style="light" />}
      {/* Content */}
    </View>
  );
}

// Or use React Navigation's native header
<Stack.Screen
  name="DarkScreen"
  component={DarkScreen}
  options={{
    headerStyle: { backgroundColor: '#1a1a1a' },
    headerTintColor: '#ffffff',
    // Status bar handled automatically
  }}
/>

// Translucent status bar for full-screen content
function FullScreenImage() {
  return (
    <View style={StyleSheet.absoluteFill}>
      <StatusBar style="light" translucent backgroundColor="transparent" />
      <Image source={...} style={StyleSheet.absoluteFill} />
    </View>
  );
}
```

**Why this matters:**
- Status bar must contrast with background
- Screen-specific styling improves UX
- useIsFocused prevents status bar flicker
- Translucent enables full-screen designs

**Related:** RN-SAFEAREA, NAV-HEADER

---

## State Management Guidelines (4 guidelines)

### STATE-CONTEXT: Use Context for Global State

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Prop drilling through many levels
function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');

  return (
    <Navigator
      user={user}
      setUser={setUser}
      theme={theme}
      setTheme={setTheme}
    />
  );
}
```

**Improved code:**
```jsx
// contexts/AuthContext.tsx
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check stored auth state
    checkAuthState().then((user) => {
      setUser(user);
      setIsLoading(false);
    });
  }, []);

  const login = async (credentials) => {
    const user = await authApi.login(credentials);
    await SecureStore.setItemAsync('token', user.token);
    setUser(user);
  };

  const logout = async () => {
    await SecureStore.deleteItemAsync('token');
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, isLoading, login, logout }),
    [user, isLoading]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// Usage
function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <NavigationContainer>
          <RootNavigator />
        </NavigationContainer>
      </ThemeProvider>
    </AuthProvider>
  );
}

function ProfileScreen() {
  const { user, logout } = useAuth();
  return (
    <View>
      <Text>Welcome, {user.name}</Text>
      <Button title="Logout" onPress={logout} />
    </View>
  );
}
```

**Why this matters:**
- Avoids prop drilling
- Centralized state management
- Custom hooks provide clean API
- Context splitting prevents unnecessary re-renders

**Related:** STATE-PERSIST, RN-MEMO

---

### STATE-PERSIST: Persist State Correctly

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Using AsyncStorage for sensitive data
import AsyncStorage from '@react-native-async-storage/async-storage';

async function storeToken(token) {
  await AsyncStorage.setItem('authToken', token); // Not secure!
}

// Not handling hydration state
const [settings, setSettings] = useState(defaultSettings);
useEffect(() => {
  AsyncStorage.getItem('settings').then(data => {
    if (data) setSettings(JSON.parse(data));
  });
}, []);
// UI flickers with default then stored value
```

**Improved code:**
```jsx
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Secure storage for sensitive data
async function storeToken(token) {
  await SecureStore.setItemAsync('authToken', token);
}

async function getToken() {
  return SecureStore.getItemAsync('authToken');
}

// AsyncStorage for non-sensitive data with proper hydration
function usePersistedState(key, defaultValue) {
  const [state, setState] = useState(defaultValue);
  const [isHydrated, setIsHydrated] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(key)
      .then((data) => {
        if (data !== null) {
          setState(JSON.parse(data));
        }
      })
      .finally(() => setIsHydrated(true));
  }, [key]);

  const setPersistedState = useCallback((value) => {
    setState(value);
    AsyncStorage.setItem(key, JSON.stringify(value));
  }, [key]);

  return [state, setPersistedState, isHydrated];
}

// Usage with loading state
function SettingsScreen() {
  const [settings, setSettings, isHydrated] = usePersistedState(
    'settings',
    defaultSettings
  );

  if (!isHydrated) {
    return <LoadingScreen />;
  }

  return <SettingsForm settings={settings} onChange={setSettings} />;
}

// MMKV for performance-critical storage
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

function useMMKVState(key, defaultValue) {
  const [state, setState] = useState(() => {
    const stored = storage.getString(key);
    return stored ? JSON.parse(stored) : defaultValue;
  });

  const setPersistedState = useCallback((value) => {
    setState(value);
    storage.set(key, JSON.stringify(value));
  }, [key]);

  return [state, setPersistedState];
}
```

**Why this matters:**
- SecureStore encrypts sensitive data
- AsyncStorage is not encrypted (use for preferences)
- Hydration state prevents UI flicker
- MMKV is 10x faster than AsyncStorage

**Related:** STATE-CONTEXT, EXPO-SECRETS

---

### STATE-QUERY: Use React Query for Server State

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Manual data fetching - no caching, loading, error handling
function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  const refresh = () => {
    setLoading(true);
    fetchProducts()
      .then(setProducts)
      .catch(setError)
      .finally(() => setLoading(false));
  };
}
```

**Improved code:**
```jsx
import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query';

// Setup
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: false, // Different for mobile
      refetchOnReconnect: true,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <NavigationContainer>
        {/* ... */}
      </NavigationContainer>
    </QueryClientProvider>
  );
}

// Usage
function ProductList() {
  const {
    data: products,
    isLoading,
    error,
    refetch,
    isRefetching,
  } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  });

  if (isLoading) return <LoadingScreen />;
  if (error) return <ErrorScreen error={error} onRetry={refetch} />;

  return (
    <FlatList
      data={products}
      renderItem={({ item }) => <ProductItem product={item} />}
      refreshControl={
        <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
      }
    />
  );
}

// Mutations
function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}

// Prefetching for navigation
function ProductListScreen({ navigation }) {
  const queryClient = useQueryClient();

  const handleProductPress = (productId) => {
    // Prefetch before navigation
    queryClient.prefetchQuery({
      queryKey: ['product', productId],
      queryFn: () => fetchProduct(productId),
    });
    navigation.navigate('ProductDetail', { productId });
  };
}
```

**Why this matters:**
- Automatic caching reduces network requests
- Built-in loading/error states
- Refetch on reconnect for mobile
- Prefetching enables instant navigation

**Related:** STATE-CONTEXT, RN-OFFLINE

---

### STATE-ZUSTAND: Consider Zustand for Complex State

**Severity:** LOW

**Problematic code:**
```jsx
// Context with too much responsibility
const AppContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [cart, setCart] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [filters, setFilters] = useState({});
  const [sortOrder, setSortOrder] = useState('asc');
  // ... many more states and handlers
  // Every update re-renders all consumers!
}
```

**Improved code:**
```jsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Cart store with persistence
const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product) => set((state) => ({
        items: [...state.items, { ...product, quantity: 1 }],
      })),

      removeItem: (productId) => set((state) => ({
        items: state.items.filter((item) => item.id !== productId),
      })),

      updateQuantity: (productId, quantity) => set((state) => ({
        items: state.items.map((item) =>
          item.id === productId ? { ...item, quantity } : item
        ),
      })),

      clearCart: () => set({ items: [] }),

      // Computed values
      get totalItems() {
        return get().items.reduce((sum, item) => sum + item.quantity, 0);
      },

      get totalPrice() {
        return get().items.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        );
      },
    }),
    {
      name: 'cart-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);

// Usage - only re-renders when selected state changes
function CartBadge() {
  const totalItems = useCartStore((state) => state.totalItems);
  return <Badge count={totalItems} />;
}

function CartScreen() {
  const items = useCartStore((state) => state.items);
  const removeItem = useCartStore((state) => state.removeItem);

  return (
    <FlatList
      data={items}
      renderItem={({ item }) => (
        <CartItem item={item} onRemove={() => removeItem(item.id)} />
      )}
    />
  );
}

function ProductCard({ product }) {
  const addItem = useCartStore((state) => state.addItem);

  return (
    <View>
      <Text>{product.name}</Text>
      <Button title="Add to Cart" onPress={() => addItem(product)} />
    </View>
  );
}
```

**Why this matters:**
- Selective subscriptions prevent unnecessary re-renders
- Built-in persistence middleware
- No provider wrapper needed
- Simpler than Redux for most apps

**Related:** STATE-CONTEXT, STATE-PERSIST

---

## Error Handling Guidelines (3 guidelines)

### ERROR-BOUNDARY: Use Error Boundaries

**Severity:** HIGH

**Problematic code:**
```jsx
// No error handling - app crashes
function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Improved code:**
```jsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <View style={styles.errorContainer}>
      <Text style={styles.errorTitle}>Something went wrong</Text>
      <Text style={styles.errorMessage}>{error.message}</Text>
      <Button title="Try Again" onPress={resetErrorBoundary} />
    </View>
  );
}

function App() {
  const handleError = (error, info) => {
    // Log to crash reporting service
    crashlytics().recordError(error);
    console.error('Error boundary caught:', error, info);
  };

  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={handleError}
      onReset={() => {
        // Reset app state if needed
      }}
    >
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="Home" component={HomeScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </ErrorBoundary>
  );
}

// Granular error boundaries for sections
function ProductSection() {
  return (
    <ErrorBoundary
      FallbackComponent={SectionErrorFallback}
      onReset={() => queryClient.invalidateQueries(['products'])}
    >
      <ProductList />
    </ErrorBoundary>
  );
}
```

**Why this matters:**
- Prevents full app crash from component errors
- Shows user-friendly error message
- Enables recovery without app restart
- Logs errors for debugging

**Related:** ERROR-CRASH, ERROR-NETWORK

---

### ERROR-CRASH: Implement Crash Reporting

**Severity:** HIGH

**Problematic code:**
```jsx
// No crash reporting - blind to production issues
try {
  riskyOperation();
} catch (error) {
  console.log(error); // Lost in production
}
```

**Improved code:**
```jsx
import * as Sentry from '@sentry/react-native';

// Initialize in app entry
Sentry.init({
  dsn: 'https://your-sentry-dsn',
  enableAutoSessionTracking: true,
  tracesSampleRate: 0.2,
  environment: process.env.APP_ENV,
});

// Wrap app
export default Sentry.wrap(App);

// Or use Expo's error reporting
import * as Updates from 'expo-updates';

// Custom error logging utility
const ErrorLogger = {
  log: (error, context = {}) => {
    Sentry.captureException(error, {
      extra: {
        ...context,
        updateId: Updates.updateId,
        channel: Updates.channel,
      },
    });
  },

  setUser: (user) => {
    Sentry.setUser({
      id: user.id,
      email: user.email,
    });
  },

  addBreadcrumb: (message, data) => {
    Sentry.addBreadcrumb({
      message,
      data,
      level: 'info',
    });
  },
};

// Usage
async function fetchUserData(userId) {
  try {
    ErrorLogger.addBreadcrumb('Fetching user data', { userId });
    const response = await api.getUser(userId);
    return response.data;
  } catch (error) {
    ErrorLogger.log(error, { userId, action: 'fetchUserData' });
    throw error;
  }
}

// Global error handler
ErrorUtils.setGlobalHandler((error, isFatal) => {
  ErrorLogger.log(error, { isFatal });
  if (isFatal) {
    Alert.alert(
      'Unexpected Error',
      'The app needs to restart.',
      [{ text: 'OK', onPress: () => Updates.reloadAsync() }]
    );
  }
});
```

**Why this matters:**
- Production crashes need visibility
- Context helps reproduce issues
- Update ID links errors to specific versions
- Global handler catches unhandled errors

**Related:** ERROR-BOUNDARY, EAS-UPDATE

---

### ERROR-NETWORK: Handle Network Errors Gracefully

**Severity:** MEDIUM

**Problematic code:**
```jsx
// No network error handling
async function loadData() {
  const response = await fetch(API_URL);
  const data = await response.json();
  setData(data);
}
```

**Improved code:**
```jsx
import NetInfo from '@react-native-community/netinfo';

// Network-aware fetching
async function fetchWithRetry(url, options = {}, retries = 3) {
  const netInfo = await NetInfo.fetch();

  if (!netInfo.isConnected) {
    throw new NetworkError('No internet connection');
  }

  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new ApiError(response.status, await response.text());
      }

      return response.json();
    } catch (error) {
      if (attempt === retries - 1) throw error;
      await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)));
    }
  }
}

// Custom error classes
class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NetworkError';
  }
}

class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

// Network status hook
function useNetworkStatus() {
  const [isConnected, setIsConnected] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state) => {
      setIsConnected(state.isConnected);
    });
    return unsubscribe;
  }, []);

  return isConnected;
}

// Usage in component
function DataScreen() {
  const isConnected = useNetworkStatus();
  const { data, error, isLoading } = useQuery({
    queryKey: ['data'],
    queryFn: () => fetchWithRetry(API_URL),
    enabled: isConnected,
  });

  if (!isConnected) {
    return <OfflineBanner />;
  }

  if (error instanceof NetworkError) {
    return <NetworkErrorScreen onRetry={refetch} />;
  }

  if (error instanceof ApiError) {
    return <ApiErrorScreen status={error.status} />;
  }

  return <DataView data={data} />;
}
```

**Why this matters:**
- Mobile networks are unreliable
- Users need feedback about connectivity
- Retry logic handles transient failures
- Different errors need different handling

**Related:** RN-OFFLINE, STATE-QUERY

---

## Push Notifications Guidelines (2 guidelines)

### NOTIF-SETUP: Configure Push Notifications Correctly

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Missing configuration and error handling
async function registerForPushNotifications() {
  const token = await Notifications.getExpoPushTokenAsync();
  console.log(token);
}
```

**Improved code:**
```jsx
import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';

// Configure notification behavior
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

async function registerForPushNotificationsAsync() {
  // Must be physical device
  if (!Device.isDevice) {
    console.log('Push notifications require physical device');
    return null;
  }

  // Check existing permissions
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  // Request if not determined
  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    console.log('Push notification permission denied');
    return null;
  }

  // Get token
  const projectId = Constants.expoConfig?.extra?.eas?.projectId;
  const token = await Notifications.getExpoPushTokenAsync({ projectId });

  // Android channel setup
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'Default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF231F7C',
    });
  }

  return token.data;
}

// Hook for notification handling
function useNotifications() {
  const [expoPushToken, setExpoPushToken] = useState(null);
  const notificationListener = useRef();
  const responseListener = useRef();

  useEffect(() => {
    registerForPushNotificationsAsync().then((token) => {
      if (token) {
        setExpoPushToken(token);
        // Send token to backend
        api.registerPushToken(token);
      }
    });

    // Foreground notification received
    notificationListener.current = Notifications.addNotificationReceivedListener(
      (notification) => {
        console.log('Notification received:', notification);
      }
    );

    // User tapped notification
    responseListener.current = Notifications.addNotificationResponseReceivedListener(
      (response) => {
        const data = response.notification.request.content.data;
        handleNotificationNavigation(data);
      }
    );

    return () => {
      Notifications.removeNotificationSubscription(notificationListener.current);
      Notifications.removeNotificationSubscription(responseListener.current);
    };
  }, []);

  return { expoPushToken };
}
```

**Why this matters:**
- Physical device required for push notifications
- Permission handling affects user experience
- Android requires notification channels
- Token must be sent to backend

**Related:** EXPO-PLUGINS, NOTIF-HANDLE

---

### NOTIF-HANDLE: Handle Notification Actions

**Severity:** MEDIUM

**Problematic code:**
```jsx
// No handling of notification taps
Notifications.addNotificationResponseReceivedListener((response) => {
  console.log(response);
});
```

**Improved code:**
```jsx
import { navigationRef } from './navigation';

// Centralized notification handler
function handleNotificationNavigation(data) {
  if (!data?.type) return;

  switch (data.type) {
    case 'new_message':
      navigationRef.navigate('Chat', {
        conversationId: data.conversationId
      });
      break;

    case 'order_update':
      navigationRef.navigate('OrderDetail', {
        orderId: data.orderId
      });
      break;

    case 'promotion':
      navigationRef.navigate('Promotion', {
        promoId: data.promoId
      });
      break;

    default:
      navigationRef.navigate('Home');
  }
}

// Handle notification that launched app
async function handleInitialNotification() {
  const response = await Notifications.getLastNotificationResponseAsync();
  if (response) {
    const data = response.notification.request.content.data;
    // Delay navigation until app is ready
    setTimeout(() => handleNotificationNavigation(data), 500);
  }
}

// Navigation ref for use outside components
// navigation.js
import { createNavigationContainerRef } from '@react-navigation/native';

export const navigationRef = createNavigationContainerRef();

export function navigate(name, params) {
  if (navigationRef.isReady()) {
    navigationRef.navigate(name, params);
  }
}

// App.js
function App() {
  useEffect(() => {
    handleInitialNotification();
  }, []);

  return (
    <NavigationContainer ref={navigationRef}>
      {/* ... */}
    </NavigationContainer>
  );
}

// Local notifications
async function scheduleLocalNotification(title, body, data, trigger) {
  await Notifications.scheduleNotificationAsync({
    content: {
      title,
      body,
      data,
      sound: 'default',
    },
    trigger, // { seconds: 60 } or { date: new Date() }
  });
}
```

**Why this matters:**
- Users expect taps to navigate to relevant content
- Initial notification requires special handling
- Navigation ref enables notification-triggered navigation
- Local notifications for reminders and timers

**Related:** NOTIF-SETUP, NAV-DEEPLINK

---

## Accessibility Guidelines (3 guidelines)

### RN-ACCESSIBILITY: Make Components Accessible

**Severity:** HIGH

**Problematic code:**
```jsx
// No accessibility properties
function ProductCard({ product, onPress }) {
  return (
    <TouchableOpacity onPress={onPress}>
      <Image source={{ uri: product.image }} />
      <Text>{product.name}</Text>
      <Text>${product.price}</Text>
    </TouchableOpacity>
  );
}
```

**Improved code:**
```jsx
function ProductCard({ product, onPress }) {
  return (
    <Pressable
      onPress={onPress}
      accessible={true}
      accessibilityRole="button"
      accessibilityLabel={`${product.name}, ${product.price} dollars`}
      accessibilityHint="Double tap to view product details"
    >
      <Image
        source={{ uri: product.image }}
        accessibilityLabel={`Image of ${product.name}`}
      />
      <Text
        accessibilityRole="header"
        style={styles.productName}
      >
        {product.name}
      </Text>
      <Text accessibilityLabel={`Price: ${product.price} dollars`}>
        ${product.price}
      </Text>
    </Pressable>
  );
}

// Form accessibility
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  return (
    <View accessibilityRole="form">
      <Text nativeID="emailLabel">Email</Text>
      <TextInput
        value={email}
        onChangeText={setEmail}
        accessibilityLabel="Email"
        accessibilityLabelledBy="emailLabel"
        textContentType="emailAddress"
        keyboardType="email-address"
        autoCapitalize="none"
        autoComplete="email"
      />

      <Text nativeID="passwordLabel">Password</Text>
      <TextInput
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        accessibilityLabel="Password"
        accessibilityLabelledBy="passwordLabel"
        textContentType="password"
        autoComplete="password"
      />

      {error && (
        <Text
          accessibilityRole="alert"
          accessibilityLiveRegion="polite"
          style={styles.error}
        >
          {error}
        </Text>
      )}

      <Pressable
        onPress={handleSubmit}
        accessibilityRole="button"
        accessibilityLabel="Sign in"
        accessibilityState={{ disabled: !email || !password }}
        disabled={!email || !password}
      >
        <Text>Sign In</Text>
      </Pressable>
    </View>
  );
}
```

**Why this matters:**
- Screen readers need labels to describe content
- accessibilityRole helps users understand interactions
- accessibilityHint describes action result
- Forms need proper labeling for usability

**Related:** RN-PRESSABLE, RN-TOUCH

---

### RN-TOUCH: Ensure Adequate Touch Targets

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Touch target too small
<TouchableOpacity onPress={handleClose} style={{ padding: 4 }}>
  <Icon name="close" size={16} />
</TouchableOpacity>
```

**Improved code:**
```jsx
// Minimum 44x44 points for touch targets (Apple HIG)
// Minimum 48x48 dp for Android (Material Design)

function IconButton({ icon, onPress, accessibilityLabel }) {
  return (
    <Pressable
      onPress={onPress}
      style={styles.iconButton}
      hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
      accessibilityRole="button"
      accessibilityLabel={accessibilityLabel}
    >
      <Icon name={icon} size={24} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  iconButton: {
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

// List items with proper touch areas
function ListItem({ item, onPress }) {
  return (
    <Pressable
      onPress={onPress}
      style={styles.listItem}
      android_ripple={{ color: 'rgba(0, 0, 0, 0.1)' }}
    >
      <View style={styles.listItemContent}>
        <Text>{item.title}</Text>
        <Text style={styles.subtitle}>{item.subtitle}</Text>
      </View>
      <Icon name="chevron-right" size={20} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  listItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    minHeight: 56, // Adequate touch height
  },
  listItemContent: {
    flex: 1,
  },
});
```

**Why this matters:**
- Small touch targets cause frustration
- Users with motor impairments need larger targets
- hitSlop extends touch area without visual change
- Platform guidelines specify minimum sizes

**Related:** RN-ACCESSIBILITY, RN-PRESSABLE

---

### RN-FONT-SCALE: Support Dynamic Font Sizes

**Severity:** MEDIUM

**Problematic code:**
```jsx
// Fixed font sizes - ignores user preferences
const styles = StyleSheet.create({
  title: {
    fontSize: 24,
  },
  body: {
    fontSize: 14,
  },
});
```

**Improved code:**
```jsx
import { PixelRatio, useWindowDimensions, Text as RNText } from 'react-native';

// Option 1: Allow system font scaling (default)
function ScalableText({ style, ...props }) {
  return <RNText style={style} {...props} />;
}

// Option 2: Limit maximum scaling
function LimitedScaleText({ style, maxFontSizeMultiplier = 1.5, ...props }) {
  return (
    <RNText
      style={style}
      maxFontSizeMultiplier={maxFontSizeMultiplier}
      {...props}
    />
  );
}

// Option 3: Use scaled font sizes
function useScaledFontSize(baseSize) {
  const { fontScale } = useWindowDimensions();
  return baseSize * Math.min(fontScale, 1.5); // Cap at 1.5x
}

// Responsive typography system
const createTypography = (fontScale) => ({
  h1: {
    fontSize: Math.min(32 * fontScale, 48),
    lineHeight: Math.min(40 * fontScale, 56),
    fontWeight: 'bold',
  },
  h2: {
    fontSize: Math.min(24 * fontScale, 36),
    lineHeight: Math.min(32 * fontScale, 44),
    fontWeight: '600',
  },
  body: {
    fontSize: Math.min(16 * fontScale, 24),
    lineHeight: Math.min(24 * fontScale, 36),
  },
  caption: {
    fontSize: Math.min(12 * fontScale, 18),
    lineHeight: Math.min(16 * fontScale, 24),
  },
});

// Usage
function TypographyProvider({ children }) {
  const { fontScale } = useWindowDimensions();
  const typography = useMemo(() => createTypography(fontScale), [fontScale]);

  return (
    <TypographyContext.Provider value={typography}>
      {children}
    </TypographyContext.Provider>
  );
}

function Title({ children }) {
  const typography = useTypography();
  return <Text style={typography.h1}>{children}</Text>;
}
```

**Why this matters:**
- Users with vision impairments need larger text
- iOS and Android have accessibility font settings
- Unlimited scaling can break layouts
- maxFontSizeMultiplier limits scaling per element

**Related:** RN-ACCESSIBILITY, RN-STYLES

---

## Expected Good Patterns

When reviewing React Native Expo code, look for these positive patterns:

### Configuration
```javascript
// app.config.js with environment support
export default ({ config }) => ({
  ...config,
  extra: {
    apiUrl: process.env.API_URL,
  },
});
```

### Performance
```jsx
// Memoized FlatList with optimizations
const MemoizedItem = memo(ItemComponent);

<FlatList
  data={data}
  renderItem={({ item }) => <MemoizedItem item={item} />}
  keyExtractor={(item) => item.id}
  getItemLayout={(data, index) => ({ length: 80, offset: 80 * index, index })}
  removeClippedSubviews={true}
/>
```

### Navigation
```tsx
// Type-safe navigation with proper structure
type RootStackParamList = {
  Home: undefined;
  Product: { productId: string };
};

navigation.navigate('Product', { productId: '123' });
```

### State Management
```jsx
// Context with custom hook
const { user, login, logout } = useAuth();
```

### Error Handling
```jsx
// Error boundary with crash reporting
<ErrorBoundary onError={Sentry.captureException}>
  <App />
</ErrorBoundary>
```

### Accessibility
```jsx
// Accessible button
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Add to cart"
  accessibilityHint="Adds this item to your shopping cart"
>
```

---

## Example Review Output

```markdown
## React Native Expo Review: ShoppingApp

### CRITICAL Issues

#### RN-FLATLIST: ScrollView Used for Long Product List
**File:** `src/screens/ProductList.tsx:45`

**Problematic code:**
```jsx
<ScrollView>
  {products.map(product => <ProductCard key={product.id} product={product} />)}
</ScrollView>
```

**Improved code:**
```jsx
<FlatList
  data={products}
  renderItem={({ item }) => <ProductCard product={item} />}
  keyExtractor={(item) => item.id}
  initialNumToRender={10}
/>
```

**Why:** ScrollView renders all 500+ products at once, causing 2-3 second load time and potential crashes on low-memory devices.

---

### HIGH Issues

#### EXPO-SECRETS: API Key Hardcoded in Source
**File:** `src/config/api.ts:3`

**Problematic code:**
```typescript
const STRIPE_KEY = 'pk_live_abc123...';
```

**Improved code:**
```typescript
const STRIPE_KEY = Constants.expoConfig?.extra?.stripeKey;
```

**Why:** API keys in source code can be extracted from app bundles. Use environment variables and EAS Secrets.

---

### MEDIUM Issues

#### NAV-TYPES: Navigation Lacks TypeScript Types
**File:** `src/navigation/index.tsx`

Navigation uses `any` types, missing type safety for screen params.

---

### Well Done

- ERROR-BOUNDARY: App wrapped in ErrorBoundary with Sentry integration
- RN-SAFEAREA: Consistent SafeAreaView usage across screens
- STATE-QUERY: React Query used for server state with proper caching
- RN-IMAGE: Using expo-image with blurhash placeholders
```
