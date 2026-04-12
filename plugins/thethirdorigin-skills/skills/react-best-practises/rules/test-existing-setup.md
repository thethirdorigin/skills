# test-existing-setup

> Use the project's existing test runner and testing library

## Why It Matters

Mixing test frameworks causes configuration conflicts, inconsistent APIs, and a fragmented test suite. A project that uses Vitest with React Testing Library has its configuration, matchers, and CI pipeline tuned for that stack. Introducing Jest or Enzyme alongside it means maintaining two sets of configs, two sets of setup files, and two different assertion styles.

Before writing any test, check `package.json` for the existing test dependencies. Common stacks include Vitest + React Testing Library, Jest + React Testing Library, or Playwright/Cypress for end-to-end tests. Follow what is already there.

## Bad

```tsx
// Project uses Vitest, but developer adds Jest for their new tests
// package.json already has: "vitest": "^1.6.0", "@testing-library/react": "^15.0.0"

// New test file uses Jest globals — breaks the existing Vitest config
import { render, screen } from "@testing-library/react";
import { jest } from "@jest/globals"; // Wrong framework

describe("UserProfile", () => {
  it("renders user name", () => {
    jest.spyOn(api, "fetchUser"); // Jest spy in a Vitest project
    render(<UserProfile userId="123" />);
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });
});
```

## Good

```tsx
// Follow the existing Vitest + React Testing Library setup
import { render, screen } from "@testing-library/react";
import { vi, describe, it, expect } from "vitest";
import { UserProfile } from "./UserProfile";

describe("UserProfile", () => {
  it("renders user name", () => {
    vi.spyOn(api, "fetchUser").mockResolvedValue({ name: "Alice" });
    render(<UserProfile userId="123" />);
    expect(screen.getByText("Alice")).toBeInTheDocument();
  });
});
```

## See Also

- [test-behaviour](test-behaviour.md) - Test user-visible behaviour, not implementation details
