# api-enum-over-bool

> Use enums instead of bool parameters for better call-site readability

## Why It Matters

A `bool` parameter is meaningless at the call site. Readers see `true` or `false` but must jump to the function signature to understand what it controls. This problem compounds when a function takes multiple booleans — `process(data, true, false, true)` is impenetrable without documentation.

Enums name each variant, making the call site self-documenting. They are also extensible: adding a third variant to an enum is a minor change, while replacing a bool with an enum is a breaking change.

## Bad

```rust
pub fn compress(data: &[u8], fast: bool) -> Vec<u8> {
    // ...
}

pub fn send_email(to: &str, subject: &str, body: &str, html: bool, urgent: bool) {
    // ...
}

// At the call site, what do these booleans mean?
compress(&payload, true);
send_email("alice@example.com", "Hello", "Hi there", true, false);
```

## Good

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompressionStrategy {
    Fast,
    BestRatio,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ContentType {
    PlainText,
    Html,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Priority {
    Normal,
    Urgent,
}

pub fn compress(data: &[u8], strategy: CompressionStrategy) -> Vec<u8> {
    // ...
}

pub fn send_email(to: &str, subject: &str, body: &str, content: ContentType, priority: Priority) {
    // ...
}

// Call sites are now self-documenting:
compress(&payload, CompressionStrategy::Fast);
send_email("alice@example.com", "Hello", "Hi there", ContentType::Html, Priority::Normal);
```

## References

- [C-CUSTOM-TYPE](https://rust-lang.github.io/api-guidelines/type-safety.html#arguments-convey-meaning-through-types-not-bool-or-option-c-custom-type)

## See Also

- [api-newtype-safety](api-newtype-safety.md) - Newtypes for primitive type safety
