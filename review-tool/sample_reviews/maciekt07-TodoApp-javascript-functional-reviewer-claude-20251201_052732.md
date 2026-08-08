# javascript-functional-reviewer Review

**Repository:** https://github.com/maciekt07/TodoApp
**Review Date:** 2025-12-01 05:27:32
**Reviewer:** javascript-functional-reviewer
**AI Provider:** claude

---

Now I have a comprehensive understanding of the codebase. This is a React TypeScript Todo application with multiple utilities, hooks, and components. Let me provide a detailed functional programming review focusing on the key areas where functional principles can be applied.

## Review: TodoApp - Functional JavaScript Analysis

### ✅ Strengths

- **ARR-MAP**: Good use of `map()` for transforming arrays throughout the codebase (e.g., tasks, categories)
- **USE-CONST**: Consistent use of `const` for immutable bindings across utility functions
- **ARROW-SIMPLE**: Clean arrow functions used appropriately for callbacks and simple transformations
- **DESTRUCTURE**: Excellent use of destructuring in function parameters and React component props
- **PURE-FUNC**: Several utility functions like `isHexColor`, `isSameDay`, and `formatTime` are properly pure
- **SPREAD-COPY**: Good use of spread operator for immutable updates in React state management

### ⚠️ Suggestions

#### PURE-FUNC: Function relies on external mutable state

**Current code:** `src/utils/getRandomGreeting.ts:1-6`
```javascript
const recentGreetings: Set<number> = new Set();
export const maxRecentGreetings = 8; // Number of recent greetings to track

const getUniqueGreeting = (): string => {
  let randomIndex: number;
  do {
    randomIndex = Math.floor(Math.random() * greetingsText.length);
  } while (recentGreetings.has(randomIndex));

  // Update recent greetings
  recentGreetings.add(randomIndex);
  if (recentGreetings.size > maxRecentGreetings) {
    const firstEntry = Array.from(recentGreetings).shift();
    if (firstEntry !== undefined) {
      recentGreetings.delete(firstEntry);
    }
  }

  return greetingsText[randomIndex];
};
```

**Suggested refactoring:**
```javascript
interface GreetingState {
  recentGreetings: Set<number>;
  maxRecentGreetings: number;
}

const createGreetingGenerator = (maxRecentGreetings = 8) => {
  let state: GreetingState = {
    recentGreetings: new Set(),
    maxRecentGreetings
  };

  return {
    getUniqueGreeting: (): string => {
      let randomIndex: number;
      do {
        randomIndex = Math.floor(Math.random() * greetingsText.length);
      } while (state.recentGreetings.has(randomIndex));

      state = updateRecentGreetings(state, randomIndex);
      return greetingsText[randomIndex];
    },
    reset: () => {
      state = { ...state, recentGreetings: new Set() };
    }
  };
};

const updateRecentGreetings = (state: GreetingState, newIndex: number): GreetingState => {
  const newRecentGreetings = new Set(state.recentGreetings);
  newRecentGreetings.add(newIndex);
  
  if (newRecentGreetings.size > state.maxRecentGreetings) {
    const firstEntry = Array.from(newRecentGreetings).shift();
    if (firstEntry !== undefined) {
      newRecentGreetings.delete(firstEntry);
    }
  }

  return { ...state, recentGreetings: newRecentGreetings };
};

// Export instance
const greetingGenerator = createGreetingGenerator();
export const getRandomGreeting = greetingGenerator.getUniqueGreeting;
```

**Why this matters:**
Encapsulating mutable state makes the function more testable, predictable, and allows multiple independent greeting generators if needed. The current approach uses global state which makes testing and reuse difficult.

**FP principle:**
Encapsulate side effects and mutable state within controlled boundaries, making state transitions explicit and predictable.

---

#### NO-SIDE-EFFECT: Function performs side effects without clear boundaries

**Current code:** `src/utils/exportTasks.ts:8-22`
```javascript
export const exportTasksToJson = (selectedTasks: Task[]): void => {
  // Get the current date and time for the filename
  const timestamp = new Date().toLocaleString().replace(/[/:, ]/g, "_");
  const filename = `Tasks_${timestamp}.json`;

  // Create a JSON blob
  const dataStr = JSON.stringify(selectedTasks, null, 2);
  const blob = new Blob([dataStr], { type: "application/json" });

  // Create a URL for the blob
  const url = window.URL.createObjectURL(blob);

  // Create a link element and initiate the download
  const linkElement = document.createElement("a");
  linkElement.href = url;
  linkElement.download = filename;
  linkElement.click();
  // Clean up the URL object
  window.URL.revokeObjectURL(url);
};
```

