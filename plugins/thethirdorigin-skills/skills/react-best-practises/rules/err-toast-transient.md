# err-toast-transient

> Use the project's toast/notification system for transient errors

## Why It Matters

`alert()` blocks the main thread and halts all JavaScript execution until the user dismisses it. It cannot be styled, does not auto-dismiss, and breaks the flow of the application. `console.error()` is invisible to users -- they have no idea something went wrong.

Toast notifications are non-blocking, auto-dismiss after a timeout, and follow the project's visual design system. They stack cleanly when multiple events occur and can be configured with different severity levels (success, warning, error) to communicate the nature of the feedback.

## Bad

```tsx
// alert() blocks the UI thread — user cannot interact until dismissed
async function handleSave(data: FormData) {
  try {
    await api.saveFacility(data);
    alert("Saved successfully!");
  } catch (err) {
    alert("Something went wrong");
  }
}

// console.error only — user gets no feedback at all
async function handleDelete(id: string) {
  try {
    await api.deleteFacility(id);
  } catch (err) {
    console.error("Delete failed:", err);
    // User clicks delete, nothing visible happens, data remains
  }
}

// Custom inline error state for a transient action — over-engineered
const [saveError, setSaveError] = useState<string | null>(null);
// Now you need to clear it, position it, animate it...
```

## Good

```tsx
import { toast } from "@/components/ui/toast";

async function handleSave(data: FormData) {
  try {
    await api.saveFacility(data);
    toast.success("Facility saved successfully.");
  } catch (err) {
    console.error("Failed to save facility:", err);
    toast.error("Failed to save facility. Please try again.");
  }
}

async function handleDelete(id: string) {
  try {
    await api.deleteFacility(id);
    toast.success("Facility deleted.");
    navigate("/facilities");
  } catch (err) {
    console.error("Failed to delete facility:", err);
    toast.error("Failed to delete facility. Please try again.");
  }
}

// For actions with specific known error cases
async function handleApprove(id: string) {
  try {
    await api.approveFacility(id);
    toast.success("Facility approved and activated.");
  } catch (err) {
    console.error("Failed to approve facility:", err);
    if (err instanceof ApiError && err.status === 403) {
      toast.error("You do not have permission to approve facilities.");
    } else {
      toast.error("Failed to approve facility. Please try again.");
    }
  }
}
```

## See Also

- [err-try-catch-async](err-try-catch-async.md) - Wrap async operations in try-catch with user-facing error messages
