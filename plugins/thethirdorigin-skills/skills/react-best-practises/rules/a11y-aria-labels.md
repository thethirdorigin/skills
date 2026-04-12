# a11y-aria-labels

> Provide aria-label for icon-only buttons and non-text interactive elements

## Why It Matters

Screen readers derive an accessible name from an element's text content, its associated `<label>`, or its `aria-label`/`aria-labelledby` attributes. An icon-only button contains no text — its SVG or icon font glyph is meaningless to assistive technology. Without an accessible name, a screen reader announces it as simply "button," leaving the user with no idea what it does.

This applies to any interactive element whose purpose is communicated visually rather than through text: icon buttons, image links, toggle switches with only icons, and close buttons represented by an "X" glyph. Adding `aria-label` takes seconds and makes the difference between a usable and an unusable interface for screen reader users.

## Bad

```tsx
import { Trash2, Settings, X, Search } from "lucide-react";

function Toolbar() {
  return (
    <div className="flex gap-2">
      {/* Screen reader announces: "button", "button", "button", "button" */}
      <button onClick={handleDelete}>
        <Trash2 size={20} />
      </button>
      <button onClick={handleSettings}>
        <Settings size={20} />
      </button>
      <button onClick={handleSearch}>
        <Search size={20} />
      </button>
    </div>
  );
}

function Modal({ onClose }: { onClose: () => void }) {
  return (
    <div className="modal">
      <button className="modal-close" onClick={onClose}>
        <X size={16} />
      </button>
      {/* ... */}
    </div>
  );
}
```

## Good

```tsx
import { Trash2, Settings, X, Search } from "lucide-react";

function Toolbar() {
  return (
    <div className="flex gap-2" role="toolbar" aria-label="Item actions">
      <button aria-label="Delete item" onClick={handleDelete}>
        <Trash2 size={20} aria-hidden="true" />
      </button>
      <button aria-label="Open settings" onClick={handleSettings}>
        <Settings size={20} aria-hidden="true" />
      </button>
      <button aria-label="Search" onClick={handleSearch}>
        <Search size={20} aria-hidden="true" />
      </button>
    </div>
  );
}

function Modal({ onClose, title }: { onClose: () => void; title: string }) {
  return (
    <div className="modal" role="dialog" aria-label={title}>
      <button aria-label="Close dialog" onClick={onClose}>
        <X size={16} aria-hidden="true" />
      </button>
      {/* ... */}
    </div>
  );
}
```

## See Also

- [a11y-form-labels](a11y-form-labels.md) - Associate every form input with a label element or aria-label
