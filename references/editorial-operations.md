# Editorial Operations Reference

Use this reference when a task creates, updates, reorganizes, or audits article content.

## Category Rules

Assign each article to one top-level category only:

1. `infra/`: server buildout, OS settings, monitoring, automation, infrastructure operations
2. `dev/`: frontend, backend, implementation design, system architecture
3. `ai/`: LLM evaluation, agents, prompting, AI automation
4. `finance/`: finance, payments, points ecosystems
5. `lpo/`: landing-page analytics and conversion optimization
6. `other/`: uncategorized research notes, tests, or miscellaneous content

## Theme Keys

- Store 1 to 3 `themes` values in frontmatter.
- Prefer managed namespaced keys in the form `domain:topic`.
- Reuse existing keys before inventing new ones.

### Initial Theme Vocabulary

- `infra:` `backup`, `security`, `network`, `observability`, `automation`, `virtualization`, `cloud`, `storage`, `cmdb`
- `dev:` `frontend`, `backend`, `architecture`, `testing`, `performance`, `dx`
- `ai:` `agents`, `llm`, `prompting`, `automation`, `evaluation`, `ops`
- `finance:` `payments`, `points`, `cards`, `miles`, `investing`
- `lpo:` `analytics`, `cro`, `landing-page`, `heatmap`, `experiments`
- `other:` `research`, `memo`, `workflow`

## Article Format

- **Hybrid Architecture**: Balance the "WOW" factor with simplicity.
  - **Premium Components**: Use rich HTML/Tailwind for the `## 超要約` (Summary) and key visuals (e.g., `
    ```

- Add a visible last-updated marker below the summary when updating an article.
- Add a `## 変更履歴 (Changelog)` section at the end when revising content.

## Title Style

- Prefer `対象名 | 主題`.
- Or use `テーマ名 2026 | 主張・論点`.
- Avoid inconsistent tone or vague titles.

## Glossary Sync

- Source of truth: `glossary/system-glossary.md`
- Add difficult technical terms, specialist vocabulary, and uncommon kanji when they first matter to readers.
- **Required Link Format**: Use the following "Scroll to Text Fragment" syntax via the main loader:
  - `[用語名](/https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="用語名")`
- Add glossary links in normal body text only.
- Do not add glossary links inside headings, code, or raw HTML tags.

## Article Listing Updates

- When publishing a new article, add its card entry to:
  1. The relevant category `index.html` (e.g., `infra/index.html`).
  2. The Home page "Latest Research Logs" section (`index.html#latest-logs`) if it represents a major recent research log.
- Keep card wording aligned with the article title, summary, and assigned category.

## Technical Log Policy

- Store infra incident reports and operational postmortems as standalone Markdown files under `infra/`.
- Include the event, root cause, corrective action, and prevention or automation follow-up.

## Maintenance Expectations

- When re-categorizing, update related links, card copy, related-article paths, and glossary references together.
- Filenames should be descriptive and date-less to ensure consistent internal linking.
- Remove obsolete HTML stubs (like the former `glossary/index.html`) only after confirming nothing still links to them.

