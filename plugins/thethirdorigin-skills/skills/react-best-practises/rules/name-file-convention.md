# name-file-convention

> Use PascalCase for component files, camelCase for utility files

## Why It Matters

When a file name matches its default export, navigation becomes effortless. Searching for the `CreditFacilityCard` component means opening `CreditFacilityCard.tsx`. Searching for the `formatCurrency` utility means opening `formatCurrency.ts`. There is no guessing, no mapping, and no ambiguity.

This convention also makes the file's purpose obvious from the file tree alone. PascalCase files contain React components; camelCase files contain utilities, hooks, or helpers. You can scan a directory and understand its structure without opening a single file.

## Bad

```tsx
// Kebab-case for a component file — does not match the export name
// File: credit-facility-card.tsx
export function CreditFacilityCard() { /* ... */ }

// PascalCase for a utility file — looks like a component
// File: FormatCurrency.ts
export function formatCurrency(amount: number): string { /* ... */ }

// Index files that re-export everything — hides the actual component location
// File: index.tsx
export { CreditFacilityCard } from "./CreditFacilityCard";
export { FacilityDetails } from "./FacilityDetails";
```

## Good

```tsx
// File: CreditFacilityCard.tsx — PascalCase matches the component name
export function CreditFacilityCard({ facility }: CreditFacilityCardProps) {
  return (
    <div className="card">
      <h3>{facility.name}</h3>
      <p>{formatCurrency(facility.balance)}</p>
    </div>
  );
}

// File: formatCurrency.ts — camelCase matches the utility function name
export function formatCurrency(amount: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount);
}

// File: useCreditFacility.ts — camelCase matches the hook name
export function useCreditFacility(id: string) {
  return useQuery({ queryKey: ["facility", id], queryFn: () => fetchFacility(id) });
}
```

## See Also

- [name-component-pascal](name-component-pascal.md) - Use PascalCase for React component names
