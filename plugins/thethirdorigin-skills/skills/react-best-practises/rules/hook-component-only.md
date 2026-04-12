# hook-component-only

> Call hooks only from React function components or custom hooks

## Why It Matters

Hooks depend on React's internal fiber tree to associate state and effects with a specific component instance. When you call a hook from a regular utility function, there is no fiber context — React cannot determine which component the state belongs to, and the call throws at runtime.

Even if the utility function happens to be called from inside a component, React cannot guarantee the fiber context will be available. The only safe call sites are function components and functions whose names start with `use`.

## Bad

```tsx
// utils/auth.ts — regular utility function
function getAuthState() {
  // Runtime error: hooks can only be called inside a component
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    setToken(localStorage.getItem("auth_token"));
  }, []);

  return token;
}
```

## Good

```tsx
// hooks/useAuth.ts — custom hook with `use` prefix
function useAuth() {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    setToken(localStorage.getItem("auth_token"));
  }, []);

  return { token, isAuthenticated: token !== null };
}

// components/Dashboard.tsx
function Dashboard() {
  const { token, isAuthenticated } = useAuth();
  // ...
}
```

## See Also

- [hook-top-level](hook-top-level.md) - Hooks must be called at the top level
- [hook-custom-prefix](hook-custom-prefix.md) - Prefix custom hooks with `use`