**Suggested refactoring:**
```javascript
// Pure function to prepare export data
const prepareTasksForExport = (tasks: Task[], timestamp = new Date()): {
  data: string;
  filename: string;
} => {
  const formattedTimestamp = timestamp.toLocaleString().replace(/[/:, ]/g, "_");
  const filename = `Tasks_${formattedTimestamp}.json`;
  const data = JSON.stringify(tasks, null, 2);
  
  return { data, filename };
};

// Pure function to create blob
const createExportBlob = (data: string): Blob => 
  new Blob([data], { type: "application/json" });

// Side effect function clearly separated
const downloadBlob = (blob: Blob, filename: string): void => {
  const url = window.URL.createObjectURL(blob);
  const linkElement = document.createElement("a");
  linkElement.href = url;
  linkElement.download = filename;
  linkElement.click();
  window.URL.revokeObjectURL(url);
};

// Composed function with clear side effect boundary
export const exportTasksToJson = (selectedTasks: Task[]): void => {
  const { data, filename } = prepareTasksForExport(selectedTasks);
  const blob = createExportBlob(data);
  downloadBlob(blob, filename);
};
```

**Why this matters:**
Separating pure data preparation from side effects makes the code more testable, reusable, and easier to reason about. Each function has a single responsibility and can be tested independently.

**FP principle:**
Isolate side effects at the boundaries of your application. Keep pure logic separate from I/O operations.

---

#### IMMUT-COPY: Complex object mutations in array processing

**Current code:** `src/utils/syncUtils.ts:60-95`
```javascript
function mergeTasks(
  localTasks: Task[],
  remoteTasks: Task[],
  localDeleted: UUID[],
  remoteDeleted: UUID[],
  localDeletedCategories: UUID[],
  remoteDeletedCategories: UUID[],
): Task[] {
  const mergedTasks = new Map<UUID, Task>();
  const allDeletedTasks = new Set([...localDeleted, ...remoteDeleted]);
  const allDeletedCategories = new Set([...localDeletedCategories, ...remoteDeletedCategories]);
  const taskOrder = new Map<UUID, number>();

  // process tasks in creation date order to establish base ordering
  const processedTasks = [...localTasks, ...remoteTasks]
    .filter((task) => !allDeletedTasks.has(task.id))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map((task: Task) => {
      // clean up task categories, removing any references to deleted categories
      if (task.category) {
        const filteredCategories = task.category.filter(
          (cat: Category) => !allDeletedCategories.has(cat.id),
        );
        if (filteredCategories.length === 0) {
          return { ...task, category: undefined };
        }
        return { ...task, category: filteredCategories };
      }
      return task;
    });

  processedTasks.forEach((task: Task, index: number) => {
    const existingTask = mergedTasks.get(task.id);
    if (!existingTask) {
      mergedTasks.set(task.id, task);
      taskOrder.set(task.id, index);
    } else {
      // if task exists use the one with latest lastSave
      const existingDate = existingTask.lastSave ? new Date(existingTask.lastSave) : new Date(0);
      const newDate = task.lastSave ? new Date(task.lastSave) : new Date(0);

      if (newDate > existingDate) {
        mergedTasks.set(task.id, task);
      }
    }
  });

  // convert to array and sort by creation date and then by task order
  return Array.from(mergedTasks.values()).sort((a, b) => {
    const dateA = new Date(a.date).getTime();
    const dateB = new Date(b.date).getTime();
    if (dateA === dateB) {
      const orderA = taskOrder.get(a.id) ?? Number.MAX_SAFE_INTEGER;
      const orderB = taskOrder.get(b.id) ?? Number.MAX_SAFE_INTEGER;
      return orderA - orderB;
    }
    return dateA - dateB;
  });
}
```

