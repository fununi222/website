# FunUni-lab: Operations & Design Guidelines

このドキュメントは、FunUni-lab ポータルの技術選定、デザインシステム、および運用ロードマップを管理する唯一の公式ドキュメント（SKILL.md）です。

---

## 1. Design System: "Synthetic Edition"

2026年4月に実施されたグローバルデザイン統一（Synthetic Edition）の設計思想です。

### 💎 Glassmorphism & Cyber-Theme
- **コンセプト**: 先進的な「研究室（Lab）」の雰囲気を演出するため、高コントラストなダークモードとガラス質感の UI を採用。
- **実装**: Tailwind CSS をベースに構成。全ページ共通の開発用設定は `assets/js/tw-config.js` に、共通の UI スタイルは `assets/css/synthetic.css` に集約。旧 `style.css` はアーカイブ化済。
- **Color Palette**: 
  - Primary: `#aaa4ff` (Purple)
  - Secondary: `#00d2ff` (Cyan)
  - Background: `#060e20` (Deep Navy)

### ✍️ Typography
- **Headlines**: `Space Grotesk` (幾何学的でフューチャリスティック)
- **Body**: `Inter` / `Noto Sans JP` (高い可読性と透明感)

---

## 2. Content Architecture: SME Engine

Markdown と HTML の二重管理を解消するため、**Synthetic Content Engine (SME)** を導入しています。

### 🚀 SME の仕組み
- **Runtime Loader**: JavaScript (`assets/js/sme.js`) がブラウザ上で URLから指定された `.md` ファイルを動的に取得・パッチします。
- **機能**:
    - URLクエリ `?md=カテゴリ名/ファイル名.md` からコンテンツを動的に取得・描画。
    - Markdown フロントマター（YAML形式）からのタイトルやメタデータの自動抽出・適用。
    - URLから現在地のカテゴリを判定し、ヘッダーとサイドバーのナビゲーションを自動アクティブ化。
    - コンテンツ読み込み完了後の `sme-loaded` イベント発火（UIの初期化や Chart.js 等で利用）。
- **ライブラリ**: `Marked.js` (パース), `DOMPurify` (安全化), `Prism.js` (コードハイライト), `Mermaid.js` (図表描画)。
- **利点**: 単一の `article.html` だけで全カテゴリの記事を表示できる「完全SPA（MD駆動型）」に移行済み。記事ごとのHTMLスタブ作成は一切不要です！

### 📝 記事作成・カテゴライズのルール
新規記事を作成する際は、必ず以下の **6つの定義済みカテゴリ** のいずれかに配置します。

1. **`infra/`** : サーバ構築、OS設定、監視、運用自動化（Terraform/Ansible等）
2. **`dev/`** : フロントエンド・バックエンドの実装設計、システムアーキテクチャ
3. **`ai/`** : LLMの検証、AIエージェント、プロンプト、AIを用いた自動化
4. **`finance/`** : 金融、決済ルート検証、ポイント経済圏
5. **`lpo/`** : LPダッシュボードおよびコンバージョン率最適化関連
6. **`other/`** : 上記のどれにも該当しないテスト、雑記、または未分類の研究ノート

#### 📝 新規記事の追加フローとフォーマット・ルール
1. ユーザーから「ブログ・メモの原稿（テキスト・HTML・MD）」を渡された場合、必ず**標準化された Markdown 形式へと変換・整形**して対応するカテゴリへ配置してください。
2. その際、大見出し（`# タイトル`）の直下には必ず `## 超要約` という見出しを設け、記事の要点を端的にまとめたパラグラフを配置すること。もしユーザーから渡された原稿に超要約が存在しない場合は、**AIが文脈を自動解析し、自ら超要約を生成して付与**してください。
3. **インタラクティブ要素とHTMLの混在ルール**:
   - SMEエンジン（`sme.js`）は、**Markdownファイル内への `<script>` や Chart.js の埋め込み（直接実行）をネイティブにサポート**しています。高度なグラフやタブUIを持たせたい場合は直接MDへ記述して構いません。
   - ただし、Markdownエンジン（Marked.js）の誤判定（コードブロック化）を防ぐため、**MD内にHTMLタグ（`<div...>`等）を記述する際は、行頭のインデント（スペース4つ等）を絶対に付けず、左詰めで記述**してください。
