# api-no-out-params

> Return values instead of taking out-parameters

## Why It Matters

Out-parameters force callers to pre-allocate and initialize mutable state before calling your function. This makes APIs harder to chain, harder to read, and harder to use in functional pipelines. It also splits the type information across the call site and the variable declaration.

Returning owned values is idiomatic Rust. The compiler's move semantics and NRVO (Named Return Value Optimization) ensure that returning even large values is efficient. Reserve `&mut` parameters for the rare case where the caller genuinely needs to reuse an existing allocation across repeated calls.

## Bad

```rust
pub fn parse_tokens(input: &str, result: &mut Vec<Token>) {
    result.clear();
    for word in input.split_whitespace() {
        result.push(Token::from(word));
    }
}

pub fn read_metadata(path: &Path, name: &mut String, size: &mut u64) -> io::Result<()> {
    let meta = fs::metadata(path)?;
    *name = path.file_name().unwrap().to_string_lossy().into_owned();
    *size = meta.len();
    Ok(())
}

// Caller must create mutable variables first:
let mut tokens = Vec::new();
parse_tokens("hello world", &mut tokens);

let mut name = String::new();
let mut size = 0u64;
read_metadata(path, &mut name, &mut size)?;
```

## Good

```rust
pub fn parse_tokens(input: &str) -> Vec<Token> {
    input.split_whitespace().map(Token::from).collect()
}

pub struct FileInfo {
    pub name: String,
    pub size: u64,
}

pub fn read_metadata(path: &Path) -> io::Result<FileInfo> {
    let meta = fs::metadata(path)?;
    Ok(FileInfo {
        name: path.file_name().unwrap().to_string_lossy().into_owned(),
        size: meta.len(),
    })
}

// Clean call sites with no pre-allocation:
let tokens = parse_tokens("hello world");
let info = read_metadata(path)?;
```

## References

- [C-NO-OUT](https://rust-lang.github.io/api-guidelines/predictability.html#functions-do-not-take-out-parameters-c-no-out)

## See Also

- [api-constructors](api-constructors.md) - Constructor patterns for return values
