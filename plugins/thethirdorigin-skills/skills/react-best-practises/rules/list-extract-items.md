# list-extract-items

> Extract list items into separate components

## Why It Matters

When list item rendering logic lives inline within a `.map()` callback, the parent component becomes harder to read and maintain. Every render of the parent re-evaluates the entire map body, and there is no way to memoize individual items to skip unnecessary re-renders.

Extracting each item into its own component creates a clear boundary. You can wrap the item component with `React.memo` so it only re-renders when its own props change. This is especially important for long lists where a single state change in one item would otherwise force every sibling to re-render.

## Bad

```tsx
interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

function ProductGrid({ products, onAddToCart }: {
  products: Product[];
  onAddToCart: (id: string) => void;
}) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((product) => (
        <div key={product.id} className="rounded border p-4">
          <img
            src={product.imageUrl}
            alt={product.name}
            className="mb-2 h-48 w-full object-cover"
          />
          <h3 className="font-semibold">{product.name}</h3>
          <p className="text-gray-600">${product.price.toFixed(2)}</p>
          <button
            onClick={() => onAddToCart(product.id)}
            className="mt-2 rounded bg-blue-600 px-4 py-2 text-white"
          >
            Add to Cart
          </button>
        </div>
      ))}
    </div>
  );
}
```

## Good

```tsx
interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
}

const ProductCard = memo(function ProductCard({ product, onAddToCart }: {
  product: Product;
  onAddToCart: (id: string) => void;
}) {
  return (
    <div className="rounded border p-4">
      <img
        src={product.imageUrl}
        alt={product.name}
        className="mb-2 h-48 w-full object-cover"
      />
      <h3 className="font-semibold">{product.name}</h3>
      <p className="text-gray-600">${product.price.toFixed(2)}</p>
      <button
        onClick={() => onAddToCart(product.id)}
        className="mt-2 rounded bg-blue-600 px-4 py-2 text-white"
      >
        Add to Cart
      </button>
    </div>
  );
});

function ProductGrid({ products, onAddToCart }: {
  products: Product[];
  onAddToCart: (id: string) => void;
}) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={onAddToCart}
        />
      ))}
    </div>
  );
}
```

## See Also

- [list-stable-keys](list-stable-keys.md) - Always provide unique, stable keys from entity IDs
