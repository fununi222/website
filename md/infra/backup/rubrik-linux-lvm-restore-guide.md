---
title: "RubrikでLinux LVMのリストアが失敗する原因と「確実」な救出手順"
date: "2026-04-24"
category: "infra"
description: "LVM環境でファイル単位リストア（FLR）が失敗するUUID競合のメカニズムを解明。Live MountとHelper VMを駆使した高度な救出手順、BMR時の致命的な落とし穴をプロが詳解。"
themes: ["infra:rubrik", "linux:lvm", "backup:dr"]
---

# RubrikでLinux LVMのリストアが失敗する原因と「確実」な救出手順

「Linuxサーバーのファイルだけ戻したいのに、ファイル単位リストア（[FLR](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="FLR")）がエラーで落ちる……」

Rubrikを運用しているエンジニアが、LVM（論理ボリュームマネージャー）環境で必ず直面する「壁」があります。それは、バックアップデータが壊れているわけではなく、LinuxカーネルとLVMの**「メタデータの競合」**という構造上の制約です。

この記事では、インフラ運用の現場で数々の修羅場をくぐり抜けてきたプロの視点から、FLRが失敗する根本原因と、**「Live Mount ＋ Helper VM」を用いた100%確実な救出メソッド**を徹底解説します。

---

## 1. なぜ「LVM」は標準のリストア（FLR）を拒絶するのか？

結論から述べます。原因は、**「同一の[UUID](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="UUID")を持つボリュームが、システム内に2つ存在することをLinuxが許さないから」**です。

### 失敗のメカニズム
1.  Rubrikがファイル救出用の一時VM（プロキシ）にバックアップディスクをアタッチ。
2.  アタッチされたディスクのLVM UUIDが、プロキシVM自身のUUIDと一致（テンプレートから展開されたOSで頻発）。
3.  Linuxカーネルが「名前の重複」を検知し、データ保護のためにディスクのマウントを拒否。
4.  Rubrik側には `Failed to parse LVM GUID list` という無慈悲なエラーが返る。

この状態は、標準のGUI操作（FLR）では突破できません。**「手動によるUUIDの付け替え」**が必要になります。

---

## 2. 【最後の砦】Live Mount ＋ Helper VMによる高度な救出フロー

標準機能が使えない場合の「最強の回避策」が、**「[Live Mount](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Live%20Mount")」**機能を活用した代替手法です。

### 実行手順：UUIDの壁を「上書き」する

#### Step 1: Rubrik UIでのマウント
対象VMのスナップショットから「Mount Virtual Disk」を実行し、稼働中の別のLinux VM（**[Helper VM](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Helper%20VM")**）にディスクをアタッチします。

#### Step 2: Helper VMでの「強制インポート」
Helper VMにログインし、以下のコマンドでディスクを認識させます。ポイントは **`vgimportclone`** です。

```bash
# 1. 接続されたデバイスを確認
sudo lsblk -f

# 2. 【最重要】UUIDを書き換えながら別名でインポート
# 元データは一切変更されず、Helper VM内だけで新しいUUIDとして認識されます
sudo vgimportclone -n temp_restore_vg /dev/sdX3

# 3. ボリュームをアクティブ化
sudo vgchange -ay temp_restore_vg

# 4. 読み取り専用（Safety First）でマウント
sudo mount -o ro,user,noload /dev/temp_restore_vg/LogVol00 /mnt/recovery
```

これで、GUIでは不可能だったファイルアクセスが可能になります。必要なデータを `cp` や `scp` で救出しましょう。

---

## 3. ベアメタル復旧（BMR）時の「致命的な落とし穴」

システム全体を復旧させる際、[ReaR](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="ReaR")（Relax-and-Recover）を利用するケースも多いでしょう。ここで、**エンジニアの9割がハマる罠**があります。

### ⚠️ リストア先パスの誤解
ReaRが再構築したディスク群は、一時的に **`/mnt/local`** にマウントされています。

*   **❌ 失敗パターン**: Rubrikから `/`（ルート）にリストア。
    → レスキューOS（メモリ上）のファイルを上書きしてしまい、再起動してもデータが空のまま。
*   **⭕ 正解パターン**: Rubrikのリストア先（Alternate Path）に **`/mnt/local`** を指定。

この一点を間違えるだけで、数時間の復旧作業がすべて無に帰します。

---

## 4. 復旧の信頼性を高める商用ツールの選択肢

「コマンド操作のミスが許されない」というエンタープライズ環境では、Rubrik公式連携の **「Cristie RBMR」** の導入を検討すべきです。

| 比較項目 | ReaR (OSS) | Cristie RBMR (商用) |
| :--- | :--- | :--- |
| **操作性** | CUIのみ（専門知識必須） | GUI搭載（直感的） |
| **異機種復旧** | 手動調整が困難 | **完全自動化**（ドライバ自動注入） |
| **検証** | 本番で試すしかない | リストアテストの自動スケジューリング |

---

## 5. まとめ：LVM環境のデータ保護を確実にするために

1.  **FLR失敗＝UUID競合** と即座に判断し、Live Mountへ切り替える。
2.  **`vgimportclone`** コマンドをマニュアル化し、Helper VMを常備する。
3.  **BMR時は `/mnt/local`**。このマントラをチーム全員で共有する。

LVMは強力なツールですが、その複雑さを理解し、Rubrikの「代替手段」を熟知しておくことが、真のレジリエンス（回復力）に繋がります。

### 💡 関連記事
*   [LVM FLR失敗の技術的詳細：UUIDメタデータの深層](https://fununi222.github.io/website/html/infra/backup/rubrik-linux-lvm-flr-cause-guide.html)
*   [Rubrik APIでリストアテストを完全自動化する方法](https://fununi222.github.io/website/html/infra/backup/rubrik-api-automation-guide.html)

## 変更履歴 (Changelog)
- **2026-04-24**: 「SEOトップ1%戦略」に基づき、記事を再構築。実務で最も危険なBMR時のパス指定ミスへの警告を強化。

