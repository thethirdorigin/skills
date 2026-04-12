# hook-useEffect-deps

> Always include a dependency array in useEffect

## Why It Matters

A `useEffect` call without a dependency array runs after every single render. If the effect sets state, that state change triggers another render, which triggers the effect again — creating an infinite loop. Even without state setters, a missing dependency array causes unnecessary API calls, DOM mutations, and computation on every render.

Always pass a dependency array. Use `[]` for mount-only effects. Use `[dep1, dep2]` to re-run when specific values change. If you genuinely need to run on every render, add a comment explaining why — this is almost always a mistake.

## Bad

```tsx
function UserList() {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    // Runs after EVERY render — infinite loop: fetch -> setUsers -> render -> fetch
    fetch("/api/users")
      .then((res) => res.json())
      .then(setUsers);
  });

  return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

## Good

```tsx
function UserList({ teamId }: { teamId: string }) {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    // Runs on mount and when teamId changes
    fetch(`/api/teams/${teamId}/users`)
      .then((res) => res.json())
      .then(setUsers);
  }, [teamId]);

  return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

## See Also

- [hook-exhaustive-deps](hook-exhaustive-deps.md) - Include all reactive values in the dependency array
