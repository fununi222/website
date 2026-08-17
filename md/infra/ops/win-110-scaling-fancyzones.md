---
title: "Windows 11 | 表示スケール110%設定とFancyZones活用 2026"
date: "2026-04-09"
category: "infra"
description: "大画面モニターやROG Ally/Steam Deckでの作業効率を最大化する、カスタムスケーリングとマウスのみでの画面分割手法。"
themes: ["infra:os", "infra:automation", "windows:config"]
updated: "2026-08-17"
---



# Windows 11 | 表示スケール110%設定とFancyZones活用 2026

## 概要
本記事は、Windows 11 (24H2/25H2) 環境における視認性と作業効率を極限まで高めるカスタマイズ手法の記録です。標準設定にはない「110%」の [カスタムスケーリング](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="カスタムスケーリング") を適用し、[PowerToys](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PowerToys") の [FancyZones](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="FancyZones") 機能をマウスの副ボタン（右クリック）のみで呼び出せるよう調整することで、キーボードを介さない直感的なマルチウィンドウ環境を構築します。

---

## 1. 絶妙なサイズ感！画面の表示スケールを「110%」にする方法

Windows 11の標準ディスプレイ設定（100%, 125%, 150%）では、「100%だと文字が小さいが、125%だと作業領域が狭すぎる」というジレンマが生じます。特に4K/2Kディスプレイやゲーミングハンドヘルド（ROG Ally等）では、110%の「カスタムスケーリング」が最適な視認性と広さを実現します。

### 設定手順
1. `Win` + `I` キーで **「設定」** を開く。
2. **「システム」** ＞ **「ディスプレイ」** をクリック。
3. **「拡大縮小」** の詳細設定から **「カスタム スケール」** に **`110`** を入力。
4. **「今すぐサインアウト」** を選択してサインアウト・再ログインし設定を反映。

---

## 2. Shiftキーはもう不要！マウスだけで完結する「6画面分割」

Microsoft公式ユーティリティ **[PowerToys](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PowerToys")** 内の **[FancyZones](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="FancyZones")** は、画面を自由な区画（6分割等）にレイアウトできるツールです。

初期状態では `Shift` キーを押しながらのドラッグが必要ですが、設定を変更することで**左ドラッグ中に副ボタン（右クリック）を1回押すだけ**でゾーン選択を起動できます。

### 設定のポイント
1. [PowerToys](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="PowerToys") 設定から **「[FancyZones](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="FancyZones")」** を有効化。
2. ❌ **「Shiftキーを押してゾーンをアクティブにする」** のチェックを外す。
3. ✅ **「主ボタンでドラッグ中に副ボタン（右クリック）でゾーンをアクティブ化」** にチェックを入れる。

---

## 3. まとめと環境構築のメリット

- **110%カスタムスケール**: 文字の滲みを抑えつつ、情報量を犠牲にしない高密度表示。
- **FancyZones マウス駆動化**: マウス単独操作やタッチパネル操作でのマルチウィンドウ移動の快適化。

---

## 変更履歴 (Changelog)
- **2026-08-17**: 読み手に寄り添うプロ品質へのリライト（煽り・誇張表現の適正化、概要・構成の洗練）。
- **2026-08-02 (v3)**: Windows 11 24H2/25H2、PowerToys v0.85+での動作検証とカスタムスケーリング設定のファクトチェック。
- **2026-04-09 (v2)**: メタデータおよびグローバルデザイン統一。
- **2026-04-06 (v1)**: 新規作成。
