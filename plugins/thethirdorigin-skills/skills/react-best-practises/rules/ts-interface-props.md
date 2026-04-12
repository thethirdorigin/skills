# ts-interface-props

> Type all component props with an interface declaration

## Why It Matters

A named interface serves as the component's API contract. It is reusable across tests, stories, and wrapper components. IDEs display the interface name in tooltips, making it easy to jump to the definition and see every accepted prop at once.

Inline types work for trivial cases, but they cannot be extended, exported, or referenced by name. As components grow, inline types become unwieldy and force duplication when other components need to pass the same shape.

## Bad

```tsx
// Inline type — cannot be exported, extended, or referenced elsewhere
function CreditFacilityCard({ title, balance, currency }: { title: string; balance: number; currency: string }) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{balance} {currency}</p>
    </div>
  );
}

// Using "any" — disables all type checking for props
function FacilityDetails(props: any) {
  return <div>{props.whatever}</div>;
}
```

## Good

```tsx
interface CreditFacilityCardProps {
  title: string;
  balance: number;
  currency: string;
  onSelect?: () => void;
}

function CreditFacilityCard({ title, balance, currency, onSelect }: CreditFacilityCardProps) {
  return (
    <div onClick={onSelect} role="button" tabIndex={0}>
      <h3>{title}</h3>
      <p>
        {new Intl.NumberFormat("en-US", { style: "currency", currency }).format(balance)}
      </p>
    </div>
  );
}

// The interface can be extended for specialized variants
interface HighlightedFacilityCardProps extends CreditFacilityCardProps {
  highlightColor: string;
}
```

## See Also

- [ts-no-any](ts-no-any.md) - Use unknown and narrow instead of any
- [ts-interface-vs-type](ts-interface-vs-type.md) - Prefer interface for object shapes, type for unions
