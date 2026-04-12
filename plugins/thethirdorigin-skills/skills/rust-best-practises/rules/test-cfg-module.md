# test-cfg-module

> Place unit tests in a #[cfg(test)] mod tests block in the same file

## Why It Matters

Colocating unit tests with the code they exercise gives tests direct access to private functions, types, and constants. You can test internal logic without exposing it through the public API, keeping the module's encapsulation intact.

The `#[cfg(test)]` attribute ensures that all test code -- helper functions, mock implementations, and the tests themselves -- is stripped from release builds. There is zero cost in binary size or compile time for production artifacts.

## Bad

```rust
// src/parser.rs
pub(crate) fn tokenize(input: &str) -> Vec<Token> {
    // ...
}

// tests/parser_tests.rs  <-- separate file, cannot access private items
#[test]
fn test_tokenize() {
    // ERROR: `tokenize` is not accessible from an external test crate
    let tokens = crate::parser::tokenize("hello");
    assert_eq!(tokens.len(), 1);
}
```

## Good

```rust
// src/parser.rs
pub(crate) fn tokenize(input: &str) -> Vec<Token> {
    // ...
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tokenize_single_word_returns_one_token() {
        let tokens = tokenize("hello");
        assert_eq!(tokens.len(), 1);
        assert_eq!(tokens[0].value, "hello");
    }

    #[test]
    fn tokenize_empty_input_returns_no_tokens() {
        let tokens = tokenize("");
        assert!(tokens.is_empty());
    }
}
```

## See Also

- [test-integration-dir](test-integration-dir.md) - Integration tests belong in tests/
- [test-descriptive-names](test-descriptive-names.md) - Naming conventions for tests
