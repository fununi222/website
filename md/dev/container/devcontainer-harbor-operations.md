---
title: "記事②：Docker Hubの制限を回避！Harborプロキシキャッシュと運用術"
date: "2026-04-16"
category: "dev"
description: "Harborのプロキシキャッシュやタグ管理機能を使い、Docker HubのAPI制限を回避しつつコストを最適化する運用術。"
themes: ["dev:operations", "infra:container", "finops"]
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.16</div>

# 記事②：Docker Hubの制限を回避！Harborプロキシキャッシュと運用術

前回の記事では、DevcontainerとHarborの基礎について解説しました。
（※基礎をおさらいしたい方は[こちら](./devcontainer-harbor-intro.md)）

本記事では、Harborを導入することで得られる「コスト削減」と「運用効率化」の具体的なテクニックを解説します。
特に、**Docker HubのPull制限に悩んでいる方**は必見です。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026年 4月16日</div>

---

## パブリックレジストリの「2つの大きな壁」

チームの規模が大きくなったり、CI/CD（継続的インテグレーション）を回し始めたりすると、[Docker Hub](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Docker%20Hub")などのパブリックレジストリを直接使うことで問題が発生します。

### 1. Docker Hubの「Pull制限」（レートリミット）

Docker Hubには厳しい制限があります。未認証ユーザーは6時間で100回、認証済みでも200回しかイメージをダウンロード（Pull）できません。
大規模なCI/CDパイプラインを回していると、この制限にすぐに引っかかり、開発が完全にストップしてしまいます。

### 2. 高額なEgress（データ転送）コスト

AWSやGoogle Cloudなどのパブリッククラウドから、インターネットを経由して外部のDocker Hubからデータをダウンロードすると、高額なデータ転送料（Egressコスト）が発生します。

## 解決策：Harborの「プロキシキャッシュ」機能

これらの問題を一発で解決するのが、Harborの**「[プロキシキャッシュ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="プロキシキャッシュ")」**機能です。

### プロキシキャッシュの仕組み

Harborを、Docker Hubとあなたの開発環境の「間」に置きます。

1. 開発者がHarborにイメージを要求します。
2. Harborにそのイメージがない場合、HarborがDocker Hubからダウンロードし、**自社内に保存（キャッシュ）**します。
3. 次に別の人が同じイメージを要求したときは、**Harborが社内のキャッシュから即座に提供**します。

### プロキシキャッシュのメリット

* **制限を回避できる:** 組織に100人の開発者がいても、HarborがDocker Hubから取得するのは「最初の1回」だけ。組織全体が「1人のユーザー」のように振る舞うため、制限に引っかかりません。
* **コスト激減:** 外部との通信が激減するため、Egressコストが大幅に下がります。
* **爆速のダウンロード:** 社内のLANネットワークから直接ダウンロードするため、待ち時間がほぼゼロになります。

> [!TIP]
> **参考データ:** Harbor バージョン2.1.1以降では、イメージの更新確認（HEADリクエスト）はDocker Hubの制限にカウントされない仕組みになっており、さらに安全です。

## ディスク容量の枯渇を防ぐ「タグ保持ルール」

Harborを使い続けると、古いイメージがどんどん溜まり、ストレージ容量を圧迫します。
そこで便利なのが**「タグ保持ルール（Tag Retention Rules）」**です。
これは「削除する条件」ではなく、**「残す条件（ホワイトリスト）」**を指定する機能です。
条件から外れた古いイメージは、自動的に削除されます。

**【ルールの例】**
* 直近にPushされた最新の10個だけを残す。
* 過去7日間にPull（利用）されたイメージだけを残す。

これにより、ストレージコストを最小限に抑えることができます。

## 間違って消したくない！「タグの不変性」

絶対に消してはいけない本番用のイメージや、Devcontainerのベースイメージを守るための機能が**「タグの不変性（Tag Immutability）」**です。
Dockerの仕様上、同じ名前のタグ（例：v1.0）で新しいイメージを上書きできてしまいます。
しかし、この機能をオンにすると、指定したタグの上書きや削除をシステムレベルで完全に禁止できます。

## まとめ：Harborで快適な運用を

* **プロキシキャッシュ:** Docker Hubの制限を回避し、ダウンロードを爆速・低コストに。
* **タグ保持ルール:** 不要な古いイメージを自動で消してストレージを節約。
* **タグの不変性:** 重要なイメージの上書きをブロックしてシステムを保護。

運用基盤が整ったら、最後は「セキュリティ」です。
次の記事では、現代の開発に必須の「DevSecOps」をいかに自動化するかを解説します。

👉 **[DevSecOpsを自動化！Harbor×Devcontainerのセキュリティ戦略](./devcontainer-harbor-security.md)**




