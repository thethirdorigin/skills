# test-custom-hooks

> Test custom hooks by testing their inputs and outputs with renderHook

## Why It Matters

Hook tests should be isolated from the components that consume them. Testing a hook through a component couples the test to that component's rendering logic, props, and structure. When the component changes, the hook test breaks — even if the hook itself is correct.

`renderHook` from React Testing Library provides a minimal wrapper that lets you call the hook, inspect its return values, and trigger updates with `act`. This isolates the hook's API and makes tests fast, focused, and resilient to component-level refactors.

## Bad

```tsx
// Testing a hook by testing the component that uses it — coupled to component details
import { render, screen, fireEvent } from "@testing-library/react";

function TestConsumer() {
  const { count, increment, decrement } = useCounter(0);
  return (
    <div>
      <span data-testid="count">{count}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}

it("increments count", () => {
  render(<TestConsumer />);
  fireEvent.click(screen.getByText("+"));
  // Test is coupled to TestConsumer's structure — if it changes, test breaks
  expect(screen.getByTestId("count")).toHaveTextContent("1");
});
```

## Good

```tsx
// Testing the hook in isolation with renderHook
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("starts with the initial value", () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it("increments the count", () => {
    const { result } = renderHook(() => useCounter(0));
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });

  it("decrements the count", () => {
    const { result } = renderHook(() => useCounter(5));
    act(() => result.current.decrement());
    expect(result.current.count).toBe(4);
  });

  it("does not decrement below zero", () => {
    const { result } = renderHook(() => useCounter(0));
    act(() => result.current.decrement());
    expect(result.current.count).toBe(0);
  });

  it("resets to the initial value", () => {
    const { result } = renderHook(() => useCounter(3));
    act(() => result.current.increment());
    act(() => result.current.increment());
    act(() => result.current.reset());
    expect(result.current.count).toBe(3);
  });
});
```

## See Also

- [test-behaviour](test-behaviour.md) - Test user-visible behaviour, not implementation details
