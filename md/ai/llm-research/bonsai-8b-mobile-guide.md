---
title: "Bonsai 8B | スマホ（Llama.cpp）導入ガイド 2026"
date: "2026-04-09"
category: "ai"
description: "Xiaomi/HyperOS 端末の Termux 上で 1-bit LLM『Bonsai 8B』を動作させ、エッジAIの真髄を体験するためのガイド。"
themes: ["ai:llm", "ai:edge", "other:tutorial"]
---

# Bonsai 8B | スマホ（Llama.cpp）導入ガイド 2026

## 超要約
PrismMLが開発した驚異の1-bit LLM「Bonsai 8B」を、Android (Xiaomi/HyperOS) 端末のTermux上で動かし、エッジAIの真髄を体験するためのインタラクティブ・ガイドです。1-bit量子化のメリットの可視化から、環境構築、ビルド、推論実行までの具体的な手順を解説します。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
/* カスタムスクロールバーとタブUIのスタイル */
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

<div class="space-y-16 mt-8">

<!-- Section 1: Overview Dashboard -->
<section id="overview">
<div class="mb-6">
<h2 class="text-2xl font-bold border-b border-white/20 pb-2 mb-4">プロジェクト概要</h2>
<p class="text-on-surface-variant leading-relaxed">
2026年3月に発表されたBonsai 8Bは、特殊な量子化技術（Q1_0_g128）により、圧倒的な軽量化と高速化を実現しました。このセクションでは、本モデルがスマホ環境においていかに革新的であるかを示す主要な指標を確認できます。
</p>
</div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<!-- Stat Card 1 -->
<div class="bg-surface-container rounded-xl shadow-sm border border-white/10 p-6 flex flex-col items-center text-center transition hover:shadow-md hover:border-primary/50 cyber-glow">
<span class="text-4xl mb-3">🧠</span>
<h3 class="text-sm text-slate-400 font-bold uppercase tracking-wider mb-1">パラメータ数</h3>
<p class="text-3xl font-bold text-primary">82億 <span class="text-lg font-normal text-slate-400">(8B)</span></p>
<p class="text-xs text-slate-500 mt-2">高度な推論能力を維持</p>
</div>
<!-- Stat Card 2 -->
<div class="bg-surface-container rounded-xl shadow-sm border border-white/10 p-6 flex flex-col items-center text-center transition hover:shadow-md hover:border-secondary/50 cyber-glow border-b-4 border-secondary">
<span class="text-4xl mb-3">💾</span>
<h3 class="text-sm text-slate-400 font-bold uppercase tracking-wider mb-1">モデルサイズ</h3>
<p class="text-3xl font-bold text-secondary">約 1.1 GB</p>
<p class="text-xs text-slate-500 mt-2">スマホのRAMに余裕で展開可能</p>
</div>
<!-- Stat Card 3 -->
<div class="bg-surface-container rounded-xl shadow-sm border border-white/10 p-6 flex flex-col items-center text-center transition hover:shadow-md hover:border-green-500/50 cyber-glow border-b-4 border-green-500">
<span class="text-4xl mb-3">⚡</span>
<h3 class="text-sm text-slate-400 font-bold uppercase tracking-wider mb-1">生成速度</h3>
<p class="text-3xl font-bold text-green-400">2.7 t/s</p>
<p class="text-xs text-slate-500 mt-2">スマホCPU単体での実測値</p>
</div>
</div>
</section>

<!-- Section 2: Data Visualization -->
<section id="visualization" class="bg-surface-container rounded-2xl p-6 md:p-8 shadow-sm border border-white/10 cyber-glow">
<div class="mb-6">
<h2 class="text-2xl font-bold mb-4">1-bit量子化のインパクト</h2>
<p class="text-on-surface-variant leading-relaxed mb-6">
Bonsai 8Bの最大の特徴はそのサイズです。一般的な80億パラメータクラスのモデルと比較して、ストレージやメモリ（RAM）への負担がどれほど軽減されているかを視覚的に確認してください。これにより、モバイル端末での完全ローカル動作が現実のものとなりました。
</p>
</div>
<div class="chart-container">
<canvas id="sizeComparisonChart"></canvas>
</div>
</section>

