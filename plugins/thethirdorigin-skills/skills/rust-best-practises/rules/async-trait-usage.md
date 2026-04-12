# async-trait-usage

> Use async_trait or native async traits (edition 2024+) for trait definitions

## Why It Matters

Rust traits historically could not have `async fn` methods because the compiler could not determine the size of the returned future at compile time. The `async_trait` crate solves this by boxing the future, providing ergonomic syntax at the cost of one heap allocation per call.

Starting with Rust edition 2024, native `async fn` in traits is fully stabilised and avoids the boxing overhead entirely. For new code on edition 2024+, prefer native async traits. For code that must support older editions, `async_trait` remains the standard solution.

## Bad

```rust
use std::future::Future;
use std::pin::Pin;

// Manual boxing — verbose, error-prone, hard to read
trait UserRepository {
    fn find_by_id(
        &self,
        id: UserId,
    ) -> Pin<Box<dyn Future<Output = Result<User>> + Send + '_>>;

    fn save(
        &self,
        user: &User,
    ) -> Pin<Box<dyn Future<Output = Result<()>> + Send + '_>>;
}

impl UserRepository for PostgresUserRepo {
    fn find_by_id(
        &self,
        id: UserId,
    ) -> Pin<Box<dyn Future<Output = Result<User>> + Send + '_>> {
        Box::pin(async move {
            // implementation
            todo!()
        })
    }

    fn save(
        &self,
        user: &User,
    ) -> Pin<Box<dyn Future<Output = Result<()>> + Send + '_>> {
        Box::pin(async move {
            // implementation
            todo!()
        })
    }
}
```

## Good

```rust
// Option A: async_trait crate (works on all editions)
use async_trait::async_trait;

#[async_trait]
trait UserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<User>;
    async fn save(&self, user: &User) -> Result<()>;
}

#[async_trait]
impl UserRepository for PostgresUserRepo {
    async fn find_by_id(&self, id: UserId) -> Result<User> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id)
            .fetch_one(&self.pool)
            .await
            .map_err(Into::into)
    }

    async fn save(&self, user: &User) -> Result<()> {
        sqlx::query("INSERT INTO users (id, name) VALUES ($1, $2)")
            .bind(user.id)
            .bind(&user.name)
            .execute(&self.pool)
            .await?;
        Ok(())
    }
}

// Option B: Native async traits (edition 2024+, zero overhead)
trait UserRepository {
    async fn find_by_id(&self, id: UserId) -> Result<User>;
    async fn save(&self, user: &User) -> Result<()>;
}
```

## See Also

- [async-send-sync](async-send-sync.md) - Send + Sync bounds for async trait objects
