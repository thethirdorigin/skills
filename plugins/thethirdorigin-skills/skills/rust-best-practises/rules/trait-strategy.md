# trait-strategy

> Use traits or closures to implement the Strategy pattern -- swap algorithms without changing callers

## Why It Matters

The Strategy pattern separates an algorithm's interface from its implementation, allowing you to swap behaviour at the call site without modifying the code that uses it. In Rust, traits provide compile-time (monomorphised) dispatch while closures and trait objects provide runtime dispatch.

Hard-coding an algorithm directly into a function means every caller is locked into that single implementation. When a second variant is needed -- a different hashing scheme, a different sorting algorithm, a different retry policy -- you must either duplicate the calling code or introduce brittle conditional branches. Defining the algorithm behind a trait or closure boundary keeps callers stable and makes the system easy to extend.

## Bad

```rust
/// Always uses quicksort. Callers that need a stable sort or a
/// domain-specific ordering have no way to change the algorithm.
fn sort_records(records: &mut [Record]) {
    // Inline quicksort implementation...
    records.sort_unstable_by(|a, b| a.key.cmp(&b.key));
}

fn process_pipeline(records: &mut [Record]) {
    // Tightly coupled -- cannot substitute a different sort strategy
    // without editing this function.
    sort_records(records);
    deduplicate(records);
}
```

## Good

```rust
/// Trait-based strategy -- compile-time dispatch, zero overhead.
trait Sorter {
    fn sort(&self, data: &mut [Record]);
}

struct QuickSort;
impl Sorter for QuickSort {
    fn sort(&self, data: &mut [Record]) {
        data.sort_unstable_by(|a, b| a.key.cmp(&b.key));
    }
}

struct StableSort;
impl Sorter for StableSort {
    fn sort(&self, data: &mut [Record]) {
        data.sort_by(|a, b| a.key.cmp(&b.key));
    }
}

fn process_pipeline(records: &mut [Record], sorter: &impl Sorter) {
    sorter.sort(records);
    deduplicate(records);
}

/// Closure-based strategy -- lightweight, no trait boilerplate.
fn transform_batch(
    data: &[u8],
    transform: impl Fn(&[u8]) -> Vec<u8>,
) -> Vec<u8> {
    transform(data)
}

// Callers choose the algorithm:
let compressed = transform_batch(&payload, compress_zstd);
let encrypted = transform_batch(&payload, encrypt_aes256);
```

## References

- [Strategy pattern in Rust](https://rust-unofficial.github.io/patterns/patterns/behavioural/strategy.html)

## See Also

- [trait-static-dispatch](trait-static-dispatch.md) - Prefer static dispatch on hot paths
- [trait-dynamic-dispatch](trait-dynamic-dispatch.md) - When runtime polymorphism is needed
