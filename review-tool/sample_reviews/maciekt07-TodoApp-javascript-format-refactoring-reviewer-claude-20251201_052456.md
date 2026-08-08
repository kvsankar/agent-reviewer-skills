# javascript-format-refactoring-reviewer Review

**Repository:** https://github.com/maciekt07/TodoApp
**Review Date:** 2025-12-01 05:24:56
**Reviewer:** javascript-format-refactoring-reviewer
**AI Provider:** claude

---

Now I have a good understanding of the codebase. Let me create a comprehensive review focusing on format refactoring opportunities.

## JavaScript Format Refactoring Review: TodoApp

### ✅ Well-Structured Code
- **JS-TEMPLATE-LONG**: Good use of multi-line template literals in `showToast.tsx` for readable content
- **JS-OBJ-LONG**: Proper multi-line object formatting in most configuration objects like `.prettierrc`
- **JS-PARAMS-DEFAULT**: Good use of default parameters in many components like `CustomEmojiPicker`

### 🔧 Refactoring Opportunities

#### max-len: JS-LONG-FUNC-PARAMS - Extract Parameter Object

**ESLint would say:**
> "Line exceeds 100 characters (max-len)", "Function has too many parameters (max-params)"

**Root cause:**
TaskItem component in `src/components/tasks/TaskItem.tsx:56-63` has complex parameter structure that makes the function signature hard to read and maintain.

**Current code:**
```typescript
export const TaskItem = memo(
  ({
    task,
    features = {},
    selection,
    onContextMenu,
    actions,
    blur,
    textHighlighter = (text) => text,
  }: TaskItemProps & { draggingId?: string; draggingHeight?: number }) => {
```

**Refactored code:**
```typescript
interface TaskItemConfig {
  task: Task;
  features?: {
    enableLinks?: boolean;
    enableGlow?: boolean;
    enableSelection?: boolean;
    enableMoveMode?: boolean;
  };
  selection?: {
    selectedIds?: UUID[];
    onSelect?: (taskId: UUID) => void;
    onDeselect?: (taskId: UUID) => void;
  };
  handlers?: {
    onContextMenu?: (e: React.MouseEvent<Element>) => void;
    textHighlighter?: (text: string) => React.ReactNode;
  };
  display?: {
    actions?: React.ReactNode;
    blur?: boolean;
  };
  dnd?: {
    draggingId?: string;
    draggingHeight?: number;
  };
}

export const TaskItem = memo(({
  task,
  features = {},
  selection,
  handlers = {},
  display = {},
  dnd = {}
}: TaskItemConfig) => {
  const { onContextMenu, textHighlighter = (text) => text } = handlers;
  const { actions, blur } = display;
  // Implementation
});
```

**Why this is better:**
- Parameter groups are logically organized
- Self-documenting parameter names
- Easy to add new options within groups
- Reduces line length naturally

**Refactoring applied:**
Introduce Parameter Object with logical grouping

---

#### max-len: JS-COMPLEX-CONDITION - Extract Predicate Functions

**ESLint would say:**
> "Line exceeds 100 characters (max-len)", "Function has too much complexity (complexity)"

**Root cause:**
Complex boolean expressions in `src/components/tasks/TasksList.tsx:300-350` for task filtering and checking.

**Current code:**
```typescript
const overdueTasks = tasks.filter(
  (task) => task.deadline && new Date() > new Date(task.deadline) && !task.done,
);

if (overdueTasks.length > 0) {
  // Complex toast logic with multiple conditions
}
```

**Refactored code:**
```typescript
function isOverdueTask(task: Task): boolean {
  return task.deadline && new Date() > new Date(task.deadline) && !task.done;
}

function hasDeadline(task: Task): boolean {
  return Boolean(task.deadline);
}

function isPastDeadline(task: Task): boolean {
  return hasDeadline(task) && new Date() > new Date(task.deadline);
}

function isIncomplete(task: Task): boolean {
  return !task.done;
}

function isOverdueTask(task: Task): boolean {
  return hasDeadline(task) && isPastDeadline(task) && isIncomplete(task);
}

const overdueTasks = tasks.filter(isOverdueTask);
```

**Why this is better:**
- Each condition has a descriptive name
- Business logic is self-documenting
- Easy to test individual predicates
- Complexity distributed across smaller functions

**Refactoring applied:**
Extract Predicate Function

---

#### max-len: JS-JSX-LONG - Extract JSX Components

**ESLint would say:**
> "Line exceeds 100 characters (max-len)", "JSX is nested too deeply (react/jsx-max-depth)"

**Root cause:**
Complex JSX structure in `src/components/tasks/TaskItem.tsx:130-240` creates deeply nested components that are hard to read.

