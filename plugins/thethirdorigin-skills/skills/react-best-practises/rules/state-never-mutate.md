# state-never-mutate

> Never mutate state objects or arrays directly

## Why It Matters

React determines whether to re-render a component by comparing the previous and next state values by reference. When you mutate an object or array in place — `state.items.push(newItem)` or `state.user.name = "new"` — the reference stays the same. React sees no change and skips the re-render, leaving the UI displaying stale data even though the underlying data has been modified.

This creates some of the most confusing bugs in React: the data is correct in the console, the component's state holds the right values, but the screen never updates. Always create a new object or array reference when updating state.

## Bad

```tsx
function ShoppingCart() {
  const [items, setItems] = useState<CartItem[]>([]);

  function addItem(item: CartItem) {
    // Mutates the existing array — same reference, no re-render
    items.push(item);
    setItems(items);
  }

  function updateQuantity(id: string, quantity: number) {
    // Mutates an object inside the array — React never sees the change
    const item = items.find((i) => i.id === id);
    if (item) {
      item.quantity = quantity;
      setItems(items);
    }
  }
}
```

## Good

```tsx
function ShoppingCart() {
  const [items, setItems] = useState<CartItem[]>([]);

  function addItem(item: CartItem) {
    // New array reference triggers re-render
    setItems((prev) => [...prev, item]);
  }

  function updateQuantity(id: string, quantity: number) {
    // New array with a new object for the updated item
    setItems((prev) =>
      prev.map((item) =>
        item.id === id ? { ...item, quantity } : item
      )
    );
  }
}
```

## See Also

- [state-immutable-updates](state-immutable-updates.md) - Use spread, map, filter for immutable updates
