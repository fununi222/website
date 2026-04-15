---
title: "Enterprise AI Architecture | クラウドAI基盤 vs. 独自エージェントの選択肢と制約"
date: "202X-04-XX"
category: "ai"
description: "外部パートナー利用不可というライセンス制約をどう回避するか。Project-Aで浮き彫りになった、エンタープライズAI公開戦略の比較。"
themes: ["ai:architecture", "enterprise:agent", "cloud:ai"]
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.15</div>

# Enterprise AI Architecture | クラウドAI基盤 vs. 独自エージェントの選択肢と制約

## 超要約

<figure class="my-10 max-w-4xl mx-auto cyber-glow">
  <img src="../assets/img/ai/enterprise-copilot-architecture.png" alt="Enterprise Copilot Architecture" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

[生成AI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="生成AI")を社内業務に統合する際、[AIエージェント開発基盤](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Copilot%20Studio")は迅速な開発を可能にしますが、ライセンス体系に起因する「外部ユーザー（BP）公開の制約」が普及の壁となる場合があります。本稿では、社外連携プロジェクトの知見をもとに、現実的な公開アーキテクチャを比較検討します。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 202X-04-XX</div>

---

## 1. AIエージェント開発基盤 における「BP排除」の壁

社外連携PoCにおいて、最大の論点となったのはライセンス制約です。

- **社内ユーザー**: 主要ライセンス等で利用可能。既存の組織内ナレッジ（SharePoint等）へのアクセスも容易。
- **外部パートナー (BP)**: **[AIエージェント開発基盤](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Copilot%20Studio") のライセンス体系上、外部テナントのユーザーへの公開が原則不可。**
- **課題**: 運用保守をBPへ委託している環境では、最もナレッジを必要とする層にAIツールを届けられない。

## 2. アーキテクチャ比較：Agent vs. Platform

制約を回避しつつ、セキュアにナレッジを公開するための3つのルートです。

| 方式 | 特徴 | 外部公開 | 構築コスト |
|---|---|---|---|
| **Native AI** | ツール統合。連携が強力。 | 不可 (Tenant制約) | 低 |
| **AIエージェント開発基盤** | ローコード開発、プラグイン連携。 | 不可 (License制約) | 中 |
| **Custom Agent (RAG)** | クラウドAPI + Web App等で独自開発。 | **可能 (Auth制御次第)** | 高 |

## 3. Project-Aプロジェクトのハイブリッド戦略

社外連携プロジェクトでは、以下のハイブリッド構成によるPoCを推進しています。

1. **データソースの正規化**: [Redmine](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Redmine") APIや T-UP からチケットを抽出し、[JSONL](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="JSONL")形式で汎用性を確保。
2. **先行PoC (Studio)**: まずは社内ユーザー向けに [AIエージェント開発基盤](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="Copilot%20Studio") で「回答の精度」を検証。
3. **拡張フェーズ (Custom)**: 精度が確認された後、BP向けの公開が必要な範囲に絞り、APIベースの独自フロントエンド（カスタムエージェント）へ移行。

---

## 結論：プラットフォームに依存しない「データ資産」の重要性
アーキテクチャの選択肢は今後も変化し続けますが、不変なのは「質の高いナレッジデータ」です。[LLM](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="LLM")の種類やライセンス形態に左右されないよう、データを疎結合に保ち、いつでも別の「器（エージェント）」へ移し替えられる設計がエンタープライズAIには不可欠です。

## 変更履歴 (Changelog)
- 2026-04-15: 新規作成。Copilot Studio の公開制約とカスタムエージェント戦略のリサーチ結果を統合。