<!-- Section 3: Interactive Installation Guide -->
<section id="installation">
<div class="mb-6">
<h2 class="text-2xl font-bold border-b border-white/20 pb-2 mb-4">セットアップ手順 (Termux)</h2>
<p class="text-on-surface-variant leading-relaxed">
Android端末（特にXiaomi / HyperOS）上でBonsaiを動かすための具体的なステップです。左側のステップをクリックして、各フェーズで必要なコマンドと詳細な解説を確認してください。
</p>
</div>

<div class="flex flex-col md:flex-row gap-6 bg-surface-container rounded-2xl border border-white/10 overflow-hidden shadow-sm cyber-glow">
<!-- Navigation Tabs -->
<div class="md:w-1/3 bg-background border-r border-white/10 flex flex-col" id="stepTabs">
<button class="tab-btn tab-active text-left p-5 border-b border-white/5 hover:bg-white/5 flex items-center gap-3" data-step="1">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">1</span>
<span class="text-on-surface">環境の構築</span>
</button>
<button class="tab-btn text-left p-5 border-b border-white/5 hover:bg-white/5 flex items-center gap-3" data-step="2">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">2</span>
<span class="text-on-surface">エンジンビルド</span>
</button>
<button class="tab-btn text-left p-5 border-b border-white/5 hover:bg-white/5 flex items-center gap-3" data-step="3">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">3</span>
<span class="text-on-surface">モデル取得</span>
</button>
<button class="tab-btn text-left p-5 hover:bg-white/5 flex items-center gap-3" data-step="4">
<span class="bg-primary text-background w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold shrink-0">4</span>
<span class="text-on-surface">推論実行</span>
</button>
</div>

<!-- Content Area -->
<div class="md:w-2/3 p-6 md:p-8" id="stepContent">
<!-- Dynamic content injected via JS -->
</div>
</div>
</section>

<!-- Section 4: Execution Demo & Conclusion -->
<section id="demo" class="bg-[#0b1221] rounded-2xl p-6 md:p-8 shadow-xl border border-white/10 cyber-glow">
<div class="mb-6">
<h2 class="text-2xl font-bold mb-4 text-green-400">実行デモ ＆ まとめ</h2>
<p class="text-on-surface-variant leading-relaxed">
セットアップが完了し、モデルを起動した際のコンソールの様子をシミュレーションします。2.7 t/sというスマホとしては驚異的な生成速度を体感してください。
</p>
</div>

<!-- Terminal Simulation -->
<div class="bg-black rounded-lg p-4 font-mono text-sm md:text-base h-64 overflow-y-auto terminal-scroll border border-white/20 relative">
<div class="absolute top-2 right-4 text-xs text-slate-500">Termux</div>
<div id="terminalOutput" class="text-slate-300 whitespace-pre-wrap"></div>
<span class="animate-pulse bg-green-500 w-2 h-5 inline-block align-middle ml-1" id="cursor"></span>
</div>

<div class="mt-8 pt-6 border-t border-white/10">
<h3 class="text-xl font-bold mb-3">次のステップ：最強AIスマホの構築</h3>
<p class="text-on-surface-variant leading-relaxed">
スマホのCPUだけで8Bモデルがこれほど軽快に動く時代が来ました。今後はこのローカルAPIを <code>llama-server</code> としてバックグラウンドで立ち上げ、OpenClaw 等の自動化エージェントツールと連携させることで、完全オフラインで動作するセキュアな自動化環境を構築することが可能です。
</p>
</div>
</section>

</div>

<script>
document.addEventListener('sme-loaded', () => {
    initBonsaiGuide();
});

setTimeout(initBonsaiGuide, 100);

