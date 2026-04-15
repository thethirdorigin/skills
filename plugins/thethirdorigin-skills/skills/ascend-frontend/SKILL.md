---
name: ascend-frontend
description: >
  How to build new pages in the Ascend Platform frontend. Covers workspace
  layout, shared component/hook/util inventories, routing, auth, styling,
  loading states, and step-by-step page-building checklist. Use when creating,
  modifying, or reviewing any page in the admin or client apps.
triggers:
  - build ascend page
  - ascend frontend
  - new page in ascend
  - add page to admin app
  - add page to client app
  - ascend shared components
  - ascend platform frontend
file-patterns:
  - frontend/apps/admin/
  - frontend/apps/client/
  - frontend/packages/shared/
  - frontend/mocked/
---

# Building Frontend Pages — Ascend Platform

<context>
You are a senior React/TypeScript engineer building pages for the Ascend Platform — a DeFi credit-facility management product with two production apps (Admin and Client) and a shared component library.

The frontend is a **pnpm monorepo** at `frontend/` with these packages:

| Package | Name | Purpose |
|---------|------|---------|
| `apps/admin` | `@ascend/admin-app` | Ops dashboard — Okta OIDC auth, port 5100 |
| `apps/client` | `@ascend/client-app` | Borrower portal — wagmi + SIWE auth, port 5200 |
| `mocked/admin` | `@ascend/admin` | Visual-reference-only admin, port 4100 |
| `mocked/client` | `@ascend/client` | Visual-reference-only client, port 4200 |
| `mocked/shared` | `@ascend/mocked-shared` | Mock data (SQLite WASM) for mocked apps |
| `packages/shared` | `@ascend/shared` | Production shared code: API client, components, hooks, types, utils, styles |

**Tech stack:** React 19, React Router 7 (v6-compat API), Vite 6, TypeScript 5.8, Tailwind CSS 4, `@openzeppelin/ui-components`, Zustand 5, TanStack React Query 5, React Hook Form 7, Lucide React (icons), Sonner (toasts), wagmi 3 + viem 2 (wallet).

**Visual reference:** Mocked apps show the target design for every page. Use them to see the final look, then build the page from first principles using shared components and real API hooks.

- Mocked Admin: https://ascend-mock-admin.vercel.app (or locally on port 4100)
- Mocked Client: https://ascend-mock-client.vercel.app (or locally on port 4200)
- Mocked source: `mocked/admin/src/pages/`, `mocked/client/src/pages/`

**Do not** port code, data patterns, or structure from the mocked apps. They exist purely for visual reference.
</context>

---

## 1. Step-by-Step Page-Building Checklist

<instructions>

### 1a. Start the mocked app to see the target design

```bash
# from frontend/
pnpm dev:mocked:admin   # port 4100
pnpm dev:mocked:client  # port 4200
```

### 1b. Create the page component

- Place the file under `src/pages/` in the target app
- Use a **default export** (required by `lazy()`)
- Simple pages: single file (`MyPage.tsx`)
- Complex pages: folder with `index.ts` barrel (`my-page/MyPage.tsx`, `my-page/index.ts`)

### 1c. Register the route

Open `src/router.tsx` in the target app:

1. Add a lazy import at the top:
```typescript
const MyPage = lazy(() => import('./pages/MyPage'));
```

2. Add the `<Route>` inside the authenticated layout group, wrapped in `SuspenseWrapper`:
```tsx
<Route
  path="my-path"
  element={
    <SuspenseWrapper>
      <MyPage />
    </SuspenseWrapper>
  }
/>
```

### 1d. Add the nav item

Open `src/layouts/AdminLayout.tsx` (or `ClientLayout.tsx`) and add an entry to the `NAV_SECTIONS` array:
```typescript
{ label: 'My Page', path: '/my-path', icon: SomeLucideIcon },
```

Active state is automatic — the layout matches `pathname === path || pathname.startsWith(path + '/')`.

### 1e. Build the page using the component/hook inventory below