**Suggested refactoring:**
```javascript
// Helper functions for better composition
const createDeletedSets = (localDeleted: UUID[], remoteDeleted: UUID[]) => ({
  allDeletedTasks: new Set([...localDeleted, ...remoteDeleted]),
  allDeletedCategories: new Set([...localDeletedCategories, ...remoteDeletedCategories])
});

const cleanTaskCategories = (task: Task, deletedCategories: Set<UUID>): Task => {
  if (!task.category) return task;
  
  const filteredCategories = task.category.filter(
    (cat: Category) => !deletedCategories.has(cat.id)
  );
  
  return filteredCategories.length === 0 
    ? { ...task, category: undefined }
    : { ...task, category: filteredCategories };
};

const processTasksArray = (
  tasks: Task[], 
  deletedTasks: Set<UUID>, 
  deletedCategories: Set<UUID>
): Task[] => 
  tasks
    .filter(task => !deletedTasks.has(task.id))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map(task => cleanTaskCategories(task, deletedCategories));

const mergeTasksWithConflictResolution = (tasks: Task[]): Map<UUID, Task> =>
  tasks.reduce((mergedTasks, task, index) => {
    const existing = mergedTasks.get(task.id);
    
    if (!existing) {
      return new Map(mergedTasks).set(task.id, { ...task, _orderIndex: index });
    }
    
    const existingDate = existing.lastSave ? new Date(existing.lastSave) : new Date(0);
    const newDate = task.lastSave ? new Date(task.lastSave) : new Date(0);
    
    if (newDate > existingDate) {
      return new Map(mergedTasks).set(task.id, { ...task, _orderIndex: index });
    }
    
    return mergedTasks;
  }, new Map<UUID, Task>());

const sortMergedTasks = (mergedTasks: Map<UUID, Task>): Task[] =>
  Array.from(mergedTasks.values())
    .sort((a, b) => {
      const dateA = new Date(a.date).getTime();
      const dateB = new Date(b.date).getTime();
      
      if (dateA === dateB) {
        const orderA = a._orderIndex ?? Number.MAX_SAFE_INTEGER;
        const orderB = b._orderIndex ?? Number.MAX_SAFE_INTEGER;
        return orderA - orderB;
      }
      
      return dateA - dateB;
    })
    .map(({ _orderIndex, ...task }) => task); // Remove helper property

function mergeTasks(
  localTasks: Task[],
  remoteTasks: Task[],
  localDeleted: UUID[],
  remoteDeleted: UUID[],
  localDeletedCategories: UUID[],
  remoteDeletedCategories: UUID[],
): Task[] {
  const { allDeletedTasks, allDeletedCategories } = createDeletedSets(
    localDeleted, 
    remoteDeleted
  );
  
  const processedTasks = processTasksArray(
    [...localTasks, ...remoteTasks],
    allDeletedTasks,
    allDeletedCategories
  );
  
  const mergedTasksMap = mergeTasksWithConflictResolution(processedTasks);
  
  return sortMergedTasks(mergedTasksMap);
}
```

**Why this matters:**
Breaking down complex operations into smaller, pure functions makes the code easier to test, debug, and understand. Each function has a single responsibility and can be composed to create the final behavior.

**FP principle:**
Compose complex operations from simple, pure functions. Each function should do one thing well and be easily testable in isolation.

---

#### ARR-REDUCE: Using imperative loop instead of functional reduce

**Current code:** `src/utils/syncUtils.ts:244-264`
```javascript
processedTasks.forEach((task: Task, index: number) => {
  const existingTask = mergedTasks.get(task.id);
  if (!existingTask) {
    mergedTasks.set(task.id, task);
    taskOrder.set(task.id, index);
  } else {
    // if task exists use the one with latest lastSave
    const existingDate = existingTask.lastSave ? new Date(existingTask.lastSave) : new Date(0);
    const newDate = task.lastSave ? new Date(task.lastSave) : new Date(0);

    if (newDate > existingDate) {
      mergedTasks.set(task.id, task);
    }
  }
});
```

**Suggested refactoring:**
```javascript
const mergedTasks = processedTasks.reduce((acc, task, index) => {
  const existing = acc.get(task.id);
  
  if (!existing) {
    return new Map(acc).set(task.id, { ...task, _orderIndex: index });
  }
  
  const existingDate = existing.lastSave ? new Date(existing.lastSave) : new Date(0);
  const newDate = task.lastSave ? new Date(task.lastSave) : new Date(0);
  
  if (newDate > existingDate) {
    return new Map(acc).set(task.id, { ...task, _orderIndex: index });
  }
  
  return acc;
}, new Map<UUID, Task>());
```

**Why this matters:**
Using `reduce` instead of `forEach` with mutations makes the operation more declarative and functional. It clearly expresses that we're accumulating values into a new data structure.

**FP principle:**
Prefer `reduce` for accumulation operations over imperative loops with mutations. It makes the data transformation intent clearer.

---

#### COMPOSE-FUNC: Complex time formatting logic should be decomposed

