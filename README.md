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

### 2. インデックス同期処理の実行
記事の作成・修正を行った後、以下のコマンドを実行して記事インデックスを更新します。
```bash
python scripts/generate_ogp_proxies.py
```
このコマンドにより以下が自動更新されます：
- `assets/data/article_index.json`
- `assets/js/article-data.js`
- `assets/js/skill-data.js`

---

## GitHub Actions 自動化

GitHub の `main` ブランチにプッシュが発生すると、GitHub Actions ワークフロー (`.github/workflows/generate-ogp.yml`) が自動的に起動し、インデックスやスキルデータを最新状態に同期して GitHub Pages へデプロイします。