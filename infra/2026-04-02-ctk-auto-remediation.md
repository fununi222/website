---
title: "VMware CBT不整合の自動検知と是正"
date: "2026-04-02"
category: "Infrastructure"
description: "VMware vSphere環境におけるバックアップトラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知とは是正を自動化する実践手法。"
---

# VMware CBT不整合の自動検知と是正

VMware vSphere環境におけるバックアップトラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知と是正を自動化する実践手法。

## 1. 背景：なぜCBT/CTKは不整合を起こすのか

VMwareの増分バックアップに不可欠な機能であるCBTは、仮想マシンの構成パラメータ（ctkEnabled）と実際の仮想ディスク（scsiX:Y.ctkEnabled）の不整合により、予期せず無効化されることがあります。

不整合が起きると、バックアップソフトはデータの整合性を保つためにフルスキャン（事実上のフルバックアップ）にフォールバックし、バックアップ時間とストレージ容量を圧迫します。

## 2. 技術スタック：PowerCLI × Jenkins

手動での確認を排除するため、PowerCLIを使用して全VMのCBTステータスを走査し、不整合を検知した場合に自動的にリセットするフローを構築しました。Jenkinsを用いることで、毎日12:00（バックアップ実行前）の定期実行と通知を一元管理しています。

## 3. 自動是正スクリプトの実装例

```powershell
# CBTの不整合をチェックし、必要に応じてリセットする
$vmlist = Get-VM | Where-Object { $_.PowerState -eq "PoweredOn" }

foreach ($vm in $vmlist) {
    $cbtEnabled = $vm.ExtensionData.Config.ChangeTrackingEnabled
    if ($cbtEnabled -ne $true) {
        Write-Host "Resetting CBT for $($vm.Name)..."
        
        # CBTの再有効化プロセス
        $spec = New-Object VMware.Vim.VirtualMachineConfigSpec
        $spec.ChangeTrackingEnabled = $true
        $vm.ExtensionData.ReconfigVM($spec)
        
        # 設定を反映させるために一時的なスナップショットを作成・削除
        $snap = New-Snapshot -VM $vm -Name "CBT-Reset-Temp"
        Remove-Snapshot $snap -Confirm:$false
    }
}
```

## 4. 運用上の注意点

スナップショットを頻繁に作成・削除するとスタンが発生する可能性があるため、バックアップ実行直前かつ低負荷な時間帯を選んで実行する必要があります。
