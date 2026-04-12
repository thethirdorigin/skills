# lint-cargo-fmt

> Run cargo fmt --check in CI to enforce consistent formatting

## Why It Matters

Code formatting debates consume review time without improving code quality. When formatting is enforced automatically, reviewers focus on logic and design instead of arguing about brace placement or import ordering.

Running `cargo fmt --all --check` in CI ensures that every merged commit follows the same formatting rules. Developers run `cargo fmt` locally before committing, and the CI check catches anything that slips through. The result is a codebase where diffs show only meaningful changes, not reformatting noise.

## Bad

```rust
// No formatting enforcement in CI.
// Developer A uses one style:
fn process(input:&str)->Result<Output,Error>{
    let data=parse(input)?;
    Ok(transform(data))
}

// Developer B uses another:
fn process(
    input: &str,
) -> Result<
    Output,
    Error,
> {
    let data = parse(input)?;
    Ok(transform(data))
}

// Every PR contains formatting "fixes" mixed with real changes.
```

## Good

```rust
// CI step:
// cargo fmt --all --check

// All code follows the same style automatically:
fn process(input: &str) -> Result<Output, Error> {
    let data = parse(input)?;
    Ok(transform(data))
}

// Optional: .rustfmt.toml for project-specific settings
// max_width = 100
// use_small_heuristics = "Max"
// imports_granularity = "Crate"
```

## See Also

- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Formatting configuration details
- [lint-clippy-all](lint-clippy-all.md) - Run clippy alongside formatting checks
