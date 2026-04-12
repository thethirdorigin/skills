# name-import-order

> Organize imports in consistent groups separated by blank lines

## Why It Matters

Consistent import order makes dependencies scannable at a glance. When imports follow a predictable structure, you can immediately see whether a file depends on external libraries, internal shared modules, or local siblings. This reduces cognitive load during code review and helps catch unnecessary dependencies early.

Randomly ordered imports force readers to hunt through the list to understand what a file depends on. Grouping with blank line separators creates visual structure that the eye can quickly parse.

## Bad

```tsx
import { formatCurrency } from "../../utils/formatCurrency";
import React, { useState, useEffect } from "react";
import { CreditFacilityCard } from "./CreditFacilityCard";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/Button";
import type { CreditFacility } from "@/types/facility";
import { z } from "zod";
import { fetchFacilities } from "../api/facilities";
```

## Good

```tsx
// 1. React
import React, { useState, useEffect } from "react";

// 2. External libraries
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";

// 3. Internal/aliased imports
import { Button } from "@/components/ui/Button";
import type { CreditFacility } from "@/types/facility";
import { formatCurrency } from "@/utils/formatCurrency";

// 4. Relative imports (siblings, parent)
import { fetchFacilities } from "../api/facilities";
import { CreditFacilityCard } from "./CreditFacilityCard";
```

## See Also

- [name-file-convention](name-file-convention.md) - Use PascalCase for component files, camelCase for utility files
