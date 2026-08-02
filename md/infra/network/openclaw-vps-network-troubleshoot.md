---
title: "OpenClaw復旧ガイド｜VPSネットワークの『見えない壁』を突破せよ"
date: "2026-04-24"
category: "infra"
description: "「名前解決はできるのにWebアクセスが落ちる」――VPS特有のパケットフィルター制約とOpenClaw通信エラーを根本から解決する、診断と復旧の全手順。"
themes: ["infra:network", "infra:vps", "other:troubleshoot"]
updated: "2026-08-02"
---

# OpenClaw復旧ガイド｜VPSネットワークの『見えない壁』を突破せよ

## 超要約
VPS（ConoHa, さくらのVPS, DigitalOcean等）上で [OpenClaw](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="OpenClaw") などの [AIエージェント](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AIエージェント") スキルを稼働させている際、「SSHやDNS名前解決は成功するが、HTTPS通信（Outbound 443）がタイムアウトする」問題が発生します。本稿では、OS内ファイアウォール（ufw/iptables）を超えたVPS事業者コントロールパネル上のインフラ層パケットフィルター遮断の切分けと復旧手順を完全解説します。

---

## 1. 診断の鉄則：なぜ『名前解決 (UDP 53)』だけが成功するのか？

- **UDP 53 (DNS)**: VPS内部およびリゾルバ通信用に標準でアウトバウンド開放。
- **TCP 80/443 (HTTP/HTTPS)**: クラウド・VPS管理層のセキュリティグループ/パケットフィルター初期設定により、ステートフル通信の戻りパケットや特定ポートがブロックされているケース。

「`nslookup` が成功する ＝ インターネット疎通OK」と誤解せず、レイヤー別に階層診断を行うことが鉄則です。

---

## 2. 三段階の診断手順 (DNS ➔ TCP 443 ➔ OpenClaw Auth)

### STEP 1：DNS（UDP 53）の確認
```bash
nslookup google.com
```

### STEP 2：TCP 443 疎通確認（接続タイムアウト判定）
```bash
curl -v --connect-timeout 5 https://www.google.com
```
*`Connected` が返るか `Connection timed out` になるかで、パケットフィルターの遮断を特定。*

### STEP 3：OpenClaw デバイス認可状態の確認
```bash
openclaw devices list
```

---

## 3. 根本解決策と環境復旧手順

1. **VPSコントロールパネルでの「パケットフィルター / セキュリティグループ」変更**: 
   OS側の `ufw` / `iptables` 許可のみならず、VPS事業者のWebコンソールから「Inbound/Outbound TCP 80, 443」を明示的に許可。
2. **DNS リゾルバの信頼性向上**:
   `/etc/resolv.conf` にパブリックDNS (`8.8.8.8`, `1.1.1.1`) を追記。
3. **OpenClaw デバイス認可コマンド再実行**:
   ```bash
   openclaw devices approve <REQUEST_ID>
   ```

---

## 4. まとめ

1. **インフラ層の疑い**: OS設定だけでなく上位のクラウド・VPSフィルターを必ず確認。
2. **L4-L7 段階診断**: UDP53 ➔ TCP443 ➔ アプリケーション認証 の順で切り分け。
3. **自律エージェントの安定化**: 堅牢なネットワーク疎通の上でAIスキルを駆動。

---

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のOpenClaw CLI, VPSインフラ層パケットフィルター、TCP/UDP段階診断のファクトチェックと目次H2構造最適化。
- **2026-04-24 (v2)**: SEOトップ1%戦略に基づきリライト。
- **2026-04-09 (v1)**: 初版作成。
