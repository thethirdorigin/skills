# anti-business-in-component

> Extract business logic into custom hooks or utility functions

## Why It Matters

Business logic embedded directly in a component is hard to test and impossible to reuse. To test a price calculation, you would have to render the entire checkout form, fill in fields, and inspect the DOM output. Extracting that logic into a hook or utility function lets you test it with simple input/output assertions — no rendering required.

Separation also makes the component easier to read. The component handles rendering and user interaction; the hook or utility handles rules, calculations, and transformations. Each can evolve independently.

## Bad

```tsx
// Complex business logic directly in the component
function OrderSummary({ items, coupon, shippingMethod }: OrderSummaryProps) {
  // 40 lines of calculation logic mixed with rendering
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  let discount = 0;
  if (coupon) {
    if (coupon.type === "percentage") {
      discount = subtotal * (coupon.value / 100);
      if (coupon.maxDiscount) {
        discount = Math.min(discount, coupon.maxDiscount);
      }
    } else if (coupon.type === "fixed") {
      discount = Math.min(coupon.value, subtotal);
    }
    if (coupon.minimumOrder && subtotal < coupon.minimumOrder) {
      discount = 0;
    }
  }

  const shippingCost =
    shippingMethod === "express" ? 15.99 :
    shippingMethod === "standard" ? 5.99 :
    subtotal >= 50 ? 0 : 5.99;

  const tax = (subtotal - discount) * 0.08875;
  const total = subtotal - discount + shippingCost + tax;

  return (
    <div>
      <p>Subtotal: ${subtotal.toFixed(2)}</p>
      {discount > 0 && <p>Discount: -${discount.toFixed(2)}</p>}
      <p>Shipping: ${shippingCost.toFixed(2)}</p>
      <p>Tax: ${tax.toFixed(2)}</p>
      <p>Total: ${total.toFixed(2)}</p>
    </div>
  );
}
```

## Good

```tsx
// Business logic in a testable hook
function useOrderCalculation(items: CartItem[], coupon: Coupon | null, shippingMethod: string) {
  return useMemo(() => {
    const subtotal = calculateSubtotal(items);
    const discount = calculateDiscount(subtotal, coupon);
    const shippingCost = calculateShipping(shippingMethod, subtotal);
    const tax = calculateTax(subtotal - discount);
    const total = subtotal - discount + shippingCost + tax;

    return { subtotal, discount, shippingCost, tax, total };
  }, [items, coupon, shippingMethod]);
}

// Component focuses on rendering
function OrderSummary({ items, coupon, shippingMethod }: OrderSummaryProps) {
  const { subtotal, discount, shippingCost, tax, total } = useOrderCalculation(
    items,
    coupon,
    shippingMethod,
  );

  return (
    <dl>
      <dt>Subtotal</dt>
      <dd>${subtotal.toFixed(2)}</dd>
      {discount > 0 && (
        <>
          <dt>Discount</dt>
          <dd>-${discount.toFixed(2)}</dd>
        </>
      )}
      <dt>Shipping</dt>
      <dd>${shippingCost.toFixed(2)}</dd>
      <dt>Tax</dt>
      <dd>${tax.toFixed(2)}</dd>
      <dt>Total</dt>
      <dd>${total.toFixed(2)}</dd>
    </dl>
  );
}
```

## See Also

- [comp-custom-hooks](comp-custom-hooks.md) - Extract shared component logic into custom hooks
