# lint-fix-root-cause

> Fix the root cause of clippy warnings -- do not silence with #[allow]

## Why It Matters

Every clippy lint exists because the pattern it flags is genuinely problematic -- it may be error-prone, confusing, inefficient, or a known source of bugs. Silencing a warning with `#[allow]` hides the problem without addressing it. The underlying issue remains in the code, waiting to cause trouble.

Fixing the root cause improves the code. A `too_many_arguments` warning is a signal that the function's API needs a builder or config struct. A `cognitive_complexity` warning means the function should be decomposed. Treating lints as design feedback produces better software.

## Bad

```rust
#[allow(clippy::too_many_arguments)]
pub fn create_user(
    name: &str,
    email: &str,
    age: u32,
    role: Role,
    department: &str,
    manager_id: Option<u64>,
    start_date: NaiveDate,
    office: &str,
) -> Result<User, Error> {
    // The warning is silenced, but the API is still painful to use.
    // Callers must remember the order of 8 parameters.
}
```

## Good

```rust
pub struct CreateUserRequest {
    pub name: String,
    pub email: String,
    pub age: u32,
    pub role: Role,
    pub department: String,
    pub manager_id: Option<u64>,
    pub start_date: NaiveDate,
    pub office: String,
}

pub fn create_user(request: CreateUserRequest) -> Result<User, Error> {
    // No warning to suppress -- the API is genuinely better.
    // Callers use named fields, and adding new fields is non-breaking.
}
```

## See Also

- [lint-expect-over-allow](lint-expect-over-allow.md) - Use #[expect] for justified overrides
- [anti-silence-clippy](anti-silence-clippy.md) - Do not blanket-suppress warnings
