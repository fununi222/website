---
title: "webMethods実践：REPEATステップと指数バックオフで作る最強のリトライ処理"
date: "2026-04-24"
category: "infra"
description: "Thundering Herd問題を回避するための指数バックオフ実装術。REPEATステップの使い方とパイプラインロールバックの注意点を詳解。"
themes: ["dev:webmethods", "ops:resilience", "backoff-strategy"]
---

# webMethods実践：REPEATステップと指数バックオフで作る最強のリトライ処理

前回の記事では、[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods")の標準機能を使った簡単なリトライ手法を解説しました。
しかし、トラフィックが多い本番環境では、標準機能の「固定間隔のリトライ」は致命的なシステム障害を引き起こす危険性を持っています。

「相手のサーバーを二次災害（リトライの集中攻撃）から守りたい」
「より柔軟でプロフェッショナルなリトライ制御を実装したい」

この記事では、中〜上級者向けに、**「REPEATステップ」と「[指数バックオフ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="指数バックオフ")（Exponential Backoff）」**を用いた、エンタープライズ水準の自律的リトライロジックの実装手順を解説します。

## なぜ「指数バックオフ」が必要なのか？

[HTTP 502エラー](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="502%20Bad%20Gateway")が起きた際、複数のクライアントが「正確に5秒後」に一斉にリトライを行うとどうなるでしょうか？
相手のサーバーにトラフィックのスパイク（急増）が発生し、再びサーバーがダウンします。これは**「Thundering Herd（群衆の暴走）問題」**と呼ばれます。

これを解決するのが[指数バックオフ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="指数バックオフ")です。
1回目のリトライは1秒後、2回目は2秒後、3回目は4秒後…というように、再試行の間隔を指数関数的に伸ばしていく戦略です。

さらに、タイミングが完全に被らないよう、ランダムな揺らぎ（ジッター）を加えるのがベストプラクティスです。

## REPEATステップを活用した実装手順

[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods")のフローサービス内でこれを実現するには、`REPEAT` ステップを使用します 。

### 1. REPEATステップの設定
フローサービスに `REPEAT` ステップを配置し、プロパティを以下のように設定します。

- **Repeat on**: `FAILURE`（失敗した場合に繰り返す）
- **Count**: 最大リトライ回数（例：5回）
- **Repeat interval**: `%waitTime%`（変数を指定することで、動的に待機時間を変更できます）

### 2. 子ステップの構成
`REPEAT` ステップの下に、以下の処理を配置します。

1. **外部API呼び出し**: `pub.client:http` を実行。
2. **成功判定**: 502エラーが起きた場合は、例外をスローして `REPEAT` を失敗させます。
3. **待機時間の計算**: 現在の実行回数から、次回の `%waitTime%` を計算してパイプラインにセットします。

⚠️ **プロの注意点：ロールバックの罠**
`REPEAT` ステップが失敗して次のイテレーション（反復）に移る際、パイプラインの変数は「反復開始時の状態」に自動的にロールバックされます。
しかし、ロールバックされるのは「第一階層の変数（Top-level variables）」のみです 。深い階層のドキュメント（IData内のデータ）に対する変更は元に戻らないため、データ不整合に注意が必要です。

## スレッド枯渇リスクへの対策

`REPEAT` と待機（Sleep）を使ったリトライは強力ですが、待機中は[Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server")のサーバースレッドを占有し続けます。

数分から数十分の長いバックオフループが大量に発生すると、ISの全スレッドが枯渇し、IS自体がダウンしてしまいます。
そのため、この手法は「数秒〜数十秒で解決する一時エラー」に限定し、長時間の障害が疑われる場合は非同期処理（キューへの退避など）に切り替える設計が必須です。

## 次のステップ：システム全体のエラー設計

IS単体でのリトライは完璧でも、その前段に[API Gateway](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="API%20Gateway")が存在する場合、システム全体を揺るがす「[リトライストーム](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="リトライストーム")」の罠が潜んでいます。

👉 **[【応用編】API Gateway連携での罠「リトライストーム」を防ぐ設計術へ](https://fununi222.github.io/website/html/infra/webmethods-retry-storm-gateway.html)**

## 変更履歴 (Changelog)
- **2026-04-24**: REPEATステップと指数バックオフを用いた高度なリトライ実装ガイドを新規作成。



