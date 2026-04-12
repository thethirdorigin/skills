# trait-supertraits

> Use supertraits to compose trait requirements

## Why It Matters

When multiple functions require the same combination of trait bounds — Service + Send + Sync + Clone — repeating those bounds at every call site creates maintenance burden and visual clutter. Adding a new requirement means updating every function signature across the codebase.

Supertraits centralise the requirement: trait Service: Send + Sync + Clone { ... } declares the contract once. Every function that takes S: Service automatically gets all the supertrait bounds. When requirements change, you update one trait definition instead of dozens of function signatures.

## Bad

```rust
trait Worker {
    fn execute(&self, task: Task) -> Result<Output, WorkerError>;
}

// Every function repeats the same bounds:
fn spawn_worker<W: Worker + Send + Sync + Clone + 'static>(worker: W) {
    tokio::spawn(async move { worker.execute(task).await });
}

fn pool_workers<W: Worker + Send + Sync + Clone + 'static>(workers: Vec<W>) {
    for worker in workers {
        spawn_worker(worker.clone());
    }
}

fn register_worker<W: Worker + Send + Sync + Clone + 'static>(
    registry: &mut Registry,
    worker: W,
) {
    registry.add(Box::new(worker));
}
```

## Good

```rust
trait Worker: Send + Sync + Clone + 'static {
    fn execute(&self, task: Task) -> Result<Output, WorkerError>;
}

// Bounds declared once, used everywhere:
fn spawn_worker<W: Worker>(worker: W) {
    tokio::spawn(async move { worker.execute(task).await });
}

fn pool_workers<W: Worker>(workers: Vec<W>) {
    for worker in workers {
        spawn_worker(worker.clone());
    }
}

fn register_worker<W: Worker>(registry: &mut Registry, worker: W) {
    registry.add(Box::new(worker));
}
```

## See Also

- [trait-single-responsibility](trait-single-responsibility.md) - Keeping individual traits focused
- [trait-static-dispatch](trait-static-dispatch.md) - How generics enable monomorphisation
