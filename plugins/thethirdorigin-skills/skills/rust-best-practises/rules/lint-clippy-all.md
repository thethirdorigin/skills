# lint-clippy-all

> Run cargo clippy --all-targets --all-features during development and CI

## Why It Matters

Running clippy with default settings misses issues hiding behind feature gates and in test or benchmark code. The `--all-targets` flag includes tests, examples, and benches. The `--all-features` flag enables every feature gate so that conditionally compiled code is also analysed.

Promoting warnings to errors with `-D warnings` in CI prevents lint regressions from merging. Developers who run the same command locally catch issues before pushing, reducing CI round-trips.

## Bad

```rust
// CI pipeline only runs:
// cargo clippy

// This misses:
// - Code behind #[cfg(feature = "advanced")] that has a redundant clone
// - A test helper that silently ignores errors
// - A benchmark that uses deprecated API
```

## Good

```rust
// CI pipeline:
// cargo clippy --all-targets --all-features -- -D warnings

// Catches issues across all feature combinations:
#[cfg(feature = "advanced")]
pub fn process(data: &[u8]) -> Result<Output, Error> {
    // clippy catches: unnecessary clone, unused variable, etc.
    let processed = data.to_vec(); // clippy: consider using `data` directly
    transform(&processed)
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_process() {
        // clippy catches: unused Result, redundant assertions, etc.
        let _ = super::process(b"test"); // clippy: unused Result that must be used
    }
}
```

## References

- [M-STATIC-VERIFICATION](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [lint-fix-root-cause](lint-fix-root-cause.md) - Fix warnings at their root
- [lint-cargo-hack](lint-cargo-hack.md) - Test feature combinations with cargo-hack
