# a11y-form-labels

> Associate every form input with a label element or aria-label

## Why It Matters

Screen readers identify form fields by their accessible name, which comes from an associated `<label>`, `aria-label`, or `aria-labelledby` attribute. An input with only a `placeholder` attribute has no accessible name — the placeholder text disappears when the user starts typing, leaving them with no way to verify which field they are editing. Screen readers may announce the input as simply "edit text" with no context.

Proper labelling also improves usability for sighted users: clicking a `<label>` focuses its associated input, expanding the clickable area. This is especially helpful on mobile devices and for users with motor difficulties who need a larger hit target.

## Bad

```tsx
function LoginForm() {
  return (
    <form>
      {/* Placeholder is not a label — disappears on focus,
          invisible to screen readers as a field name */}
      <input type="email" placeholder="Email" />
      <input type="password" placeholder="Password" />

      {/* Visual text nearby but not programmatically associated */}
      <span>Phone number</span>
      <input type="tel" />

      <button type="submit">Log In</button>
    </form>
  );
}
```

## Good

```tsx
function LoginForm() {
  return (
    <form>
      {/* Explicit label with htmlFor — click label to focus input */}
      <div>
        <label htmlFor="email">Email address</label>
        <input id="email" type="email" placeholder="you@example.com" />
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" />
      </div>

      {/* aria-label works when a visible label is not desired */}
      <div>
        <input
          type="tel"
          aria-label="Phone number"
          placeholder="(555) 123-4567"
        />
      </div>

      {/* aria-labelledby for complex label compositions */}
      <div>
        <span id="amount-label">Donation amount</span>
        <span id="amount-currency">(USD)</span>
        <input
          type="number"
          aria-labelledby="amount-label amount-currency"
          min={1}
        />
      </div>

      <button type="submit">Log In</button>
    </form>
  );
}
```

## See Also

- [a11y-aria-labels](a11y-aria-labels.md) - Provide aria-label for icon-only buttons and non-text interactive elements
