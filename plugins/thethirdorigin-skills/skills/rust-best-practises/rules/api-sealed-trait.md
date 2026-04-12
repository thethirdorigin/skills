# api-sealed-trait

> Seal traits to prevent external implementations when needed

## Why It Matters

Adding a new required method to a public trait is a breaking change — every downstream implementation must be updated. This forces library authors to either never evolve their traits or to release major versions for every addition. Sealed traits solve this by restricting implementations to the defining crate.

A sealed trait uses a private supertrait that external crates cannot access. Since no external crate can implement the private supertrait, they cannot implement the sealed trait either. This allows the library to add new methods freely in minor versions. Use sealing for extension traits, marker traits, and internal abstractions where external implementations would be incorrect or unsupported.

## Bad

```rust
// Any crate can implement this trait
pub trait Encoder {
    fn encode(&self, data: &[u8]) -> Vec<u8>;
    fn content_type(&self) -> &str;
}

// Six months later, you need to add a new method:
pub trait Encoder {
    fn encode(&self, data: &[u8]) -> Vec<u8>;
    fn content_type(&self) -> &str;
    fn encoding_name(&self) -> &str; // BREAKING CHANGE — all external impls fail
}
```

## Good

```rust
mod private {
    pub trait Sealed {}
}

/// Encoder trait for supported content encodings.
///
/// This trait is sealed and cannot be implemented outside this crate.
pub trait Encoder: private::Sealed {
    fn encode(&self, data: &[u8]) -> Vec<u8>;
    fn content_type(&self) -> &str;
}

pub struct GzipEncoder;
pub struct BrotliEncoder;

impl private::Sealed for GzipEncoder {}
impl private::Sealed for BrotliEncoder {}

impl Encoder for GzipEncoder {
    fn encode(&self, data: &[u8]) -> Vec<u8> {
        gzip_compress(data)
    }

    fn content_type(&self) -> &str {
        "application/gzip"
    }
}

impl Encoder for BrotliEncoder {
    fn encode(&self, data: &[u8]) -> Vec<u8> {
        brotli_compress(data)
    }

    fn content_type(&self) -> &str {
        "application/br"
    }
}

// Adding a new method in a minor version is safe:
// No external crate can implement Encoder, so no one breaks.
pub trait Encoder: private::Sealed {
    fn encode(&self, data: &[u8]) -> Vec<u8>;
    fn content_type(&self) -> &str;
    fn encoding_name(&self) -> &str; // Non-breaking addition
}
```

## References

- [C-SEALED](https://rust-lang.github.io/api-guidelines/future-proofing.html#sealed-traits-protect-against-downstream-implementations-c-sealed)

## See Also

- [api-object-safe](api-object-safe.md) - Object safety for trait objects
- [api-essential-inherent](api-essential-inherent.md) - When to use inherent methods vs traits
