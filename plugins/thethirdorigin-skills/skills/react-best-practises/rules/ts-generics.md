# ts-generics

> Use generics for reusable hooks, utilities, and components

## Why It Matters

Without generics, you end up duplicating logic for each data type. A `useUserList` hook and a `useProductList` hook might have identical fetching, pagination, and caching logic but differ only in the type of items returned. Generics let you write the logic once and parameterize the type.

Generic hooks and components preserve full type safety for every consumer. The caller specifies the type, and TypeScript infers everything downstream. No casts, no `any`, and no manual type assertions needed.

## Bad

```tsx
// Separate hooks with identical logic — only the type differs
function useUserList() {
  const [items, setItems] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    fetchUsers().then(setItems).finally(() => setIsLoading(false));
  }, []);

  return { items, isLoading };
}

function useFacilityList() {
  const [items, setItems] = useState<CreditFacility[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    fetchFacilities().then(setItems).finally(() => setIsLoading(false));
  }, []);

  return { items, isLoading };
}

// A "generic" approach using any — loses type safety
function useList(fetcher: () => Promise<any[]>) {
  const [items, setItems] = useState<any[]>([]);
  // items[0].whatever — no type checking
  return { items };
}
```

## Good

```tsx
// One generic hook serves all types with full type safety
function useList<T>(fetcher: () => Promise<T[]>) {
  const [items, setItems] = useState<T[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    fetcher().then(setItems).finally(() => setIsLoading(false));
  }, [fetcher]);

  return { items, isLoading };
}

// Consumers get full type inference — no need to specify the generic manually
const { items: users } = useList(fetchUsers);           // users: User[]
const { items: facilities } = useList(fetchFacilities); // facilities: CreditFacility[]

// Generic component example
interface DataTableProps<T> {
  rows: T[];
  columns: Array<{ key: keyof T; label: string }>;
  onRowClick?: (row: T) => void;
}

function DataTable<T>({ rows, columns, onRowClick }: DataTableProps<T>) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={String(col.key)}>{col.label}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i} onClick={() => onRowClick?.(row)}>
            {columns.map((col) => (
              <td key={String(col.key)}>{String(row[col.key])}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

## See Also

- [ts-discriminated-unions](ts-discriminated-unions.md) - Use discriminated unions for state machines
