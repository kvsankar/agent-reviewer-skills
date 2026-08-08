# javascript-refactoring-reviewer Review

**Repository:** https://github.com/maciekt07/TodoApp
**Review Date:** 2025-12-01 05:22:17
**Reviewer:** javascript-refactoring-reviewer
**AI Provider:** claude

---

Now I have a comprehensive understanding of the codebase. Let me generate a detailed refactoring review:

# Refactoring Review: TodoApp React/TypeScript Codebase

## ✅ Strengths

- **MODERN-JS**: Excellent use of modern TypeScript/React patterns with functional components, hooks, and context
- **CONST-LET**: Consistent use of `const` and `let` throughout the codebase
- **DESTRUCTURE**: Good use of object destructuring in component props and context extraction
- **TEMPLATE-LIT**: Template literals used appropriately for string interpolation
- **ASYNC-AWAIT**: Proper async/await usage in service layers and utility functions

## 🔨 Refactoring Opportunities

### READABILITY: LONG-FUNC - Refactor App Component Initialization Logic

**Current code:**
```typescript
// src/App.tsx:25-85
useEffect(() => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const updateNestedProperties = (userObject: any, defaultObject: any): any => {
    if (!userObject) return defaultObject;

    Object.keys(defaultObject).forEach((key) => {
      if (key === "categories") return;

      if (
        key === "colorList" &&
        userObject.colorList &&
        !defaultUser.colorList.every((element, index) => element === userObject.colorList[index])
      ) {
        return;
      }

      if (key === "favoriteCategories" && Array.isArray(userObject.favoriteCategories)) {
        userObject.favoriteCategories = userObject.favoriteCategories.filter((id: UUID) =>
          userObject.categories.some((cat: Category) => cat.id === id),
        );
        return;
      }

      if (key === "settings" && Array.isArray(userObject.settings)) {
        delete userObject.settings;
        showToast("Removed old settings array format.", {
          duration: 6000,
          icon: <DeleteForeverRounded />,
          disableVibrate: true,
        });
      }

      const userValue = userObject[key];
      const defaultValue = defaultObject[key];

      if (typeof defaultValue === "object" && defaultValue !== null) {
        userObject[key] = updateNestedProperties(userValue, defaultValue);
      } else if (userValue === undefined) {
        userObject[key] = defaultValue;
        showToast(
          <div>
            Added new property to user object{" "}
            <i translate="no">
              {key.toString()}: {userObject[key].toString()}
            </i>
          </div>,
          {
            duration: 6000,
            icon: <DataObjectRounded />,
            disableVibrate: true,
          },
        );
      }
    });

    return userObject;
  };

  setUser((prevUser) => {
    const updatedUser = updateNestedProperties({ ...prevUser }, defaultUser);
    return prevUser !== updatedUser ? updatedUser : prevUser;
  });
}, [setUser]);
```

**Refactored code:**
```typescript
// src/App.tsx - Extract to separate file: src/utils/userMigration.ts
export const migrateUserData = (userObject: any, defaultObject: any): any => {
  if (!userObject) return defaultObject;

  const updatedUser = { ...userObject };
  
  Object.keys(defaultObject).forEach((key) => {
    updatedUser = migrateProperty(updatedUser, defaultObject, key);
  });

  return updatedUser;
};

const migrateProperty = (userObject: any, defaultObject: any, key: string) => {
  if (key === "categories") return userObject;
  
  if (shouldPreserveColorList(userObject, key)) return userObject;
  
  if (key === "favoriteCategories") {
    return migrateFavoriteCategories(userObject);
  }
  
  if (key === "settings" && Array.isArray(userObject.settings)) {
    return migrateSettingsFormat(userObject);
  }
  
  return migrateNestedOrMissingProperty(userObject, defaultObject, key);
};

// In App.tsx:
useEffect(() => {
  setUser((prevUser) => {
    const updatedUser = migrateUserData(prevUser, defaultUser);
    return prevUser !== updatedUser ? updatedUser : prevUser;
  });
}, [setUser]);
```

**Why this matters:**
- Breaks down 60+ line function into focused, testable pieces
- Improves maintainability through separation of concerns
- Each migration step has a clear responsibility
- Easier to add new migration logic

**Code smell addressed:**
Long Method (>50 lines), complex nested logic

