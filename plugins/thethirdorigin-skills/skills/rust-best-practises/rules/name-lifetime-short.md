# name-lifetime-short

> Use short lowercase lifetimes: 'a, 'de, 'src

## Why It Matters

Lifetime annotations are syntactic overhead that readers must parse around to understand the actual types and relationships. Short names like `'a` minimize visual noise while still satisfying the compiler. In most cases, a single lifetime parameter is unambiguous and needs no descriptive name.

When a function has multiple lifetimes that could be confused, use short but descriptive names like `'src` and `'dst` or `'de` (for deserialization). Reserve verbose names for genuinely complex lifetime relationships -- they are rare.

## Bad

```rust
fn parse_transaction<'input_lifetime>(
    data: &'input_lifetime str,
    config: &'input_lifetime ParserConfig,
) -> Result<Transaction<'input_lifetime>> {
    // 'input_lifetime adds noise to every usage
    let header = parse_header::<'input_lifetime>(data)?;
    Ok(Transaction::new(header))
}

struct LedgerView<'database_connection_lifetime> {
    entries: &'database_connection_lifetime [LedgerEntry],
}
```

## Good

```rust
fn parse_transaction<'a>(
    data: &'a str,
    config: &'a ParserConfig,
) -> Result<Transaction<'a>> {
    let header = parse_header(data)?;
    Ok(Transaction::new(header))
}

struct LedgerView<'a> {
    entries: &'a [LedgerEntry],
}

// Multiple lifetimes — use short descriptive names
fn merge_ledgers<'src, 'dst>(
    source: &'src Ledger,
    destination: &'dst mut Ledger,
) -> MergeResult<'dst> {
    // 'src vs 'dst is clear and concise
    destination.append_from(source)
}
```

## See Also

- [name-funcs-snake](name-funcs-snake.md) - snake_case for functions and variables
