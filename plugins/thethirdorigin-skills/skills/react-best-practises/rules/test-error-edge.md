# test-error-edge

> Test error states and edge cases, not just the happy path

## Why It Matters

Edge cases are where bugs hide. A test suite that only covers successful form submission, successful API responses, and populated lists gives false confidence. Real users encounter network failures, empty datasets, validation errors, and race conditions constantly.

Testing error states and boundaries ensures the application degrades gracefully. It also documents how the component behaves in unusual conditions, making it easier for other developers to understand and maintain the error handling logic.

## Bad

```tsx
// Only testing the happy path — no error coverage
describe("OrderForm", () => {
  it("submits the order", async () => {
    server.use(http.post("/api/orders", () => HttpResponse.json({ id: "order-1" })));

    render(<OrderForm />);
    await userEvent.type(screen.getByLabelText("Item"), "Widget");
    await userEvent.type(screen.getByLabelText("Quantity"), "5");
    await userEvent.click(screen.getByRole("button", { name: "Place Order" }));

    expect(await screen.findByText("Order confirmed")).toBeInTheDocument();
  });
  // No tests for validation, network errors, empty states, or edge cases
});
```

## Good

```tsx
describe("OrderForm", () => {
  it("submits a valid order", async () => {
    server.use(http.post("/api/orders", () => HttpResponse.json({ id: "order-1" })));

    render(<OrderForm />);
    await userEvent.type(screen.getByLabelText("Item"), "Widget");
    await userEvent.type(screen.getByLabelText("Quantity"), "5");
    await userEvent.click(screen.getByRole("button", { name: "Place Order" }));

    expect(await screen.findByText("Order confirmed")).toBeInTheDocument();
  });

  it("shows validation error for empty item name", async () => {
    render(<OrderForm />);
    await userEvent.click(screen.getByRole("button", { name: "Place Order" }));

    expect(screen.getByText("Item name is required")).toBeInTheDocument();
  });

  it("shows validation error for zero quantity", async () => {
    render(<OrderForm />);
    await userEvent.type(screen.getByLabelText("Item"), "Widget");
    await userEvent.type(screen.getByLabelText("Quantity"), "0");
    await userEvent.click(screen.getByRole("button", { name: "Place Order" }));

    expect(screen.getByText("Quantity must be at least 1")).toBeInTheDocument();
  });

  it("displays a network error message when the API fails", async () => {
    server.use(http.post("/api/orders", () => HttpResponse.error()));

    render(<OrderForm />);
    await userEvent.type(screen.getByLabelText("Item"), "Widget");
    await userEvent.type(screen.getByLabelText("Quantity"), "5");
    await userEvent.click(screen.getByRole("button", { name: "Place Order" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Failed to place order");
  });

  it("disables the submit button while the request is in flight", async () => {
    server.use(
      http.post("/api/orders", async () => {
        await delay(100);
        return HttpResponse.json({ id: "order-1" });
      }),
    );

    render(<OrderForm />);
    await userEvent.type(screen.getByLabelText("Item"), "Widget");
    await userEvent.type(screen.getByLabelText("Quantity"), "5");
    await userEvent.click(screen.getByRole("button", { name: "Place Order" }));

    expect(screen.getByRole("button", { name: "Placing..." })).toBeDisabled();
  });
});
```

## See Also

- [err-handle-all-states](err-handle-all-states.md) - Handle loading, error, and empty states in every data-fetching component
