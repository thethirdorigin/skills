# anti-primitive-obsession

> Use newtypes where raw strings and integers represent domain concepts

## Why It Matters

When multiple parameters share the same primitive type, the compiler cannot catch argument swaps. Calling `transfer(account_a, account_b, amount)` with `(u64, u64, u64)` compiles even if you accidentally swap the account IDs with the amount. The bug manifests at runtime as a nonsensical transfer from account "500" to account "1" for amount "42".

Newtype wrappers turn these runtime bugs into compile-time errors. `transfer(from: AccountId, to: AccountId, amount: Satoshis)` makes it impossible to pass a `Satoshis` where an `AccountId` is expected. The type names also serve as documentation, making function signatures self-explanatory.

## Bad

```rust
pub fn transfer(
    from_account: u64,
    to_account: u64,
    amount: u64,
) -> Result<(), TransferError> {
    // Easy to call with swapped arguments:
    // transfer(amount, to_account, from_account) -- compiles!
    debit(from_account, amount)?;
    credit(to_account, amount)?;
    Ok(())
}

pub fn send_email(
    from: &str,
    to: &str,
    subject: &str,
    body: &str,
) -> Result<(), EmailError> {
    // send_email(body, subject, to, from) -- compiles!
    todo!()
}
```

## Good

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct AccountId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct Satoshis(u64);

pub fn transfer(
    from: AccountId,
    to: AccountId,
    amount: Satoshis,
) -> Result<(), TransferError> {
    // transfer(amount, to, from) -- compile error!
    // The types enforce correct usage.
    debit(from, amount)?;
    credit(to, amount)?;
    Ok(())
}

#[derive(Debug, Clone)]
pub struct EmailAddress(String);

impl EmailAddress {
    pub fn parse(input: &str) -> Result<Self, ValidationError> {
        // Validate format at construction time
        if !input.contains('@') {
            return Err(ValidationError::InvalidEmail);
        }
        Ok(Self(input.to_string()))
    }
}

pub fn send_email(
    from: &EmailAddress,
    to: &EmailAddress,
    subject: &Subject,
    body: &Body,
) -> Result<(), EmailError> {
    // Cannot swap from/to with subject/body -- different types.
    todo!()
}
```

## See Also

- [api-newtype-safety](api-newtype-safety.md) - Newtype patterns for API safety
- [anti-bool-params](anti-bool-params.md) - Replace booleans with enums
