# comp-custom-hooks

> Extract shared component logic into custom hooks, not Higher-Order Components

## Why It Matters

Custom hooks compose without nesting wrappers. Each hook call is visible in the component body, making data flow easy to trace. You can read a component top-to-bottom and see exactly which hooks provide which values.

Higher-Order Components (HOCs) create deeply nested wrapper hierarchies that are difficult to debug. The React DevTools tree fills with anonymous wrappers, prop names collide between HOCs, and TypeScript types become complex to maintain. Custom hooks solve the same code-reuse problem with none of these drawbacks.

## Bad

```tsx
// HOC wrapper hell — opaque data flow, colliding props, deep nesting
const withAuth = (Component: React.ComponentType<any>) =>
  function WithAuth(props: any) {
    const user = useAuthInternal();
    return <Component {...props} user={user} />;
  };

const withTheme = (Component: React.ComponentType<any>) =>
  function WithTheme(props: any) {
    const theme = useThemeInternal();
    return <Component {...props} theme={theme} />;
  };

const withAnalytics = (Component: React.ComponentType<any>) =>
  function WithAnalytics(props: any) {
    const track = useAnalyticsInternal();
    return <Component {...props} track={track} />;
  };

// Three layers of wrapping — where does `user` come from?
export default withAuth(withTheme(withAnalytics(Dashboard)));
```

## Good

```tsx
// Custom hooks — explicit, composable, easy to trace
function Dashboard() {
  const { user, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const { track } = useAnalytics();

  useEffect(() => {
    track("dashboard_viewed", { userId: user.id });
  }, [track, user.id]);

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return (
    <div className={theme === "dark" ? "bg-gray-900" : "bg-white"}>
      <h1>Welcome, {user.name}</h1>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <DashboardContent />
    </div>
  );
}
```

## See Also

- [hook-custom-prefix](hook-custom-prefix.md) - Name custom hooks with the use prefix
