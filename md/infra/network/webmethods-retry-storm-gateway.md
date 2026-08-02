---
title: "API Gateway連携での罠「リトライストーム」を防ぐwebMethods設計術"
date: "2026-04-24"
category: "infra"
description: "マルチレイヤー環境におけるカスケード障害「リトライストーム」の原因と対策。Gatewayへのリトライ責任集約とべき等性の担保について。"
themes: ["infra:api-gateway", "dev:webmethods", "system-design"]
updated: "2026-08-02"
---

# API Gateway連携での罠「リトライストーム」を防ぐwebMethods設計術

## 超要約
[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods") [Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server") (IS) と [webMethods API Gateway](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="API%20Gateway") が複合するマルチレイヤー構成において、全レイヤーが個別に自動リトライを試みると、リクエスト数が乗算的に急増する「[リトライストーム](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="リトライストーム") (Retry Storm)」が発生し、システム全体を共倒れさせます。本稿では、リトライ責任の一元化、バルクヘッド、サーキットブレーカー、および [べき等性](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="べき等性") (Idempotency Key) 担保設計を解説します。

---

## 1. カスケード障害「リトライストーム」の乗算メカニズム

多層システム（Client ➔ API Gateway ➔ Integration Server ➔ Backend API）において、各レイヤーがそれぞれ3回リトライを設定している場合、1回のリクエスト失敗が `3 × 3 × 3 = 27倍` の負荷へと爆発します。

障害中のバックエンドに対しこのトラフィックが集中することで、ネットワーク帯域およびISスレッドプールが即時枯渇し、全サービスへ障害が連鎖します。

---

## 2. API Gateway を中心とした3つの連鎖防衛策

1. **リトライ責任の一体化（Gateway委譲）**: ネットワーク/L7エラーのリトライ責任をエッジ（API Gateway）に集約し、IS層ではインラインリトライを行わずエラーを即時返却。
2. **バルクヘッド & Retry-After ヘッダーの活用**: Gateway側で並列上限（Bulkhead）とサーキットブレーカーを設定。溢れたトラフィックに対し `429 / 503` と `Retry-After: 30` ヘッダーを返しクライアント側待機を強制。
3. **ヘルスチェック連動アクティブ・フェイルオーバー**: 一時障害ノードをGatewayが自律切り離し、別系の正常ノードへルーティング。

---

## 3. べき等性（Idempotency）とトランザクション保護

自動再試行を行う前提として、複数回実行されてもデータ不整合が発生しない「[べき等性](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="べき等性")」の担保が絶対要件です。

- **Idempotency-Key ヘッダー検証**: API Gateway / IS レイヤーでユニークなキー（UUID/トランザクションID）をRedis等で重複チェック。
- 二重決済・二重更新の完全防犯。

---

## 4. まとめ

1. **レイヤー多層化の排除**: リトライはエッジ層（API Gateway）に単一化。
2. **サーキットブレーカー導入**: 障害発生時の遮断と Retry-After 制御。
3. **Idempotency Key 適用**: データ不整合の防止。

---

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のwebMethods API Gateway / Integration Server 10.x/11.x リトライストーム対策、サーキットブレーカー、Idempotency Keyのファクトチェックと目次H2構造最適化。
- **2026-04-24 (v2)**: 新規作成。
