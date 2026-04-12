# anti-deny-warnings

> Use specific lint names instead of blanket #[deny(warnings)]

## Why It Matters

`#![deny(warnings)]` turns every compiler warning into a hard error. This seems disciplined, but it effectively opts out of Rust's stability guarantee. When a new version of `rustc` introduces a previously unknown lint, code that compiled yesterday will fail today -- not because anything changed in your source, but because the compiler got smarter.

This is especially damaging in library crates published to crates.io: downstream users who run `cargo update` or `rustup update` suddenly face build failures they cannot fix without patching your crate. Even in application code, a routine toolchain update during CI can block an unrelated, time-sensitive deployment. The right approach is to name the specific lints you care about in source and reserve the blanket deny-warnings behaviour for CI via `RUSTFLAGS`.

## Bad

```rust
// crate root
#![deny(warnings)]

// A routine `rustup update` introduces a new lint and this crate
// stops compiling. Library consumers are blocked with no workaround.

pub fn calculate(x: f64) -> f64 {
    x * 2.0
}
```

## Good

```rust
// crate root -- name the specific lints you want to enforce.
#![deny(clippy::correctness, rust_2018_idioms, unsafe_op_in_unsafe_fn)]
#![warn(clippy::suspicious, clippy::style, clippy::pedantic)]

pub fn calculate(x: f64) -> f64 {
    x * 2.0
}

// In CI (not in source code), promote all warnings to errors:
// RUSTFLAGS="-D warnings" cargo build
// RUSTFLAGS="-D warnings" cargo clippy --all-targets
```

## References

- [deny(warnings) anti-pattern](https://rust-unofficial.github.io/patterns/anti_patterns/deny-warnings.html)

## See Also

- [lint-clippy-all](lint-clippy-all.md) - Run Clippy with broad lint groups
- [lint-enable-warnings](lint-enable-warnings.md) - Keep warnings visible during development
- [lint-expect-over-allow](lint-expect-over-allow.md) - Prefer expect over allow for intentional suppressions
