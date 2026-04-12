# api-non-exhaustive

> Use #[non_exhaustive] on public enums and structs to allow future additions

## Why It Matters

Without `#[non_exhaustive]`, adding a new variant to a public enum is a breaking change -- every downstream `match` that exhaustively covers all variants will fail to compile. Similarly, adding a new field to a public struct with public fields breaks every struct literal construction site in downstream code. This forces library authors into painful semver-major bumps for routine additions.

The `#[non_exhaustive]` attribute tells the compiler that the type may gain new variants or fields in the future. Downstream code must include a wildcard arm (`_ =>`) in matches and cannot construct the struct directly, preserving your ability to evolve the API freely in minor versions. Within the defining crate, the attribute has no effect -- you can still match exhaustively and construct freely.

## Bad

```rust
/// Errors that can occur during document processing.
#[derive(Debug, thiserror::Error)]
pub enum ProcessingError {
    #[error("document not found: {0}")]
    NotFound(String),
    #[error("access denied for document: {0}")]
    Unauthorized(String),
}

// Six months later, you need to add a new variant:
//   RateLimited { retry_after: Duration }
// This is a BREAKING CHANGE -- every downstream match fails:
//
//   match err {
//       ProcessingError::NotFound(id) => ...,
//       ProcessingError::Unauthorized(id) => ...,
//       // ERROR: non-exhaustive pattern -- ProcessingError::RateLimited not covered
//   }

/// Configuration for the export pipeline.
pub struct ExportConfig {
    pub format: OutputFormat,
    pub compression: bool,
}

// Adding `pub quality: u8` later breaks all downstream construction:
//   ExportConfig { format: Csv, compression: true }
//   // ERROR: missing field `quality`
```

## Good

```rust
/// Errors that can occur during document processing.
#[derive(Debug, thiserror::Error)]
#[non_exhaustive]
pub enum ProcessingError {
    #[error("document not found: {0}")]
    NotFound(String),
    #[error("access denied for document: {0}")]
    Unauthorized(String),
}

// Downstream code is forced to include a wildcard arm:
//   match err {
//       ProcessingError::NotFound(id) => ...,
//       ProcessingError::Unauthorized(id) => ...,
//       _ => handle_unknown_error(err),
//   }
//
// Adding RateLimited in a minor version is now non-breaking.

/// Configuration for the export pipeline.
#[non_exhaustive]
pub struct ExportConfig {
    pub format: OutputFormat,
    pub compression: bool,
}

impl ExportConfig {
    /// Create a new config with sensible defaults.
    pub fn new(format: OutputFormat) -> Self {
        Self {
            format,
            compression: false,
        }
    }
}

// Downstream must use the constructor + field mutation, not struct literals.
// Adding new fields with defaults in minor versions is non-breaking.
```

## References

- [C-STRUCT-PRIVATE / extensibility](https://rust-unofficial.github.io/patterns/idioms/priv-extend.html)

## See Also

- [api-private-fields](api-private-fields.md) - Keep struct fields private with accessor methods
- [api-sealed-trait](api-sealed-trait.md) - Seal traits to prevent external implementations
