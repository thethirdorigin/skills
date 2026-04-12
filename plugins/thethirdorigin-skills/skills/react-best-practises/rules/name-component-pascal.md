# name-component-pascal

> Use PascalCase for React component names

## Why It Matters

React uses casing to distinguish between custom components and native HTML elements. When JSX encounters a lowercase tag like `<myComponent />`, it treats it as a built-in HTML element and renders it as an unknown DOM node. Only PascalCase tags like `<MyComponent />` are recognized as React components.

Consistent PascalCase naming also makes components instantly recognizable in code. When scanning a file, you can tell at a glance which identifiers are components versus utility functions or variables.

## Bad

```tsx
// Lowercase function name — React treats <creditFacilityCard /> as an HTML element
function creditFacilityCard({ title, balance }: CreditFacilityCardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{balance}</p>
    </div>
  );
}

// Snake case — same problem, plus violates JavaScript conventions
const credit_facility_card = ({ title, balance }: CreditFacilityCardProps) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{balance}</p>
    </div>
  );
};

export default credit_facility_card;
```

## Good

```tsx
function CreditFacilityCard({ title, balance }: CreditFacilityCardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>{balance}</p>
    </div>
  );
}

// Usage in JSX matches the component name exactly
function Dashboard() {
  return (
    <section>
      <CreditFacilityCard title="Business Line" balance={50000} />
    </section>
  );
}
```

## See Also

- [name-file-convention](name-file-convention.md) - Match file names to component names
