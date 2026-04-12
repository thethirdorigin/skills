# doc-explain-why

> Comments explain why, not what — the code shows what

## Why It Matters

A comment that restates the code — "increment counter by 1" above counter += 1 — adds no information. It occupies visual space, competes with the code for the reader's attention, and inevitably drifts out of sync when the code changes. When a reader sees a stale "what" comment, they lose trust in all comments in the file.

"Why" comments capture context that is invisible in the code: business rules, performance trade-offs, workarounds for upstream bugs, or the reason a seemingly wrong approach is actually correct. These comments age well because the reasoning behind a decision changes far less often than the implementation details.

## Bad

```rust
// Create a new HashMap
let mut cache = HashMap::new();

// Loop through all users
for user in &users {
    // Check if the user is active
    if user.is_active() {
        // Insert the user into the cache
        cache.insert(user.id, user.clone());
    }
}

// Return the cache
cache
```

## Good

```rust
// Pre-warm the cache with active users to avoid cold-start latency
// on the first batch of incoming requests after deployment.
let mut cache = HashMap::new();
for user in &users {
    if user.is_active() {
        cache.insert(user.id, user.clone());
    }
}
cache
```

## See Also

- [doc-no-living-comments](doc-no-living-comments.md) - Avoiding comments that must track code changes
- [doc-summary-sentence](doc-summary-sentence.md) - Doc comments that describe the public interface
