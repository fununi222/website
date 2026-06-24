# Content Architecture Reference

Use this reference when a task touches SME-driven article rendering, embedded interactivity, or content loading behavior.

## SME Overview

- `assets/js/sme.js` loads Markdown based on `?md=category/file.md`.
- It extracts YAML frontmatter metadata.
- It infers the active category from the URL.
- It emits `sme-loaded` after content insertion completes.

## Current Runtime Stack

- `Marked.js`
- `DOMPurify`
- `Prism.js`
- `Mermaid.js`
- `Chart.js`

## Required Rules for Raw HTML in Markdown

1. Keep HTML tags flush-left. Leading indentation of four or more spaces can turn HTML into a code block.
2. Delay DOM-dependent interactive initialization by at least 300ms after injection.
3. Keep page-specific data and logic scoped instead of leaking globals.
4. Preserve or improve fallback behavior for missing or broken Markdown targets.

## Interactive Pattern

Use a delayed initializer such as:

```js
setTimeout(() => {
  initCharts();
}, 300);
```

Apply the same pattern to tabs, calculators, accordions, or any code that expects injected nodes to exist.
