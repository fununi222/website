# Editorial Operations Reference

Use this reference when a task creates, updates, reorganizes, or audits article content.

## Direct Static HTML Authoring Policy

FunUni-lab adopts **Direct Static HTML Authoring** for new articles:
- Articles are created as standalone HTML files (`category/sub/article.html`).
- Zero-overhead static delivery, complete SEO/OGP integration, and rich UI styling via Tailwind CSS.

## Category Rules

Assign each article to one top-level category only:

1. `infra/`: server buildout, OS settings, monitoring, automation, infrastructure operations
2. `dev/`: frontend, backend, implementation design, system architecture
3. `ai/`: LLM evaluation, agents, prompting, AI automation
4. `finance/`: finance, payments, points ecosystems
5. `lpo/`: landing-page analytics and conversion optimization
6. `other/`: uncategorized research notes, tests, travel, or lifestyle content
7. `youtube/`: YouTube analytics, video strategy, creator research

## Article Structure & Design Components

- **Reader-First Architecture**: 読み手に寄り添い、過度な装飾や不要な煽りを排した洗練されたレイアウト。
  - **Global Navigation**: Header with domain links.
  - **Breadcrumbs**: Clear hierarchical path (`Home / Category / Title`).
  - **概要（Summary）**: 記事の冒頭に、読者が知りたい要点を簡潔にまとめたアクセントカードを設置。
  - **見出しと構成**: H2, H3の階層を整理し、表（`.table-wrap`）や箇条書きを用いて要点をスッキリ伝える。
  - **Author/Insight Callouts**: 著者の鑑賞メモ、注意点、補足情報などのリッチボックス（`.callout-memo`, `.callout-alert`）。
  - **Changelog**: 末尾に `変更履歴 (Changelog)` を記載。

## Title & Writing Style

- **Natural & Descriptive**: 過度な煽り語（「最強」「神コスパ」「究極」「完全攻略」「裏ワザ」等）は使わず、読者に内容が素直に伝わる自然なタイトル。
- Prefer `対象名 | 主題` or `テーマ名 2026 | 主張・論点`.
- Avoid clickbait, hype words, or aggressive marketing tones.

## Publishing & Listing Updates

- When adding or updating an article:
  1. Ensure the article is saved in its respective category directory (e.g., `other/travel/my-article.html`).
  2. Register or sync the article metadata in `assets/data/article_index.json` and `assets/js/article-data.js`.
  3. Verify that the relevant category index (e.g., `other/index.html`) correctly lists the new entry.