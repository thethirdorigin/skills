---
name: react-best-practises
description: React and TypeScript conventions and best practices for architecture, state management, hooks, testing, error handling, security, and accessibility. Complements Vercel react-best-practices skill (which covers performance). Use when writing, reviewing, or refactoring React/TypeScript code.
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
---
  - React state management
---

# React and TypeScript Best Practices

<context>
You are a senior React/TypeScript engineer focused on writing maintainable, accessible, type-safe code. Before implementing, always discover the project's frontend structure, shared components, styling approach, and existing patterns. Match them — do not reinvent the wheel.

This skill covers architecture, correctness, and quality. For performance optimisation (waterfalls, bundle size, memoisation, re-renders), defer to the **Vercel react-best-practices** skill.

**Companion skill**: Vercel react-best-practices (69 performance rules). Install per-project: `npx skills add vercel-labs/agent-skills`
</context>

## 1. Architecture Discovery

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

## 2. Component Architecture

<instructions>
### Functional Components Only
- Use function declarations for components (not arrow function assignments)
- One page-level component per file
- Smaller helper components may coexist in the same file if they are not exported

### Composition Over Inheritance
- Compose with `children` and render props
- Use compound component pattern for related elements (e.g., Tabs + TabPanel + TabList)
- Extract shared logic into custom hooks, not Higher-Order Components

### File Organisation
- Match the existing project structure discovered in Phase 1
- Common patterns:
  - Pages: `pages/` or `app/` directory, one file per route
  - Components: `components/` directory, one directory per complex component
  - Hooks: `hooks/` directory for custom hooks
  - Utils: `utils/` or `lib/` for pure utility functions
  - Types: `types/` for shared TypeScript interfaces
  - Stores: `stores/` for state management stores

### Component Purity
- Components must be pure and idempotent: same inputs produce same outputs
- Side effects belong in `useEffect`, event handlers, or server actions — never in the render body
- Do not mutate props, state, or hook return values after receiving them
- Perform all mutations BEFORE creating JSX
</instructions>

<anti-patterns>
- Class components (use functional components with hooks)
- Calling component functions directly: `MyComponent()` — always use JSX `<MyComponent />`
- Deep prop drilling beyond 2 levels — use composition, context, or state management
- Inline styles — prefer CSS classes matching the project's styling approach
- Excessive `<div>` nesting — use fragments `<>...</>` and semantic HTML
- Defining components inside other components (causes remount on every render)
</anti-patterns>

## 3. Hooks Rules and Patterns

<instructions>
### Critical Rules (ESLint-enforced)
- Call hooks at the top level ONLY — never inside conditions, loops, or nested functions
- Call hooks ONLY from React function components or custom hooks — never from regular functions
- Call hooks before any early returns

### Hook-Specific Patterns
- **useState**: use callback for expensive initialisation: `useState(() => parseData(raw))`
- **useEffect**: always include a dependency array; always return cleanup for subscriptions/timers
- **useReducer**: switch from useState when a component has 4+ related state variables
- **useMemo/useCallback**: profile first — do not premature-optimise
- **Custom hooks**: prefix with `use`, extract when logic is reused 2+ times

### Dependency Arrays
- Include ALL reactive values used inside the hook
- Enable `eslint-plugin-react-hooks` exhaustive-deps rule
- If a dependency changes too often, refactor the code — do not lie about dependencies
</instructions>

<anti-patterns>
- Hooks inside conditions or loops
- useEffect for derived state — calculate inline or use useMemo instead
- Missing dependencies in useEffect/useMemo/useCallback arrays
- useEffect on every render (missing dependency array)
- useEffect as an event handler — put interaction logic in event handlers directly
</anti-patterns>

## 4. State Management

<instructions>
### Local State
- `useState` for simple UI state: toggles, search text, filter values, pagination
- `useReducer` for complex state with multiple interdependent fields
- Derive data inline: compute `filteredRows` -> `sortedRows` -> `paginatedRows` rather than storing derived state

