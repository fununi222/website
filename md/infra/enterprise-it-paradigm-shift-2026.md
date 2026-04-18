---
title: "Enterprise IT 2026 | 4つの定説とパラダイムシフト"
date: "2026-04-09"
category: "infra"
description: "クラウド、AI翻訳、AIエージェント、AI防御をめぐる4つの定説を再検証するインタラクティブ分析。"
themes: ["infra:strategy", "infra:cloud", "ai:enterprise"]
---

# Enterprise IT 2026 | 4つの定説とパラダイムシフト

## 超要約
2026年のエンタープライズITでは、クラウド、AI翻訳、AIエージェント、AIセキュリティをめぐる「わかりやすい定説」が、現場ではそのまま通用しなくなっています。本記事は4つの神話を「神話 vs 現実」で比較しながら、次世代IT戦略に必要な前提を整理します。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

---

<style>
.paradigm-shell {
  --ps-border: rgba(255,255,255,0.08);
  --ps-panel: rgba(15, 23, 42, 0.62);
  --ps-panel-strong: rgba(15, 23, 42, 0.9);
  --ps-accent: #d6a37f;
  --ps-accent-deep: #b87c5e;
}
.paradigm-shell .ps-panel {
  background: var(--ps-panel);
  border: 1px solid var(--ps-border);
  backdrop-filter: blur(16px);
  box-shadow: 0 24px 60px rgba(2, 6, 23, 0.32);
}
.paradigm-shell .ps-panel-strong {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.82));
  border: 1px solid var(--ps-border);
  backdrop-filter: blur(18px);
}
.paradigm-shell .ps-content-section {
  display: none;
  animation: psFade 0.3s ease-in-out;
}
.paradigm-shell .ps-content-section.active {
  display: block;
}
.paradigm-shell .ps-nav-item,
.paradigm-shell .ps-arch-btn {
  transition: all 0.22s ease;
}
.paradigm-shell .ps-nav-item.active {
  background: linear-gradient(90deg, rgba(214, 163, 127, 0.18), rgba(214, 163, 127, 0.04));
  border-left: 4px solid var(--ps-accent-deep);
  font-weight: 700;
  color: #f8fafc;
}
.paradigm-shell .ps-chart-container {
  position: relative;
  width: 100%;
  max-width: 720px;
  margin-inline: auto;
  height: 300px;
}
@media (min-width: 768px) {
  .paradigm-shell .ps-chart-container {
    height: 350px;
  }
}
@keyframes psFade {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<div class="paradigm-shell max-w-6xl mx-auto py-8">
<div class="ps-panel-strong rounded-[30px] p-6 md:p-8 mb-8 relative overflow-hidden">
<div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(214,163,127,0.18),transparent_32%),radial-gradient(circle_at_bottom_right,rgba(110,231,183,0.12),transparent_28%)] pointer-events-none"></div>
<div class="relative z-10">
<div class="text-[10px] uppercase tracking-[0.3em] text-amber-200 font-bold mb-3">Enterprise Strategy Dashboard</div>
<h2 class="text-3xl md:text-5xl font-bold tracking-tight text-on-surface mb-4">2026年 <span class="text-[#d6a37f]">エンタープライズIT</span> パラダイムシフト</h2>
<p class="max-w-3xl text-slate-300 leading-relaxed">クラウド最適化、AI翻訳、AIエージェント、AI防御優位といった魅力的な定説は、現場運用ではしばしば条件付きです。ここでは4つの神話を、実務上の現実と並べて検証します。</p>
</div>
</div>

<div class="grid md:grid-cols-[280px,1fr] gap-6 items-start">
<nav class="ps-panel rounded-[26px] overflow-hidden">
<div class="p-6 border-b border-white/10">
<h3 class="text-xl font-bold text-on-surface leading-tight">2026年<br><span class="text-[#d6a37f]">エンタープライズIT</span><br>パラダイムシフト</h3>
</div>
<div class="py-4 text-sm">
<button class="ps-nav-item active w-full text-left px-6 py-3 text-slate-300 hover:bg-white/5" data-target="ps-intro">序論：変革期における定説の再考</button>
<button class="ps-nav-item w-full text-left px-6 py-3 text-slate-300 hover:bg-white/5" data-target="ps-myth1">神話1：クラウド至上主義の限界</button>
<button class="ps-nav-item w-full text-left px-6 py-3 text-slate-300 hover:bg-white/5" data-target="ps-myth2">神話2：AI翻訳とオフショアの錯覚</button>
<button class="ps-nav-item w-full text-left px-6 py-3 text-slate-300 hover:bg-white/5" data-target="ps-myth3">神話3：AIエージェントと技術的負債</button>
<button class="ps-nav-item w-full text-left px-6 py-3 text-slate-300 hover:bg-white/5" data-target="ps-myth4">神話4：防御優位性とAIマルウェア</button>
<button class="ps-nav-item w-full text-left px-6 py-3 text-slate-300 hover:bg-white/5" data-target="ps-conclusion">結論：次世代IT戦略</button>
</div>
</nav>

