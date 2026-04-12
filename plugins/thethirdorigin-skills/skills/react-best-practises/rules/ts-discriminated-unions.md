# ts-discriminated-unions

> Use discriminated unions for state machines and async status patterns

## Why It Matters

A type like `{ isLoading: boolean; error: Error | null; data: T | null }` allows impossible states. Nothing prevents `isLoading: true` and `data: someValue` from coexisting, or `error: someError` with `data: someValue`. Every consumer must handle these impossible combinations defensively, and bugs hide in the gaps.

Discriminated unions make impossible states unrepresentable. When you switch on the discriminant field (`status`), TypeScript narrows the type automatically. Each branch has access to exactly the properties that exist in that state, and the compiler ensures you handle every case.

## Bad

```tsx
// Allows impossible states: isLoading + data, or error + data simultaneously
interface FacilityState {
  isLoading: boolean;
  error: Error | null;
  data: CreditFacility[] | null;
}

function useFacilities(): FacilityState {
  const [state, setState] = useState<FacilityState>({
    isLoading: false,
    error: null,
    data: null,
  });
  // Bug: nothing prevents setState({ isLoading: true, error: someError, data: someData })
  return state;
}

function FacilityList() {
  const { isLoading, error, data } = useFacilities();
  // Must handle every combination defensively
  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return null; // What state is this? Impossible to tell.
  return <DataTable rows={data} />;
}
```

## Good

```tsx
type FacilityState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: Error }
  | { status: "success"; data: CreditFacility[] };

function useFacilities(): FacilityState {
  const [state, setState] = useState<FacilityState>({ status: "idle" });

  useEffect(() => {
    setState({ status: "loading" });
    fetchFacilities()
      .then((data) => setState({ status: "success", data }))
      .catch((error) => setState({ status: "error", error }));
  }, []);

  return state;
}

function FacilityList() {
  const state = useFacilities();

  switch (state.status) {
    case "idle":
      return null;
    case "loading":
      return <Skeleton />;
    case "error":
      // TypeScript knows "error" exists here
      return <ErrorMessage error={state.error} />;
    case "success":
      // TypeScript knows "data" exists here
      return <DataTable rows={state.data} />;
  }
}
```

## See Also

- [ts-interface-vs-type](ts-interface-vs-type.md) - Prefer interface for object shapes, type for unions
