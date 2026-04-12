# log-structured-events

> Use structured events with named properties and message templates

## Why It Matters

Positional string formatting produces human-readable log lines but machine-opaque ones. When you need to find all login events for a specific user in a log aggregation system, parsing `"User alice logged in from 10.0.0.1"` with regex is fragile and slow. Structured fields like `user_id = "alice"` are indexed and queryable directly.

Named properties also make logs self-documenting. A structured event clearly declares what data it carries, while a format string requires reading the code to know which positional argument maps to which value.

## Bad

```rust
use log::info;

fn handle_login(user_id: &str, ip_addr: &str) {
    // Positional formatting -- not queryable, fields unnamed
    info!("User {} logged in from {}", user_id, ip_addr);

    // To find all logins by user_id, you must regex-parse every log line:
    // grep "User alice" logs.txt
}
```

## Good

```rust
use tracing::info;

fn handle_login(user_id: &str, ip_addr: &str) {
    // Named, structured fields -- queryable in any log aggregation system
    info!(
        user_id = %user_id,
        ip_addr = %ip_addr,
        "User logged in"
    );

    // In Datadog/Grafana/CloudWatch: filter by user_id = "alice"
    // No parsing required.
}
```

## See Also

- [log-defer-formatting](log-defer-formatting.md) - Defer formatting to the subscriber
- [log-hierarchical-naming](log-hierarchical-naming.md) - Use hierarchical target names
- [log-redact-sensitive](log-redact-sensitive.md) - Never log sensitive data
