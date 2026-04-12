# hook-custom-prefix

> Prefix custom hooks with use and extract when logic is reused in 2+ components

## Why It Matters

The `use` prefix is not just a naming convention — it signals to React and the `eslint-plugin-react-hooks` linter that this function follows the Rules of Hooks. Without the prefix, the linter cannot enforce hook ordering and dependency rules inside the function, letting bugs slip through.

Extracting shared hook logic into a custom hook also eliminates duplication. When two components independently implement the same subscription, fetch, or state machine, bug fixes must be applied in both places. A single custom hook centralises the logic.

## Bad

```tsx
// utils/fetchUser.ts — regular function calling hooks
function fetchUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUser(userId).then((data) => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]);

  return { user, loading };
}

// Duplicated in ProfilePage.tsx AND SettingsPage.tsx:
function ProfilePage({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUser(userId).then((data) => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]);
}
```

## Good

```tsx
// hooks/useUser.ts — custom hook with `use` prefix
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);

    getUser(userId)
      .then((data) => {
        if (!cancelled) {
          setUser(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err);
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [userId]);

  return { user, loading, error };
}

// ProfilePage.tsx
function ProfilePage({ userId }: { userId: string }) {
  const { user, loading, error } = useUser(userId);
  // Single source of truth, no duplication
}
```

## See Also

- [hook-component-only](hook-component-only.md) - Hooks must be called from components or custom hooks
