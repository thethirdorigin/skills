# iter-option-as-iter

> Treat Option as a zero-or-one element iterator for functional composition

## Why It Matters

`Option<T>` implements `IntoIterator`, yielding one element for `Some` and zero elements for `None`. This means `Option` integrates directly with iterator adapters like `.extend()`, `.chain()`, `.flatten()`, and `for` loops -- eliminating repetitive `if let Some(...)` boilerplate when you need to merge optional values into collections or iterator pipelines.

Leveraging this trait makes code more declarative: instead of branching on the presence or absence of a value, you express intent ("extend this collection with whatever the option holds") and let the iterator machinery handle the empty case. The result is shorter, more composable, and easier to chain with other iterator operations.

## Bad

```rust
fn gather_headers(
    required: Vec<Header>,
    auth: Option<Header>,
    trace_id: Option<Header>,
    request_id: Option<Header>,
) -> Vec<Header> {
    let mut headers = required;

    // Repetitive if-let for every optional header.
    if let Some(h) = auth {
        headers.push(h);
    }
    if let Some(h) = trace_id {
        headers.push(h);
    }
    if let Some(h) = request_id {
        headers.push(h);
    }

    headers
}
```

## Good

```rust
fn gather_headers(
    required: Vec<Header>,
    auth: Option<Header>,
    trace_id: Option<Header>,
    request_id: Option<Header>,
) -> Vec<Header> {
    // Option implements IntoIterator -- extend handles Some/None.
    let mut headers = required;
    headers.extend(auth);
    headers.extend(trace_id);
    headers.extend(request_id);
    headers
}

// Or build everything in a single iterator chain:
fn gather_headers_chain(
    required: Vec<Header>,
    auth: Option<Header>,
    trace_id: Option<Header>,
    request_id: Option<Header>,
) -> Vec<Header> {
    required
        .into_iter()
        .chain(auth)
        .chain(trace_id)
        .chain(request_id)
        .collect()
}

// flatten() also works with iterators of Options:
fn collect_valid(values: Vec<Option<u32>>) -> Vec<u32> {
    values.into_iter().flatten().collect()
}
```

## References

- [Option as iterator idiom](https://rust-unofficial.github.io/patterns/idioms/option-iter.html)

## See Also

- [iter-chains](iter-chains.md) - Compose operations with iterator chains
- [iter-option-combinators](iter-option-combinators.md) - Use Option combinators instead of match