**Current code:**
```jsx
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
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          handleSelectChange(task.id);
        }
      }}
      tabIndex={0}
      role="checkbox"
      aria-checked={isSelected}
    />
  )}
  {/* More nested JSX... */}
</TaskContainer>
```

**Refactored code:**
```jsx
function TaskItem({ task, features, selection, handlers, display }: TaskItemConfig) {
  return (
    <TaskContainer {...getTaskContainerProps(task, features, handlers, dnd)}>
      <TaskControls 
        task={task} 
        features={features} 
        selection={selection}
        onSelectionChange={handleSelectChange}
      />
      <TaskContent 
        task={task} 
        textHighlighter={textHighlighter} 
        features={features}
      />
      <TaskActions actions={actions} />
    </TaskContainer>
  );
}

function TaskControls({ task, features, selection, onSelectionChange }) {
  return (
    <>
      <DragControl task={task} features={features} />
      <SelectionControl 
        task={task} 
        selection={selection} 
        onSelectionChange={onSelectionChange}
      />
    </>
  );
}

function DragControl({ task, features }) {
  const { enableMoveMode } = features;
  const { moveMode } = useContext(TaskContext);
  
  if (!enableMoveMode || !moveMode) return null;
  
  return (
    <DragHandle {...listeners}>
      <DragIndicatorRounded sx={{ mr: "4px", ml: "-8px" }} />
    </DragHandle>
  );
}

function SelectionControl({ task, selection, onSelectionChange }) {
  const { selectedIds = [] } = selection || {};
  
  if (!selection || selectedIds.length === 0) return null;
  
  const isSelected = selectedIds.includes(task.id);
  
  return (
    <StyledRadio
      clr={getFontColor(task.color)}
      checked={isSelected}
      icon={<RadioUnchecked />}
      checkedIcon={<RadioChecked />}
      onChange={() => onSelectionChange(task.id)}
      onKeyDown={handleSelectionKeyDown(onSelectionChange, task.id)}
      tabIndex={0}
      role="checkbox"
      aria-checked={isSelected}
    />
  );
}

function handleSelectionKeyDown(onSelectionChange: Function, taskId: UUID) {
  return (e: React.KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onSelectionChange(taskId);
    }
  };
}
```

**Why this is better:**
- Each component has single responsibility
- JSX nesting is reduced significantly
- Components are reusable and testable
- Logic is encapsulated in smaller functions

**Refactoring applied:**
Extract Component, Extract Event Handler

---

#### max-len: JS-LONG-TEMPLATE - Multi-line Template Literals

**ESLint would say:**
> "Line exceeds 100 characters (max-len)"

**Root cause:**
Long template literals in notification logic in `src/components/tasks/TasksList.tsx:330-340`.

**Current code:**
```javascript
showToast(
  <div translate="no" style={{ wordBreak: "break-word" }}>
    <b translate="yes">Overdue task{overdueTasks.length > 1 && "s"}: </b>
    {listFormat.format(taskNames)}
  </div>,
  {
    id: "overdue-tasks",
    type: "error",
    disableVibrate: true,
    preventDuplicate: true,
    visibleToasts: toasts,
    duration: 3400,
    icon: <RingAlarm animate sx={{ color: ColorPalette.red }} />,
    style: {
      borderColor: ColorPalette.red,
      boxShadow: user.settings.enableGlow ? `0 0 18px -8px ${ColorPalette.red}` : "none",
    },
  },
);
```

**Refactored code:**
```javascript
function createOverdueTaskMessage(overdueTasks: Task[], listFormat: Intl.ListFormat) {
  const taskNames = overdueTasks.map(task => task.name);
  const isPlural = overdueTasks.length > 1;
  
  return (
    <div translate="no" style={{ wordBreak: "break-word" }}>
      <b translate="yes">
        Overdue task{isPlural && "s"}: 
      </b>
      {listFormat.format(taskNames)}
    </div>
  );
}

function getOverdueToastOptions(user: User, toasts: Toast[]) {
  return {
    id: "overdue-tasks",
    type: "error" as const,
    disableVibrate: true,
    preventDuplicate: true,
    visibleToasts: toasts,
    duration: 3400,
    icon: <RingAlarm animate sx={{ color: ColorPalette.red }} />,
    style: {
      borderColor: ColorPalette.red,
      boxShadow: user.settings.enableGlow 
        ? `0 0 18px -8px ${ColorPalette.red}` 
        : "none",
    },
  };
}

// Usage:
showToast(
  createOverdueTaskMessage(overdueTasks, listFormat),
  getOverdueToastOptions(user, toasts)
);
```

**Why this is better:**
- Message creation logic is extracted and testable
- Toast options are in a separate function
- Each function has a single responsibility
- No line length issues

**Refactoring applied:**
Extract Function for Template Creation

---