<main class="space-y-6">
<section id="ps-intro" class="ps-content-section active">
<div class="mb-8">
<span class="inline-block px-3 py-1 bg-white/10 text-slate-300 rounded-full text-xs font-semibold mb-4 tracking-wider">INTRODUCTION</span>
<h3 class="text-3xl md:text-4xl font-bold mb-6 text-on-surface">4つの「定説」を覆すパラダイムシフト</h3>
</div>
<p class="text-lg text-slate-300 leading-relaxed mb-8 ps-panel p-6 rounded-[24px] border-l-4 border-[#b87c5e]">2026年、生成AIとクラウドインフラの成熟は多くの可能性を生みましたが、同時に現場から乖離した「わかりやすい神話」も増やしました。本ダッシュボードは、それらの定説がどこで破綻し、何を前提に再設計すべきかを見直すための導線です。</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="ps-panel p-6 rounded-[22px]">
<h4 class="text-xl font-bold mb-3 text-on-surface">背景</h4>
<p class="text-slate-300 leading-relaxed">「全部クラウドへ」「AIで言語の壁は消える」「AIが負債を片付ける」といった期待は、部分的には正しいものの、適用条件を外すと逆効果になり得ます。</p>
</div>
<div class="ps-panel p-6 rounded-[22px]">
<h4 class="text-xl font-bold mb-3 text-on-surface">実態と課題</h4>
<p class="text-slate-300 leading-relaxed">実際の運用データやインシデントレポートは、コスト膨張、仕様齟齬、ブラックボックス化、バックアップ破壊といった別の問題を示しています。</p>
</div>
</div>
<div class="mt-10 text-center">
<p class="text-slate-400 mb-4">左のメニューから各神話と現実を切り替えられます。</p>
<button class="bg-[#b87c5e] text-white px-8 py-3 rounded-xl font-bold hover:bg-[#a0684c] transition-colors shadow-lg shadow-[#b87c5e]/20" data-jump="ps-myth1">データ探索を開始する</button>
</div>
</section>

<section id="ps-myth1" class="ps-content-section">
<div class="mb-8">
<span class="inline-block px-3 py-1 bg-rose-500 text-white rounded-full text-xs font-semibold mb-4 tracking-wider">MYTH 1</span>
<h3 class="text-3xl font-bold mb-6 text-on-surface">「すべてのシステムをパブリッククラウドに移行すれば最適化される」</h3>
</div>
<p class="text-lg text-slate-300 leading-relaxed mb-8 ps-panel p-6 rounded-[24px]">データ取り出し頻度が高いアクティブアーカイブ環境では、クラウドの従量課金とエグレス料金が、想定より早く財務を圧迫します。ここでは全面クラウド化の神話と、オンプレ回帰や特化型クラウドの現実を比較します。</p>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
<div class="ps-panel p-6 rounded-[22px] border-t-4 border-rose-500">
<h4 class="text-xl font-bold mb-4 text-rose-300 flex items-center gap-2"><span class="text-2xl">✖</span> 神話</h4>
<p class="text-slate-300">パブリッククラウド全面移行は、長期的に見ても常にコスト最適と俊敏性を両立する万能解である。</p>
</div>
<div class="ps-panel p-6 rounded-[22px] border-t-4 border-emerald-400">
<h4 class="text-xl font-bold mb-4 text-emerald-300 flex items-center gap-2"><span class="text-2xl">✔</span> 現実</h4>
<p class="text-slate-300">アクティブアーカイブやデータ主権要件では、固定費化しやすい特化型クラウドやオンプレ構成の方が予測可能で強いことがあります。</p>
</div>
</div>
<div class="ps-panel p-6 rounded-[24px] mb-8">
<h4 class="text-lg font-bold mb-4 text-center text-on-surface">5年間のインフラ維持コスト推移予測</h4>
<p class="text-sm text-slate-400 text-center mb-4">アクティブアーカイブ環境における累積コスト比較イメージ</p>
<div class="ps-chart-container">
<canvas id="ps-cloud-cost-chart"></canvas>
</div>
</div>
</section>

