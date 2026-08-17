---
title: "webMethodsのHTTP 502エラー完全ガイド：原因と標準リトライの実装手順"
date: "2026-04-24"
category: "infra"
description: "Integration Serverでの502エラー検知から、throwExceptionForRetryを用いた標準リトライの実装、メモリリークを防ぐ設定まで詳しく解説。"
themes: ["dev:webmethods", "infra:api", "error-handling"]
updated: "2026-08-17"
---



# webMethodsのHTTP 502エラー完全ガイド：原因と標準リトライの実装手順

## 概要
[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods") [Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server") (IS) で外部Web API / マイクロサービス連携時に突発発生する [HTTP 502 Bad Gateway](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="502%20Bad%20Gateway") エラーは、一時的なネットワーク過負荷やサービス瞬断が起因の大半を占めます。本稿では、TRY-CATCH ブロックによるステータス捕捉、`pub.flow:getLastError` の メモリリーク防止チューニング、および `pub.flow:throwExceptionForRetry` を用いた標準自動リトライ実装を解説します。

---

## 1. なぜ HTTP 502 Bad Gateway エラーに自動再試行が有効なのか？

502 Bad Gateway はクライアントのパラメータエラー（4xx）やアプリケーションの致命的例外（500）ではなく、リバースプロキシや API Gateway がバックエンドサーバーから正しい応答を受信できなかった一時的通信障害です。短時間の待機後に再試行（Retry）を行うことで、大部分のトランザクションが正常完了します。

---

## 2. ステップ1：TRY-CATCH-FINALLY による例外補獲

webMethods Integration Server (IS 10.3+) の標準フロー制御を活用します。

- **TRY ステップ**: `pub.client:http` や REST / SOAP コールを実行。
- **CATCH ステップ**: 発生した例外を捕捉し、エラーコードの判定へ分岐。

---

## 3. ステップ2：502 エラーの判別と `getLastError` メモリリーク対策

`pub.flow:getLastError` を用いて `lastError/header/status` が `502`（または 503/429）であるかを検証。

> [!CAUTION]
> **OOM (Out Of Memory) 防御** 
> ループ処理や高頻度エラー発生時、`getLastError` の情報がパイプラインへ蓄積しメモリを圧迫します。IS 拡張設定で `watt.server.getLastError.removeLastError = true` を適用し、取得後のエラーオブジェクト自動破棄を有効化します。

---

## 4. ステップ3：`pub.flow:throwExceptionForRetry` による標準リトライ発火

502エラー検知時、`pub.flow:throwExceptionForRetry` を呼び出すことで `ISRuntimeException` をスロー。

- **動作特性**: ISの実行エンジンおよびトリガープロパティ（Max retries / Retry interval）に従い、サービス全体を自動再実行。
- **制約事項**: トップレベルフローサービスまたは Trigger / JMS 経由起動のサービスで有効。子サービス内部呼び出しでは制限あり。

---

## 5. まとめ

1. **TRY-CATCH による確実な捉え**: HTTP 502 を 4xx エラーと切り分けて捕捉。
2. **IS 設定の最適化**: `removeLastError=true` によるメモリ枯渇防止。
3. **リトライ適用**: トップレベルでの `throwExceptionForRetry` 活用。

---

## 変更履歴 (Changelog)
- **2026-08-17**: 読み手に寄り添うプロ品質へのリライト（煽り・誇張表現の適正化、概要・構成の洗練）。
- **2026-08-02 (v3)**: 2026年最新のwebMethods Integration Server 10.x/11.x 502エラーハンドリング、`throwExceptionForRetry` / `getLastError` メモリチューニングのファクトチェックと目次H2構造最適化。
- **2026-04-24 (v2)**: 新規作成。
