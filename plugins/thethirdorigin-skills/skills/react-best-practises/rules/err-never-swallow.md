# err-never-swallow

> Always log or display errors -- never catch and ignore silently

## Why It Matters

A swallowed error is a hidden bug. When a catch block does nothing, the operation fails silently, and the application continues in an inconsistent state. Users see stale data or broken UI with no indication that something went wrong. Developers debugging production issues find no logs, no traces, and no clues.

Every catch block should either display the error to the user, log it for debugging, or both. Even errors you expect and handle gracefully should be logged at an appropriate level so you can monitor their frequency and detect regressions.

## Bad

```tsx
// Empty catch — error vanishes completely
try {
  await api.syncFacilityData(facilityId);
} catch (e) {
  // ignore
}

// Catching and returning null — caller has no idea something failed
async function fetchFacility(id: string): Promise<CreditFacility | null> {
  try {
    return await api.getFacility(id);
  } catch (e) {
    return null; // Was it a 404? A network timeout? A 500? Nobody knows.
  }
}

// Catching and logging a useless message
try {
  await api.updateFacility(id, data);
} catch (e) {
  console.log("error"); // What error? Where? What was the input?
}
```

## Good

```tsx
// Log with context and inform the user
try {
  await api.syncFacilityData(facilityId);
} catch (err) {
  console.error(`Failed to sync facility ${facilityId}:`, err);
  toast.error("Failed to sync facility data. Please try again.");
}

// Return null when appropriate, but log the error
async function fetchFacility(id: string): Promise<CreditFacility | null> {
  try {
    return await api.getFacility(id);
  } catch (err) {
    console.error(`Failed to fetch facility ${id}:`, err);
    // Re-throw unexpected errors, handle expected ones
    if (err instanceof ApiError && err.status === 404) {
      return null;
    }
    throw err;
  }
}

// Log structured context for debugging
try {
  await api.updateFacility(id, data);
} catch (err) {
  console.error("Failed to update facility:", { id, data, error: err });
  setError(err instanceof Error ? err : new Error("Unknown error"));
}
```

## See Also

- [err-try-catch-async](err-try-catch-async.md) - Wrap async operations in try-catch with user-facing error messages
