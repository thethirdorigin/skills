# doc-intra-links

> Use intra-doc links to reference related types and functions

## Why It Matters

Plain-text references like "See the Config struct" are not clickable in rustdoc. Users must manually search for the type, which breaks their reading flow. Worse, plain-text references do not break when the target is renamed or removed, so they silently go stale.

Intra-doc links — [`Config`], [`Config::builder`], [`crate::auth::Session`] — generate clickable hyperlinks in rustdoc and are checked by the compiler. If the target type is renamed or deleted, cargo doc warns about the broken link. This keeps cross-references accurate and makes documentation navigable.

## Bad

```rust
/// Creates a new server instance.
///
/// See the Config struct for available configuration options.
/// The server uses the default ConnectionPool if none is specified.
/// Errors are returned as ServerError variants.
pub fn new(config: Config) -> Result<Server, ServerError> {
    // ...
}
```

## Good

```rust
/// Creates a new server instance.
///
/// See [`Config`] for available configuration options.
/// The server uses the default [`ConnectionPool`] if none is
/// provided via [`Config::pool`].
///
/// # Errors
///
/// Returns [`ServerError::InvalidConfig`] if the configuration
/// contains conflicting options. See [`ServerError`] for the
/// full list of failure modes.
pub fn new(config: Config) -> Result<Server, ServerError> {
    // ...
}
```

## References

- [C-LINK](https://rust-lang.github.io/api-guidelines/documentation.html#function-docs-include-error-panic-and-safety-considerations-c-failure) — Use intra-doc links for cross-references

## See Also

- [doc-summary-sentence](doc-summary-sentence.md) - Writing the summary line that precedes links
- [doc-module-docs](doc-module-docs.md) - Module-level documentation where links are most valuable
