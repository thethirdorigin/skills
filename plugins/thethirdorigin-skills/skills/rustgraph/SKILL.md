---
name: rustgraph
description: >
  Tool-knowledge skill for the rustgraph binary. Knows how to locate, index,
  and query a Rust codebase knowledge graph stored in SQLite. Provides CLI
  reference, database schema, and a library of reusable SQL query patterns.
  Used by other skills (audit, project-guide) as a composable building block.
triggers:
  - use rustgraph
  - query knowledge graph
  - index this codebase
  - explore with rustgraph
  - rustgraph
  - knowledge graph
  - codebase graph
---

# rustgraph — Rust Codebase Knowledge Graph

<context>
You have access to **rustgraph**, a CLI tool that indexes Rust codebases into a SQLite knowledge graph. The graph captures every type, trait, function, impl block, call site, import, and relationship in the workspace. You can query it with structured commands or raw SQL.

This skill teaches you how to use the tool. It does NOT tell you what to look for — that judgment belongs to the skill that invoked you (audit, project-guide, or direct user request).
</context>

---

## Step 0 — Locate the binary

<instructions>
Find the `rustgraph` binary. Check these locations in order:

1. `which rustgraph` (on PATH)
2. The project's own `target/release/rustgraph` (if rustgraph is a workspace member)
3. Common development locations: `~/github/thethirdorigin/rustgraph/target/release/rustgraph`
4. Debug build fallback: same paths with `target/debug/rustgraph`

If found, set a shell variable for subsequent commands:

```bash
RUSTGRAPH=/path/to/rustgraph
```

If not found, tell the user to build it:

```
rustgraph binary not found. Build it with:
  cd <rustgraph-repo> && cargo build --release
```

Then stop.
</instructions>

---

## Step 1 — Index the workspace

<instructions>
Build the knowledge graph for the current Rust workspace:

```bash
$RUSTGRAPH index . -o rustgraph.db
```

If the command fails (no `Cargo.toml`, not a Rust project), inform the user and stop.

After indexing, confirm with a summary:

```bash
$RUSTGRAPH stats -d rustgraph.db
```

Report: `Indexed: N files, N structs, N enums, N traits, N functions, N impl blocks, N edges, N calls tracked`
</instructions>

---

## CLI Reference

### Knowledge-base queries

All commands accept `--json` for machine-readable output and `-d <db>` to specify the database.

| Command | Purpose |
|---------|---------|
| `rustgraph function <NAME>` | Full context: callers, callees, types, impl context, docstring |
| `rustgraph struct <NAME>` | Fields, trait impls, methods, where referenced |
| `rustgraph trait <NAME>` | Methods, implementors, supertraits, usage as bounds |
| `rustgraph enum <NAME>` | Variants, trait impls, methods, references |
| `rustgraph file <PATH>` | All entities and relationships in a file |
| `rustgraph search <TERM>` | Search across all entity names |
| `rustgraph deps <NAME>` | Dependency chain (add `--reverse` for dependents) |
| `rustgraph graph <NAME> --format dot\|json` | Subgraph for visualisation |

### Utility commands

| Command | Purpose |
|---------|---------|
| `rustgraph stats` | Summary statistics for the indexed codebase |
| `rustgraph sql "<SQL>"` | Run raw SQL against the graph |
| `rustgraph schema` | Print full database schema |

---

## Database Schema

### Tables

`files`, `structs`, `enums`, `traits`, `functions`, `impl_blocks`, `modules`, `edges`, `type_refs`, `function_calls`, `use_statements`, `consts_statics`, `type_aliases`, `macro_invocations`, `derives`, `annotations`, `struct_fields`, `enum_variants`, `trait_methods`, `crates`, `crate_deps`

### Edge kinds

`contains`, `implements`, `has_method`, `field_type_ref`, `param_type_ref`, `return_type_ref`, `uses_trait`, `module_contains`, `depends_on`, `calls`, `imports`, `supertrait_of`, `macro_use`

### Key columns

