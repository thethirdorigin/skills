# err-try-catch-async

> Wrap async operations in try-catch with user-facing error messages

## Why It Matters

Unhandled async errors cause silent failures or cryptic error messages. A network request that fails without a try-catch produces an unhandled promise rejection in the console, but the user sees nothing -- or worse, sees a frozen loading spinner that never resolves.

Wrapping async operations in try-catch gives you two opportunities: show the user a clear error message explaining what went wrong, and log the technical details for debugging. Both are essential for a production application.

## Bad

```tsx
// No error handling — unhandled promise rejection on failure
async function handleCreateFacility(data: FacilityFormData) {
  await api.createFacility(data);
  navigate("/facilities");
}

// Catching but not informing the user
async function handleApproveFacility(id: string) {
  try {
    await api.approveFacility(id);
  } catch (err) {
    console.log(err); // User sees nothing, thinks the action succeeded
  }
}
```

## Good

```tsx
async function handleCreateFacility(data: FacilityFormData) {
  try {
    await api.createFacility(data);
    toast.success("Credit facility created successfully.");
    navigate("/facilities");
  } catch (err) {
    console.error("Failed to create facility:", err);
    toast.error("Failed to create credit facility. Please try again.");
  }
}

async function handleApproveFacility(id: string) {
  try {
    setIsSubmitting(true);
    await api.approveFacility(id);
    toast.success("Facility approved.");
    queryClient.invalidateQueries({ queryKey: ["facility", id] });
  } catch (err) {
    console.error("Failed to approve facility:", err);

    const message =
      err instanceof ApiError && err.status === 409
        ? "This facility has already been approved."
        : "Failed to approve facility. Please try again.";

    toast.error(message);
  } finally {
    setIsSubmitting(false);
  }
}
```

## See Also

- [err-never-swallow](err-never-swallow.md) - Always log or display errors
