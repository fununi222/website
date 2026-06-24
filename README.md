# FunUni-lab Web Portal

FunUni-lab の技術ブログ・ナレッジ共有用の静的ポータルサイトです。

## 概要

本ポータルは **ハイブリッド・スタティック・アーキテクチャ** を採用しています。
1. **Markdown ソース (`md/`)**: 記事のすべてのデータ実体はここに格納されます。
2. **HTML プロキシ (`html/`)**: SNS等での共有（OGP対応）および検索エンジンのクローリング向けの個別静的ページ群です。アクセス時にメインビューワーである `article.html` へ自動リダイレクトされます。
3. **メインビューワー (`article.html`)**: `sme.js` エンジンを用い、クエリパラメータから Markdown を読み込んで美しくレンダリングします。

## ディレクトリ構成

- `md/` - 各カテゴリの Markdown 原稿
  - `infra/` - インフラ・AIOps・運用設計・監視など
  - `dev/` - フロントエンド・バックエンド・アーキテクチャなど
  - `ai/` - 生成AI・LLM評価・自動化エージェントなど
  - `finance/` - ポイ活・資産保護・金融エンジニアリングなど
  - `lpo/` - LP分析・コンバージョン改善など
  - `other/` - その他ライフスタイル・旅・備忘録
- `html/` - 自動生成される OGP/SNS用 HTML プロキシ
- `assets/` - スタイルシート、ロゴ・画像アセット、データインデックス
- `scripts/` - インフラ管理・パブリッシング用自動化スクリプト群
- `references/` - 設計システム、ライティングスタイル、カテゴリ定義等のガイドライン

---

## 開発・執筆フロー (ローカル実行)

### 1. セットアップ
Python 3 がインストールされていることを確認し、画像圧縮などのスクリプトを使用する場合は依存ライブラリをインストールします。
```bash
pip install -r requirements.txt
```

### 2. 記事の執筆
`md/` フォルダの適切なカテゴリ配下に Markdown ファイル（拡張子 `.md`）を作成し、YAML フロントマターを記述して記事を執筆します。

### 3. パブリッシング処理の実行
記事の作成・修正を行った後、**必ず** 以下のコマンドをプロジェクトルートで実行して OGP プロキシ HTML の生成および記事インデックスを更新します。
```bash
python scripts/generate_ogp_proxies.py
```
このコマンドにより以下が自動生成・更新されます：
- `html/` ディレクトリ内のプロキシファイル群
- `assets/data/article_index.json`
- `assets/js/article-data.js`
- `assets/js/skill-data.js` (SKILL.md からのスキルスコア抽出)

---

## 他環境からの執筆と自動化の仕組み (GitHub Actions)

ローカル環境（PC）以外から GitHub へ直接コミットして記事を追加した場合（GitHub Web UI、Obsidian 自動同期、スマートフォン等）でも、正常にサイトが生成されるように自動化を導入しています。

### 自動ビルド＆プッシュ機構
GitHub の `main` ブランチにプッシュが発生すると、GitHub Actions ワークフロー (`.github/workflows/generate-ogp.yml`) が自動的に起動します。
1. プッシュされた Markdown ファイルを検出
2. Python ランタイム上で `python scripts/generate_ogp_proxies.py` を実行
3. 更新された `html/` プロキシやインデックスファイルを、GitHub Actions 側からリポジトリへ**自動的にコミット＆プッシュ**

これにより、どの環境から Markdown を書いてプッシュしても、自動的にインデックスが更新されて本番の GitHub Pages へ反映されるため、手動ビルドなしで作業を続けることができます。
