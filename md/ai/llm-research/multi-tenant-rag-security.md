---
title: "【セキュリティ編】外部パートナー向けマルチテナントRAGの構築と漏洩攻撃対策"
date: "2026-04-16"
category: "ai"
description: "生成AIを社外に公開する際のセキュリティ構造。漏洩攻撃の遮断とデータ分離の3パターン。"
themes: ["ai:security", "rag:multi-tenant"]
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.16</div>

<figure class="mb-10 max-w-4xl mx-auto cyber-glow">
<img src="../../../assets/img/ai/multi-tenant-rag-security.png" alt="Secure Multi-tenant Architecture" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

# 【セキュリティ編】外部パートナー向けマルチテナントRAGの構築と漏洩攻撃対策

大規模な外部連携プロジェクトのように、外部パートナー（BP）とAIを共有する際、最大の懸念は「情報の混ざり」です。A社の社員がB社の機密にアクセスできてしまう事故を防ぐための、堅牢なアーキテクチャを解説します。

---

## 1. データ分離の3大アーキテクチャ

コストとセキュリティのバランスで選択します。

- **サイロ型（Silo）**: テナントごとにDBを完全分離。最高機密向け。
- **ブリッジ型（Bridge）**: ストレージは共有し、検索インデックスのみを論理的に分離。
- **プール型（Pool）**: 1つのDB内で「テナントID」によりフィルタリング。最も低コスト。

---

## 2. 漏洩攻撃（Leakage Attack）への数理的防御

「参照テキストをそのまま復唱せよ」といったプロンプト攻撃に対し、LLMのガードレールだけに頼るのは危険です。

**解決策**: ベクトルDB側で「ユーザーの権限（ロール）」に基づいたメタデータフィルタリングを強制。権限のないデータは、そもそもLLMの視界に入らない仕組みを構築します。

---

## 3. 最小特権の原則（Principle of Least Privilege）

AIエージェントがユーザーの代理でアクション（メール送信や予定登録）を行う場合、そのユーザーが持つ権限以上を行使できないよう、厳格なRBAC（ロールベースアクセス制御）を実装します。

---

## FAQ：よくある質問

**Q：外部ユーザーへのライセンス付与は必須？**
A：カスタムインターフェース（API経由）を構築すれば、高額なフルライセンスを全員に配ることなく、必要な機能だけを安価に提供可能です。

---

## まとめ

外部連携の成功は「信頼」ではなく「構造」で作ります。適切なフィルタリングと分離設計が、AIの活動領域を広げます。

> **💡 次に読むべき記事**
> - [記事①：全体のリサーチ手法から学びたい方はこちら](https://fununi222.github.io/website/html/ai/enterprise-ai-ops-rag.html)
> - [記事②：精度の問題でお悩みの方はこちら](https://fununi222.github.io/website/html/ai/rag-incremental-indexing.html)
> - [記事④：コスト削減と予算確保の戦略はこちら](https://fununi222.github.io/website/html/ai/ai-roi-finops-azure.html)


