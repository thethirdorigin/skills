# test-data-testid-last

> Use data-testid only when semantic selectors are not available

## Why It Matters

`data-testid` tests nothing about accessibility. It only proves that a DOM node exists with a particular attribute. Preferring it as the default selector strategy means your tests pass even when elements are missing labels, roles, or accessible names — hiding real accessibility bugs.

The recommended priority is: `getByRole` (verifies role and accessible name), then `getByLabelText` (verifies form labels), then `getByText` (verifies visible text), and finally `getByTestId` as a last resort for complex dynamic content where no semantic selector applies, such as a canvas element or a dynamically generated container.

## Bad

```tsx
// data-testid on everything — no accessibility verification
function SearchResults({ results }: { results: Result[] }) {
  return (
    <div data-testid="search-results">
      {results.map((result) => (
        <div key={result.id} data-testid={`result-${result.id}`}>
          <span data-testid={`result-title-${result.id}`}>{result.title}</span>
          <button data-testid={`result-save-${result.id}`}>Save</button>
        </div>
      ))}
    </div>
  );
}

// Tests pass even if elements are completely inaccessible
it("renders results", () => {
  render(<SearchResults results={mockResults} />);
  expect(screen.getByTestId("result-title-1")).toHaveTextContent("First Result");
  fireEvent.click(screen.getByTestId("result-save-1"));
});
```

## Good

```tsx
// Semantic selectors first — data-testid only for the canvas
function SearchResults({ results }: { results: Result[] }) {
  return (
    <section aria-label="Search results">
      {results.map((result) => (
        <article key={result.id}>
          <h3>{result.title}</h3>
          <button aria-label={`Save ${result.title}`}>Save</button>
          <canvas data-testid={`result-chart-${result.id}`} /> {/* No semantic alternative */}
        </article>
      ))}
    </section>
  );
}

it("renders results with accessible structure", () => {
  render(<SearchResults results={mockResults} />);

  // getByRole — verifies accessibility
  expect(screen.getByRole("region", { name: "Search results" })).toBeInTheDocument();

  // getByText — verifies visible content
  expect(screen.getByText("First Result")).toBeInTheDocument();

  // getByRole with accessible name — verifies button is properly labelled
  fireEvent.click(screen.getByRole("button", { name: "Save First Result" }));

  // data-testid only for the canvas where no semantic selector exists
  expect(screen.getByTestId("result-chart-1")).toBeInTheDocument();
});
```

## See Also

- [test-accessible-selectors](test-accessible-selectors.md) - Prefer accessible selectors: getByRole, getByLabelText, getByText