**Current code:** `src/utils/timeUtils.ts:44-63`
```javascript
export const formatDate = (input: Date): string => {
  const today = new Date();
  const date = new Date(input);
  const rtf = new Intl.RelativeTimeFormat(getLocale(), { numeric: "auto" });

  if (isSameDay(today, date)) {
    return `${rtf.format(0, "day")} ${formatTime(date)}`;
  }

  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  if (isSameDay(yesterday, date)) {
    return `${rtf.format(-1, "day")} ${formatTime(date)}`;
  }

  const daysDiff = Math.floor((date.getTime() - today.getTime()) / MS_IN_DAY);

  if (daysDiff >= -6 && daysDiff <= 6) {
    return `${getDayOfWeek(date)} ${formatTime(date)}`;
  }

  return formatDateOnly(date);
};
```

**Suggested refactoring:**
```javascript
const createRelativeFormatter = (locale = getLocale()) =>
  new Intl.RelativeTimeFormat(locale, { numeric: "auto" });

const getYesterday = (today: Date): Date => {
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  return yesterday;
};

const calculateDayDifference = (date: Date, reference: Date): number =>
  Math.floor((date.getTime() - reference.getTime()) / MS_IN_DAY);

const isWithinWeek = (daysDiff: number): boolean =>
  daysDiff >= -6 && daysDiff <= 6;

const formatTodayDate = (date: Date, rtf: Intl.RelativeTimeFormat): string =>
  `${rtf.format(0, "day")} ${formatTime(date)}`;

const formatYesterdayDate = (date: Date, rtf: Intl.RelativeTimeFormat): string =>
  `${rtf.format(-1, "day")} ${formatTime(date)}`;

const formatWeekDate = (date: Date): string =>
  `${getDayOfWeek(date)} ${formatTime(date)}`;

export const formatDate = (input: Date): string => {
  const today = new Date();
  const date = new Date(input);
  const rtf = createRelativeFormatter();

  if (isSameDay(today, date)) {
    return formatTodayDate(date, rtf);
  }

  const yesterday = getYesterday(today);
  if (isSameDay(yesterday, date)) {
    return formatYesterdayDate(date, rtf);
  }

  const daysDiff = calculateDayDifference(date, today);
  
  if (isWithinWeek(daysDiff)) {
    return formatWeekDate(date);
  }

  return formatDateOnly(date);
};
```

**Why this matters:**
Breaking down complex logic into small, focused functions makes each piece easier to test, understand, and reuse. Each function has a clear, single responsibility.

**FP principle:**
Compose complex operations from simple, focused functions. Each function should do one thing well and have a descriptive name.

---

#### CURRY-PATTERN: Missed opportunity for currying in utility functions

**Current code:** `src/utils/colorUtils.ts:45-58`
```javascript
export const isDarkMode = (
  darkmode: DarkModeOptions,
  systemTheme: SystemTheme,
  backgroundColor: string,
): boolean => {
  switch (darkmode) {
    case "light":
      return false;
    case "dark":
      return true;
    case "system":
      return systemTheme === "dark";
    case "auto":
      return isDark(backgroundColor);
    default:
      return false;
  }
};
```

**Suggested refactoring:**
```javascript
// Curried version for better reusability
const createDarkModeChecker = (systemTheme: SystemTheme) => 
  (backgroundColor: string) => 
  (darkmode: DarkModeOptions): boolean => {
    switch (darkmode) {
      case "light":
        return false;
      case "dark":
        return true;
      case "system":
        return systemTheme === "dark";
      case "auto":
        return isDark(backgroundColor);
      default:
        return false;
    }
  };

// Specialized functions
export const createDarkModeCheckerForTheme = (systemTheme: SystemTheme, backgroundColor: string) =>
  createDarkModeChecker(systemTheme)(backgroundColor);

// Original function for backward compatibility
export const isDarkMode = (
  darkmode: DarkModeOptions,
  systemTheme: SystemTheme,
  backgroundColor: string,
): boolean => createDarkModeChecker(systemTheme)(backgroundColor)(darkmode);

// Usage examples:
// const checkDarkMode = createDarkModeCheckerForTheme(systemTheme, bgColor);
// const isUserInDarkMode = checkDarkMode('auto');
```

**Why this matters:**
Currying enables creating specialized functions for specific contexts, reducing the need to pass the same parameters repeatedly and making the code more reusable.

**FP principle:**
Use currying to create specialized functions from general ones, enabling partial application and better composition.

---

#### MEMOIZATION: Missing memoization for expensive operations

