# ts-satisfies

> Use the satisfies operator for type-safe object literals

## Why It Matters

Annotating a variable with `: Type` widens the type to the annotation. Literal string values become `string`, literal numbers become `number`, and you lose the precise inference TypeScript would otherwise provide. This means you cannot use the variable as a discriminant or get autocomplete for its specific literal values.

The `satisfies` operator validates that a value conforms to a type without widening it. You get compile-time checking that the shape is correct, and you retain the exact literal types for downstream use. It is the best of both worlds: type safety and precise inference.

## Bad

```tsx
// Type annotation widens literal types — loses precision
interface RouteConfig {
  path: string;
  label: string;
  requiredRole: "admin" | "viewer" | "editor";
}

const facilityRoute: RouteConfig = {
  path: "/facilities",
  label: "Credit Facilities",
  requiredRole: "admin",
};

// facilityRoute.requiredRole is typed as "admin" | "viewer" | "editor", not "admin"
// Cannot narrow on the specific literal value without a type assertion

// No type checking at all — typos are silent
const dashboardRoute = {
  path: "/dashboard",
  label: "Dashboard",
  requiredRole: "admn",  // Typo — no error because there is no type constraint
};
```

## Good

```tsx
interface RouteConfig {
  path: string;
  label: string;
  requiredRole: "admin" | "viewer" | "editor";
}

const facilityRoute = {
  path: "/facilities",
  label: "Credit Facilities",
  requiredRole: "admin",
} satisfies RouteConfig;

// facilityRoute.requiredRole is typed as "admin" (literal), not the full union
// Type-safe AND preserves precise inference

const dashboardRoute = {
  path: "/dashboard",
  label: "Dashboard",
  requiredRole: "admn",  // Error: "admn" is not assignable to "admin" | "viewer" | "editor"
} satisfies RouteConfig;

// Works well with record types too
const STATUS_LABELS = {
  active: "Active",
  frozen: "Frozen",
  closed: "Closed",
} satisfies Record<string, string>;

// STATUS_LABELS.active is typed as "Active", not string
```

## See Also

- [ts-interface-props](ts-interface-props.md) - Type all component props with an interface declaration
