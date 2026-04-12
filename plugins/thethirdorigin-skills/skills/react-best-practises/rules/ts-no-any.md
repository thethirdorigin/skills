# ts-no-any

> Use unknown and narrow, or specific types, instead of any

## Why It Matters

`any` disables TypeScript's type system for everything it touches. It propagates silently: a function returning `any` infects every variable that stores its result. Bugs that the compiler would catch at build time become runtime errors discovered in production.

`unknown` is the type-safe counterpart. It forces you to narrow the type before using the value, which means you write the validation code that would otherwise be missing. The result is code that handles unexpected shapes explicitly instead of crashing on `.property` access of `undefined`.

## Bad

```tsx
// "any" disables type checking — typos and wrong property access are silent
function parseFacilityResponse(data: any) {
  return {
    name: data.facilityName,
    balance: data.currentBalance,
    status: data.stats,            // Typo: should be "status" — no error
  };
}

// "any" in state — everything downstream loses type safety
const [facility, setFacility] = useState<any>(null);

// "any" in event handler — no autocomplete, no error checking
const handleChange = (e: any) => {
  setName(e.taget.value);          // Typo: should be "target" — no error
};
```

## Good

```tsx
// Specific type — compiler catches typos and wrong access
interface FacilityResponse {
  facilityName: string;
  currentBalance: number;
  status: "active" | "frozen" | "closed";
}

function parseFacilityResponse(data: FacilityResponse) {
  return {
    name: data.facilityName,
    balance: data.currentBalance,
    status: data.status,
  };
}

// "unknown" with narrowing for truly dynamic data
function parseApiError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === "string") {
    return error;
  }
  return "An unexpected error occurred";
}

// Typed event handler — full autocomplete and error checking
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setName(e.target.value);
};
```

## See Also

- [ts-interface-props](ts-interface-props.md) - Type all component props with an interface declaration
