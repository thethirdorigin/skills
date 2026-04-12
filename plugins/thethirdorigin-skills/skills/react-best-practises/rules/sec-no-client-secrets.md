# sec-no-client-secrets

> Keep secrets, API keys, and tokens out of client-side code

## Why It Matters

Every line of JavaScript shipped to the browser is visible to anyone who opens DevTools or inspects the bundle. Environment variables prefixed with `REACT_APP_`, `NEXT_PUBLIC_`, or `VITE_` are embedded directly in the build output as plain strings. Obfuscation and minification do not hide them — a simple search through the bundle or network tab reveals them instantly.

Once a secret is exposed, attackers can make API calls at your expense, access paid services under your account, or exfiltrate data from third-party integrations. The only safe approach is to keep secrets on the server and let the frontend communicate through your own backend, which acts as a proxy and adds authentication and rate limiting.

## Bad

```tsx
// .env
REACT_APP_STRIPE_SECRET_KEY=sk_live_abc123...
REACT_APP_OPENAI_API_KEY=sk-def456...

// src/api.ts — these values are baked into the JS bundle
const stripe = new Stripe(process.env.REACT_APP_STRIPE_SECRET_KEY!);

async function generateText(prompt: string) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      // Anyone can extract this key from the bundle
      Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
    }),
  });
  return response.json();
}
```

## Good

```tsx
// Frontend calls your own backend — no secrets in the browser
async function generateText(prompt: string) {
  const response = await fetch("/api/ai/generate", {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error("Generation failed");
  }

  return response.json();
}

// Backend holds the secret and enforces access control
// server/routes/ai.ts
import { openai } from "../lib/openai"; // Initialised with server-only env var

app.post("/api/ai/generate", requireAuth, rateLimit, async (req, res) => {
  const { prompt } = req.body;

  const completion = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: prompt }],
  });

  res.json({ text: completion.choices[0].message.content });
});
```

## See Also

- [sec-httponly-cookies](sec-httponly-cookies.md) - Use HttpOnly cookies for auth tokens instead of localStorage
