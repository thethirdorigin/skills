# test-mockable-design

> Design for testability -- accept traits so dependencies can be mocked

## Why It Matters

Functions that depend on concrete types like database pools, HTTP clients, or filesystem handles can only be tested with those real services running. This makes tests slow, flaky, and dependent on external infrastructure. A test that requires a running PostgreSQL instance is not a unit test -- it is an integration test with extra steps.

Accepting trait bounds instead of concrete types lets you substitute lightweight mock implementations in tests. The production code uses the real service; test code uses an in-memory fake. Both satisfy the same trait contract, and the compiler verifies the substitution is valid.

## Bad

```rust
use sqlx::PgPool;

pub async fn get_user(db: &PgPool, user_id: i64) -> Result<User, AppError> {
    let row = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(user_id)
        .fetch_one(db)
        .await?;
    Ok(row)
}

// Test requires a real PostgreSQL database:
#[tokio::test]
async fn test_get_user() {
    let pool = PgPool::connect("postgres://localhost/test_db").await.unwrap();
    let user = get_user(&pool, 1).await.unwrap();
    assert_eq!(user.name, "Alice");
}
```

## Good

```rust
#[async_trait]
pub trait UserRepository {
    async fn find_by_id(&self, user_id: i64) -> Result<User, AppError>;
}

pub async fn get_user(
    repo: &impl UserRepository,
    user_id: i64,
) -> Result<User, AppError> {
    repo.find_by_id(user_id).await
}

// Production implementation:
pub struct PgUserRepository {
    pool: PgPool,
}

#[async_trait]
impl UserRepository for PgUserRepository {
    async fn find_by_id(&self, user_id: i64) -> Result<User, AppError> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(user_id)
            .fetch_one(&self.pool)
            .await
            .map_err(AppError::from)
    }
}

// Test with a mock -- no database needed:
#[cfg(test)]
mod tests {
    use super::*;

    struct MockUserRepo;

    #[async_trait]
    impl UserRepository for MockUserRepo {
        async fn find_by_id(&self, user_id: i64) -> Result<User, AppError> {
            Ok(User { id: user_id, name: "Alice".into() })
        }
    }

    #[tokio::test]
    async fn get_user_returns_user_from_repository() {
        let user = get_user(&MockUserRepo, 1).await.unwrap();
        assert_eq!(user.name, "Alice");
    }
}
```

## References

- [M-MOCKABLE-SYSCALLS](https://rust-lang.github.io/api-guidelines/future-proofing.html)
- [M-DESIGN-FOR-AI](https://rust-lang.github.io/api-guidelines/future-proofing.html)

## See Also

- [test-cfg-module](test-cfg-module.md) - Colocate unit tests with the code
- [test-test-util-feature](test-test-util-feature.md) - Share test utilities via feature flags
