---
title: "三井住友カード×Revolut 攻略ダッシュボード"
date: "2026-04-09"
category: "Finance"
description: "「100万円修行」を効率的に達成するための最適解。ブランド別手数料回避術とチャージ残高の高還元ルートをインタラクティブに整理。"
---

<div class="text-[10px] text-emerald-500 opacity-60 text-right mb-6 tracking-widest font-mono">Interactive Guide: v2024.04</div>

# 三井住友カード × Revolut 攻略ダッシュボード

## 超要約
[三井住友カード](article.html?md=glossary/system-glossary.md#:~:text="三井住友カード")から[Revolut](article.html?md=glossary/system-glossary.md#:~:text="Revolut")へのチャージは、2024年6月の手数料改定により、**Mastercardブランドなら完全無料**、**VisaブランドでもOliveデビットモードなら無料**で修行（100万円利用）にカウント可能です。本ダッシュボードでは、お持ちのブランドに応じた最適設定と、チャージ後の「高還元な出口戦略」をシミュレートできます。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

---

<section class="mb-12 bg-surface-container rounded-2xl border border-white/5 overflow-hidden shadow-xl">
<div class="p-6 sm:p-8">
<div class="mb-6">
<h2 class="text-xl font-bold flex items-center gap-3 mb-2">
<span class="material-symbols-outlined text-emerald-500">payments</span>
STEP 1: カードブランド別 手数料シミュレーター
</h2>
<p class="text-[11px] text-on-surface-variant leading-relaxed">
お持ちの三井住友カード（またはOlive）のブランドを選択してください。[Revolut](article.html?md=glossary/system-glossary.md#:~:text="Revolut")へのチャージにかかる手数料と最適な設定方法をご案内します。
</p>
</div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8" id="brand-selectors">
<button data-brand="mastercard" class="brand-btn w-full py-3 px-4 rounded-xl border border-white/10 font-bold text-center transition-all duration-200 bg-surface text-on-surface-variant hover:border-emerald-500/50 hover:bg-emerald-500/5" onclick="updateBrandView('mastercard')">
Mastercard
</button>
<button data-brand="visa" class="brand-btn w-full py-3 px-4 rounded-xl border border-white/10 font-bold text-center transition-all duration-200 bg-surface text-on-surface-variant hover:border-emerald-500/50 hover:bg-emerald-500/5" onclick="updateBrandView('visa')">
Visa (通常)
</button>
<button data-brand="olive" class="brand-btn w-full py-3 px-4 rounded-xl border border-white/10 font-bold text-center transition-all duration-200 bg-surface text-on-surface-variant hover:border-emerald-500/50 hover:bg-emerald-500/5" onclick="updateBrandView('olive')">
Olive (Visa)
</button>
</div>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">

<div id="result-card" class="bg-black/20 rounded-xl p-6 border border-white/5 h-full flex flex-col justify-center transition-all duration-300">
<div class="inline-block px-3 py-1 rounded-full text-[10px] font-bold mb-3 w-max bg-emerald-500/20 text-emerald-400 tracking-widest uppercase" id="result-badge">王道ルート</div>
<h3 class="text-lg font-bold mb-2 text-on-surface" id="result-title">そのままチャージで手数料0円</h3>
<p class="text-[11px] text-on-surface-variant mb-4 leading-relaxed" id="result-desc">
2024年6月11日よりMastercardからのチャージ手数料が撤廃されました。特別な設定なしで、そのままRevolutへチャージして100万円修行のカウント対象となります。
</p>
<div class="mt-auto bg-surface p-4 rounded-lg border border-white/5 flex items-center justify-between shadow-sm">
<span class="text-[10px] font-bold text-on-surface-variant">10万円チャージ時の推定手数料</span>
<span class="text-2xl font-black text-emerald-500" id="result-fee">0 JPY</span>
</div>
</div>

<div class="bg-black/20 rounded-xl p-4 border border-white/5">
<h4 class="text-[10px] font-bold text-on-surface-variant text-center mb-4 uppercase tracking-widest">Brand Fee Comparison (per 100k)</h4>
<div class="relative h-[250px]">
<canvas id="feeChart"></canvas>
</div>
</div>

</div>
</div>
</section>

---

<section class="mb-12 bg-surface-container rounded-2xl border border-white/5 overflow-hidden shadow-xl">
<div class="p-6 sm:p-8">
<div class="mb-6">
<h2 class="text-xl font-bold flex items-center gap-3 mb-2">
<span class="material-symbols-outlined text-secondary">cached</span>
STEP 2: Revolutチャージ後の出口ルート
</h2>
<p class="text-[11px] text-on-surface-variant leading-relaxed">
[Revolut](article.html?md=glossary/system-glossary.md#:~:text="Revolut")にチャージした残高をどう使うか？お使いの端末OSによって最適な攻略ルートが異なります。
</p>
</div>

<div class="flex flex-wrap gap-2 mb-8 border-b border-white/5 pb-4">
<button data-route="android" class="route-btn px-6 py-2 rounded-full font-bold text-[10px] uppercase tracking-widest transition-all duration-200 bg-secondary text-background shadow-glow" onclick="updateRouteView('android')">
📱 Android (楽天証券)
</button>
<button data-route="iphone" class="route-btn px-6 py-2 rounded-full font-bold text-[10px] uppercase tracking-widest transition-all duration-200 bg-surface text-on-surface-variant border border-white/5 hover:bg-white/5" onclick="updateRouteView('iphone')">
🍎 iPhone / Universal
</button>
</div>

<div id="route-display" class="bg-black/20 rounded-xl p-8 border border-white/5">
<h3 class="text-sm font-bold text-on-surface mb-8 text-center tracking-normal" id="route-title">還元率維持に最適！楽天証券つみたてルート</h3>

<div class="flex flex-col md:flex-row items-center justify-between gap-4" id="flow-diagram">
<!-- Injected by JS -->
</div>

<div class="mt-10 p-6 bg-surface/50 rounded-xl text-xs text-on-surface-variant border border-emerald-500/20 border-l-4 border-l-emerald-500 leading-relaxed" id="route-note">
<!-- Injected by JS -->
</div>
</div>
</div>
</section>

---

<section class="bg-surface-container border border-amber-500/30 rounded-2xl shadow-xl overflow-hidden p-8 sm:p-10 mb-12">
<div class="flex flex-col md:flex-row gap-10 items-center">
<div class="md:w-2/3">
<h2 class="text-xl font-bold flex items-center gap-3 mb-4 text-amber-500">
<span class="material-symbols-outlined">lightbulb</span>
ポイ活ガチ勢に「Androidサブ機」が必須な理由
</h2>
<p class="text-[11px] text-on-surface-variant mb-6 leading-relaxed">
iPhoneユーザーであっても、おサイフケータイ対応のAndroid端末（中古サブ機）を1台持つことが強く推奨されます。上記の「[楽天Edy](article.html?md=glossary/system-glossary.md#:~:text="楽天Edy") ➡️ [楽天キャッシュ](article.html?md=glossary/system-glossary.md#:~:text="楽天キャッシュ")」ルートは、AndroidのFeliCa機能がないと物理的に実行不可能なためです。
</p>
<ul class="space-y-3 text-[11px] text-on-surface leading-loose">
<li class="flex items-start gap-3">
<span class="material-symbols-outlined text-emerald-500 text-sm">check_circle</span>
<span><strong>SIM契約不要：</strong> 自宅のWi-Fiやテザリングで運用可能。月額維持費は完全に0円。</span>
</li>
<li class="flex items-start gap-3">
<span class="material-symbols-outlined text-emerald-500 text-sm">check_circle</span>
<span><strong>MNPキャンペーン活用：</strong> IIJmioやワイモバイルのMNP契約なら、最新エントリーモデルが一括1円〜で購入可能です。</span>
</li>
</ul>
</div>
<div class="md:w-1/3 bg-black/30 p-6 rounded-2xl border border-white/5 w-full">
<h3 class="font-bold text-[10px] text-on-surface-variant mb-4 text-center border-b border-white/10 pb-3 uppercase tracking-widest">Typical MNP Bargains</h3>
<div class="space-y-3 text-[11px]">
<div class="flex justify-between items-center bg-surface p-2.5 rounded-lg border border-white/5">
<span class="font-bold">IIJmio</span>
<span class="text-amber-500 font-bold">110 JPY〜</span>
</div>
<div class="flex justify-between items-center bg-surface p-2.5 rounded-lg border border-white/5">
<span class="font-bold">Y!mobile</span>
<span class="text-amber-500 font-bold">1 JPY</span>
</div>
<div class="flex justify-between items-center bg-surface p-2.5 rounded-lg border border-white/5">
<span class="font-bold">Rakuten</span>
<span class="text-amber-500 font-bold">Effective Free</span>
</div>
</div>
</div>
</div>
</section>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const contentData = {
    brands: {
        mastercard: {
            badge: "王道ルート",
            badgeColor: "bg-emerald-500/20 text-emerald-400",
            title: "そのままチャージで手数料0円",
            desc: "2024年6月11日よりMastercardからのチャージ手数料が撤廃されました。特別な設定なしで、そのままRevolutへチャージして100万円修行のカウント対象となります。最もシンプルでおすすめです。",
            fee: "0 JPY",
            feeColor: "text-emerald-500",
            chartHighlight: 0
        },
        visa: {
            badge: "要注意",
            badgeColor: "bg-red-500/20 text-red-400",
            title: "1.7%の手数料が発生します",
            desc: "VisaブランドのクレジットカードとしてそのままRevolutにチャージすると、チャージ金額に対して1.7%の手数料が引かれてしまいます。100万円修行においてはこの手数料が大きな痛手となります。",
            fee: "Approx 1,700 JPY",
            feeColor: "text-red-500",
            chartHighlight: 1
        },
        olive: {
            badge: "裏ワザ",
            badgeColor: "bg-amber-500/20 text-amber-400",
            title: "デビットモード切替で手数料0円",
            desc: "Visaブランドでも、Oliveフレキシブルペイなら三井住友銀行アプリで「デビットモード」に切り替えてからチャージすることで手数料が無料になります。デビット利用分も100万円修行の対象と公式に明記されています。",
            fee: "0 JPY",
            feeColor: "text-amber-500",
            chartHighlight: 2
        }
    },
    routes: {
        android: {
            title: "還元率維持に最適！楽天Edy ➡️ 楽天キャッシュルート",
            note: "<strong>解説：</strong> Androidのおサイフケータイ機能を活用し、[楽天Edy](article.html?md=glossary/system-glossary.md#:~:text="楽天Edy")を経由して[楽天キャッシュ](article.html?md=glossary/system-glossary.md#:~:text="楽天キャッシュ")に変換するルートです。これにより、楽天証券での投信積立（月5万円まで）に充当でき、安定してポイント還元を受けつつ残高を現金化に近い形で消化できます。",
            nodes: [
                { name: "Revolut", icon: "💳", color: "bg-surface" },
                { name: "ANA Pay", icon: "✈️", color: "bg-blue-900/20" },
                { name: "楽天Edy", icon: "📱", color: "bg-red-900/20", badge: "Android FeliCa" },
                { name: "楽天Cash", icon: "💰", color: "bg-red-900/20" },
                { name: "楽天証券", icon: "📈", color: "border-primary border-2 bg-primary/5" }
            ]
        },
        iphone: {
            title: "普段使いで消費！モバイルSuica / Amazonルート",
            note: "<strong>解説：</strong> Android端末がない場合の共通ルートです。RevolutからANA Payへチャージし、そこからApple Pay / Google Payを経由してモバイルSuicaやAmazonギフト券にチャージします。日々の交通費や買い物で確実に消費するための実用的なルートです。",
            nodes: [
                { name: "Revolut", icon: "💳", color: "bg-surface" },
                { name: "ANA Pay", icon: "✈️", color: "bg-blue-900/20" },
                { name: "Pay Wallets", icon: "📱", color: "bg-surface" },
                { name: "Suica / AMZN", icon: "🛒", color: "border-primary border-2 bg-primary/5" }
            ]
        }
    }
};

let feeChart;

function initFeeChart() {
    const ctx = document.getElementById('feeChart')?.getContext('2d');
    if (!ctx) return;
    feeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mastercard', 'Visa (Stock)', 'Olive (Debit)'],
            datasets: [{
                label: 'Fee (JPY) per 100k',
                data: [0, 1700, 0],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)', 
                    'rgba(255, 255, 255, 0.05)', 
                    'rgba(255, 255, 255, 0.05)'  
                ],
                borderRadius: 6,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { backgroundColor: '#1c1917', titleFont: { size: 10 }, bodyFont: { size: 10 } }
            },
            scales: {
                y: { beginAtZero: true, max: 2000, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#a3aac4', font: { size: 9 } } },
                x: { grid: { display: false }, ticks: { color: '#dee5ff', font: { size: 10 } } }
            }
        }
    });
}

function updateBrandView(brandId) {
    const data = contentData.brands[brandId];
    if (!data) return;

    document.querySelectorAll('.brand-btn').forEach(btn => {
        btn.classList.remove('border-emerald-500/50', 'bg-emerald-500/5', 'text-on-surface');
        btn.classList.add('border-white/10', 'bg-surface', 'text-on-surface-variant');
        if (btn.dataset.brand === brandId) {
            btn.classList.add('border-emerald-500/50', 'bg-emerald-500/5', 'text-on-surface');
            btn.classList.remove('border-white/10', 'bg-surface', 'text-on-surface-variant');
        }
    });

    document.getElementById('result-badge').className = `inline-block px-3 py-1 rounded-full text-[10px] font-bold mb-3 w-max transition-all duration-300 ${data.badgeColor} tracking-widest uppercase`;
    document.getElementById('result-badge').innerText = data.badge;
    document.getElementById('result-title').innerText = data.title;
    document.getElementById('result-desc').innerText = data.desc;
    document.getElementById('result-fee').innerText = data.fee;
    document.getElementById('result-fee').className = `text-2xl font-black transition-all duration-300 ${data.feeColor}`;

    const bgColors = ['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.05)'];
    if (data.chartHighlight === 0) bgColors[0] = 'rgba(16, 185, 129, 0.8)';
    if (data.chartHighlight === 1) bgColors[1] = 'rgba(239, 68, 68, 0.8)';
    if (data.chartHighlight === 2) bgColors[2] = 'rgba(245, 158, 11, 0.8)';

    if (feeChart) {
        feeChart.data.datasets[0].backgroundColor = bgColors;
        feeChart.update();
    }
}
window.updateBrandView = updateBrandView;

function buildRouteNodes(nodes) {
    const container = document.getElementById('flow-diagram');
    if (!container) return;
    container.innerHTML = ''; 

    nodes.forEach((node, index) => {
        const nodeEl = document.createElement('div');
        nodeEl.className = `flex flex-col items-center justify-center p-4 rounded-2xl border border-white/5 shadow-lg w-full md:w-32 h-24 text-center relative ${node.color} transition-all hover:scale-105`;
        
        if (node.badge) {
            nodeEl.innerHTML += `<span class="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-amber-500 text-background text-[7px] font-bold px-2 py-0.5 rounded-full whitespace-nowrap tracking-tighter uppercase">${node.badge}</span>`;
        }

        nodeEl.innerHTML += `
            <div class="text-2xl mb-1">${node.icon}</div>
            <div class="font-bold text-[9px] text-on-surface uppercase tracking-tighter">${node.name}</div>
        `;
        container.appendChild(nodeEl);

        if (index < nodes.length - 1) {
            const arrowEl = document.createElement('div');
            arrowEl.className = 'flex items-center justify-center text-xs text-on-surface-variant opacity-30 md:rotate-0 rotate-90';
            arrowEl.innerHTML = '<span class="material-symbols-outlined">arrow_forward</span>';
            container.appendChild(arrowEl);
        }
    });
}

function updateRouteView(routeId) {
    const data = contentData.routes[routeId];
    if (!data) return;

    document.querySelectorAll('.route-btn').forEach(btn => {
        btn.classList.remove('bg-secondary', 'text-background', 'shadow-glow');
        btn.classList.add('bg-surface', 'text-on-surface-variant', 'border', 'border-white/5');
        
        if (btn.dataset.route === routeId) {
            btn.classList.add('bg-secondary', 'text-background', 'shadow-glow');
            btn.classList.remove('bg-surface', 'text-on-surface-variant', 'border-white/5');
        }
    });

    document.getElementById('route-title').innerText = data.title;
    document.getElementById('route-note').innerHTML = data.note;
    buildRouteNodes(data.nodes);
}
window.updateRouteView = updateRouteView;

setTimeout(() => {
    initFeeChart();
    updateBrandView('mastercard');
    updateRouteView('android');
}, 300);
</script>

## 変更履歴 (Changelog)
- 2026-04-09: `SKILL.md` の運用ルールに合わせ、更新日表示と更新履歴を追記。