#### complexity: JS-COMPLEX-FUNC - Extract Functions to Reduce Complexity

**ESLint would say:**
> "Function has too much complexity (complexity)", "Function has too many statements (max-statements)"

**Root cause:**
The `showToast` function in `src/utils/showToast.tsx:82-150` handles multiple concerns including duplicate prevention, vibration, type configuration, and toast display.

**Current code:**
```typescript
export const showToast = (
  message: Renderable,
  {
    type = "success",
    disableClickDismiss,
    disableVibrate,
    dismissButton,
    preventDuplicate,
    visibleToasts,
    ...toastOptions
  }: ToastProps = {} as ToastProps,
): void => {
  // Prevent showing duplicate of toasts if enabled
  if (preventDuplicate) {
    if (!toastOptions.id || !visibleToasts) {
      throw new Error("[Toast] `preventDuplicate: true` requires both `id` and `visibleToasts`.");
    }
    const alreadyVisible = visibleToasts.some((t) => t.id === toastOptions.id && t.visible);
    if (alreadyVisible) {
      const elem = document.getElementById(toastOptions.id);
      if (elem) {
        applyBounce(elem);
      }
      return;
    }
  }

  // Complex logic continues...
};
```

**Refactored code:**
```typescript
function validateDuplicatePreventionProps(preventDuplicate: boolean, id?: string, visibleToasts?: Toast[]): void {
  if (preventDuplicate && (!id || !visibleToasts)) {
    throw new Error("[Toast] `preventDuplicate: true` requires both `id` and `visibleToasts`.");
  }
}

function handleDuplicatePrevention(id: string, visibleToasts: Toast[]): boolean {
  const alreadyVisible = visibleToasts.some(t => t.id === id && t.visible);
  
  if (alreadyVisible) {
    const element = document.getElementById(id);
    if (element) {
      applyBounce(element);
    }
    return true; // Toast was duplicate and handled
  }
  
  return false; // Not a duplicate, continue
}

function handleDeviceVibration(type: ExtendedToastType, disableVibrate: boolean): void {
  if (disableVibrate || !('vibrate' in navigator)) return;
  
  const vibrationPattern = type === "error" ? [100, 50, 100] : [100];
  
  try {
    navigator.vibrate(vibrationPattern);
  } catch (err) {
    console.error(err);
  }
}

function configureCustomToastType(type: ExtendedToastType, toastOptions: ToastOptions): ToastOptions {
  if (!(type in customTypeConfig)) return toastOptions;
  
  const { icon, borderColor } = customTypeConfig[type as CustomToastType];
  
  return {
    ...toastOptions,
    icon,
    style: {
      ...toastOptions.style,
      borderColor,
    },
  };
}

function selectToastFunction(type: ExtendedToastType) {
  return {
    error: toast.error,
    success: toast.success,
    loading: toast.loading,
    custom: toast.custom,
    blank: toast,
    warning: toast,
    info: toast,
  }[type];
}

export const showToast = (
  message: Renderable,
  {
    type = "success",
    disableClickDismiss,
    disableVibrate,
    dismissButton,
    preventDuplicate,
    visibleToasts,
    ...toastOptions
  }: ToastProps = {} as ToastProps,
): void => {
  if (preventDuplicate) {
    validateDuplicatePreventionProps(preventDuplicate, toastOptions.id, visibleToasts);
    
    const isDuplicate = handleDuplicatePrevention(toastOptions.id!, visibleToasts!);
    if (isDuplicate) return;
  }

  handleDeviceVibration(type, disableVibrate);
  
  const configuredOptions = configureCustomToastType(type, toastOptions);
  const toastFunction = selectToastFunction(type);

  toastFunction(
    createToastContent(message, disableClickDismiss, dismissButton),
    configuredOptions
  );
};

function createToastContent(
  message: Renderable, 
  disableClickDismiss: boolean, 
  dismissButton: boolean
) {
  return (t: Toast) => (
    <div onClick={getClickHandler(disableClickDismiss, dismissButton, t.id)}>
      {message}
      {dismissButton && <DismissButton onDismiss={() => toast.dismiss(t.id)} />}
    </div>
  );
}

function getClickHandler(disableClickDismiss: boolean, dismissButton: boolean, toastId: string) {
  return !disableClickDismiss && !dismissButton 
    ? () => toast.dismiss(toastId) 
    : undefined;
}

function DismissButton({ onDismiss }: { onDismiss: () => void }) {
  return (
    <div>
      <Button
        variant="outlined"
        fullWidth
        onClick={onDismiss}
        sx={{ 
          mt: "8px", 
          w: "100%", 
          p: "12px 24px", 
          fontSize: "16px", 
          borderRadius: "16px" 
        }}
      >
        Dismiss
      </Button>
    </div>
  );
}
```

