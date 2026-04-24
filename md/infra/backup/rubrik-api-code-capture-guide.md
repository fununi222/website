---
title: "APIドキュメントはもう読まない｜Rubrik Code Captureで実現する『ポチポチ自動化』"
date: "2026-04-24"
category: "infra"
description: "ブラウザの操作をそのままAPIコードに変換。Rubrik API Code Captureを使い、プログラミング未経験から数分で自動化スクリプトを生成する裏技を公開。"
themes: ["infra:rubrik", "dev:api", "ops:automation"]
---

# APIドキュメントはもう読まない｜Rubrik Code Captureで実現する『ポチポチ自動化』

<figure class="mb-10 max-w-4xl mx-auto cyber-glow">
  <img src="../../../assets/img/infra/rubrik-api-code-capture.png" alt="Rubrik API Code Capture Workflow" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

「API自動化は便利そうだけど、英語のマニュアルを読み込む時間がない……」
「管理画面でやっているこの操作、APIではどう書けばいいのか全くわからない」

多くのインフラエンジニアが抱えるこの悩み、実は**「画面をポチポチ操作するだけ」**で解決できます。Rubrikが提供する「[API Code Capture](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Code%20Capture")」を使えば、あなたのブラウザ操作は、その瞬間に実用的なPythonやPowerShellのコードへと変換されます。

本記事では、自動化の学習コストをゼロにする「Code Capture」の破壊的な活用術を伝授します。

---

## 1. Rubrik API Code Captureとは？

Google Chromeの拡張機能として提供されている、API自動化の「録画装置」です。

*   **機能**: あなたがRubrikの管理画面で行うクリックや入力を監視し、裏側で実行された[GraphQL](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="GraphQL")や[REST API](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="REST%20API")のクエリをリアルタイムで生成します。
*   **価値**: 「どのエンドポイントを叩くか」「どんなJSONを送るか」を調べる必要が一切なくなります。答えは常に、目の前の画面にあります。

---

## 2. 爆速開発の3ステップ：UIからコードへ

マニュアルを開く前に、以下の手順を実行してください。

### STEP 1：拡張機能の起動
Chromeウェブストアから[インストール](#)し、有効化します。Rubrikの管理画面を開くと、アイコンがアクティブになります。

### STEP 2：GUIでの「模範演技」
自動化したい操作（例：スナップショットの取得、特定レポートの表示、ユーザーの追加）を、ブラウザ上で丁寧に行います。

### STEP 3：コードの抽出と転写
拡張機能のパネルを開くと、実行されたAPIリクエストが一覧表示されます。
*   **Python / PowerShell / cURL** など、好みの形式を選択してコピー。
*   あとは自分のスクリプトファイルに貼り付けるだけで、自動化の「核」が完成します。

---

## 3. 【プロの知恵】キャプチャ後の「仕上げ」が資産を作る

キャプチャしたコードをそのまま動かすのも良いですが、さらに価値を高めるためのTipsです。

1.  **IDの変数化**: `vm_id` などの固有名詞を、ループ処理や引数で渡せるように書き換えます。
2.  **Postmanでの検証**: 複雑なクエリの場合、一度「Postman」などのツールで挙動をテストし、レスポンスの構造を把握すると開発がスムーズです。
3.  **AIエージェントへの投入**: キャプチャしたコードを[Cursor](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Cursor")などのAIに渡し、「このAPIを使って、エラーハンドリング付きの自動化ツールを作って」と指示。これで、プロ級のツールが数分で手に入ります。

---

## 4. まとめ：『UIで学び、コードで動かす』

API自動化は、もはや特別なスキルではありません。「Code Capture」を使えば、管理画面を使えるすべてのエンジニアが、自動化のスタートラインに立てます。

1.  **マニュアルを閉じる**: 画面上の操作から「生きたコード」を盗む。
2.  **操作をコード化する**: UIの知識を、スクリプトという永続的な資産に変える。
3.  **人間を解放する**: 単純な画面操作をAIやスクリプトに丸投げし、あなたはより高度なアーキテクチャ設計に集中する。

さあ、今すぐお気に入りの操作を「録画」して、自動化の第一歩を踏み出しましょう。

👉 **[次に読む：APIを統合し、運用の『自律化』を実現するSOAR連携戦略はこちら](https://fununi222.github.io/website/html/infra/backup/rubrik-graphql-xsoar-automation.html)**

## 変更履歴 (Changelog)
- **2026-04-24**: 「SEOトップ1%戦略」に基づき全面リライト。ブラウザ操作からのコード生成手順を具体化し、AI支援型開発（Cursor連携等）による「爆速開発フロー」の概念を導入。
- **2026-04-18**: 新規作成。

