# a11y-semantic-html

> Use semantic HTML elements for their intended purpose

## Why It Matters

Semantic HTML elements like `<button>`, `<nav>`, `<main>`, and `<article>` carry built-in behavior and meaning. A `<button>` is focusable, responds to Enter and Space keys, and is announced as a button by screen readers without any additional code. A `<div>` doing the same job requires manual `tabIndex`, `role`, `onKeyDown` handlers, and careful ARIA attributes to achieve the same result — and most implementations miss something.

Choosing the correct element means assistive technologies can build an accurate model of your page. Screen readers use landmarks like `<nav>` and `<main>` to let users jump between sections. Search engines use heading hierarchy to understand content structure. The browser provides default styles, focus management, and form submission behavior. Using divs and spans for everything throws all of this away and forces you to rebuild it poorly.

## Bad

```tsx
function Navigation({ links }: { links: { href: string; label: string }[] }) {
  return (
    <div className="nav-bar">
      {links.map((link) => (
        <div
          key={link.href}
          className="nav-link"
          onClick={() => window.location.href = link.href}
        >
          {link.label}
        </div>
      ))}
    </div>
  );
}

function DeleteButton({ onDelete }: { onDelete: () => void }) {
  // Not focusable, no keyboard support, not announced as a button
  return (
    <div className="btn btn-danger" onClick={onDelete}>
      Delete
    </div>
  );
}
```

## Good

```tsx
function Navigation({ links }: { links: { href: string; label: string }[] }) {
  return (
    <nav aria-label="Main navigation">
      <ul>
        {links.map((link) => (
          <li key={link.href}>
            <a href={link.href}>{link.label}</a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

function DeleteButton({ onDelete }: { onDelete: () => void }) {
  return (
    <button type="button" className="btn btn-danger" onClick={onDelete}>
      Delete
    </button>
  );
}
```

## See Also

- [a11y-role-sparingly](a11y-role-sparingly.md) - Use role attributes only when semantic HTML elements are not appropriate
