---
title: "Obsidian | Google Drive Sync によるマルチプラットフォーム無料同期術 2026"
date: "2026-04-13"
category: "infra"
description: "ObsidianのメモをGoogle Drive Syncプラグインで同期。Windows、Android、iOS間での構築手順と運用ルールを詳解。"
themes: ["infra:os", "infra:automation", "other:tool"]
updated: "2026-08-02"
---

# Obsidian | Google Drive Sync によるマルチプラットフォーム無料同期術 2026

## 超要約
[Obsidian](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Obsidian") は優れたローカルファーストの知識管理ツールですが、モバイル端末との同期には通常有料サブスクリプション（Obsidian Sync）が必要です。本記事では、コミュニティプラグイン **[Google Drive Sync](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Google Drive Sync")** を活用し、Windows PC、Android、iOS の 3OS 間で [Vault](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Vault (保管庫)") を無料で完全同期する手法を解説します。

---

## 1. 同期システムのデザインと最重要ルール

- **Pull (ダウンロード) は自動**: アプリ起動時、自動的に Google Drive から最新のファイル群を取得。
- **Push (アップロード) は手動**: 編集したメモをクラウドに反映させるには、**明示的な手動 Push** が基本。

> [!CAUTION]
> **最重要：Vault名の完全統一**
> PC、Android、iOS のすべてで、**全く同じVault名（大文字・小文字も完全に一致）**にする必要があります。プラグインは「Vault名」をキーにして Google Drive 上のフォルダを識別するため、ここがズレると同期が成立しません。

---

## 2. Windows PC でのベース設定（親Vaultの作成）

1. **新規 Vault の作成**: Obsidian で Vault 名を入力（例：`MyNotes`）。
2. **プラグイン導入**: `Settings` > `Community plugins` > `Google Drive Sync` をインストール＆有効化。
3. **Google アカウント認証**: `Get Refresh token` より認証コードを取得して貼り付け。
4. **初回 Push**: `Google Drive Sync: Push to Google Drive` を実行しマイドライブ上にフォルダを生成。

---

## 3. Android 端末での同期設定

1. Termux または Play ストア版 Obsidian をインストール。
2. PCと全く同名の Vault名（`MyNotes`）で新規作成。
3. プラグイン認証後、`Google Drive Sync: Pull from Google Drive` を初回実行。

---

## 4. iOS (iPhone / iPad) での同期設定

1. App Store より Obsidian をインストール。
2. **「Store in iCloud」をオフ（ローカル保存）** にして Vault 作成。
3. プラグイン認証後、`Pull from Google Drive` を実行。

---

## 5. 運用上の鉄則とベストプラクティス

1. **編集後は必ず「Push」する習慣**: アプリを閉じる前にコマンドパレットから Push。
2. **同時編集の回避**: コンフリクトを防ぐため、「端末A完了 ➔ Push ➔ 端末Bで Pull」のシーケンスを守る。
3. **バックアップの併用**: PC側で Git または Google Drive PC 版による定期自動バックアップを併用。

---

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のObsidian v1.6+ / Google Drive Syncプラグイン認証手順、iOSローカルストレージ設定のファクトチェックと目次H2見出し標準化。
- **2026-04-13 (v2)**: メタデータおよびグローバルデザイン統一。
- **2026-04-06 (v1)**: 新規作成。