<section id="ps-myth2" class="ps-content-section">
<div class="mb-8">
<span class="inline-block px-3 py-1 bg-rose-500 text-white rounded-full text-xs font-semibold mb-4 tracking-wider">MYTH 2</span>
<h3 class="text-3xl font-bold mb-6 text-on-surface">「AI翻訳の進化で、言語の壁がなくなりオフショア開発が容易になる」</h3>
</div>
<p class="text-lg text-slate-300 leading-relaxed mb-8 ps-panel p-6 rounded-[24px]">AI翻訳は文章を流暢にしますが、ハイコンテクストな要求や暗黙知まで自動で補完してくれるわけではありません。ここでは「理解の錯覚」がどう生まれるかを、簡単な対話図で体験できます。</p>
<div class="ps-panel p-6 rounded-[24px]">
<h4 class="text-lg font-bold mb-6 text-center text-on-surface">インタラクティブ体験：「理解の錯覚」メカニズム</h4>
<div class="flex flex-col md:flex-row items-center justify-center gap-4 text-center">
<div class="w-full md:w-1/3 bg-white/5 p-4 rounded-xl border border-white/10">
<h5 class="font-bold text-sm text-slate-400 mb-2">発注側（日本）</h5>
<p class="text-sm bg-slate-950/40 p-3 rounded-lg min-h-[84px] flex items-center justify-center text-slate-200">「あの画面、いい感じでユーザーが使いやすいように適当に調整しておいて」</p>
</div>
<div class="text-2xl text-slate-500">➔</div>
<div class="w-full md:w-1/3 bg-sky-500/10 p-4 rounded-xl border border-sky-400/20 cursor-pointer hover:bg-sky-500/15 transition-colors" id="ps-translation-box">
<h5 class="font-bold text-sm text-sky-300 mb-2">AI 翻訳ツール</h5>
<p id="ps-translation-text" class="text-sm bg-slate-950/40 p-3 rounded-lg min-h-[84px] flex items-center justify-center font-mono text-slate-500">[ 翻訳を実行 ]</p>
</div>
<div class="text-2xl text-slate-500">➔</div>
<div class="w-full md:w-1/3 bg-white/5 p-4 rounded-xl border border-white/10 cursor-pointer hover:bg-white/10 transition-colors" id="ps-outcome-box">
<h5 class="font-bold text-sm text-slate-400 mb-2">開発側（オフショア）</h5>
<p id="ps-outcome-text" class="text-sm bg-slate-950/40 p-3 rounded-lg min-h-[84px] flex items-center justify-center text-slate-500">[ 結果を見る ]</p>
</div>
</div>
<div id="ps-resolution-box" class="mt-8 p-4 bg-[#f6f2ee]/10 rounded-xl hidden border border-[#d6a37f]/20">
<p class="text-on-surface font-bold mb-2">解決策：厳密な要求工学</p>
<p class="text-sm text-slate-300">ワイヤーフレーム、データ構造、受け入れ条件、エッジケースを視覚化し、曖昧な期待値を排除することが必要です。</p>
</div>
</div>
</section>

