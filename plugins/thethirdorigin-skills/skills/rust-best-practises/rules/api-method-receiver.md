# api-method-receiver

> Functions with a clear receiver are methods, not free functions

## Why It Matters

Methods are discoverable through the type system. IDE autocomplete shows all methods on a type when the user types a dot. Free functions require the user to already know the function name and the module it lives in.

When a function has a natural "subject" — the value it primarily operates on — make it a method on that type. Reserve free functions for constructors, conversions between types, and operations without a clear receiver.

## Bad

```rust
pub fn account_balance(account: &Account) -> Decimal {
    account.ledger.iter().map(|e| e.amount).sum()
}

pub fn account_is_active(account: &Account) -> bool {
    account.status == Status::Active
}

pub fn format_account_summary(account: &Account) -> String {
    format!("{}: {}", account.name, account_balance(account))
}

// Callers must know these functions exist and import them:
use crate::accounts::{account_balance, account_is_active, format_account_summary};
let bal = account_balance(&my_account);
```

## Good

```rust
impl Account {
    pub fn balance(&self) -> Decimal {
        self.ledger.iter().map(|e| e.amount).sum()
    }

    pub fn is_active(&self) -> bool {
        self.status == Status::Active
    }

    pub fn summary(&self) -> String {
        format!("{}: {}", self.name, self.balance())
    }
}

// Callers discover methods via autocomplete:
let bal = my_account.balance();
if my_account.is_active() {
    println!("{}", my_account.summary());
}
```

## References

- [C-METHOD](https://rust-lang.github.io/api-guidelines/predictability.html#functions-with-a-clear-receiver-are-methods-c-method)

## See Also

- [api-essential-inherent](api-essential-inherent.md) - Core functionality as inherent methods
