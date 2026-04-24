---
title: "AIコードレビューを「シニア級」に変えるプロンプト術：ペルソナ指定と思考の連鎖（CoT）の威力"
date: "2026-04-24"
category: "dev"
description: "AIによるコードレビューの質を劇的に向上させる手法を解説。専門家ペルソナの指定とChain-of-Thought（CoT）を組み合わせ、表面的な指摘を超えた本質的なバグ検知を実現。"
themes: ["ai:prompt-engineering", "dev:code-review", "ai:cot"]
---

# AIコードレビューを「シニア級」に変えるプロンプト術：ペルソナ指定と思考の連鎖（CoT）の威力

「AIに[コードレビュー](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AIコードレビュー")を頼んでも、命名規則の指摘ばかり……」
そう感じているなら、指示の出し方が原因かもしれません。

最新のベンチマークによると、AIに対して「シニアアーキテクト」などのペルソナを指定するだけで、人間の専門家の評価との整合性が劇的に向上することが証明されています。

さらに、**「[思考の連鎖（CoT：Chain-of-Thought）](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="CoT")」**という技術を組み合わせれば、AIは複雑なロジックの中に潜む致命的なバグを論理的に追い詰めることができます。

## 記事のポイント

### 1. 役割（ペルソナ）を与える
AIに対して単に「レビューして」と言うのではなく、「あなたはGoogleのシニアエンジニアです」といった具体的な背景を与えます。これにより、AI内部の知識が「専門家モード」へと切り替わり、より高度な観点（パフォーマンス、保守性、セキュリティ）での指摘が可能になります。

### 2. 思考のプロセスを書き出させる
`<thinking>` タグなどを用いて、結論を出す前にAI自身に1行ずつロジックを解析させます。これが「[思考の連鎖（CoT）](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="CoT")」です。ステップバイステップで推論させることで、複雑な条件分岐におけるバグの見落としを防ぎます。

### 3. 文脈（コンテキスト）を渡す
関数単体ではなく、関連ファイルやクラス全体の情報を与えることが重要です。プロジェクト全体のライフサイクルを把握させることで、リソースの解放漏れ（メモリリーク）などの検知精度が飛躍的に高まります。

## 次のステップ：実践編
AIを専門家モードに切り替えた後は、具体的な言語（Java/JavaScript）特有のバグをいかに検知させるかが重要です。

👉 **[【実践編】Null判定・リソース漏れをAIで即解決！最強プロンプト集へ](https://fununi222.github.io/website/html/dev/ai-code-review-practical-prompts.html)**

## 変更履歴 (Changelog)
- **2026-04-24**: [AIコードレビュー](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AIコードレビュー")の質を向上させるためのペルソナ指定とCoTプロンプトの解説記事を新規作成。

