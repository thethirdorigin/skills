# err-result-recoverable

> Use Result<T, E> for all recoverable errors — never panic in library code

## Why It Matters

Library code serves callers who each have different recovery strategies. A web server may want to return a 400 response, a CLI tool may want to print a friendly message and exit, and a test harness may want to assert the specific error variant. When library code panics, it robs every caller of that choice and crashes the entire program.

Result<T, E> makes fallibility explicit in the type signature. Callers see at compile time that an operation can fail and must handle it. This is Rust's primary mechanism for recoverable errors and the foundation of a robust error-handling strategy.

## Bad

```rust
pub fn parse(input: &str) -> Data {
    if input.is_empty() {
        panic!("empty input");
    }
    if !input.starts_with('{') {
        panic!("expected JSON object");
    }
    // ... parsing logic
    Data { /* fields */ }
}
```

## Good

```rust
#[derive(Debug)]
pub enum ParseError {
    EmptyInput,
    InvalidFormat { expected: &'static str },
}

pub fn parse(input: &str) -> Result<Data, ParseError> {
    if input.is_empty() {
        return Err(ParseError::EmptyInput);
    }
    if !input.starts_with('{') {
        return Err(ParseError::InvalidFormat {
            expected: "JSON object starting with '{'",
        });
    }
    // ... parsing logic
    Ok(Data { /* fields */ })
}
```

## See Also

- [err-panic-bugs-only](err-panic-bugs-only.md) - When panics are appropriate
- [err-canonical-structs](err-canonical-structs.md) - Designing rich error types
