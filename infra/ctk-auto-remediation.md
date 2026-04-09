---
title: "VMware vSphere | CBT不整合の自動検知と是非 2026"
date: "2026-04-09"
category: "Infrastructure"
description: "VMware vSphere環境におけるバックアップトラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知と是正を自動化する実践手法。"
themes: ["infra:backup", "infra:automation", "infra:virtualization"]
---

# VMware vSphere | CBT不整合の自動検知と是正 2026
<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

## 超要約
本レポートは、[VMware vSphere](/article.html?md=glossary/system-glossary.md#:~:text=VMware vSphere) 基盤における増分[バックアップ](/article.html?md=glossary/system-glossary.md#:~:text=%E3%83%90%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)の生命線である [CBT (Changed Block Tracking)](/article.html?md=glossary/system-glossary.md#:~:text=CBT (Changed Block Tracking)) の不整合問題を解決する自動化手法について解説します。不整合発生によるフルスキャンのフォールバックを防ぐため、[PowerShell](/article.html?md=glossary/system-glossary.md#:~:text=PowerShell) (PowerCLI) と [Jenkins](/article.html?md=glossary/system-glossary.md#:~:text=Jenkins) を組み合わせ、[スナップショット](/article.html?md=glossary/system-glossary.md#:~:text=%E3%82%B9%E3%83%8A%E3%83%83%E3%83%97%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88)生成を介したステータスの自動リセットフローを構築し、運用の安定性を向上させます。

---

[VMware vSphere](/article.html?md=glossary/system-glossary.md#:~:text=VMware vSphere)環境における[バックアップ](/article.html?md=glossary/system-glossary.md#:~:text=%E3%83%90%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)トラブルを防ぐ。CBT（Changed Block Tracking）不整合の検知と是正を自動化する実践手法。

## 1. 背景：なぜCBT/CTKは不整合を起こすのか

VMwareの増分[バックアップ](/article.html?md=glossary/system-glossary.md#:~:text=%E3%83%90%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)に不可欠な機能である [CBT](/article.html?md=glossary/system-glossary.md#:~:text=CBT) は、仮想マシンの構成パラメータ（ctkEnabled）と実際の仮想ディスク（scsiX:Y.ctkEnabled）の不整合により、予期せず無効化されることがあります。

不整合が起きると、[バックアップ](/article.html?md=glossary/system-glossary.md#:~:text=%E3%83%90%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)ソフトはデータの整合性を保つためにフルスキャン（事実上のフルバックアップ）にフォールバックし、[バックアップ](/article.html?md=glossary/system-glossary.md#:~:text=%E3%83%90%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)時間とストレージ容量を圧迫します。

## 2. 技術スタック：PowerShell × Jenkins

手動での確認を排除するため、[PowerShell](/article.html?md=glossary/system-glossary.md#:~:text=PowerShell) (PowerCLI) を使用して全VMの [CBT](/article.html?md=glossary/system-glossary.md#:~:text=CBT) ステータスを走査し、不整合を検知した場合に自動的にリセットするフローを構築しました。[Jenkins](/article.html?md=glossary/system-glossary.md#:~:text=Jenkins) を用いることで、毎日12:00（バックアップ実行前）の定期実行と通知を一元管理しています。

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

[スナップショット](/article.html?md=glossary/system-glossary.md#:~:text=%E3%82%B9%E3%83%8A%E3%83%83%E3%83%97%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88)を頻繁に作成・削除するとスタンが発生する可能性があるため、[バックアップ](/article.html?md=glossary/system-glossary.md#:~:text=%E3%83%90%E3%83%83%E3%82%AF%E3%82%A2%E3%83%83%E3%83%97)実行直前かつ低負荷な時間帯を選んで実行する必要があります。


## 変更履歴 (Changelog)
- **2026-04-09**: `SKILL.md` 準拠のグローバルデザイン統一およびメタデータ標準化アップデートを実施。
- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデート、超要約・コンテンツ整理を実施。
