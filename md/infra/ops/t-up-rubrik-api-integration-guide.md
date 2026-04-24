---
title: "【技術編】APIで繋ぐ！T-UP × Rubrik不整合検知システムの構築ガイド"
date: "2026-04-24"
category: "infra"
description: "資産管理ツールT-UPとRubrik APIを連携させ、ゾンビバックアップを自動検知・解消するシステムの実装ガイド。Pythonによる名寄せロジックと主要APIエンドポイントを詳解。"
themes: ["dev:api", "infra:rubrik", "ops:automation"]
---

# APIで繋ぐ！T-UP × Rubrik不整合検知システムの構築ガイド

前回の記事では、[ゾンビバックアップ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="ゾンビバックアップ")を根絶するための全体戦略を解説しました。今回は、エンジニア向けに、資産管理ツール「[T-UP](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="T-UP")」とRubrikをAPIで繋ぎ、自動で不整合を検知・解消するシステムの具体的な実装方法を解説します。

## 1. システムアーキテクチャ

自動化の核となるのは、3つのソースからデータを収集し、[名寄せ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="名寄せ")を行う「Sync Agent（Python等で記述）」です。

- **データソースA (T-UP)**: CSVエクスポートまたはDB参照により、サーバーの管理状態（稼働・廃棄・休止）を取得。
- **データソースB (vSphere)**: `vSphere Automation API` を使用し、VMの存在確認とパワー状態を取得。
- **データソースC (Rubrik)**: `Rubrik [RSC](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="RSC") API` を使用し、保護状態（SLA Domain）とRelic状態を取得。

## 2. [名寄せ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="名寄せ")ロジックの実装ポイント

ホスト名は重複や変更が多いため、キーには必ず **`vSphere Instance UUID`** を使用します。

### 判定アルゴリズムの例
Pythonで各ソースのデータを辞書形式で保持し、以下のように突合します。

```python
# 疑似コード
for uuid in rubrik_protected_vms:
    if uuid not in vsphere_vms:
        # vSphereから消えているのにRubrikにデータがある = Relic
        if uuid in tup_decommissioned_list:
            # 資産台帳でも廃棄済み
            apply_unprotected_sla(uuid) # Rubrik SLAを解除
```

## 3. 使用する主要なRubrik APIエンドポイント

Rubrik Security Cloud（[RSC](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="RSC")）では、[GraphQL](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="GraphQL")を用いて以下の情報を一括取得します。

- **VM一覧とSLA状態の取得**: `vms` クエリを使用。`instanceUuid` や `effectiveSlaDomain` フィールドを含めます。
- **バックアップの一時停止**: `pauseManagedVolume` などのミューテーション。
- **SLAの変更（解除）**: `assignSlaDomain` ミューテーションで、SLA IDを `UNPROTECTED` に設定。

## 4. 安全な運用のための「承認」プロセス

自動化が「意図しない削除」を引き起こさないよう、以下の安全弁を設けます。

1. **ドライランモード**: 初回実行時は実際にAPIを叩かず、不整合の一覧をレポート（CSV）として出力する。
2. **閾値リミッター**: 一度に削除・解除する対象が全資産の5%を超える場合は、処理を中断してアラートを出す。
3. **監査ログ**: すべてのAPI操作をログに記録し、いつ誰（どのサービスアカウント）が変更したかを追跡可能にする。

## まとめ：[真実のソース](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="真実のソース")を中心とした運用へ

API連携による不整合検知は、導入初期こそ工数がかかりますが、一度稼働すれば「消し忘れ」というヒューマンエラーを恒久的に排除できます。

まずは一部のセグメントからスモールスタートし、徐々に自動化の範囲を広げていくことをお勧めします。

👉 **[① 戦略編：ゾンビバックアップを根絶するIT資産管理の自動化戦略へ戻る](https://fununi222.github.io/website/html/infra/zombie-backup-asset-management-strategy.html)**

## 変更履歴 (Changelog)
- **2026-04-24**: T-UP、vSphere、Rubrik APIを用いた不整合検知システムの技術実装ガイドを新規作成。Pythonによる名寄せロジックと主要エンドポイントを詳解。

