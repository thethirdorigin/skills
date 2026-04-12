# comp-pure-render

> Keep components pure — same props produce the same JSX output

## Why It Matters

React assumes components are pure functions of their props and state. Given the same inputs, a component should always return the same JSX. This guarantee is what makes React's concurrent features, Strict Mode double-rendering, and memoisation work correctly.

Impure renders — reading `Date.now()`, calling `Math.random()`, or mutating external variables during render — produce different output on each call. React may call your render function multiple times per commit (Strict Mode does this intentionally to surface impurities). Side effects in render multiply unpredictably, causing duplicate API calls, flickering UI, and state corruption that is extremely difficult to reproduce.

## Bad

```tsx
// Impure — reads live clock during render, mutates external variable
let renderCount = 0;

function TransactionList({ transactions }: { transactions: Transaction[] }) {
  renderCount++; // Mutating external variable during render
  const now = Date.now(); // Different value every render

  return (
    <div>
      <p>Rendered {renderCount} times at {now}</p>
      {transactions.map((tx) => (
        <div key={tx.id}>
          {tx.description} — {tx.amount > 0 ? "credit" : "debit"}
        </div>
      ))}
    </div>
  );
}
```

## Good

```tsx
// Pure — same props always produce the same output
function TransactionList({ transactions }: { transactions: Transaction[] }) {
  return (
    <ul>
      {transactions.map((tx) => (
        <li key={tx.id}>
          {tx.description} — {tx.amount > 0 ? "credit" : "debit"}
        </li>
      ))}
    </ul>
  );
}

// Side effects and live values belong in hooks or event handlers
function TransactionPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [lastFetched, setLastFetched] = useState<number>(0);

  useEffect(() => {
    setLastFetched(Date.now());
    fetchTransactions().then(setTransactions);
  }, []);

  return (
    <div>
      <p>Last updated: {new Date(lastFetched).toLocaleTimeString()}</p>
      <TransactionList transactions={transactions} />
    </div>
  );
}
```

## See Also

- [comp-side-effects](comp-side-effects.md) - Place side effects in useEffect or event handlers
