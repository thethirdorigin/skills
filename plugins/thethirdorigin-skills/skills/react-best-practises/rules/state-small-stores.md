# state-small-stores

> Keep stores small and focused — one per domain concern

## Why It Matters

A single monolithic store that holds user data, cart items, notifications, and UI flags creates a re-render blast radius that spans the entire application. Any change to any field in the store notifies every subscribed component, even those that only care about an unrelated slice. Performance degrades as the app grows, and the store file becomes a merge-conflict hotspot.

Splitting state into small, domain-focused stores limits re-render scope to the components that actually use the changed data. Each store is easier to understand, test, and maintain independently. Teams can work on separate stores without stepping on each other.

## Bad

```tsx
// One massive store for everything
const useAppStore = create<AppState>((set) => ({
  // User domain
  user: null,
  setUser: (user) => set({ user }),
  // Cart domain
  cartItems: [],
  addToCart: (item) => set((s) => ({ cartItems: [...s.cartItems, item] })),
  // Notifications domain
  notifications: [],
  addNotification: (n) => set((s) => ({ notifications: [...s.notifications, n] })),
  // UI domain
  sidebarOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));

// Adding an item to cart re-renders the sidebar, user menu, and notification badge
```

## Good

```tsx
// stores/useUserStore.ts
const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user: User | null) => set({ user }),
}));

// stores/useCartStore.ts
const useCartStore = create<CartState>((set) => ({
  items: [],
  addItem: (item: CartItem) =>
    set((s) => ({ items: [...s.items, item] })),
  removeItem: (id: string) =>
    set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
}));

// stores/useNotificationStore.ts
const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  add: (n: Notification) =>
    set((s) => ({ notifications: [...s.notifications, n] })),
  dismiss: (id: string) =>
    set((s) => ({
      notifications: s.notifications.filter((n) => n.id !== id),
    })),
}));

// Cart changes only re-render cart-related components
```

## See Also

- [state-selectors](state-selectors.md) - Use selectors to subscribe to only needed slices
