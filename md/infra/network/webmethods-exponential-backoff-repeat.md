---
title: "webMethods実践：REPEATステップと指数バックオフで作る最強のリトライ処理"
date: "2026-04-24"
category: "infra"
description: "Thundering Herd問題を回避するための指数バックオフ実装術。REPEATステップの使い方とパイプラインロールバックの注意点を詳解。"
themes: ["dev:webmethods", "ops:resilience", "backoff-strategy"]
updated: "2026-08-02"
---

# webMethods実践：REPEATステップと指数バックオフで作る最強のリトライ処理

## 超要約
[webMethods](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="webMethods") [Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server") で外部APIを呼出す際、一定間隔での単純再試行は Thundering Herd（群衆の暴走）を引き起こし、バックエンド障害を増幅させます。本稿では、`REPEAT` ステップと [指数バックオフ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="指数バックオフ") (Exponential Backoff + Full Jitter) を用いた強靭な自己回復リトライ処理の構築手順とパイプラインロールバックの注意点を解説します。

---

## 1. なぜ指数バックオフ（Exponential Backoff）とジッター（Jitter）が必要なのか？

外部サービスで [502 Bad Gateway](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="502%20Bad%20Gateway") や 503/429 エラーが起きた際、複数のリクエストが一斉に固定間隔（例: 5秒ごと）で再試行を行うと、アクセススパイクが原因で復旧中のバックエンドが再びダウンします。

- **指数バックオフ**: 待機時間を `1s ➔ 2s ➔ 4s ➔ 8s` と倍々で延ばす。
- **フル・ジッター (Full Jitter)**: 待機時間にランダムな揺らぎを加算し、リクエストタイミングの重複を分散。

---

## 2. REPEAT ステップを活用した実装手順

1. **`REPEAT` ステップの配置とプロパティ設定**:
   - `Repeat on`: `FAILURE`（例外または失敗時に繰り返し）
   - `Count`: 最大再試行回数（例: 5回）
   - `Repeat interval`: `%waitTime%`（動的パイプライン変数を指定）
2. **フロー内部ロジック**:
   - `pub.client:http` 呼び出し。
   - HTTPステータスが 502/503/429 の場合、例外をスロー。
   - 次回 `%waitTime%` を `Base * (2 ^ Count) + RandomJitter` で再計算しパイプラインへ保持。

> [!WARNING]
> **パイプライン変数ロールバックの注意点**  
> `REPEAT` が失敗して次の反復に移る際、トップレベルの変数状態は反復開始時に自動戻り（ロールバック）します。しかし、深層の IData ドキュメント内変数の変更は巻き戻らないため、データ不整合に注意が必要です。

---

## 3. サーバースレッド（IS Thread Pool）の枯渇リスクと回避策

長時間（数分〜数十分）に及ぶ `REPEAT` + Sleep ループを過剰に実行すると、[Integration Server](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Integration%20Server") のワーカースレッドが枯渇し、サーバー全体の応答が停止します。

- **使い分けの基準**:
  - 短時間（数秒〜数十秒）のスパイク障害 ➔ `REPEAT` によるインラインバックオフ。
  - 長時間の中断が想定される場合 ➔ Messaging (UM/MQ) キューへ退避させ非同期リスナーで再試行。

---

## 4. まとめ

1. **Jitter付き指数バックオフ**: 外部システム保護のための必須デザイン。
2. **パイプライン設計の注意**: トップレベル変数のロールバック挙動を考慮。
3. **スレッドプール管理**: 長時間待機は非同期キューイングへオフロード。

---

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のwebMethods Integration Server 10.x/11.x, Exponential Backoff + Jitter, REPEATステップロールバック仕様のファクトチェックと目次H2構造最適化。
- **2026-04-24 (v2)**: 新規作成。
