# sec-update-deps

> Keep dependencies updated to patch known vulnerabilities

## Why It Matters

Published vulnerabilities in npm packages are catalogued in public databases and targeted by automated scanners within hours of disclosure. If your application depends on a package with a known CVE and you have not updated, you are running code with a publicly documented exploit path. Attackers do not need to discover the vulnerability themselves — they simply scan for applications using the affected version.

Regular dependency auditing and automated update tooling (Dependabot, Renovate) catch these issues before they reach production. The effort to review and merge a dependency update is orders of magnitude smaller than the effort to respond to a breach caused by a known, patched vulnerability.

## Bad

```tsx
// package.json — pinned to old versions, no automated updates
{
  "dependencies": {
    "lodash": "4.17.15",      // Has prototype pollution CVE-2020-8203
    "axios": "0.21.0",        // Has SSRF vulnerability CVE-2021-3749
    "node-fetch": "2.6.0"     // Has regex DoS vulnerability
  }
}

// No audit step in CI pipeline
// No dependabot.yml or renovate.json
// npm audit warnings ignored for months
```

## Good

```tsx
// package.json — uses compatible version ranges, stays current
{
  "dependencies": {
    "lodash": "^4.17.21",
    "axios": "^1.7.2",
    "node-fetch": "^3.3.2"
  }
}

// .github/dependabot.yml — automated PRs for updates
// version: 2
// updates:
//   - package-ecosystem: "npm"
//     directory: "/"
//     schedule:
//       interval: "weekly"
//     open-pull-requests-limit: 10

// CI pipeline includes audit step
// scripts in package.json:
// "audit": "npm audit --audit-level=high",
// "preinstall": "npx check-engine"
```

## See Also
