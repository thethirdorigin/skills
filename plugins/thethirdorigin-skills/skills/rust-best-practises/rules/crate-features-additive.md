# crate-features-additive

> Features must be additive -- enabling a feature must not disable public items

## Why It Matters

Cargo unifies features across the entire dependency graph. If crate A depends on your library with the "advanced" feature and crate B depends on it with only the default features, Cargo enables "advanced" for both. If enabling "advanced" removes a public item that crate B relies on, the build breaks with a confusing error that neither crate owner caused.

Additive features only add capabilities: new types, new methods, new trait implementations. They never remove or replace existing public API surface. This guarantees that any combination of features is a superset of each individual feature.

## Bad

```rust
// Enabling "advanced" removes basic_parse -- not additive!
#[cfg(not(feature = "advanced"))]
pub fn basic_parse(input: &str) -> Result<Value, Error> {
    // Simple parser for basic use cases
    simple_parser::parse(input)
}

#[cfg(feature = "advanced")]
pub fn advanced_parse(input: &str) -> Result<Ast, Error> {
    // Full AST parser
    ast_parser::parse(input)
}

// Crate A: mycrate = { features = ["advanced"] }
// Crate B: mycrate = {}  -- expects basic_parse to exist
// Cargo enables "advanced" for both --> basic_parse disappears --> crate B fails
```

## Good

```rust
// basic_parse is always available -- no cfg gate
pub fn basic_parse(input: &str) -> Result<Value, Error> {
    simple_parser::parse(input)
}

// advanced_parse is added when the feature is enabled -- purely additive
#[cfg(feature = "advanced")]
pub fn advanced_parse(input: &str) -> Result<Ast, Error> {
    ast_parser::parse(input)
}

// Both features can coexist. Enabling "advanced" adds functionality
// without removing anything.
```

## References

- [M-FEATURES-ADDITIVE](https://rust-lang.github.io/api-guidelines/future-proofing.html)

## See Also

- [crate-workspace-deps](crate-workspace-deps.md) - Centralise dependency versions
- [lint-cargo-hack](lint-cargo-hack.md) - Test feature combinations
