# Blog Brush-up Changelog (2026-04-06)

## Synthetic Content Engine (SME) Advanced Integration
Expanded the core functionality of the new Markdown-driven SPA architecture to natively support safe Javascript execution, automated summary generation, and legacy URL preservation.

### [NEW] DOMPurify Interactive Script Bypass (`sme.js`)
- **Widget Execution Engine**: Successfully integrated `Chart.js` and other dynamic HTML/JS widgets directly inside Markdown files.
- **Security Logic Bypass**: Refactored the `DOMPurify` pipeline to intercept and temporarily extract `<script>` blocks prior to HTML sanitization, safely re-injecting them into the DOM post-render. This prevents the security filter from aggressively shredding interactive code payload logic.
- **Markdown Parser Hardening**: Mitigated `marked.js` accidental code-block parsing by establishing strict indentation rules (no 4-space leading indents for injected HTML elements).

### [NEW] Legacy URL Resurrection Router (`404.html`)
- **Fallback Redirection**: Created a smart client-side router operating as the 404 handler to capture requests targeting the now-deleted pre-SPA `.html` files.
- **Automated Mapping**: Auto-redirects old links and bookmarks to the proper universal viewer node (e.g. `[legacy-url].html` -> `article.html?md=[new-category]/[new-name].md`), saving SEO and external inbound links.

### [MODIFY] Operational Automation Guidelines (`SKILL.md`)
- **Super Summary Autogeneration**: Imposed a strict rule mandating the AI to automatically parse uploaded text and auto-generate an executive `## 超要約` segment at the top of all future Markdown notes during translation.
- **Article Version Control Protocol**: Instituted a standard demanding chronological metadata updates (filename + frontmatter dates) and an inline `## 変更履歴` (Changelog) section for any modified or appended legacy article.
- **Glossary Terminology Cross-linking**: Formally integrated the Glossary into the writing workflow. AI is now mandated to dynamically extract complex/technical jargon from article bodies, append them to the system Glossary, and cross-link those terms within the text.

---
## Single Page Application (SPA) Architectural Refactor
Eliminated the 1:1 `.html` file coupling requirement for `.md` notes. Converted the website into a fully Markdown-driven Single Page Application relying on dynamic routing parameters.

### [NEW] Universal Viewer Node (`article.html`)
- **Master Shell**: Created a single `article.html` node at the root to render all blog posts globally.
- **Dynamic Routing**: Extrapolated the SME engine router to ingest URL queries (e.g. `?md=infra/xxxxx.md`).
- **State Emulation**: Intercepts the query parameter string to conditionally parse and auto-assign `active` classes onto relative navigation and sidebar components, seamlessly feigning standalone page behavior.

### [DELETE/MODIFY] Obsolete HTML Mass-Purge
- **Grid Rewrite**: Altered all category grids to redirect to the new syntax `https://fununi222.github.io/website/article.html?md=category/xxx.md`.
- **Purge**: Deprecated and deleted all `template` stubs and standalone `2026-` HTML shells inside individual category folders.

---

## Global Directory Reorganization & System Glossary
Completed a massive reorganization of the website's structure to enforce a strict 6-category standard, extracted root-level temporary scripts into a dedicated folder, and upgraded the UI vocabulary management system.

### [NEW/MODIFY] Category Engine Restructuring
- **Directories Reorganized**: Replaced legacy folders and explicitly created `infra`, `dev`, `ai`, `finance`, `lpo`, and `other` directories to group content correctly.
- **`other/` Category Added**: Created an explicitly defined fallback category for notes and research that do not fit standard categories.
- **Global Navigation & Sidebar Updates**: All HTML pages (`index.html`, `ai/index.html`, etc.) were patched to align with the new 6 categories, linking to their respective `index.html` grids.
- **Article Location Migrated**: Relocated DevOps/Web development articles into their correct new paths (e.g., `dev` and `ai`). Rebuilt visual grids inside all index folders dynamically via Python scripting.

### [NEW/MODIFY] Dynamic Glossary Dashboard
- **Directory Migration**: Moved `glossary.html` to `glossary/index.html` and `glossary.md` to `glossary/2026-04-06-system-glossary.md`. Fixed global absolute paths.
- **Markdown Table Architecture**: Converted the generic glossary Markdown layout into a robust `| 用語 | カテゴリ | 概要 |` Markdown table.
- **Interactive UI (VanillaJS)**: Embedded a highly responsive script in `glossary/index.html` triggered by `sme-loaded` that converts the static generated table into a dynamic component, providing **instant column sorting** and **incremental search filtering** directly in the browser shell.

