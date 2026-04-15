---
name: react-best-practises
description: >
  React and TypeScript conventions and best practices with 78 rules across 11 categories.
  Use when writing, reviewing, or refactoring React/TypeScript code. Covers hooks,
  state management, component architecture, TypeScript patterns, error handling,
  security, testing, accessibility, and common anti-patterns.
triggers:
  - writing React code
  - working on frontend
  - creating a component
  - React review
  - frontend development
  - TypeScript patterns
  - adding a page
  - form implementation
  - React testing
  - React state management
file-patterns:
  - .tsx
  - .jsx
  - frontend/
---

# React and TypeScript Best Practices

<context>
You are a senior React/TypeScript engineer focused on writing maintainable, accessible, type-safe code. Before implementing, always discover the project's frontend structure, shared components, styling approach, and existing patterns. Match them — do not reinvent the wheel.

This skill covers architecture, correctness, and quality. For performance optimisation (waterfalls, bundle size, memoisation, re-renders), defer to the **Vercel react-best-practices** skill.

**Companion skill**: Vercel react-best-practices (69 performance rules). Install per-project: `npx skills add vercel-labs/agent-skills`
</context>

## When to Apply

Reference these guidelines when:
- Writing new React components, hooks, or pages
- Implementing forms, lists, or async data flows
- Reviewing code for correctness, accessibility, or type safety
- Refactoring existing frontend code
- Setting up state management or error handling

## Architecture Discovery

<instructions>
Before writing any React code, perform these discovery steps:

- Identify the frontend structure: monorepo (workspaces, packages, apps) or single app
- Find shared/common directories: components, hooks, utils, lib, helpers, shared, common
- Identify the UI component library in use (MUI, Radix, Chakra, Ant, custom, etc.) — always check it before building custom components
- Find theme/style configuration files: CSS variables, Tailwind config, design tokens, styled-components theme
- Identify the routing library (React Router, Next.js App Router, TanStack Router)
- Identify the state management approach: Zustand, Redux, Context API, Jotai, Recoil
- Identify the data fetching library: React Query, SWR, RTK Query, or custom
- Identify the form library: React Hook Form, Formik, or custom
- Check for existing icon library (Lucide, Heroicons, FontAwesome)
- Read any frontend guide, README, or ARCHITECTURE files in the frontend directory
- Check the existing test setup: test runner, testing library, test file locations
</instructions>

## Shared Component and Styling Discovery

<instructions>
### Component Reuse
- ALWAYS search for existing shared/common components before building custom
- Check the UI component library first (discovered above)
- Check the shared component directory for project-specific components
- If a component exists but needs modification, extend it — do not duplicate

### Styling Consistency
- Identify the styling approach: Tailwind, CSS Modules, styled-components, CSS-in-JS, plain CSS
- Match it exactly — do not introduce a different approach
- Find and reuse existing:
  - Colour tokens / CSS variables / design tokens
  - Spacing scales and breakpoints
  - Typography styles and font configuration
  - Border radius, shadow, and other design system values
- Use semantic colour tokens (e.g., `--color-error`) over raw hex values
- Follow existing responsive breakpoint patterns (mobile-first or desktop-first)
- Use existing icon library — do not mix icon sets

### Forms
- Identify the form library in use (React Hook Form, Formik, etc.)
- Use the UI library's form field components if available
- Follow existing validation patterns
</instructions>

---

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Hooks Rules and Patterns | CRITICAL | `hook-` | 10 |
| 2 | State Management | CRITICAL | `state-` | 10 |
| 3 | Component Architecture | HIGH | `comp-` | 10 |
| 4 | TypeScript Patterns | HIGH | `ts-` | 7 |
| 5 | Error Handling | HIGH | `err-` | 6 |
| 6 | Security | HIGH | `sec-` | 6 |
| 7 | Testing | MEDIUM | `test-` | 7 |
| 8 | Code Quality and Naming | MEDIUM | `name-` | 7 |
| 9 | List Rendering | MEDIUM | `list-` | 3 |
| 10 | Accessibility | MEDIUM | `a11y-` | 7 |
| 11 | Anti-patterns | REFERENCE | `anti-` | 5 |

---

## Quick Reference

### 1. Hooks Rules and Patterns (CRITICAL)

- [`hook-top-level`](rules/hook-top-level.md) - Call hooks at the top level only — never inside conditions or loops
- [`hook-component-only`](rules/hook-component-only.md) - Call hooks only from React components or custom hooks
- [`hook-before-returns`](rules/hook-before-returns.md) - Call all hooks before any early return statements
- [`hook-useState-callback`](rules/hook-useState-callback.md) - Use callback initialiser for expensive useState computations
- [`hook-useEffect-cleanup`](rules/hook-useEffect-cleanup.md) - Return cleanup functions from useEffect for subscriptions and timers
- [`hook-useEffect-deps`](rules/hook-useEffect-deps.md) - Always include a dependency array in useEffect
- [`hook-useReducer-complex`](rules/hook-useReducer-complex.md) - Switch to useReducer when 4+ related state variables
- [`hook-memo-profile-first`](rules/hook-memo-profile-first.md) - Profile before applying useMemo or useCallback
- [`hook-custom-prefix`](rules/hook-custom-prefix.md) - Prefix custom hooks with `use`, extract when reused in 2+ components
- [`hook-exhaustive-deps`](rules/hook-exhaustive-deps.md) - Include all reactive values in dependency arrays

