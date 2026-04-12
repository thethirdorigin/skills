# own-temporary-mut

> Rebind mutable data as immutable once the preparation phase is complete

## Why It Matters

Making mutability explicit and scoped communicates intent clearly: "this data is being built, then frozen." When a binding stays `mut` for an entire function but mutations only happen in the first few lines, readers must scan the whole function to confirm nothing else modifies it. This wastes review effort and invites accidental mutations during the read phase.

Rebinding with `let data = data;` (shadowing without `mut`) tells the compiler and the reader that mutations are done. The compiler enforces immutability after that point, turning a potential bug into a compile error. For construction sequences, a block scope achieves the same effect while keeping the mutable binding invisible outside the block.

## Bad

```rust
fn build_pipeline(stages: &[StageConfig]) -> Result<Pipeline> {
    // `mut` needed only for the setup loop, but stays mutable for 30+ more lines
    let mut handlers: Vec<Box<dyn Handler>> = Vec::with_capacity(stages.len());
    for stage in stages {
        handlers.push(stage.into_handler()?);
    }

    // ... 30 lines of read-only pipeline validation and assembly ...
    // Nothing below mutates `handlers`, but the compiler allows it.
    // A future editor might accidentally call handlers.push() or handlers.clear() here.

    let mut metrics = MetricsCollector::new();
    metrics.register("pipeline.stages", handlers.len() as u64);
    metrics.register("pipeline.created_at", now_millis());

    // `metrics` stays mutable even though registration is done
    // and the rest of the function only reads from it.

    validate_pipeline(&handlers, &metrics)?;
    Ok(Pipeline::new(handlers, metrics))
}
```

## Good

```rust
fn build_pipeline(stages: &[StageConfig]) -> Result<Pipeline> {
    // Option 1: Shadow the binding to freeze it after setup
    let mut handlers: Vec<Box<dyn Handler>> = Vec::with_capacity(stages.len());
    for stage in stages {
        handlers.push(stage.into_handler()?);
    }
    let handlers = handlers; // Frozen -- compiler rejects mutations below this line

    // Option 2: Use a block scope to confine mutability
    let metrics = {
        let mut m = MetricsCollector::new();
        m.register("pipeline.stages", handlers.len() as u64);
        m.register("pipeline.created_at", now_millis());
        m // Returned as immutable
    };

    // Both `handlers` and `metrics` are now immutable.
    // Accidental mutations are compile errors, not runtime bugs.
    validate_pipeline(&handlers, &metrics)?;
    Ok(Pipeline::new(handlers, metrics))
}
```

## References

- [Temporary mutability idiom](https://rust-unofficial.github.io/patterns/idioms/temporary-mutability.html)

## See Also

- [own-borrow-prefer](own-borrow-prefer.md) - Borrow over clone where possible
