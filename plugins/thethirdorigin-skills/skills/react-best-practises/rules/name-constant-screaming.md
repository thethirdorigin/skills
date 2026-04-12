# name-constant-screaming

> Use SCREAMING_SNAKE_CASE for module-level constants

## Why It Matters

Module-level constants are values that never change for the lifetime of the application. SCREAMING_SNAKE_CASE makes them visually distinct from mutable variables. When you see `PAGE_SIZE` in code, you immediately know it is a fixed value defined at the module level, not something computed or passed in.

This convention also discourages accidental reassignment. A developer seeing `pageSize` might assume it can be changed; `PAGE_SIZE` signals immutability at a glance.

## Bad

```tsx
// Looks like a regular mutable variable
const pageSize = 25;
const defaultSort = "name";
const maxRetries = 3;
const apiTimeout = 5000;

function CreditFacilityList() {
  // Reader cannot tell if pageSize is a constant or computed value
  const facilities = useFacilities({ limit: pageSize, sort: defaultSort });
  return <DataTable data={facilities} />;
}
```

## Good

```tsx
const PAGE_SIZE = 25;
const DEFAULT_SORT = "name";
const MAX_RETRIES = 3;
const API_TIMEOUT_MS = 5000;

function CreditFacilityList() {
  // PAGE_SIZE is clearly a fixed constant
  const facilities = useFacilities({ limit: PAGE_SIZE, sort: DEFAULT_SORT });
  return <DataTable data={facilities} />;
}
```

## See Also

- [name-variable-camel](name-variable-camel.md) - Use camelCase for variables, functions, and hook names
