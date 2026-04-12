# hook-exhaustive-deps

> Include all reactive values used inside the hook in the dependency array

## Why It Matters

When a reactive value (prop, state, or derived variable) is used inside a `useEffect`, `useMemo`, or `useCallback` but omitted from the dependency array, the hook captures a stale closure. The callback continues to reference the value from the render when it was first created, never seeing subsequent updates.

This leads to subtle bugs: an effect that fetches data for a user ID that has already changed, a memoised value computed from an outdated filter, or a callback that acts on state from ten renders ago. Enable the `react-hooks/exhaustive-deps` ESLint rule and treat its warnings as errors.

## Bad

```tsx
function ChatRoom({ roomId, theme }: { roomId: string; theme: Theme }) {
  useEffect(() => {
    // `roomId` is used but omitted from deps — stale closure
    const connection = createConnection(roomId);
    connection.on("message", (msg) => {
      // `theme` is used but omitted — toast always uses the initial theme
      showToast(msg, { style: theme.toastStyle });
    });
    connection.connect();

    return () => connection.disconnect();
  }, []); // Missing: roomId, theme
}
```

## Good

```tsx
function ChatRoom({ roomId, theme }: { roomId: string; theme: Theme }) {
  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on("message", (msg) => {
      showToast(msg, { style: theme.toastStyle });
    });
    connection.connect();

    return () => connection.disconnect();
  }, [roomId, theme]); // All reactive values included
}
```

## See Also

- [hook-useEffect-deps](hook-useEffect-deps.md) - Always include a dependency array in useEffect
