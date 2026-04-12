# fmt-comment-space

> Place a single space after comment sigils

## Why It Matters

A space after `//` and inside `/* */` is the universal Rust style. Unlike most formatting issues, rustfmt does not automatically fix comment spacing, so this must be enforced through habit and code review.

Consistent comment formatting improves scannability. When every comment follows the same pattern, readers can quickly distinguish comments from commented-out code and parse the text without visual friction.

## Bad

```rust
//Calculate the compound interest over the given period
fn compound_interest(principal: f64, rate: f64, periods: u32) -> f64 {
    /*This uses the standard compound interest formula*/
    let factor = (1.0 + rate).powi(periods as i32); //apply exponentiation
    principal * factor //return final amount
}
```

## Good

```rust
// Calculate the compound interest over the given period
fn compound_interest(principal: f64, rate: f64, periods: u32) -> f64 {
    /* This uses the standard compound interest formula */
    let factor = (1.0 + rate).powi(periods as i32); // apply exponentiation
    principal * factor // return final amount
}
```

## See Also

- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Automate formatting with cargo fmt
