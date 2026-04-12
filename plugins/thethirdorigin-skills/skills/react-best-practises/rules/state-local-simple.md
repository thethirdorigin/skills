# state-local-simple

> Use useState for simple, isolated UI state like toggles, search text, and pagination

## Why It Matters

Not every piece of state needs to live in a global store. When state is only relevant to a single component — a modal's open/close flag, a search input's current text, or a dropdown's selected index — placing it in a global store adds indirection, increases coupling, and triggers re-renders in unrelated components that subscribe to the same store.

Local `useState` is the simplest state primitive React offers. It is scoped to one component, easy to reason about, and trivial to delete or refactor. Reserve global state for data that genuinely needs to be shared across distant parts of the component tree.

## Bad

```tsx
// Global store for a single modal's visibility — overkill
const useModalStore = create<{ isOpen: boolean; toggle: () => void }>((set) => ({
  isOpen: false,
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
}));

function SettingsPage() {
  const { isOpen, toggle } = useModalStore();

  return (
    <>
      <button onClick={toggle}>Edit Profile</button>
      {isOpen && <EditProfileModal onClose={toggle} />}
    </>
  );
}
```

## Good

```tsx
function SettingsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsModalOpen(true)}>Edit Profile</button>
      {isModalOpen && (
        <EditProfileModal onClose={() => setIsModalOpen(false)} />
      )}
    </>
  );
}
```

## See Also

- [state-close-to-usage](state-close-to-usage.md) - Keep state as close to its usage as possible
- [hook-useReducer-complex](hook-useReducer-complex.md) - Use useReducer for complex related state