Follow these structural conventions:
- Outer wrapper: `<div className="space-y-6 sm:space-y-8">`
- Start with `<PageHeader title="..." subtitle="..." icon={LucideIcon} />`
- Optional `action` prop on PageHeader for primary CTA button
- Stat cards in a responsive grid: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4`
- Content sections in bordered containers: `rounded-xl border border-border p-5 sm:p-6`

### 1f. Handle loading, error, and empty states

Every data-driven page must handle all three states:
```tsx
{isLoading ? (
  <LoadingState variant="section" />
) : error ? (
  <EmptyState
    title="Unable to load data"
    description="Something went wrong. Please try again later."
    icon={<AlertTriangle className="h-10 w-10 text-ascend-error" />}
  />
) : items.length === 0 ? (
  <EmptyState title="No items" description="Adjust your filters." />
) : (
  /* render content */
)}
```

Use `variant="page"` for full-page loading, `variant="section"` for inline sections.
</instructions>

---

## 2. Provider Tree

<context>
Pages render inside this provider hierarchy (set up in `main.tsx`). You do not need to add providers — just understand what is available.

```
StrictMode
  └─ WagmiProvider (wagmiConfig)
       └─ QueryClientProvider (staleTime: 60s, retry: 1, no refocus refetch)
            └─ ApiProvider (base URL + auth interceptors)
                 └─ App
                 └─ Toaster (sonner, top-right, richColors)
```

**Admin auth:** Okta OIDC + PKCE. Token stored in Zustand (`useAdminAuthStore`) with sessionStorage persistence. `createAdminAuthConfig` wires Bearer injection + session-expired logout. Dev mode: fake "local-dev-admin" user (no Okta needed).

**Client auth:** wagmi wallet connect + SIWE. Tokens stored in Zustand (`useWalletStore`) with sessionStorage persistence. `createSiweAuthConfig` wires Bearer injection + refresh-on-401 + token clearing.

Both apps proxy `/api` to `VITE_API_PROXY_TARGET` (default `http://localhost:3000`) via Vite dev server.
</context>

---

## 3. Shared Component Inventory

<instructions>
Import from `@ascend/shared/components`. Always prefer these over building custom equivalents.

### Layout & Structure
| Component | Key Props | Notes |
|-----------|-----------|-------|
| `PageHeader` | `title`, `subtitle?`, `icon?: LucideIcon`, `action?: ReactNode` | Use at the top of every page |
| `SplitPage` | `panel`, `children` | Responsive split layout for detail pages |
| `AscendLogo` | `className?`, `size?` | SVG logo using `currentColor` |

### Data Display
| Component | Key Props | Notes |
|-----------|-----------|-------|
| `StatCard` | `title`, `value`, `subtitle?`, `icon?`, `badges?`, `trend?`, `loading?`, `onClick?` | Has built-in shimmer when `loading` is true |
| `StatusBadge` | `status`, `configMap?` | Green/yellow/red/blue based on status string |
| `BarChart` | `items`, `total?`, `barHeight?`, `formatTooltip?` | CSS hover tooltips; export `BarChartItem` type |
| `FacilityCard` | `facility`, `metrics?` | Links to `/credit-facilities/:id` |

### Feedback & State
| Component | Key Props | Notes |
|-----------|-----------|-------|
| `LoadingState` | `variant?: 'page' \| 'section' \| 'inline'`, `message?` | Use `page` for route-level, `section` for inline |
| `EmptyState` | `title`, `description`, `icon?`, `action?` | Default Inbox icon |
| `ErrorBoundary` | `children`, `fallback?` | Class component; wraps pages in router |
| `ConfirmDialog` | `open`, `onOpenChange`, `title`, `description`, `onConfirm`, `variant?` | Portal + focus trap. **Always use this instead of OZ UI Dialog** |

### Table System
| Component | Key Props | Notes |
|-----------|-----------|-------|
| `DataTable` | `columns: DataTableColumn[]`, `rows`, `rowKey`, `sort?`, `onRowClick?` | Generic table with sortable headers |
| `SearchBar` | `value`, `onChange`, `placeholder?` | Styled search input |
| `FilterTabs` | `filters`, `active`, `onChange`, `counts?` | Pill-style filter tabs |
| `SortableHeader` | `label`, `sortKey`, `activeSortKey`, `direction`, `onSort` | Column header with sort indicator |
| `PaginationControls` | `page`, `setPage`, `pageSize`, `setPageSize`, `totalItems`, `label` | Full pagination bar with page-size selector |
| `PageNumbers` | `currentPage`, `totalPages`, `onPageChange` | Standalone page number nav |
| `ViewModeToggle` | `viewMode: 'grid' \| 'list'`, `onChange` | Grid/list toggle buttons |
| `MarginAccountsTablePanel` | Large props object | Pre-built table for margin accounts |

