# name-no-get-prefix

> Name simple getters after the field without a get_ prefix

## Why It Matters

In Rust, simple field accessors are named after the field they expose -- `name()`, not `get_name()`. The `get_` prefix adds noise without information, since the method signature already communicates that it returns a value without side effects. This convention is followed by the standard library (`Vec::len()`, `String::capacity()`, `Path::extension()`) and the entire ecosystem.

Reserve `get` for methods that do something more than return a field, such as `HashMap::get()` which performs a lookup and returns an `Option`.

## Bad

```rust
impl CreditFacility {
    fn get_id(&self) -> &FacilityId {
        &self.id
    }

    fn get_status(&self) -> FacilityStatus {
        self.status
    }

    fn get_balance(&self) -> Decimal {
        self.balance
    }

    fn get_customer_name(&self) -> &str {
        &self.customer_name
    }
}
```

## Good

```rust
impl CreditFacility {
    fn id(&self) -> &FacilityId {
        &self.id
    }

    fn status(&self) -> FacilityStatus {
        self.status
    }

    fn balance(&self) -> Decimal {
        self.balance
    }

    fn customer_name(&self) -> &str {
        &self.customer_name
    }
}
```

## References

- [C-GETTER](https://rust-lang.github.io/api-guidelines/naming.html#c-getter) - Getter names follow Rust convention

## See Also

- [name-funcs-snake](name-funcs-snake.md) - snake_case for functions and methods
