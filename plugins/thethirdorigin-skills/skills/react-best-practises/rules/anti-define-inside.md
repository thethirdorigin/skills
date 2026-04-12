# anti-define-inside

> Never define a component inside another component's body

## Why It Matters

When a component is defined inside another component's render function, React creates a brand new function identity on every render. React uses referential identity to determine whether a component in the tree is the same type as before. A new identity means React unmounts the old instance and mounts a fresh one — destroying all internal state, resetting animations, losing focus, and remounting every child.

This is not a performance optimisation concern — it is a correctness bug. Typing into an input inside an inner component causes the input to lose focus on every keystroke because the component unmounts and remounts between renders.

## Bad

```tsx
// Child defined inside Parent — new identity every render
function Parent() {
  const [count, setCount] = useState(0);

  // This function is recreated on every render of Parent
  function Child() {
    const [text, setText] = useState("");
    return (
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type here..."
      />
    );
  }

  return (
    <div>
      <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>
      {/* Every time count changes, Child unmounts and remounts.
          The input loses focus and text resets to "" */}
      <Child />
    </div>
  );
}
```

## Good

```tsx
// Child defined outside Parent — stable identity across renders
function Child() {
  const [text, setText] = useState("");
  return (
    <input
      value={text}
      onChange={(e) => setText(e.target.value)}
      placeholder="Type here..."
    />
  );
}

function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>
      {/* Child keeps its identity — state, focus, and animations are preserved */}
      <Child />
    </div>
  );
}
```

## See Also

- [comp-functional-only](comp-functional-only.md) - Use function declarations for components
