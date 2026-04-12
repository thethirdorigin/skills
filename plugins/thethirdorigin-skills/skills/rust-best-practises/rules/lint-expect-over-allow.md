# lint-expect-over-allow

> Use #[expect] with a reason attribute instead of #[allow] for justified overrides

## Why It Matters

Sometimes a clippy lint fires on code that is intentionally written that way -- for example, a function that genuinely needs many arguments during a migration, or an intentional fallthrough pattern. In these cases, the override should be temporary and traceable.

`#[expect]` is superior to `#[allow]` because the compiler warns when the expected lint no longer fires. This means stale overrides -- where the underlying code has changed and the lint no longer applies -- get cleaned up automatically. Combined with a `reason` attribute, each override documents why it exists and links to a tracking issue.

## Bad

```rust
// Silent, permanent suppression. Nobody knows why it's here.
// If the function is later refactored to fewer arguments, the allow stays forever.
#[allow(clippy::too_many_arguments)]
pub fn send_notification(
    user_id: u64,
    channel: Channel,
    subject: &str,
    body: &str,
    priority: Priority,
    retry_count: u32,
    timeout: Duration,
    metadata: &Metadata,
) -> Result<(), Error> {
    // ...
}
```

## Good

```rust
// Temporary override with justification and tracking issue.
// When #123 lands and this function takes a config struct,
// the compiler will warn that the expect is no longer needed.
#[expect(
    clippy::too_many_arguments,
    reason = "Will be refactored to NotificationRequest struct in #123"
)]
pub fn send_notification(
    user_id: u64,
    channel: Channel,
    subject: &str,
    body: &str,
    priority: Priority,
    retry_count: u32,
    timeout: Duration,
    metadata: &Metadata,
) -> Result<(), Error> {
    // ...
}
```

## References

- [M-LINT-OVERRIDE-EXPECT](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [lint-fix-root-cause](lint-fix-root-cause.md) - Fix the root cause first
- [anti-silence-clippy](anti-silence-clippy.md) - Do not blanket-suppress warnings
