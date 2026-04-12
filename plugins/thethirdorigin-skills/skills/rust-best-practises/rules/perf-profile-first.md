# perf-profile-first

> Profile before optimising -- never guess where the bottleneck is

## Why It Matters

Human intuition about performance is unreliable. The function you assume is slow is often not the bottleneck. Optimising cold code wastes development time, adds complexity, and may even make performance worse by defeating compiler optimisations or increasing code size.

Profiling tools like `cargo flamegraph`, `criterion`, and `divan` reveal where time is actually spent. Once you know the real bottleneck, you can make targeted improvements and verify the impact with before-and-after measurements.

## Bad

```rust
// "This function must be slow because it does string manipulation"
// Rewritten with unsafe for "performance" without any measurement

pub fn extract_tokens(input: &str) -> Vec<&str> {
    let bytes = input.as_bytes();
    let mut tokens = Vec::new();
    let mut start = 0;
    // Unsafe pointer arithmetic -- complex, error-prone, and possibly no faster
    unsafe {
        let ptr = bytes.as_ptr();
        for i in 0..bytes.len() {
            if *ptr.add(i) == b' ' {
                tokens.push(std::str::from_utf8_unchecked(&bytes[start..i]));
                start = i + 1;
            }
        }
        if start < bytes.len() {
            tokens.push(std::str::from_utf8_unchecked(&bytes[start..]));
        }
    }
    tokens
}
```

## Good

```rust
// Step 1: Write clear, idiomatic code
pub fn extract_tokens(input: &str) -> Vec<&str> {
    input.split_whitespace().collect()
}

// Step 2: Profile to identify actual bottlenecks
// $ cargo flamegraph --bin my-app
// Result: 80% of time is in database queries, not string parsing

// Step 3: If this function IS the bottleneck, benchmark and optimise
// benches/tokenizer.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_extract_tokens(c: &mut Criterion) {
    let input = "the quick brown fox ".repeat(1000);
    c.bench_function("extract_tokens", |b| {
        b.iter(|| extract_tokens(black_box(&input)))
    });
}

criterion_group!(benches, bench_extract_tokens);
criterion_main!(benches);
```

## See Also

- [perf-benchmark-hotpaths](perf-benchmark-hotpaths.md) - Benchmark identified hot paths
- [perf-zero-cost-trust](perf-zero-cost-trust.md) - Trust the compiler for iterator chains
