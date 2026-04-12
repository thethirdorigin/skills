# iter-chains

> Prefer iterator chains over explicit for loops

## Why It Matters

Iterator chains express data transformations declaratively: filter, map, collect. Each step has a clear, single purpose, and the chain reads top-to-bottom as a pipeline. The Rust compiler optimises iterator chains as zero-cost abstractions, generating the same machine code as hand-written loops with manual index tracking and conditional pushes.

Explicit for loops with mutable accumulators scatter the transformation logic across variable declarations, conditionals, and push calls. They require the reader to mentally simulate the loop to understand the output. Iterator chains make the intent visible at a glance.

## Bad

```rust
fn active_usernames(users: &[User]) -> Vec<String> {
    let mut result = Vec::new();
    for user in users {
        if user.is_active() {
            let name = user.name().to_uppercase();
            result.push(name);
        }
    }
    result
}
```

## Good

```rust
fn active_usernames(users: &[User]) -> Vec<String> {
    users
        .iter()
        .filter(|user| user.is_active())
        .map(|user| user.name().to_uppercase())
        .collect()
}
```

## See Also

- [iter-no-intermediate-vec](iter-no-intermediate-vec.md) - Keeping chains lazy to avoid extra allocations
- [iter-into-consume](iter-into-consume.md) - Using into_iter when ownership transfer is needed