### Table Hooks (from `@ascend/shared/components`)
| Hook | Returns |
|------|---------|
| `useTableControls` | `{ query, setQuery, page, setPage, pageSize, setPageSize, resetPage }` |
| `usePaginatedRows` | `{ rows, safePage, totalPages }` |

### Constants
| Export | Value |
|--------|-------|
| `PAGE_SIZE_OPTIONS` | `[6, 12, 24]` |
| `TABLE_PAGE_SIZE_OPTIONS` | `[10, 25, 50]` |
| `INPUT_CLASS` | Tailwind input class string |
</instructions>

<anti-patterns>
- Using OZ UI `Dialog` directly — Tailwind v4 purges its positioning classes. Always use `ConfirmDialog`.
- Building custom loading/empty components — use the shared ones for consistency.
- Creating page-local pagination logic — use `PaginationControls` + `useTableControls` or `usePaginatedRows`.
</anti-patterns>

---

## 4. Shared Hooks Inventory

<instructions>
Import from `@ascend/shared/hooks`. All query hooks use `useApi()` internally — no manual fetch calls needed.

### Facilities
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useFacilities` | `params?` (limit, offset, status, search) | Paginated list query |
| `useFacility` | `facilityId` | Single facility detail |
| `useFacilitySummary` | — | Aggregate stats (TVL, utilization, counts) |
| `useFacilityOnChainMetrics` | `facilityIds: string[]` | Batch OCM; normalizes into per-facility cache |
| `useSingleFacilityOnChainMetrics` | `facilityId` | Reads per-facility cache — instant on list→detail nav |
| `useFacilityModules` | `facilityId` | Modules attached to a facility |
| `usePauseFacility` | — | Mutation |
| `useUnpauseFacility` | — | Mutation |
| `useUpdateFacility` | — | Mutation |

### Margin Accounts
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useMarginAccounts` | `facilityId, params?` | Paginated accounts for a facility |
| `useMarginAccount` | `facilityId, accountId` | Single account detail |
| `useMarginAccountsSummary` | `facilityId` | Account stats for a facility |
| `useInsolventAccounts` | `facilityId` | Insolvent accounts list |
| `useMarginAccountMetrics` | `facilityId, accountIds` | Batch metrics per facility |
| `useSingleMarginAccountMetrics` | `facilityId, accountId` | Single account metrics |
| `useGlobalMarginAccounts` | `facilities, params` | Multi-facility distributed fetch; returns query + `cfMap` |
| `useMultiFacilityMarginAccountMetrics` | `rows` | `{ metricsMap, isLoading }` |

### Templates
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useTemplates` | `params?` | Paginated template list |
| `useTemplate` | `templateId` | Single template |
| `useCreateTemplate` | — | Mutation |
| `useUpdateTemplate` | — | Mutation |
| `useDeleteTemplate` | — | Mutation |
| `useDeployTemplate` | — | Mutation |

### Modules
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useModules` | `params?` | Paginated module list |
| `useModule` | `moduleId` | Single module |
| `useAllModules` | — | All modules (no pagination) |
| `useFacilitiesByModule` | `moduleId` | `{ facilities, isLoading }` |
| `useSetModuleStatus` | — | Mutation |
| `useCreateModule` | — | Mutation |
| `useUpdateModule` | — | Mutation |
| `useDeleteModule` | — | Mutation |

### Chain Hub & Borrower
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useChainHubAddresses` | — | `Record<canonicalChainKey, string[]>` |
| `useBorrowerSummary` | `address` | Borrower summary data |
| `useBorrowerMarginAccounts` | `address, params?` | Borrower's margin accounts |

### Identity & System
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useAdminMe` | — | Current admin user info |
| `useIndexerStatus` | — | Indexer health status |
| `useSystemStatus` | — | Overall system status |

### Utility Hooks
| Hook | Parameters | Returns |
|------|-----------|---------|
| `useDebounce` | `value, delay` | Debounced value (use for search inputs) |
| `usePagination` | `items[], options?` | Client-side pagination with `paginatedItems` |
| `useTableState` | `options?` | Search, filter, sort state + `toggleSort` |
| `usePageResetOnChange` | `key, page, setPage` | Reset page to 1 when key changes |
| `useSendContractTransaction` | — | `{ sendContractTransaction, status, error, reset }` |
| `queryKeys` | — | React Query key factory (use for manual cache ops) |
</instructions>

---

## 5. Shared Utils Inventory

<instructions>
Import from `@ascend/shared/utils`.