**Why this is better:**
- Each function has single responsibility
- Main function reads like documentation
- Easy to test individual behaviors
- Complexity distributed across smaller functions
- No complexity warnings

**Refactoring applied:**
Extract Function, Decompose Complex Function

---

#### object-curly-newline: JS-OBJ-LONG - Multi-line Objects

**ESLint would say:**
> "Object literal should have line breaks (object-curly-newline)"

**Root cause:**
Style object in `src/components/TopBar.tsx:30-38` has multiple properties on complex lines.

**Current code:**
```typescript
<Toolbar
  sx={{
    position: "relative",
    m: "0 !important",
    p: "0 !important",
    minHeight: "0 !important",
  }}
>
```

**Refactored code:**
```typescript
const toolbarStyles = {
  position: "relative",
  margin: "0 !important",
  padding: "0 !important", 
  minHeight: "0 !important",
} as const;

const titleStyles = {
  position: "absolute",
  left: "50%",
  transform: "translateX(-50%)",
  fontWeight: 600,
  color: getFontColor(theme.secondary),
} as const;

<Toolbar sx={toolbarStyles}>
  <IconButton
    size="large"
    edge="start" 
    color="inherit"
    aria-label="menu"
    sx={{ 
      ml: 2, 
      color: getFontColor(theme.secondary) 
    }}
    onClick={() => n("/")}
  >
    <ArrowBackIosNewRounded />
  </IconButton>
  <Typography
    variant="h5"
    component="div"
    sx={titleStyles}
  >
    {title}
  </Typography>
</Toolbar>
```

**Why this is better:**
- Style objects are reusable
- JSX is cleaner and more readable
- Styles are easier to maintain
- Better separation of concerns

**Refactoring applied:**
Extract Style Object

---

#### max-len: JS-SPREAD-LONG - Multi-line Spreads

**ESLint would say:**
> "Line exceeds 100 characters (max-len)"

**Root cause:**
Complex spread operations in `src/components/ColorPicker.tsx:180-200` for grid and popover configuration.

**Current code:**
```typescript
const counts: { [categoryId: UUID]: number } = {};
uniqueCategories.forEach((category) => {
  const categoryTasks = tasks.filter((task) =>
    task.category?.some((cat) => cat.id === category.id),
  );
  counts[category.id] = categoryTasks.length;
});
```

**Refactored code:**
```typescript
function calculateCategoryCounts(
  categories: Category[], 
  tasks: Task[]
): Record<UUID, number> {
  return categories.reduce((counts, category) => {
    const categoryTaskCount = countTasksForCategory(tasks, category);
    return {
      ...counts,
      [category.id]: categoryTaskCount,
    };
  }, {});
}

function countTasksForCategory(tasks: Task[], category: Category): number {
  return tasks.filter(task => 
    task.category?.some(cat => cat.id === category.id)
  ).length;
}

function sortCategoriesByCountAndName(
  categories: Category[], 
  counts: Record<UUID, number>
): Category[] {
  return [...categories].sort((a, b) => {
    const countComparison = compareByCount(counts, a, b);
    return countComparison !== 0 
      ? countComparison 
      : compareByName(a, b);
  });
}

function compareByCount(
  counts: Record<UUID, number>, 
  categoryA: Category, 
  categoryB: Category
): number {
  const countA = counts[categoryA.id] || 0;
  const countB = counts[categoryB.id] || 0;
  return countB - countA; // Descending order
}

function compareByName(categoryA: Category, categoryB: Category): number {
  return (categoryA.name || "").localeCompare(categoryB.name || "");
}

// Usage:
const counts = calculateCategoryCounts(uniqueCategories, tasks);
const sortedCategories = sortCategoriesByCountAndName(uniqueCategories, counts);
```

**Why this is better:**
- Complex logic is broken into named functions
- Each function has a single responsibility
- Easy to test individual sorting criteria
- Business logic is self-documenting

**Refactoring applied:**
Extract Function, Decompose Complex Sorting Logic

---

### 💡 Refactoring Wisdom
> "Don't fight ESLint—refactor so it has nothing to complain about. Complex code hiding behind long lines usually indicates deeper structural issues that deserve attention."

The TodoApp shows many good practices but has opportunities for extracting components and functions to make the code more maintainable. The most impactful changes would be:

1. **TaskItem component decomposition** - Breaking down the complex JSX into smaller, focused components
2. **showToast function simplification** - Extracting multiple concerns into separate functions  
3. **Predicate function extraction** - Making complex boolean logic more readable and testable
4. **Style object extraction** - Moving inline styles to reusable objects
5. **Parameter object introduction** - Simplifying complex function signatures

These refactorings would naturally resolve ESLint formatting warnings while making the code more maintainable and testable.


---

*Generated by Claude Code Skills Review Tool using claude*
