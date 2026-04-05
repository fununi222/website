---
title: "OpenClaw 外部通信[トラブルシュート](../glossary/index.html)（VPS編）"
date: "2026-04-06"
category: "Network"
description: "VPS パケットフィルター制約による fetch failed を切り分け、復旧まで整理。"
---

# 【技術レポート】OpenClaw 外部通信疎通トラブルシュート
<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono mt-2">Last Updated: 2026-04-06</div>
## ～ VPS 環境におけるパケットフィルターの罠と解決策 ～

本レポートでは、XServer VPS 環境に **OpenClaw** を構築する際、ブラウザ操作（`browser-js`）や外部通信が `fetch failed` で失敗する問題の特定と解決プロセスを記録します。

## 1. 発生した現象と環境
- **対象:** OpenClaw v2026.4.1 (Running on XServer VPS / Ubuntu)
- **現象:**
  - `openclaw skills check` ではツールが `Ready` と表示される。
  - エージェントがブラウザ（`browser-js`）を起動しても、外部サイトへのアクセスがすべてタイムアウトまたは `fetch failed` になる。
  - サーバー内からの `curl` も無反応。ただし `nslookup`（名前解決）のみ成功する。

## 2. トラブルの主因：VPS 固有のパケットフィルター
今回の最大の問題は、OS 内部の設定ではなく、**VPS 事業者側（インフラ層）のパケットフィルター仕様**にありました。

### インフラ・レイヤー：双方向遮断の壁
XServer VPS のパケットフィルターが「ON」の場合、許可したポート（デフォルトでは SSH 用の 22番など）以外の通信を**双方向で遮断**します。

- **DNS（UDP 53）が通った理由:** 多くの VPS プロバイダーでは管理用に 53番ポートをデフォルトで開放しているため、名前解決までは成功します。
- **HTTP/HTTPS（TCP 80/443）が死んだ理由:** サーバーから外へリクエストを投げた際、その「戻りパケット」がフィルターに阻まれます。一般的な PC やホームルーター（ステートフル・インスペクション機能付き）では自動で許可される通信ですが、**厳格な VPS のパケットフィルターでは「戻り」も明示的な許可、あるいはフィルターの全解除が必要**になります。

> **PC ユーザーとの違い:**
> ローカル PC や Mac で OpenClaw を動かす場合、通常は NAT 内側にいるためこの問題は発生しません。これは VPS という「インターネット直結の仮想サーバー」特有の制約です。

## 3. 解決までのステップ

### ステップ1：権限（Scope）の解放
OpenClaw 2026 以降、外部インターフェース（Discord 等）からの操作には明示的な書き込み権限が必要です。

```bash
openclaw devices list
openclaw devices approve <REQUEST_ID>
```

### ステップ2：DNS の安定化
外部通信の信頼性を高めるため、名前解決の参照先を Google 公開 DNS に固定します。

```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

### ステップ3：インフラ・フィルターの開放（最重要）
XServer VPS 管理パネルにて以下のいずれかを実施します。
1. **「パケットフィルター」を一時的に OFF に設定。**
2. **「TCP 80 / 443」を接続許可ポートとして追加。**

## 4. 診断用コマンド（疎通確認のベストプラクティス）

```bash
# 1. DNSが引けるか（UDP 53の確認）
nslookup google.com

# 2. ポートが空いているか（TCPハンドシェイクの確認）
curl -v --connect-timeout 5 https://www.google.com
```

## 5. 結論
今回のケースでは、AI モデル（LLM）の能力不足ではなく、純粋な**ネットワーク・インフラの制約**がボトルネックとなっていました。実際、OpenClaw は `gemini-3.1-flash-lite-preview` のような軽量モデルでも、インフラが適切に整っていれば十分に高度なツール操作を実行可能です。

VPS での構築においては、**「サーバーの SSH ポートが開いている ＝ 外の世界と通信できる」ではない** という点に留意する必要があります。


## 変更履歴 (Changelog)
- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデートを実施。
