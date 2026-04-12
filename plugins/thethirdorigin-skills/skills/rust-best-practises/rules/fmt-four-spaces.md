# fmt-four-spaces

> Use 4-space indentation, never tabs

## Why It Matters

Rust's standard style mandates 4-space indentation, and rustfmt enforces it by default. Fighting this convention causes unnecessary diff noise when collaborators run the formatter, and it signals unfamiliarity with the ecosystem to reviewers.

Consistent indentation also matters for nested match arms and closures, where Rust code can indent several levels deep. Four spaces strike a balance between readability and horizontal space.

## Bad

```rust
fn process_order(order: &Order) -> Result<Receipt> {
  // 2-space indentation — non-standard
  match order.status {
    Status::Pending => {
      validate(order)?;
      charge(order)
    }
    Status::Completed => Ok(order.receipt()),
  }
}
```

## Good

```rust
fn process_order(order: &Order) -> Result<Receipt> {
    // 4-space indentation — rustfmt default
    match order.status {
        Status::Pending => {
            validate(order)?;
            charge(order)
        }
        Status::Completed => Ok(order.receipt()),
    }
}
```

## See Also

- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Automate formatting with cargo fmt
