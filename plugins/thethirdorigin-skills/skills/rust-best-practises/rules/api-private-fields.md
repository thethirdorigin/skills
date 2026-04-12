# api-private-fields

> Keep struct fields private — use accessor methods

## Why It Matters

Public fields lock you into a specific representation forever. Renaming a field, changing its type, adding validation, or computing a value lazily all become breaking changes when fields are public. Every downstream crate that accesses the field directly must be updated.

Private fields with accessor methods give you the freedom to evolve internals without breaking callers. You can add caching, validation, or deprecation warnings behind the same method signature. The only time public fields are appropriate is for simple data-transfer structs that have no invariants and exist solely to group related values.

## Bad

```rust
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
    pub max_connections: usize,
    pub timeout_ms: u64,
}

// Any caller can write invalid state:
let mut config = ServerConfig { /* ... */ };
config.port = 0;             // Invalid port
config.max_connections = 0;  // Invalid — server cannot accept connections
config.timeout_ms = 0;       // Probably unintended

// Renaming `timeout_ms` to `timeout: Duration` is a breaking change.
```

## Good

```rust
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
    timeout: Duration,
}

impl ServerConfig {
    pub fn new(host: impl Into<String>, port: u16) -> Result<Self, ConfigError> {
        if port == 0 {
            return Err(ConfigError::InvalidPort);
        }
        Ok(Self {
            host: host.into(),
            port,
            max_connections: 100,
            timeout: Duration::from_secs(30),
        })
    }

    pub fn host(&self) -> &str {
        &self.host
    }

    pub fn port(&self) -> u16 {
        self.port
    }

    pub fn max_connections(&self) -> usize {
        self.max_connections
    }

    pub fn timeout(&self) -> Duration {
        self.timeout
    }

    pub fn set_max_connections(&mut self, n: usize) -> Result<(), ConfigError> {
        if n == 0 {
            return Err(ConfigError::InvalidMaxConnections);
        }
        self.max_connections = n;
        Ok(())
    }
}

// Internal representation can change without breaking callers.
// Validation is enforced at construction and mutation boundaries.
```

## References

- [C-STRUCT-PRIVATE](https://rust-lang.github.io/api-guidelines/flexibility.html#structs-have-private-fields-c-struct-private)

## See Also

- [api-constructors](api-constructors.md) - Constructor patterns for private structs
- [api-builder-pattern](api-builder-pattern.md) - Builder pattern for complex configuration
