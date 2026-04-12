# hook-useState-callback

> Use callback initialiser for expensive useState computations

## Why It Matters

When you pass a value directly to `useState`, that expression evaluates on every render — even though React only uses the result on the initial mount. For cheap computations this is harmless, but for expensive operations like parsing, sorting large arrays, or reading from storage, the wasted work adds up across renders.

The callback form `useState(() => expensiveComputation())` runs the function only once during the initial render. Subsequent renders skip the initialiser entirely, eliminating unnecessary computation without any added complexity.

## Bad

```tsx
interface DataViewerProps {
  rawCsv: string;
}

function DataViewer({ rawCsv }: DataViewerProps) {
  // parseCSV executes on EVERY render, result discarded after mount
  const [rows, setRows] = useState(parseCSV(rawCsv));
  const [sortColumn, setSortColumn] = useState("date");

  return <Table rows={rows} sortBy={sortColumn} onSort={setSortColumn} />;
}
```

## Good

```tsx
interface DataViewerProps {
  rawCsv: string;
}

function DataViewer({ rawCsv }: DataViewerProps) {
  // parseCSV runs only on the initial mount
  const [rows, setRows] = useState(() => parseCSV(rawCsv));
  const [sortColumn, setSortColumn] = useState("date");

  return <Table rows={rows} sortBy={sortColumn} onSort={setSortColumn} />;
}
```

## See Also

- [hook-memo-profile-first](hook-memo-profile-first.md) - Profile before applying memoisation
