# log-otel-conventions

> Follow OpenTelemetry semantic conventions for span and attribute names

## Why It Matters

Observability platforms like Datadog, Grafana, and Honeycomb understand OpenTelemetry semantic conventions out of the box. Standard attribute names like `http.request.method` and `http.response.status_code` automatically populate dashboards, alerts, and service maps without custom configuration.

Custom attribute names like `req_method` or `status` require manual mapping in every observability tool. They also break cross-service correlation: when service A uses `user_id` and service B uses `usr`, tracing a request across services requires knowing both conventions.

## Bad

```rust
use tracing::info;

async fn handle_request(req: &Request) -> Response {
    // Custom attribute names -- no tool understands these by default
    let span = tracing::info_span!(
        "handle_req",
        method = %req.method(),
        path = %req.uri().path(),
        usr = %req.user_id(),
    );

    let response = process(req).await;

    info!(
        parent: &span,
        dur_ms = elapsed.as_millis() as u64,
        status = response.status().as_u16(),
        "Request done"
    );

    response
}
```

## Good

```rust
use tracing::info;

async fn handle_request(req: &Request) -> Response {
    // OpenTelemetry semantic conventions -- tools understand these natively
    let span = tracing::info_span!(
        "HTTP request",
        http.request.method = %req.method(),
        url.path = %req.uri().path(),
        user.id = %req.user_id(),
        otel.kind = "server",
    );

    let response = process(req).await;

    info!(
        parent: &span,
        http.response.status_code = response.status().as_u16(),
        "Request completed"
    );

    response
}
```

## See Also

- [log-structured-events](log-structured-events.md) - Use structured events with named properties
- [log-hierarchical-naming](log-hierarchical-naming.md) - Hierarchical naming for filtering
