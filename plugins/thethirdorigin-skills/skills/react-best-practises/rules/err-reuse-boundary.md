# err-reuse-boundary

> Search for existing ErrorBoundary components before creating new ones

## Why It Matters

Most projects already have a shared ErrorBoundary component with consistent styling, error logging, and recovery behavior. Creating a new one in every feature directory leads to fragmented error UI, duplicated logic, and inconsistent user experience across the application.

Before writing a new ErrorBoundary, search the codebase for existing implementations. Reusing the shared component means one place to update styling, one place to add error reporting integrations, and a consistent recovery experience for users.

## Bad

```tsx
// Feature-specific ErrorBoundary duplicated in every directory
// File: features/facilities/FacilityErrorBoundary.tsx
class FacilityErrorBoundary extends React.Component<Props, State> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("Facility error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong in facilities.</div>;
    }
    return this.props.children;
  }
}

// Another copy in a different feature
// File: features/dashboard/DashboardErrorBoundary.tsx
class DashboardErrorBoundary extends React.Component<Props, State> {
  // Nearly identical implementation...
}
```

## Good

```tsx
// File: components/ErrorBoundary.tsx — single shared implementation
// Already exists in the project with logging, styling, and retry support

// File: features/facilities/FacilityList.tsx
import { ErrorBoundary } from "@/components/ErrorBoundary";

function FacilityPage() {
  return (
    <ErrorBoundary
      fallback={<ErrorMessage title="Failed to load facilities" />}
      onError={(error) => reportError("FacilityPage", error)}
    >
      <FacilityList />
    </ErrorBoundary>
  );
}

// File: features/dashboard/Dashboard.tsx
import { ErrorBoundary } from "@/components/ErrorBoundary";

function DashboardPage() {
  return (
    <ErrorBoundary
      fallback={<ErrorMessage title="Failed to load dashboard" />}
      onError={(error) => reportError("DashboardPage", error)}
    >
      <Dashboard />
    </ErrorBoundary>
  );
}

// Same component, consistent UX, different fallback messages per section
```

## See Also

- [err-error-boundary](err-error-boundary.md) - Place Error Boundaries at route or section level