### 2. State Management (CRITICAL)

- [`state-local-simple`](rules/state-local-simple.md) - Use useState for simple, isolated UI state
- [`state-reducer-complex`](rules/state-reducer-complex.md) - Use useReducer for complex interdependent state
- [`state-derive-inline`](rules/state-derive-inline.md) - Compute derived values inline instead of storing in state
- [`state-match-existing`](rules/state-match-existing.md) - Use the project's existing state management library
- [`state-small-stores`](rules/state-small-stores.md) - Keep stores small and focused — one per domain concern
- [`state-selectors`](rules/state-selectors.md) - Use selectors to subscribe to only needed state slices
- [`state-close-to-usage`](rules/state-close-to-usage.md) - Keep state as close to its usage as possible
- [`state-query-library`](rules/state-query-library.md) - Use the project's data fetching library for server state
- [`state-never-mutate`](rules/state-never-mutate.md) - Never mutate state objects or arrays directly
- [`state-immutable-updates`](rules/state-immutable-updates.md) - Use spread, map, filter for immutable state updates

### 3. Component Architecture (HIGH)

- [`comp-functional-only`](rules/comp-functional-only.md) - Use function declarations for components
- [`comp-one-per-file`](rules/comp-one-per-file.md) - One page-level component per file
- [`comp-composition`](rules/comp-composition.md) - Compose with children and render props
- [`comp-compound-pattern`](rules/comp-compound-pattern.md) - Use compound component pattern for related elements
- [`comp-custom-hooks`](rules/comp-custom-hooks.md) - Extract shared logic into custom hooks, not HOCs
- [`comp-match-structure`](rules/comp-match-structure.md) - Follow the existing project file structure
- [`comp-pure-render`](rules/comp-pure-render.md) - Keep components pure — same props, same output
- [`comp-side-effects`](rules/comp-side-effects.md) - Side effects in useEffect or event handlers, never in render
- [`comp-no-inline-styles`](rules/comp-no-inline-styles.md) - Use CSS classes matching the project's styling approach
- [`comp-jsx-fragments`](rules/comp-jsx-fragments.md) - Use fragments and semantic HTML, avoid unnecessary divs

### 4. TypeScript Patterns (HIGH)

- [`ts-interface-props`](rules/ts-interface-props.md) - Type all component props with an interface
- [`ts-no-any`](rules/ts-no-any.md) - Use `unknown` and narrow instead of `any`
- [`ts-discriminated-unions`](rules/ts-discriminated-unions.md) - Use discriminated unions for state machines
- [`ts-export-types`](rules/ts-export-types.md) - Export types alongside components when consumers need them
- [`ts-satisfies`](rules/ts-satisfies.md) - Use `satisfies` for type-safe object literals
- [`ts-generics`](rules/ts-generics.md) - Use generics for reusable hooks, utilities, and components
- [`ts-interface-vs-type`](rules/ts-interface-vs-type.md) - Prefer `interface` for objects, `type` for unions

### 5. Error Handling (HIGH)

- [`err-error-boundary`](rules/err-error-boundary.md) - Place Error Boundaries at route or section level
- [`err-try-catch-async`](rules/err-try-catch-async.md) - Wrap async operations in try-catch with user-facing messages
- [`err-toast-transient`](rules/err-toast-transient.md) - Use toast/notification system for transient errors
- [`err-reuse-boundary`](rules/err-reuse-boundary.md) - Search for existing ErrorBoundary before creating new ones
- [`err-never-swallow`](rules/err-never-swallow.md) - Always log or display errors — never catch and ignore
- [`err-handle-all-states`](rules/err-handle-all-states.md) - Handle loading, error, and success states for async operations

### 6. Security (HIGH)

- [`sec-no-inner-html`](rules/sec-no-inner-html.md) - Sanitise content before using `dangerouslySetInnerHTML`
- [`sec-validate-input`](rules/sec-validate-input.md) - Validate user input on both client and server
- [`sec-httponly-cookies`](rules/sec-httponly-cookies.md) - Use HttpOnly cookies for auth tokens, not localStorage
- [`sec-sanitise-urls`](rules/sec-sanitise-urls.md) - Sanitise URL parameters before rendering
- [`sec-no-client-secrets`](rules/sec-no-client-secrets.md) - Keep secrets and API keys out of client-side code
- [`sec-update-deps`](rules/sec-update-deps.md) - Keep dependencies updated to patch vulnerabilities

