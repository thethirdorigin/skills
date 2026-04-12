# doc-errors-section

> Document errors with an Errors section for fallible functions

## Why It Matters

When a function returns Result, callers need to know what errors can occur so they can handle each case appropriately. Without an Errors section, they must read the implementation source code to discover which variants are possible and under what conditions. This is fragile — implementation details change, and undocumented error behavior is effectively undefined behavior for the caller.

An explicit Errors section lists each error variant with its trigger condition. This forms a contract between the function and its callers, making the API predictable and testable.

## Bad

```rust
/// Connects to the remote server.
pub fn connect(url: &str) -> Result<Connection, ConnectError> {
    // Callers have no idea what errors to expect.
    // They must read the source to learn about InvalidUrl,
    // DnsFailure, Timeout, and Refused variants.
    // ...
}
```

## Good

```rust
/// Connects to the remote server at the given URL.
///
/// # Errors
///
/// - [`ConnectError::InvalidUrl`] if the URL scheme is not `http` or `https`.
/// - [`ConnectError::DnsFailure`] if the hostname cannot be resolved.
/// - [`ConnectError::Timeout`] if the server does not respond within 30 seconds.
/// - [`ConnectError::Refused`] if the server actively refuses the connection.
pub fn connect(url: &str) -> Result<Connection, ConnectError> {
    // ...
}
```

## See Also

- [doc-panics-section](doc-panics-section.md) - Documenting panic conditions
- [doc-summary-sentence](doc-summary-sentence.md) - Writing the opening summary line
