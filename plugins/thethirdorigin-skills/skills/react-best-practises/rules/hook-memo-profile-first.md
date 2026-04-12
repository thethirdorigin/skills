# hook-memo-profile-first

> Profile before applying useMemo or useCallback — avoid premature optimisation

## Why It Matters

`useMemo` and `useCallback` are not free. On every render, React must compare each dependency against its previous value. When applied indiscriminately to every computed value and callback, this comparison overhead can exceed the cost of the computation it claims to save.

Measure first using React DevTools Profiler or browser performance tools. Identify which components actually re-render too frequently or too slowly, then apply memoisation surgically to those specific bottlenecks. This keeps the codebase simple and ensures every optimisation delivers measurable improvement.

## Bad

```tsx
function ProductCard({ product }: { product: Product }) {
  // Memoising a trivial string concatenation — comparison costs more than the work
  const displayName = useMemo(
    () => `${product.brand} ${product.name}`,
    [product.brand, product.name]
  );

  // Memoising every callback regardless of cost
  const handleClick = useCallback(() => {
    navigate(`/products/${product.id}`);
  }, [product.id]);

  // Memoising a simple boolean check
  const isOnSale = useMemo(
    () => product.salePrice < product.price,
    [product.salePrice, product.price]
  );

  return (
    <div onClick={handleClick}>
      <h3>{displayName}</h3>
      {isOnSale && <Badge>Sale</Badge>}
    </div>
  );
}
```

## Good

```tsx
function ProductCard({ product }: { product: Product }) {
  // Simple computations — no memoisation needed
  const displayName = `${product.brand} ${product.name}`;
  const isOnSale = product.salePrice < product.price;

  function handleClick() {
    navigate(`/products/${product.id}`);
  }

  return (
    <div onClick={handleClick}>
      <h3>{displayName}</h3>
      {isOnSale && <Badge>Sale</Badge>}
    </div>
  );
}

// Memoise only when profiling reveals a bottleneck
function ProductSearch({ products }: { products: Product[] }) {
  const [query, setQuery] = useState("");

  // Profiling showed this filter over 10,000 products causes visible lag
  const filtered = useMemo(
    () => products.filter((p) => matchesSearch(p, query)),
    [products, query]
  );

  return <ProductGrid products={filtered} />;
}
```

## See Also

- [hook-useState-callback](hook-useState-callback.md) - Use callback initialiser for expensive initial state
