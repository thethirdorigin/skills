# sec-validate-input

> Validate user input on both client and server

## Why It Matters

Client-side validation provides immediate feedback and a better user experience, but it offers zero security. Any determined user can bypass it by disabling JavaScript, modifying the DOM, or sending requests directly with curl or Postman. The server is the only trustworthy enforcement point.

Defining validation schemas with a library like Zod or Yup allows you to share the same rules between client and server. The client validates for UX; the server validates for security. Skipping either side means you either frustrate users with slow round-trip errors or leave your API open to malformed and malicious payloads.

## Bad

```tsx
// Client-only validation — server trusts whatever arrives
function RegistrationForm() {
  const [email, setEmail] = useState("");

  const handleSubmit = async () => {
    if (!email.includes("@")) {
      alert("Invalid email");
      return;
    }
    // Server handler trusts req.body without validation
    await fetch("/api/register", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  };

  return <input value={email} onChange={(e) => setEmail(e.target.value)} />;
}

// Server — no validation at all
app.post("/api/register", (req, res) => {
  const { email } = req.body; // Could be anything: object, array, script tag
  db.users.create({ email });
  res.json({ ok: true });
});
```

## Good

```tsx
import { z } from "zod";

// Shared schema — single source of truth
const registrationSchema = z.object({
  email: z.string().email("Enter a valid email address"),
  name: z.string().min(1, "Name is required").max(200),
});

type RegistrationData = z.infer<typeof registrationSchema>;

// Client — validates for UX
function RegistrationForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (formData: FormData) => {
    const result = registrationSchema.safeParse(Object.fromEntries(formData));

    if (!result.success) {
      setErrors(
        Object.fromEntries(
          result.error.issues.map((issue) => [issue.path[0], issue.message]),
        ),
      );
      return;
    }

    await fetch("/api/register", {
      method: "POST",
      body: JSON.stringify(result.data),
    });
  };

  return (
    <form action={handleSubmit}>
      <input name="email" type="email" />
      {errors.email && <span role="alert">{errors.email}</span>}
      <input name="name" type="text" />
      {errors.name && <span role="alert">{errors.name}</span>}
      <button type="submit">Register</button>
    </form>
  );
}

// Server — validates for security
app.post("/api/register", (req, res) => {
  const result = registrationSchema.safeParse(req.body);

  if (!result.success) {
    return res.status(400).json({ errors: result.error.flatten() });
  }

  db.users.create(result.data);
  res.json({ ok: true });
});
```

## See Also

- [sec-sanitise-urls](sec-sanitise-urls.md) - Sanitise URL parameters before using in queries or rendering
