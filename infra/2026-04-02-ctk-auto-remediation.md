---
title: "VMware CBT不整合の自動検知と是正"
date: "2026-04-06"
category: "Infrastructure"
description: "VMware vSphere環境におけるバックアップトラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知とは是正を自動化する実践手法。"
---

# VMware CBT不整合の自動検知と是正
<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono mt-2">Last Updated: 2026-04-06</div>

## 超要約
本レポートは、[VMware vSphere](../glossary/index.html) 基盤における増分[バックアップ](../glossary/index.html)の生命線である [CBT (Changed Block Tracking)](../glossary/index.html) の不整合問題を解決する自動化手法について解説します。不整合発生によるフルスキャンのフォールバックを防ぐため、[PowerShell](../glossary/index.html) (PowerCLI) と [Jenkins](../glossary/index.html) を組み合わせ、[スナップショット](../glossary/index.html)生成を介したステータスの自動リセットフローを構築し、運用の安定性を向上させます。

---

[VMware vSphere](../glossary/index.html)環境における[バックアップ](../glossary/index.html)トラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知と是正を自動化する実践手法。

## 1. 背景：なぜCBT/CTKは不整合を起こすのか

VMwareの増分[バックアップ](../glossary/index.html)に不可欠な機能である [CBT](../glossary/index.html) は、仮想マシンの構成パラメータ（ctkEnabled）と実際の仮想ディスク（scsiX:Y.ctkEnabled）の不整合により、予期せず無効化されることがあります。

不整合が起きると、[バックアップ](../glossary/index.html)ソフトはデータの整合性を保つためにフルスキャン（事実上のフルバックアップ）にフォールバックし、[バックアップ](../glossary/index.html)時間とストレージ容量を圧迫します。

## 2. 技術スタック：[PowerShell](../glossary/index.html) × [Jenkins](../glossary/index.html)

手動での確認を排除するため、PowerCLIを使用して全VMの [CBT](../glossary/index.html) ステータスを走査し、不整合を検知した場合に自動的にリセットするフローを構築しました。[Jenkins](../glossary/index.html) を用いることで、毎日12:00（バックアップ実行前）の定期実行と通知を一元管理しています。

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

[スナップショット](../glossary/index.html)を頻繁に作成・削除するとスタンが発生する可能性があるため、[バックアップ](../glossary/index.html)実行直前かつ低負荷な時間帯を選んで実行する必要があります。


## 変更履歴 (Changelog)
- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデート、超要約・コンテンツ整理を実施。
