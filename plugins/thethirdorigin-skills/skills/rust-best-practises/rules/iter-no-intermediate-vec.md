# iter-no-intermediate-vec

> Avoid collecting intermediate iterators — keep chains lazy

## Why It Matters

Each call to .collect() materialises the entire iterator into a new heap-allocated collection. When you collect after filtering and then collect again after mapping, you allocate two Vecs and iterate the data twice. For large datasets this doubles memory usage and halves cache efficiency.

Rust iterators are lazy by design. Chaining .filter().map().collect() processes each element through the entire pipeline before moving to the next, resulting in a single allocation for the final result. Keep the chain lazy until the very end.

## Bad

```rust
fn expensive_pipeline(orders: &[Order]) -> Vec<Summary> {
    // First allocation: filtered orders
    let active: Vec<&Order> = orders
        .iter()
        .filter(|o| o.is_active())
        .collect();

    // Second allocation: enriched orders
    let enriched: Vec<EnrichedOrder> = active
        .iter()
        .map(|o| enrich(o))
        .collect();

    // Third allocation: final summaries
    let summaries: Vec<Summary> = enriched
        .iter()
        .map(|e| summarize(e))
        .collect();

    summaries
}
```

## Good

```rust
fn expensive_pipeline(orders: &[Order]) -> Vec<Summary> {
    orders
        .iter()
        .filter(|o| o.is_active())
        .map(|o| enrich(o))
        .map(|e| summarize(&e))
        .collect() // Single allocation for the final Vec
}
```

## See Also

- [iter-chains](iter-chains.md) - Preferring iterator chains over for loops
- [iter-zero-cost](iter-zero-cost.md) - Trusting the compiler to optimise iterator pipelines
