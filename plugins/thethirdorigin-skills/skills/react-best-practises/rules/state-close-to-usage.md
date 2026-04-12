# state-close-to-usage

> Keep state as close to its usage as possible

## Why It Matters

State that is lifted higher than necessary creates invisible dependencies. A search input's text stored in a global store means every keystroke triggers store updates and potentially re-renders components across the application that subscribe to that store. It also makes the component harder to reuse — it now depends on an external store that must exist in the environment.

Start with state in the component that owns it. Lift only when a sibling or parent genuinely needs the value. This principle — colocation — keeps components self-contained, easy to test in isolation, and simple to delete or move.

## Bad

```tsx
// Global store holds state only one component uses
const useSearchStore = create<{ query: string; setQuery: (q: string) => void }>(
  (set) => ({
    query: "",
    setQuery: (query) => set({ query }),
  })
);

// SearchInput.tsx
function SearchInput() {
  const { query, setQuery } = useSearchStore();
  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}

// No other component reads `query` — global store is unnecessary overhead
```

## Good

```tsx
// State lives in the component that owns the search input
function SearchPanel() {
  const [query, setQuery] = useState("");
  const results = useSearchResults(query);

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <SearchResults items={results} />
    </div>
  );
}

// If a sibling later needs `query`, lift to the nearest common parent — not global
function PageWithSearch() {
  const [query, setQuery] = useState("");

  return (
    <>
      <SearchInput value={query} onChange={setQuery} />
      <SearchSuggestions query={query} />
    </>
  );
}
```

## See Also

- [state-local-simple](state-local-simple.md) - Use useState for simple isolated UI state