### Formatting
| Function | Purpose |
|----------|---------|
| `formatCurrency` | Locale-aware currency formatting |
| `formatCompactUsd` | Compact USD from uint256 string (e.g. "$1.2M") |
| `formatPercent` | Decimal ratio string → percentage string |
| `formatBorrowRate` | Fixed-point borrow rate → percentage |
| `formatBorrowRates` | Range string for multi-token facilities |
| `formatUd60x18AsPercent` | UD60x18 fixed-point → percentage |
| `formatTokenAmount` | Human-readable token amount |
| `formatHealthFactor` | LTV → health factor display string |
| `formatNetworkLabel` | Chain ID → human-readable network name |
| `truncateAddress` | `0xAbCd...EfGh` middle-ellipsis |

### Numeric
| Function | Purpose |
|----------|---------|
| `bigintToFloat` | uint256 string + decimals → number |
| `bigintPercent` | BigInt-safe percentage calculation |
| `compareBigIntStrings` | Comparator for numeric string sorting |
| `epochSecondsToMs` | Unix seconds → milliseconds |

### Chain & Address
| Function | Purpose |
|----------|---------|
| `getExplorerAddressUrl` | Returns block explorer URL or null |
| `hexToChainAddress` | `0x` hex → API `{ EVM: number[] }` format |
| `chainIdLabel` | Chain ID → label |
| `evmChainNumber` | Extract numeric chain ID |
| `canonicalChainKey` | Canonical chain key string |
| `chainIdsEqual` | Compare chain IDs |

### Table Sorting
| Function | Purpose |
|----------|---------|
| `createRowComparator` | Generic table row sort comparator factory |
| `createMarginAccountRowComparator` | Preconfigured comparator (inverts HF asc/desc) |

### Display
| Function | Purpose |
|----------|---------|
| `healthFactorColor` | Returns Tailwind classes for health factor status |

### Storage
| Function | Purpose |
|----------|---------|
| `sessionStorageAdapter` | Zustand persist adapter for sessionStorage |
</instructions>

---

## 6. Types

<instructions>
Import from `@ascend/shared/types`. All types are auto-generated from the backend OpenAPI spec.

Regenerate after backend API changes:
```bash
pnpm --filter @ascend/shared generate:api-types
```

Key type aliases (from `components['schemas']`): `FacilityResponse`, `FacilityOnchainMetricsResponse`, `CreditFacilityStatus`, `TemplateResponse`, `ModuleResponse`, `MarginAccountResponse`, `BorrowerSummaryResponse`, `TokenBalanceResponse`, `PaginatedResponse<T>`, `TransactionStatus`, `KycStatus`, `ComponentStatus`, `StatusSummaryResponse`.
</instructions>

---

## 7. Styling

<instructions>
Tailwind CSS 4 with CSS-first configuration. No `tailwind.config.ts` file.

### Setup (already configured per app)
Each app's `src/index.css` imports:
1. `tailwindcss` with `source(none)` + `@source` directives pointing at the app, `packages/shared/src`, and `@openzeppelin/ui-*` packages
2. `@openzeppelin/ui-styles/global.css` — OZ UI base styles
3. `@ascend/shared/styles/ascend-theme.css` — Ascend brand overrides

### Theme Tokens
| Token | Value | Usage |
|-------|-------|-------|
| `--primary` / `bg-primary` | `#2d7dd2` (Ascend blue) | Primary buttons, active nav, links |
| `--primary-foreground` | `#f8fafc` | Text on primary backgrounds |
| `--background` / `bg-background` | `#ffffff` | Page background |
| `--foreground` / `text-foreground` | `#020817` | Default text |
| `--muted` / `bg-muted` | `#f1f5f9` | Muted backgrounds (filter tabs, chips) |
| `--muted-foreground` / `text-muted-foreground` | `#64748b` | Secondary text, labels, icons |
| `--border` / `border-border` | `#e2e8f0` | Borders, dividers |
| `--accent` / `bg-accent` | `#f1f5f9` | Hover backgrounds |
| `--radius` | `0.5rem` | Default border radius |
| Font | Figtree | Loaded via `<link>` in index.html |

### Brand Colors (Tailwind classes)
| Class | Value | Usage |
|-------|-------|-------|
| `text-ascend-primary` / `bg-ascend-primary` | `#2d7dd2` | Brand blue |
| `text-ascend-success` | `#00cc66` | Active/healthy states |
| `text-ascend-error` | `#ff3333` | Error/shutdown states |
| `text-ascend-warning` | `#ffcc00` | Paused/warning states |

