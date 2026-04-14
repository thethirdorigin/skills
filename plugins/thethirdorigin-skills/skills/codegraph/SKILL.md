---
name: codegraph
description: >
  Tool-knowledge skill for CodeGraph, a local-first semantic code intelligence
  system. Knows how to initialize, index, and query a multi-language codebase
  knowledge graph via MCP tools, CLI, or raw SQL. Replaces grep, glob, and
  file reads for symbol search, call tracing, and structural exploration.
  Used by other skills (audit, project-guide) as a composable building block.
triggers:
  - use codegraph
  - query knowledge graph
  - index this codebase
  - explore with codegraph
  - codegraph
  - knowledge graph
  - codebase graph
  - search code
  - find symbol
  - find function
  - trace callers
  - what calls this
  - explore codebase
  - code intelligence
---

# CodeGraph — Semantic Code Intelligence

<context>
You have access to **CodeGraph**, a local-first code intelligence system that builds a semantic knowledge graph from any codebase. It parses source code with tree-sitter, extracts symbols (functions, classes, methods, types) and relationships (calls, imports, extends, implements), stores everything in a local SQLite database with FTS5 search, and resolves cross-file references.

**When `.codegraph/` exists in a project, CodeGraph is your PRIMARY tool for all code search and exploration.** Use it BEFORE grep, glob, or file reads. The only exceptions are literal text search (grep) and file editing (Read + StrReplace).

**When another skill (audit, project-guide) says "use the codegraph skill"**, follow this skill's steps to initialize, index if needed, and query the knowledge graph. Return structured data for the calling skill to consume.

**Supported languages**: TypeScript, JavaScript, TSX, JSX, Python, Go, Rust, Java, C, C++, C#, PHP, Ruby, Swift, Kotlin, Dart, Svelte, Liquid, Pascal/Delphi.
</context>

---

## Tool Selection Matrix

<instructions>
Use this table for every search or exploration task. There is no ambiguity — each task maps to exactly one tool.

| Task | Tool | Fallback (codegraph unavailable) |
|------|------|----------------------------------|
| Find a symbol by name | `codegraph_search` | Grep for definition patterns |
| Understand how a system works | `codegraph_explore` (via explore agent) | Spawn explore agent with file reads |
| Get context for a task or bug | `codegraph_context` | Read multiple files manually |
| Trace what calls a function | `codegraph_callers` | Grep for the function name |
| Trace what a function calls | `codegraph_callees` | Read the function, follow imports |
| Check blast radius before editing | `codegraph_impact` | Grep for references |
| Get a symbol's full source code | `codegraph_node` with `includeCode: true` | Read the file directly |
| Browse project file structure | `codegraph_files` | Glob or ls |
| Check index health and stats | `codegraph_status` | Count files manually |
| Find an exact string or regex | Grep / rg | — |
| Search inside file content | Grep / Read | — |
| Edit a file | Read then StrReplace | — |

The last three rows are the ONLY cases where grep or Read is the correct first choice. Everything above that line goes through CodeGraph.

Use the fallback column ONLY when CodeGraph is not initialized (no `.codegraph/` directory) and the user declines to initialize it.
</instructions>

---

## Step 0 — Detect and Initialize

<instructions>
Before any code exploration, check whether CodeGraph is initialized:

1. Look for a `.codegraph/` directory in the project root (or walk up parent directories)
2. If `.codegraph/codegraph.db` exists, CodeGraph is ready — proceed to Step 1
3. If `.codegraph/` does not exist, ask the user: "This project doesn't have CodeGraph initialized. Run `codegraph init -i` to build a knowledge graph?"
4. If the user agrees, run `codegraph init -i` from the project root
5. If the user declines, fall back to the fallback column in the tool selection matrix

After initialization, confirm with `codegraph status` to verify the index is healthy.
</instructions>

---

## Step 1 — MCP Tools Reference

<instructions>
When CodeGraph is available as an MCP server, use these tools directly. Each tool supports an optional `projectPath` parameter for cross-project queries.

