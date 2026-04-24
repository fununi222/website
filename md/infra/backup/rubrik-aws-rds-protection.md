---
title: "Infra | Rubrik：AWS RDS クラウドネイティブ保護の技術詳解 2026"
date: "2026-04-10"
category: "infra"
description: "RDSスナップショットAPIのオーケストレーション、DSPMによる機密データ発見、論理バックアップ抽出パイプラインからGotchasまで。"
themes: ["infra:cloud", "infra:database", "ai:ops"]
---

# Infra | Rubrik：AWS RDS クラウドネイティブ保護の技術詳解 2026

<figure class="mb-10 max-w-4xl mx-auto cyber-glow">
  <img src="../../../../assets/img/infra/backup/rubrik-aws-rds-protection.png" alt="Rubrik AWS RDS Protection Architecture" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Standard Edition: v2026.04.10</div>

Rubrikは、独自ストレージへのデータ転送ではなく、AWSネイティブの[AWS RDS](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AWS%20RDS")スナップショット[API](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="API")をオーケストレーションすることで、[IAM Role](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="IAM%20Role")ベースのセキュアかつスケーラブルなデータ保護を実現する。本稿では、最新の仕様に基づき、アーキテクチャ上の制約、論理バックアップへの対応、および運用の勘所（Gotchas）を整理する。

---

## 1. AWS RDS B/Uの技術仕様とアーキテクチャ制約

- **クラウドネイティブ・オーケストレーション:** Rubrik独自のストレージにデータを引き抜くのではなく、AWSネイティブのRDSスナップショットAPIをRubrik Security Cloud (RSC) から呼び出し、ライフサイクルを統合管理する。
- **SLAドメインベースのポリシー制御:** バックアップ頻度（RPO）、保持期間（Retention）、クロスリージョン・クロスアカウントのレプリケーション要件を[SLA Domain](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="SLA%20Domain")として定義し、AWSリソースタグベースでRDSインスタンスへ自動適用が可能。
- **アーキテクチャ上の制約（従来型マルウェアスキャンの非互換性）:** RDSのスナップショットはAWSプロプライエタリなブロックレベルイメージであり、ホストOSも隠蔽されている。そのため、ファイル単位のエントロピー計測（暗号化の振る舞い検知）やYARAルールによるシグネチャベースのウイルススキャンは構造的に実行できない。

## 2. RDS環境に特化したセキュリティアプローチ

- **[DSPM](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="DSPM")（データセキュリティ態勢管理）による機密データ発見:** 従来のマルウェア検知の代わりに「データ漏洩リスクの可視化」にフォーカス。Rubrikが一時的なスキャナーリソースを起動してスナップショットをマウントし、DB内のテーブルに直接アクセスして[PII](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PII")（個人情報）や[PCI](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PCI")（クレジットカード情報）の保存場所を自動で分類・マッピングする。
- **イミュータビリティ（不変性）による論理的隔離:** AWSアカウントの特権ID侵害に伴うデータ全消去（DROP）やスナップショット削除を防ぐため、RSC側から[Retention Lock](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Retention%20Lock")を適用。さらに、RDSデータをRubrik側の管理下にあるイミュータブルな隔離領域（[Rubrik Cloud Vault](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Rubrik%20Cloud%20Vault")）へ完全に引き抜いて保護する機能（PostgreSQL等で順次対応）により、アカウント境界を越えた復元力を担保する。

> [!NOTE]
> ### Tech Insight: 「スナップショット」と「引き抜き（Vaulting）」の決定的違い
> 一般的な「スナップショット管理」は、データのコントロールがユーザーのAWSアカウント内に留まります。対してRubrikの「引き抜き」は、スナップショットからデータブロックを読み取り、Rubrikが管理する**別のアカウント・別の物理ネットワーク（隔離領域）**へ転送することを指します。
> - **開始時**: AWSのスナップショットとして撮影。
> - **転送時**: その中身を吸い出し、[Rubrik Cloud Vault](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Rubrik%20Cloud%20Vault")へ格納。
> - **結果**: あなたのAWSアカウントが完全に破壊されても、データは「外」で生き残っている「独立したバックアップ」へと昇華されます。

## 3. 論理バックアップ（SQLダンプ）への対応方針

- **結論:** Rubrik（およびAWSネイティブのスナップショット機能）は、取得したスナップショットから**直接「論理バックアップ（SQLダンプやCSVなど）」を生成・抽出して提供するネイティブ機能を持っていません。**
- **アーキテクチャの思想（RTO優先）:** RubrikはTB〜PBクラスのデータ保護を前提としており、抽出に時間がかかりリソースを消費する論理ダンプ処理をプラットフォーム側で行うアーキテクチャを採用していません。代わりに、スナップショットから新規のDBインスタンス全体を即座にプロビジョニングする「Export（クローン作成）」アプローチをとります。
- **DSPMの例外:** 前述した機密データ（PIIなど）のスキャン機能では、Rubrikがバックグラウンドで一時的なコンピュートリソースを立ち上げ、スナップショットをマウントして論理的にテーブルを読み取りますが、これはあくまで「メタデータの可視化」用であり、ユーザーがダンプファイルとしてダウンロードできるわけではありません。

## 4. 論理バックアップが必要な場合のAIOps的解決策

特定のテーブルデータの復元や、開発環境のマスキングテスト用にどうしても論理ダンプ（`pg_dump` や `mysqldump`）が必要な場合、[AIOps](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AIOps")エンジニアはRubrikのAPIを利用して以下の「一時インスタンス生成・破棄パイプライン」を自動化します。

- **フェーズ1 (Provision):** Rubrik API経由で、本番環境の任意時点（スナップショットまたは[PITR](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PITR")）のデータを元に、隔離されたサブネットに一時的なRDSインスタンスをエクスポート（作成）する。
- **フェーズ2 (Extraction):** 一時インスタンスのステータスが `Available` になったことをWebhook等で検知し、CI/CDツール（GitLab CI, GitHub Actionsなど）から対象DBに接続し、必要な論理ダンプコマンドを実行する。
- **フェーズ3 (Teardown):** ダンプデータの取得完了後、API経由で即座に一時インスタンスを削除し、クラウドリソースの課金を最小限に抑える。

## 5. 実行デモ（コード / コマンド例）

### 5.1. SLAドメインの自動割り当て
新規作成された[AWS RDS](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AWS%20RDS")インスタンスに対し、RubrikのREST [API](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="API")経由で[SLA Domain](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="SLA%20Domain")を割り当てる実装例。

```python
import requests
import os
import json

# Rubrik API接続情報
RUBRIK_NODE_IP = "rubrik.example.local"
API_TOKEN = os.getenv("RUBRIK_API_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def assign_sla_to_rds(rds_instance_id, sla_domain_id):
    """RDSインスタンスにSLAドメインを割り当てる"""
    url = f"https://{RUBRIK_NODE_IP}/api/v1/aws/rds_instance/{rds_instance_id}"
    payload = {"configuredSlaDomainId": sla_domain_id}

    try:
        response = requests.patch(url, headers=HEADERS, data=json.dumps(payload), verify=False)
        response.raise_for_status()
        result = response.json()
        print(f"Success: SLA Domain updated for RDS {result['name']}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
```

### 5.2. 抽出用の一時DBインスタンス自動生成
論理ダンプを取得するための前準備として、特定のスナップショットから安価なインスタンスタイプで一時的なRDSインスタンスをプロビジョニングする。

```python
def create_temp_rds_for_dump(snapshot_id, target_subnet_group, target_sg):
    """論理ダンプ抽出用の一時RDSインスタンスをエクスポートする"""
    url = f"https://{RUBRIK_NODE_IP}/api/v1/aws/rds_instance/snapshot/{snapshot_id}/export"

    # 抽出作業用のため、マルチAZを無効化し安価なインスタンスクラスを指定
    payload = {
        "targetInstanceId": "temp-dump-db-instance",
        "instanceClass": "db.t3.medium",
        "isMultiAz": False,
        "subnetGroupId": target_subnet_group,
        "vpcSecurityGroupIds": [target_sg]
    }

    try:
        response = requests.post(url, headers=HEADERS, data=json.dumps(payload), verify=False)
        response.raise_for_status()
        task_info = response.json()
        print(f"Export Job Started. Task ID: {task_info['id']}")
        return task_info['id']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
```

## 6. 運用上の注意点（Gotchas）

- **[KMS](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="KMS")キーの権限スコープ:** 暗号化されたRDSをクロスアカウント/クロスリージョンでリストアする場合、リストア先環境の[IAM Role](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="IAM%20Role")に対し、元データのKMSカスタマー管理キー（CMK）の `kms:Decrypt` および `kms:CreateGrant` 権限が必要。
- **AWS APIのレート制限（Throttling）:** 大規模環境で数百のRDSスナップショットを同時処理すると、AWS側のAPIレート制限に抵触する。SLA開始ウィンドウの分散が必要。
- **自動バックアップ無効化の副作用:** AWS側でRDSの自動バックアップ（保持期間0）を無効化するとトランザクションログが保持されず、[PITR](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PITR")が不可能になる。
- **一時的なコストの発生:** 論理バックアップ取得のたびにRDSインスタンスがプロビジョニングされ、稼働時間に応じたコンピュート/ストレージ料金が発生する。Teardown（破棄）の自動化が不可欠。
- **プロビジョニングのオーバーヘッド:** AWS RDSのエクスポート処理には一定のプロビジョニング時間（数分〜十数分）がかかるため、リアルタイムのダンプ取得要件には適さない。
- **データマスキングの考慮:** 一時DBには本番データがそのまま含まれる。ダンプ取得後に開発環境へ渡す前に、PIIデータのマスキング（スクラブ）が必要。

## 7. 参考文献

- **Rubrik API Documentation (AWS RDS):** https://build.rubrik.com/api-reference/rubrik-cdm-api/aws-rds/
- **Rubrik Python SDK (rubrik_cdm) Repository:** https://github.com/rubrikinc/rubrik-sdk-for-python

## 変更履歴 (Changelog)
- **2026-04-10**: 「スナップショット」と「引き抜き（Vaulting）」の技術的相違に関する解説（Tech Insight）を追記。
- **2026-04-10**: 論理バックアップへの対応方針とAIOps自動化パイプラインに関する技術解説を統合。
- **2026-04-10**: AWS RDSクラウドネイティブ保護に関する技術解説を独立記事として新規作成。