### OZ UI Components
Import from `@openzeppelin/ui-components`: `Button`, `Card`, `Tabs`, `Tooltip`, form elements.
- `Button`: use `variant` and `size` props; add `className="gap-2"` for icon + text
- For modals, always use the shared `ConfirmDialog`, never `Dialog` from OZ UI

### Responsive Breakpoints
Mobile-first: `sm:` (640px), `md:` (768px), `lg:` (1024px). The layout container caps at `max-w-[1400px]`.
</instructions>

<anti-patterns>
- Adding a `tailwind.config.ts` — Tailwind v4 uses CSS-first config via `@theme inline` in `ascend-theme.css`
- Using raw hex colors instead of semantic tokens — prefer `text-foreground`, `bg-muted`, `border-border`
- Forgetting `sm:`/`lg:` responsive variants — pages must work on mobile
</anti-patterns>

---

## 8. Caching Strategy

<instructions>
On-chain metrics (OCM) use a batch + normalization pattern:

1. `useFacilityOnChainMetrics(facilityIds)` fetches metrics for multiple facilities in one request
2. The hook normalizes results into per-facility cache entries via `queryClient.setQueryData`
3. `useSingleFacilityOnChainMetrics(facilityId)` reads the per-facility cache — instant hit when navigating from list to detail

The same pattern applies to margin account metrics with `useMarginAccountMetrics` and `useSingleMarginAccountMetrics`.

Default staleTime is 60s (set at QueryClient level). Hooks may override individually.
</instructions>

---

## 9. Common Import Pattern

<instructions>
A well-structured page typically has these import groups:

```typescript
// 1. React + Router
import { useState, useMemo } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

// 2. Lucide icons
import { Building2, Plus, AlertTriangle } from 'lucide-react';

// 3. OZ UI components
import { Button } from '@openzeppelin/ui-components';

// 4. Shared components
import { PageHeader, StatCard, LoadingState, EmptyState } from '@ascend/shared/components';

// 5. Shared hooks
import { useFacilities, useFacilitySummary } from '@ascend/shared/hooks';

// 6. Shared utils
import { formatCompactUsd, formatPercent } from '@ascend/shared/utils';

// 7. Shared types (type-only imports)
import type { FacilityResponse } from '@ascend/shared/types';

// 8. Toasts for user feedback
import { toast } from 'sonner';

// 9. App-local imports (stores, guards, page-specific components)
import { useAdminAuthStore } from '../stores/useAdminAuthStore';
```
</instructions>

---

## 10. Page Examples

<examples>

<example>
GOOD — Dashboard page (summary + cards pattern):

```typescript
export default function DashboardPage() {
  const { data, isLoading, error } = useFacilities({ limit: 6 });
  const { data: statusData } = useSystemStatus();

  const facilities = data?.items ?? [];
  const facilityIds = useMemo(() => facilities.map((f) => f.id), [facilities]);
  const { data: ocmData } = useFacilityOnChainMetrics(facilityIds);

  return (
    <div className="space-y-6 sm:space-y-8">
      <PageHeader title="Dashboard" subtitle="Overview." icon={LayoutDashboard} />

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:gap-4">
        <StatCard title="Facilities" value={String(data?.total_count ?? 0)} loading={isLoading} />
        <StatCard title="System Health" value="Operational" />
      </div>

      {isLoading ? (
        <LoadingState variant="section" />
      ) : error ? (
        <EmptyState title="Unable to load" description="Try again later." />
      ) : facilities.length === 0 ? (
        <EmptyState title="No facilities" description="Deploy one to get started." />
      ) : (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {facilities.map((f) => (
            <FacilityCard key={f.id} facility={f} metrics={metricsMap.get(f.id)} />
          ))}
        </div>
      )}
    </div>
  );
}
```
</example>

<example>
GOOD — List page with search, filters, pagination, and view toggle:

```typescript
export default function CreditFacilitiesPage() {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(6);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const debouncedQuery = useDebounce(searchQuery, 750);

  usePageResetOnChange(`${statusFilter}|${debouncedQuery}`, page, setPage);

  const { data, isLoading, error } = useFacilities({
    limit: pageSize,
    offset: (page - 1) * pageSize,
    status: statusFilter !== 'all' ? statusFilter : undefined,
    search: debouncedQuery.trim() || undefined,
  });

  return (
    <div className="space-y-6 sm:space-y-8">
      <PageHeader
        title="Credit Facilities"
        icon={Building2}
        action={<Button className="gap-2"><Plus className="h-4 w-4" /> Deploy</Button>}
      />
      {/* StatCards, search/filter controls, content, PaginationControls */}
    </div>
  );
}
```
</example>

