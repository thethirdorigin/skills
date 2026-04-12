# name-handler-prefix

> Prefix event handlers with handle, callback props with on

## Why It Matters

The `on`/`handle` convention creates a clear contract between parent and child components. Props prefixed with `on` signal "I accept a callback function." Functions prefixed with `handle` signal "I am the implementation that responds to an event." This pairing mirrors native DOM events (`onClick`, `onSubmit`) and is a widely understood React convention.

Without this convention, it becomes unclear whether a prop is a callback, a data value, or a configuration option. Consistent prefixes make component APIs self-documenting.

## Bad

```tsx
// No prefix — "submit" could be a boolean, a string, or a function
interface FormProps {
  submit: (data: FormData) => void;
  cancel: () => void;
  change: (field: string, value: string) => void;
}

function CreditFacilityForm({ submit, cancel }: FormProps) {
  // "save" does not indicate it handles an event
  const save = () => {
    const data = collectFormData();
    submit(data);
  };

  return (
    <form>
      <button onClick={save}>Save</button>
      <button onClick={cancel}>Cancel</button>
    </form>
  );
}
```

## Good

```tsx
interface CreditFacilityFormProps {
  onSubmit: (data: FormData) => void;
  onCancel: () => void;
  onChange: (field: string, value: string) => void;
}

function CreditFacilityForm({ onSubmit, onCancel, onChange }: CreditFacilityFormProps) {
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const data = collectFormData();
    onSubmit(data);
  };

  const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange("name", event.target.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" onChange={handleNameChange} />
      <button type="submit">Save</button>
      <button type="button" onClick={onCancel}>Cancel</button>
    </form>
  );
}
```

## See Also

- [name-boolean-prefix](name-boolean-prefix.md) - Prefix boolean props and variables with is, has, should, or can
