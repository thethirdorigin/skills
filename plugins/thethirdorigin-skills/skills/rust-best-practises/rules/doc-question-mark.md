# doc-question-mark

> Use ? in doc examples, not .unwrap()

## Why It Matters

Doc examples are often the first Rust code a user copies into their project. When examples use .unwrap(), they teach callers to ignore errors — a habit that leads to panics in production. The ? operator demonstrates proper error handling and makes the example production-ready from the start.

Additionally, .unwrap() in a doc test will panic with an opaque "called unwrap on Err" message if the example breaks due to an API change. The ? operator produces a clear error message and a test failure that points to the actual problem.

## Bad

```rust
/// Loads configuration from a TOML file.
///
/// # Examples
///
/// ```
/// let config = mylib::load_config("app.toml").unwrap();
/// let name = config.get("name").unwrap();
/// println!("App: {}", name);
/// ```
pub fn load_config(path: &str) -> Result<Config, ConfigError> {
    // ...
}
```

## Good

```rust
/// Loads configuration from a TOML file.
///
/// # Examples
///
/// ```
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// # std::fs::write("app.toml", "name = \"my-app\"")?;
/// let config = mylib::load_config("app.toml")?;
/// let name = config.get("name")?;
/// assert_eq!(name, "my-app");
/// # std::fs::remove_file("app.toml")?;
/// # Ok(())
/// # }
/// ```
pub fn load_config(path: &str) -> Result<Config, ConfigError> {
    // ...
}
```

## References

- [C-QUESTION-MARK](https://rust-lang.github.io/api-guidelines/documentation.html#examples-use--not-try-not-unwrap-c-question-mark) — Examples use ? not try! or unwrap

## See Also

- [doc-examples-runnable](doc-examples-runnable.md) - Including runnable examples in doc comments
- [err-question-mark](err-question-mark.md) - Using ? for error propagation in general
