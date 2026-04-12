# crate-workspace-deps

> Use { workspace = true } for shared dependencies -- do not duplicate versions

## Why It Matters

When multiple crates in a workspace each specify their own dependency versions, version drift is inevitable. Crate A pins `serde = "1.0.193"` while crate B uses `serde = "1.0.210"`, leading to multiple versions compiled into the final binary, increased compile times, and potential type mismatches at crate boundaries.

Workspace dependencies centralise version management in the root `Cargo.toml`. Every crate references the shared version with `{ workspace = true }`, and updating a dependency version is a single-line change in one file.

## Bad

```rust
// crate-a/Cargo.toml
// [dependencies]
// serde = { version = "1.0.193", features = ["derive"] }
// tokio = { version = "1.35", features = ["full"] }
// tracing = "0.1.40"

// crate-b/Cargo.toml
// [dependencies]
// serde = { version = "1.0.210", features = ["derive"] }  <-- different version!
// tokio = { version = "1.37", features = ["rt-multi-thread"] }  <-- different version!
// tracing = "0.1.37"  <-- different version!

// Result: multiple serde versions compiled, type mismatches at boundaries,
// and nobody knows which version is "correct."
```

## Good

```rust
// Cargo.toml (workspace root)
// [workspace.dependencies]
// serde = { version = "1.0", features = ["derive"] }
// tokio = { version = "1", features = ["full"] }
// tracing = "0.1"

// crate-a/Cargo.toml
// [dependencies]
// serde = { workspace = true }
// tokio = { workspace = true }
// tracing = { workspace = true }

// crate-b/Cargo.toml
// [dependencies]
// serde = { workspace = true }
// tokio = { workspace = true, features = ["rt-multi-thread"] }  // additive features OK
// tracing = { workspace = true }

// One place to update. All crates stay in sync.
```

## See Also

- [crate-features-additive](crate-features-additive.md) - Features must be additive
- [lint-cargo-audit](lint-cargo-audit.md) - Audit dependencies for vulnerabilities
