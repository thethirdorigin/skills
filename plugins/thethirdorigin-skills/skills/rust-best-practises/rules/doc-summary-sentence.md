# doc-summary-sentence

> Start every public item's doc comment with a summary sentence under 15 words

## Why It Matters

The summary sentence is the most-read line of any documentation. It appears in IDE hover tooltips, rustdoc module listings, and search results. When a developer scans a list of 30 functions, they read the first sentence of each to find the one they need. A long, rambling opener forces them to read an entire paragraph before deciding if the item is relevant.

Keep the summary sentence short, imperative, and specific. It should answer "what does this do?" in a single breath. Save details, caveats, and examples for subsequent paragraphs.

## Bad

```rust
/// This function is responsible for taking a user ID as input, querying the
/// database to find the corresponding user record, and returning it wrapped
/// in a Result type that indicates whether the operation succeeded or failed.
pub fn find_user(id: UserId) -> Result<User, DbError> {
    // ...
}
```

## Good

```rust
/// Finds a user by their unique identifier.
///
/// Queries the primary database and returns the full user record.
/// Returns `Err(DbError::NotFound)` if no user exists with the given ID.
///
/// # Errors
///
/// - [`DbError::NotFound`] if the user does not exist.
/// - [`DbError::Connection`] if the database is unreachable.
pub fn find_user(id: UserId) -> Result<User, DbError> {
    // ...
}
```

## References

- [M-FIRST-DOC-SENTENCE](https://rust-lang.github.io/api-guidelines/documentation.html) — First line is a short summary sentence

## See Also

- [doc-errors-section](doc-errors-section.md) - Documenting error conditions
- [doc-examples-runnable](doc-examples-runnable.md) - Adding runnable examples