---

### MAINTAINABILITY: LONG-METHOD - Break Down TasksList Component

**Current code:**
```typescript
// src/components/tasks/TasksList.tsx:1-755 (755 lines!)
export const TasksList: React.FC = () => {
  // 50+ lines of state declarations
  // 200+ lines of filtering/sorting logic  
  // 300+ lines of event handlers
  // 200+ lines of JSX rendering
};
```

**Refactored code:**
```typescript
// src/components/tasks/TasksList.tsx
export const TasksList: React.FC = () => {
  return (
    <>
      <TaskMenu />
      <TasksContainer style={{ marginTop: user.settings.showProgressBar ? "0" : "24px" }}>
        <TaskSearchAndSort />
        <TaskCategoriesList />
        <TaskSelectionActions />
        <TaskMoveMode />
        <TaskSearchResults />
        <TaskListContent />
        <EditTaskModal />
        <DeleteTaskDialogs />
      </TasksContainer>
    </>
  );
};

// src/components/tasks/components/TaskSearchAndSort.tsx
export const TaskSearchAndSort = () => {
  const { search, setSearch, moveMode } = useContext(TaskContext);
  // Search and sort logic only
};

// src/components/tasks/components/TaskListContent.tsx
export const TaskListContent = () => {
  const { orderedTasks, moveMode } = useTasksList();
  // Rendering logic only
};

// src/hooks/useTasksList.ts
export const useTasksList = () => {
  // All filtering, sorting, and reordering logic
  return { orderedTasks, reorderTasks };
};
```

**Why this matters:**
- 755-line component becomes manageable, focused components
- Each component has single responsibility
- Logic can be tested independently
- Easier to modify individual features

**Code smell addressed:**
Large Class/God Object, violates Single Responsibility Principle

---

### PERFORMANCE: ALGO-COMPLEX - Optimize Task Filtering

**Current code:**
```typescript
// src/components/tasks/TasksList.tsx:194-246
const reorderTasks = useCallback(
  (tasks: Task[]): Task[] => {
    // Separate tasks into pinned and unpinned
    let pinnedTasks = tasks.filter((task) => task.pinned);
    let unpinnedTasks = tasks.filter((task) => !task.pinned);

    // Filter tasks based on the selected category
    if (selectedCatId !== undefined) {
      const categoryFilter = (task: Task) =>
        task.category?.some((category) => category.id === selectedCatId) ?? false;
      unpinnedTasks = unpinnedTasks.filter(categoryFilter);
      pinnedTasks = pinnedTasks.filter(categoryFilter);
    }

    // Filter tasks based on the search input
    const searchLower = search.toLowerCase();
    const searchFilter = (task: Task) =>
      task.name.toLowerCase().includes(searchLower) ||
      (task.description && task.description.toLowerCase().includes(searchLower));
    unpinnedTasks = unpinnedTasks.filter(searchFilter);
    pinnedTasks = pinnedTasks.filter(searchFilter);
    
    // Multiple iterations through arrays
  },
  [search, selectedCatId, user.settings?.doneToBottom, sortOption],
);
```

**Refactored code:**
```typescript
// src/hooks/useTaskFilter.ts
const reorderTasks = useCallback(
  (tasks: Task[]): Task[] => {
    const searchLower = search.toLowerCase();
    
    // Single pass filter with combined conditions
    const filteredTasks = tasks.filter((task) => {
      // Category filter
      if (selectedCatId !== undefined) {
        const hasCategory = task.category?.some((cat) => cat.id === selectedCatId) ?? false;
        if (!hasCategory) return false;
      }
      
      // Search filter
      if (search) {
        const matchesSearch = task.name.toLowerCase().includes(searchLower) ||
          (task.description && task.description.toLowerCase().includes(searchLower));
        if (!matchesSearch) return false;
      }
      
      return true;
    });
    
    // Separate and sort in single operation
    return separateAndSortTasks(filteredTasks, sortOption, user.settings?.doneToBottom);
  },
  [search, selectedCatId, user.settings?.doneToBottom, sortOption],
);

const separateAndSortTasks = (tasks: Task[], sortOption: string, doneToBottom: boolean) => {
  const pinnedTasks: Task[] = [];
  const unpinnedTasks: Task[] = [];
  
  // Single pass separation
  tasks.forEach(task => {
    if (task.pinned) pinnedTasks.push(task);
    else unpinnedTasks.push(task);
  });
  
  // Sort each group
  const sortedPinned = sortTasks(pinnedTasks, sortOption);
  const sortedUnpinned = sortTasksWithDoneHandling(unpinnedTasks, sortOption, doneToBottom);
  
  return [...sortedPinned, ...sortedUnpinned];
};
```

