# log-redact-sensitive

> Redact sensitive data in logs -- never log passwords, tokens, or PII

## Why It Matters

Log storage systems are rarely access-controlled with the same rigour as application databases. Logs are often shipped to third-party aggregation services, stored in shared buckets, or accessible to broad engineering teams. A password, API token, or email address in a log line becomes a compliance violation and a security incident waiting to happen.

The fix is structural: implement custom `Debug` and `Display` traits that redact sensitive fields, and log only non-sensitive identifiers. This makes accidental exposure impossible rather than relying on developer discipline at every log call site.

## Bad

```rust
use tracing::info;

#[derive(Debug)]
struct LoginRequest {
    username: String,
    password: String,
    mfa_token: Option<String>,
}

fn handle_login(request: &LoginRequest) {
    // Logs the password and MFA token in plaintext
    info!(?request, "Processing login");

    // Also bad -- individual fields logged explicitly
    info!(
        username = %request.username,
        password = %request.password,  // Password in logs!
        "Authenticating user"
    );
}
```

## Good

```rust
use std::fmt;
use tracing::info;

struct LoginRequest {
    username: String,
    password: String,
    mfa_token: Option<String>,
}

// Custom Debug that redacts sensitive fields
impl fmt::Debug for LoginRequest {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("LoginRequest")
            .field("username", &self.username)
            .field("password", &"[REDACTED]")
            .field("mfa_token", &self.mfa_token.as_ref().map(|_| "[REDACTED]"))
            .finish()
    }
}

fn handle_login(request: &LoginRequest) {
    // Safe -- Debug implementation redacts sensitive fields
    info!(?request, "Processing login");

    // Even better -- log only non-sensitive identifiers
    info!(
        username = %request.username,
        "Authenticating user"
    );
}
```

## See Also

- [log-structured-events](log-structured-events.md) - Use structured events with named properties
- [api-debug-display](api-debug-display.md) - Implement Debug and Display thoughtfully
