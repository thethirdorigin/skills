# a11y-color-contrast

> Meet WCAG 2.1 AA contrast ratios (4.5:1 normal text, 3:1 large text)

## Why It Matters

Low contrast text is not just an accessibility concern for users with visual impairments — it affects everyone. Users reading on mobile devices in sunlight, older monitors with faded displays, or aging eyes that naturally lose contrast sensitivity all struggle with insufficient color contrast. The WCAG AA standard of 4.5:1 for normal text and 3:1 for large text (18px+ bold or 24px+ regular) is the minimum threshold for comfortable reading across these conditions.

Failing to meet contrast requirements excludes a significant portion of your audience and can also create legal liability under accessibility regulations. Contrast issues are among the most commonly cited WCAG violations in accessibility audits.

## Bad

```tsx
// Light grey on white — contrast ratio 2.3:1 (fails AA)
function StatusMessage({ message }: { message: string }) {
  return (
    <p style={{ color: "#aaaaaa", backgroundColor: "#ffffff" }}>
      {message}
    </p>
  );
}

// Subtle placeholder-style text used for actual content
function EmptyState() {
  return (
    <div className="flex flex-col items-center py-12">
      {/* #999 on #f5f5f5 = 2.8:1 — fails AA for normal text */}
      <p style={{ color: "#999999", backgroundColor: "#f5f5f5" }}>
        No items found. Try adjusting your filters.
      </p>
    </div>
  );
}
```

## Good

```tsx
// Dark text on white — contrast ratio 7.4:1 (passes AAA)
function StatusMessage({ message }: { message: string }) {
  return (
    <p style={{ color: "#595959", backgroundColor: "#ffffff" }}>
      {message}
    </p>
  );
}

// Use CSS custom properties for consistent, tested contrast
function EmptyState() {
  return (
    <div className="flex flex-col items-center py-12">
      {/* --text-secondary on --bg-surface verified at 5.2:1 */}
      <p className="text-secondary bg-surface">
        No items found. Try adjusting your filters.
      </p>
    </div>
  );
}

// Define contrast-safe design tokens
// :root {
//   --text-primary: #1a1a1a;     /* 16.6:1 on white */
//   --text-secondary: #595959;   /* 7.4:1 on white */
//   --text-disabled: #767676;    /* 4.5:1 on white — minimum AA */
//   --bg-surface: #ffffff;
// }
```

## See Also
