# anti-god-component

> Split components over 300-500 lines into smaller, focused components

## Why It Matters

God components accumulate data fetching, state management, business logic, and rendering into a single file. They are hard to test because setting up the required state is complex, hard to review because every change touches unrelated logic, and hard to modify without side effects because responsibilities are tangled.

Smaller components with clear responsibilities are independently testable, easier to review in pull requests, and safer to change. A component that handles one thing well can be reused, memoised, and code-split. A 600-line monolith cannot.

## Bad

```tsx
// Dashboard.tsx — 600+ lines, does everything
function Dashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [sortColumn, setSortColumn] = useState<string>("name");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [isExporting, setIsExporting] = useState(false);

  useEffect(() => { /* fetch users */ }, []);

  const filteredUsers = users.filter((u) => {
    /* 30 lines of filtering logic */
  });

  const sortedUsers = [...filteredUsers].sort((a, b) => {
    /* 20 lines of sorting logic */
  });

  const paginatedUsers = sortedUsers.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE,
  );

  async function handleExport() {
    /* 25 lines of CSV export logic */
  }

  return (
    <div>
      {/* 50 lines of filter UI */}
      {/* 40 lines of table rendering */}
      {/* 30 lines of pagination UI */}
      {/* 20 lines of export button and modal */}
    </div>
  );
}
```

## Good

```tsx
// Dashboard.tsx — composes focused sub-components, under 80 lines
function Dashboard() {
  const { users, isLoading, error } = useUsers();
  const { filteredUsers, filters, setFilters } = useUserFilters(users);
  const { sortedUsers, sortColumn, sortDirection, toggleSort } = useUserSort(filteredUsers);
  const { page, pageData, setPage, totalPages } = usePagination(sortedUsers, PAGE_SIZE);

  if (isLoading) return <DashboardSkeleton />;
  if (error) return <ErrorBanner message="Failed to load users" />;

  return (
    <div>
      <DashboardFilters filters={filters} onChange={setFilters} />
      <UserTable
        users={pageData}
        sortColumn={sortColumn}
        sortDirection={sortDirection}
        onSort={toggleSort}
      />
      <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
      <ExportButton users={filteredUsers} />
    </div>
  );
}
```

## See Also

- [anti-business-in-component](anti-business-in-component.md) - Extract business logic into custom hooks or utility functions