- Most entity tables have: `id`, `name`, `file_id`, `line`, `visibility`, `is_in_test_module`
- `functions` additionally has: `body_line_count`, `param_count`, `return_type`, `is_async`
- `structs` additionally has: `field_count`
- `function_calls` has: `caller_fn_id`, `callee_name`, `file_id`, `line`, `is_method_call`
- `derives` has: `entity_id`, `entity_kind`, `derive_name`
- `annotations` has: `entity_id`, `entity_kind`, `attribute`, `line`
- `crate_deps` has: `crate_id`, `dep_name`, `dep_kind` (normal, dev, build)

---

## Reusable Query Patterns

These queries are building blocks. Combine and adapt them for your use case.

### Structural overview

```sql
-- Largest files by line count
SELECT relative_path, line_count FROM files ORDER BY line_count DESC LIMIT 20;

-- Entity distribution by file
SELECT f.relative_path, COUNT(DISTINCT s.id) as structs, COUNT(DISTINCT fn_.id) as functions
FROM files f
LEFT JOIN structs s ON s.file_id = f.id
LEFT JOIN functions fn_ ON fn_.file_id = f.id
GROUP BY f.id ORDER BY structs + functions DESC LIMIT 20;

-- Edge distribution (graph health check)
SELECT edge_kind, COUNT(*) as cnt FROM edges GROUP BY edge_kind ORDER BY cnt DESC;
```

### Type analysis

```sql
-- Pub structs with their derives
SELECT f.relative_path, s.name, GROUP_CONCAT(d.derive_name, ', ') as derives
FROM structs s
JOIN files f ON s.file_id = f.id
LEFT JOIN derives d ON d.entity_kind = 'struct' AND d.entity_id = s.id
WHERE s.visibility = 'pub' AND s.is_in_test_module = 0
GROUP BY s.id ORDER BY f.relative_path, s.name;

-- Large structs (> 8 fields)
SELECT s.name, f.relative_path, s.line, s.field_count
FROM structs s JOIN files f ON s.file_id = f.id
WHERE s.field_count > 8 AND s.is_in_test_module = 0
ORDER BY s.field_count DESC;

-- Pub structs missing a specific derive (parameterise the derive name)
SELECT s.name, f.relative_path, s.line
FROM structs s JOIN files f ON s.file_id = f.id
WHERE s.visibility = 'pub' AND s.is_in_test_module = 0
AND s.id NOT IN (SELECT entity_id FROM derives WHERE entity_kind = 'struct' AND derive_name = 'Debug')
ORDER BY f.relative_path;
```

### Function analysis

```sql
-- Long functions (body > N lines, parameterise threshold)
SELECT fn_.name, f.relative_path, fn_.line, fn_.body_line_count
FROM functions fn_ JOIN files f ON fn_.file_id = f.id
WHERE fn_.body_line_count > 40 AND fn_.is_in_test_module = 0
ORDER BY fn_.body_line_count DESC;

-- Functions with many parameters (> N)
SELECT fn_.name, f.relative_path, fn_.line, fn_.param_count
FROM functions fn_ JOIN files f ON fn_.file_id = f.id
WHERE fn_.param_count > 5 AND fn_.is_in_test_module = 0
ORDER BY fn_.param_count DESC;

-- Functions with most callers (high-impact change targets)
SELECT fn_.name, f.relative_path, fn_.line, COUNT(DISTINCT fc.caller_fn_id) as caller_count
FROM functions fn_
JOIN files f ON fn_.file_id = f.id
JOIN function_calls fc ON fc.callee_name = fn_.name
GROUP BY fn_.id HAVING caller_count > 5
ORDER BY caller_count DESC LIMIT 20;

-- Orphan functions (no callers, not pub, not test, not main)
SELECT fn_.name, f.relative_path, fn_.line
FROM functions fn_ JOIN files f ON fn_.file_id = f.id
WHERE fn_.visibility != 'pub' AND fn_.is_in_test_module = 0
AND fn_.name NOT IN (SELECT DISTINCT callee_name FROM function_calls)
AND fn_.name != 'main'
ORDER BY f.relative_path;

-- Result<_, String> return types (string-typed errors)
SELECT fn_.name, f.relative_path, fn_.line, fn_.return_type
FROM functions fn_ JOIN files f ON fn_.file_id = f.id
WHERE fn_.return_type LIKE '%String%' AND fn_.return_type LIKE '%Result%'
AND fn_.is_in_test_module = 0;
```

