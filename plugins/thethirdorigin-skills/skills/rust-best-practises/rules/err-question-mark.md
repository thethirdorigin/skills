# err-question-mark

> Use the ? operator for error propagation — do not match-and-rewrap

## Why It Matters

The ? operator is Rust's idiomatic shorthand for propagating errors up the call stack. It calls From::from() on the error automatically, converting it to the function's return type. This keeps the happy path front and center and reduces visual noise.

Match-and-rewrap patterns obscure the actual business logic under layers of boilerplate. They also introduce opportunities for mistakes: forgetting a variant, swapping Ok and Err arms, or silently discarding context. The ? operator eliminates all of these issues in a single character.

## Bad

```rust
fn read_config(path: &Path) -> Result<Config, MyError> {
    let mut file = match File::open(path) {
        Ok(f) => f,
        Err(e) => return Err(MyError::Io(e)),
    };
    let mut contents = String::new();
    match file.read_to_string(&mut contents) {
        Ok(_) => {},
        Err(e) => return Err(MyError::Io(e)),
    };
    match toml::from_str(&contents) {
        Ok(config) => Ok(config),
        Err(e) => Err(MyError::Parse(e)),
    }
}
```

## Good

```rust
impl From<io::Error> for MyError {
    fn from(err: io::Error) -> Self {
        MyError::Io(err)
    }
}

impl From<toml::de::Error> for MyError {
    fn from(err: toml::de::Error) -> Self {
        MyError::Parse(err)
    }
}

fn read_config(path: &Path) -> Result<Config, MyError> {
    let mut file = File::open(path)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let config = toml::from_str(&contents)?;
    Ok(config)
}
```

## See Also

- [err-anyhow-app](err-anyhow-app.md) - When to use anyhow vs typed errors
- [err-context-chain](err-context-chain.md) - Adding context to propagated errors
