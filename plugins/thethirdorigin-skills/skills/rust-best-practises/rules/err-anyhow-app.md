# err-anyhow-app

> Use anyhow/eyre for application errors; use concrete types for library errors

## Why It Matters

Libraries and applications have fundamentally different error-handling needs. A library's callers must match on error variants to decide how to recover: retry on timeout, show a validation message to the user, or escalate a permissions error. This requires concrete, typed error enums. If a library returns anyhow::Error, callers are reduced to string matching or downcasting — both fragile and error-prone.

Applications, on the other hand, typically log errors and exit or display them to a user. They rarely match on specific variants from deep in the dependency tree. Here, anyhow or eyre shines: it provides effortless error chaining with .context(), automatic backtrace capture, and seamless interop with any Error type via the ? operator.

## Bad

```rust
// Library crate returning anyhow — callers cannot match variants
pub fn connect(url: &str) -> anyhow::Result<Connection> {
    let parsed = Url::parse(url)?;
    let stream = TcpStream::connect(parsed.socket_addrs(|| None)?[0])?;
    Ok(Connection::new(stream))
}

// Caller is stuck:
match connect(url) {
    Err(e) => {
        // Can only do string inspection or risky downcast
        if e.to_string().contains("refused") { /* retry? */ }
    }
    Ok(conn) => { /* ... */ }
}
```

## Good

```rust
// Library crate — typed errors with thiserror
#[derive(Debug, thiserror::Error)]
pub enum ConnectError {
    #[error("invalid URL: {0}")]
    InvalidUrl(#[from] url::ParseError),

    #[error("DNS resolution failed for {host}")]
    DnsFailure { host: String, source: io::Error },

    #[error("connection refused by {addr}")]
    Refused { addr: SocketAddr, source: io::Error },
}

pub fn connect(url: &str) -> Result<Connection, ConnectError> {
    let parsed = Url::parse(url)?;
    // ... typed error construction
    Ok(Connection::new(stream))
}

// Application crate — anyhow for ergonomic chaining
fn main() -> anyhow::Result<()> {
    let conn = mylib::connect(&config.url)
        .context("failed to connect to primary database")?;

    let data = conn.fetch_all()
        .context("failed to load initial dataset")?;

    Ok(())
}
```

## References

- M-APP-ERROR — Application-level error handling with anyhow/eyre

## See Also

- [err-canonical-structs](err-canonical-structs.md) - Designing library error types
- [err-context-chain](err-context-chain.md) - Adding context to errors
