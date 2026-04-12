# test-behaviour

> Test user-visible behaviour, not implementation details

## Why It Matters

Implementation tests break on refactors even when behaviour is unchanged. If you test that a specific internal function was called or that state holds a particular value, renaming that function or restructuring state breaks the test — even though the user experience is identical.

Behaviour tests verify what users actually see and interact with: rendered text, element visibility, form submissions, and navigation. These tests survive refactors, catch real regressions, and serve as living documentation of what the component does from the user's perspective.

## Bad

```tsx
// Testing implementation details — breaks on any internal refactor
import { render } from "@testing-library/react";
import { Counter } from "./Counter";

it("increments internal state", () => {
  const { container } = render(<Counter />);
  const instance = container.firstChild as any;

  // Accessing internal state — this is not what users see
  expect(instance._reactInternals.memoizedState.count).toBe(0);

  // Testing that a specific handler name exists
  expect(typeof instance.handleIncrement).toBe("function");
});

it("calls the increment utility", () => {
  const spy = vi.spyOn(utils, "incrementValue");
  render(<Counter />);
  fireEvent.click(screen.getByRole("button"));

  // Tied to internal implementation — refactoring breaks this
  expect(spy).toHaveBeenCalledWith(0);
});
```

## Good

```tsx
// Testing user-visible behaviour — survives refactors
import { render, screen, fireEvent } from "@testing-library/react";
import { Counter } from "./Counter";

it("displays zero initially", () => {
  render(<Counter />);
  expect(screen.getByText("Count: 0")).toBeInTheDocument();
});

it("increments the displayed count when the button is clicked", () => {
  render(<Counter />);
  fireEvent.click(screen.getByRole("button", { name: "Increment" }));
  expect(screen.getByText("Count: 1")).toBeInTheDocument();
});

it("disables the button at the maximum value", () => {
  render(<Counter max={2} />);
  fireEvent.click(screen.getByRole("button", { name: "Increment" }));
  fireEvent.click(screen.getByRole("button", { name: "Increment" }));
  expect(screen.getByRole("button", { name: "Increment" })).toBeDisabled();
});
```

## See Also

- [test-accessible-selectors](test-accessible-selectors.md) - Prefer accessible selectors: getByRole, getByLabelText, getByText