### Trait analysis

```sql
-- Traits with exactly 1 non-test implementor
SELECT t.name, f.relative_path, t.line, COUNT(ib.id) as impl_count,
       GROUP_CONCAT(ib.self_type, ', ') as implementors
FROM traits t
JOIN files f ON t.file_id = f.id
LEFT JOIN impl_blocks ib ON ib.trait_name = t.name AND ib.is_in_test_module = 0
WHERE t.is_in_test_module = 0
GROUP BY t.id HAVING impl_count = 1
ORDER BY t.name;

-- Files with many traits (potential trait explosion)
SELECT f.relative_path, COUNT(*) as trait_count
FROM traits t JOIN files f ON t.file_id = f.id
GROUP BY f.id HAVING trait_count > 5
ORDER BY trait_count DESC;
```

### Call graph analysis

```sql
-- .unwrap()/.expect() calls outside test modules
SELECT fn_.name, f.relative_path, fc.line, fc.callee_name
FROM function_calls fc
JOIN functions fn_ ON fc.caller_fn_id = fn_.id
JOIN files f ON fc.file_id = f.id
WHERE fc.callee_name IN ('unwrap', 'expect') AND fc.is_method_call = 1
AND fn_.is_in_test_module = 0
ORDER BY f.relative_path, fc.line;

-- Complex functions (most outgoing calls)
SELECT fn_.name, f.relative_path, fn_.line, fn_.body_line_count, COUNT(fc.id) as call_count
FROM functions fn_
JOIN files f ON fn_.file_id = f.id
LEFT JOIN function_calls fc ON fc.caller_fn_id = fn_.id
WHERE fn_.visibility = 'pub' AND fn_.is_in_test_module = 0
GROUP BY fn_.id ORDER BY call_count DESC LIMIT 10;
```

### Dependency and annotation queries

```sql
-- Check for a specific dev dependency (e.g. mockall)
SELECT dep_name FROM crate_deps WHERE dep_kind = 'dev' AND dep_name = 'mockall';

-- #[allow(dead_code)] annotations
SELECT a.attribute, f.relative_path, a.line
FROM annotations a
JOIN structs s ON a.entity_kind = 'struct' AND a.entity_id = s.id
JOIN files f ON s.file_id = f.id
WHERE a.attribute LIKE '%dead_code%'
UNION ALL
SELECT a.attribute, f.relative_path, a.line
FROM annotations a
JOIN functions fn_ ON a.entity_kind = 'function' AND a.entity_id = fn_.id
JOIN files f ON fn_.file_id = f.id
WHERE a.attribute LIKE '%dead_code%';

-- Unused imports
SELECT us.path, f.relative_path, us.line
FROM use_statements us JOIN files f ON us.file_id = f.id
WHERE us.is_glob = 0
AND us.path NOT IN (
  SELECT DISTINCT metadata FROM edges WHERE edge_kind = 'imports' AND metadata IS NOT NULL
) LIMIT 50;
```

---

## Tips

- Always use `--json` when feeding output to subsequent analysis; use plain text for human-readable exploration.
- Run queries in parallel where possible to reduce wall-clock time.
- For large codebases, index once and reuse the `.db` file across multiple queries.
- Use `rustgraph function <NAME>` before reading source — it gives you callers, callees, and type context without opening a file.
- Combine `rustgraph deps <NAME> --reverse` with caller counts to estimate blast radius of changes.

---

## References

- [rustgraph](https://github.com/thethirdorigin/rustgraph) — Source repository
