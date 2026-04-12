# perf-benchmark-hotpaths

> Create benchmarks around identified hot paths early

## Why It Matters

Without benchmarks, performance regressions are discovered in production -- after they have already affected users. A seemingly innocent change like switching from a `HashMap` to a `BTreeMap` or adding an extra allocation in a serialisation path can degrade throughput significantly.

Benchmarks for hot paths provide a baseline measurement and catch regressions in CI. They also give you confidence when refactoring: if the benchmark shows no regression, the change is safe to merge.

## Bad

```rust
// No benchmarks anywhere in the project.
// Performance regressions discovered only when users complain
// or monitoring alerts fire in production.

pub fn serialize_response(response: &Response) -> Vec<u8> {
    // Changed from manual serialization to serde_json.
    // Is it faster? Slower? Nobody knows until production.
    serde_json::to_vec(response).unwrap()
}
```

## Good

```rust
// benches/serialization.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use my_crate::{Response, serialize_response};

fn bench_serialize_small_response(c: &mut Criterion) {
    let response = Response::fixture_small();
    c.bench_function("serialize_small_response", |b| {
        b.iter(|| serialize_response(black_box(&response)))
    });
}

fn bench_serialize_large_response(c: &mut Criterion) {
    let response = Response::fixture_large();
    c.bench_function("serialize_large_response", |b| {
        b.iter(|| serialize_response(black_box(&response)))
    });
}

fn bench_parse_request(c: &mut Criterion) {
    let raw = include_bytes!("../fixtures/large_request.json");
    c.bench_function("parse_large_request", |b| {
        b.iter(|| parse_request(black_box(raw)))
    });
}

criterion_group!(
    benches,
    bench_serialize_small_response,
    bench_serialize_large_response,
    bench_parse_request,
);
criterion_main!(benches);
```

## References

- [M-HOTPATH](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [perf-profile-first](perf-profile-first.md) - Profile before optimising
- [perf-partition-throughput](perf-partition-throughput.md) - Partition work for throughput
