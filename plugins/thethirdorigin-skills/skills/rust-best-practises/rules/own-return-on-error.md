# own-return-on-error

> Return consumed arguments inside the error type when a function takes ownership and fails

## Why It Matters

When a function accepts arguments by value (`self`, `String`, `Vec<T>`, etc.) and the operation can fail, the caller permanently loses access to those values on the error path. This forces callers into defensive cloning before every call "just in case," or into awkward two-phase patterns where they first validate, then execute.

Returning the consumed arguments inside the error type gives the caller the option to recover the data and retry, log it, or take a different path. This pattern is used in the standard library itself -- `Mutex::lock` returns a `PoisonError` that contains the `MutexGuard`, and `mpsc::Sender::send` returns the unsent message inside `SendError<T>`.

## Bad

```rust
struct EmailClient {
    connection: SmtpConnection,
}

struct Email {
    to: String,
    subject: String,
    body: String,
}

#[derive(Debug, thiserror::Error)]
#[error("failed to send email: {reason}")]
struct SendError {
    reason: String,
}

impl EmailClient {
    // Takes ownership of both self and email.
    // On failure, the caller loses the connection AND the email.
    fn send(self, email: Email) -> Result<Receipt, SendError> {
        if !self.connection.is_healthy() {
            return Err(SendError {
                reason: "connection lost".into(),
            });
        }
        // ... send logic ...
        Ok(Receipt::new())
    }
}

// Caller must clone defensively to handle retries
fn deliver(client: EmailClient, email: Email) -> Result<Receipt> {
    let email_backup = email.clone(); // Defensive clone -- wasteful if send succeeds
    match client.send(email) {
        Ok(receipt) => Ok(receipt),
        Err(_) => {
            let new_client = EmailClient::reconnect()?;
            new_client.send(email_backup).map_err(Into::into)
        }
    }
}
```

## Good

```rust
struct EmailClient {
    connection: SmtpConnection,
}

struct Email {
    to: String,
    subject: String,
    body: String,
}

#[derive(Debug, thiserror::Error)]
#[error("failed to send email: {reason}")]
struct SendError {
    reason: String,
    /// The client and email are returned so the caller can retry.
    pub recovered: (EmailClient, Email),
}

impl EmailClient {
    // On failure, both self and email are returned inside the error.
    fn send(self, email: Email) -> Result<Receipt, SendError> {
        if !self.connection.is_healthy() {
            return Err(SendError {
                reason: "connection lost".into(),
                recovered: (self, email),
            });
        }
        // ... send logic ...
        Ok(Receipt::new())
    }
}

// Caller recovers values from the error -- no defensive cloning needed
fn deliver(client: EmailClient, email: Email) -> Result<Receipt> {
    match client.send(email) {
        Ok(receipt) => Ok(receipt),
        Err(err) => {
            let (old_client, email) = err.recovered;
            let new_client = EmailClient::reconnect()?;
            new_client.send(email).map_err(Into::into)
        }
    }
}
```

## References

- [Return consumed arg on error](https://rust-unofficial.github.io/patterns/idioms/return-consumed-arg-on-error.html)

## See Also

- [err-result-recoverable](err-result-recoverable.md) - Use Result for recoverable errors
