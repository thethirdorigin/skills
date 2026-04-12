# fmt-single-line-small

> Use single-line format for small items

## Why It Matters

Spreading tiny expressions across multiple lines wastes vertical space and makes code harder to scan. When a struct literal, tuple, or simple expression fits comfortably within the line width, keeping it on one line improves readability by reducing the amount of code a reader must scroll through.

rustfmt already collapses small items onto single lines when they fit. Writing them this way manually keeps your code consistent with formatted output.

## Bad

```rust
// Unnecessarily verbose for a two-field struct
let point = Point {
    x,
    y,
};

// Simple Ok wrapping doesn't need three lines
let result = Ok(
    value,
);

// Trivial enum variant construction
let color = Color::Rgb(
    255,
    0,
    0,
);
```

## Good

```rust
// Compact — fits well within line width
let point = Point { x, y };

// Simple wrapping on one line
let result = Ok(value);

// Trivial construction stays inline
let color = Color::Rgb(255, 0, 0);
```

## See Also

- [fmt-line-width](fmt-line-width.md) - Keep lines under 100 characters
