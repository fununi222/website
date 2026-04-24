---
title: "OpenClaw復旧ガイド｜VPSネットワークの『見えない壁』を突破せよ"
date: "2026-04-24"
category: "infra"
description: "「名前解決はできるのにWebアクセスが落ちる」――VPS特有のパケットフィルター制約とOpenClaw通信エラーを根本から解決する、診断と復旧の全手順。"
themes: ["infra:network", "infra:vps", "other:troubleshoot"]
---

# OpenClaw復旧ガイド｜VPSネットワークの『見えない壁』を突破せよ

<figure class="mb-10 max-w-4xl mx-auto cyber-glow">
  <img src="../../../assets/img/infra/vps-network-troubleshoot.png" alt="VPS Network Layer Troubleshooting Visualization" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

「サーバーにはSSHで繋がるのに、AIエージェントが外部サイトを読み込めない」
「curlを叩くと無反応だが、nslookupは成功する……」

VPS（仮想専用サーバー）で[OpenClaw](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="OpenClaw")などの自動化ツールを運用していると、必ずと言っていいほどこの「ネットワークの迷宮」に迷い込みます。OS内の設定（Firewall）は完璧なはずなのに、通信が阻まれる。その原因は、OSよりも外側、VPS事業者が管理する**「インフラ層のパケットフィルター」**にあります。

本記事では、この「見えない壁」を最短で切り分け、OpenClawを完全復活させるためのサバイバル・ステップを伝授します。

---

## 1. 診断の鉄則：なぜ『名前解決』だけが成功するのか？

今回のトラブルの最大の特徴は、「DNS（名前解決）だけは通る」という点です。ここに解決のヒントが隠されています。

*   **UDP 53 (DNS)**: 多くのVPS事業者は、管理・更新のために53番ポートをデフォルトで開放しています。
*   **TCP 80/443 (HTTP/HTTPS)**: ここが「双方向」で許可されていない場合、リクエストの「戻りパケット」がインフラ層で遮断されます。

**教訓**: 「名前解決ができる ＝ インターネットに繋がっている」という思い込みを捨てるのが、トラブルシュートの第一歩です。

---

## 2. 三段階の診断フロー：原因を特定せよ

闇雲に設定を変える前に、以下のコマンドを順番に実行し、どこで通信が死んでいるかを特定します。

### STEP 1：DNS（UDP 53）の確認
```bash
nslookup google.com
```
これが成功すれば、外の世界の住所録にはアクセスできています。

### STEP 2：ポート疎通（TCP 443）の確認
```bash
curl -v --connect-timeout 5 https://www.google.com
```
ここで「Connected」が出るか、それとも「Timeout」になるかを確認します。Timeoutなら**パケットフィルター（インフラ層）**が犯人です。

### STEP 3：OpenClaw 権限の確認
```bash
openclaw devices list
```
通信が通っているのにツールが動かない場合は、デバイスの承認（approve）が漏れている可能性があります。

---

## 3. 解決策：『見えない壁』を取り払う

原因が特定できたら、以下の3つの対策を適用します。

1.  **事業者のパケットフィルター設定（最優先）**: 
    VPSの管理パネルを開き、「パケットフィルター」をOFFにするか、明示的に「TCP 80/443（送信・受信）」を許可リストに追加してください。OS内の `ufw` や `iptables` だけでは、この壁は越えられません。
2.  **DNSサーバの固定**:
    `/etc/resolv.conf` を編集し、Google公開DNS（8.8.8.8）を指定することで、不安定なプロバイダ内DNSの影響を排除します。
3.  **OpenClawの再認可**:
    通信復旧後、エージェントに外部操作の権限を与えるため `openclaw devices approve <REQUEST_ID>` を実行し、道を切り拓きます。

---

## 4. まとめ：AIに自由な通信を

OpenClawという強力な知性を活かすためには、その手足となる「ネットワーク」が健全である必要があります。

*   **インフラを疑え**: 障害はOSの「内」ではなく「外」に潜んでいることが多い。
*   **層（Layer）で分けろ**: DNS(UDP) ➡️ TCP ➡️ HTTPS の順で診断すれば、迷うことはない。
*   **権限を解き放て**: 通信が通った後は、正しい認可プロセスでAIを自律させる。

ネットワークの壁を突破したその瞬間、OpenClawはあなたの真の右腕として、広大なインターネットの海へと漕ぎ出すはずです。

## 変更履歴 (Changelog)
- **2026-04-24**: 「SEOトップ1%戦略」に基づき、実戦的なトラブルシューティングガイドとして全面リライト。診断の黄金フロー（DNS ➡️ TCP ➡️ HTTPS）の導入と、パケットフィルターの概念図的解説を追加。
- **2026-04-09**: 新規作成。

