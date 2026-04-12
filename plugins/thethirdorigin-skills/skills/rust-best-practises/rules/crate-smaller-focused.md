# crate-smaller-focused

> Prefer smaller, focused crates over monolithic ones

## Why It Matters

A monolithic crate with dozens of modules covering unrelated concerns creates several problems. Compile times suffer because any change recompiles the entire crate. Dependency graphs become tangled because every module can access every other module's internals. API boundaries blur because there is no forced separation between subsystems.

Smaller, focused crates compile in parallel, enforce clear dependency directions through `Cargo.toml`, and present well-defined public APIs. When you modify the `email` crate, only crates that depend on `email` recompile -- not the entire workspace.

## Bad

```rust
// src/lib.rs -- one massive crate doing everything
pub mod auth;
pub mod database;
pub mod api;
pub mod email;
pub mod reporting;
pub mod cache;
pub mod queue;
pub mod billing;

// auth/ can reach into database/ internals
// email/ depends on queue/ which depends on database/
// Circular dependencies form silently within the module tree.
// Changing a database model recompiles all 50 modules.
```

## Good

```rust
// Cargo.toml (workspace)
// [workspace]
// members = [
//     "crates/auth",
//     "crates/db",
//     "crates/api",
//     "crates/email",
//     "crates/reporting",
// ]

// crates/auth/Cargo.toml
// [dependencies]
// db = { path = "../db" }

// crates/email/Cargo.toml
// [dependencies]
// db = { path = "../db" }  -- explicit dependency
// auth is NOT listed -- email cannot access auth internals

// crates/api/Cargo.toml
// [dependencies]
// auth = { path = "../auth" }
// db = { path = "../db" }
// email = { path = "../email" }

// Clear dependency direction: api -> auth -> db
// Modifying email only recompiles email and api.
```

## References

- [M-SMALLER-CRATES](https://rust-lang.github.io/api-guidelines/future-proofing.html)

## See Also

- [crate-workspace-deps](crate-workspace-deps.md) - Centralise shared dependency versions
- [crate-no-glob-reexport](crate-no-glob-reexport.md) - Explicit public API surface
