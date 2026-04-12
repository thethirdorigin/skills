# fmt-cargo-fmt

> Run cargo fmt before every commit

## Why It Matters

Automated formatting eliminates style debates in code review. When every developer runs the same formatter, diffs contain only meaningful changes -- never reformatting noise. Reviewers can focus on logic, correctness, and design instead of bikeshedding indentation.

Running `cargo fmt` as a pre-commit hook or CI gate ensures that unformatted code never reaches the main branch. This is especially important on teams where developers use different editors with different default settings.

## Bad

```rust
// Developer commits without running cargo fmt
// Reviewer leaves comments about formatting
// Next commit is pure reformatting — obscures real changes in git blame

fn  process(  items: Vec<Item> )->Result<()>{
for item in items{
    if item.is_valid(){handle(item)?;}
}
Ok(())}
```

## Good

```rust
// .pre-commit-config.yaml or .git/hooks/pre-commit runs cargo fmt --check
// CI pipeline includes: cargo fmt -- --check

fn process(items: Vec<Item>) -> Result<()> {
    for item in items {
        if item.is_valid() {
            handle(item)?;
        }
    }
    Ok(())
}
```

## See Also

- [fmt-four-spaces](fmt-four-spaces.md) - 4-space indentation standard
- [fmt-line-width](fmt-line-width.md) - 100-character line width
- [fmt-trailing-commas](fmt-trailing-commas.md) - Trailing commas in multi-line lists
