---
title: "2026年3月投資まとめ：地獄の1ヶ月ダッシュボード"
date: "2026-04-09"
category: "finance"
description: "3月の歴史的急落局面をデータで可視化。日経平均、実質賃金、金と原油の逆転現象から読み解く生存戦略。"
themes: ["finance:market", "finance:macro", "finance:asset"]
updated: "2026-08-02"
---

# 2026年3月投資まとめ：地獄の1ヶ月を生き抜くダッシュボード

## 超要約
画面が市場の急落で埋め尽くされた3月。[日経平均](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="日経平均") は約13%の暴落を記録しましたが、その背後では13ヶ月ぶりの「[実質賃金](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="実質賃金") プラス転換」という歴史的変化も起きています。有事に強いはずの「金（ゴールド）」と「原油（コモディティ）」の資金流動バランスの変化を読み解き、長期資産形成のための論理的な現状把握を行います。

---

## 1. 衝撃：日経平均 約13%の歴史的暴落

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start my-8">
<div class="bg-surface-container rounded-2xl p-6 border border-white/5 shadow-inner">
<h3 class="text-center font-bold text-on-surface-variant text-xs uppercase tracking-widest mb-6 font-headline">Nikkei 225 Performance (Mar 2026)</h3>
<div class="relative h-[250px]">
<canvas id="nikkeiChart"></canvas>
</div>
<div class="text-center mt-6 text-rose-500 font-black text-2xl tracking-tighter">
58,851 JPY <span class="text-xs opacity-50 px-2 font-normal">📉</span> 51,064 JPY
</div>
</div>

<div class="space-y-4">
<h3 class="font-bold text-xs text-on-surface-variant uppercase tracking-widest mb-4 font-headline">暴落を招いた「3つのマクロ要因」</h3>

<div class="group border border-white/5 rounded-xl transition-all hover:border-white/10 overflow-hidden">
<button class="w-full text-left p-4 flex justify-between items-center bg-surface-container/50 hover:bg-surface-container transition-colors" onclick="toggleAccordion('logic-1')">
<span class="text-xs font-bold text-on-surface">⚠️ 1. 中東地政学リスクと投資家回避心理</span>
<span class="material-symbols-outlined text-sm opacity-50 transition-transform" id="arrow-logic-1">expand_more</span>
</button>
<div class="hidden p-4 text-[10px] text-on-surface-variant leading-relaxed bg-black/20" id="logic-1">
地政学的緊迫化の継続により、リスク資産からの資金引き上げ（Risk-off）が世界的に加速しました。
</div>
</div>

<div class="group border border-white/5 rounded-xl transition-all hover:border-white/10 overflow-hidden">
<button class="w-full text-left p-4 flex justify-between items-center bg-surface-container/50 hover:bg-surface-container transition-colors" onclick="toggleAccordion('logic-2')">
<span class="text-xs font-bold text-on-surface">🛢️ 2. ホルムズ海峡懸念と原油サプライチェーンショック</span>
<span class="material-symbols-outlined text-sm opacity-50 transition-transform" id="arrow-logic-2">expand_more</span>
</button>
<div class="hidden p-4 text-[10px] text-on-surface-variant leading-relaxed bg-black/20" id="logic-2">
エネルギー輸送ルートの不透明感から原油先物が急騰。企業の製造・物流コスト増による業績圧迫が懸念されました。
</div>
</div>

<div class="group border border-white/5 rounded-xl transition-all hover:border-white/10 overflow-hidden">
<button class="w-full text-left p-4 flex justify-between items-center bg-surface-container/50 hover:bg-surface-container transition-colors" onclick="toggleAccordion('logic-3')">
<span class="text-xs font-bold text-on-surface">📈 3. コストプッシュ型インフレと政策金利懸念</span>
<span class="material-symbols-outlined text-sm opacity-50 transition-transform" id="arrow-logic-3">expand_more</span>
</button>
<div class="hidden p-4 text-[10px] text-on-surface-variant leading-relaxed bg-black/20" id="logic-3">
原油高に伴う物価上昇（[インフレ](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="インフレ")）圧力により、中央銀行の金利引き上げ観測が強まり株価の重石となりました。
</div>
</div>
</div>
</div>

---

## 2. 光：13ヶ月ぶりの快挙「実質賃金」プラス転換

