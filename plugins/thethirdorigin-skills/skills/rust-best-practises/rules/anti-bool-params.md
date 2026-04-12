# anti-bool-params

> Replace boolean parameters with enums for call-site clarity

## Why It Matters

A call site like `deploy(true, false)` is opaque -- you must navigate to the function signature to understand what each boolean means. Worse, swapping the two arguments compiles without error and produces subtly wrong behaviour: deploying to staging with production settings, or deploying to production without dry-run protection.

Enums make every call site self-documenting. `deploy(Environment::Production, DryRun::No)` communicates intent immediately. The compiler also prevents swapping arguments because `Environment` and `DryRun` are distinct types.

## Bad

```rust
pub fn deploy(
    production: bool,
    dry_run: bool,
) -> Result<(), DeployError> {
    if production && !dry_run {
        // Actually deploy to production
    }
    Ok(())
}

// Call site -- what does true, false mean?
deploy(true, false)?;

// Accidentally swapped -- deploys nothing but thinks it's production
deploy(false, true)?;

pub fn create_user(
    name: &str,
    is_admin: bool,
    send_welcome_email: bool,
    require_mfa: bool,
) -> Result<User, Error> {
    // create_user("Alice", true, false, true) -- which bool is which?
    todo!()
}
```

## Good

```rust
#[derive(Debug, Clone, Copy)]
pub enum Environment {
    Production,
    Staging,
}

#[derive(Debug, Clone, Copy)]
pub enum DryRun {
    Yes,
    No,
}

pub fn deploy(
    env: Environment,
    dry_run: DryRun,
) -> Result<(), DeployError> {
    match (env, dry_run) {
        (Environment::Production, DryRun::No) => {
            // Actually deploy to production
        }
        (Environment::Production, DryRun::Yes) => {
            // Simulate production deployment
        }
        (Environment::Staging, _) => {
            // Deploy to staging
        }
    }
    Ok(())
}

// Call site is self-documenting:
deploy(Environment::Production, DryRun::No)?;

// For multiple options, use a builder or options struct:
pub struct CreateUserOptions {
    pub role: UserRole,
    pub welcome_email: WelcomeEmail,
    pub mfa: MfaRequirement,
}

pub enum UserRole { Admin, Member }
pub enum WelcomeEmail { Send, Skip }
pub enum MfaRequirement { Required, Optional }
```

## See Also

- [api-enum-over-bool](api-enum-over-bool.md) - Enum design patterns
- [anti-primitive-obsession](anti-primitive-obsession.md) - Use newtypes for domain concepts
