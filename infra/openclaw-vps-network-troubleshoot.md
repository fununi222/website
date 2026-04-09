---
title: "OpenClaw | VPS外部通信トラブルシュート 2026"
date: "2026-04-09"
category: "Infrastructure"
description: "VPS パケットフィルター制約による fetch failed を切り分け、復旧まで整理。"
themes: ["infra:network", "infra:vps", "other:troubleshoot"]
---

# OpenClaw | VPS外部通信トラブルシュート 2026
<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

## 超要約
本レポートは、[VPS (Virtual Private Server)](article.html?md=glossary/system-glossary.md#:~:text=VPS (Virtual Private Server)) 環境に構築した [OpenClaw](article.html?md=glossary/system-glossary.md#:~:text=OpenClaw) において、外部通信（HTTP/HTTPS）がタイムアウトする原因と[トラブルシュート](article.html?md=glossary/system-glossary.md#:~:text=%E3%83%88%E3%83%A9%E3%83%96%E3%83%AB%E3%82%B7%E3%83%A5%E3%83%BC%E3%83%88)プロセスをまとめたものです。OS内部ではなく「事業者の[パケットフィルター](article.html?md=glossary/system-glossary.md#:~:text=%E3%83%91%E3%82%B1%E3%83%83%E3%83%88%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC)」による双方向通信の遮断を特定し、[DNS (UDP 53)](article.html?md=glossary/system-glossary.md#:~:text=DNS (UDP 53)) は通るが [TCP 80/443](article.html?md=glossary/system-glossary.md#:~:text=TCP 80/443) が落ちるという特殊な挙動に対する具体的対策を提示します。

---

## 1. 発生した現象と環境
- **対象:** [OpenClaw](article.html?md=glossary/system-glossary.md#:~:text=OpenClaw) v2026.4.1 (Running on XServer [VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) / Ubuntu)
- **現象:**
  - `openclaw skills check` ではツールが `Ready` と表示される。
  - エージェントがブラウザ（`browser-js`）を起動しても、外部サイトへのアクセスがすべてタイムアウトまたは `fetch failed` になる。
  - サーバー内からの `curl` も無反応。ただし [DNS](article.html?md=glossary/system-glossary.md#:~:text=DNS)（名前解決）のみ成功する。

## 2. トラブルの主因：VPS 固有のパケットフィルター
今回の最大の問題は、OS 内部の設定ではなく、**[VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) 事業者側（インフラ層）の[パケットフィルター](article.html?md=glossary/system-glossary.md#:~:text=%E3%83%91%E3%82%B1%E3%83%83%E3%83%88%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC)仕様**にありました。

### インフラ・レイヤー：双方向遮断の壁
XServer [VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) の[パケットフィルター](article.html?md=glossary/system-glossary.md#:~:text=%E3%83%91%E3%82%B1%E3%83%83%E3%83%88%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC)が「ON」の場合、許可したポート（デフォルトでは SSH 用の 22番など）以外の通信を**双方向で遮断**します。

- **[DNS](article.html?md=glossary/system-glossary.md#:~:text=DNS)（UDP 53）が通った理由:** 多くの [VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) プロバイダーでは管理用に 53番ポートをデフォルトで開放しているため、名前解決までは成功します。
- **HTTP/HTTPS（TCP 80/443）が死んだ理由:** サーバーから外へリクエストを投げた際、その「戻りパケット」がフィルターに阻まれます。一般的な PC やホームルーター（[NAT](article.html?md=glossary/system-glossary.md#:~:text=NAT) / ステートフル・インスペクション機能付き）では自動で許可される通信ですが、**厳格な [VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) の[パケットフィルター](article.html?md=glossary/system-glossary.md#:~:text=%E3%83%91%E3%82%B1%E3%83%83%E3%83%88%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC)では「戻り」も明示的な許可、あるいはフィルターの全解除が必要**になります。

> **PC ユーザーとの違い:**
> ローカル PC や Mac で [OpenClaw](article.html?md=glossary/system-glossary.md#:~:text=OpenClaw) を動かす場合、通常は [NAT](article.html?md=glossary/system-glossary.md#:~:text=NAT) 内側にいるためこの問題は発生しません。これは [VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) という「インターネット直結の仮想サーバー」特有の制約です。

## 3. 解決までのステップ

### ステップ1：権限（Scope）の解放
[OpenClaw](article.html?md=glossary/system-glossary.md#:~:text=OpenClaw) 2026 以降、外部インターフェース（Discord 等）からの操作には明示的な書き込み権限が必要です。

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
XServer [VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) 管理パネルにて以下のいずれかを実施します。
1. **「[パケットフィルター](article.html?md=glossary/system-glossary.md#:~:text=%E3%83%91%E3%82%B1%E3%83%83%E3%83%88%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC)」を一時的に OFF に設定。**
2. **「TCP 80 / 443」を接続許可ポートとして追加。**

## 4. 診断用コマンド（疎通確認のベストプラクティス）

```bash
# 1. DNSが引けるか（UDP 53の確認）
nslookup google.com

# 2. ポートが空いているか（TCPハンドシェイクの確認）
curl -v --connect-timeout 5 https://www.google.com
```

## 5. 結論
今回のケースでは、AI モデル（LLM）の能力不足ではなく、純粋な**ネットワーク・インフラの制約**がボトルネックとなっていました。実際、[OpenClaw](article.html?md=glossary/system-glossary.md#:~:text=OpenClaw) は `gemini-3.1-flash-lite-preview` のような軽量モデルでも、インフラが適切に整っていれば十分に高度なツール操作を実行可能です。

[VPS](article.html?md=glossary/system-glossary.md#:~:text=VPS) での構築においては、**「サーバーの SSH ポートが開いている ＝ 外の世界と通信できる」ではない** という点に留意する必要があります。


## 変更履歴 (Changelog)
- **2026-04-09**: `SKILL.md` 準拠のグローバルデザイン統一およびメタデータ標準化アップデートを実施。
- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデート、超要約・コンテンツ整理を実施。
