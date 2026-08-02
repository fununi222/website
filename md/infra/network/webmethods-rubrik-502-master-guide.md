---
title: "webMethods×Rubrik連携の極致｜502エラーを『デザイン』するレジリエンス戦略"
date: "2026-04-24"
category: "infra"
description: "「リトライがシステムを殺す」事態を防ぐ。webMethods Integration Serverによる指数バックオフ実装と、運用の平穏を守るエラー判定分離のマスターガイド。"
themes: ["dev:webmethods", "infra:rubrik", "ops:resilience"]
updated: "2026-08-02"
---

# webMethods×Rubrik連携の極致｜502エラーを『デザイン』するレジリエンス戦略

## 超要約
[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods") [Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server") (IS) と [Rubrik](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Rubrik") Security Cloud (RSC) の API 連携において発生する [HTTP 502 Bad Gateway](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="502%20Bad%20Gateway") / 504 Gateway Timeout に対し、単なる手動再試行や無制限リトライは二次障害（リトライストーム）を引き起こします。本稿では、[REPEAT-TRY-CATCH](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="REPEAT-TRY-CATCH") による指数バックオフ＋ジッター実装と、「開始処理」と「状態確認ポーリング」のエラー判定分離設計を解説します。

---

## 1. 502 Bad Gateway / 504 Gateway Timeout の発生要因

- **100秒タイムアウトの壁**: API Gateway またはロードバランサーがバックエンドの重い集計/GraphQL処理の応答を100秒前後で打ち切る。
- **一時的負荷スパイク**: SaaS側のバックグラウンド処理やインデックス更新に伴う過渡的レイテンシ低下。

---

## 2. 黄金のパターン：REPEAT-TRY-CATCH による指数バックオフ＋ジッター

1. **`REPEAT`**: 最大試行回数（3〜5回）を指定。
2. **`TRY`**: 共通HTTP通信サービスを呼び出し、ステータス非200で例外スロー。
3. **`CATCH`**: `pub.flow:wait` を用い、指数バックオフ（`60s ➔ 120s ➔ 240s`）＋ [ジッター](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="ジッター") (±10〜20%の無作為な揺らぎ) を動的計算して適用。

---

## 3. エラーハンドリング運用分離：開始処理 (Mutation) vs 状態確認 (Query)

| 処理種別 | API要求 | 失敗時のビジネスインパクト | 障害対処方針 |
| :--- | :--- | :--- | :--- |
| **開始指示 (Mutation)** | オンデマンドバックアップ要求 | **高** (保護未実行リスク) | 即時アラート通知 & 最大限の自動リトライ |
| **状態確認 (Query)** | バックアップ進捗ポーリング | **低** (ジョブ自体は非同期実行中) | 警告扱い & 次回ポーリングへ静観引継ぎ ([Fail-Safe](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Fail-Safe")) |

---

## 4. まとめ

1. **ジッター付きバックオフ**: リトライストームを防ぎAPI負荷を分散。
2. **処理の性質に応じた分岐**: Mutation (指示) と Query (確認) の重要度分け。
3. **レジリエンス設計**: システム全体として一時通信エラーを自己吸収。

---

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のwebMethods Integration Server 10.x/11.x, Rubrik Security Cloud API 502/504タイムアウト、Fail-Safe運用のファクトチェックと目次H2構造最適化。
- **2026-04-24 (v2)**: SEOトップ1%戦略に基づきリライト。
- **2026-04-18 (v1)**: 初版作成。
