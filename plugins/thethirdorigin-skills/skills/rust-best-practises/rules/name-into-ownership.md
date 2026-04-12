# name-into-ownership

> Use into_ prefix for methods that consume self and transfer ownership

## Why It Matters

The `into_` prefix signals ownership transfer -- the method takes `self` by value, consuming the original. After calling an `into_` method, the caller knows the original value is gone (moved). This is a critical semantic signal: the caller cannot accidentally use the value after conversion.

Misusing `to_` for methods that consume self hides the ownership transfer, leading to confusing compiler errors when callers try to use the moved value.

## Bad

```rust
impl RequestBuilder {
    // Misleading: to_ suggests self is borrowed, but this consumes self
    fn to_request(self) -> Request {
        Request {
            method: self.method,
            url: self.url,
            body: self.body,
        }
    }
}

impl RawTransaction {
    // Misleading: as_ suggests a cheap view, but this consumes self
    fn as_signed(self, key: &SigningKey) -> SignedTransaction {
        SignedTransaction::sign(self, key)
    }
}
```

## Good

```rust
impl RequestBuilder {
    // into_ clearly signals: self is consumed, you get a Request back
    fn into_request(self) -> Request {
        Request {
            method: self.method,
            url: self.url,
            body: self.body,
        }
    }
}

impl RawTransaction {
    // into_ signals ownership transfer — original is consumed
    fn into_signed(self, key: &SigningKey) -> SignedTransaction {
        SignedTransaction::sign(self, key)
    }
}

impl ResponseBody {
    // into_inner is the idiomatic name for extracting the wrapped value
    fn into_inner(self) -> Vec<u8> {
        self.0
    }
}
```

## References

- [C-CONV](https://rust-lang.github.io/api-guidelines/naming.html#c-conv) - Ad-hoc conversions follow `as_`, `to_`, `into_` conventions

## See Also

- [name-as-cheap](name-as-cheap.md) - as_ prefix for cheap conversions
- [name-to-expensive](name-to-expensive.md) - to_ prefix for expensive conversions