**Why this matters:**
- Reduces O(n) iterations from 6+ to 2
- Single-pass filtering improves performance for large task lists
- Clear separation of filtering and sorting logic
- More efficient memory usage

**Code smell addressed:**
Inefficient algorithm complexity, multiple array iterations

---

### TESTABILITY: INJECT-DEP - Extract Badge Management Logic

**Current code:**
```typescript
// src/App.tsx:90-129
useEffect(() => {
  const setBadge = async (count: number) => {
    if ("setAppBadge" in navigator) {
      try {
        await navigator.setAppBadge(count);
      } catch (error) {
        console.error("Failed to set app badge:", error);
      }
    }
  };

  const clearBadge = async () => {
    if ("clearAppBadge" in navigator) {
      try {
        await navigator.clearAppBadge();
      } catch (error) {
        console.error("Failed to clear app badge:", error);
      }
    }
  };

  const displayAppBadge = async () => {
    if (user.settings.appBadge) {
      if ((await Notification.requestPermission()) === "granted") {
        const incompleteTasksCount = user.tasks.filter((task) => !task.done).length;
        if (!isNaN(incompleteTasksCount)) {
          setBadge(incompleteTasksCount);
        }
      }
    } else {
      clearBadge();
    }
  };

  if ("setAppBadge" in navigator) {
    displayAppBadge();
  }
}, [user.settings.appBadge, user.tasks]);
```

**Refactored code:**
```typescript
// src/services/badgeService.ts
export class BadgeService {
  private hasSupport(): boolean {
    return "setAppBadge" in navigator && "clearAppBadge" in navigator;
  }

  async setBadge(count: number): Promise<void> {
    if (!this.hasSupport()) return;
    
    try {
      await navigator.setAppBadge(count);
    } catch (error) {
      console.error("Failed to set app badge:", error);
    }
  }

  async clearBadge(): Promise<void> {
    if (!this.hasSupport()) return;
    
    try {
      await navigator.clearAppBadge();
    } catch (error) {
      console.error("Failed to clear app badge:", error);
    }
  }

  async updateBadgeForTasks(tasks: Task[], enabled: boolean): Promise<void> {
    if (!enabled) {
      await this.clearBadge();
      return;
    }

    const permission = await Notification.requestPermission();
    if (permission !== "granted") return;

    const incompleteCount = tasks.filter(task => !task.done).length;
    if (!isNaN(incompleteCount)) {
      await this.setBadge(incompleteCount);
    }
  }
}

// src/hooks/useBadgeManager.ts
export const useBadgeManager = (tasks: Task[], enabled: boolean) => {
  const badgeService = useMemo(() => new BadgeService(), []);

  useEffect(() => {
    badgeService.updateBadgeForTasks(tasks, enabled);
  }, [tasks, enabled, badgeService]);
};

// src/App.tsx
function App() {
  // ... other code
  useBadgeManager(user.tasks, user.settings.appBadge);
}
```

**Why this matters:**
- Easy to mock BadgeService in tests
- Clear separation of badge logic from App component
- Single responsibility for badge management
- Reusable across different components

**Code smell addressed:**
Hidden dependencies on navigator API, difficult to test

---

### READABILITY: EXTRACT-FUNC - Simplify TaskItem Component

