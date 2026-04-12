# test-descriptive-names

> Use descriptive test names that explain what is verified

## Why It Matters

Test names appear in failure output. When a CI pipeline reports `parse_empty_input_returns_empty_input_error ... FAILED`, you know exactly what broke without opening the test file. A name like `test1` or `test_parse` tells you nothing -- you must read the test body, check the assertion, and work backward to understand the intent.

Descriptive names also serve as living documentation. Scanning the test list tells you what behaviours the module guarantees, which is invaluable during code review and onboarding.

## Bad

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1() {
        assert!(parse("42").is_ok());
    }

    #[test]
    fn test_parse() {
        assert!(parse("").is_err());
    }

    #[test]
    fn it_works() {
        let result = transfer(100, 50);
        assert!(result.is_ok());
    }
}
```

## Good

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_valid_integer_returns_value() {
        assert_eq!(parse("42").unwrap(), 42);
    }

    #[test]
    fn parse_empty_input_returns_empty_input_error() {
        assert!(matches!(parse(""), Err(ParseError::EmptyInput)));
    }

    #[test]
    fn transfer_sufficient_funds_debits_sender() {
        let result = transfer(100, 50).unwrap();
        assert_eq!(result.sender_balance, 50);
    }

    #[test]
    fn transfer_insufficient_funds_fails_with_overdraft_error() {
        let result = transfer(30, 50);
        assert!(matches!(result, Err(TransferError::InsufficientFunds { .. })));
    }
}
```

## See Also

- [test-cfg-module](test-cfg-module.md) - Place unit tests in the same file
- [test-error-paths](test-error-paths.md) - Test error paths explicitly
