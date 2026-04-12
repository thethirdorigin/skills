# comp-match-structure

> Follow the existing project file structure discovered in architecture discovery

## Why It Matters

Consistent structure means developers know where to find things. When the project uses `pages/` and `components/`, a new page belongs in `pages/` and a new shared component belongs in `components/`. Introducing a competing pattern like `features/` fragments the codebase and forces every developer to check multiple locations.

Architecture discovery (reading the existing folder layout, examining how similar components are organised) should always happen before creating new files. Match the conventions already in place, even if you personally prefer a different structure.

## Bad

```tsx
// Project uses pages/ + components/, but developer invents a new pattern
// src/
//   pages/
//     Dashboard.tsx
//     Settings.tsx
//   components/
//     Button.tsx
//     Modal.tsx
//   features/            <-- new competing pattern
//     billing/
//       BillingPage.tsx
//       BillingCard.tsx

// Now developers must check both pages/ and features/ for page components
import { BillingPage } from "../features/billing/BillingPage";
import { Dashboard } from "../pages/Dashboard";
```

## Good

```tsx
// Follow the existing structure — new page goes in pages/, new component in components/
// src/
//   pages/
//     Dashboard.tsx
//     Settings.tsx
//     Billing.tsx          <-- new page follows existing pattern
//   components/
//     Button.tsx
//     Modal.tsx
//     BillingCard.tsx      <-- new shared component follows existing pattern

import { Billing } from "../pages/Billing";
import { BillingCard } from "../components/BillingCard";
```

## See Also

- [name-file-convention](name-file-convention.md) - Follow the project's file naming convention
