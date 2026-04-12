# test-mock-api

> Mock API calls at the network level, not internal functions

## Why It Matters

Function-level mocks (`vi.mock('../api/users')`) are tightly coupled to import paths and internal module structure. Renaming a file, moving a function, or changing how the API client is organised breaks every test that mocks it — even though the actual HTTP behaviour is unchanged.

Network-level mocking with MSW (Mock Service Worker) intercepts the actual HTTP request, testing the full request/response cycle including URL construction, serialisation, headers, and status code handling. Tests remain valid regardless of how the internal code is structured, and they catch bugs in the HTTP layer that function mocks skip entirely.

## Bad

```tsx
// Mocking internal functions — tightly coupled to file structure
import { vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { UserList } from "./UserList";

// Breaks if api/users.ts is renamed or restructured
vi.mock("../api/users", () => ({
  fetchUsers: vi.fn().mockResolvedValue([
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" },
  ]),
}));

it("renders users", async () => {
  render(<UserList />);
  expect(await screen.findByText("Alice")).toBeInTheDocument();
});

// Another test mocking a different path to the same API
vi.mock("../../services/userService", () => ({
  getUsers: vi.fn().mockResolvedValue([{ id: 1, name: "Alice" }]),
}));
```

## Good

```tsx
// MSW — mocks at the network level, decoupled from internal structure
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { render, screen } from "@testing-library/react";
import { UserList } from "./UserList";

const server = setupServer();

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it("renders the user list", async () => {
  server.use(
    http.get("/api/users", () =>
      HttpResponse.json([
        { id: 1, name: "Alice" },
        { id: 2, name: "Bob" },
      ]),
    ),
  );

  render(<UserList />);
  expect(await screen.findByText("Alice")).toBeInTheDocument();
  expect(screen.getByText("Bob")).toBeInTheDocument();
});

it("shows an error when the API returns 500", async () => {
  server.use(
    http.get("/api/users", () => new HttpResponse(null, { status: 500 })),
  );

  render(<UserList />);
  expect(await screen.findByRole("alert")).toHaveTextContent("Failed to load users");
});

it("shows empty state when no users exist", async () => {
  server.use(
    http.get("/api/users", () => HttpResponse.json([])),
  );

  render(<UserList />);
  expect(await screen.findByText("No users found")).toBeInTheDocument();
});
```

## See Also

- [test-behaviour](test-behaviour.md) - Test user-visible behaviour, not implementation details