<section id="ps-myth3" class="ps-content-section">
<div class="mb-8">
<span class="inline-block px-3 py-1 bg-rose-500 text-white rounded-full text-xs font-semibold mb-4 tracking-wider">MYTH 3</span>
<h3 class="text-3xl font-bold mb-6 text-on-surface">「AIエージェントが、レガシーシステムの技術的負債を自動で解消する」</h3>
</div>
<p class="text-lg text-slate-300 leading-relaxed mb-8 ps-panel p-6 rounded-[24px]">AI による補修は、設計刷新を伴わないと「接ぎ木」に終わりがちです。ここではレガシー、AI 接ぎ木、AgentOps 導入後の3状態を切り替えて、なぜ統治層が必要かを可視化しています。</p>
<div class="ps-panel p-6 rounded-[24px]">
<div class="flex justify-between items-center mb-6 gap-3 flex-wrap">
<h4 class="text-lg font-bold text-on-surface">システムアーキテクチャの変遷</h4>
<div class="flex gap-2 flex-wrap">
<button class="ps-arch-btn px-4 py-2 text-sm rounded-xl bg-slate-800 text-white font-bold" data-arch="legacy">レガシー</button>
<button class="ps-arch-btn px-4 py-2 text-sm rounded-xl bg-white/10 text-slate-300 hover:bg-white/15" data-arch="grafting">AI接ぎ木</button>
<button class="ps-arch-btn px-4 py-2 text-sm rounded-xl bg-white/10 text-slate-300 hover:bg-white/15" data-arch="agentops">AgentOps導入</button>
</div>
</div>
<div class="relative h-64 bg-slate-950/35 border border-white/10 rounded-2xl overflow-hidden p-4">
<div id="ps-arch-legacy" class="absolute inset-0 p-6 flex flex-col justify-center items-center transition-opacity duration-300">
<div class="w-48 h-24 bg-slate-700 rounded border-2 border-slate-500 flex items-center justify-center mb-2 font-mono text-slate-200">Monolithic Core</div>
<div class="flex gap-4">
<div class="w-16 h-16 bg-slate-800 rounded-full border border-slate-500 flex items-center justify-center text-xs text-slate-300">DB</div>
<div class="w-16 h-16 bg-slate-800 rounded-full border border-slate-500 flex items-center justify-center text-xs text-slate-300">API</div>
</div>
<p class="mt-4 text-sm text-slate-400 font-bold">硬直化したデジタル負債</p>
</div>
<div id="ps-arch-grafting" class="absolute inset-0 p-6 flex flex-col justify-center items-center opacity-0 pointer-events-none transition-opacity duration-300">
<div class="relative">
<div class="w-48 h-24 bg-slate-700 rounded border-2 border-slate-500 flex items-center justify-center mb-2 font-mono text-slate-300 opacity-50">Monolithic Core</div>
<div class="absolute -top-4 -right-4 w-20 h-10 bg-rose-300/20 border-rose-400 border-2 border-dashed flex items-center justify-center text-[10px] font-bold text-rose-300 rotate-12">AI Code</div>
<div class="absolute top-1/2 -left-6 w-16 h-8 bg-rose-300/20 border-rose-400 border-2 border-dashed flex items-center justify-center text-[10px] font-bold text-rose-300 -rotate-12">AI Fix</div>
<div class="absolute -bottom-4 right-4 w-24 h-10 bg-rose-300/20 border-rose-400 border-2 border-dashed flex items-center justify-center text-[10px] font-bold text-rose-300">AIOps</div>
</div>
<p class="mt-8 text-sm text-rose-300 font-bold">Grafting によるブラックボックス化</p>
</div>
<div id="ps-arch-agentops" class="absolute inset-0 p-6 flex flex-col justify-center items-center opacity-0 pointer-events-none transition-opacity duration-300">
<div class="w-full max-w-md h-12 bg-emerald-400/10 border-2 border-emerald-400 rounded flex items-center justify-center mb-4 text-emerald-300 font-bold shadow-sm">AgentOps Observability Layer</div>
<div class="flex gap-6 w-full max-w-md justify-between">
<div class="flex-1 h-20 bg-slate-900 border-2 border-slate-600 rounded flex items-center justify-center flex-col shadow-sm">
<span class="text-xs text-slate-500">1-bit LLM (Edge)</span>
<span class="font-bold text-sm text-on-surface">Bonsai-8B</span>
</div>
<div class="flex-1 h-20 bg-slate-900 border-2 border-slate-600 rounded flex items-center justify-center flex-col shadow-sm">
<span class="text-xs text-slate-500">Microservice</span>
<span class="font-bold text-sm text-on-surface">Core Logic</span>
</div>
</div>
<p class="mt-4 text-sm text-emerald-300 font-bold">非決定論的システムの透過的管理</p>
</div>
</div>
</div>
</section>