### codegraph_search
Find symbols by name across the entire codebase. Returns locations and signatures, not source code.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | yes | — | Symbol name or partial name (e.g. "auth", "UserService", "handleSubmit") |
| `kind` | string | no | — | Filter: function, method, class, interface, type, variable, route, component |
| `limit` | number | no | 10 | Maximum results (1-100) |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_context
Build comprehensive context for a task. Returns entry points, related symbols, and key code snippets.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `task` | string | yes | — | Description of the task, bug, or feature |
| `maxNodes` | number | no | 20 | Maximum symbols to include |
| `includeCode` | boolean | no | true | Include code snippets for key symbols |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_explore
Deep exploration — returns comprehensive context grouped by file with full source code sections and a relationship map. Designed to replace multiple codegraph_node + Read calls in a single invocation.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | yes | — | Symbol names, file names, or short code terms. Use `codegraph_search` first to discover names |
| `maxFiles` | number | no | 12 | Maximum files to include source from (1-20) |
| `projectPath` | string | no | current | Path to a different initialized project |

Use specific symbol names and file names in the query — NOT natural language sentences.
- GOOD: `"AuthService loginUser session-manager.ts"`
- BAD: `"how does user authentication work in the login flow"`

**Explore budget** scales with project size:

| Indexed files | Max explore calls |
|---------------|-------------------|
| < 500 | 1 |
| 500 – 4,999 | 2 |
| 5,000 – 14,999 | 3 |
| 15,000 – 24,999 | 4 |
| 25,000+ | 5 |

Stop exploring and synthesize your answer once you hit the budget.

### codegraph_callers
Find all functions/methods that call a specific symbol.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol` | string | yes | — | Function, method, or class name |
| `limit` | number | no | 20 | Maximum callers (1-100) |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_callees
Find all functions/methods that a specific symbol calls.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol` | string | yes | — | Function, method, or class name |
| `limit` | number | no | 20 | Maximum callees (1-100) |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_impact
Analyze what code is affected by changing a symbol. Traverses the dependency graph to a configurable depth.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol` | string | yes | — | Symbol name to analyze |
| `depth` | number | no | 2 | Traversal depth (1-10) |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_node
Get detailed information about a single symbol, optionally with full source code.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `symbol` | string | yes | — | Symbol name (supports "Parent.child" qualified notation) |
| `includeCode` | boolean | no | false | Include full source code |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_files
Get the indexed file structure. Faster than filesystem scanning and includes metadata.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | no | all | Filter to files under this directory |
| `pattern` | string | no | — | Glob filter (e.g. "*.tsx", "**/*.test.ts") |
| `format` | string | no | tree | Output: tree, flat, or grouped (by language) |
| `includeMetadata` | boolean | no | true | Include language and symbol count per file |
| `maxDepth` | number | no | unlimited | Maximum directory depth |
| `projectPath` | string | no | current | Path to a different initialized project |

### codegraph_status
Get index health: file count, node count, edge count, database size, breakdown by kind and language.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `projectPath` | string | no | current | Path to a different initialized project |
</instructions>

---

## Step 2 — CLI Reference

<instructions>
Use the CLI when MCP is not available (CI pipelines, standalone terminal use, or when you need raw SQLite access for audit queries).

### Lifecycle commands

| Command | Description |
|---------|-------------|
| `codegraph init [path]` | Create `.codegraph/` directory and config. Add `-i` to also index |
| `codegraph index [path]` | Full index. Add `--force` to clear and rebuild |
| `codegraph sync [path]` | Incremental update (changed files only) |
| `codegraph status [path]` | Show index statistics |
| `codegraph uninit [path]` | Remove CodeGraph data. Add `--force` to skip prompt |
| `codegraph unlock [path]` | Remove a stale lock file |

### Query commands

| Command | Description |
|---------|-------------|
| `codegraph query <search>` | Symbol search. Options: `--kind`, `--limit`, `--json` |
| `codegraph files [path]` | File tree. Options: `--format tree\|flat\|grouped`, `--filter <dir>`, `--pattern <glob>`, `--max-depth`, `--json` |
| `codegraph context <task>` | Build AI context. Options: `--max-nodes`, `--no-code`, `--format markdown\|json` |
| `codegraph affected [files...]` | Find test files affected by changes. Options: `--stdin`, `--depth`, `--filter <glob>`, `--json` |

### MCP server

```bash
codegraph serve --mcp    # Start stdio MCP server
```

### CI example — run only affected tests

```bash
AFFECTED=$(git diff --name-only HEAD | codegraph affected --stdin --quiet)
if [ -n "$AFFECTED" ]; then
  npx vitest run $AFFECTED
