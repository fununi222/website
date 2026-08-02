---
title: "OpenClaw | Yahoo!リアルタイム検索を活用した動的スキルの構築"
date: "2026-04-09"
category: "ai"
description: "X APIの高騰を回避し、Yahoo!リアルタイム検索をデータソースとして活用するAIエージェントスキルの実装ガイド。"
themes: ["ai:agent", "ai:tool-integration", "ai:automation"]
updated: "2026-08-02"
---

# OpenClaw | Yahoo!リアルタイム検索を活用した動的スキルの構築

## 超要約
[X](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="X") [API](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="API") の高額な費用やアカウント制約、凍結リスクを回避し、Yahoo!リアルタイム検索をデータソースとして活用する [OpenClaw](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="OpenClaw") ベースの [AIエージェント](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="AIエージェント") スキル構築ガイドです。[Playwright](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="Playwright") によるスクレイピングと [LLM](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="LLM") による構造化抽出を組み合わせ、重要告知やトレンド情報を自動要約するシステムを構築します。

---

## 1. 手法の比較分析 (X API vs Yahoo! リアルタイム検索)

| 比較項目 | 公式 X API (Basic/Pro) | Yahoo! リアルタイム検索 + OpenClaw |
| :--- | :--- | :--- |
| **月額利用コスト** | $100 ~ $5,000 /月 | **$0 (完全無料)** |
| **認証・レートリミット** | 厳格なAPI Key / OAuth 認証 | ログイン不要 (Playwright Headless) |
| **検索精度 & 速度** | 制限あり (取得ポスト数制限) | 高速インデックス・ユーザー指定検索可能 |
| **アカウント凍結リスク** | 規約改定による突然のアクセス遮断リスク | 自律スクレイピングによる安全なデータ収集 |

---

## 2. スキル実装コード（Python & Playwright）

OpenClawに組み込むPlaywrightベースの検索・取得スクリプトの実装例です。

```python
# OpenClaw Agent Skill: Yahoo! Realtime Search Collector (2026)
import asyncio
from playwright.async_api import async_playwright
import json

async def search_realtime(query: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = f"https://search.yahoo.co.jp/realtime/search?p={query}"
        await page.goto(url)
        await page.wait_for_selector(".Tweet_tweet__Container")
        
        tweets = []
        elements = await page.query_selector_all(".Tweet_tweet__Container")
        for el in elements[:10]:
            text = await el.inner_text()
            tweets.append(text)
            
        await browser.close()
        return tweets

# Run search
# results = asyncio.run(search_realtime("OpenAI id:OpenAI"))
```

---

## 3. 情報フィルタリングの階層構造

1. **生データ収集**: Playwright経由でYahoo!リアルタイム検索結果をDOM取得。
2. **ノイズ除去**: あいさつ・日常雑談・スパムポストを正規表現/LLMでカット。
3. **重要告知の抽出**: イベント、更新告知、障害情報をLLMで構造化JSON化。

---

<script>
document.addEventListener('sme-loaded', () => { initOpenClawSkill(); });
setTimeout(initOpenClawSkill, 200);

function initOpenClawSkill() {
  if (window._initOpenClawDone) return;
  window._initOpenClawDone = true;

  window.switchOpenClawTab = (showId, hideId, btn) => {
    const showEl = document.getElementById(showId);
    const hideEl = document.getElementById(hideId);
    if (showEl && hideEl) {
      showEl.classList.remove('hidden');
      hideEl.classList.add('hidden');
    }
  };
}
</script>

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年最新のPlaywright async API、Yahoo!リアルタイム検索DOMセレクタ、OpenClawスキル定義のファクトチェック。
- **2026-04-09 (v2)**: メタデータおよびインターフェースデザイン標準化。
- **2026-04-06 (v1)**: 新規作成。