<example>
GOOD — Detail page with tabs and mutations:

```typescript
export default function CreditFacilityDetailPage() {
  const { facilityId, tab } = useParams();
  const navigate = useNavigate();
  const { data: facility, isLoading, error } = useFacility(facilityId!);
  const pauseMutation = usePauseFacility();
  const [showConfirm, setShowConfirm] = useState(false);

  if (isLoading) return <LoadingState variant="page" />;
  if (error || !facility) return <EmptyState title="Facility not found" />;

  return (
    <div className="space-y-6">
      <PageHeader title={facility.name} action={/* pause/unpause button */} />
      <Tabs activeTab={tab} onChange={(t) => navigate(`/credit-facilities/${facilityId}/${t}`)}>
        {/* Tab panels */}
      </Tabs>
      <ConfirmDialog open={showConfirm} onOpenChange={setShowConfirm} onConfirm={() => pauseMutation.mutate(facilityId!)} />
    </div>
  );
}
```
</example>

<example>
BAD — Direct fetch call instead of shared hooks:

```typescript
export default function MyPage() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch('/api/v1/facilities').then(r => r.json()).then(setData);
  }, []);
  // ...
}
```

Use `useFacilities()` from `@ascend/shared/hooks` — it handles auth tokens, caching, error states, and type safety.
</example>

<example>
BAD — Missing loading/error/empty state handling:

```typescript
export default function MyPage() {
  const { data } = useFacilities();
  return (
    <div>
      {data?.items.map(f => <div key={f.id}>{f.name}</div>)}
    </div>
  );
}
```

Always handle `isLoading`, `error`, and empty arrays with `LoadingState`, `EmptyState`, and appropriate user feedback.
</example>

<example>
BAD — Using OZ UI Dialog for modals:

```tsx
import { Dialog } from '@openzeppelin/ui-components';
<Dialog open={open}>...</Dialog>
```

Tailwind v4 purges OZ Dialog positioning classes. Always use:
```tsx
import { ConfirmDialog } from '@ascend/shared/components';
```
</example>

</examples>

---

## 11. Commands Reference

<instructions>

| Command | Working dir | Purpose |
|---------|-------------|---------|
| `pnpm dev:admin` | `frontend/` | Start admin app (port 5100) |
| `pnpm dev:client` | `frontend/` | Start client app (port 5200) |
| `pnpm dev:mocked` | `frontend/` | Start both mocked apps |
| `pnpm dev:mocked:admin` | `frontend/` | Mocked admin only (port 4100) |
| `pnpm dev:mocked:client` | `frontend/` | Mocked client only (port 4200) |
| `pnpm typecheck` | `frontend/` | Type-check all packages |
| `pnpm --filter @ascend/shared generate:api-types` | `frontend/` | Regenerate types from OpenAPI spec |

The backend serves on `localhost:3000`. Start it from the repo root:
```bash
SEPOLIA_RPC_URL=<rpc-url> docker compose up -d
```

Swagger UI: http://localhost:9002/v1/swagger
OpenAPI spec: `backend/open_api/platform_service_open_api_spec.json`
</instructions>

---

## 12. Architecture Differences: Admin vs Client

<instructions>

| Aspect | Admin (`apps/admin`) | Client (`apps/client`) |
|--------|---------------------|----------------------|
| Auth mechanism | Okta OIDC + PKCE | wagmi + SIWE |
| Auth store | `useAdminAuthStore` | `useWalletStore` |
| Auth guard | `RequireAuth` → redirect to `/login` | `RequireWallet` → redirect to `/` |
| Auth UI | Dedicated `LoginPage`, `OktaCallbackPage` | Connect/disconnect in layout header |
| Route protection | All routes inside `RequireAuth` + `AdminLayout` | Most routes open; `RequireWallet` group for gated routes |
| Branding | "Ascend Admin" + "Internal Use Only" chip | "Ascend" |
| Layout header | Notifications, user name, sign out, optional wallet (local dev) | Notifications, wallet connect/disconnect |
| Dev port | 5100 | 5200 |
| Wagmi usage | Available (local dev admin wallet ops only) | Primary (SIWE auth flow) |

When adding a new page, use the correct auth store and patterns for the target app.
</instructions>