fi
```

### Raw SQLite access

For deep queries (audit data gathering, cross-correlation), query the database directly:

```bash
sqlite3 .codegraph/codegraph.db "SELECT kind, COUNT(*) FROM nodes GROUP BY kind ORDER BY COUNT(*) DESC;"
```
</instructions>

---

## Step 3 — Database Schema

<instructions>

### Tables

| Table | Purpose |
|-------|---------|
| `nodes` | Code symbols: functions, classes, methods, types, variables, etc. |
| `edges` | Relationships between symbols: calls, imports, extends, contains, etc. |
| `files` | Indexed source files with content hashes and metadata |
| `unresolved_refs` | References pending resolution (from_node, reference_name, candidates) |
| `nodes_fts` | FTS5 virtual table for full-text search over symbol names, signatures, docstrings |
| `project_metadata` | Key-value store for project-level metadata |

### nodes columns

`id`, `kind`, `name`, `qualified_name`, `file_path`, `language`, `start_line`, `start_col`, `end_line`, `end_col`, `docstring`, `signature`, `visibility`, `is_exported`, `is_async`, `is_static`, `is_abstract`, `decorators` (JSON), `type_parameters` (JSON), `updated_at`

### edges columns

`source`, `target`, `kind`, `metadata` (JSON), `line`, `col`, `provenance`

### files columns

`path` (PK), `content_hash`, `language`, `size`, `modified_at`, `indexed_at`, `node_count`, `errors` (JSON)

### NodeKind values

`file`, `module`, `class`, `struct`, `interface`, `trait`, `protocol`, `function`, `method`, `property`, `field`, `variable`, `constant`, `enum`, `enum_member`, `type_alias`, `namespace`, `parameter`, `import`, `export`, `route`, `component`

### EdgeKind values

`contains`, `calls`, `imports`, `exports`, `extends`, `implements`, `references`, `type_of`, `returns`, `instantiates`, `overrides`, `decorates`
</instructions>

---

## Step 4 — Reusable SQL Query Patterns

<instructions>
These patterns are building blocks for audit data gathering, cross-correlation, and structural analysis. Adapt column filters and thresholds to the task.

### Structural overview

```sql
-- Node distribution by kind
SELECT kind, COUNT(*) as cnt FROM nodes GROUP BY kind ORDER BY cnt DESC;

-- Edge distribution (graph health check)
SELECT kind, COUNT(*) as cnt FROM edges GROUP BY kind ORDER BY cnt DESC;

-- Files by symbol count (densest files)
SELECT path, node_count, language FROM files ORDER BY node_count DESC LIMIT 20;

-- Files by size
SELECT path, size, language FROM files ORDER BY size DESC LIMIT 20;

-- Language distribution
SELECT language, COUNT(*) as file_count, SUM(node_count) as total_nodes
FROM files GROUP BY language ORDER BY file_count DESC;
```

### Symbol analysis

```sql
-- Functions by line count (long functions)
SELECT n.name, n.file_path, n.start_line, (n.end_line - n.start_line) as body_lines
FROM nodes n
WHERE n.kind IN ('function', 'method') AND (n.end_line - n.start_line) > 40
ORDER BY body_lines DESC LIMIT 20;

-- High fan-in: symbols with most callers (high-impact change targets)
SELECT target_node.name, target_node.file_path, target_node.kind,
       COUNT(DISTINCT e.source) as caller_count
FROM edges e
JOIN nodes target_node ON e.target = target_node.id
WHERE e.kind = 'calls'
GROUP BY e.target HAVING caller_count > 5
ORDER BY caller_count DESC LIMIT 20;

-- Orphan functions: not called by anything, not exported
SELECT n.name, n.file_path, n.start_line
FROM nodes n
WHERE n.kind IN ('function', 'method')
AND n.is_exported = 0
AND n.id NOT IN (SELECT DISTINCT target FROM edges WHERE kind = 'calls')
ORDER BY n.file_path, n.start_line;

-- Async functions
SELECT n.name, n.file_path, n.start_line, n.language
FROM nodes n
WHERE n.kind IN ('function', 'method') AND n.is_async = 1
ORDER BY n.file_path;
```

### Call graph analysis

```sql
-- Callers of a specific symbol
SELECT caller.name, caller.kind, caller.file_path, caller.start_line
FROM edges e
JOIN nodes caller ON e.source = caller.id
JOIN nodes callee ON e.target = callee.id
WHERE e.kind = 'calls' AND callee.name = '<SYMBOL_NAME>'
ORDER BY caller.file_path;

