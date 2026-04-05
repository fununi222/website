---
title: "OSSを活用したインフラ運用の自動化"
date: "2026-04-03"
category: "Infrastructure"
description: "AnsibleやTerraform、独自開発の自動化ツールを組み合わせたインフラ運用の効率化。"
---

# OSS Infrastructure Automation & Monitoring - リサーチまとめ

## 1. 自動化・構成管理 (IaC)
* **Ansible**: エージェントレスでvSphere環境とも相性が良く、プレイブックの可読性が高い。定型作業の自動化に最適。
* **Terraform**: vSphere Providerを利用したインフラのコード化に必須。宣言的な管理が可能。
* **Pulumi**: PythonやTypeScriptでインフラ定義ができるため、インフラエンジニアが慣れ親しんだ言語で記述可能。

## 2. 監視・可観測性 (Observability)
* **Prometheus + Grafana**: モダンなメトリクス監視のデファクト。vSphere Exporterを組み合わせることでVMのメトリクスを収集可能。
* **Zabbix**: 伝統的な監視システム。トリガー設定やアクション（通知・スクリプト実行）が強力で、レガシー環境との親和性が高い。
* **Netdata**: 軽量・リアルタイム監視。ボトルネック調査の初動確認に非常に強力。

## 3. 次の一手：AI活用への統合
* **Local LLM (Ollamaなど)**: 監視ログをLLMに食わせて「正常性判断」をさせるPoCは非常に興味深い。
* **n8n**: ワークフロー自動化OSS。GitHubや監視ツールと連携させ、異常検知時にSlackやTeamsへ自動通知・自動是正を流すハブとして優秀。

## 今後の検討方針
1. **まずはTerraform/Ansibleでの構成管理を固める**
2. **Prometheus + Grafanaで可視化を強化**
3. **n8nを組み合わせて、検知後の初動対応を自動フロー化する**
