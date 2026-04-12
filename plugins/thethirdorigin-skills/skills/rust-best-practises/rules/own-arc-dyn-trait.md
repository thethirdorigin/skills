# own-arc-dyn-trait

> Use Arc\<dyn Trait + Send + Sync\> for trait objects in dependency injection

## Why It Matters

Dependency injection in async Rust requires sharing service implementations across multiple handlers and tasks. `Box<dyn Trait>` works for single-owner scenarios but cannot be cheaply cloned or shared across threads. `Arc<dyn Trait + Send + Sync>` solves both problems: it is cloneable (cheap atomic increment) and thread-safe.

This pattern is the foundation of DI in async Rust applications. It enables constructor injection where each handler receives its dependencies as `Arc<dyn Trait>` and can freely clone and pass them to spawned tasks.

## Bad

```rust
// Box is not Clone — cannot share across handlers
struct PaymentService {
    repo: Box<dyn TransactionRepo>,
    gateway: Box<dyn PaymentGateway>,
}

// Missing Send + Sync — cannot use in async tasks
struct LedgerService {
    repo: Arc<dyn LedgerRepo>,  // may not be Send + Sync
}
```

## Good

```rust
// Arc + Send + Sync — cloneable and thread-safe
struct PaymentService {
    repo: Arc<dyn TransactionRepo + Send + Sync>,
    gateway: Arc<dyn PaymentGateway + Send + Sync>,
}

impl PaymentService {
    fn new(
        repo: Arc<dyn TransactionRepo + Send + Sync>,
        gateway: Arc<dyn PaymentGateway + Send + Sync>,
    ) -> Self {
        Self { repo, gateway }
    }

    async fn process(&self, tx: Transaction) -> Result<Receipt> {
        self.repo.save(&tx).await?;
        self.gateway.charge(&tx).await
    }
}

// In application setup:
let repo: Arc<dyn TransactionRepo + Send + Sync> = Arc::new(PostgresTransactionRepo::new(pool));
let gateway: Arc<dyn PaymentGateway + Send + Sync> = Arc::new(StripeGateway::new(api_key));
let service = PaymentService::new(repo, gateway);
```

## See Also

- [own-arc-async](own-arc-async.md) - Arc for shared ownership across async tasks
- [async-send-sync](async-send-sync.md) - Send + Sync bounds for async containers
