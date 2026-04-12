# state-derive-inline

> Compute derived values inline instead of storing them in state

## Why It Matters

When you store a value in state that can be computed from other state, you create two sources of truth that must be kept in sync. Every time the source state changes, you must remember to update the derived state as well. Forgetting a single sync point causes the UI to display stale or contradictory data.

Computing derived values inline during render guarantees they are always consistent with the current state. The computation runs on every render, but for most cases this is negligible. If profiling reveals the computation is expensive, reach for `useMemo` — but start with the simple inline approach.

## Bad

```tsx
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");
  // Derived state stored separately — must be manually synced
  const [filteredTodos, setFilteredTodos] = useState<Todo[]>([]);
  const [activeCount, setActiveCount] = useState(0);

  useEffect(() => {
    const result = todos.filter((t) =>
      filter === "all" ? true : filter === "active" ? !t.done : t.done
    );
    setFilteredTodos(result);
    setActiveCount(todos.filter((t) => !t.done).length);
  }, [todos, filter]); // Forgetting a dependency here causes stale data
}
```

## Good

```tsx
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

  // Derived inline — always in sync, no extra state or effects
  const filteredTodos = todos.filter((t) =>
    filter === "all" ? true : filter === "active" ? !t.done : t.done
  );
  const activeCount = todos.filter((t) => !t.done).length;

  return (
    <>
      <p>{activeCount} items left</p>
      <FilterBar current={filter} onChange={setFilter} />
      {filteredTodos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </>
  );
}
```

## See Also

- [state-local-simple](state-local-simple.md) - Use useState for simple isolated state
