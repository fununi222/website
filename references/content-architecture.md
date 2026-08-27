# Content Architecture Reference

Use this reference when a task creates, updates, or maintains articles and interactive pages on FunUni-lab.

## Architecture Evolution: Direct Static HTML

FunUni-lab utilizes a **Direct Static HTML Architecture** powered by AI authoring:

1. **Direct HTML Articles (`category/sub/article.html`)**:
   - AI authors output fully-styled, standalone HTML articles directly.
   - Zero-runtime overhead (no client-side Markdown parsing required).
   - Built-in SEO/OGP meta tags and structured semantics out-of-the-box.
   - High performance with 0ms First Contentful Paint.

2. **Legacy / Hybrid Support**:
   - Existing Markdown articles in `md/` and viewer `article.html` (`sme.js`) remain accessible for historical archives.
   - New articles should be authored as direct static HTML.

## Article Tech Stack

- **Styling**: Tailwind CSS CDN + Synthetic Design System (`assets/css/synthetic.css`)
- **Typography**: Inter, Space Grotesk, Noto Sans JP
- **Icons**: Google Material Symbols Outlined
- **Interactive / Data Visualization**: Chart.js, MathJax, Mermaid.js (as needed)

## Required Rules for Direct HTML Articles

1. **Design Consistency**:
   - Dark Obsidian theme (`#0a0c14`), glassmorphism cards (`.glass-card`), and glowing accents.
   - Global navigation header with correct relative path to `index.html` and domain indices.
   - Breadcrumbs navigation at the top of the article.
   - Standard Summary Box (`概要（Summary）`) in an accented glass card.
   - Changelog (`変更履歴 (Changelog)`) at the end of the article.
2. **SEO & OGP**:
   - `<title>`, `<meta name="description">`, OpenGraph tags, and Twitter Cards must be present in `<head>`.
3. **Table & Code Styling**:
   - Tables must be wrapped in `<div class="table-wrap">` for mobile responsiveness.
4. **Scoped Scripts**:
   - Keep page-specific interactive logic modular and scoped to prevent global namespace pollution.