<section id="ps-myth4" class="ps-content-section">
<div class="mb-8">
<span class="inline-block px-3 py-1 bg-rose-500 text-white rounded-full text-xs font-semibold mb-4 tracking-wider">MYTH 4</span>
<h3 class="text-3xl font-bold mb-6 text-on-surface">「AIセキュリティツールを入れれば、攻撃者に対して優位に立てる」</h3>
</div>
<p class="text-lg text-slate-300 leading-relaxed mb-8 ps-panel p-6 rounded-[24px]">AI は防御側にも恩恵をもたらしますが、同時に攻撃者にも新しい認知攻撃面を与えます。ここでは AI マルウェアやバックアップ破壊の脅威をふまえ、なぜ絶対的イミュータビリティが必要かを整理します。</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
<div class="ps-panel p-6 rounded-[24px]">
<h4 class="text-lg font-bold mb-2 text-center text-on-surface">ランサムウェア被害と支払いのパラドックス</h4>
<p class="text-xs text-slate-400 text-center mb-4">被害率は上昇する一方、支払い率は低下。背景にはバックアップへの集中攻撃があります。</p>
<div class="ps-chart-container" style="height: 250px;">
<canvas id="ps-ransomware-chart"></canvas>
</div>
</div>
<div class="ps-panel-strong p-6 rounded-[24px] flex flex-col justify-center">
<h4 class="text-lg font-bold mb-4 text-[#d6a37f]">絶対的イミュータビリティ・アーキテクチャ</h4>
<div class="flex flex-col gap-3">
<div class="bg-slate-800 p-3 rounded border border-slate-600 flex justify-between items-center">
<span class="font-mono text-sm text-slate-200">本番環境 (AWS / On-Prem)</span>
<span class="text-rose-300 text-xs font-bold">侵害リスク大</span>
</div>
<div class="flex justify-center text-slate-500">⬇ Air-gap</div>
<div class="bg-slate-800 p-3 rounded border border-slate-600 flex justify-between items-center">
<span class="font-mono text-sm text-slate-200">バックアップ管理サーバー</span>
<span class="text-amber-300 text-xs font-bold">管理者ID窃取リスク</span>
</div>
<div class="flex justify-center text-slate-500">⬇ WORM</div>
<div class="bg-gradient-to-r from-emerald-950 to-slate-900 p-4 rounded border border-emerald-700 flex justify-between items-center">
<div>
<span class="font-bold text-emerald-300 block">Immutable Storage</span>
<span class="text-xs text-slate-400">S3 Object Lock / Vault</span>
</div>
<span class="text-xs bg-emerald-800 text-emerald-100 px-2 py-1 rounded">削除・改ざん不可</span>
</div>
</div>
</div>
</div>
</section>

<section id="ps-conclusion" class="ps-content-section">
<div class="mb-8">
<span class="inline-block px-3 py-1 bg-slate-800 text-white rounded-full text-xs font-semibold mb-4 tracking-wider">CONCLUSION</span>
<h3 class="text-3xl font-bold mb-6 text-on-surface">非決定論的システム時代のIT戦略</h3>
</div>
<div class="ps-panel p-8 rounded-[24px] border-t-8 border-[#b87c5e]">
<p class="text-lg text-slate-300 leading-relaxed mb-6">2026年のエンタープライズITでは、多くのテクノロジー定説が限定条件付きでしか成立しないことが明確になりました。</p>
<p class="text-lg text-slate-300 leading-relaxed mb-8">これからの戦略は、AI とクラウドの利便性を享受しつつ、その裏側にある不確実性と構造的脆弱性を前提に設計する必要があります。</p>
</div>
</section>
</main>
</div>
</div>

