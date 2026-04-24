---
title: "webMethodsのHTTP 502エラー完全ガイド：原因と標準リトライの実装手順"
date: "2026-04-24"
category: "infra"
description: "Integration Serverでの502エラー検知から、throwExceptionForRetryを用いた標準リトライの実装、メモリリークを防ぐ設定まで徹底解説。"
themes: ["dev:webmethods", "infra:api", "error-handling"]
---

# webMethodsのHTTP 502エラー完全ガイド：原因と標準リトライの実装手順

外部APIとの連携中、突然発生する「[HTTP 502 Bad Gateway](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="502%20Bad%20Gateway")」。
システム連携を担当するエンジニアであれば、一度は頭を抱えたことがあるのではないでしょうか。

「とりあえず再実行すれば直るけど、毎回手動で対応するのは限界…」
「webMethodsで自動リトライさせたいけど、正しいやり方がわからない」

この記事では、[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods") [Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server")（IS）において、502エラーを正確に検知し、標準機能を使って安全に自動リトライさせる手順を初心者にもわかりやすく解説します。

この記事を読めば、一時的な通信エラーによる夜間の障害対応から解放されます！

## なぜHTTP 502エラーにリトライが有効なのか？

結論から言うと、**[HTTP 502エラー](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="502%20Bad%20Gateway")は「リトライすれば解決する可能性が高い一時的なエラー」**です。

502エラーは、クライアント側のミス（400番台）でも、処理のバグ（500）でもありません。中継地点のゲートウェイが、裏側のサーバーから正しい応答を受け取れなかったことを示します。原因の多くは「一時的な過負荷」や「サーバーの再起動中」です。

そのため、少し待ってから再リクエスト（リトライ）を送る戦略が非常に有効なのです。

## ステップ1：TRY-CATCHブロックでエラーを捕捉する

webMethodsで外部APIを呼び出す際（`pub.client:http`など）、まずはエラーを安全にキャッチする仕組みが必要です。

[Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server") 10.3以降では、専用の「TRY」「CATCH」「FINALLY」ステップが導入され、より直感的にエラー処理を記述できるようになりました。

1. **TRYステップ**: 外部APIを呼び出す処理を配置します。
2. **CATCHステップ**: エラーが発生した場合にのみ実行されます。ここでエラー内容を解析します。

## ステップ2：502エラーを正確に見極める

CATCHブロックに入ったら、発生したエラーが本当に502なのかを確認します。
使用するのは `pub.flow:getLastError` サービスです。

- **チェックする項目**: `lastError/header/status` の値が「502」であるかを検証します。
- **重要ポイント**: 400（不正なリクエスト）や404（見つからない）の場合はリトライしても無駄なので、そのままエラーとして処理を終了させます。

⚠️ **プロの注意点：メモリリークを防ぐ設定**
`pub.flow:getLastError` をループ内で何度も呼び出すと、エラー情報がパイプラインに蓄積し、最悪の場合サーバーがメモリ不足（OOM）でクラッシュします。
必ずISの管理者設定で `watt.server.getLastError.removeLastError` を `true` に設定しておきましょう。

## ステップ3：組み込み機能でリトライを実行する

502エラーであることが確認できたら、いよいよリトライです。
webMethodsには、非常に便利な組み込みサービスが用意されています。それが `pub.flow:throwExceptionForRetry` です。

### throwExceptionForRetryの働き
このサービスを呼び出すと、エラーが「一時的エラー（ISRuntimeException）」としてパッケージ化され、[Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server")の基盤システムが**「入力データを元に、サービス全体を自動的に再実行」**してくれます。

- **メリット**: 自分で複雑なループ処理を書く必要がなく、設定画面（トリガープロパティなど）から「最大リトライ回数」や「待機時間」を簡単に指定できます 。
- **デメリット**: 「トップレベルのサービス」または「トリガーから起動されたサービス」でしか機能しません。子サービス（ネストされたサービス）の中で呼んでも無効になるので注意が必要です 。

## 次のステップ：固定待機時間の限界

標準機能は簡単で強力ですが、「待機時間が常に固定（例：毎回5秒後）」という弱点があります。
一斉にリトライが走ると、復旧しかけた相手サーバーを再びダウンさせてしまう危険性があります。

これを防ぐための高度なテクニック「[指数バックオフ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="指数バックオフ")」の実装については、次の記事で詳しく解説します。

👉 **[【実践編】REPEATステップと指数バックオフで作る最強のリトライ処理へ](https://fununi222.github.io/website/html/infra/webmethods-exponential-backoff-repeat.html)**

## 変更履歴 (Changelog)
- **2026-04-24**: webMethods Integration ServerにおけるHTTP 502エラーハンドリングの基礎ガイドを新規作成。



