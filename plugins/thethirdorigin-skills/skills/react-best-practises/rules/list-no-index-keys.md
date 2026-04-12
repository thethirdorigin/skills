# list-no-index-keys

> Never use array indices as keys for dynamic lists

## Why It Matters

When you use array indices as keys and the list order changes (via sorting, filtering, or insertion), React sees the same key at the same position and reuses the existing component instance. This means internal state from the old item bleeds into the new item occupying that position.

The result is visually jarring and functionally broken: checkboxes appear checked on the wrong rows, text inputs show values from different records, and animations trigger on items that did not actually change. These bugs are difficult to reproduce because they only surface after specific user interactions that mutate list order.

## Bad

```tsx
interface Contact {
  id: string;
  name: string;
  selected: boolean;
}

function ContactList({ contacts }: { contacts: Contact[] }) {
  const [sortAsc, setSortAsc] = useState(true);

  const sorted = [...contacts].sort((a, b) =>
    sortAsc ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name),
  );

  return (
    <>
      <button onClick={() => setSortAsc((prev) => !prev)}>Toggle Sort</button>
      <ul>
        {sorted.map((contact, index) => (
          // BUG: After re-sorting, checkbox state sticks to the position,
          // not the contact. Checking "Alice" then sorting will show
          // the check on whichever contact lands in position 0.
          <li key={index}>
            <input type="checkbox" />
            {contact.name}
          </li>
        ))}
      </ul>
    </>
  );
}
```

## Good

```tsx
interface Contact {
  id: string;
  name: string;
  selected: boolean;
}

function ContactList({ contacts }: { contacts: Contact[] }) {
  const [sortAsc, setSortAsc] = useState(true);

  const sorted = [...contacts].sort((a, b) =>
    sortAsc ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name),
  );

  return (
    <>
      <button onClick={() => setSortAsc((prev) => !prev)}>Toggle Sort</button>
      <ul>
        {sorted.map((contact) => (
          <li key={contact.id}>
            <input type="checkbox" />
            {contact.name}
          </li>
        ))}
      </ul>
    </>
  );
}
```

## See Also

- [list-stable-keys](list-stable-keys.md) - Always provide unique, stable keys from entity IDs