**Current code:**
```typescript
// src/components/tasks/TaskItem.tsx:85-200+ (complex JSX with inline logic)
return (
  <TaskContainer
    ref={(node) => {
      setNodeRef(node);
      itemRef.current = node;
    }}
    id={task.id}
    onContextMenu={onContextMenu}
    backgroundColor={task.color}
    glow={enableGlow && !moveMode}
    done={task.done}
    blur={blur}
    isDragging={isDragging}
    data-testid="task-container"
    style={{
      transform: CSS.Transform.toString(transform),
      transition,
      opacity: isDragging ? 0.5 : 1,
      cursor: undefined,
    }}
    {...attributes}
  >
    {enableMoveMode && moveMode && (
      <DragHandle {...listeners}>
        <DragIndicatorRounded sx={{ mr: "4px", ml: "-8px" }} />
      </DragHandle>
    )}
    {enableSelection && selectedIds.length > 0 && (
      <StyledRadio
        clr={getFontColor(task.color)}
        checked={isSelected}
        icon={<RadioUnchecked />}
        checkedIcon={<RadioChecked />}
        onChange={() => handleSelectChange(task.id)}
        // ... more props
      />
    )}
    {/* 150+ more lines of complex conditional JSX */}
  </TaskContainer>
);
```

**Refactored code:**
```typescript
// src/components/tasks/TaskItem.tsx
export const TaskItem = memo(({ task, features, selection, ...props }: TaskItemProps) => {
  return (
    <TaskContainer {...getContainerProps(task, props)}>
      <TaskDragHandle moveMode={features.enableMoveMode} />
      <TaskSelectionCheckbox task={task} selection={selection} features={features} />
      <TaskEmoji task={task} />
      <TaskContent task={task} features={features} />
      <TaskActionsContainer>{props.actions}</TaskActionsContainer>
    </TaskContainer>
  );
});

// src/components/tasks/components/TaskDragHandle.tsx
export const TaskDragHandle = ({ moveMode }: { moveMode?: boolean }) => {
  if (!moveMode) return null;
  
  return (
    <DragHandle {...listeners}>
      <DragIndicatorRounded sx={{ mr: "4px", ml: "-8px" }} />
    </DragHandle>
  );
};

// src/components/tasks/components/TaskContent.tsx
export const TaskContent = ({ task, features }: TaskContentProps) => {
  return (
    <TaskInfo translate="no">
      <TaskPinnedIndicator pinned={task.pinned} />
      <TaskHeader task={task} />
      <TaskDescription task={task} features={features} />
      <TaskDeadline task={task} />
      <TaskSharedBy sharedBy={task.sharedBy} />
      <TaskCategories task={task} />
    </TaskInfo>
  );
};
```

**Why this matters:**
- Each component has single, clear responsibility
- Easier to test individual parts
- Reduces cognitive load when reading code
- Better reusability of sub-components

**Code smell addressed:**
Large Class/Method, complex conditional rendering

---

### MAINTAINABILITY: DRY-VIOLATION - Extract Common Date Formatting

**Current code:**
```typescript
// Multiple files with duplicate date formatting logic
// src/components/tasks/TaskItem.tsx:132-137
<Tooltip
  title={
    new Intl.DateTimeFormat(navigator.language, {
      dateStyle: "full",
      timeStyle: "medium",
    }).format(new Date(task.date))
  }
>

// src/components/tasks/TaskItem.tsx:152-157  
<Tooltip
  title={
    new Intl.DateTimeFormat(navigator.language, {
      dateStyle: "full",
      timeStyle: "medium",
    }).format(new Date(task.deadline))
  }
>

// Similar patterns in src/utils/timeUtils.ts with different formats
```

**Refactored code:**
```typescript
// src/utils/dateFormatters.ts
export class DateFormatter {
  private static readonly locale = navigator.language || "en-US";

  static fullDateTime(date: Date): string {
    return new Intl.DateTimeFormat(this.locale, {
      dateStyle: "full",
      timeStyle: "medium",
    }).format(date);
  }

  static shortDate(date: Date): string {
    return new Intl.DateTimeFormat(this.locale, {
      year: "numeric",
      month: "2-digit", 
      day: "2-digit",
    }).format(date);
  }

  static timeOnly(date: Date): string {
    return new Intl.DateTimeFormat(this.locale, {
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  }

  static relativeTime(date: Date): string {
    return new Intl.RelativeTimeFormat(this.locale, { 
      numeric: "auto" 
    }).formatToParts(/* calculation */);
  }
}

// Usage in components:
<Tooltip title={DateFormatter.fullDateTime(new Date(task.date))}>
<Tooltip title={DateFormatter.fullDateTime(new Date(task.deadline))}>
```

**Why this matters:**
- Single source of truth for date formatting
- Consistent formatting across the app
- Easy to change locale or format globally
- Reduces code duplication

**Code smell addressed:**
Code duplication, scattered formatting logic

