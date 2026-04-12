# doc-examples-runnable

> Include runnable Examples section in doc comments for public APIs

## Why It Matters

Runnable examples in doc comments serve double duty: they teach users how to call the API, and they are automatically compiled and executed by cargo test. This means your examples are always tested against the current code — if the API changes and the example breaks, your CI catches it immediately.

Prose descriptions of usage require the reader to translate English into code. A working example eliminates ambiguity: it shows exact types, exact method calls, and exact expected output. For complex builders or multi-step workflows, an example is worth more than a page of prose.

## Bad

```rust
/// Parses a configuration string.
///
/// Pass a TOML-formatted string and this function will return
/// a Config struct. Make sure the string has a "name" key.
pub fn parse_config(input: &str) -> Result<Config, ConfigError> {
    // ...
}
```

## Good

```rust
/// Parses a TOML configuration string into a [`Config`].
///
/// # Examples
///
/// ```
/// use mylib::parse_config;
///
/// let config = parse_config(r#"
///     name = "my-app"
///     timeout = 30
/// "#)?;
///
/// assert_eq!(config.name(), "my-app");
/// assert_eq!(config.timeout(), 30);
/// # Ok::<(), mylib::ConfigError>(())
/// ```
///
/// # Errors
///
/// Returns [`ConfigError::MissingField`] if the `name` key is absent.
pub fn parse_config(input: &str) -> Result<Config, ConfigError> {
    // ...
}
```

## References

- [C-EXAMPLE](https://rust-lang.github.io/api-guidelines/documentation.html#examples-use--not-try-not-unwrap-c-question-mark) — Every public API item should include examples

## See Also

- [doc-question-mark](doc-question-mark.md) - Using ? instead of unwrap in examples
- [doc-summary-sentence](doc-summary-sentence.md) - Writing effective summary lines
