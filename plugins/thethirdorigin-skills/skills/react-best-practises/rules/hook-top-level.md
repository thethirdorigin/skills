# hook-top-level

> Call hooks at the top level only — never inside conditions, loops, or nested functions

## Why It Matters

React tracks hooks by their call index on each render. When you place a hook inside a condition, loop, or nested function, the number and order of hook calls can differ between renders. React then mismatches hooks to their stored state, corrupting every hook that follows the skipped one.

This is not a stylistic preference — it is a hard requirement of the hooks runtime. Violating it produces silent, difficult-to-diagnose bugs where one piece of state suddenly holds another's value.

## Bad

```tsx
function UserProfile({ isLoggedIn }: { isLoggedIn: boolean }) {
  // Hook call order changes depending on isLoggedIn
  if (isLoggedIn) {
    const [user, setUser] = useState<User | null>(null);
  }

  const [theme, setTheme] = useState("light");
  // When isLoggedIn flips, `theme` state now reads from `user`'s slot
}
```

## Good

```tsx
function UserProfile({ isLoggedIn }: { isLoggedIn: boolean }) {
  // Hooks always called in the same order
  const [user, setUser] = useState<User | null>(null);
  const [theme, setTheme] = useState("light");

  // Use the value conditionally instead
  useEffect(() => {
    if (isLoggedIn) {
      fetchCurrentUser().then(setUser);
    }
  }, [isLoggedIn]);
}
```

## See Also

- [hook-component-only](hook-component-only.md) - Hooks must live inside components or custom hooks
- [hook-before-returns](hook-before-returns.md) - Call all hooks before any early return
