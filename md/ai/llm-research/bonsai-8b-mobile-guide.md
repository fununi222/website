---
title: "Bonsai 8B | スマホ（Llama.cpp）導入ガイド 2026"
date: "2026-04-09"
category: "ai"
description: "Xiaomi/HyperOS 端末の Termux 上で 1-bit LLM『Bonsai 8B』を動作させ、エッジAIの基本と応用を体験するためのガイド。"
themes: ["ai:llm", "ai:edge", "other:tutorial"]
updated: "2026-08-17"
---



# Bonsai 8B | スマホ（Llama.cpp）導入ガイド 2026

## 概要
PrismMLおよびBitNet研究チームが確立した1.58ビット（1-bit）LLM「Bonsai 8B」を、Android (Xiaomi / HyperOS) 端末のTermux環境上で動かし、エッジAIの基本と応用を体験するためのインタラクティブ・ガイドです。1-bit量子化のメリット（VRAM消費93%削減）の可視化から、Arm NEON最適化、環境構築、ビルド、推論実行までの具体的な手順を解説します。

---

<style>
.chart-container {
 position: relative;
 width: 100%;
 max-width: 800px;
 margin-left: auto;
 margin-right: auto;
 height: 300px;
 max-height: 400px;
}
@media (min-width: 768px) {
 .chart-container {
 height: 350px;
 }
}
.terminal-scroll::-webkit-scrollbar {
 width: 8px;
}
.terminal-scroll::-webkit-scrollbar-track {
 background: #060e20; 
}
.terminal-scroll::-webkit-scrollbar-thumb {
 background: #1e293b; 
 border-radius: 4px;
}
.terminal-scroll::-webkit-scrollbar-thumb:hover {
 background: #334155; 
}
.tab-btn {
 transition: all 0.2s ease-in-out;
}
.tab-active {
 background-color: rgba(255, 255, 255, 0.05);
 border-left: 4px solid #00d2ff !important;
 font-weight: 700;
}
</style>

## 1. プロジェクト概要：Bonsai 8BとエッジAIの革新

2026年現在、1-bit量子化技術（BitNet b1.58 / Q1_0_g128）により、80億パラメータクラス（8B）の高度な思考モデルがわずか1.1GBのメモリ領域で動作可能となりました。

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-8">
<div class="bg-surface-container rounded-xl shadow-sm border border-white/10 p-6 flex flex-col items-center text-center transition hover:shadow-md hover:border-primary/50 cyber-glow">
<span class="text-4xl mb-3">🧠</span>
<h3 class="text-sm text-slate-400 font-bold uppercase tracking-wider mb-1">パラメータ数</h3>
<p class="text-3xl font-bold text-primary">82億 <span class="text-lg font-normal text-slate-400">(8B)</span></p>
<p class="text-xs text-slate-500 mt-2">高度な推論能力と指示追従性を保持</p>
</div>

<div class="bg-surface-container rounded-xl shadow-sm border border-white/10 p-6 flex flex-col items-center text-center transition hover:shadow-md hover:border-secondary/50 cyber-glow border-b-4 border-secondary">
<span class="text-4xl mb-3">💾</span>
<h3 class="text-sm text-slate-400 font-bold uppercase tracking-wider mb-1">モデルサイズ (RAM)</h3>
<p class="text-3xl font-bold text-secondary">約 1.1 GB</p>
<p class="text-xs text-slate-500 mt-2">スマホのメインメモリ（RAM）で余裕動作</p>
</div>

<div class="bg-surface-container rounded-xl shadow-sm border border-white/10 p-6 flex flex-col items-center text-center transition hover:shadow-md hover:border-green-500/50 cyber-glow border-b-4 border-green-500">
<span class="text-4xl mb-3">⚡</span>
<h3 class="text-sm text-slate-400 font-bold uppercase tracking-wider mb-1">生成速度</h3>
<p class="text-3xl font-bold text-green-400">2.7 ~ 3.5 t/s</p>
<p class="text-xs text-slate-500 mt-2">スマホCPU（Snapdragon / Dimensity）単体実測</p>
</div>
</div>

