# api-builder-pattern

> Use the Builder pattern when a type has 4+ optional parameters

## Why It Matters

Constructors with many optional parameters produce call sites littered with `None` values that obscure the one or two fields the caller actually wants to set. Worse, positional arguments make it easy to swap two `Option<Duration>` parameters without the compiler noticing.

The Builder pattern solves both problems. Required parameters go into the builder constructor, optional parameters are set through named methods, and `build()` validates invariants. Call sites read like a configuration checklist, and adding new optional fields is a non-breaking change.

## Bad

```rust
pub struct HttpClient {
    base_url: String,
    timeout: Option<Duration>,
    max_retries: Option<u32>,
    user_agent: Option<String>,
    proxy: Option<Url>,
    follow_redirects: Option<bool>,
}

impl HttpClient {
    pub fn new(
        base_url: String,
        timeout: Option<Duration>,
        max_retries: Option<u32>,
        user_agent: Option<String>,
        proxy: Option<Url>,
        follow_redirects: Option<bool>,
    ) -> Self {
        // ...
    }
}

// Call site is unreadable:
let client = HttpClient::new(
    "https://api.example.com".into(),
    None,
    Some(3),
    None,
    None,
    Some(true),
);
```

## Good

```rust
pub struct HttpClient { /* private fields */ }

pub struct HttpClientBuilder {
    base_url: String,
    timeout: Duration,
    max_retries: u32,
    user_agent: Option<String>,
    proxy: Option<Url>,
    follow_redirects: bool,
}

impl HttpClient {
    pub fn builder(base_url: impl Into<String>) -> HttpClientBuilder {
        HttpClientBuilder {
            base_url: base_url.into(),
            timeout: Duration::from_secs(30),
            max_retries: 3,
            user_agent: None,
            proxy: None,
            follow_redirects: true,
        }
    }
}

impl HttpClientBuilder {
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn max_retries(mut self, n: u32) -> Self {
        self.max_retries = n;
        self
    }

    pub fn user_agent(mut self, agent: impl Into<String>) -> Self {
        self.user_agent = Some(agent.into());
        self
    }

    pub fn build(self) -> HttpClient {
        HttpClient { /* ... */ }
    }
}

// Call site is self-documenting:
let client = HttpClient::builder("https://api.example.com")
    .max_retries(5)
    .timeout(Duration::from_secs(10))
    .build();
```

## References

- [C-BUILDER](https://rust-lang.github.io/api-guidelines/type-safety.html#builders-enable-construction-of-complex-values-c-builder)
- [M-INIT-BUILDER](https://rust-lang.github.io/api-guidelines/type-safety.html)

## See Also

- [api-constructors](api-constructors.md) - Constructor conventions
- [api-private-fields](api-private-fields.md) - Keep fields private for encapsulation