### Global State
- Identify the existing store pattern in the project (Zustand, Redux, Context, etc.)
- Keep stores small and focused: one per domain concern
- Use selectors to prevent unnecessary re-renders
- Do not lift every piece of state to global — keep state as close to usage as possible

### Server State
- Use the project's data fetching library (React Query, SWR, etc.) for all API data
- Separate queries from mutations
- Configure `staleTime` and `cacheTime` appropriately
- Use consistent query key patterns matching existing code

### Immutability — Critical
- NEVER mutate state directly
- Objects: use spread operator `{...state, field: newValue}` or `structuredClone`
- Arrays: use `.map()`, `.filter()`, `.concat()`, spread — NEVER `.push()`, `.splice()`, or index assignment
- Values used in props, state, hooks, or JSX become immutable after creation
</instructions>

<anti-patterns>
- Storing derived data in state (calculate it instead)
- Lifting every piece of state to global scope
- Direct state mutation: `state.items.push(newItem)`
- Using array indices as state keys
- Context API for frequently-updating values (causes full subtree re-renders)
</anti-patterns>

## 5. TypeScript Patterns

<instructions>
- Type ALL component props with `interface` (not type alias for component props)
- Never use `any` — use `unknown` and narrow, or use specific types
- Use discriminated unions for state machines and loading/error/success patterns:
  ```
  type State =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'error'; error: Error }
    | { status: 'success'; data: T }
  ```
- Export types alongside components when consumers need them
- Use the `satisfies` operator for type-safe object literals
- Use generics for reusable utilities, hooks, and components
- Prefer `interface` for object shapes (extendable) and `type` for unions/intersections
</instructions>

<anti-patterns>
- `any` type anywhere — always use proper typing
- Non-null assertions (`!`) without clear justification
- Type casting (`as`) to silence errors — fix the underlying type issue
- Untyped event handlers: use `React.MouseEvent<HTMLButtonElement>` etc.
</anti-patterns>

## 6. Shared Component and Styling Discovery

<instructions>
### Component Reuse
- ALWAYS search for existing shared/common components before building custom
- Check the UI component library first (discovered in Phase 1)
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

## 7. Error Handling

