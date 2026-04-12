# test-accessible-selectors

> Prefer accessible selectors: getByRole, getByLabelText, getByText

## Why It Matters

Accessible selectors verify that the element is actually accessible to assistive technologies. If `getByRole('button', { name: 'Submit' })` cannot find your submit button, screen readers cannot find it either. Your test just caught an accessibility bug for free.

Selectors like `getByTestId` or `container.querySelector` only verify that a DOM node exists with a particular attribute or class. They tell you nothing about whether the element is perceivable, operable, or labelled. Accessible selectors enforce correctness at the intersection of functionality and accessibility.

## Bad

```tsx
// Implementation-coupled selectors — no accessibility verification
import { render } from "@testing-library/react";
import { LoginForm } from "./LoginForm";

it("submits credentials", async () => {
  const { container } = render(<LoginForm onSubmit={vi.fn()} />);

  // CSS class selector — breaks on styling changes, verifies nothing about accessibility
  const emailInput = container.querySelector(".email-input");
  const passwordInput = container.querySelector('[data-testid="password-field"]');
  const submitBtn = container.querySelector("#submit-btn");

  fireEvent.change(emailInput!, { target: { value: "user@example.com" } });
  fireEvent.change(passwordInput!, { target: { value: "s3cure" } });
  fireEvent.click(submitBtn!);
});
```

## Good

```tsx
// Accessible selectors — test finds elements the way users and screen readers do
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

it("submits credentials", async () => {
  const handleSubmit = vi.fn();
  render(<LoginForm onSubmit={handleSubmit} />);

  // getByRole and getByLabelText verify the elements are accessible
  await userEvent.type(screen.getByLabelText("Email address"), "user@example.com");
  await userEvent.type(screen.getByLabelText("Password"), "s3cure");
  await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

  expect(handleSubmit).toHaveBeenCalledWith({
    email: "user@example.com",
    password: "s3cure",
  });
});
```

## See Also

- [test-data-testid-last](test-data-testid-last.md) - Use data-testid only when semantic selectors are not available
