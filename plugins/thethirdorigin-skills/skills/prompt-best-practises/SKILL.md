---
name: prompt-best-practises
description: Guidelines for writing effective prompts and Claude Code skills. Use when creating, improving, or reviewing skills and prompt templates. Covers XML structuring, few-shot examples, role assignment, output control, and agentic patterns.
triggers:
  - creating a new skill
  - writing a skill
  - improving a skill
  - prompt engineering
  - structuring instructions for Claude
  - skill authoring
  - building a prompt template
---

# Prompt Best Practices for Skill Authoring

This skill guides the creation and refinement of Claude Code skills and prompt templates. Apply these principles to produce skills that are clear, consistent, and effective.

## 1. Clarity and Directness

<instructions>
- Lead with the task or instruction, not background context
- Use imperative verbs: "Use", "Prefer", "Always", "Never", "Check", "Identify"
- One instruction per bullet — do not combine multiple directives
- Be explicit about desired behaviour rather than relying on inference
- Apply the "colleague test": if a colleague with minimal context would be confused by your prompt, Claude will be too
- Use sequential numbered lists when order matters; use bullets when it does not
</instructions>

<anti-patterns>
- Vague instructions: "Handle errors properly" (instead: "Return Result<T, E> for all fallible operations and propagate errors with the ? operator")
- Assuming context: "Fix the bug" without specifying which bug, where, or how to identify it
- Combining directives: "Use TypeScript and make sure to add tests and also update the docs"
</anti-patterns>

## 2. Structured Formatting with XML Tags

<instructions>
- Use consistent, descriptive tag names throughout a skill:
  - `<instructions>` — primary directives and rules
  - `<context>` — background information, project setup, tech stack
  - `<examples>` — input/output demonstrations (wrap individual items in `<example>`)
  - `<anti-patterns>` — what NOT to do, common mistakes
  - `<constraints>` — hard boundaries and limitations
- Nest tags when content has natural hierarchy
- XML tags eliminate ambiguity — Claude knows exactly where instructions start and end
- Place long reference documents inside their own tags at the TOP of the skill, above instructions
</instructions>

<examples>
<example>
Good — Clear tag separation:
```
<context>
  Stack: React 19 + TypeScript + Vite
</context>

<instructions>
  - Use functional components exclusively
  - Type all props with interfaces
</instructions>

<anti-patterns>
  - Class components
  - Using `any` type
</anti-patterns>
```
</example>

<example>
Bad — Mixed concerns without tags:
```
We use React 19 with TypeScript. Use functional components.
Don't use class components. Type all props. Don't use any.
```
</example>
</examples>

## 3. Role Assignment

<instructions>
- Set a role in the opening context to focus behaviour and tone
- Even a single sentence makes a measurable difference
- Match the role to the skill's domain
- Roles establish expertise level, communication style, and decision-making framework
</instructions>

<examples>
<example>
"You are a senior Rust engineer specialising in async systems and hexagonal architecture."
</example>
<example>
"You are a React accessibility expert reviewing components for WCAG 2.1 AA compliance."
</example>
</examples>

## 4. Few-Shot Examples

<instructions>
- Include 3-5 examples for best results
- Make examples:
  - **Relevant**: mirror actual use cases from the target codebase
  - **Diverse**: cover edge cases, not just the happy path
  - **Structured**: consistent format across all examples
- Label examples as GOOD or BAD explicitly
- Wrap examples in `<examples>` with individual `<example>` tags
- Ask Claude to evaluate your examples for relevance and diversity, or to generate additional ones
</instructions>

<anti-patterns>
- Only showing the happy path (include error cases, edge cases, empty states)
- Examples that are too similar to each other
- Examples without labels — Claude cannot distinguish good from bad
</anti-patterns>

## 5. Output Format Control

<instructions>
- Tell Claude what TO do, not what NOT to do (positive framing)
  - Instead of "Do not use markdown": "Write your response as smoothly flowing prose paragraphs"
  - Instead of "Don't add comments": "Write self-documenting code with descriptive names"
