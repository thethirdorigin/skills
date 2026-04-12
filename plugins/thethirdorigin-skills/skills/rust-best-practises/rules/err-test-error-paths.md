# err-test-error-paths

> Test error paths explicitly — not just happy paths

## Why It Matters

Error paths are where bugs hide. A function might return the wrong error variant, lose context from the source error, or even panic instead of returning Err. These defects are invisible when tests only exercise the success case.

Explicit error-path tests verify that the correct variant is returned, that context information is preserved, and that the error message is actionable. They also serve as documentation: a test named parse_empty_input_returns_empty_error tells the reader exactly what behavior to expect without reading the implementation.

## Bad

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_json() {
        let result = parse(r#"{"name": "Alice"}"#).unwrap();
        assert_eq!(result.name, "Alice");
    }

    // No tests for empty input, malformed JSON, missing fields,
    // or any other error condition.
}
```

## Good

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_json() {
        let result = parse(r#"{"name": "Alice"}"#).unwrap();
        assert_eq!(result.name, "Alice");
    }

    #[test]
    fn parse_empty_input_returns_error() {
        assert!(matches!(parse(""), Err(ParseError::EmptyInput)));
    }

    #[test]
    fn parse_malformed_json_returns_syntax_error() {
        let err = parse("{not json}").unwrap_err();
        assert!(matches!(err, ParseError::Syntax { .. }));
    }

    #[test]
    fn parse_missing_field_includes_field_name() {
        let err = parse(r#"{"age": 30}"#).unwrap_err();
        match err {
            ParseError::MissingField { field } => assert_eq!(field, "name"),
            other => panic!("expected MissingField, got {other:?}"),
        }
    }

    #[test]
    fn parse_error_display_is_actionable() {
        let err = parse("").unwrap_err();
        let msg = err.to_string();
        assert!(msg.contains("empty"), "error message should mention empty input: {msg}");
    }
}
```

## References

- [C-GOOD-ERR](https://rust-lang.github.io/api-guidelines/interoperability.html#examples-use-question-mark-operator-c-good-err) — Errors should be tested and well-documented

## See Also

- [err-result-recoverable](err-result-recoverable.md) - Using Result for recoverable errors
- [err-context-chain](err-context-chain.md) - Ensuring errors carry useful context
