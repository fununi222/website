---
title: "Enterprise AI Architecture | クラウドAI基盤 vs. 独自エージェントの選択肢と制約"
date: "2026-04-15"
category: "ai"
description: "外部パートナー利用不可というライセンス制約をどう回避するか。AI Knowledge Conciergeで浮き彫りになった、エンタープライズAI公開戦略の比較。"
themes: ["ai:architecture", "enterprise:agent", "cloud:ai"]
updated: "2026-08-17"
---


<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.15</div>

# Enterprise AI Architecture | クラウドAI基盤 vs. 独自エージェントの選択肢と制約

[生成AI](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="生成AI")を社内業務に統合する際、[AIエージェント開発基盤](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Copilot%20Studio")は迅速な開発を可能にしますが、ライセンス体系に起因する「外部ユーザー（BP）公開の制約」が普及の壁となる場合があります。本稿では、社外連携プロジェクトの知見をもとに、現実的な公開アーキテクチャを比較検討します。

---

## 1. AIエージェント開発基盤 における「BP排除」の壁

社外連携PoCにおいて、最大の論点となったのはライセンス制約です。

- **社内ユーザー**: 主要ライセンス等で利用可能。既存の組織内ナレッジ（SharePoint等）へのアクセスも容易。
- **外部パートナー (BP)**: **[AIエージェント開発基盤](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Copilot%20Studio") は、共有先・認証方式・チャネルごとに利用条件が変わる。少なくとも組織内共有ではユーザーライセンスが前提となり、外部BPへそのまま横展開する設計はライセンス/テナント/認証の事前確認が必須。**
- **課題**: 運用保守をBPへ委託している環境では、最もナレッジを必要とする層にAIツールを届けられない。

## 2. アーキテクチャ比較：Agent vs. Platform

制約を回避しつつ、セキュアにナレッジを公開するための3つのルートです。

| 方式 | 特徴 | 外部公開 | 構築コスト |---|---|---|---| **Native AI** | Microsoft 365 や Teams など既存ツールとの統合が強力。 | 組織/テナント前提になりやすい | 低 | **AIエージェント開発基盤** | ローコード開発、プラグイン連携、複数チャネル公開。 | 認証方式・共有範囲・ライセンス確認が必須 | 中 | **Custom Agent (RAG)** | クラウドAPI + Web App等で独自開発。 | **可能 (Auth制御次第)** | 高 |

## 3. AI Knowledge Conciergeプロジェクトのハイブリッド戦略

社外連携プロジェクトでは、以下のハイブリッド構成によるPoCを推進しています。

1. **データソースの正規化**: [Redmine](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Redmine") APIや Jira からチケットを抽出し、[JSONL](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="JSONL")形式で汎用性を確保。
2. **先行PoC (Studio)**: まずは社内ユーザー向けに [AIエージェント開発基盤](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Copilot%20Studio") で「回答の精度」を検証。
3. **拡張フェーズ (Custom)**: 精度が確認された後、BP向けの公開が必要な範囲に絞り、APIベースの独自フロントエンド（カスタムエージェント）へ移行。

---

## ファクトチェックメモ
- Microsoft Learn では、Copilot Studio の組織内共有で「利用ユーザーに Copilot Studio per user license が必要」と説明されています。
- 認証方式によって「リンクを知る誰でも利用可能」「組織内ユーザーを共有で制御可能」など挙動が変わるため、外部BP向けは公開チャネルだけでなく、Entra ID / Generic OAuth2 / Web Chat などの認証設計とコストモデルを分けて評価します。

## 結論：プラットフォームに依存しない「データ資産」の重要性
アーキテクチャの選択肢は今後も変化し続けますが、不変なのは「質の高いナレッジデータ」です。[LLM](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="LLM")の種類やライセンス形態に左右されないよう、データを疎結合に保ち、いつでも別の「器（エージェント）」へ移し替えられる設計がエンタープライズAIには不可欠です。

## 変更履歴 (Changelog)
- **2026-08-17**: 読み手に寄り添うプロ品質へのリライト（煽り・誇張表現の適正化、概要・構成の洗練）。
- 2026-04-15: 新規作成。Copilot Studio の公開制約とカスタムエージェント戦略のリサーチ結果を統合。
- 2026-07-11: 日付を確定し、Microsoft Learn の共有/認証仕様に合わせて外部公開の表現を精緻化。

