# comp-one-per-file

> Export one page-level component per file — helper components may coexist if unexported

## Why It Matters

One exported component per file makes components easy to find, import, and code-split. When a file exports multiple page-level components, imports become ambiguous, tree-shaking is less effective, and developers must read the entire file to understand which component they need.

Small private helper components that exist solely to support the main component are an implementation detail. Keeping them in the same file avoids polluting the directory with tiny single-use files while still maintaining a clear public API of one export per file.

## Bad

```tsx
// UserPage.tsx — two exported page-level components in one file
export function UserProfile({ user }: UserProfileProps) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}

export function UserSettings({ user }: UserSettingsProps) {
  return (
    <form>
      <label>Display Name</label>
      <input defaultValue={user.name} />
    </form>
  );
}
```

## Good

```tsx
// UserProfile.tsx — one exported component, private helper coexists
function AvatarBadge({ status }: { status: "online" | "offline" }) {
  return (
    <span className={`badge badge-${status}`} aria-label={status}>
      {status === "online" ? "●" : "○"}
    </span>
  );
}

export function UserProfile({ user }: UserProfileProps) {
  return (
    <div>
      <AvatarBadge status={user.status} />
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

## See Also

- [comp-functional-only](comp-functional-only.md) - Use function declarations for components
