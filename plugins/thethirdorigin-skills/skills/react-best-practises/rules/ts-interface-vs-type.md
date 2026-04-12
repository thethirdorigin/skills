# ts-interface-vs-type

> Prefer interface for object shapes, type for unions and intersections

## Why It Matters

Interfaces and type aliases overlap significantly, but each has strengths the other lacks. Interfaces support declaration merging, allowing third-party libraries to extend your types. They also produce clearer error messages and are slightly more performant for the TypeScript compiler when checking object shapes.

Type aliases handle unions, intersections, mapped types, and conditional types that interfaces cannot express. Using each construct for its strength produces idiomatic TypeScript that other developers expect and understand.

## Bad

```tsx
// Using type for a plain object shape — loses declaration merging and extension
type UserProps = {
  name: string;
  email: string;
  role: string;
};

// Using interface for a union — interfaces cannot express unions
// This does not compile:
// interface Status = "idle" | "loading" | "error" | "success";

// Using type for everything, even extendable objects
type BaseCardProps = {
  title: string;
  className?: string;
};

type FacilityCardProps = BaseCardProps & {
  balance: number;
  status: string;
};
```

## Good

```tsx
// Interface for object shapes — extendable and mergeable
interface UserProps {
  name: string;
  email: string;
  role: string;
}

// Interface for component props — supports extends
interface BaseCardProps {
  title: string;
  className?: string;
}

interface FacilityCardProps extends BaseCardProps {
  balance: number;
  status: FacilityStatus;
}

// Type for unions — interfaces cannot express this
type FacilityStatus = "active" | "frozen" | "closed";

// Type for discriminated unions
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: Error }
  | { status: "success"; data: T };

// Type for intersections and mapped types
type ReadonlyFacility = Readonly<CreditFacility>;
type FacilityKeys = keyof CreditFacility;
type PartialUpdate = Partial<Pick<CreditFacility, "name" | "status">>;
```

## See Also

- [ts-interface-props](ts-interface-props.md) - Type all component props with an interface declaration
