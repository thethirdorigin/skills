# lint-cargo-hack

> Use cargo-hack to test feature combinations

## Why It Matters

Cargo unifies features across the dependency graph, which means users of your crate may enable feature combinations you never tested locally. A crate that compiles with `--all-features` and with default features may fail when only a single non-default feature is enabled, because a type or import is missing without its companion feature.

`cargo hack` systematically tests feature combinations by checking each feature in isolation, powerset combinations, or specific groupings. This catches compilation failures, missing `cfg` guards, and accidentally non-additive features before users discover them.

## Bad

```rust
// CI only tests two configurations:
// cargo check                        (default features)
// cargo check --all-features         (everything enabled)

// But a user enables only "compression":
// mycrate = { features = ["compression"] }
//
// This fails because compression.rs uses a type from the "encoding"
// module that isn't gated behind its own feature:
#[cfg(feature = "compression")]
pub fn compress(data: &[u8]) -> Vec<u8> {
    let encoded = encode(data); // ERROR: encode() requires "encoding" feature
    zstd::compress(&encoded)
}
```

## Good

```rust
// CI pipeline:
// cargo install cargo-hack
// cargo hack check --each-feature --no-dev-deps

// This tests each feature independently:
//   cargo check --features compression   (catches missing encode dependency)
//   cargo check --features encoding
//   cargo check --features async
//   cargo check --no-default-features

// For thorough testing of feature interactions:
// cargo hack check --feature-powerset --no-dev-deps

// Fix: gate the dependency properly
#[cfg(feature = "compression")]
pub fn compress(data: &[u8]) -> Vec<u8> {
    #[cfg(feature = "encoding")]
    let input = encode(data);
    #[cfg(not(feature = "encoding"))]
    let input = data;
    zstd::compress(input)
}
```

## See Also

- [lint-clippy-all](lint-clippy-all.md) - Run clippy with all features
- [crate-features-additive](crate-features-additive.md) - Features must be additive
