# iter-option-combinators

> Use Option/Result combinators for concise, chainable transformations

## Why It Matters

Match expressions on Option and Result are sometimes necessary, but they often expand simple transformations into five or more lines of boilerplate. Combinators like map, and_then, unwrap_or, and transpose express the same logic in a single fluent chain that reads like a sentence: "map the value, or return a default."

Combinators also compose naturally with the ? operator and iterator chains. A match block breaks the flow and forces the reader to mentally track each arm. Combinators keep the transformation pipeline flat and scannable.

## Bad

```rust
fn lookup_timeout(config: &Config) -> Duration {
    match config.get("timeout") {
        Some(val) => match val.parse::<u64>() {
            Ok(secs) => Duration::from_secs(secs),
            Err(_) => Duration::from_secs(30),
        },
        None => Duration::from_secs(30),
    }
}

fn user_display_name(user: &User) -> Option<String> {
    match user.nickname() {
        Some(nick) => Some(format!("@{nick}")),
        None => None,
    }
}
```

## Good

```rust
fn lookup_timeout(config: &Config) -> Duration {
    config
        .get("timeout")
        .and_then(|val| val.parse::<u64>().ok())
        .map(Duration::from_secs)
        .unwrap_or(Duration::from_secs(30))
}

fn user_display_name(user: &User) -> Option<String> {
    user.nickname().map(|nick| format!("@{nick}"))
}

// transpose() is useful when Option<Result<T, E>> needs to become Result<Option<T>, E>:
fn parse_optional_port(input: Option<&str>) -> Result<Option<u16>, ParseIntError> {
    input.map(|s| s.parse::<u16>()).transpose()
}
```

## See Also

- [iter-chains](iter-chains.md) - Iterator chains use the same combinator philosophy
- [err-question-mark](err-question-mark.md) - Using ? with Result combinators