<script>
(() => {
  const init = () => {
    const root = document.querySelector('.paradigm-shell');
    if (!root) return;

    const state = { translationRevealed: false, outcomeRevealed: false };
    const chartInstances = {};

    const destroyChart = (id) => {
      if (chartInstances[id]) {
        chartInstances[id].destroy();
        chartInstances[id] = null;
      }
    };

    function navigate(targetId) {
      console.log('Navigating to:', targetId);
      root.querySelectorAll('.ps-nav-item').forEach(button => {
        button.classList.toggle('active', button.dataset.target === targetId);
      });
      root.querySelectorAll('.ps-content-section').forEach(section => {
        section.classList.toggle('active', section.id === targetId);
      });
      
      // Lazy render charts
      if (targetId === 'ps-myth1') setTimeout(renderCloudCostChart, 100);
      if (targetId === 'ps-myth4') setTimeout(renderRansomwareChart, 100);
    }

    function toggleTranslation() {
      const el = root.querySelector('#ps-translation-text');
      if (!state.translationRevealed) {
        el.innerHTML = '"Adjust that screen nicely so it\'s easy for users to use, appropriately."';
        el.classList.remove('text-slate-500');
        el.classList.add('text-slate-100', 'font-semibold');
        state.translationRevealed = true;
      }
    }

    function toggleOutcome() {
      if (!state.translationRevealed) return;
      const el = root.querySelector('#ps-outcome-text');
      if (!state.outcomeRevealed) {
        el.innerHTML = '発注者の意図と異なる、現地解釈に基づく実装へ着地';
        el.classList.remove('text-slate-500');
        el.classList.add('text-rose-300', 'font-bold');
        root.querySelector('#ps-resolution-box').classList.remove('hidden');
        state.outcomeRevealed = true;
      }
    }

    function switchArch(type) {
      root.querySelectorAll('.ps-arch-btn').forEach(button => {
        const active = button.dataset.arch === type;
        button.classList.toggle('bg-slate-800', active);
        button.classList.toggle('text-white', active);
        button.classList.toggle('bg-white/10', !active);
        button.classList.toggle('text-slate-300', !active);
      });
      ['legacy', 'grafting', 'agentops'].forEach(key => {
        const el = root.querySelector('#ps-arch-' + key);
        if (!el) return;
        el.classList.toggle('opacity-0', key !== type);
        el.classList.toggle('pointer-events-none', key !== type);
      });
    }

    function renderCloudCostChart() {
      const canvas = root.querySelector('#ps-cloud-cost-chart');
      if (!canvas || typeof Chart === 'undefined') return;
      destroyChart('cloudCostChart');
      chartInstances.cloudCostChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: ['2024', '2025', '2026', '2027', '2028'],
          datasets: [
            { label: 'パブリッククラウド', data: [100, 160, 280, 480, 750], borderColor: '#fb7185', backgroundColor: 'rgba(251, 113, 133, 0.12)', fill: true, tension: 0.4, borderWidth: 3 },
            { label: '特化型 / オンプレミス', data: [200, 220, 240, 260, 280], borderColor: '#6ee7b7', backgroundColor: 'transparent', borderDash: [5, 5], tension: 0.1, borderWidth: 3 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'top', labels: { color: '#cbd5e1' } }, tooltip: { mode: 'index', intersect: false } },
          scales: {
            x: { ticks: { color: '#cbd5e1' }, grid: { color: 'rgba(255,255,255,0.06)' } },
            y: { beginAtZero: true, ticks: { color: '#cbd5e1' }, title: { display: true, text: '累積コスト指数', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.08)' } }
          }
        }
      });
    }

    function renderRansomwareChart() {
      const canvas = root.querySelector('#ps-ransomware-chart');
      if (!canvas || typeof Chart === 'undefined') return;
      destroyChart('ransomwareChart');
      chartInstances.ransomwareChart = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
          labels: ['2023', '2024', '2025'],
          datasets: [
            { type: 'line', label: 'バックアップ標的率 (%)', data: [80, 89, 96], borderColor: '#fb7185', backgroundColor: '#fb7185', borderWidth: 3, yAxisID: 'y' },
            { type: 'bar', label: '被害遭遇率 (%)', data: [18.6, 21.0, 24.0], backgroundColor: '#6ee7b7', yAxisID: 'y' },
            { type: 'bar', label: '身代金支払い率 (%)', data: [18.0, 16.3, 13.0], backgroundColor: '#94a3b8', yAxisID: 'y' }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { size: 10 } } }, tooltip: { mode: 'index', intersect: false } },
          scales: {
            x: { ticks: { color: '#cbd5e1' }, grid: { color: 'rgba(255,255,255,0.06)' } },
            y: { beginAtZero: true, max: 100, ticks: { color: '#cbd5e1' }, title: { display: true, text: '割合 (%)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.08)' } }
          }
        }
      });
    }

    // Bindings
    root.querySelectorAll('.ps-nav-item').forEach(button => button.addEventListener('click', () => navigate(button.dataset.target)));
    root.querySelectorAll('[data-jump]').forEach(button => button.addEventListener('click', () => navigate(button.dataset.jump)));
    root.querySelector('#ps-translation-box')?.addEventListener('click', toggleTranslation);
    root.querySelector('#ps-outcome-box')?.addEventListener('click', toggleOutcome);
    root.querySelectorAll('.ps-arch-btn').forEach(button => button.addEventListener('click', () => switchArch(button.dataset.arch)));

    // Init state
    switchArch('legacy');
    navigate('ps-intro');
  };

  // Wait for SME engine to settle the DOM
  setTimeout(init, 500);
})();
</script>

## 変更履歴 (Changelog)
- **2026-04-09**: `SKILL.md` 準拠のグローバルデザイン統一およびメタデータ標準化アップデートを実施。新規作成。

