---
title: "OpenClaw | Yahoo!リアルタイム検索を活用した動的スキルの構築"
date: "2026-04-09"
category: "AI & Agents"
description: "X APIの高騰を回避し、Yahoo!リアルタイム検索をデータソースとして活用するAIエージェントスキルの実装ガイド。"
themes: ["ai:agent", "ai:tool-integration", "ai:automation"]
---

# OpenClaw | Yahoo!リアルタイム検索を活用した動的スキルの構築
<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

## 超要約
[X](article.html?md=glossary/system-glossary.md#:~:text=X) [API](article.html?md=glossary/system-glossary.md#:~:text=API)の高額な費用やアカウント制約、凍結リスクを回避し、[Yahoo!リアルタイム検索](https://search.yahoo.co.jp/realtime)をデータソースとして活用する、[OpenClaw](article.html?md=glossary/system-glossary.md#:~:text=OpenClaw) ベースの[AIエージェント](article.html?md=glossary/system-glossary.md#:~:text=AI%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88)スキル構築ガイドです。
[Playwright](article.html?md=glossary/system-glossary.md#:~:text=Playwright)によるスクレイピングと、[LLM](article.html?md=glossary/system-glossary.md#:~:text=LLM)を用いた高度なフィルタリングを組み合わせ、価値の高い「推し活」情報を自動で抽出・要約するシステムを構築します。

## 1. 手法の比較分析
なぜ公式の [X](article.html?md=glossary/system-glossary.md#:~:text=X) [API](article.html?md=glossary/system-glossary.md#:~:text=API) ではなく「Yahoo!リアルタイム検索」を採用するのかを分析します。以下のレーダーチャートは、個人開発者がエージェントを構築する際の主要な指標に基づいた比較です。

<div class="bg-white rounded-2xl shadow-sm border border-stone-200 p-6 md:p-8 my-8 text-stone-800">
<div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
<div id="comparisonChartContainer" class="w-full flex justify-center" style="position: relative; width: 100%; min-height: 300px; height: 350px;">
<!-- Canvas injected by script -->
</div>
<div class="space-y-4">
<div class="p-4 bg-rose-50 rounded-lg border border-rose-100">
<h3 class="font-bold text-rose-800 flex items-center mb-2">🏆 Yahoo!リアルタイム検索の優位性</h3>
<ul class="space-y-2 text-sm text-stone-700">
<li class="flex items-start">
<span class="mr-2">✔️</span>
<span><strong>完全無料・ログイン不要:</strong> アカウントBANのリスクや高額な維持費（月額$100〜）が不要です。</span>
</li>
<li class="flex items-start">
<span class="mr-2">✔️</span>
<span><strong>強力なクエリ:</strong> <code>(id:ユーザー名)</code>を指定することで、公式タイムラインに近い精度で抽出可能。</span>
</li>
<li class="flex items-start">
<span class="mr-2">✔️</span>
<span><strong>圧倒的な速報性:</strong> 公式告知のインデックス速度が極めて速く、最新情報を逃しません。</span>
</li>
</ul>
</div>
</div>
</div>
</div>

## 2. スキル実装コード（Python）
OpenClawにスキルを追加するための具体的な実装方法を確認します。タブを切り替えて、Playwrightを用いた「スクレイピングロジック」と、AIの賢さを決める「プロンプトエンジニアリング」のコードを参照してください。

<div class="bg-stone-900 rounded-2xl shadow-lg overflow-hidden my-8 border border-white/5 cyber-glow">
<div class="p-6 md:p-8 text-stone-100">
<div class="flex flex-wrap gap-2 mb-4 border-b border-stone-700 pb-2">
<button id="btn-py" class="tab-btn active px-4 py-2 rounded-t-md font-medium text-sm transition-colors border-b-2 border-primary text-white" onclick="switchOpenClawTab('code-python', 'code-prompt', this)">💻 Playwright スクレイピング</button>
<button id="btn-prompt" class="tab-btn px-4 py-2 rounded-t-md font-medium text-sm transition-colors text-stone-400 hover:text-stone-100" onclick="switchOpenClawTab('code-prompt', 'code-python', this)">🧠 システムプロンプト定義</button>
</div>

<div class="relative bg-black/40 rounded-lg p-4 overflow-x-auto text-sm font-mono border border-stone-800 min-h-[350px]">
<div id="code-python" class="code-content block whitespace-pre text-emerald-400"></div>
<div id="code-prompt" class="code-content hidden whitespace-pre text-secondary"></div>
</div>
</div>
</div>

## 3. 情報フィルタリングの階層構造
生データのスクレイピングだけではノイズが多くなります。設定したプロンプトがどのように「日常のつぶやき」を削ぎ落とし、価値の高い「告知情報」だけを抽出・要約するかの優先順位構造を視覚化します。

<div class="bg-white rounded-2xl shadow-sm border border-stone-200 p-6 md:p-8 my-8 text-stone-800">
<div class="flex flex-col md:flex-row items-center justify-center gap-6">
<div class="w-full md:w-1/3 bg-stone-100 p-4 rounded-lg border border-stone-200 text-center relative opacity-50">
<div class="text-[10px] font-bold text-stone-500 mb-2 uppercase tracking-wider">Raw Data</div>
<div class="space-y-1 text-xs text-stone-400 line-through font-mono">
<div>「おはみこ〜！☀️」</div>
<div>「今日のご飯おいしかった」</div>
<div>「ねむい...」</div>
</div>
<div class="absolute -right-4 top-1/2 transform -translate-y-1/2 text-2xl text-stone-300 hidden md:block">➔</div>
<div class="absolute -bottom-4 left-1/2 transform -translate-x-1/2 text-2xl text-stone-300 md:hidden">⬇</div>
</div>

<div class="w-full md:w-2/3 space-y-3">
<div class="flex items-center p-3 bg-rose-50 border border-rose-200 rounded-lg shadow-sm">
<div class="flex-shrink-0 w-8 h-8 bg-rose-500 text-white rounded-full flex items-center justify-center font-bold text-sm">1</div>
<div class="ml-4">
<h4 class="font-bold text-stone-800 text-sm">公式告知・スケジュール</h4>
<p class="text-[10px] text-stone-600">配信開始時間、イベント出演など最重要情報</p>
</div>
</div>
<div class="flex items-center p-3 bg-orange-50 border border-orange-200 rounded-lg shadow-sm">
<div class="flex-shrink-0 w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold text-sm">2</div>
<div class="ml-4">
<h4 class="font-bold text-stone-800 text-sm">グッズ・物販情報</h4>
<p class="text-[10px] text-stone-600">販売開始、予約締切、在庫状況など</p>
</div>
</div>
<div class="flex items-center p-3 bg-amber-50 border border-amber-200 rounded-lg shadow-sm">
<div class="flex-shrink-0 w-8 h-8 bg-amber-500 text-white rounded-full flex items-center justify-center font-bold text-sm">3</div>
<div class="ml-4">
<h4 class="font-bold text-stone-800 text-sm">新作・アップデート</h4>
<p class="text-[10px] text-stone-600">新作ゲーム告知、新曲MV公開など</p>
</div>
</div>
</div>
</div>
</div>

## 4. エージェント動作シミュレーション
構築したスキルがOpenClaw上でどのように動作するかを体験できる対話型デモです。「さくらみこ」さんをターゲットに、エージェントが裏側でスクレイピングを行い、プロンプトに従って要約を生成する流れをシミュレートします。

<div class="bg-rose-50 rounded-2xl shadow-inner border border-rose-100 p-6 md:p-8 my-8 text-stone-800">
<div class="max-w-2xl mx-auto bg-white rounded-xl shadow-md overflow-hidden border border-stone-200">
<div class="bg-stone-100 px-4 py-3 border-b border-stone-200 flex items-center justify-between">
<div class="flex items-center">
<span class="text-xl mr-2">🤖</span>
<span class="font-bold text-stone-700 text-sm">OpenClaw Agent</span>
</div>
<div class="text-[10px] text-stone-400 font-mono">Skill: fetch_x_posts</div>
</div>

<div id="chat-container" class="p-4 h-64 overflow-y-auto space-y-4 bg-stone-50 flex flex-col font-body text-sm">
<div class="self-start bg-white border border-stone-200 p-3 rounded-2xl rounded-tl-none max-w-[80%] shadow-sm text-stone-700">
こんにちは！特定ユーザーの最新情報を検索・要約する準備ができています。シミュレーションを開始しますか？
</div>
</div>

<div class="p-3 bg-white border-t border-stone-200">
<button id="start-demo-btn" class="w-full bg-rose-600 hover:bg-rose-700 text-white font-bold py-3 px-4 rounded-lg transition-all active:scale-95 shadow-sm text-sm" onclick="runOpenClawDemo()">
「みこちの最新ニュースを教えて」と送信する
</button>
</div>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const codeData = {
'code-python': `# OpenClaw ツール実装: fetch_x_posts
import asyncio
from playwright.async_api import async_playwright

async def fetch_x_posts(user_id: str):
    """
    Yahooリアルタイム検索を利用して指定ユーザーの最新ポストを取得する
    """
    url = f"https://search.yahoo.co.jp/realtime/search?p=(id:{user_id})&ei=UTF-8"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        # 動的レンダリングを待機し、最新の3件のテキストを取得
        await page.wait_for_selector(".Tweet_body", timeout=5000)
        posts = await page.locator(".Tweet_body").all_text_contents()
        
        await browser.close()
        return posts[:3]`,
'code-prompt': `# OpenClaw エージェントへの指示出し（システムプロンプト）
TOOL_DESCRIPTION = """
このツールは、Xの最新ポスト3件をテキスト配列として返します。
取得した生データから、以下の優先順位に従って情報を抽出し、
ファン向けに【3行程度で要約】して回答を作成してください。

[抽出の優先順位]
1. 公式の告知（配信開始時間、イベント出演、コラボ情報など）
2. グッズ情報（販売開始、予約締切など）
3. 新作・重要アップデート（新作ゲーム、新曲公開など）

[注意事項]
日常的な挨拶やつぶやき（例：「おはよう」「お腹すいた」）は無視。
ファンが『今すぐ確認・行動すべき情報』を最優先すること。
読みやすく絵文字を適度に活用すること。
"""`
};

function switchOpenClawTab(showId, hideId, btn) {
const showElem = document.getElementById(showId);
const hideElem = document.getElementById(hideId);
if(showElem) { showElem.classList.remove('hidden'); showElem.classList.add('block'); }
if(hideElem) { hideElem.classList.add('hidden'); hideElem.classList.remove('block'); }

const container = btn.closest('.p-6');
container.querySelectorAll('.tab-btn').forEach(b => {
b.classList.remove('border-b-2', 'border-primary', 'text-white');
b.classList.add('text-stone-400');
});
btn.classList.add('border-b-2', 'border-primary', 'text-white');
btn.classList.remove('text-stone-400');
}
window.switchOpenClawTab = switchOpenClawTab;

setTimeout(function() {
// Inject Code
const pyElem = document.getElementById('code-python');
const promptElem = document.getElementById('code-prompt');
if(pyElem) pyElem.innerText = codeData['code-python'];
if(promptElem) promptElem.innerText = codeData['code-prompt'];

// Inject Chart
const chartContainer = document.getElementById('comparisonChartContainer');
if (chartContainer) {
chartContainer.innerHTML = '<canvas id="comparisonChart"></canvas>';
const ctx = document.getElementById('comparisonChart').getContext('2d');
new Chart(ctx, {
type: 'radar',
data: {
labels: ['コスト効率', '垢BAN安全性', '速報性', 'クエリ柔軟性', '導入手軽さ'],
datasets: [
{
label: 'Yahoo!リアルタイム',
data: [100, 100, 95, 90, 80],
backgroundColor: 'rgba(170, 164, 255, 0.2)',
borderColor: '#aaa4ff',
pointBackgroundColor: '#aaa4ff',
borderWidth: 2
},
{
label: '公式 X API',
data: [20, 60, 90, 40, 50],
backgroundColor: 'rgba(0, 210, 255, 0.1)',
borderColor: '#00d2ff',
pointBackgroundColor: '#00d2ff',
borderWidth: 2
}
]
},
options: {
responsive: true,
maintainAspectRatio: false,
scales: { r: { min: 0, max: 100, ticks: { display: false }, grid: { color: 'rgba(255,255,255,0.05)' }, pointLabels: { font: { size: 10, family: "'Inter', sans-serif" }, color: '#a3aac4' } } },
plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11, color: '#a3aac4' }, color: '#a3aac4' } } }
}
});
}
}, 250);

