# state-immutable-updates

> Use spread, map, filter, and concat for immutable state updates

## Why It Matters

Mutating methods like `splice`, `sort`, `reverse`, and direct index assignment modify arrays and objects in place without creating a new reference. React compares state by reference identity — if the reference has not changed, it assumes the data has not changed and skips the re-render. The UI silently falls out of sync with the actual data.

Immutable update patterns — spread syntax, `map`, `filter`, `concat`, and `slice` — always produce new references. React detects the change and re-renders the component. These patterns are also safer in concurrent rendering, where React may read state at different points in time.

## Bad

```tsx
function TaskBoard() {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);

  function removeTask(id: string) {
    // splice mutates the original array
    const index = tasks.findIndex((t) => t.id === id);
    tasks.splice(index, 1);
    setTasks(tasks); // Same reference — no re-render
  }

  function updateTitle(id: string, title: string) {
    // Direct property assignment mutates the object in place
    const task = tasks.find((t) => t.id === id);
    if (task) {
      task.title = title;
      setTasks([...tasks]); // Shallow copy hides the mutation but causes subtle bugs
    }
  }

  function sortByPriority() {
    // sort mutates the original array
    tasks.sort((a, b) => a.priority - b.priority);
    setTasks(tasks);
  }
}
```

## Good

```tsx
function TaskBoard() {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);

  function removeTask(id: string) {
    // filter returns a new array without the removed item
    setTasks((prev) => prev.filter((t) => t.id !== id));
  }

  function updateTitle(id: string, title: string) {
    // map returns a new array with a new object for the updated task
    setTasks((prev) =>
      prev.map((t) => (t.id === id ? { ...t, title } : t))
    );
  }

  function sortByPriority() {
    // Spread into a new array, then sort the copy
    setTasks((prev) => [...prev].sort((a, b) => a.priority - b.priority));
  }

  function addTask(task: Task) {
    // Spread to append
    setTasks((prev) => [...prev, task]);
  }

  function insertAtIndex(index: number, task: Task) {
    // Slice and spread to insert at a specific position
    setTasks((prev) => [
      ...prev.slice(0, index),
      task,
      ...prev.slice(index),
    ]);
  }
}
```

## See Also

- [state-never-mutate](state-never-mutate.md) - Never mutate state objects or arrays directly
