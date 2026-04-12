# comp-jsx-fragments

> Use fragments and semantic HTML — avoid unnecessary wrapper divs

## Why It Matters

Extra wrapper divs add DOM weight, break CSS layout assumptions (flexbox and grid count direct children), and reduce accessibility. A `<div>` carries no semantic meaning — screen readers cannot infer the purpose of nested divs.

Fragments (`<>...</>`) add zero DOM nodes, keeping the rendered output clean. When a wrapper element is needed for layout or styling, use semantic HTML elements (`<article>`, `<section>`, `<nav>`, `<header>`) that convey meaning to assistive technologies and improve SEO.

## Bad

```tsx
// Unnecessary wrapper divs — breaks parent flexbox, adds DOM noise
function PageHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div>
      <div>
        <div>
          <h1>{title}</h1>
        </div>
        <div>
          <p>{subtitle}</p>
        </div>
      </div>
    </div>
  );
}

// Parent uses flexbox expecting direct children, but gets a single div wrapper
function Navigation({ items }: { items: NavItem[] }) {
  return (
    <div> {/* This div becomes the only flex child */}
      {items.map((item) => (
        <a key={item.href} href={item.href}>{item.label}</a>
      ))}
    </div>
  );
}
```

## Good

```tsx
// Fragment — no extra DOM nodes
function PageHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </>
  );
}

// Semantic HTML when a wrapper is needed
function Navigation({ items }: { items: NavItem[] }) {
  return (
    <nav aria-label="Main navigation">
      {items.map((item) => (
        <a key={item.href} href={item.href}>{item.label}</a>
      ))}
    </nav>
  );
}
```

## See Also

- [a11y-semantic-html](a11y-semantic-html.md) - Use semantic HTML elements for accessibility