let demoRunning = false;
async function runOpenClawDemo() {
if (demoRunning) return;
demoRunning = true;
const btn = document.getElementById('start-demo-btn');
const chat = document.getElementById('chat-container');

btn.disabled = true;
btn.classList.add('opacity-50', 'cursor-not-allowed');
chat.innerHTML = '';

const addMsg = (type, content) => {
const div = document.createElement('div');
div.className = `self-${type === 'user' ? 'end' : type === 'system' ? 'center' : 'start'} ${type === 'system' ? 'w-full' : 'max-w-[85%]'} text-[12px] opacity-0 translate-y-2 transition-all duration-300`;
let inner = `<div class="p-3 rounded-2xl ${type === 'user' ? 'bg-primary text-background rounded-tr-none font-bold' : type === 'system' ? 'bg-stone-800 text-emerald-400 font-mono text-[10px] rounded-md border border-white/5' : 'bg-surface text-on-surface border border-white/5 rounded-tl-none'} shadow-sm">${content}</div>`;
div.innerHTML = inner;
chat.appendChild(div);
chat.scrollTop = chat.scrollHeight;
setTimeout(() => { div.classList.remove('opacity-0', 'translate-y-2'); }, 50);
};

const addLoader = () => {
const div = document.createElement('div');
div.id = 'demo-loader';
div.className = 'self-start';
div.innerHTML = '<div class="bg-surface p-3 rounded-2xl rounded-tl-none shadow-sm border border-white/10 inline-block"><div class="animate-spin rounded-full h-4 w-4 border-2 border-primary/20 border-t-primary"></div></div>';
chat.appendChild(div);
chat.scrollTop = chat.scrollHeight;
};

addMsg('user', 'みこちの最新ニュースを教えて');
await new Promise(r => setTimeout(r, 800));

addLoader();
await new Promise(r => setTimeout(r, 1500));
const loader = document.getElementById('demo-loader');
if(loader) loader.remove();
addMsg('system', 'Executing [fetch_x_posts] args: {"user_id": "sakuramiko35"}<br>> Yahoo Search accessed.<br>> Extracted 3 posts.');

await new Promise(r => setTimeout(r, 800));
addLoader();
await new Promise(r => setTimeout(r, 1200));
const loader2 = document.getElementById('demo-loader');
if(loader2) loader2.remove();
addMsg('system', '> Applying filtering rules through Gemini...');

await new Promise(r => setTimeout(r, 1000));
addMsg('bot', '最新の情報を3件まとめました！🌸<br><ul class="mt-2 space-y-1"><li>🔥 <strong>20:00より「エンドラ討伐」配信予定</strong></li><li>🛍️ <strong>新グッズが本日より受注開始（～末日）</strong></li><li>📢 <strong>明日19時の公式番組にゲスト出演決定</strong></li></ul>');

await new Promise(r => setTimeout(r, 1000));
demoRunning = false;
btn.disabled = false;
btn.classList.remove('opacity-50', 'cursor-not-allowed');
btn.innerText = "もう一度実行する";
}
window.runOpenClawDemo = runOpenClawDemo;
</script>

## 変更履歴 (Changelog)
- **2026-04-09**: `SKILL.md` 準拠のグローバルデザイン統一およびメタデータ標準化アップデートを実施。
- **2026-04-06**: 新規作成。Yahoo!リアルタイム検索を用いたOpenClawスキル実装ガイド。
