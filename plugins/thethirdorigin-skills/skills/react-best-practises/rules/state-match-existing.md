# state-match-existing

> Use the project's existing state management library — do not introduce a new one

## Why It Matters

Every state management library has its own mental model, API surface, and patterns for defining stores, dispatching updates, and subscribing to changes. When a second library is introduced alongside the first, developers must learn and context-switch between both. State flows become fragmented — some data lives in Redux, some in Zustand, and some in Context — making it difficult to trace where a value comes from or why it changed.

Before writing any state management code, discover what the project already uses. Check `package.json` for libraries like Redux Toolkit, Zustand, Jotai, Recoil, MobX, or Valtio. Search for existing store files and follow their conventions for file structure, naming, and patterns.

## Bad

```tsx
// Project already uses Redux Toolkit throughout, but this file introduces Zustand
import { create } from "zustand";

const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  addNotification: (n: Notification) =>
    set((s) => ({ notifications: [...s.notifications, n] })),
  dismiss: (id: string) =>
    set((s) => ({
      notifications: s.notifications.filter((n) => n.id !== id),
    })),
}));
```

## Good

```tsx
// Follow the project's existing Redux Toolkit pattern
import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

interface NotificationState {
  notifications: Notification[];
}

const notificationSlice = createSlice({
  name: "notifications",
  initialState: { notifications: [] } as NotificationState,
  reducers: {
    addNotification(state, action: PayloadAction<Notification>) {
      state.notifications.push(action.payload);
    },
    dismiss(state, action: PayloadAction<string>) {
      state.notifications = state.notifications.filter(
        (n) => n.id !== action.payload
      );
    },
  },
});

export const { addNotification, dismiss } = notificationSlice.actions;
export default notificationSlice.reducer;
```

## See Also

- [state-small-stores](state-small-stores.md) - Keep stores small and focused per domain
