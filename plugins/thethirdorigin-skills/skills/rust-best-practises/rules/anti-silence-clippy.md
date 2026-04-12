# anti-silence-clippy

> Fix clippy warnings at their root -- do not blanket-suppress with #[allow]

## Why It Matters

Blanket `#[allow]` attributes on modules or crates suppress entire categories of warnings, hiding real problems alongside false positives. A module-level `#[allow(clippy::complexity)]` silences warnings about overly complex match arms, deeply nested control flow, and redundant operations -- all of which are genuine maintainability risks.

Each warning deserves individual attention. Most can be fixed by improving the code. The few that are genuinely inapplicable should use `#[expect]` with a reason, not a blanket allow that suppresses future warnings too.

## Bad

```rust
// Blanket suppression at the module level -- hides all complexity warnings
#[allow(clippy::complexity)]
mod order_processing {
    pub fn process_order(order: &Order) -> Result<Receipt, Error> {
        // 150 lines of deeply nested match/if/for
        // clippy would flag 12 different issues, all hidden
        match order.status {
            Status::New => {
                if order.items.len() > 0 {
                    for item in &order.items {
                        match item.category {
                            Category::Physical => {
                                if item.weight > 0.0 {
                                    // ... 80 more lines
                                }
                            }
                            _ => {}
                        }
                    }
                }
            }
            _ => {}
        }
        todo!()
    }
}
```

## Good

```rust
mod order_processing {
    pub fn process_order(order: &Order) -> Result<Receipt, Error> {
        validate_order(order)?;
        let items = categorize_items(&order.items);
        let shipping = calculate_shipping(&items.physical)?;
        let total = compute_total(&items, shipping);
        Ok(Receipt::new(order.id, total))
    }

    fn validate_order(order: &Order) -> Result<(), Error> {
        if order.items.is_empty() {
            return Err(Error::EmptyOrder);
        }
        Ok(())
    }

    fn categorize_items(items: &[Item]) -> CategorizedItems {
        let physical: Vec<_> = items.iter().filter(|i| i.is_physical()).collect();
        let digital: Vec<_> = items.iter().filter(|i| i.is_digital()).collect();
        CategorizedItems { physical, digital }
    }

    fn calculate_shipping(items: &[&Item]) -> Result<Money, Error> {
        items
            .iter()
            .filter(|i| i.weight > 0.0)
            .map(|i| shipping_cost(i))
            .sum::<Result<Money, Error>>()
    }
}
```

## See Also

- [lint-fix-root-cause](lint-fix-root-cause.md) - Fix the root cause of warnings
- [lint-expect-over-allow](lint-expect-over-allow.md) - Use #[expect] for justified overrides
- [anti-monolith-function](anti-monolith-function.md) - Split monolithic functions