- Specify the exact format you want: code blocks, lists, tables, prose
- Use XML format indicators when needed: "Write analysis in `<analysis>` tags"
- Match your prompt style to your desired output — if your prompt uses less markdown, the output will too
- For structured output, describe the schema explicitly
</instructions>

## 6. Long Context Placement

<instructions>
- Place longform data and reference documents at the TOP of the prompt, above queries and instructions
- This positioning can improve performance by up to 30%
- Wrap documents in `<document>` tags with metadata subtags
- For grounded responses: ask Claude to quote relevant parts of the document before performing the task
- Structure: Reference Material → Context → Instructions → Examples → Query
</instructions>

## 7. Thinking and Reasoning

<instructions>
- For complex multi-step tasks, guide Claude to reason before acting:
  - "Before implementing, analyse the existing patterns in this module"
  - "Think through the trade-offs, then recommend one approach"
- Use targeted thinking guidance, not blanket defaults:
  - Instead of "Always think step by step": "When deciding between approaches, evaluate trade-offs before committing"
- For constrained reasoning: "Pick one approach and commit. Avoid revisiting decisions. Course-correct only if new information contradicts your reasoning."
- After tool results, prompt reflection: "Carefully evaluate the results and determine optimal next steps before proceeding"
</instructions>

<anti-patterns>
- Over-prompting thinking: "If in doubt, always use extended thinking" (creates unnecessary latency)
- Prescriptive step-by-step plans when the task structure is uncertain (prefer general instructions)
</anti-patterns>

## 8. Agentic Patterns for Skills

<instructions>
### Incremental Progress
- Break work into small, verifiable steps
- Track what is done and what is pending
- Commit progress frequently rather than batching

### State Management
- Use structured formats (JSON, tables) for tracking data like test results or checklists
- Use freeform text for progress notes and reasoning
- Use git for checkpointing across sessions

### Safety and Autonomy Balance
- Take local, reversible actions freely (editing files, running tests)
- For hard-to-reverse actions (deleting, force-pushing, posting publicly), ask the user first
- Provide guidance: "Consider reversibility and potential impact before acting"

### Tool Usage
- Be explicit about which tools to use: "Use the Read tool to inspect the file first"
- Encourage parallel tool calls when no dependencies exist: "Make all independent calls in parallel"
- Control trigger intensity: use "Use this tool when..." not "CRITICAL: You MUST use this tool"
- If a skill should be proactive, state so: "By default, implement changes rather than only suggesting them"

### Avoiding Over-Engineering
- "Only make directly requested or clearly necessary changes"
- "Keep solutions simple and focused"
- "Do not add features beyond what is asked"
- "Do not create helpers for one-time operations"
- "Do not design for hypothetical future requirements"
</instructions>

## 9. Anti-Patterns in Skill Authoring

<anti-patterns>
- **Over-engineering instructions**: Adding so many constraints that Claude cannot satisfy them all
- **Contradictory constraints**: "Be concise" AND "Include comprehensive examples for every rule"
- **Negative framing throughout**: A skill full of "don't do X" — reframe as "do Y instead"
- **Missing context**: Instructions that assume knowledge of a specific project without discovery steps
- **Hardcoded paths**: Referencing specific file paths instead of discovery prompts like "find the shared component directory"
- **Aggressive trigger language**: "CRITICAL: You MUST always..." — use measured guidance instead
- **No examples**: Rules without concrete good/bad demonstrations
- **Stale references**: Linking to patterns that may have changed — prefer dynamic discovery
</anti-patterns>

## 10. Skill Composition

<instructions>

### How skills load sub-skills

Skills are NOT automatically in context when another skill references them.
Claude must explicitly invoke the Skill tool to load each dependency. Two
mechanisms ensure this happens:

1. **Hooks** — The `skill-activation.py` hook reads `dependencies` from each
   SKILL.md frontmatter, resolves the full chain transitively, and injects
   Skill tool invocation instructions into Claude's context before the skill
   even starts.
2. **In-skill instructions** — Each parent skill should have a "Step 0" or
   "Phase 0" that explicitly tells Claude to invoke the Skill tool for its
   dependencies. This is the safety net in case hooks are not installed.

Both mechanisms are needed. The hook fires first (belt), the in-skill
instruction reinforces (suspenders).

