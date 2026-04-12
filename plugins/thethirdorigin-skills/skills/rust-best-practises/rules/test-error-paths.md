# test-error-paths

> Test error paths explicitly, not just happy paths

## Why It Matters

Error handling code is where bugs hide. A function that works perfectly for valid inputs may panic on empty strings, return the wrong error variant for malformed data, or silently discard context when wrapping errors. These bugs only surface in production under unexpected conditions -- exactly when you need reliability most.

Testing each error variant explicitly ensures that your error types carry the right information, that error messages are useful for debugging, and that error propagation chains remain intact as the code evolves.

## Bad

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_config() {
        let config = Config::from_str("port = 8080").unwrap();
        assert_eq!(config.port, 8080);
    }

    // No tests for invalid input, missing fields, or malformed syntax.
    // When parse("") panics in production, nobody knows why.
}
```

## Good

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_config_returns_expected_values() {
        let config = Config::from_str("port = 8080").unwrap();
        assert_eq!(config.port, 8080);
    }

    #[test]
    fn parse_empty_input_returns_empty_input_error() {
        assert!(matches!(
            Config::from_str(""),
            Err(ConfigError::EmptyInput)
        ));
    }

    #[test]
    fn parse_missing_port_returns_missing_field_error() {
        let err = Config::from_str("host = localhost").unwrap_err();
        assert!(matches!(err, ConfigError::MissingField { field } if field == "port"));
    }

    #[test]
    fn parse_invalid_port_returns_parse_int_error_with_context() {
        let err = Config::from_str("port = abc").unwrap_err();
        assert!(matches!(err, ConfigError::InvalidValue { field, .. } if field == "port"));
        assert!(err.to_string().contains("abc"));
    }

    #[test]
    fn parse_malformed_syntax_returns_syntax_error_with_line_number() {
        let err = Config::from_str("port 8080").unwrap_err();
        assert!(matches!(err, ConfigError::SyntaxError { line: 1, .. }));
    }
}
```

## References

- [C-GOOD-ERR](https://rust-lang.github.io/api-guidelines/interoperability.html#error-types-are-meaningful-and-well-behaved-c-good-err)

## See Also

- [err-canonical-structs](err-canonical-structs.md) - Design meaningful error types
- [test-descriptive-names](test-descriptive-names.md) - Naming conventions for tests
