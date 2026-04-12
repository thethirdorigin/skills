# async-all-io

> Make all I/O operations async -- use the project's async runtime

## Why It Matters

Blocking I/O in an async function monopolises the runtime thread. While a `std::fs::read_to_string` call waits for the disk, no other task on that thread can make progress. In a web server handling hundreds of concurrent requests, a single blocking call can stall all requests scheduled on the same worker thread.

Use the async equivalents from your runtime (`tokio::fs`, `tokio::net`, etc.) for all file, network, and database operations. These yield control back to the runtime while waiting, allowing other tasks to run.

## Bad

```rust
async fn load_config(path: &str) -> Result<AppConfig> {
    // Blocks the runtime thread while waiting for disk I/O
    let content = std::fs::read_to_string(path)?;
    let config: AppConfig = serde_json::from_str(&content)?;
    Ok(config)
}

async fn fetch_exchange_rate(url: &str) -> Result<Decimal> {
    // std::net blocks — entire runtime thread is stalled
    let response = std::io::Read::read_to_string(
        &mut std::net::TcpStream::connect(url)?
    )?;
    Ok(parse_rate(&response)?)
}
```

## Good

```rust
async fn load_config(path: &str) -> Result<AppConfig> {
    // Yields to the runtime while waiting for disk I/O
    let content = tokio::fs::read_to_string(path).await?;
    let config: AppConfig = serde_json::from_str(&content)?;
    Ok(config)
}

async fn fetch_exchange_rate(client: &reqwest::Client, url: &str) -> Result<Decimal> {
    // Async HTTP — other tasks continue while we wait for the response
    let response = client.get(url).send().await?.text().await?;
    Ok(parse_rate(&response)?)
}
```

## See Also

- [async-no-block](async-no-block.md) - Never block in async context
