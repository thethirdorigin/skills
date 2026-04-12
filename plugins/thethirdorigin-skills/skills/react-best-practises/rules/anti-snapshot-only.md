# anti-snapshot-only

> Avoid using snapshot tests as the sole testing strategy

## Why It Matters

Snapshots catch unintended changes but do not verify correctness. A snapshot test passes as long as the output matches the last saved snapshot — it says nothing about whether the output is right. When snapshots break, developers routinely run "update all snapshots" without reviewing the diffs, rubber-stamping whatever the component currently produces.

Snapshots are useful for stable, visual structures like icon components or layout wrappers. For interactive components with state changes, error handling, and user flows, behaviour tests provide real verification. Use snapshots as a complement, never as the only line of defence.

## Bad

```tsx
// Snapshot as the only test for a complex interactive form
import { render } from "@testing-library/react";
import { RegistrationForm } from "./RegistrationForm";

describe("RegistrationForm", () => {
  it("renders correctly", () => {
    const { container } = render(
      <RegistrationForm onSubmit={vi.fn()} />,
    );
    // This is the entire test suite for a form with validation,
    // error states, conditional fields, and submission logic
    expect(container).toMatchSnapshot();
  });
});
```

## Good

```tsx
// Snapshots for stable structure, behaviour tests for interactions
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { RegistrationForm } from "./RegistrationForm";

describe("RegistrationForm", () => {
  it("shows validation errors for empty required fields", async () => {
    render(<RegistrationForm onSubmit={vi.fn()} />);
    await userEvent.click(screen.getByRole("button", { name: "Register" }));

    expect(screen.getByText("Email is required")).toBeInTheDocument();
    expect(screen.getByText("Password is required")).toBeInTheDocument();
  });

  it("shows password strength indicator as user types", async () => {
    render(<RegistrationForm onSubmit={vi.fn()} />);
    await userEvent.type(screen.getByLabelText("Password"), "abc");

    expect(screen.getByText("Weak")).toBeInTheDocument();

    await userEvent.clear(screen.getByLabelText("Password"));
    await userEvent.type(screen.getByLabelText("Password"), "C0mplex!Pass#2024");

    expect(screen.getByText("Strong")).toBeInTheDocument();
  });

  it("submits valid form data", async () => {
    const handleSubmit = vi.fn();
    render(<RegistrationForm onSubmit={handleSubmit} />);

    await userEvent.type(screen.getByLabelText("Email"), "alice@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "SecurePass123!");
    await userEvent.click(screen.getByRole("button", { name: "Register" }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: "alice@example.com",
      password: "SecurePass123!",
    });
  });

  it("disables the submit button while submitting", async () => {
    const handleSubmit = vi.fn(() => new Promise(() => {})); // Never resolves
    render(<RegistrationForm onSubmit={handleSubmit} />);

    await userEvent.type(screen.getByLabelText("Email"), "alice@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "SecurePass123!");
    await userEvent.click(screen.getByRole("button", { name: "Register" }));

    expect(screen.getByRole("button", { name: "Registering..." })).toBeDisabled();
  });
});
```

## See Also

- [test-behaviour](test-behaviour.md) - Test user-visible behaviour, not implementation details
