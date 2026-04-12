# anti-tight-coupling

> Avoid tight coupling between components via shared mutable state

## Why It Matters

Shared mutable state creates invisible dependencies between components. When two sibling components both read and write the same mutable object, changing one component's writes silently breaks the other's reads. There is no compiler warning, no type error, and no prop-drilling to trace — the dependency is hidden.

Lifting state to a common parent or using a store with selectors makes the data flow explicit. Each component receives only what it needs, updates are predictable, and dependencies are visible in the component's props or selector declarations.

## Bad

```tsx
// Shared mutable object — invisible coupling between siblings
const sharedState = {
  selectedIds: new Set<string>(),
  lastAction: "",
};

function SelectionList({ items }: { items: Item[] }) {
  const [, forceUpdate] = useState(0);

  function handleToggle(id: string) {
    // Mutating shared object directly
    if (sharedState.selectedIds.has(id)) {
      sharedState.selectedIds.delete(id);
    } else {
      sharedState.selectedIds.add(id);
    }
    sharedState.lastAction = `toggled ${id}`;
    forceUpdate((n) => n + 1);
  }

  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <input
            type="checkbox"
            checked={sharedState.selectedIds.has(item.id)}
            onChange={() => handleToggle(item.id)}
          />
          {item.name}
        </li>
      ))}
    </ul>
  );
}

// This sibling reads sharedState but has no way to know when it changes
function SelectionSummary() {
  // Stale — never re-renders when SelectionList mutates sharedState
  return <p>{sharedState.selectedIds.size} items selected</p>;
}
```

## Good

```tsx
// State lifted to parent — data flow is explicit and reactive
function SelectionPage({ items }: { items: Item[] }) {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  function handleToggle(id: string) {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  return (
    <div>
      <SelectionSummary count={selectedIds.size} />
      <SelectionList
        items={items}
        selectedIds={selectedIds}
        onToggle={handleToggle}
      />
    </div>
  );
}

function SelectionList({ items, selectedIds, onToggle }: SelectionListProps) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <input
            type="checkbox"
            checked={selectedIds.has(item.id)}
            onChange={() => onToggle(item.id)}
          />
          {item.name}
        </li>
      ))}
    </ul>
  );
}

function SelectionSummary({ count }: { count: number }) {
  return <p>{count} items selected</p>;
}
```

## See Also

- [state-never-mutate](state-never-mutate.md) - Never mutate state directly — always use the setter function
