# err-panic-bugs-only

> Reserve panic for programming bugs and contract violations only

## Why It Matters

A panic unwinds the stack and terminates the current thread. In many programs this means the entire process crashes. This is the correct response to a programming bug — an invariant that the developer believed would always hold has been violated, and continuing execution could cause data corruption or security issues.

However, expected failures like "file not found," "invalid user input," or "network timeout" are not bugs. They are normal operational conditions that the program should handle gracefully. Using panic for these situations turns routine errors into catastrophic failures and makes the program brittle.

## Bad

```rust
fn find_user(db: &Database, id: UserId) -> User {
    match db.query_user(id) {
        Some(user) => user,
        // "Not found" is a normal condition, not a bug
        None => panic!("user {id} not found"),
    }
}

fn parse_port(input: &str) -> u16 {
    // User typos are expected, not bugs
    input.parse().expect("invalid port number")
}
```

## Good

```rust
fn find_user(db: &Database, id: UserId) -> Result<User, UserError> {
    db.query_user(id).ok_or(UserError::NotFound(id))
}

fn parse_port(input: &str) -> Result<u16, ParseIntError> {
    input.parse()
}

// Panic IS appropriate here: the internal invariant was violated
fn get_cached_entry(&self, index: usize) -> &Entry {
    assert!(
        index < self.cache.len(),
        "cache index {index} out of bounds (len {}): internal invariant violated",
        self.cache.len()
    );
    &self.cache[index]
}
```

## References

- M-PANIC-IS-STOP — A panic is a hard stop, not a recoverable error
- M-PANIC-ON-BUG — Panic only on programming errors and violated invariants

## See Also

- [err-result-recoverable](err-result-recoverable.md) - Using Result for expected failures
- [err-canonical-structs](err-canonical-structs.md) - Designing error types for recoverable errors
