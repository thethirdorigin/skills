# name-no-weasel

> Use specific names -- remove Service, Manager, Handler, Helper, Processor

## Why It Matters

Words like Manager, Service, Handler, Helper, and Processor are "weasel words" that hide a type's actual responsibility behind a vague label. What does `CreditFacilityManager` do? Manage credit facilities -- but how? Does it create them? Store them? Validate them? The name doesn't tell you, which means it attracts unrelated responsibilities over time and grows into a god object.

Specific names force clear thinking about what a type actually does. A `CreditFacilityRepository` stores and retrieves. A `CreditFacilities` is a collection. A `DisbursementPolicy` decides whether to disburse. Each name constrains the type to a single responsibility.

## Bad

```rust
struct CreditFacilityManager {
    // What does "manage" mean? This struct will accumulate everything.
    db: DatabaseConnection,
    cache: Cache,
    validator: Validator,
    notifier: Notifier,
}

struct PaymentProcessorService {
    // "Processor" + "Service" — double weasel words
    gateway: PaymentGateway,
}

struct TransactionHelper {
    // "Helper" is the vaguest of all — helps how?
}
```

## Good

```rust
struct CreditFacilities {
    // Collection of facilities — clear and specific
    entries: HashMap<FacilityId, CreditFacility>,
}

struct PaymentGateway {
    // Specific: it's the gateway to the payment provider
    client: HttpClient,
    api_key: ApiKey,
}

struct TransactionValidator {
    // Specific: it validates transactions
    rules: Vec<Box<dyn ValidationRule>>,
}

struct DisbursementPolicy {
    // Specific: it encodes the policy for disbursements
    min_amount: Decimal,
    max_amount: Decimal,
    cooling_period: Duration,
}
```

## References

- [M-CONCISE-NAMES](https://rust-lang.github.io/api-guidelines/naming.html) - Use precise, intention-revealing names

## See Also

- [name-types-pascal](name-types-pascal.md) - PascalCase for types and traits
