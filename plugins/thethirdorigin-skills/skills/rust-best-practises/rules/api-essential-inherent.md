# api-essential-inherent

> Essential functionality is inherent — users should not need trait imports

## Why It Matters

When core methods are defined on a trait rather than as inherent methods, users must discover and import that trait before they can call basic operations. This is frustrating — the type is in scope, the method exists, but the compiler says it does not. The user must hunt through documentation to find which trait to import.

Place essential, everyday methods directly on the type as inherent methods. Reserve traits for interoperability patterns (Iterator, Display, From) and for methods that genuinely need polymorphism across multiple types.

## Bad

```rust
pub trait Queryable {
    fn execute(&self, sql: &str) -> Result<Rows, DbError>;
    fn fetch_one(&self, sql: &str) -> Result<Row, DbError>;
    fn fetch_all(&self, sql: &str) -> Result<Vec<Row>, DbError>;
}

pub struct Database { /* ... */ }

impl Queryable for Database {
    fn execute(&self, sql: &str) -> Result<Rows, DbError> { /* ... */ }
    fn fetch_one(&self, sql: &str) -> Result<Row, DbError> { /* ... */ }
    fn fetch_all(&self, sql: &str) -> Result<Vec<Row>, DbError> { /* ... */ }
}

// Caller must import the trait to use basic methods:
use mylib::Queryable; // Without this, db.execute("...") fails
let db = Database::connect("postgres://...").await?;
db.execute("DELETE FROM sessions WHERE expired = true").await?;
```

## Good

```rust
pub struct Database { /* ... */ }

// Core methods are inherent — no trait import needed
impl Database {
    pub fn execute(&self, sql: &str) -> Result<Rows, DbError> { /* ... */ }
    pub fn fetch_one(&self, sql: &str) -> Result<Row, DbError> { /* ... */ }
    pub fn fetch_all(&self, sql: &str) -> Result<Vec<Row>, DbError> { /* ... */ }
}

// Traits for interop only — Iterator, Display, etc.
impl fmt::Display for Database {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Database({})", self.url)
    }
}

// Caller just uses the type:
let db = Database::connect("postgres://...").await?;
db.execute("DELETE FROM sessions WHERE expired = true").await?;
```

## References

- [M-ESSENTIAL-FN-INHERENT](https://rust-lang.github.io/api-guidelines/flexibility.html)

## See Also

- [api-method-receiver](api-method-receiver.md) - Functions with receivers are methods
