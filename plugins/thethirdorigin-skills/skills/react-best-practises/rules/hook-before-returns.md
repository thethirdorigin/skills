# hook-before-returns

> Call all hooks before any early return statements

## Why It Matters

An early return placed before a hook call means that hook executes on some renders but not others. This is the same problem as a conditional hook — React's call index shifts, and every hook after the skipped one reads from the wrong state slot.

Move all hook calls to the top of the function body, before any guard clauses or early returns. You can still return early after all hooks have been called.

## Bad

```tsx
function OrderDetails({ orderId }: { orderId: string | null }) {
  if (!orderId) {
    return <p>Select an order to view details.</p>;
  }

  // This hook only runs when orderId is truthy — broken call order
  const [order, setOrder] = useState<Order | null>(null);

  useEffect(() => {
    fetchOrder(orderId).then(setOrder);
  }, [orderId]);

  return <OrderCard order={order} />;
}
```

## Good

```tsx
function OrderDetails({ orderId }: { orderId: string | null }) {
  // All hooks called unconditionally at the top
  const [order, setOrder] = useState<Order | null>(null);

  useEffect(() => {
    if (orderId) {
      fetchOrder(orderId).then(setOrder);
    }
  }, [orderId]);

  // Early return after all hooks
  if (!orderId) {
    return <p>Select an order to view details.</p>;
  }

  return <OrderCard order={order} />;
}
```

## See Also

- [hook-top-level](hook-top-level.md) - Never call hooks inside conditions or loops
