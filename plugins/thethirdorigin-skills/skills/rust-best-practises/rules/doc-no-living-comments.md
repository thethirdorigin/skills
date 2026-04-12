# doc-no-living-comments

> Do not maintain comments that must update alongside code changes

## Why It Matters

A "living comment" is one that describes a specific value, count, or behavior that changes whenever the code changes. "Returns the first 3 items" above code that now returns 5 items is a bug in the documentation. These comments create a maintenance burden: every code change requires a corresponding comment change, and the two inevitably fall out of sync.

The fix is to make the code self-documenting. Named constants, descriptive variable names, and well-chosen function names eliminate the need for comments that track implementation details. When the constant changes from 3 to 5, the code is still correct and readable — no comment to update.

## Bad

```rust
// Process the first 3 items in the queue
fn preview(queue: &VecDeque<Job>) -> Vec<&Job> {
    queue.iter().take(3).collect()
    // If someone changes 3 to 5, the comment is now wrong.
    // If someone changes the logic to use .skip(), the comment is misleading.
}

// The timeout is 30 seconds
const TIMEOUT: Duration = Duration::from_secs(60);
// Comment says 30, code says 60. Which is correct?
```

## Good

```rust
const PREVIEW_COUNT: usize = 5;

fn preview(queue: &VecDeque<Job>) -> Vec<&Job> {
    queue.iter().take(PREVIEW_COUNT).collect()
}

const REQUEST_TIMEOUT: Duration = Duration::from_secs(60);
// No comment needed — the name and value speak for themselves.

// When a comment IS valuable, it explains WHY, not WHAT:
// Use a longer timeout because the upstream geocoding API
// is known to take 20-40s under load.
const GEOCODING_TIMEOUT: Duration = Duration::from_secs(60);
```

## See Also

- [doc-explain-why](doc-explain-why.md) - Writing comments that capture intent
- [doc-summary-sentence](doc-summary-sentence.md) - Doc comments for public API items