function initBonsaiGuide() {
    if (window._bonsaiGuideInitialized) return;
    window._bonsaiGuideInitialized = true;

    const stepsData = {
        1: {
            title: "Termux環境の構築",
            description: "まずはAndroidのターミナルエミュレータ「Termux」をインストールし、必要なビルドツールを揃えます。F-Droid等から最新版を入手してください。",
            code: "# パッケージの更新\npkg update && pkg upgrade\n\n# 必要なツールのインストール\npkg install git cmake clang python wget"
        },
        2: {
            title: "1-bit対応版 llama.cpp のビルド",
            description: "Bonsaiは特殊な量子化（Q1_0_g128）を使用しているため、通常のアプリではなく、PrismMLが公開している専用の llama.cpp をソースからビルドする必要があります。",
            code: "# リポジトリのクローン\ngit clone https://github.com/PrismML-Eng/llama.cpp\ncd llama.cpp\n\n# ビルド実行 (-jオプションでマルチコア活用)\ncmake -B build\ncmake --build build -j$(nproc)"
        },
        3: {
            title: "モデルファイルの取得",
            description: "Hugging Faceから約1.15GBのモデルをダウンロードします。※リポジトリが非公開設定(Gated)の場合、ブラウザで規約同意後にトークン付きでダウンロードする必要があります。",
            code: "# 正しいリポジトリからダウンロード\nwget -O Bonsai-8B.gguf \\\n  https://huggingface.co/prism-ml/Bonsai-8B-gguf/resolve/main/Bonsai-8B.gguf\n\n# サイズ確認\nls -lh Bonsai-8B.gguf"
        },
        4: {
            title: "推論の実行",
            description: "準備が整いました。ビルドした専用のクライアントを使用して、モデルを読み込み、プロンプトを送信します。",
            code: "./build/bin/llama-cli \\\n  -m Bonsai-8B.gguf \\\n  -p \"こんにちは、自己紹介してください。\""
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
            tab.style.borderLeft = '4px solid #00d2ff'; // secondary color

            const stepId = tab.getAttribute('data-step');
            renderStepContent(stepId);
        });
    });

    renderStepContent(1);

    const ctxEl = document.getElementById('sizeComparisonChart');
    if (ctxEl) {
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
                        titleFont: { family: 'Inter' },
                        bodyFont: { family: 'Inter' },
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
                },
                animation: { duration: 1500, easing: 'easeOutQuart' }
            }
        });
    }

    const terminalOutput = document.getElementById('terminalOutput');
    if (terminalOutput) {
        const sequence = [
            { text: "~/llama.cpp $ ./build/bin/llama-cli -m Bonsai-8B.gguf -p \"こんにちは、自己紹介してください。\"", delay: 500, color: "text-slate-300" },
            { text: "\nLoading model...\n", delay: 800, color: "text-slate-500" },
            { text: "▄▄ ▄▄\n██ ██\n██ ██  ▀▀█▄ ███▄███▄  ▀▀█▄    ▄████ ████▄ ████▄\n██ ██ ▄█▀██ ██ ██ ██ ▄█▀██    ██    ██ ██ ██ ██\n██ ██ ▀█▄██ ██ ██ ██ ▀█▄██ ██ ▀████ ████▀ ████▀\n                                    ██    ██\n                                    ▀▀    ▀▀\n", delay: 1000, color: "text-green-500" },
            { text: "build      : b8196-f5dda7207\nmodel      : Bonsai-8B.gguf\nmodalities : text\n\n", delay: 400, color: "text-slate-400" },
            { text: "> こんにちは、自己紹介してください。\n\n", delay: 600, color: "text-white" },
            { text: "こんにちは！私はBonsaiと呼ばれ、PrismMLによって開発されたAIアシスタントです。\n", delay: 50, type: true, color: "text-green-300" },
            { text: "私は低レイテンシーと低メモリ使用量を最優先に考えた1-bitモデルです。\n", delay: 50, type: true, color: "text-green-300" },
            { text: "何かお手伝いできるか、ご質問がありましたら、遠慮なくお気軽にお知らせください！\n\n", delay: 50, type: true, color: "text-green-300" },
            { text: "[ Prompt: 2.6 t/s | Generation: 2.7 t/s ]\n", delay: 800, color: "text-slate-500" },
            { text: "~/llama.cpp $ ", delay: 1000, color: "text-slate-300" }
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
                    await new Promise(r => setTimeout(r, 40 + Math.random() * 30)); 
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
- **2026-04-09**: `SKILL.md` 準拠のグローバルデザイン統一およびメタデータ標準化アップデートを実施。
- **2026-04-07**: 新規作成。Bonsai 8Bのスマホ導入手順およびインタラクティブガイドを追加。

