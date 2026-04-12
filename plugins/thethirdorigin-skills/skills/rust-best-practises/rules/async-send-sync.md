# async-send-sync

> All trait objects in async containers need Send + Sync bounds

## Why It Matters

Multi-threaded async runtimes (like Tokio's default configuration) can move tasks between OS threads at any `.await` point. If a trait object inside a future is not `Send`, the future itself is not `Send`, and it cannot be spawned with `tokio::spawn`. Without `Sync`, it cannot be safely shared across threads via `Arc`.

Adding `Send + Sync` at the trait object definition site catches this early. Without these bounds, the error appears at distant call sites where the future is spawned -- producing confusing error messages that point far from the actual problem.

## Bad

```rust
// Missing Send + Sync — compiles here, but fails at spawn sites
struct AppState {
    ledger_repo: Arc<dyn LedgerRepo>,
    payment_gateway: Arc<dyn PaymentGateway>,
}

async fn handle_request(state: AppState) -> Result<Response> {
    // ERROR at spawn: future is not Send because Arc<dyn LedgerRepo> is not Send
    let entries = state.ledger_repo.list_entries().await?;
    Ok(Response::ok(entries))
}

// The error message points here, not at the struct definition
tokio::spawn(handle_request(state)); // confusing compilation error
```

## Good

```rust
// Send + Sync declared at the definition — errors caught immediately
struct AppState {
    ledger_repo: Arc<dyn LedgerRepo + Send + Sync>,
    payment_gateway: Arc<dyn PaymentGateway + Send + Sync>,
}

async fn handle_request(state: AppState) -> Result<Response> {
    let entries = state.ledger_repo.list_entries().await?;
    Ok(Response::ok(entries))
}

// Compiles cleanly — all trait objects are Send + Sync
tokio::spawn(handle_request(state));
```

## See Also

- [own-arc-dyn-trait](own-arc-dyn-trait.md) - Arc\<dyn Trait\> for dependency injection
- [async-futures-send](async-futures-send.md) - Validate futures are Send with compile-time assertions
