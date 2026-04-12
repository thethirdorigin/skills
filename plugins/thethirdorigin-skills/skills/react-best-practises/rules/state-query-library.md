# state-query-library

> Use the project's data fetching library for all server state

## Why It Matters

Manual `useEffect` + `useState` for API calls misses critical edge cases: race conditions when requests overlap, caching identical requests across components, background refetching when data goes stale, retry logic on transient failures, and optimistic updates for responsive UI. Implementing all of these correctly is a substantial engineering effort, and most hand-rolled solutions handle only the happy path.

Data fetching libraries like TanStack Query, SWR, or Apollo Client solve these problems out of the box. They separate server state (data that lives on a remote server) from client state (UI state local to the browser), providing a dedicated cache, automatic deduplication, and consistent loading/error states.

## Bad

```tsx
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);
    setError(null);

    fetch(`/api/users/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!cancelled) {
          setUser(data);
          setIsLoading(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err);
          setIsLoading(false);
        }
      });

    return () => { cancelled = true; };
  }, [userId]);
  // No caching, no deduplication, no background refetch, no retry
}
```

## Good

```tsx
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ["users", userId],
    queryFn: () =>
      fetch(`/api/users/${userId}`).then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<User>;
      }),
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorBanner error={error} />;
  if (!user) return null;

  return <ProfileCard user={user} />;
}
```

## See Also

- [err-handle-all-states](err-handle-all-states.md) - Handle loading, error, and empty states
