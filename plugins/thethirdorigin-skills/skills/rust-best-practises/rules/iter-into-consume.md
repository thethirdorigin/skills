# iter-into-consume

> Use into_iter() when consuming the collection

## Why It Matters

When you no longer need the original collection, iterating by reference and then cloning each element wastes both CPU cycles and memory. Each clone allocates new heap storage for types like String and Vec, only to discard the original moments later.

into_iter() moves elements out of the collection, transferring ownership directly to the loop body or the next iterator adapter. For owned collections, this is a simple pointer hand-off with no allocation overhead. The original collection is consumed and dropped, which is exactly what you want when you are done with it.

## Bad

```rust
fn process_all(items: Vec<Task>) -> Vec<Report> {
    let mut reports = Vec::new();
    for item in items.iter() {
        // Clone needed because iter() borrows
        let owned = item.clone();
        reports.push(execute(owned));
    }
    reports
}
```

## Good

```rust
fn process_all(items: Vec<Task>) -> Vec<Report> {
    items
        .into_iter()
        .map(execute)
        .collect()
}
```

## See Also

- [iter-chains](iter-chains.md) - Preferring iterator chains over for loops
- [iter-no-intermediate-vec](iter-no-intermediate-vec.md) - Avoiding unnecessary intermediate collections
