# api-debug-display

> All public types implement Debug; user-facing types implement Display

## Why It Matters

Debug is the single most important trait for developer experience. Without it, types cannot appear in log messages, error chains, or test failure output. Every public type should implement Debug, either via derive or a manual implementation that redacts sensitive fields.

Display serves a different purpose: it provides human-readable output intended for end users, not developers. Error types, configuration descriptions, and status messages benefit from Display. Implement Display when a type will appear in user-facing contexts such as CLI output, HTTP responses, or formatted reports.

## Bad

```rust
pub struct DatabaseConfig {
    pub host: String,
    pub port: u16,
    pub password: String,
}

pub enum ApiError {
    NotFound(String),
    Unauthorized,
    Internal(String),
}

// Cannot debug-print: log::error!("config: {:?}", config);  // compile error
// Cannot display to user: println!("Error: {}", err);        // compile error
```

## Good

```rust
#[derive(Clone, PartialEq, Eq)]
pub struct DatabaseConfig {
    host: String,
    port: u16,
    password: String,
}

// Manual Debug to redact the password field
impl fmt::Debug for DatabaseConfig {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("DatabaseConfig")
            .field("host", &self.host)
            .field("port", &self.port)
            .field("password", &"[REDACTED]")
            .finish()
    }
}

#[derive(Debug)]
pub enum ApiError {
    NotFound(String),
    Unauthorized,
    Internal(String),
}

impl fmt::Display for ApiError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::NotFound(resource) => write!(f, "resource not found: {resource}"),
            Self::Unauthorized => write!(f, "authentication required"),
            Self::Internal(msg) => write!(f, "internal error: {msg}"),
        }
    }
}
```

## References

- [C-DEBUG](https://rust-lang.github.io/api-guidelines/debuggability.html#all-public-types-implement-debug-c-debug)
- [M-PUBLIC-DEBUG](https://rust-lang.github.io/api-guidelines/debuggability.html)
- [M-PUBLIC-DISPLAY](https://rust-lang.github.io/api-guidelines/debuggability.html)

## See Also

- [api-common-traits](api-common-traits.md) - Eagerly derive common traits
