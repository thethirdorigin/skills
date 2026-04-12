# err-error-boundary

> Place Error Boundaries at route or section level to catch rendering errors

## Why It Matters

When a React component throws during rendering, the entire component tree unmounts by default. Without an Error Boundary, a single broken component takes down the whole application, leaving users with a blank white screen and no way to recover.

Error Boundaries catch rendering errors in their subtree and display a fallback UI. Placing them at the route or major section level means a crash in one part of the app does not affect the rest. Users see a helpful error message and can navigate to other sections that still work.

## Bad

```tsx
// No Error Boundary — one broken component crashes the entire app
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/facilities" element={<FacilityList />} />
        <Route path="/facilities/:id" element={<FacilityDetails />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

// If FacilityDetails throws, the entire app goes white.
// Dashboard becomes inaccessible even though it has no errors.
```

## Good

```tsx
import { ErrorBoundary } from "@/components/ErrorBoundary";

function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary fallback={<AppErrorPage />}>
        <Layout>
          <Routes>
            <Route
              path="/facilities"
              element={
                <ErrorBoundary fallback={<SectionError section="Facilities" />}>
                  <FacilityList />
                </ErrorBoundary>
              }
            />
            <Route
              path="/facilities/:id"
              element={
                <ErrorBoundary fallback={<SectionError section="Facility Details" />}>
                  <FacilityDetails />
                </ErrorBoundary>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ErrorBoundary fallback={<SectionError section="Dashboard" />}>
                  <Dashboard />
                </ErrorBoundary>
              }
            />
          </Routes>
        </Layout>
      </ErrorBoundary>
    </BrowserRouter>
  );
}

// If FacilityDetails throws, only that route shows an error.
// Dashboard and navigation remain fully functional.
```

## See Also

- [err-handle-all-states](err-handle-all-states.md) - Handle loading, error, and success states for all async operations
