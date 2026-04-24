---
title: "GUI画面のスクレイピングは時代遅れ？Rubrik API Code Captureの活用法"
date: "2026-04-16"
category: "infra"
description: "GUIの裏側で実行されるAPIを可視化するブラウザ拡張機能「Rubrik API Code Capture」の使い方と、Postmanを用いた検証方法を解説します。"
themes: ["infra:api", "infra:automation", "infra:security"]
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.16</div>

# GUI画面のスクレイピングは時代遅れ？Rubrik API Code Captureの活用法

前回の記事で、「[Rubrik](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Rubrik")のログ抽出にGUI画面のHTMLスクレイピングは不要」とお伝えしました。
（※ログ取得の基礎から振り返りたい方は[こちら](./rubrik-threat-log-extraction.md)）

しかし、こんな不安を感じていませんか？
「APIが便利なのは分かったけど、プログラミングや複雑なマニュアルを読むのは苦手…」

ご安心ください。
Rubrikが公式に提供している強力なツールを使えば、ノーコードでAPIの裏側を覗き見することができます。
この記事では、自動化の救世主「Rubrik API Code Capture」の使い方を3つのステップで分かりやすく解説します。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026年 4月16日</div>

---

## Rubrik API Code Captureとは？

「Rubrik API Code Capture」は、Google Chrome向けの拡張機能です。

このツールの機能は非常にシンプルかつ強力です。
あなたが普段通りRubrikの管理画面（GUI）をポチポチとクリック操作するだけで、**「その操作を行うために裏側で使われたAPIコード」を自動的に録画して表示**してくれます。

つまり、「この画面のログを取得するスクリプトはどう書くの？」という疑問に対する答えを、システム自らがコードで教えてくれるのです。

## API Code Captureの使い方（3ステップ）

使い方は驚くほど簡単です。

### ステップ1：拡張機能のインストール
まずはChromeウェブストアから拡張機能を無料でインストールし、有効化します。

### ステップ2：普段通りGUIを操作する
ブラウザ上でRubrikの画面を開き、取得したい検体の詳細画面や、ログのダウンロード画面まで手動で進みます。
これが「スクレイピングで取りたい」と思っていた画面を表示させる作業です。

### ステップ3：裏側のAPIコードをコピーする
拡張機能のアイコンをクリックすると、たった今あなたが行った操作に対応するAPIのリクエスト（要求）とレスポンス（応答）のコードが綺麗にハイライトされて表示されます。
あとはこれをコピーして、自社のスクリプトツールに貼り付けるだけです。

## Postmanを使った検証のすすめ

コピーしたAPIコードが正しく動くか、いきなり本番環境のスクリプトに組み込むのは不安ですよね。
そんな時は、「Postman」というAPIテストツールを使うのがおすすめです。

コピーした設定をPostmanに貼り付けて実行するだけで、実際にどのようなCSVやJSONのログデータが返ってくるかを安全にテスト・確認することができます。

## メリット・デメリット

**▼ API Code Captureのメリット**
* 分厚いAPIマニュアルを読む時間を100%削減できる。
* 自分が欲しいデータのAPIだけをピンポイントで見つけられる。
* Pythonなどのコードスニペットも簡単に作成できる。

**▼ デメリット**
* Google Chromeブラウザを利用できる環境が必要。

## 具体例（リアルケース）

ある企業では、毎朝SOCアナリストがRubrikの画面にログインし、脅威アラートをCSVで手動ダウンロードしていました。
このツールを使ってダウンロード操作時のAPIをキャプチャし、そのコードを自動実行プログラムに組み込んだ結果、毎朝の単純作業が「ゼロ」になりました。

## FAQ（よくある質問）

**Q. この拡張機能は誰でも無料で使えますか？**
A. はい、Chromeウェブストアから無料でインストールして利用可能です。

**Q. 取得したAPIはPython以外でも使えますか？**
A. はい。API自体は言語に依存しないため、PowerShellやGo言語など、あらゆる環境で利用できます。

## まとめ

* ログ抽出の自動化に迷ったら「Rubrik API Code Capture」を使いましょう。
* GUIの操作をそのままAPIコードに変換してくれるため、マニュアル要らずです。
* Postman等のツールと組み合わせることで、安全にテスト開発が可能です。

APIの取得方法が分かれば、あとは他のシステムと連携させるだけです。
次はいよいよ、SOARツールなどを用いた「完全自動化」の世界へご案内します。

👉 **[Rubrikログ抽出を完全自動化！GraphQLとXSOAR連携による次世代SOC運用](./rubrik-graphql-xsoar-automation.md)**