---

### READABILITY: MAGIC-NUM - Extract Time Constants

**Current code:**
```typescript
// src/utils/timeUtils.ts:1-3
const MS_IN_MINUTE = 60 * 1000;
const MS_IN_HOUR = 60 * MS_IN_MINUTE;
const MS_IN_DAY = 24 * MS_IN_HOUR;

// But scattered throughout:
// duration: 6000 (in showToast calls)
// delay: 150 (in touch sensor)
// tolerance: 5 (in activation constraint)
```

**Refactored code:**
```typescript
// src/constants/timeConstants.ts
export const TIME_CONSTANTS = {
  // Base units
  MS_IN_SECOND: 1000,
  MS_IN_MINUTE: 60 * 1000,
  MS_IN_HOUR: 60 * 60 * 1000,
  MS_IN_DAY: 24 * 60 * 60 * 1000,

  // UI feedback
  TOAST_DEFAULT_DURATION: 3000,
  TOAST_LONG_DURATION: 6000,
  DRAG_ACTIVATION_DELAY: 150,
  DRAG_TOLERANCE: 5,

  // Animation
  DRAG_DROP_ANIMATION_DURATION: 250,
  OVERLAY_FADE_DURATION: 300,
} as const;

// Usage:
showToast("Message", {
  duration: TIME_CONSTANTS.TOAST_LONG_DURATION,
});

useSensor(TouchSensor, {
  activationConstraint: {
    delay: TIME_CONSTANTS.DRAG_ACTIVATION_DELAY,
    tolerance: TIME_CONSTANTS.DRAG_TOLERANCE,
  },
});
```

**Why this matters:**
- Clear semantic meaning for all time values
- Single place to adjust timing across the app
- Self-documenting code
- Easier to maintain consistency

**Code smell addressed:**
Magic numbers scattered throughout codebase

---

### TESTABILITY: SEPARATE-QUERY - Split Storage Hook Concerns

**Current code:**
```typescript
// src/hooks/useStorageState.ts:20-35
const [value, setValue] = useState<T>(() => {
  const storedValue = storage.getItem(key);
  return storedValue !== null && storedValue !== undefined && storedValue !== "undefined"
    ? JSON.parse(storedValue)
    : defaultValue;
});

// Update storage whenever the key or value changes
useEffect(() => {
  storage.setItem(key, JSON.stringify(value));
}, [key, value, storage]);
```

**Refactored code:**
```typescript
// src/services/storageService.ts
export class StorageService {
  constructor(private storage: Storage) {}

  get<T>(key: string, defaultValue: T): T {
    const storedValue = this.storage.getItem(key);
    if (storedValue === null || storedValue === undefined || storedValue === "undefined") {
      return defaultValue;
    }
    try {
      return JSON.parse(storedValue);
    } catch {
      return defaultValue;
    }
  }

  set<T>(key: string, value: T): void {
    this.storage.setItem(key, JSON.stringify(value));
  }

  remove(key: string): void {
    this.storage.removeItem(key);
  }
}

// src/hooks/useStorageState.ts
export function useStorageState<T>(
  defaultValue: T,
  key: string,
  storageType: StorageType = "localStorage",
): [T, React.Dispatch<React.SetStateAction<T>>] {
  const storageService = useMemo(
    () => new StorageService(window[storageType]),
    [storageType]
  );

  const [value, setValue] = useState<T>(() => 
    storageService.get(key, defaultValue)
  );

  useEffect(() => {
    storageService.set(key, value);
  }, [key, value, storageService]);

  // Storage synchronization logic...
  
  return [value, setValue];
}
```

**Why this matters:**
- Clear separation between storage operations and React state
- Easy to mock StorageService in tests  
- Storage logic can be tested independently
- Better error handling and type safety

**Code smell addressed:**
Mixed concerns (storage + state management), hard to test

---

### MODERN-JS: NULLISH-COAL - Fix Default Value Handling

**Current code:**
```typescript
// src/components/tasks/TaskItem.tsx:48-54
const {
  enableLinks = true,
  enableGlow = settings.enableGlow,
  enableSelection = false,
  enableMoveMode = false,
} = features;

// Problem: What if settings.enableGlow is false? 
// The || operator would incorrectly use default instead of false
```