---

## 2. 1-bit量子化（BitNet b1.58）のメモリ比較インパクト

Bonsai 8Bの最大の特徴は、従来の16ビット（FP16）や4ビット（Q4_K_M）と比較した際の非常に高いメモリ帯域節約効果です。

<div class="bg-surface-container rounded-2xl p-6 md:p-8 shadow-sm border border-white/10 cyber-glow my-8">
<p class="text-on-surface-variant leading-relaxed mb-6">
80億パラメータモデルでありながら、ファイルサイズを1.1GBまで圧縮することで、GPUを持たないスマートフォン端末でも完全ローカル＆プライベートなオフラインAI動作が実現しました。
</p>
<div class="chart-container">
<canvas id="sizeComparisonChart"></canvas>
</div>
</div>

---

## 3. セットアップ手順 (Android Termux)

Android端末（特にXiaomi / HyperOS / Galaxy）上でBonsaiを動かすためのステップバイステップガイドです。以下の各ステップをタップしてコマンドを確認してください。

<div class="flex flex-col md:flex-row gap-6 bg-surface-container rounded-2xl border border-white/10 overflow-hidden shadow-sm cyber-glow my-8">
<div class="md:w-1/3 bg-background border-r border-white/10 flex flex-col" id="stepTabs">
<button class="tab-btn tab-active text-left p-5 border-b border-white/5 hover:bg-white/5 flex items-center gap-3" data-step="1">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">1</span>
<span class="text-on-surface">Termux環境構築</span>
</button>
<button class="tab-btn text-left p-5 border-b border-white/5 hover:bg-white/5 flex items-center gap-3" data-step="2">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">2</span>
<span class="text-on-surface">llama.cppビルド</span>
</button>
<button class="tab-btn text-left p-5 border-b border-white/5 hover:bg-white/5 flex items-center gap-3" data-step="3">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">3</span>
<span class="text-on-surface">モデル取得 (GGUF)</span>
</button>
<button class="tab-btn text-left p-5 hover:bg-white/5 flex items-center gap-3" data-step="4">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">4</span>
<span class="text-on-surface">推論・API起動</span>
</button>
</div>

<div class="md:w-2/3 p-6 md:p-8" id="stepContent">
<!-- Dynamic content injected via JS -->
</div>
</div>

---

## 4. 実行コンソール・デモ ＆ 将来展望

<div id="demo" class="bg-[#0b1221] rounded-2xl p-6 md:p-8 shadow-xl border border-white/10 cyber-glow my-8">
<p class="text-on-surface-variant leading-relaxed mb-6">
セットアップ完了後、`llama-cli` を起動した際のコンソールシミュレーションです。スマホ単体でリアルタイムに思考・生成される速度をご確認ください。
</p>

<div class="bg-black rounded-lg p-4 font-mono text-sm md:text-base h-64 overflow-y-auto terminal-scroll border border-white/20 relative">
<div class="absolute top-2 right-4 text-xs text-slate-500">Termux Terminal</div>
<div id="terminalOutput" class="text-slate-300 whitespace-pre-wrap"></div>
<span class="animate-pulse bg-green-500 w-2 h-5 inline-block align-middle ml-1" id="cursor"></span>
</div>

<div class="mt-8 pt-6 border-t border-white/10">
<h3 class="text-xl font-bold mb-3">ローカルAPI化とエージェント連携の展望</h3>
<p class="text-on-surface-variant leading-relaxed">
スマホのCPUだけで8Bモデルがこれほど軽快に動く時代となりました。今後はこのローカル推論エンジンを `llama-server --host 127.0.0.1 --port 8080` としてバックグラウンド常駐させ、OpenClawやTaskerなどの自動化ツールと連携させることで、完全オフラインのプライベートAIエージェント環境が完結します。
</p>
</div>
</div>

---

<script>
document.addEventListener('sme-loaded', () => {
 initBonsaiGuide();
});

setTimeout(initBonsaiGuide, 150);

