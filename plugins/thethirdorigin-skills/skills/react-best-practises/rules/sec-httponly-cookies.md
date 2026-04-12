# sec-httponly-cookies

> Use HttpOnly cookies for auth tokens instead of localStorage

## Why It Matters

Any JavaScript running on your page can read `localStorage`, including scripts injected through XSS vulnerabilities, compromised third-party libraries, or malicious browser extensions. A single XSS exploit gives an attacker full access to every token stored in `localStorage`.

HttpOnly cookies cannot be read or modified by client-side JavaScript. The browser automatically attaches them to requests, and the `Secure` flag ensures they are only sent over HTTPS. Combined with `SameSite=Strict`, they also defend against cross-site request forgery. This makes HttpOnly cookies the strongest default for storing authentication tokens in browser applications.

## Bad

```tsx
// Login handler stores JWT in localStorage — accessible to any script on the page
async function handleLogin(credentials: { email: string; password: string }) {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  const { token } = await response.json();
  localStorage.setItem("authToken", token); // Vulnerable to XSS
}

// Every API call manually attaches the token
async function fetchUserProfile() {
  const token = localStorage.getItem("authToken");
  return fetch("/api/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
```

## Good

```tsx
// Login handler — server sets an HttpOnly cookie in the response
async function handleLogin(credentials: { email: string; password: string }) {
  await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include", // Tells the browser to accept and send cookies
    body: JSON.stringify(credentials),
  });
  // No token handling on the client — the cookie is managed by the browser
}

// API calls include cookies automatically
async function fetchUserProfile() {
  return fetch("/api/me", {
    credentials: "include",
  });
}

// Server sets the cookie (Express example)
app.post("/api/auth/login", async (req, res) => {
  const user = await authenticate(req.body);
  const token = generateJWT(user);

  res.cookie("session", token, {
    httpOnly: true,   // Not accessible via document.cookie
    secure: true,     // HTTPS only
    sameSite: "strict", // No cross-site sending
    maxAge: 60 * 60 * 1000, // 1 hour
    path: "/",
  });

  res.json({ user: { id: user.id, name: user.name } });
});
```

## See Also

- [sec-no-client-secrets](sec-no-client-secrets.md) - Keep secrets, API keys, and tokens out of client-side code
