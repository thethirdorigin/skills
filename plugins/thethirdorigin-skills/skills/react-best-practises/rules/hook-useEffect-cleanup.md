# hook-useEffect-cleanup

> Return a cleanup function from useEffect for subscriptions, timers, and listeners

## Why It Matters

When a component unmounts or an effect re-runs, React calls the cleanup function returned from the previous effect invocation. Without cleanup, event listeners, WebSocket connections, intervals, and subscriptions accumulate — each mount adds another listener, and none are removed.

This causes memory leaks, stale callbacks firing against unmounted components, and duplicate side effects. In Strict Mode during development, React intentionally double-mounts components to surface missing cleanup early.

## Bad

```tsx
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    // No cleanup — listener leaks on every mount/unmount cycle
  }, []);

  return <span>Width: {width}px</span>;
}
```

## Good

```tsx
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return <span>Width: {width}px</span>;
}
```

## See Also

- [hook-useEffect-deps](hook-useEffect-deps.md) - Always include a dependency array