-- Callees of a specific symbol
SELECT callee.name, callee.kind, callee.file_path, callee.start_line
FROM edges e
JOIN nodes caller ON e.source = caller.id
JOIN nodes callee ON e.target = callee.id
WHERE e.kind = 'calls' AND caller.name = '<SYMBOL_NAME>'
ORDER BY callee.file_path;

-- Complex functions (most outgoing calls)
SELECT caller.name, caller.file_path, caller.start_line, COUNT(*) as call_count
FROM edges e
JOIN nodes caller ON e.source = caller.id
WHERE e.kind = 'calls' AND caller.kind IN ('function', 'method')
GROUP BY e.source ORDER BY call_count DESC LIMIT 20;
```

### Relationship queries

```sql
-- Inheritance chains: what extends what
SELECT child.name as child, parent.name as parent,
       child.file_path as child_file, parent.file_path as parent_file
FROM edges e
JOIN nodes child ON e.source = child.id
JOIN nodes parent ON e.target = parent.id
WHERE e.kind = 'extends'
ORDER BY parent.name, child.name;

-- Interface/trait implementations
SELECT impl.name as implementor, iface.name as interface,
       impl.file_path, impl.kind
FROM edges e
JOIN nodes impl ON e.source = impl.id
JOIN nodes iface ON e.target = iface.id
WHERE e.kind = 'implements'
ORDER BY iface.name, impl.name;

-- Import graph: what imports what
SELECT importer.name, importer.file_path, imported.name, imported.file_path
FROM edges e
JOIN nodes importer ON e.source = importer.id
JOIN nodes imported ON e.target = imported.id
WHERE e.kind = 'imports'
ORDER BY importer.file_path;

-- Cross-file dependencies: files connected by edges
SELECT DISTINCT n1.file_path as source_file, n2.file_path as target_file, e.kind
FROM edges e
JOIN nodes n1 ON e.source = n1.id
JOIN nodes n2 ON e.target = n2.id
WHERE n1.file_path != n2.file_path AND e.kind != 'contains'
ORDER BY source_file, target_file;
```

### Audit-oriented queries

```sql
-- Symbols with no documentation (public only)
SELECT n.name, n.kind, n.file_path, n.start_line
FROM nodes n
WHERE n.visibility = 'public' AND n.is_exported = 1
AND (n.docstring IS NULL OR n.docstring = '')
AND n.kind IN ('function', 'method', 'class', 'interface', 'trait')
ORDER BY n.file_path;

-- Classes/structs with many fields (potential god objects)
SELECT parent.name, parent.kind, parent.file_path, COUNT(*) as field_count
FROM edges e
JOIN nodes parent ON e.source = parent.id
JOIN nodes field ON e.target = field.id
WHERE e.kind = 'contains' AND field.kind IN ('field', 'property')
AND parent.kind IN ('class', 'struct', 'interface')
GROUP BY parent.id HAVING field_count > 8
ORDER BY field_count DESC;

-- Single-implementation interfaces/traits
SELECT iface.name, iface.file_path, COUNT(DISTINCT e.source) as impl_count
FROM nodes iface
LEFT JOIN edges e ON e.target = iface.id AND e.kind = 'implements'
WHERE iface.kind IN ('interface', 'trait')
GROUP BY iface.id HAVING impl_count = 1
ORDER BY iface.name;

