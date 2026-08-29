# FunUni-lab Web Portal

FunUni-lab の技術ブログ・ナレッジ共有用の静的ポータルサイトです。

## 概要

本ポータルは **Direct Static HTML アーキテクチャ** を採用しています。

1. **Direct Static HTML 記事**: 各カテゴリディレクトリ（`infra/`, `dev/`, `ai/`, `finance/`, `lpo/`, `other/`, `youtube/`, `glossary/`）配下に完全な単体静的 HTML 記事として格納されます。
2. **高速表示 & 完全な SEO/OGP**: クライアントサイドでの JavaScript レンダリング（Markdown パース）待ちがなく、ブラウザで開いた瞬間に 0ms で画面が完全表示されます。
3. **リッチな UI & データ可視化**: Tailwind CSS、Prism.js（シンタックスハイライト）、Mermaid.js（ダイアグラム）、Chart.js（チャート）を直接活用した高度な表現が可能です。

## ディレクトリ構成

- `infra/` - インフラ・AIOps・クラウド・運用設計・監視など
- `dev/` - フロントエンド・バックエンド・アーキテクチャ・AIコーディングなど
- `ai/` - 生成AI・LLM評価・自動化エージェントなど
- `finance/` - ポイ活・資産運用・金融エンジニアリングなど
- `lpo/` - LP分析・コンバージョン改善など
- `other/` - ライフスタイル・聖地巡礼・旅行・グルメなど
- `youtube/` - YouTubeアナリティクス・動画戦略など
- `glossary/` - システム・用語集
- `assets/` - スタイルシート、ロゴ・画像アセット、データインデックス（`article_index.json`, `article-data.js`）
- `scripts/` - インデックス生成・同期スクリプト群
- `references/` - 設計システム、ライティングスタイル、カテゴリ定義等のガイドライン

---

## 記事の執筆とインデックス同期

### 1. 記事の執筆
各カテゴリの適切なサブディレクトリ配下に、標準テンプレートに沿った HTML ファイルを作成します。

### 2. インデックスの同期
記事の作成・修正後は、`assets/data/article_index.json` と `assets/js/article-data.js` に同じ記事メタデータ（title、description、date、updated、category、path、`direct_html: true`）を追加・更新します。記事ファイルは HTML のみで管理し、Markdown 変換や OGP プロキシ生成は行いません。

---

## GitHub Actions 自動化

GitHub の `main` ブランチへのプッシュで、GitHub Pages が直接 HTML の記事・インデックス・アセットを配信します。
