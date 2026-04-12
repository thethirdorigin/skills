# a11y-focus-management

> Maintain visible focus indicators and logical tab order

## Why It Matters

Keyboard users rely on focus indicators to know where they are on the page, the same way mouse users rely on the cursor. Removing the default outline with `outline: none` without providing a replacement makes the page completely unusable for keyboard navigation — users press Tab and have no idea which element is selected. This is one of the most common and most damaging accessibility failures.

The `:focus-visible` pseudo-class solves the design concern that motivated removing outlines in the first place: it shows focus styles only for keyboard navigation, not for mouse clicks. This gives you clean visual design for mouse users while preserving essential navigation cues for keyboard users. Combined with logical tab order (following the visual reading flow), focus management creates a predictable, navigable interface.

## Bad

```tsx
// Global CSS that removes all focus indicators
// * { outline: none; }
// *:focus { outline: 0; }

function Card({ title, onEdit }: { title: string; onEdit: () => void }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {/* tabIndex creates a confusing tab order — this div gets focus
          before logically earlier interactive elements */}
      <div tabIndex={5} onClick={onEdit} className="edit-link">
        Edit
      </div>
    </div>
  );
}

function SearchPage() {
  return (
    <div>
      {/* Using positive tabIndex forces unnatural tab order */}
      <input tabIndex={3} placeholder="Search..." />
      <button tabIndex={1}>Filters</button>
      <button tabIndex={2}>Sort</button>
    </div>
  );
}
```

## Good

```tsx
// Global focus styles that only appear for keyboard navigation
// *:focus-visible {
//   outline: 2px solid var(--focus-color, #2563eb);
//   outline-offset: 2px;
// }

function Card({ title, onEdit }: { title: string; onEdit: () => void }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {/* Native button — naturally in tab order, no explicit tabIndex needed */}
      <button type="button" onClick={onEdit}>
        Edit
      </button>
    </div>
  );
}

function SearchPage() {
  return (
    <div>
      {/* DOM order matches visual order — natural tab sequence */}
      <input placeholder="Search..." aria-label="Search" />
      <button type="button">Filters</button>
      <button type="button">Sort</button>
    </div>
  );
}

// Managing focus after dynamic content changes (e.g., opening a modal)
function useModalFocus(isOpen: boolean) {
  const previousFocus = useRef<HTMLElement | null>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  return modalRef;
}
```

## See Also

- [a11y-keyboard-nav](a11y-keyboard-nav.md) - Ensure keyboard navigation works for all interactive elements
