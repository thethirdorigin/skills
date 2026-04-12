# perf-partition-throughput

> Partition work into independent chunks for throughput optimisation

## Why It Matters

Processing items sequentially through a shared mutable structure creates a bottleneck that no amount of hardware can overcome. A single thread holding a mutex while processing each item serialises all work, even on a 64-core machine.

Partitioning data into independent slices allows each partition to be processed on its own thread or task without synchronisation overhead. The results are merged at the end. This pattern scales linearly with available cores and is the foundation of high-throughput data processing.

## Bad

```rust
use std::sync::Mutex;

fn process_all(items: &[Item]) -> Vec<Result> {
    let results = Mutex::new(Vec::new());

    // Every thread contends on the same mutex
    items.par_iter().for_each(|item| {
        let result = expensive_computation(item);
        results.lock().unwrap().push(result); // serialisation point
    });

    results.into_inner().unwrap()
}
```

## Good

```rust
use rayon::prelude::*;

fn process_all(items: &[Item]) -> Vec<Result> {
    // Each partition processes independently -- no shared mutable state
    items
        .par_iter()
        .map(|item| expensive_computation(item))
        .collect()
}

// For more control over partitioning:
fn process_batched(items: &[Item], batch_size: usize) -> Vec<Result> {
    items
        .par_chunks(batch_size)
        .flat_map(|chunk| {
            // Each chunk is processed independently
            chunk.iter().map(|item| expensive_computation(item))
        })
        .collect()
}

// For async workloads with independent partitions:
async fn process_async(items: Vec<Item>) -> Vec<Result> {
    let mut handles = Vec::new();

    for chunk in items.chunks(100) {
        let chunk = chunk.to_vec();
        handles.push(tokio::spawn(async move {
            let mut results = Vec::with_capacity(chunk.len());
            for item in &chunk {
                results.push(process_item(item).await);
            }
            results
        }));
    }

    let mut all_results = Vec::new();
    for handle in handles {
        all_results.extend(handle.await.unwrap());
    }
    all_results
}
```

## References

- [M-THROUGHPUT](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [perf-profile-first](perf-profile-first.md) - Profile before optimising
- [perf-benchmark-hotpaths](perf-benchmark-hotpaths.md) - Benchmark hot paths
