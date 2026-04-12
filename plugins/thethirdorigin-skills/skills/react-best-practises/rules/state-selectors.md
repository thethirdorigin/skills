# state-selectors

> Use selectors to subscribe to only the state slices a component needs

## Why It Matters

When a component subscribes to an entire store object, it re-renders whenever any field in that store changes — even fields the component never reads. In a store with user data, preferences, and session info, updating the user's notification count forces a re-render in a component that only displays the user's name.

Selectors narrow the subscription to specific fields. The component only re-renders when the selected value actually changes, dramatically reducing unnecessary render cycles as the store and component tree grow.

## Bad

```tsx
function UserGreeting() {
  // Subscribes to the entire store — re-renders on ANY state change
  const store = useUserStore();

  return <h1>Welcome, {store.user.name}</h1>;
}

function NotificationBadge() {
  // Also subscribes to everything — re-renders when name changes too
  const store = useUserStore();

  return <span>{store.notifications.length}</span>;
}
```

## Good

```tsx
function UserGreeting() {
  // Only re-renders when user.name changes
  const userName = useUserStore((state) => state.user.name);

  return <h1>Welcome, {userName}</h1>;
}

function NotificationBadge() {
  // Only re-renders when the notification count changes
  const count = useNotificationStore((state) => state.notifications.length);

  return <span>{count}</span>;
}

// For multiple fields, use shallow comparison to avoid object identity issues
import { shallow } from "zustand/shallow";

function UserCard() {
  const { name, avatar } = useUserStore(
    (state) => ({ name: state.user.name, avatar: state.user.avatar }),
    shallow
  );

  return (
    <div>
      <img src={avatar} alt={name} />
      <span>{name}</span>
    </div>
  );
}
```

## See Also

- [state-small-stores](state-small-stores.md) - Keep stores small and focused per domain
