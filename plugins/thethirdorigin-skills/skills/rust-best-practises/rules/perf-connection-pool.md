# perf-connection-pool

> Use connection pooling for database and HTTP clients

## Why It Matters

Establishing a new database or HTTP connection is expensive: TCP handshake, TLS negotiation, authentication, and protocol setup can take tens of milliseconds. In a request-handling context, opening a new connection per request multiplies this latency by the request rate and can exhaust the server's connection limit under load.

Connection pooling amortises the setup cost across many requests. Connections are created once, returned to the pool after use, and reused by subsequent requests. The pool also manages connection limits, health checks, and idle timeout, preventing resource exhaustion.

## Bad

```rust
use sqlx::PgConnection;

async fn get_user(user_id: i64) -> Result<User, Error> {
    // New connection per request -- TCP + TLS + auth every time
    let mut conn = PgConnection::connect("postgres://localhost/mydb").await?;
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(user_id)
        .fetch_one(&mut conn)
        .await?;
    Ok(user)
    // Connection dropped here -- cannot be reused
}

async fn fetch_external_data(url: &str) -> Result<String, Error> {
    // New HTTP client per request -- no connection reuse
    let client = reqwest::Client::new();
    let body = client.get(url).send().await?.text().await?;
    Ok(body)
}
```

## Good

```rust
use sqlx::PgPool;

pub struct AppState {
    db: PgPool,
    http: reqwest::Client,
}

impl AppState {
    pub async fn new(database_url: &str) -> Result<Self, Error> {
        let db = PgPool::builder()
            .max_connections(20)
            .idle_timeout(Duration::from_secs(300))
            .connect(database_url)
            .await?;

        // reqwest::Client maintains an internal connection pool
        let http = reqwest::Client::builder()
            .pool_max_idle_per_host(10)
            .timeout(Duration::from_secs(30))
            .build()?;

        Ok(Self { db, http })
    }
}

async fn get_user(pool: &PgPool, user_id: i64) -> Result<User, Error> {
    // Borrows a connection from the pool -- returned automatically on drop
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(user_id)
        .fetch_one(pool)
        .await?;
    Ok(user)
}

async fn fetch_external_data(client: &reqwest::Client, url: &str) -> Result<String, Error> {
    // Reuses existing connections from the client's internal pool
    let body = client.get(url).send().await?.text().await?;
    Ok(body)
}
```

## See Also

- [crate-avoid-statics](crate-avoid-statics.md) - Pass shared resources through constructors
- [test-mockable-design](test-mockable-design.md) - Accept traits for testability
