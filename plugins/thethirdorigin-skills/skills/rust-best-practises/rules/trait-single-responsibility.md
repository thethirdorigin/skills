# trait-single-responsibility

> Keep traits focused with a single responsibility

## Why It Matters

A "god trait" that bundles unrelated capabilities forces every implementor to provide all of them, even when only one is relevant. A struct that just needs to send emails must also implement user lookup and report formatting. This couples unrelated concerns, bloats implementations with stub methods, and makes mocking in tests painful — you end up creating a mock that implements twelve methods when you only care about one.

Small, focused traits are easier to implement, easier to mock, and easier to compose. When a function needs multiple capabilities, it can require multiple trait bounds: fn run<T: UserRepo + EmailSender>(service: &T). This is strictly more flexible than a single fat trait because callers can mix and match implementations.

## Bad

```rust
trait UserService {
    fn find_user(&self, id: UserId) -> Result<User, Error>;
    fn save_user(&self, user: &User) -> Result<(), Error>;
    fn send_welcome_email(&self, user: &User) -> Result<(), Error>;
    fn format_user_report(&self, users: &[User]) -> String;
    fn validate_password(&self, password: &str) -> bool;
    fn generate_avatar(&self, user: &User) -> Vec<u8>;
}

// Every implementor must provide all six methods.
// Every mock must stub all six methods.
```

## Good

```rust
trait UserRepo {
    fn find(&self, id: UserId) -> Result<User, RepoError>;
    fn save(&self, user: &User) -> Result<(), RepoError>;
}

trait EmailSender {
    fn send(&self, to: &str, subject: &str, body: &str) -> Result<(), EmailError>;
}

trait PasswordValidator {
    fn validate(&self, password: &str) -> bool;
}

// Compose via trait bounds when multiple capabilities are needed:
fn register_user<R: UserRepo, E: EmailSender, V: PasswordValidator>(
    repo: &R,
    email: &E,
    validator: &V,
    input: RegistrationInput,
) -> Result<User, RegistrationError> {
    if !validator.validate(&input.password) {
        return Err(RegistrationError::WeakPassword);
    }
    let user = User::from(input);
    repo.save(&user)?;
    email.send(user.email(), "Welcome", "Thanks for joining!")?;
    Ok(user)
}
```

## See Also

- [trait-supertraits](trait-supertraits.md) - Composing trait requirements via supertraits
- [trait-dynamic-dispatch](trait-dynamic-dispatch.md) - Using focused traits with dyn for DI
