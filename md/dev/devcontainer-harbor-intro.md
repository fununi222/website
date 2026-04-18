---
title: "記事①：Devcontainer×Harbor入門！開発環境の課題と解決策を完全解説"
date: "2026-04-16"
category: "dev"
description: "開発環境の一貫性を担保するDevcontainerと、セキュアなコンテナレジストリHarborの基礎を分かりやすく解説します。"
themes: ["dev:environment", "infra:container"]
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.16</div>

# 記事①：Devcontainer×Harbor入門！開発環境の課題と解決策を完全解説

「私のパソコンでは動くのに、本番環境では動かない…」
「新しく入ったメンバーの環境構築に、毎回3日もかかっている…」
開発現場で、こんな悩みを抱えていませんか？

実は、これらを劇的に解決する組み合わせがあります。それが**「[Devcontainer](https://fununi222.github.io/websi../../article.html?md=glossary/system-glossary.md#:~:text="Devcontainer")」**と**「[Harbor](https://fununi222.github.io/websi../../article.html?md=glossary/system-glossary.md#:~:text="Harbor")」**です。
この記事では、開発環境をコード化するDevcontainerと、エンタープライズ向けの強力なコンテナレジストリであるHarborの基礎知識を、分かりやすく解説します。

これを読めば、あなたのチームの開発スピードが圧倒的に上がります！

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026年 4月16日</div>

---

## Devcontainer（Development Containers）とは？

Devcontainerは、Visual Studio Code（VS Code）の拡張機能から生まれた技術です。
簡単に言うと、**「Dockerコンテナの中に、完全な開発環境を丸ごと作る仕組み」**です。

### 開発環境をコードで管理できる

Devcontainerでは、プロジェクトのルートにある `.devcontainer/devcontainer.json` というファイルで、必要な設定をすべて管理します。
* どのOSを使うか
* どのプログラミング言語（PythonやNode.jsなど）のバージョンを使うか
* VS Codeのどの拡張機能をインストールするか
これらをすべてコードとして保存できるのです。

### メリット：環境構築が「15分」で終わる

新入社員が入ってきたとき、手作業でツールをインストールすると1〜3日かかることもありますよね 。
しかし、Devcontainerを使えば、VS Codeで「コンテナで開く」をクリックするだけです。
たった15分で、他のメンバーと全く同じ環境が完成します。

* **環境の一貫性:** 依存関係のズレがなくなり、「私の環境だけ動かない」が消滅します。
* **ホストを汚さない:** 自分のパソコン（ホストマシン）に色々なソフトを入れなくて済むため、パソコンが重くなりません。

## CNCFの卒業プロジェクト「Harbor」とは？

Devcontainerで作った環境（コンテナイメージ）を、チーム内で安全に保存・共有する場所が必要です。
そこで活躍するのが**「Harbor」**です。
Harborは、VMwareが開発し、現在はCloud Native Computing Foundation (CNCF) という世界的組織で「Graduated（卒業）」ステータスを獲得している、最高ランクのコンテナレジストリです。

### なぜDocker HubではなくHarborなのか？

「[Docker Hub](https://fununi222.github.io/websi../../article.html?md=glossary/system-glossary.md#:~:text="Docker%20Hub")を使えばいいのでは？」と思うかもしれません。
しかし、Harborには企業で使うべき圧倒的なメリットがあります。

1. **オンプレミスやプライベートクラウドに構築できる:** 機密データを外部に出す必要がありません。
2. **強力な権限管理（RBAC）:** 「このチームは見るだけ」「この人は書き込み可能」など、細かく権限を設定できます。
3. **セキュリティ対策が標準装備:** イメージの脆弱性スキャン機能が最初から備わっています。

## DevcontainerとHarborを組み合わせるメリット

この2つを組み合わせると、以下のような「最強の開発基盤」が完成します。

* **一貫したセキュリティ:** Harborに保存された安全なイメージだけを、Devcontainerのベースとして使うことができます。
* **高速な開発サイクル:** チーム全員が同じレジストリから環境を取得するため、無駄なトラブルシューティングの時間がゼロになります。

## まとめ：最強の開発環境を手に入れよう

* **Devcontainer:** 環境構築を自動化し、「私の環境では動かない」を無くす。
* **Harbor:** コンテナイメージを安全に保管し、チームの権限を細かく管理する。

基礎が分かったところで、次は「実運用」での悩みである**「ネットワークコストの削減」と「Docker Hubの制限回避」**について見ていきましょう。

👉 **[Docker Hubの制限を回避！Harborプロキシキャッシュと運用術](./devcontainer-harbor-operations.md)**

