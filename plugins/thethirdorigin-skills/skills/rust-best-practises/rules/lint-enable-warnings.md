# lint-enable-warnings

> Enable key compiler lints at workspace level

## Why It Matters

Rust's default lint configuration is conservative -- many useful warnings are off by default to avoid overwhelming new users. Enabling additional lints at the workspace level catches issues early and consistently across all crates in the workspace.

Workspace-level configuration in `Cargo.toml` applies to every crate automatically. New crates inherit the same standards without developers remembering to add lint attributes. This eliminates the pattern of discovering lint violations months after the code was written.

## Bad

```rust
// No workspace-level lint configuration.
// Each crate relies on compiler defaults.
// Useful warnings like unused lifetimes, missing Debug impls,
// and ambiguous negative literals go undetected.

// Cargo.toml
// [workspace]
// members = ["crate-a", "crate-b", "crate-c"]
// (no lint section)

// This compiles without warning despite the ambiguity:
let x = -1i32.abs(); // Is this -(1.abs()) or (-1).abs()?
```

## Good

```rust
// Cargo.toml (workspace root)
// [workspace.lints.rust]
// ambiguous_negative_literals = "warn"
// missing_debug_implementations = "warn"
// unused_lifetimes = "warn"
// unsafe_op_in_unsafe_fn = "warn"
// elided_lifetimes_in_paths = "warn"
// trivial_numeric_casts = "warn"
//
// [workspace.lints.clippy]
// doc_markdown = "warn"
// manual_let_else = "warn"
// needless_pass_by_value = "warn"
// redundant_closure_for_method_calls = "warn"

// Each crate's Cargo.toml inherits workspace lints:
// [lints]
// workspace = true

// Now this triggers a warning at compile time:
let x = -1i32.abs(); // warning: ambiguous negative literal
let x = (-1i32).abs(); // Clear: absolute value of -1
```

## See Also

- [lint-clippy-all](lint-clippy-all.md) - Run clippy with all targets and features
- [lint-cargo-fmt](lint-cargo-fmt.md) - Enforce consistent formatting
