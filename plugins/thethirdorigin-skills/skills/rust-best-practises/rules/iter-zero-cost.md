# iter-zero-cost

> Trust zero-cost abstractions — the compiler optimises iterator chains

## Why It Matters

Rust's Iterator trait is one of the language's flagship zero-cost abstractions. The compiler monomorphises each adapter (map, filter, fold) and inlines the closures, producing machine code that is equivalent to — and sometimes better than — hand-rolled loops with manual index management.

Reaching for unsafe pointer arithmetic or manual SIMD "for performance" before profiling is premature optimisation that sacrifices safety and readability for no measurable gain. The standard iterator combinators handle bounds checking, aliasing rules, and loop unrolling correctly. Start with idiomatic iterators, profile under realistic workloads, and only hand-optimise the specific hot spots that benchmarks identify.

## Bad

```rust
fn sum_squares(data: &[f64]) -> f64 {
    let mut total = 0.0;
    let ptr = data.as_ptr();
    let len = data.len();
    // Unsafe pointer arithmetic "for performance"
    unsafe {
        for i in 0..len {
            let val = *ptr.add(i);
            total += val * val;
        }
    }
    total
}
```

## Good

```rust
fn sum_squares(data: &[f64]) -> f64 {
    data.iter()
        .map(|x| x * x)
        .sum()
}

// If profiling reveals this is a bottleneck, consider:
// 1. Checking compiler flags (-C opt-level=3, -C target-cpu=native)
// 2. Using chunks() for explicit SIMD
// 3. Using rayon for parallelism: data.par_iter().map(|x| x * x).sum()
```

## See Also

- [iter-chains](iter-chains.md) - Preferring iterator chains for clarity
- [iter-no-intermediate-vec](iter-no-intermediate-vec.md) - Keeping pipelines lazy
