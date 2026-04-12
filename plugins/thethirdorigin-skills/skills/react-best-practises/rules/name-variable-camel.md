# name-variable-camel

> Use camelCase for variables, functions, and hook names

## Why It Matters

camelCase is the universal JavaScript convention. When every variable and function follows the same casing pattern, the codebase becomes predictable. Developers can guess a name without looking it up, and search tools return consistent results.

Mixing casing styles forces readers to remember which convention applies where. A function named `GetCreditFacilities` looks like a class constructor in JavaScript, while `get_credit_facilities` looks like Python code. camelCase eliminates this ambiguity across the entire codebase.

## Bad

```tsx
// Snake case — looks like Python, not JavaScript
const total_amount = 0;
const user_name = "Alice";

// PascalCase for a regular function — looks like a component or constructor
function GetCreditFacilities() {
  return fetch("/api/credit-facilities");
}

// Mixed conventions in the same file
const is_active = true;
const pageCount = 10;
function fetch_Users() { /* ... */ }
```

## Good

```tsx
const totalAmount = 0;
const userName = "Alice";

function getCreditFacilities() {
  return fetch("/api/credit-facilities");
}

// Custom hooks also use camelCase, prefixed with "use"
function useCreditFacility(id: string) {
  const [facility, setFacility] = useState<CreditFacility | null>(null);
  // ...
  return facility;
}
```

## See Also

- [name-constant-screaming](name-constant-screaming.md) - Use SCREAMING_SNAKE_CASE for module-level constants
