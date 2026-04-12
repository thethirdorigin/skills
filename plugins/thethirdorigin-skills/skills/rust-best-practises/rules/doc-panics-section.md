# doc-panics-section

> Document panic conditions with a Panics section

## Why It Matters

A function that panics under certain inputs will crash the caller's program. If the panic conditions are undocumented, callers discover them only through runtime failures — often in production. This is especially dangerous for library code where the caller has no control over the implementation.

A Panics section explicitly lists every condition under which the function will panic. This allows callers to validate their inputs before calling, add defensive checks, or choose an alternative API. It also signals to reviewers that the panic is intentional, not a bug.

## Bad

```rust
/// Returns the element at the given index.
pub fn get_unchecked(&self, index: usize) -> &T {
    // Panics if index >= len, but callers have no way to know
    // without reading the source.
    &self.data[index]
}
```

## Good

```rust
/// Returns a reference to the element at the given index.
///
/// # Panics
///
/// Panics if `index` is greater than or equal to the buffer length.
/// Use [`get`](Self::get) for a non-panicking alternative that returns `Option<&T>`.
pub fn get_unchecked(&self, index: usize) -> &T {
    &self.data[index]
}
```

## See Also

- [doc-errors-section](doc-errors-section.md) - Documenting recoverable error conditions
- [doc-safety-section](doc-safety-section.md) - Documenting unsafe function requirements
- [err-panic-bugs-only](err-panic-bugs-only.md) - When panics are appropriate
