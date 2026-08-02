---
title: "【完全ガイド】Rubrik脅威監視で検体を特定！詳細ログの取得方法と仕組み"
date: "2026-04-16"
category: "infra"
description: "Rubrik Security Cloud の脅威監視ログを GUI スクレイピングではなく API ファーストで取得するための基礎ガイド。"
themes: ["infra:backup", "rubrik:operations"]
updated: "2026-08-02"
---

# 【完全ガイド】Rubrik脅威監視で検体を特定！詳細ログの取得方法と仕組み

## 超要約
[Rubrik](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Rubrik") Security Cloud (RSC) の Threat Monitoring（脅威監視）で特定されたマルウェア・ランサムウェア検体や監査ログの取得手法を解説します。DOMスクレイピングに頼らず、Rubrikの「APIファースト」アーキテクチャを活用したGraphQL API / Webhook / Syslog経由での信頼性の高いログ抽出とSIEM（Splunk, Google Chronicle等）連携のベストプラクティスを提示します。

---

## 1. Rubrik Threat Monitoring（脅威監視）のログ生成メカニズム

Rubrikはバックアップデータを不変ストレージに保存するだけでなく、バックグラウンドで機械学習モデルおよびYARAルールを用いてマルウェアシグネチャを走査（スキャン）します。

検体が検出された際、システム内部では以下のような標準イベントログが即時に生成されます。
- `ThreatMonitoringAnalysisSucceeded`: スキャン完了イベント
- `ThreatMonitoringHashCatalogAnalysisMatchesFound`: マルウェアハッシュ一致検出イベント

---

## 2. GUIスクリーン・スクレイピングが「アンチパターン」である理由

ダッシュボード画面（GUI）のHTML要素をPuppeteerやSeleniumでパース・スクレイピングする手法は、以下の理由からエンタープライズ運用で禁止されるべきです。

- **画面UI変更に伴う壊れやすさ**: RSCのアップデートでCSSクラスやDOM構造がわずかに変更されただけで収集スクリプトが即時破綻。
- **セキュリティ発報時の信頼性欠如**: インシデント発生時にログ抽出が失敗し、フォレンジック監査が停滞。

---

## 3. APIファースト（GraphQL / REST API）による構造化データ取得

Rubrikの管理画面（RSC GUI）で実施できるあらゆる操作・表示は、バックエンドの **GraphQL API** 経由で100%同じデータをJSON形式で取得可能です。

- **RSC GraphQL API**: 検出された脅威のハッシュ値、影響を受けたファイルパス、バックアップ世代を一括クエリ。
- **Syslog / Webhook リアルタイム発報**: SIEM（Splunk, Microsoft Sentinel, Google Chronicle）へJSON形式で即時自動転送。

---

## 4. 取得手法の比較（API vs スクレイピング）

| 比較項目 | HTML/DOM スクレイピング | Rubrik GraphQL API / Syslog |
| :--- | :--- | :--- |
| **保守性・耐障害性** | 弱（UI改変でエラー多発） | **高（セマンティックバージョン維持）** |
| **処理速度 & 精度** | 遅い（ブラウザ描画待ち） | **高速（構造化JSONデータ取得）** |
| **セキュリティ連携** | 不可（ブラウザ自動化依存） | **SOAR/SIEMとシームレス連携可能** |

---

## 5. まとめと連携手法

Rubrikで脅威検体が発見された場合、GUIスクレイピングではなく公式GraphQL APIおよびSyslog連携を活用するのが正解です。

---

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のRubrik Security Cloud (RSC) GraphQL API、Threat Monitoring YARAルール連携、SIEMインテグレーションのファクトチェックと目次H2構造最適化。
- **2026-04-16 (v2)**: グローバルデザイン統一および構成最適化。
- **2026-04-06 (v1)**: 初版作成。
