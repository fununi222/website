---
title: "記事③：DevSecOpsを自動化！Harbor×Devcontainerのセキュリティ戦略"
date: "2026-04-16"
category: "dev"
description: "脆弱性スキャンの自動化(Trivy)、SBOMの生成、Cosignによる署名など、コンテナ開発におけるDevSecOpsの実現方法を解説します。"
themes: ["dev:security", "infra:container", "security:devsecops"]
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Research Log: v2026.04.16</div>

# 記事③：DevSecOpsを自動化！Harbor×Devcontainerのセキュリティ戦略

これまでの記事で、[Devcontainer](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Devcontainer")と[Harbor](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Harbor")の基礎、そしてコストを下げる運用術を解説しました。
（※前回の記事は[こちら](./devcontainer-harbor-operations.md)）

最終回となる本記事では、エンタープライズ企業で最も重視される**「セキュリティと認証」**について解説します。
Harborを導入すれば、面倒なセキュリティチェックをすべて自動化し、「[DevSecOps](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="DevSecOps")」を実現できます。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026年 4月16日</div>

---

## 脆弱性スキャンを自動化（Trivyの統合）

Harborには、オープンソースの脆弱性スキャナである「[Trivy](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Trivy")」や「Clair」が最初から統合されています。
使い方は簡単です。CI/CDパイプラインなどを通じてHarborにイメージをPushするだけで、**自動的に脆弱性がないかスキャン**してくれます。

さらに、VS Codeの拡張機能（Veracode Scanなど）を使えば、Devcontainerの中でコードを書いている最中に、リアルタイムで脆弱性を発見・修正することも可能です。

## SBOM（ソフトウェア部品表）の自動生成

最近のセキュリティ基準で必須になりつつあるのが「[SBOM](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="SBOM")（Software Bill of Materials）」です。
これは、ソフトウェアに「どんな部品（ライブラリ）が使われているか」を示す一覧表です。

Harbor バージョン2.11以降では、イメージをPushした瞬間に**Trivyが裏側で動いて、このSBOMを自動的に生成**してくれます。
これにより、PCI-DSSなどの厳しいコンプライアンス要件を満たすための書類作成の手間がゼロになります。

## Cosignによる「イメージの署名」で改ざん防止

スキャンをして安全だと分かっても、そのイメージが本番環境に行くまでに「改ざん」されたら意味がありません。
Harborは、Sigstoreプロジェクトの「Cosign」というツールと連携しています。

これにより、コンテナイメージに「これは間違いなく安全なイメージです」という**暗号学的な署名（ハンコのようなもの）**を付けることができます。
「署名のない怪しいイメージは、絶対にダウンロードさせない」という設定（コンテンツトラスト）にすれば、システムは劇的に安全になります。

## Devcontainerからのセキュアな認証方法

Harborをプライベート（非公開）で使う場合、DevcontainerからHarborにアクセスするための「パスワード」が必要です。しかし、パスワードをそのままファイルに書くのは危険です。

### 1. docker-credential-pass の活用

パスワードを平文で保存しないために、`docker-credential-pass` などのヘルパーツールを使います。
これを使えば、GPGという仕組みでパスワードを強力に暗号化して保存でき、Devcontainerはそこから安全にパスワードを読み取ります。

### 2. CI/CDには「ロボットアカウント」を使う

自動化されたCI/CDパイプラインからHarborにアクセスする際は、個人のパスワードを使ってはいけません。
Harborの**「ロボットアカウント」**機能を使います。
これは、Harborの画面にはログインできない「システム専用のアカウント」です。

「イメージのPushとPullしかできない」といった権限を絞ることができ、トークン（パスワード）の有効期限も設定できるため、万が一漏洩しても被害を最小限に抑えられます。

## まとめ：Harborで安全なソフトウェアサプライチェーンを

* **Trivy統合:** イメージをアップロードするだけで自動で脆弱性チェック。
* **SBOM生成:** コンプライアンスに必要な部品表を自動で作成。
* **Cosign署名:** 改ざんを防止し、安全なイメージだけを利用。
* **ロボットアカウント:** セキュリティを保ったままCI/CDを自動化。

DevcontainerとHarborを組み合わせることで、開発スピードとセキュリティを両立する、最新鋭のクラウドネイティブ開発環境が完成します。

### 次のステップ：自社環境に導入しよう

Harborを構築し、セキュアなコンテナ環境を手に入れたいとお考えですか？
自社インフラへのインストールからCI/CDの構築まで、専門のエンジニアがサポートするプランもご用意しています。

👉 ** 高品質なクラウドインフラ・導入サポートのお問い合わせはこちら**


