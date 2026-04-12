# test-doc-examples

> Keep doc examples as executable tests -- they run with cargo test

## Why It Matters

Rust's doc tests are unique: code blocks inside `///` comments compile and execute as part of `cargo test`. This means your documentation is always verified against the actual API. When a function signature changes, broken doc examples fail the test suite immediately rather than silently misleading users.

Prose-only documentation or commented-out code examples rot over time. Executable doc examples serve double duty as both documentation and regression tests, ensuring that the examples users copy-paste actually work.

## Bad

```rust
/// Parses a duration string like "5s" or "100ms".
///
/// Usage: call `parse_duration("5s")` to get a Duration.
/// You can also use "ms" for milliseconds.
pub fn parse_duration(input: &str) -> Result<Duration, ParseError> {
    // ...
}

// The documentation describes usage in prose but provides no
// compilable example. If the API changes, the docs become wrong
// and nobody notices.
```

## Good

```rust
/// Parses a duration string like `"5s"` or `"100ms"`.
///
/// # Examples
///
/// ```
/// use my_crate::parse_duration;
/// use std::time::Duration;
///
/// let d = parse_duration("5s").unwrap();
/// assert_eq!(d, Duration::from_secs(5));
///
/// let d = parse_duration("100ms").unwrap();
/// assert_eq!(d, Duration::from_millis(100));
/// ```
///
/// # Errors
///
/// Returns [`ParseError::InvalidUnit`] for unrecognised suffixes:
///
/// ```
/// use my_crate::{parse_duration, ParseError};
///
/// let err = parse_duration("5x").unwrap_err();
/// assert!(matches!(err, ParseError::InvalidUnit { .. }));
/// ```
pub fn parse_duration(input: &str) -> Result<Duration, ParseError> {
    // ...
}
```

## See Also

- [test-cfg-module](test-cfg-module.md) - Unit tests belong in the same file
- [test-error-paths](test-error-paths.md) - Test error paths explicitly
