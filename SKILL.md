# FunUni-lab Technical Knowledge Management

This skill preserves the authoritative yet accessible voice of the FunUni-lab engineering laboratory. Every entry must reflect the rigorous documentation standards of a **Professional Technical Writer & Senior Systems Architect**, prioritizing clarity, empathy, and practical value over exaggerated claims.

## Strategic Core Domains

The archive is organized into four primary domains to maximize topical relevance and E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness).

1.  **Autonomous Infrastructure**: Focus on AIOps, Self-healing systems (AWS, Rubrik, PagerDuty), and resilient architectural design.
2.  **AI Engineering & Agents**: Focus on next-gen development (OpenAI Codex, Cursor, Claude Code), autonomous agents, and AI-native workflows.
3.  **Finance & Asset Strategy**: Focus on financial engineering (point ecosystems), wealth protection against inflation, and algorithmic asset optimization.
4.  **Strategic Travel & Life**: Focus on high-value travel guides (Niseko Strategy, Es Con Field), and engineering-led lifestyle design (KISS Principle).

### Architecture: Direct Static HTML

The portal uses a **Direct Static HTML Architecture** for native social media compatibility (OGP) without a client-side content renderer.

1.  **Direct HTML Articles**: Each article is a complete HTML document under its category directory and is the source of truth.
2.  **Compatibility Router (`article.html`)**: Legacy Markdown URLs redirect to their matching direct HTML article; it does not render content.
3.  **Dynamic Hub Engine (`archive-loader.js`)**: Processes the JSON index to automatically render category hub pages (`infra/index.html` etc.).

## Content Strategy: Reader-Centric Knowledge Ecosystem

Every article must be treated as a valuable, reader-first resource that clearly solves problems without unnecessary hype or monetization noise.

### 1. Mandatory Execution Standards
1.  **Reader Empathy & Problem Statement**: Start by addressing the reader's genuine question or challenge.
2.  **Objective & Honest Analysis**: Provide practical, verified guidance without sensationalism (avoid: "最強", "神コスパ", "裏ワザ", "完全攻略").
3.  **Structure & Visual Aids**: Use clear headings (H2/H3), comparison tables, and code snippets to maximize readability.
4.  **Internal Link Ecosystem**: Connect cluster articles naturally to guide the reader to relevant follow-up details.
5.  **Clean SEO Titles**: Descriptive, accurate titles (~32 characters) that reflect real search intent without clickbait.
6.  **Changelog**: Conclude every article with a `## 変更履歴 (Changelog)`.

## Asset & Design Standards

- **Aesthetic Excellence**: Use curated color palettes (HSL), smooth gradients, and glassmorphism.
- **Mirrored Asset Structure (Standard)**: To ensure scalability and manageability, image assets MUST mirror the direct HTML article hierarchy.
    - **Article**: `[category]/[subcategory]/[article].html`
    - **Image**: `assets/img/[category]/[subcategory]/[image-name].png`
- **Relative Pathing Strategy**:
    - **Category Level (Depth 3)**: Use `../../../assets/img/[category]/...`
    - **Sub-category Level (Depth 4)**: Use `../../../../assets/img/[category]/[subcategory]/...`
- **Direct article pages**: Include breadcrumbs and internal links directly in each HTML article.

## Terminology & Governance (Nomenclature)

To maintain a professional, high-authority technical archive, all articles must adhere to strict naming conventions. Avoid internal codenames or project-specific jargon that lacks external context.

- **Asset & Ticket Management**: Always use **"Jira"** as the "Source of Truth" for operational workflows and asset lifecycle management. (Avoid: T-UP, internal tracker names).
- **AI Systems**: Use **"AI Knowledge Concierge"** as the professional designation for internal autonomous knowledge engines and RAG-based support systems. (Avoid: Project-A, Project-X).
- **Public-Grade Anonymization**: When documenting internal research logs, prioritize functional descriptions over specific internal project codes to preserve confidentiality while maximizing technical value.

## Verification Checklist (Quality Gate)

- [ ] **Topical Authority**: Does this article strengthen its assigned Strategic Core Domain?
- [ ] **Professional Nomenclature**: Are internal codenames replaced with professional terms (Jira, AI Knowledge Concierge)?
- [ ] **Intent Fulfillment**: Does it outperform top competitors in strategic depth?
- [ ] **Cluster Integrity**: Is it properly linked within its topic cluster ecosystem?
- [ ] **AIOps Integration**: Does it mention automation or AI agents where relevant?
- [ ] **ROI Focus**: Does the reader gain a clear "Strategic Advantage" or "Action"?

## ⚙️ Publishing Workflow (CRITICAL)

Whenever a new HTML article is added, update its metadata in both `assets/data/article_index.json` and `assets/js/article-data.js`. The `archive-loader.js` engine parses this JSON to build the category hub grids without manual card edits.

## Critical Files & Directories

- Direct article directories: `infra/`, `ai/`, `dev/`, `finance/`, `lpo/`, `other/`, `youtube/`, `glossary/`
- `glossary/system-glossary.html` (The Archive's Technical Dictionary)
- `SKILL.md` (This Governance Document)

## 📊 System Optimization Dashboard (LPO)

The following metrics power the "System Optimization Dashboard" radar chart on the portal's homepage. Update these values when you publish new strategic articles or achieve significant engineering milestones.

### 💼 仕事のスキル (Professional)
- **技術適応力**: 95
- **プロジェクト推進力**: 85
- **チーム貢献・SL力**: 75
- **課題解決・改善提案**: 95
- **ドメイン知識**: 85

### 💻 IT・テクニカルスキル (Technical)
- **IaC・構成管理**: 85
- **監視・可観測性**: 85
- **開発力(Frontend/Python)**: 90
- **生成AI・LLM活用**: 85
- **AIエージェント運用**: 85
