# crate-no-glob-reexport

> Re-export items individually, not via glob re-exports

## Why It Matters

A `pub use internal::*` re-export exposes every public item in the internal module as part of your crate's public API. Adding a new helper function or type to the internal module accidentally becomes a public API addition. Removing or renaming an internal item becomes a breaking change that you never intended.

Explicit re-exports create a curated public API surface. You control exactly what users can import, and internal refactoring does not affect downstream consumers. The list of re-exports also serves as documentation of the crate's public interface.

## Bad

```rust
// src/lib.rs
mod internal;

// Everything in internal is now public API -- including helpers,
// intermediate types, and items you never meant to expose.
pub use internal::*;

// src/internal.rs
pub struct Config { /* ... */ }
pub struct ConfigBuilder { /* ... */ }
pub struct Error { /* ... */ }
pub fn validate_config(c: &Config) -> bool { /* ... */ }  // internal helper, now public
pub(crate) fn parse_raw(input: &str) -> RawConfig { /* ... */ }  // this one is fine

// Adding `pub struct CacheEntry` to internal.rs silently adds it to the public API.
// Removing `validate_config` is now a breaking change.
```

## Good

```rust
// src/lib.rs
mod internal;

// Explicit public API -- only these items are exposed
pub use internal::{Config, ConfigBuilder, Error};

// src/internal.rs
pub struct Config { /* ... */ }
pub struct ConfigBuilder { /* ... */ }
pub struct Error { /* ... */ }
pub fn validate_config(c: &Config) -> bool { /* ... */ }  // remains internal
pub struct CacheEntry { /* ... */ }  // also internal -- not re-exported

// Adding or removing internal items does not affect the public API.
// The re-export list is the single source of truth for what is public.
```

## References

- [M-NO-GLOB-REEXPORTS](https://rust-lang.github.io/api-guidelines/future-proofing.html)

## See Also

- [crate-smaller-focused](crate-smaller-focused.md) - Smaller crates with clear APIs
- [crate-features-additive](crate-features-additive.md) - Features must be additive
