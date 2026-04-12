# ts-export-types

> Export types alongside components when consumers need them

## Why It Matters

When a component's prop types are private, consumers who need to pass the same shape must duplicate the type definition or resort to `React.ComponentProps<typeof Component>`. This creates fragile coupling and makes refactoring harder because changes to the component's props do not propagate to duplicated types elsewhere.

Exporting the prop interface alongside the component gives consumers a first-class type to reference. Wrapper components can extend it, test files can construct valid props, and documentation tools can generate accurate API references.

## Bad

```tsx
// Props interface is private — consumers cannot reference it
interface CardProps {
  title: string;
  balance: number;
  status: "active" | "frozen" | "closed";
}

export function CreditFacilityCard({ title, balance, status }: CardProps) {
  return (
    <div className={`card card--${status}`}>
      <h3>{title}</h3>
      <p>{balance}</p>
    </div>
  );
}

// In another file: consumer must duplicate the type or use ComponentProps
// This type gets out of sync when CardProps changes
interface DuplicatedCardProps {
  title: string;
  balance: number;
  status: "active" | "frozen" | "closed";
}
```

## Good

```tsx
// Props interface is exported alongside the component
export interface CreditFacilityCardProps {
  title: string;
  balance: number;
  status: "active" | "frozen" | "closed";
  onSelect?: (id: string) => void;
}

export function CreditFacilityCard({ title, balance, status, onSelect }: CreditFacilityCardProps) {
  return (
    <div className={`card card--${status}`}>
      <h3>{title}</h3>
      <p>{balance}</p>
    </div>
  );
}

// In another file: consumers import and extend the type directly
import { CreditFacilityCard, type CreditFacilityCardProps } from "./CreditFacilityCard";

interface HighlightedCardProps extends CreditFacilityCardProps {
  highlightColor: string;
}

function HighlightedCard({ highlightColor, ...cardProps }: HighlightedCardProps) {
  return (
    <div style={{ borderColor: highlightColor }}>
      <CreditFacilityCard {...cardProps} />
    </div>
  );
}
```

## See Also

- [ts-interface-props](ts-interface-props.md) - Type all component props with an interface declaration
