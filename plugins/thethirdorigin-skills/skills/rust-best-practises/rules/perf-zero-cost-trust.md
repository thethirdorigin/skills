# perf-zero-cost-trust

> Trust the compiler to optimise iterator chains and generics

## Why It Matters

Rust's zero-cost abstractions are not marketing -- they are a design principle backed by monomorphisation and aggressive inlining. The compiler specialises generic functions for each concrete type, unrolls iterator adaptors into straight-line code, and eliminates bounds checks when it can prove they are unnecessary.

Hand-unrolling loops, writing unsafe pointer arithmetic, or avoiding iterators "for performance" produces code that is harder to read, harder to maintain, and usually no faster. In many cases, the hand-written version is slower because it defeats the compiler's optimisation passes.

## Bad

```rust
// Hand-unrolled loop with unsafe pointer arithmetic
// "for performance" -- but actually harder for the compiler to optimise
pub fn sum_squares(values: &[f64]) -> f64 {
    let mut total = 0.0;
    let len = values.len();
    let ptr = values.as_ptr();
    unsafe {
        let mut i = 0;
        while i < len {
            let v = *ptr.add(i);
            total += v * v;
            i += 1;
        }
    }
    total
}
```

## Good

```rust
// Idiomatic iterator chain -- the compiler generates the same (or better) assembly
pub fn sum_squares(values: &[f64]) -> f64 {
    values.iter().map(|v| v * v).sum()
}

// The compiler:
// 1. Inlines the closure
// 2. Uses SIMD instructions when available
// 3. Unrolls the loop as appropriate
// 4. Eliminates bounds checks (iter() is already bounds-safe)

// For complex transformations, iterators compose cleanly:
pub fn process_valid_scores(entries: &[Entry]) -> Vec<f64> {
    entries
        .iter()
        .filter(|e| e.is_valid())
        .map(|e| e.score() * e.weight())
        .filter(|&s| s > 0.0)
        .collect()
}
```

## See Also

- [perf-profile-first](perf-profile-first.md) - Profile before optimising
- [unsafe-reserve-ffi](unsafe-reserve-ffi.md) - Reserve unsafe for justified cases