4. **画像の配置とスタイリングのルール**:
   - ユーザーから原稿と一緒に画像が提供された場合、単なるMarkdownの画像記法ではなく、現在のモダンなUIテーマ（ダーク/サイバー）に馴染むように**HTMLの `<figure>` タグとTailwindクラスを用いて美しく配置**してください。
   - 推奨レイアウト例: `<figure class="my-10 max-w-4xl mx-auto cyber-glow"> <img src="..." class="rounded-2xl shadow-xl border border-white/10 hover:border-primary/50 transition-colors"> </figure>`
   - （※AI自身はローカルに画像を保存できない場合があるため、その際は上記のような仮パスでのプレースホルダーを記述して対応します）。
5. （もうHTMLのスタブ作成は不要です！単一の `.md` ファイルを作成するだけで完了します。）
6. 対象カテゴリの `index.html` にある記事一覧グリッド（`div#latest`内等）へ、作成したMDファイルへのリンクを追記します。
   - 例: `<a href="../article.html?md=infra/新しい記事.md">...</a>`
7. **日付と更新履歴の管理ルール**:
   - 新規記事を作成する場合は、必ずファイル名（例: `YYYY-MM-DD-filename.md`）とフロントマター（`date: "YYYY-MM-DD"`）の両方に作成日の日付を付与すること。
   - 過去の類似記事をベースに情報を追加・改定する場合は、上記の日付を**改定日の最新のものに更新**してください（ファイル名も変更すること）。
   - **記事本文中での日付明記**: 記事本文の冒頭（例：大見出しや「超要約」の直下）に、目立たないスタイルで作成・更新日時を配置してください。（推奨例: `<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: YYYY-MM-DD</div>`）
   - さらに、更新した記事の末尾または適切な箇所に `## 変更履歴 (Changelog)` セクションを必ず追記し、簡易的なアップデート内容のログ（例：`- 2026-04-06: 〇〇について最新の知見を元に追記`）を残すこと。

### 📖 System Glossary (用語集) の管理
- **格納場所**: `glossary/2026-04-06-system-glossary.md` 
- **フォーマット**: プレーンな Markdown テーブル (`| 用語・技術名 | カテゴリ | 概要・詳細 |`) を使用して用語を管理します。
- **UI連携**: `glossary/index.html` 側に埋め込まれたスクリプトが、SMEエンジンの `sme-loaded` イベント発火後にこのテーブルをフックし、**動的ソート** および **インクリメンタル検索** が可能な UIコンポーネントへ自動変換します。
- 単語を増やす際は、単純に `.md` 内のテーブル行を追記するだけで反映されます。
---

## 3. Blog Improvement Roadmap (2026)

`BLOG_IMPROVEMENT_PROPOSAL.md` より統合された改善計画です。

### 🏁 優先課題 (Priority 1)
- **SEO 基礎の徹底**: 全記事への `meta description` 導入、OGP / Twitter Card 実装。
- **回遊性の向上**: 記事末尾への「関連記事」「カテゴリ一覧へ戻る」ボタンの自動生成。

### 📅 30日ロードマップ
- **Week 1**: サイト全体のメタ情報・OGP 整備、`sitemap.xml` 生成。
- **Week 2**: 回遊導線（関連記事・新着リスト）の実装。
- **Week 3**: SME エンジンのさらなる拡張（メタデータの MD からの自動抽出など）。
- **Week 4**: Google Analytics / Heatmap による計測と改善サイクル開始。

---

## 4. Technical Logs: Infrastructure & IT

### VMware CBT/CTK 不整合是正
- **重要点**: バックアップ故障を防ぐため、`ChangeTrackingEnabled` のリセットとスナップショットの瞬断によるコミットを自動化。
- ** Jenkins 連携**: 1日1回バックアップ実行前に走査することで、失敗させない能動的運用を実現。

---

## 5. KPIs (Success Metrics)

- **平均滞在時間**: +20%
- **閲覧ページ数/Session**: +30%
- **検索流入比率**: +15%
- **直帰率**: -10%
