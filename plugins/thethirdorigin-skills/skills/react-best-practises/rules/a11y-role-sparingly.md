# a11y-role-sparingly

> Use role attributes only when semantic HTML elements are not appropriate

## Why It Matters

The `role` attribute tells assistive technology what an element represents, but it does not provide the behavior that semantic elements include by default. A `<div role="button">` is announced as a button, but it is not focusable, does not respond to Enter or Space keys, and does not participate in form submission. You must add `tabIndex`, `onKeyDown`, and other handlers manually, and most implementations are incomplete.

A native `<button>` provides all of this for free. The `role` attribute should be reserved for truly custom widgets that have no semantic HTML equivalent — composite widgets like tree views, grids, or tabbed interfaces where the underlying structure is necessarily built from generic elements.

## Bad

```tsx
function ActionBar({ onSave, onCancel }: {
  onSave: () => void;
  onCancel: () => void;
}) {
  return (
    <div role="toolbar">
      {/* role="button" on a div — not focusable, no keyboard support */}
      <div role="button" onClick={onSave} className="btn-primary">
        Save
      </div>
      <div role="button" onClick={onCancel} className="btn-secondary">
        Cancel
      </div>
    </div>
  );
}

function PageLayout({ children }: { children: React.ReactNode }) {
  return (
    <div role="main">
      <div role="navigation">
        <div role="link" onClick={() => navigate("/home")}>Home</div>
      </div>
      {children}
    </div>
  );
}
```

## Good

```tsx
function ActionBar({ onSave, onCancel }: {
  onSave: () => void;
  onCancel: () => void;
}) {
  return (
    <div role="toolbar" aria-label="Form actions">
      {/* Native buttons — focusable, keyboard-accessible, correct role */}
      <button type="button" onClick={onSave} className="btn-primary">
        Save
      </button>
      <button type="button" onClick={onCancel} className="btn-secondary">
        Cancel
      </button>
    </div>
  );
}

function PageLayout({ children }: { children: React.ReactNode }) {
  return (
    <main>
      <nav aria-label="Primary">
        <a href="/home">Home</a>
      </nav>
      {children}
    </main>
  );
}

// Role is appropriate here — no native HTML element for a tree view
function FileTree({ nodes }: { nodes: TreeNode[] }) {
  return (
    <ul role="tree" aria-label="File explorer">
      {nodes.map((node) => (
        <li key={node.id} role="treeitem" aria-expanded={node.isExpanded}>
          {node.name}
          {node.children && (
            <ul role="group">
              {/* Recursive children */}
            </ul>
          )}
        </li>
      ))}
    </ul>
  );
}
```

## See Also

- [a11y-semantic-html](a11y-semantic-html.md) - Use semantic HTML elements for their intended purpose