**Current code:** `src/utils/colorUtils.ts:12-36`
```javascript
export const getFontColor = (backgroundColor: string): string => {
  if (!isHexColor(backgroundColor)) {
    console.error("Invalid hex color:", backgroundColor);
    return ColorPalette.fontDark;
  }

  const hexColor = backgroundColor.startsWith("#") ? backgroundColor.slice(1) : backgroundColor;

  // If shorthand hex color (e.g., #fff), expand it to full form
  const expandedHex =
    hexColor.length === 3
      ? hexColor
          .split("")
          .map((char) => char + char)
          .join("")
      : hexColor;

  const red = parseInt(expandedHex.slice(0, 2), 16);
  const green = parseInt(expandedHex.slice(2, 4), 16);
  const blue = parseInt(expandedHex.slice(4, 6), 16);

  const brightness = Math.round((red * 299 + green * 587 + blue * 114) / 1000);

  const threshold = 128;
  return brightness > threshold ? ColorPalette.fontDark : ColorPalette.fontLight;
};
```

**Suggested refactoring:**
```javascript
const memoize = <T extends (...args: any[]) => any>(fn: T): T => {
  const cache = new Map();
  return ((...args: Parameters<T>) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
};

const calculateFontColorUncached = (backgroundColor: string): string => {
  if (!isHexColor(backgroundColor)) {
    console.error("Invalid hex color:", backgroundColor);
    return ColorPalette.fontDark;
  }

  const hexColor = backgroundColor.startsWith("#") ? backgroundColor.slice(1) : backgroundColor;

  // If shorthand hex color (e.g., #fff), expand it to full form
  const expandedHex = hexColor.length === 3
    ? hexColor.split("").map(char => char + char).join("")
    : hexColor;

  const [red, green, blue] = [
    parseInt(expandedHex.slice(0, 2), 16),
    parseInt(expandedHex.slice(2, 4), 16),
    parseInt(expandedHex.slice(4, 6), 16)
  ];

  const brightness = Math.round((red * 299 + green * 587 + blue * 114) / 1000);
  const threshold = 128;
  
  return brightness > threshold ? ColorPalette.fontDark : ColorPalette.fontLight;
};

// Memoized version for performance
export const getFontColor = memoize(calculateFontColorUncached);
```

**Why this matters:**
Color calculations may be performed frequently in UI updates. Memoization prevents recalculating the same color values repeatedly, improving performance.

**FP principle:**
Use memoization to cache results of expensive pure function calls, trading memory for computation time.

---

#### POINT-FREE: Unnecessary intermediate variables in array operations

**Current code:** `src/contexts/TaskProvider.tsx:75-84`
```javascript
const handleSelectTask = useCallback(
  (taskId: UUID) => {
    setAnchorEl(null);
    setMultipleSelectedTasks((prevSelectedTaskIds) => {
      if (prevSelectedTaskIds.includes(taskId)) {
        // Deselect the task if already selected
        return prevSelectedTaskIds.filter((id) => id !== taskId);
      } else {
        // Select the task if not selected
        return [...prevSelectedTaskIds, taskId];
      }
    });
  },
  [setMultipleSelectedTasks],
);
```

**Suggested refactoring:**
```javascript
const toggleTaskInArray = (taskId: UUID) => (tasks: UUID[]): UUID[] =>
  tasks.includes(taskId)
    ? tasks.filter(id => id !== taskId)
    : [...tasks, taskId];

const handleSelectTask = useCallback(
  (taskId: UUID) => {
    setAnchorEl(null);
    setMultipleSelectedTasks(toggleTaskInArray(taskId));
  },
  [setMultipleSelectedTasks],
);
```

**Why this matters:**
The functional approach separates the pure logic (toggling task selection) from the side effect (setting anchor element), making the code more testable and reusable.

**FP principle:**
Extract pure logic into separate functions, leaving only side effects in the imperative code. This makes the logic easier to test and reason about.

---

### 💡 Functional Programming Wisdom

> "Functional programming is about writing pure functions, about removing hidden inputs and outputs as far as we can, so that as much of our code as possible just describes a relationship between inputs and outputs."
> — Eric Elliott

The TodoApp shows good foundational understanding of functional principles with proper use of array methods, immutable updates, and React's functional patterns. The main areas for improvement involve better separation of pure logic from side effects, increased use of function composition, and strategic application of memoization for performance-critical operations.


---

*Generated by Claude Code Skills Review Tool using claude*
