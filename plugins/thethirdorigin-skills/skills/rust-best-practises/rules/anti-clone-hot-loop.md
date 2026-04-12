# anti-clone-hot-loop

> Avoid cloning large data structures in hot loops

## Why It Matters

Cloning inside a loop multiplies the allocation cost by the iteration count. A 1KB struct cloned 10,000 times produces 10MB of heap allocations that must also be freed, putting pressure on the allocator and the garbage collector (in the form of drop calls). Even for small structs, the cumulative overhead of clone-and-drop in a tight loop can dominate runtime.

The fix is almost always to borrow instead of clone. If the called function only reads the data, accept a reference. If it needs ownership of part of the data, clone only that part. Reserve `.clone()` for cases where you genuinely need independent ownership.

## Bad

```rust
struct Report {
    headers: Vec<String>,
    metadata: HashMap<String, String>,
    template: String,
}

fn generate_reports(report: &Report, entries: &[Entry]) -> Vec<String> {
    let mut results = Vec::new();
    for entry in entries {
        // Clones the entire Report on every iteration:
        // headers Vec, metadata HashMap, template String -- all copied
        let owned_report = report.clone();
        results.push(render(owned_report, entry));
    }
    results
}

fn render(report: Report, entry: &Entry) -> String {
    // Only reads report.template -- didn't need ownership of the whole struct
    format!("{}: {}", report.template, entry.value)
}
```

## Good

```rust
struct Report {
    headers: Vec<String>,
    metadata: HashMap<String, String>,
    template: String,
}

fn generate_reports(report: &Report, entries: &[Entry]) -> Vec<String> {
    let mut results = Vec::new();
    for entry in entries {
        // Borrow instead of clone -- zero allocation cost
        results.push(render(report, entry));
    }
    results
}

fn render(report: &Report, entry: &Entry) -> String {
    // Accepts a reference -- no ownership needed
    format!("{}: {}", report.template, entry.value)
}

// Even more idiomatic with iterators:
fn generate_reports_iter(report: &Report, entries: &[Entry]) -> Vec<String> {
    entries.iter().map(|entry| render(report, entry)).collect()
}
```

## See Also

- [own-borrow-prefer](own-borrow-prefer.md) - Prefer borrowing over owning
- [perf-profile-first](perf-profile-first.md) - Profile before optimising