### 7. Testing (MEDIUM)

- [`test-existing-setup`](rules/test-existing-setup.md) - Use the project's existing test runner and testing library
- [`test-behaviour`](rules/test-behaviour.md) - Test user-visible behaviour, not implementation details
- [`test-error-edge`](rules/test-error-edge.md) - Test error states and edge cases, not just the happy path
- [`test-custom-hooks`](rules/test-custom-hooks.md) - Test custom hooks with renderHook
- [`test-accessible-selectors`](rules/test-accessible-selectors.md) - Prefer accessible selectors: getByRole, getByLabelText, getByText
- [`test-data-testid-last`](rules/test-data-testid-last.md) - Use data-testid only when semantic selectors are unavailable
- [`test-mock-api`](rules/test-mock-api.md) - Mock API calls at the network level, not internal functions

### 8. Code Quality and Naming (MEDIUM)

- [`name-component-pascal`](rules/name-component-pascal.md) - PascalCase for component names
- [`name-variable-camel`](rules/name-variable-camel.md) - camelCase for variables and functions
- [`name-constant-screaming`](rules/name-constant-screaming.md) - SCREAMING_SNAKE_CASE for constants
- [`name-file-convention`](rules/name-file-convention.md) - PascalCase for component files, camelCase for utilities
- [`name-boolean-prefix`](rules/name-boolean-prefix.md) - Prefix boolean props with `is`, `has`, `should`, `can`
- [`name-handler-prefix`](rules/name-handler-prefix.md) - Prefix handlers with `handle`, callbacks with `on`
- [`name-import-order`](rules/name-import-order.md) - Organize imports in consistent groups

### 9. List Rendering (MEDIUM)

- [`list-stable-keys`](rules/list-stable-keys.md) - Provide unique, stable keys from entity IDs
- [`list-no-index-keys`](rules/list-no-index-keys.md) - Never use array indices as keys for dynamic lists
- [`list-extract-items`](rules/list-extract-items.md) - Extract list items into separate components

### 10. Accessibility (MEDIUM)

- [`a11y-semantic-html`](rules/a11y-semantic-html.md) - Use semantic HTML elements for their intended purpose
- [`a11y-aria-labels`](rules/a11y-aria-labels.md) - Provide aria-label for icon-only buttons
- [`a11y-keyboard-nav`](rules/a11y-keyboard-nav.md) - Ensure keyboard navigation for all interactive elements
- [`a11y-role-sparingly`](rules/a11y-role-sparingly.md) - Use role only when semantic elements are not appropriate
- [`a11y-color-contrast`](rules/a11y-color-contrast.md) - Meet WCAG 2.1 AA contrast ratios
- [`a11y-form-labels`](rules/a11y-form-labels.md) - Associate every input with a label or aria-label
- [`a11y-focus-management`](rules/a11y-focus-management.md) - Maintain visible focus indicators and logical tab order

### 11. Anti-patterns (REFERENCE)

- [`anti-god-component`](rules/anti-god-component.md) - Split components over 300-500 lines into focused pieces
- [`anti-business-in-component`](rules/anti-business-in-component.md) - Extract business logic to hooks or utilities
- [`anti-tight-coupling`](rules/anti-tight-coupling.md) - Avoid coupling components via shared mutable state
- [`anti-snapshot-only`](rules/anti-snapshot-only.md) - Avoid snapshot-only testing strategy
- [`anti-define-inside`](rules/anti-define-inside.md) - Never define components inside other components

---

## How to Use

Reference these guidelines by task type:

| Task | Primary Categories |
|------|-------------------|
| New component | `comp-`, `ts-`, `name-` |
| New hook | `hook-`, `state-` |
| Form implementation | `hook-`, `state-`, `ts-`, `a11y-` |
| List/table rendering | `list-`, `comp-`, `a11y-` |
| Async data flow | `state-`, `err-`, `hook-` |
| Error handling | `err-`, `comp-` |
| Code review | `anti-`, `hook-`, `a11y-` |
| Testing | `test-` |
| Security review | `sec-` |

### Rule Application

1. **Check relevant category** based on task type
2. **Apply rules** with matching prefix
3. **Prioritise** CRITICAL > HIGH > MEDIUM > REFERENCE
4. **Read rule files** in `rules/` for detailed examples

---

## References

- [React Rules](https://react.dev/reference/rules) — Official React rules covering component purity, hooks rules, and immutability requirements
- [freeCodeCamp React Best Practices](https://www.freecodecamp.org/news/best-practices-for-react/) — Comprehensive guide covering component patterns, state management, naming, testing, and error handling
- [Vercel React Best Practices](https://vercel.com/blog/introducing-react-best-practices) — Performance-focused 69-rule guide (covered by the Vercel react-best-practices skill)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) — Installable skill pack including composition patterns, web design guidelines, and React Native skills