### Declaring dependencies

Add `dependencies` to the YAML frontmatter — list the skill names this skill
needs loaded before it can execute:

```yaml
dependencies:
  - codegraph
```

Dependencies are resolved transitively. If `reviewpr` depends on `audit` and
`audit` depends on `codegraph`, loading `reviewpr` will resolve all three in
the right order: codegraph → audit → reviewpr.

### Writing Step 0

If your skill depends on other skills, add a Step 0 section immediately after
the `<context>` block:

```markdown
## Step 0 — Load required sub-skills

<instructions>
Before proceeding to Step 1, invoke the Skill tool for each dependency:

1. **REQUIRED**: Invoke the Skill tool with `skill="codegraph"`
2. **If Cargo.toml detected**: Invoke the Skill tool with `skill="rust-best-practises"`

Do not proceed to Step 1 until dependencies are loaded.
</instructions>
```

Key rules:
- Place Step 0 before any other steps — it must execute first
- Use the exact phrase `Invoke the Skill tool with skill="<name>"`
- State which dependencies are always required vs conditional on stack detection
- Include a gate: "Do not proceed until X is loaded"
- Do NOT say "loaded automatically by the plugin" — this is false and causes
  Claude to skip the loading step

### Declaring file patterns

Add `file-patterns` to the YAML frontmatter for skills that should be
suggested when specific files are edited:

```yaml
file-patterns:
  - .tsx              # extension match (file must end with this)
  - frontend/         # directory match (file path must contain this)
  - Cargo.toml        # exact filename match
```

The `file-tracker.py` hook matches edited file paths against these patterns
and suggests the relevant skills. No config files to maintain.

</instructions>

## 11. Skill File Template

Use this template when creating a new skill:

```markdown
---
name: skill-name
description: One-line description of what the skill does and when to use it
triggers:
  - natural language trigger phrase 1
  - natural language trigger phrase 2
  - natural language trigger phrase 3
dependencies:                          # optional — skills to load first
  - codegraph
file-patterns:                         # optional — file edits that suggest this skill
  - .tsx
  - frontend/
---

# Skill Name

<context>
  Brief description of the domain, tech stack, or role this skill serves.
  All context is discovered dynamically — no hardcoded project paths.
</context>

## Step 0 — Load required sub-skills (if dependencies exist)

<instructions>
Before proceeding, invoke the Skill tool for each dependency:
1. **REQUIRED**: Invoke the Skill tool with `skill="codegraph"`
Do not proceed until dependencies are loaded.
</instructions>

## Step 1: Discovery
<instructions>
  Steps to understand the current project state before acting.
</instructions>

## Step 2: Rules and Guidelines
<instructions>
  Primary directives — what TO do.
</instructions>

<anti-patterns>
  What NOT to do, with explanations of why.
</anti-patterns>

## Step 3: Examples
<examples>
<example>
  GOOD: [concrete demonstration]
</example>
<example>
  BAD: [concrete counter-example]
</example>
</examples>

## References
- [Source Name](URL) — brief description of what it covers
```

### Skill Quality Checklist

Before finalising a skill, verify:

- [ ] Frontmatter has `name`, `description`, and `triggers`
- [ ] `name` matches the directory name
- [ ] Description is specific enough for trigger matching
- [ ] Triggers use natural language phrases users would actually say
- [ ] `dependencies` lists any skills that must be loaded first
- [ ] `file-patterns` lists file extensions or directories that suggest this skill
- [ ] If dependencies exist, a Step 0 with explicit Skill tool invocations is present
- [ ] Step 0 does NOT say "loaded automatically" — uses `Invoke the Skill tool with skill="..."`
- [ ] Instructions use positive framing (what TO do)
- [ ] Anti-patterns section exists with explanations
- [ ] At least 2-3 examples with GOOD/BAD labels
- [ ] No hardcoded project-specific paths (uses discovery prompts)
- [ ] XML tags are properly opened and closed
- [ ] Long reference material placed at the TOP
- [ ] References section at the end with source URLs

## References

- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — Official Anthropic guide covering clarity, XML tags, examples, thinking, agentic patterns, output control, and tool use