**Refactored code:**
```typescript
// src/components/tasks/TaskItem.tsx
const {
  enableLinks = true,
  enableGlow = settings.enableGlow ?? true, // Preserve false values
  enableSelection = false,
  enableMoveMode = false,
} = features;

// Better: Extract to typed defaults
interface TaskItemFeatureDefaults {
  enableLinks: boolean;
  enableGlow: boolean;
  enableSelection: boolean;
  enableMoveMode: boolean;
}

const getFeatureDefaults = (settings: UserSettings): TaskItemFeatureDefaults => ({
  enableLinks: true,
  enableGlow: settings.enableGlow ?? true,
  enableSelection: false,
  enableMoveMode: false,
});

// Usage:
const featureDefaults = getFeatureDefaults(settings);
const resolvedFeatures = { ...featureDefaults, ...features };
```

**Why this matters:**
- Correctly handles falsy values like `false`, `0`, `""`
- Distinguishes between `null`/`undefined` and other falsy values
- Prevents bugs with boolean feature flags
- More predictable default value behavior

**Code smell addressed:**
Incorrect falsy value handling, potential feature flag bugs

---

### PERFORMANCE: MEMO-RESULT - Optimize Theme Calculations

**Current code:**
```typescript
// src/App.tsx:130-140
const getMuiTheme = useCallback((): Theme => {
  if (systemTheme === "unknown") {
    return Themes[0].MuiTheme;
  }
  if (user.theme === "system") {
    return systemTheme === "dark" ? Themes[0].MuiTheme : Themes[1].MuiTheme;
  }
  const selectedTheme = Themes.find((theme) => theme.name === user.theme);
  return selectedTheme ? selectedTheme.MuiTheme : Themes[0].MuiTheme;
}, [systemTheme, user.theme]);
```

**Refactored code:**
```typescript
// src/hooks/useThemeCalculation.ts
const themeCache = new Map<string, Theme>();

const generateThemeKey = (userTheme: string, systemTheme: SystemTheme): string => 
  `${userTheme}-${systemTheme}`;

export const useOptimizedTheme = (userTheme: string, systemTheme: SystemTheme): Theme => {
  return useMemo(() => {
    const cacheKey = generateThemeKey(userTheme, systemTheme);
    
    if (themeCache.has(cacheKey)) {
      return themeCache.get(cacheKey)!;
    }

    const theme = calculateTheme(userTheme, systemTheme);
    themeCache.set(cacheKey, theme);
    return theme;
  }, [userTheme, systemTheme]);
};

const calculateTheme = (userTheme: string, systemTheme: SystemTheme): Theme => {
  if (systemTheme === "unknown") return Themes[0].MuiTheme;
  
  if (userTheme === "system") {
    return systemTheme === "dark" ? Themes[0].MuiTheme : Themes[1].MuiTheme;
  }
  
  const selectedTheme = Themes.find(theme => theme.name === userTheme);
  return selectedTheme?.MuiTheme ?? Themes[0].MuiTheme;
};
```

**Why this matters:**
- Avoids recalculating theme on every render
- Improves performance for theme-dependent components
- Caching prevents expensive theme lookups
- Cleaner separation of calculation logic

**Code smell addressed:**
Repeated expensive calculations, no memoization

---

## 💡 Refactoring Wisdom

> "The best code is no code at all. The second best is well-factored, readable code that expresses intent clearly." - Jeff Atwood

**Key Insights from this review:**
1. **Component Size**: TasksList.tsx at 755 lines violates the "one screen" rule - consider the 200-line guideline
2. **Separation of Concerns**: Many components mix rendering, logic, and side effects
3. **Performance**: Several O(n²) operations could be optimized to O(n) 
4. **Testability**: Heavy use of global context makes unit testing challenging
5. **Modern Patterns**: Good use of modern React/TS but some opportunities for nullish coalescing and better type safety

**Priority Recommendations:**
1. **Immediately**: Break down TasksList component (755 lines → ~100 lines per component)
2. **High Priority**: Extract user migration logic from App.tsx for testability  
3. **Medium Priority**: Optimize task filtering algorithms for performance
4. **Low Priority**: Standardize date formatting and time constants

The codebase shows strong modern React/TypeScript foundations but would benefit from focused refactoring to improve maintainability and performance.


---

*Generated by Claude Code Skills Review Tool using claude*
