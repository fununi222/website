---
title: "VMware vSphere | CBT不整合の自動検知と是正 2026"
date: "2026-04-09"
category: "infra"
description: "VMware vSphere環境におけるバックアップトラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知と是正を自動化する実践手法。"
themes: ["infra:backup", "infra:automation", "infra:virtualization"]
updated: "2026-08-17"
---



# VMware vSphere | CBT不整合の自動検知と是正 2026

## 概要
本レポートは、[VMware vSphere](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="VMware vSphere") 8.0 / ESXi 環境における増分 [バックアップ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="バックアップ") の生命線である [CBT (Changed Block Tracking)](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="CBT (Changed Block Tracking")) の不整合問題を解決する自動化手法について解説します。不整合発生によるフルスキャンのフォールバックを防ぐため、[PowerShell](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PowerShell") (PowerCLI) と CI/CD パイプラインを組み合わせ、[スナップショット](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="スナップショット") 生成を介したステータスの自動リセットフローを構築し、バックアップ運用の安定性を向上させます。

---

## 1. 背景：なぜCBT/CTKは不整合を起こすのか

VMwareの増分バックアップに不可欠な機能である [CBT](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="CBT") は、仮想マシンの構成パラメータ（`ctkEnabled = TRUE`）と実際の仮想ディスク設定（`scsiX:Y.ctkEnabled = TRUE`）のズレ、あるいはVMware ESXiの不意な停電・異常終了や障害復旧時に予期せず不整合（CTK corrupt）を起こすことがあります。

不整合が起きると、バックアップソフト（Veeam、Rubrik、Commvault等）は安全のためにフルスキャン（事実上のフルバックアップ）にフォールバックし、バックアップウィンドウの超過やストレージI/Oの突発的な増大を招きます。

---

## 2. 自動化アーキテクチャ：PowerShell (PowerCLI) × スケジューラ

手動でのCTK不整合確認を排除するため、PowerCLIを用いて定期的に全VMの [CBT](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="CBT") ステータスを検査し、不整合を検知した場合に自動的に再初期化（Reset）するワークフローを構築します。

1. **毎日12:00（夜間バックアップ実行前）にPowerCLIジョブが起動**
2. **全PoweredOn仮想マシンの `ChangeTrackingEnabled` フラグを評価**
3. **フラグ無効化または不整合VMに対し、CBT構成パラメータの再定義と一時スナップショット生成・即時削除（CTKマップの強制再構築）を自律実行**
4. **結果をSlack / Teamsへ自動通知**

---

## 3. 自動是正スクリプトの実装例

```powershell
# VMware vSphere CBT不整合自動チェック＆是正スクリプト (2026 vSphere 8.0対応)
Connect-VIServer -Server "vcenter.internal.domain" -Protocol https

$vmlist = Get-VM | Where-Object { $_.PowerState -eq "PoweredOn" }

foreach ($vm in $vmlist) {
 $cbtEnabled = $vm.ExtensionData.Config.ChangeTrackingEnabled
 if ($cbtEnabled -ne $true) {
 Write-Host "WARNING: CBT inconsistent for $($vm.Name). Initiating auto-remediation..." -ForegroundColor Yellow
 
 # CBT再有効化パラメータ定義
 $spec = New-Object VMware.Vim.VirtualMachineConfigSpec
 $spec.ChangeTrackingEnabled = $true
 $vm.ExtensionData.ReconfigVM($spec)
 
 # CTKマップを再初期化するために一時スナップショットを作成・削除
 $snap = New-Snapshot -VM $vm -Name "CBT-Reset-AutoRemediation" -Description "Temporary snapshot for CBT map reset"
 Remove-Snapshot -Snapshot $snap -Confirm:$false
 
 Write-Host "SUCCESS: CBT successfully reset for $($vm.Name)." -ForegroundColor Green
 }
}

Disconnect-VIServer -Confirm:$false
```

---

## 4. 運用上の注意点とベストプラクティス

- **スタン（Stun）時間の最小化**: スナップショットの削除時には一時的なI/Oスタンが発生するため、高負荷なデータベースサーバー（SQL/Oracle）ではI/O低負荷時間帯を選んで実行する必要があります。
- **NVMeoF / vSAN 8.0 OSA/ESAでの留意点**: vSAN Express Storage Architecture (ESA) 環境では、従来のVMFSと比較してスナップショット処理が非常に高速ですが、CBTマップの再生成時には仮想ディスクサイズに比例した検証が発生します。

---

## 変更履歴 (Changelog)
- **2026-08-17**: 読み手に寄り添うプロ品質へのリライト（煽り・誇張表現の適正化、概要・構成の洗練）。
- **2026-08-02 (v3)**: 2026年最新のvSphere 8.0 Update 3 / vSAN ESA CBT動向、PowerCLI 13.x環境でのCBT再初期化スクリプトのファクトチェックと改訂。
- **2026-04-09 (v2)**: メタデータおよびグローバルデザイン標準化。
- **2026-04-06 (v1)**: 新規作成。