### [DELETE/MOVE] Root Cleanup
- Swept the root directory mapping and relocated temporary Python automation scripts (`fix.py`, `rearrange.py`, `patch_other.py`, `move_glossary.py`) to a new `scripts/` folder to maintain pure root visibility.

---

# Blog Brush-up Changelog (2026-04-05)## SME Migration & Global Cleanup
Fully migrated the research portal to the Synthetic Content Engine (SME) architecture. Extracted all legacy HTML content into Markdown and cleaned up redundant styles by creating centralized shared assets. Resolved dynamic rendering issues involving Markdown, Meramaid.js, and Prism.js.

### [NEW/MODIFY] SME Framework Enhancement (`assets/js/sme.js`)
- **Frontmatter Parsing**: Engine now dynamically extracts titles and metadata from Markdown YAML frontmatter.
- **Library Integration**: Added automatic initialization and rendering for Mermaid.js diagrams and Prism.js syntax highlighting post-content injection.
- **Event Dispatcher**: Triggering `sme-loaded` CustomEvent after processing for ad-hoc script execution (e.g., Chart.js).
- **Bug Fix**: Resolved `ReferenceError: metadata is not defined` crash.

### [NEW] Shared Assets Extraction
- **`assets/js/tw-config.js`**: Extracted duplicate inline Tailwind CSS configuration from all article HTML stubs.
- **`assets/css/synthetic.css`**: Extracted duplicate inline CSS styles (like `.mesh-gradient`, `#sme-content` styles) from all article HTML stubs.
- **`assets/archive/style.css.bak`**: Archived the obsolete global `style.css`.

### [MODIFY] Article Migration & Cleanup (All `ai/`, `it/`, `points/` & `glossary.html`)
- **Markdown Conversion**: Extracted hardcoded HTML content into clean `.md` files.
- **Stub Refactoring**: Replaced legacy HTML structure with lightweight SME stubs referencing the unified `tw-config.js` and `synthetic.css`.
- **Library Restoration**: Ensured all stubs correctly load `prism.min.js` and `mermaid.min.js` to fix rendering bugs.

---

# Blog Brush-up Changelog (2026-04-03)

## Overview
Based on the guidelines in `SKILL.md`, the FunUni-lab blog has been updated to a premium, monochrome, VS Code-inspired dark theme.

## Modifications

### [MODIFY] [style.css](file:///c:/Users/fumiy/.openclaw/workspace/website/style.css)
- **Theme Shift**: Transitioned from a colorful gradient theme to a strict "Dark Modern" monochrome palette (`#0d0f14` background).
- **Editor Aesthetics**:
    - Added a subtle grid background pattern.
    - Implemented "Syntax Highlighting" utility classes (`.syntax-keyword`, `.syntax-string`, `.syntax-comment`, etc.).
    - Added decorative "Editor Tabs" to cards using pseudo-elements.
    - Added a mock "Line Number" sidebar to article content blocks.
- **Glassmorphism**: Enhanced `backdrop-filter: blur(20px)` and semi-transparent borders for all containers.
- **Typography**: switched headers to `JetBrains Mono` for a coding environment feel.

### [MODIFY] [index.html](file:///c:/Users/fumiy/.openclaw/workspace/website/index.html)
- Updated titles to use "coding" notation (e.g., `FunUni-lab`).
- Applied monochrome styling and removed legacy inline gradients.
- Updated the featured post to the latest article.

### [FIX] [2026-04-03-operation-automation.html](file:///c:/Users/fumiy/.openclaw/workspace/website/it/2026-04-03-operation-automation.html)
- **Syntax Fix**: Added missing `<head>`, `<meta>`, and `<link>` tags.
- **Styling**: Wrapped content in `.article-content` and added syntax highlighting spans to technical terms (`vSphere`, `philosophy`, etc.).
- **Consistency**: Applied the same fixes to the version inside the `it/` directory.

## Re-use Guidelines
- When adding new articles, wrap the main content in `<main class="article-content animate-in">`.
- Use `<span class="syntax-keyword">`, `<span class="syntax-string">`, etc. to highlight technical terms in prose.
- Ensure the character set and viewport meta tags are present for proper rendering.