-- FTS5 search (what codegraph_search uses internally)
SELECT n.name, n.kind, n.file_path, n.start_line
FROM nodes_fts fts
JOIN nodes n ON n.rowid = fts.rowid
WHERE nodes_fts MATCH '"<TERM>"*'
ORDER BY bm25(nodes_fts, 10.0, 5.0, 1.0, 2.0) LIMIT 20;
```
</instructions>

---

## Configuration

<instructions>
CodeGraph stores its configuration in `.codegraph/config.json`. Key options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `languages` | string[] | [] (auto-detect) | Restrict to specific languages |
| `exclude` | string[] | ["node_modules/**", "dist/**", ...] | Glob patterns to ignore |
| `frameworks` | string[] | [] | Framework hints for better resolution |
| `maxFileSize` | number | 1048576 (1MB) | Skip files larger than this |
| `extractDocstrings` | boolean | true | Extract docstrings from code |
| `trackCallSites` | boolean | true | Track call site locations |

For large projects, add slow-to-index directories to `exclude` to keep indexing fast.
</instructions>

---

<anti-patterns>
- Using Grep or glob to find symbol definitions, callers, or implementations when `.codegraph/` exists
- Spawning explore agents that scan files with grep/glob when `codegraph_explore` answers in one call
- Calling `codegraph_explore` or `codegraph_context` in the main session — these return large source code blocks that fill context; use them in explore agents or use the lightweight tools (search, callers, callees, impact, node) in the main session
- Using natural language sentences in `codegraph_explore` queries — use symbol names, file names, and short code terms discovered via `codegraph_search`
- Re-reading files that `codegraph_explore` already returned source code for — the returned sections are complete and authoritative
- Exceeding the explore call budget — stop and synthesize once you hit the limit
- Falling back to grep without first checking whether `.codegraph/` exists in the project
- Running `codegraph index --force` on every session — the MCP server auto-syncs on file changes; use `codegraph sync` for manual incremental updates
</anti-patterns>

---

<examples>

<example>
GOOD — Symbol discovery with codegraph_search:

Task: "Find the UserService class"

1. `codegraph_search` with query "UserService", kind "class"
2. Result: `UserService (class) at src/services/user-service.ts:15`
3. If source code needed: `codegraph_node` with symbol "UserService", includeCode true
</example>

<example>
BAD — Using grep when codegraph is available:

Task: "Find the UserService class"

1. `Grep` for "class UserService" across all files
2. Multiple results including comments, tests, and type references
3. Read each file to determine which is the actual definition

This wastes tool calls and context. Use `codegraph_search` instead.
</example>

<example>
GOOD — Exploration workflow (search then explore):

Task: "Understand how authentication works"

1. `codegraph_search` with query "auth" to discover symbol names
2. Results: `AuthService`, `authenticate`, `AuthMiddleware`, `auth-handler.ts`
3. Spawn explore agent with: "Use `codegraph_explore` with query 'AuthService authenticate AuthMiddleware auth-handler.ts'"
4. Agent gets full source code, relationship map, and connected symbols in 1-2 calls
</example>

<example>
GOOD — Impact analysis before editing:

Task: "Refactor the validateInput function"

1. `codegraph_impact` with symbol "validateInput", depth 2
2. Result shows 8 symbols across 4 files affected
3. `codegraph_callers` with symbol "validateInput" to see all call sites
4. Now you know every file that needs updating before you start editing
</example>

<example>
GOOD — Audit skill invoking codegraph for data gathering:

Task: "Audit this codebase for code quality"

1. Check `.codegraph/` exists; if not, run `codegraph init -i`
2. `codegraph_status` for overview metrics (files, nodes, edges by kind)
3. Run SQL queries against `.codegraph/codegraph.db` for structural analysis:
   - Node/edge distribution
   - Long functions (body > 40 lines)
   - High fan-in symbols (> 5 callers)
   - Orphan functions
   - Undocumented public symbols
4. `codegraph_callers` / `codegraph_callees` for call graph analysis on flagged symbols
5. `codegraph_impact` to determine blast radius of findings
</example>

<example>
GOOD — Correct fallback to grep (literal text search):

Task: "Find all TODO comments in the codebase"

CodeGraph indexes symbols, not arbitrary text. Use Grep:
1. `Grep` for "TODO" across all files

Similarly, use Grep for: string literals, error messages, configuration values, regex patterns, log statements.
</example>

</examples>

---

## Tips

- Use `codegraph_search` before `codegraph_explore` — discover symbol names first, then explore with those names
- Use `--json` with CLI commands when piping output to subsequent processing
- For large codebases, index once and rely on auto-sync (MCP server) or `codegraph sync` (CLI)
- Use `codegraph_node` with `includeCode: false` (the default) to get location and signature without consuming context on source code
- Combine `codegraph_impact` with `codegraph_callers` to estimate full blast radius before refactoring
- The `codegraph_files` tool with `format: "grouped"` gives a quick language breakdown of the project
- Use `codegraph affected` in CI to run only the tests impacted by your changes

---

## References

- [CodeGraph](https://github.com/colbymchenry/codegraph) — Source repository
- [tree-sitter](https://tree-sitter.github.io/) — Parser framework used for AST extraction