<instructions>
### Three-Layer Approach
1. **Error Boundaries**: at route or section level, catch rendering errors, show fallback UI
2. **try-catch**: in async event handlers and data fetching, with user-facing messages
3. **Toast/notification system**: for transient errors (identify the project's toast library)

### Patterns
- Search for existing ErrorBoundary components before creating new ones
- Never swallow errors silently — always log or display
- Handle loading, error, and success states for all async operations
- Use inline error states for form validation
- Log errors to console in development, to a logging service in production
</instructions>

<anti-patterns>
- Missing error handling for async operations
- Showing raw error messages to users
- Error boundaries around individual components (too granular)
- Silently catching and ignoring errors
</anti-patterns>

## 8. Security

<instructions>
- NEVER use `dangerouslySetInnerHTML` without sanitising with a library like DOMPurify
- Never trust user input — validate on both client and server
- Use HttpOnly cookies for auth tokens, not localStorage
- Sanitise URL parameters before using in queries or rendering
- No secrets, API keys, or tokens in client-side code
- Keep dependencies updated to patch known vulnerabilities
</instructions>

## 9. Testing

<instructions>
### Approach
- Use the project's existing test runner and testing library
- Common stack: Vitest/Jest + React Testing Library
- Test **behaviour**, not implementation details
- Test error states and edge cases, not just the happy path

### What to Test
- Custom hooks: test inputs and outputs
- Components: test user interactions and rendered output
- Utilities: pure function input/output
- Integration: test page-level flows with mocked API calls

### Test Selectors
- Prefer accessible selectors: `getByRole`, `getByLabelText`, `getByText`
- Use `data-testid` only when semantic selectors are not available
- Mock API calls, not internal functions
</instructions>

<anti-patterns>
- Testing implementation details (state values, internal methods)
- Snapshot tests as the sole test strategy
- Testing library internals (React Query cache, router state)
- Skipping error state tests
</anti-patterns>

## 10. Code Quality and Naming

<instructions>
### Naming Conventions
- **Components**: PascalCase — `CreditFacilityCard`, `StatusBadge`
- **Variables, functions**: camelCase — `getCreditFacilities`, `totalAmount`
- **Constants**: SCREAMING_SNAKE_CASE — `PAGE_SIZE_OPTIONS`, `DEFAULT_SORT`
- **Files**: PascalCase for components (`StatCard.tsx`), camelCase for utilities (`formatCurrency.ts`)
- **Boolean props**: prefix with `is`, `has`, `should`, `can` — `isLoading`, `hasError`, `shouldRender`
- **Event handlers**: prefix with `handle` — `handleSubmit`, `handleFilterChange`
- **Callback props**: prefix with `on` — `onSubmit`, `onChange`, `onFilterChange`

### Import Organisation
- React imports first
- External library imports second
- Internal/project imports third (aliases like `@/` or package names)
- Relative imports last
- Group with blank lines between sections

### JSX Practices
- Self-close components with no children: `<Component />`
- Boolean props shorthand: `<Component flag />` not `flag={true}`
- String props without braces: `variant="primary"` not `variant={"primary"}`
- Use fragments `<>...</>` instead of unnecessary wrapper `<div>`s
</instructions>

## 11. List Rendering

<instructions>
- Always provide unique, stable keys — use entity IDs from your data
- NEVER use array indices as keys — this causes state bugs when items are reordered or filtered
- Extract list items into separate components for readability
- For large lists, consider virtualisation (identified in Phase 1 or via the Vercel performance skill)
</instructions>

## 12. Accessibility

<instructions>
- Use semantic HTML elements: `<button>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<header>`, `<footer>`
- Provide `aria-label` for icon-only buttons and non-text interactive elements
- Ensure keyboard navigation works for all interactive elements
- Use `role` attributes only when semantic elements are not appropriate
- Colour contrast: meet WCAG 2.1 AA minimum (4.5:1 for normal text, 3:1 for large text)
- Form labels: every input has an associated `<label>` or `aria-label`
- Focus management: visible focus indicators, logical tab order
</instructions>

## 13. Comprehensive Anti-Patterns

<anti-patterns>
### Architecture
- Mixing render logic with side effects
- God components with 500+ lines — split into smaller focused components
- Business logic in components — extract to hooks or utility functions
- Tight coupling between components via shared mutable state

### State
- Storing derived data in state
- Prop drilling beyond 2 levels
- Over-using Context for frequently-updating values
- Direct state mutation

### Performance (defer to Vercel skill for details)
- Sequential awaits when parallel is possible
- Creating new objects/functions on every render without memoisation (when profiling shows impact)
- Missing keys or index-based keys in lists

### TypeScript
- Using `any` type
- Type assertions (`as`) to silence errors
- Not typing event handlers
- Inconsistent interface naming

### Testing
- Testing implementation details
- No error state coverage
- Snapshot-only testing
- Skipping accessibility tests
</anti-patterns>

## References

- [React Rules](https://react.dev/reference/rules) — Official React rules covering component purity, hooks rules, and immutability requirements
- [freeCodeCamp React Best Practices](https://www.freecodecamp.org/news/best-practices-for-react/) — Comprehensive guide covering component patterns, state management, naming, testing, and error handling
- [Vercel React Best Practices](https://vercel.com/blog/introducing-react-best-practices) — Performance-focused 69-rule guide (covered by the Vercel react-best-practices skill)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) — Installable skill pack including composition patterns, web design guidelines, and React Native skills