function initBonsaiGuide() {
 if (window._bonsaiGuideInitialized) return;
 window._bonsaiGuideInitialized = true;

 const stepsData = {
 1: {
 title: "Termux環境の構築",
 description: "まずはAndroidのターミナルエミュレータ「Termux」をF-Droidから最新版をインストールし、必要なC/C++ビルドツールをセットアップします。",
 code: "# パッケージの更新\npkg update && pkg upgrade\n\n# 必要な開発ツールの導入\npkg install git cmake clang python wget"
 },
 2: {
 title: "1-bit量子化対応 llama.cpp のビルド",
 description: "BonsaiはQ1_0_g128量子化を使用するため、対応カーネルを含む llama.cpp をソースからコンパイルします。",
 code: "# リポジトリのクローン\ngit clone https://github.com/PrismML-Eng/llama.cpp\ncd llama.cpp\n\n# ARM NEONアクセラレーション付きビルド\ncmake -B build -DGGML_NATIVE=ON\ncmake --build build -j$(nproc)"
 },
 3: {
 title: "モデルファイルの取得 (1.1GB GGUF)",
 description: "Hugging Faceから軽量GGUFモデルをダウンロードします。",
 code: "# モデルの取得\nwget -O Bonsai-8B.gguf \\\n https://huggingface.co/prism-ml/Bonsai-8B-gguf/resolve/main/Bonsai-8B.gguf\n\n# ファイルサイズ確認\nls -lh Bonsai-8B.gguf"
 },
 4: {
 title: "推論・ローカルAPIの実行",
 description: "CLIでの対話、または他アプリから叩けるローカルHTTP APIサーバーとして起動します。",
 code: "# CLI対話モード\n./build/bin/llama-cli -m Bonsai-8B.gguf -p \"こんにちは、自己紹介してください。\"\n\n# ローカルAPIサーバー化 (ポート8080)\n./build/bin/llama-server -m Bonsai-8B.gguf --port 8080"
 }
 };

 const stepTabs = document.querySelectorAll('.tab-btn');
 const contentContainer = document.getElementById('stepContent');

 if (!contentContainer) return;

 function renderStepContent(stepId) {
 const data = stepsData[stepId];
 contentContainer.innerHTML = `
 <h3 class="text-xl font-bold mb-3 text-on-surface">${data.title}</h3>
 <p class="text-on-surface-variant mb-5 leading-relaxed">${data.description}</p>
 <div class="bg-black/50 rounded-lg p-4 relative group border border-white/10">
 <pre class="font-mono text-sm text-slate-300 overflow-x-auto whitespace-pre-wrap"><code>${data.code}</code></pre>
 </div>
 `;
 }

 stepTabs.forEach(tab => {
 tab.addEventListener('click', () => {
 stepTabs.forEach(t => {
 t.classList.remove('tab-active');
 t.style.borderLeft = 'none';
 });
 tab.classList.add('tab-active');
 tab.style.borderLeft = '4px solid #00d2ff';

 const stepId = tab.getAttribute('data-step');
 renderStepContent(stepId);
 });
 });

 renderStepContent(1);

 const ctxEl = document.getElementById('sizeComparisonChart');
 if (ctxEl && typeof Chart !== 'undefined') {
 const ctx = ctxEl.getContext('2d');
 new Chart(ctx, {
 type: 'bar',
 data: {
 labels: ['FP16 (非量子化)', '4-bit (通常量子化)', '1-bit (Bonsai 8B)'],
 datasets: [{
 label: 'モデルサイズ (GB)',
 data: [16.0, 4.5, 1.1],
 backgroundColor: [
 'rgba(170, 164, 255, 0.2)',
 'rgba(170, 164, 255, 0.5)',
 'rgba(0, 210, 255, 0.8)'
 ],
 borderColor: [
 'rgba(170, 164, 255, 0.5)',
 'rgba(170, 164, 255, 0.8)',
 'rgba(0, 210, 255, 1)'
 ],
 borderWidth: 1,
 borderRadius: 4
 }]
 },
 options: {
 responsive: true,
 maintainAspectRatio: false,
 plugins: {
 legend: { display: false },
 tooltip: {
 callbacks: { label: function(context) { return context.parsed.y + ' GB'; } },
 backgroundColor: 'rgba(6, 14, 32, 0.9)',
 padding: 10
 }
 },
 scales: {
 y: {
 beginAtZero: true,
 title: { display: true, text: 'ファイルサイズ (GB)', color: '#aaa4ff' },
 grid: { color: 'rgba(255, 255, 255, 0.1)' },
 ticks: { color: '#94a3b8' }
 },
 x: {
 ticks: { color: '#94a3b8' },
 grid: { display: false }
 }
 }
 }
 });
 }

 const terminalOutput = document.getElementById('terminalOutput');
 if (terminalOutput) {
 const sequence = [
 { text: "~/llama.cpp $ ./build/bin/llama-cli -m Bonsai-8B.gguf -p \"こんにちは、自己紹介してください。\"", delay: 400, color: "text-slate-300" },
 { text: "\nLoading model...\n", delay: 600, color: "text-slate-500" },
 { text: "▄▄ ▄▄\n██ ██\n██ ██ ▀▀█▄ ███▄███▄ ▀▀█▄ ▄████ ████▄ ████▄\n██ ██ ▄█▀██ ██ ██ ██ ▄█▀██ ██ ██ ██ ██ ██\n██ ██ ▀█▄██ ██ ██ ██ ▀█▄██ ██ ▀████ ████▀ ████▀\n ██ ██\n ▀▀ ▀▀\n", delay: 800, color: "text-green-500" },
 { text: "build : b8196-f5dda7207\nmodel : Bonsai-8B.gguf (Q1_0_g128)\nmodalities : text\n\n", delay: 400, color: "text-slate-400" },
 { text: "> こんにちは、自己紹介してください。\n\n", delay: 500, color: "text-white" },
 { text: "こんにちは！私はBonsaiと呼ばれ、1.58ビット量子化で動作する高効率AIアシスタントです。\n", delay: 40, type: true, color: "text-green-300" },
 { text: "超低メモリ・低電力消費を特徴とし、スマートフォンのCPU単体でも快適に推論可能です。\n", delay: 40, type: true, color: "text-green-300" },
 { text: "ご質問やタスクの自動化について、何でもお気軽にお知らせください！\n\n", delay: 40, type: true, color: "text-green-300" },
 { text: "[ Prompt: 2.6 t/s | Generation: 2.7 t/s ]\n", delay: 600, color: "text-slate-500" },
 { text: "~/llama.cpp $ ", delay: 800, color: "text-slate-300" }
 ];

 let seqIndex = 0;
 async function typeWriter() {
 if (seqIndex >= sequence.length) return;
 const step = sequence[seqIndex];
 await new Promise(r => setTimeout(r, step.delay));

 const span = document.createElement('span');
 span.className = step.color;
 terminalOutput.appendChild(span);

 if (step.type) {
 for (let i = 0; i < step.text.length; i++) {
 span.textContent += step.text.charAt(i);
 terminalOutput.parentElement.scrollTop = terminalOutput.parentElement.scrollHeight;
 await new Promise(r => setTimeout(r, 30)); 
 }
 } else {
 span.textContent = step.text;
 terminalOutput.parentElement.scrollTop = terminalOutput.parentElement.scrollHeight;
 }
 seqIndex++;
 typeWriter();
 }

 const observer = new IntersectionObserver((entries) => {
 if (entries[0].isIntersecting) {
 typeWriter();
 observer.disconnect();
 }
 }, { threshold: 0.5 });

 observer.observe(document.getElementById('demo'));
 }
}
</script>

## 変更履歴 (Changelog)
- **2026-08-17**: 読み手に寄り添うプロ品質へのリライト（煽り・誇張表現の適正化、概要・構成の洗練）。
- **2026-08-02 (v3)**: 2026年最新のBitNet b1.58量子化技術ファクトチェック、ARM NEONビルド最適化、TermuxローカルAPIサーバー化手順を追加。
- **2026-04-09 (v2)**: グローバルデザイン統一およびメタデータ標準化アップデートを実施。
- **2026-04-07 (v1)**: 新規作成。
