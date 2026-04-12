# name-consts-screaming

> Use SCREAMING_SNAKE_CASE for constants and statics

## Why It Matters

SCREAMING_SNAKE_CASE visually distinguishes compile-time constants and statics from regular variables. Readers can immediately tell that `MAX_RETRIES` is a fixed value without checking its definition. The compiler enforces this convention with `#[warn(non_upper_case_globals)]`, so deviating triggers warnings.

This is particularly important in configuration and threshold values, where mistaking a constant for a mutable variable could lead to incorrect assumptions about the code's behavior.

## Bad

```rust
const maxRetries: u32 = 3;
const defaultTimeout: Duration = Duration::from_secs(30);
static globalConfig: Lazy<Config> = Lazy::new(|| Config::load());

fn retry_operation() {
    for _ in 0..maxRetries {
        // reader might think maxRetries is a local variable
    }
}
```

## Good

```rust
const MAX_RETRIES: u32 = 3;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);
static GLOBAL_CONFIG: Lazy<Config> = Lazy::new(|| Config::load());

fn retry_operation() {
    for _ in 0..MAX_RETRIES {
        // clearly a constant — no ambiguity
    }
}
```

## References

- [C-CASE](https://rust-lang.github.io/api-guidelines/naming.html#c-case) - RFC 430 naming conventions

## See Also

- [name-types-pascal](name-types-pascal.md) - PascalCase for types and traits
- [name-funcs-snake](name-funcs-snake.md) - snake_case for functions and variables
