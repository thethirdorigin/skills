# sec-no-inner-html

> Sanitise content before using dangerouslySetInnerHTML with DOMPurify

## Why It Matters

React escapes string content by default, which prevents most XSS attacks. However, `dangerouslySetInnerHTML` bypasses this protection entirely and injects raw HTML into the DOM. If that HTML originates from user input, a database field, or any external source, an attacker can embed `<script>` tags, event handlers, or other malicious payloads that execute in the context of your application.

Sanitising with a battle-tested library like DOMPurify strips dangerous elements and attributes while preserving safe formatting. This gives you the ability to render rich content without opening a direct path to cross-site scripting.

## Bad

```tsx
interface CommentProps {
  body: string; // User-submitted HTML from a rich text editor
}

function Comment({ body }: CommentProps) {
  // Directly injecting user-controlled HTML — any <script>, <img onerror>,
  // or <a href="javascript:..."> in the body will execute.
  return <div dangerouslySetInnerHTML={{ __html: body }} />;
}
```

## Good

```tsx
import DOMPurify from "dompurify";

interface CommentProps {
  body: string;
}

function Comment({ body }: CommentProps) {
  const sanitisedHtml = DOMPurify.sanitize(body, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "ul", "ol", "li", "br"],
    ALLOWED_ATTR: ["href", "target", "rel"],
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitisedHtml }} />;
}
```

## See Also

- [sec-validate-input](sec-validate-input.md) - Validate user input on both client and server
