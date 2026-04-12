# err-handle-all-states

> Handle loading, error, and success states for all async operations

## Why It Matters

Every async operation has at least three states: loading, error, and success. Rendering only the success state means users see a blank screen while data loads and a crash or frozen UI when an error occurs. Both outcomes erode trust and make the application feel broken.

Handling all states explicitly gives users continuous feedback. A skeleton or spinner during loading confirms the app is working. A clear error message with a retry option keeps users in control. The success state displays the actual content. Together, these three states create a complete, reliable user experience.

## Bad

```tsx
// Only renders the success state — blank screen while loading, crash on error
function FacilityDetails({ id }: { id: string }) {
  const { data } = useQuery({
    queryKey: ["facility", id],
    queryFn: () => fetchFacility(id),
  });

  // If data is undefined (loading) or the query errored, this crashes
  return (
    <div>
      <h1>{data.name}</h1>
      <p>Balance: {data.balance}</p>
      <p>Status: {data.status}</p>
    </div>
  );
}

// Handles loading but ignores errors
function FacilityList() {
  const { data, isLoading } = useQuery({
    queryKey: ["facilities"],
    queryFn: fetchFacilities,
  });

  if (isLoading) return <Skeleton />;

  // Error state falls through to rendering with undefined data
  return <DataTable rows={data ?? []} />;
}
```

## Good

```tsx
function FacilityDetails({ id }: { id: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["facility", id],
    queryFn: () => fetchFacility(id),
  });

  if (isLoading) {
    return <FacilityDetailsSkeleton />;
  }

  if (error) {
    return (
      <ErrorMessage
        title="Failed to load facility"
        message="Please check your connection and try again."
        onRetry={() => window.location.reload()}
      />
    );
  }

  if (!data) {
    return <EmptyState message="Facility not found." />;
  }

  return (
    <div>
      <h1>{data.name}</h1>
      <p>Balance: {formatCurrency(data.balance)}</p>
      <StatusBadge status={data.status} />
    </div>
  );
}

function FacilityList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["facilities"],
    queryFn: fetchFacilities,
  });

  if (isLoading) return <TableSkeleton rows={5} columns={4} />;

  if (error) {
    return (
      <ErrorMessage
        title="Failed to load facilities"
        onRetry={() => window.location.reload()}
      />
    );
  }

  if (!data || data.length === 0) {
    return <EmptyState message="No credit facilities found." />;
  }

  return <DataTable rows={data} columns={FACILITY_COLUMNS} />;
}
```

## See Also

- [err-error-boundary](err-error-boundary.md) - Place Error Boundaries at route or section level to catch rendering errors
