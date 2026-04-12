# err-context-chain

> Carry context strings in error variants, not raw inner errors alone

## Why It Matters

When an error surfaces as "No such file or directory," the user has no idea which file or which operation triggered it. Was it the config file? A temp file? A socket path? Raw inner errors describe the symptom but not the situation.

Context-rich errors describe what the code was trying to do when the failure occurred. "Failed to read config at /etc/app.toml: No such file or directory" tells the user exactly what went wrong and where to look. This is the difference between a 30-second fix and a 30-minute debugging session.

## Bad

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error(transparent)]
    Io(#[from] io::Error),

    #[error(transparent)]
    Json(#[from] serde_json::Error),
}

fn load_config() -> Result<Config, AppError> {
    let contents = fs::read_to_string("/etc/app.toml")?;
    let config = serde_json::from_str(&contents)?;
    Ok(config)
}

// Error message: "No such file or directory (os error 2)"
// Which file? What operation? The caller has no idea.
```

## Good

```rust
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("failed to read config at {path}")]
    Read {
        path: PathBuf,
        #[source]
        source: io::Error,
    },

    #[error("failed to parse config at {path}")]
    Parse {
        path: PathBuf,
        #[source]
        source: serde_json::Error,
    },
}

fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let contents = fs::read_to_string(path).map_err(|source| ConfigError::Read {
        path: path.to_owned(),
        source,
    })?;

    let config = serde_json::from_str(&contents).map_err(|source| ConfigError::Parse {
        path: path.to_owned(),
        source,
    })?;

    Ok(config)
}

// Error message: "failed to read config at /etc/app.toml: No such file or directory (os error 2)"
```

## See Also

- [err-canonical-structs](err-canonical-structs.md) - Full error type design with backtraces
- [err-anyhow-app](err-anyhow-app.md) - Using .context() in application code
