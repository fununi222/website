---
title: "Infra | Amazon RDS：マネージドデータベースの核心と AIOps 自動修復 2026"
date: "2026-04-10"
category: "infra"
description: "RDSパラメータグループ、Multi-AZ、ストレージ自動スケーリングから、Boto3による自動スケールアップ実装まで。"
themes: ["infra:cloud", "infra:database", "ai:ops"]
---

# Infra | Amazon RDS：マネージドデータベースの核心と AIOps 自動修復 2026

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Standard Edition: v2026.04.10</div>

## 超要約

<figure class="my-10 max-w-4xl mx-auto cyber-glow">
  <img src="assets/img/aws-rds-tech-deep-dive-2026.png" alt="Amazon RDS Technical Visualization" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

[AWS RDS](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="AWS%20RDS")は、プロビジョニング、バックアップ、パッチ適用、および高可用性（[Multi-AZ](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Multi-AZ")）を自動化するマネージドサービスである。本稿では、その内部仕様、運用の勘所（Gotchas）、および [Boto3](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Boto3") を用いた [AIOps](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="AIOps") ワークフローの構築方法を整理する。

---

## 1. RDSの技術仕様

- **サポートエンジン:** [Amazon Aurora](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Amazon%20Aurora")、PostgreSQL、MySQL、MariaDB、Oracle、SQL Server。マイナーバージョンの自動アップグレード（`AutoMinorVersionUpgrade`）は設定可能だが、メンテナンスウィンドウ内の実行となり再起動を伴う。
- **ストレージとIOPS:** 汎用SSD（gp2/gp3）、プロビジョンドIOPS SSD（io1/io2）等をサポート。最大64TiBまで拡張可能。ストレージの自動スケーリングは、空き容量が10%未満、かつ指定された上限（`MaxAllocatedStorage`）を下回る場合にトリガーされる。
- **高可用性構成（[Multi-AZ](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Multi-AZ")）:**
    - **Multi-AZ DB インスタンス:** 異なるAZのスタンバイインスタンスへ同期レプリケーションを実施。
    - **Multi-AZ DB クラスター:** 1つのプライマリと2つの読み取り可能なスタンバイ（合計3つのAZ）で構成され、Quorumベースのコミットによりトランザクションレイテンシを低減し、フェイルオーバー時間を短縮（通常35秒未満）。
- **パラメータグループ管理:** データベースの設定値を [API](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="API") 経由で [IaC](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="IaC") 管理可能。適用タイプは「動的（`dynamic`、即座に反映）」と「静的（`static`、再起動時に反映）」に分かれ、厳密な制約がある。
- **バックアップ機構:** 自動バックアップ（最大35日保持）に加え、[PITR](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="PITR") により、トランザクションログを用いて秒単位での特定時刻の新規インスタンス復元をサポート。既存インスタンスのインプレース上書きは不可。

## 2. 実行デモ（Boto3による自動スナップショット取得とスケールアップ）

[AIOps](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="AIOps")のアラート発報時（CPU高騰やデッドロック頻発時）に、事後調査用の[スナップショット](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="スナップショット")を自動取得し、即時スケールアップで暫定復旧を図る [Boto3](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Boto3") スクリプトの実装例。

```python
import boto3
from datetime import datetime

# RDSクライアントの初期化
rds = boto3.client('rds', region_name='ap-northeast-1')

def auto_remediate_rds_load(db_identifier: str, target_instance_class: str):
    # 1. 状態保存のための手動スナップショット取得
    snapshot_id = f"incident-preserve-{db_identifier}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Creating snapshot: {snapshot_id}")

    rds.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier=db_identifier
    )

    # 完了待機 (ポーリング)
    waiter = rds.get_waiter('db_snapshot_completed')
    waiter.wait(
        DBInstanceIdentifier=db_identifier,
        DBSnapshotIdentifier=snapshot_id,
        WaiterConfig={'Delay': 30, 'MaxAttempts': 60}
    )
    print("Snapshot creation completed.")

    # 2. リソース枯渇への暫定対処（スケールアップの即時適用）
    print(f"Modifying DB instance {db_identifier} to {target_instance_class}...")
    rds.modify_db_instance(
        DBInstanceIdentifier=db_identifier,
        DBInstanceClass=target_instance_class,
        ApplyImmediately=True  # 注意: ダウンタイム（再起動）が発生
    )
    print("Modification request sent. Instance is entering 'modifying' state.")

if __name__ == "__main__":
    auto_remediate_rds_load('production-mysql-01', 'db.m6g.xlarge')
```

## 3. 運用上の注意点（Gotchas）

- **ストレージ自動スケーリングのクールダウン:** 容量拡張処理が完了（または最低6時間）するまで、次のスケーリングリクエストはブロックされる。突発的な大量書き込みによるスパイクには追いつけないリスクがある。
- **ストレージの縮小（Shrink）不可:** RDSのストレージ容量は拡張のみ可能。縮小が必要な場合は、論理ダンプ（`pg_dump` 等）でデータを抽出し、小さなストレージを持つ別インスタンスにリストアし直す必要がある。
- **ApplyImmediatelyによる意図しない再起動:** インスタンスクラスの変更など、`ApplyImmediately=True` を設定すると、多くの場合メンテナンスウィンドウを待たずにデータベースの強制再起動が走る。クライアント側の[トラブルシュート](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="トラブルシュート")（リトライロジック）が不可欠。
- **max_connections の枯渇:** デフォルトの最大接続数はインスタンスのメモリ量に依存する。[AWS Lambda](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="AWS%20Lambda") 等から高頻度で直接接続を行うと瞬時に枯渇するため、必ず「[Amazon RDS Proxy](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Amazon%20RDS%20Proxy")」によるコネクションプーリングを推奨。

## 4. 参考文献

- **Amazon RDS 開発者ガイド:** https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/Welcome.html
- **[Boto3](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Boto3") RDS API リファレンス:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html
- **[Amazon RDS Proxy](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Amazon%20RDS%20Proxy") の管理:** https://docs.aws.amazon.com/ja_jp/AmazonRDS/latest/UserGuide/rds-proxy.html

## 変更履歴 (Changelog)
- **2026-04-10**: Amazon RDSの技術仕様とBoto3を用いた自己修復ワークフローに関する深掘り記事を新規作成。

