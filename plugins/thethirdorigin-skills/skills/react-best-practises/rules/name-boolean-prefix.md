# name-boolean-prefix

> Prefix boolean props and variables with is, has, should, or can

## Why It Matters

Boolean variables answer yes-or-no questions. Prefixing them with `is`, `has`, `should`, or `can` makes the question explicit. Reading `if (isLoading)` is immediately clear; reading `if (loading)` requires a moment to confirm the variable is a boolean and not, say, a loading state string or an object.

This convention also prevents naming collisions. A component might have both a `disabled` style variant and an `isDisabled` boolean prop. The prefix distinguishes the boolean flag from other uses of the same word.

## Bad

```tsx
interface CreditFacilityCardProps {
  loading: boolean;        // Is this a boolean or a loading state object?
  error: boolean;          // Collides with an Error object name
  visible: boolean;        // Adjective alone is ambiguous
  disabled: boolean;       // Could be a CSS class or a boolean
  authenticated: boolean;  // Past participle without prefix
}

function CreditFacilityCard({ loading, error, visible }: CreditFacilityCardProps) {
  if (loading) return <Skeleton />;
  if (error) return <Alert />;        // "error" looks like it holds an Error object
  if (!visible) return null;
  return <div>...</div>;
}
```

## Good

```tsx
interface CreditFacilityCardProps {
  isLoading: boolean;
  hasError: boolean;
  isVisible: boolean;
  isDisabled: boolean;
  isAuthenticated: boolean;
}

function CreditFacilityCard({ isLoading, hasError, isVisible }: CreditFacilityCardProps) {
  if (isLoading) return <Skeleton />;
  if (hasError) return <Alert />;     // Clearly a boolean, not an Error object
  if (!isVisible) return null;
  return <div>...</div>;
}

// "can" and "should" for capability and intent booleans
const canEditFacility = user.role === "admin" && !facility.isLocked;
const shouldAutoRefresh = isVisible && !isEditing;
```

## See Also

- [name-handler-prefix](name-handler-prefix.md) - Prefix event handlers with handle, callback props with on
