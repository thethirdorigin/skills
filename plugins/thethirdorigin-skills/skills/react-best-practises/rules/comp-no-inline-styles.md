# comp-no-inline-styles

> Use CSS classes matching the project's styling approach instead of inline styles

## Why It Matters

Inline styles bypass the project's styling system entirely. They cannot use media queries, pseudo-classes (`:hover`, `:focus`), pseudo-elements, or the project's design tokens. Every inline style is a one-off value that drifts from the design system over time.

Whether the project uses Tailwind, CSS Modules, styled-components, or plain CSS, the styling approach provides consistency, responsive behaviour, and theming support that inline styles cannot replicate. Match whatever styling convention the project already uses.

## Bad

```tsx
// Inline styles — no hover states, no responsive behaviour, no design tokens
function NotificationBanner({ message }: { message: string }) {
  return (
    <div
      style={{
        marginTop: 16,
        padding: "12px 24px",
        backgroundColor: "#f5f5f5",
        borderRadius: 8,
        border: "1px solid #e0e0e0",
        fontSize: 14,
        color: "#333",
      }}
    >
      <p style={{ margin: 0, fontWeight: 600 }}>{message}</p>
    </div>
  );
}
```

## Good

```tsx
// Tailwind — responsive, themeable, consistent with design system
function NotificationBanner({ message }: { message: string }) {
  return (
    <div className="mt-4 px-6 py-3 bg-gray-100 rounded-lg border border-gray-200">
      <p className="text-sm font-semibold text-gray-800">{message}</p>
    </div>
  );
}

// CSS Modules — scoped styles with full CSS capabilities
import styles from "./NotificationBanner.module.css";

function NotificationBanner({ message }: { message: string }) {
  return (
    <div className={styles.banner}>
      <p className={styles.message}>{message}</p>
    </div>
  );
}
```

## See Also

- [comp-jsx-fragments](comp-jsx-fragments.md) - Use fragments and semantic HTML — avoid unnecessary wrapper divs
