# comp-side-effects

> Place side effects in useEffect or event handlers, never in the render body

## Why It Matters

Render functions can run multiple times per commit. React Strict Mode intentionally double-invokes them to surface impurities, and concurrent features like Suspense may discard and replay renders. A side effect placed directly in the render body executes every time React calls the function — not just when the component mounts or updates.

This causes duplicate analytics events, redundant API calls, race conditions, and corrupted external state. Moving side effects into `useEffect` (for synchronisation with external systems) or event handlers (for user-initiated actions) ensures they fire exactly when intended.

## Bad

```tsx
// Side effect in render body — fires on every render, duplicated in Strict Mode
function Dashboard({ userId }: { userId: string }) {
  analytics.track("dashboard_viewed", { userId }); // Fires 2x in Strict Mode
  const data = api.fetchSync(`/users/${userId}`); // Blocks render, runs repeatedly

  return (
    <div>
      <h1>Dashboard</h1>
      <UserStats data={data} />
    </div>
  );
}
```

## Good

```tsx
// Side effects in useEffect and event handlers — controlled execution
function Dashboard({ userId }: { userId: string }) {
  const [data, setData] = useState<UserStats | null>(null);

  useEffect(() => {
    analytics.track("dashboard_viewed", { userId });
  }, [userId]);

  useEffect(() => {
    let cancelled = false;
    api.fetchUserStats(userId).then((result) => {
      if (!cancelled) setData(result);
    });
    return () => { cancelled = true; };
  }, [userId]);

  function handleExport() {
    analytics.track("dashboard_exported", { userId });
    downloadCsv(data);
  }

  if (!data) return <LoadingSkeleton />;

  return (
    <div>
      <h1>Dashboard</h1>
      <UserStats data={data} />
      <button onClick={handleExport}>Export CSV</button>
    </div>
  );
}
```

## See Also

- [comp-pure-render](comp-pure-render.md) - Keep components pure — same props produce the same JSX output
