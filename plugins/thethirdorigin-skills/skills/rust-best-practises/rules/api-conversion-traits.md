# api-conversion-traits

> Implement From, AsRef, and AsMut for standard conversions

## Why It Matters

Rust's standard conversion traits power the `.into()` call, the `?` operator for error propagation, and generic function boundaries like `impl AsRef<str>`. When your types implement these traits, they integrate seamlessly with the rest of the ecosystem. Users can convert between types without learning custom method names.

Prefer `From` over `Into` (implementing From gives you Into for free). Use `TryFrom` when the conversion can fail. Implement `FromStr` when a type can be parsed from text, enabling `.parse()` on strings.

## Bad

```rust
pub struct Email(String);

impl Email {
    // Custom conversion method — callers must know this exists
    pub fn from_string(s: String) -> Self {
        Email(s)
    }

    // Custom parsing — doesn't integrate with .parse()
    pub fn parse(s: &str) -> Result<Self, EmailError> {
        if s.contains('@') {
            Ok(Email(s.to_owned()))
        } else {
            Err(EmailError::MissingAtSign)
        }
    }
}
```

## Good

```rust
pub struct Email(String);

impl From<String> for Email {
    fn from(s: String) -> Self {
        Email(s)
    }
}

impl AsRef<str> for Email {
    fn as_ref(&self) -> &str {
        &self.0
    }
}

impl FromStr for Email {
    type Err = EmailError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s.contains('@') {
            Ok(Email(s.to_owned()))
        } else {
            Err(EmailError::MissingAtSign)
        }
    }
}

// Now callers can use:
//   let email: Email = "user@example.com".parse()?;
//   let email: Email = raw_string.into();
//   send_message(email.as_ref());
```

## References

- [C-CONV-TRAITS](https://rust-lang.github.io/api-guidelines/interoperability.html#conversions-use-the-standard-traits-from-asref-asmut-c-conv-traits)

## See Also

- [api-impl-asref](api-impl-asref.md) - Accept impl AsRef for flexible inputs
- [api-newtype-safety](api-newtype-safety.md) - Newtypes that benefit from conversion traits