<div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center my-8">
<div class="flex flex-col space-y-4 order-2 lg:order-1">
<div class="p-5 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl border-l-4 border-l-emerald-500">
<h4 class="font-bold text-emerald-400 mb-2 text-sm italic">🍙 「おにぎり」で例える実質賃金</h4>
<p class="text-[11px] text-on-surface leading-loose">以前： おにぎり100円→102円。給料は100円のまま。<br><span class="text-[9px] opacity-60">（購買力の低下＝実質賃金マイナス）</span></p>
<p class="text-[11px] text-on-surface leading-loose">現在： おにぎり102円。給料は103円に増加。<br><span class="text-[10px] font-bold text-emerald-400">（購買力の拡大＝実質賃金プラス転換！）</span></p>
</div>
<p class="text-[11px] text-on-surface-variant leading-relaxed">
生鮮食品を除外した **「[コアCPI](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="コアCPI")（[消費者物価指数](https://fununi222.github.io/website/html/glossary/system-glossary.html#:~:text="消費者物価指数")）」** が落ち着いたことがプラス転換の大きな要因です。
</p>
</div>

<div class="bg-surface-container rounded-2xl p-6 border border-white/5 shadow-inner order-1 lg:order-2">
<h3 class="text-center font-bold text-on-surface-variant text-xs uppercase tracking-widest mb-6 font-headline">Real Wage Index (Y-o-Y %)</h3>
<div class="relative h-[220px]">
<canvas id="wagesChart"></canvas>
</div>
</div>
</div>

---

## 3. アセットアロケーション：有事の金 vs 実利の原油

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-8">
<div class="bg-surface-container p-6 rounded-2xl border border-white/5">
<h3 class="font-bold text-yellow-400 mb-3">金（Gold）の動向</h3>
<p class="text-xs text-on-surface-variant leading-relaxed">
有事の安全資産とされる金ですが、急速な米金利高止まりや利益確定売りにより一時的な調整局面を経験。長期的にはインフレヘッジとしての価値を維持。
</p>
</div>
<div class="bg-surface-container p-6 rounded-2xl border border-white/5">
<h3 class="font-bold text-amber-500 mb-3">原油（Commodity）の動向</h3>
<p class="text-xs text-on-surface-variant leading-relaxed">
実需リスクに直結する原油はボラティリティが上昇。エネルギーセクターや資源関連銘柄への資金シフトが見られました。
</p>
</div>
</div>

---

<script>
document.addEventListener('sme-loaded', () => { initMarketDashboard(); });
setTimeout(initMarketDashboard, 200);

function initMarketDashboard() {
  if (window._initMarketDashDone) return;
  window._initMarketDashDone = true;

  window.toggleAccordion = (id) => {
    const el = document.getElementById(id);
    const arrow = document.getElementById('arrow-' + id);
    if (el) {
      el.classList.toggle('hidden');
      if (arrow) arrow.style.transform = el.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
    }
  };

  if (typeof Chart !== 'undefined') {
    const nikkeiCtx = document.getElementById('nikkeiChart');
    if (nikkeiCtx) {
      new Chart(nikkeiCtx.getContext('2d'), {
        type: 'line',
        data: {
          labels: ['3/1', '3/8', '3/15', '3/22', '3/31'],
          datasets: [{
            label: '日経平均株価',
            data: [58851, 56200, 53400, 51800, 51064],
            borderColor: '#f43f5e',
            backgroundColor: 'rgba(244, 63, 94, 0.1)',
            fill: true,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }
        }
      });
    }

    const wagesCtx = document.getElementById('wagesChart');
    if (wagesCtx) {
      new Chart(wagesCtx.getContext('2d'), {
        type: 'bar',
        data: {
          labels: ['11月', '12月', '1月', '2月', '3月'],
          datasets: [{
            label: '実質賃金 前年比(%)',
            data: [-1.2, -0.8, -0.4, -0.1, 0.4],
            backgroundColor: ['#f43f5e','#f43f5e','#f43f5e','#f43f5e','#10b981'],
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }
        }
      });
    }
  }
}
</script>

## 変更履歴 (Changelog)
- **2026-08-02 (v3)**: 2026年3月マクロ経済動向、日経平均推移、実質賃金・CPI指標のファクトチェックと目次H2見出し標準化。
- **2026-04-09 (v2)**: グローバルデザインおよびインタラクティブアコーディオン適用。
- **2026-04-06 (v1)**: 新規作成。
