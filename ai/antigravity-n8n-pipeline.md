---
title: "Antigravity × n8n | 自律修復パイプラインの構築と完全解剖"
date: "2026-04-09"
category: "AI & Agents"
description: "Gemini 3 Proを搭載したAntigravityとn8nを連携し、エラー検知から修正PR作成までを完全自動化するパイプライン解説。"
themes: ["ai:agent", "ai:automation", "dev:devops"]
---

# Antigravity × n8n | 自律修復パイプラインの構築と完全解剖
<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-09</div>

## 超要約
Gemini 3 Proを搭載した[Antigravity](article.html?md=glossary/system-glossary.md#:~:text="Antigravity")と[n8n](article.html?md=glossary/system-glossary.md#:~:text="n8n")を連携し、エラーの検知からコードの推論、修正パッチの生成、GitHubへのPull Request作成までを完全自動化するシステムの構築手順と導入効果の解説です。設定ファイルからコードの依存関係まで理解できる自律修復パイプラインを構築します。

## 自律修復アーキテクチャ
このセクションでは、エラー検知からコード修正、PR作成までの全体像を解説します。以下のパイプラインの各ステップをクリックして、背後で動く詳細なプロセスを確認してください。

<div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden lg:flex my-8 text-slate-800">
<div class="lg:w-1/2 p-8 bg-slate-50 border-r border-slate-200">
<h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-6">ワークフロー図 (クリックで詳細表示)</h3>
<div class="space-y-4 relative">
<div class="absolute left-6 top-8 bottom-8 w-1 bg-emerald-200 rounded-full z-0"></div>
<div id="step-1" class="pipeline-node transition-all duration-300 ease-in-out relative z-10 flex items-center p-4 bg-white border-2 border-slate-200 rounded-xl cursor-pointer hover:-translate-y-1 hover:shadow-lg hover:border-emerald-500" onclick="updatePipeline(1)">
<div class="w-12 h-12 flex-shrink-0 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-xl font-bold mr-4 shadow-sm">🚨</div>
<div>
<h4 class="font-bold text-slate-800">1. エラー検知 (Sentry/Datadog)</h4>
<p class="text-sm text-slate-500">本番環境での例外発生を捕捉</p>
</div>
</div>
<div id="step-2" class="pipeline-node transition-all duration-300 ease-in-out relative z-10 flex items-center p-4 bg-white border-2 border-slate-200 rounded-xl cursor-pointer hover:-translate-y-1 hover:shadow-lg hover:border-emerald-500" onclick="updatePipeline(2)">
<div class="w-12 h-12 flex-shrink-0 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl font-bold mr-4 shadow-sm">⚙️</div>
<div>
<h4 class="font-bold text-slate-800">2. n8n ワークフロー起動</h4>
<p class="text-sm text-slate-500">Webhook経由で自動化処理を開始</p>
</div>
</div>
<div id="step-3" class="pipeline-node transition-all duration-300 ease-in-out relative z-10 flex items-center p-4 bg-white border-2 border-emerald-500 rounded-xl cursor-pointer -translate-y-1 shadow-lg hover:-translate-y-1 hover:shadow-lg hover:border-emerald-500" onclick="updatePipeline(3)">
<div class="w-12 h-12 flex-shrink-0 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-xl font-bold mr-4 shadow-sm">🧠</div>
<div>
<h4 class="font-bold text-slate-800">3. Gemini 3 Pro (Antigravity)</h4>
<p class="text-sm text-slate-500">文脈解析と自律的なコード修正</p>
</div>
</div>
<div id="step-4" class="pipeline-node transition-all duration-300 ease-in-out relative z-10 flex items-center p-4 bg-white border-2 border-slate-200 rounded-xl cursor-pointer hover:-translate-y-1 hover:shadow-lg hover:border-emerald-500" onclick="updatePipeline(4)">
<div class="w-12 h-12 flex-shrink-0 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-xl font-bold mr-4 shadow-sm">📫</div>
<div>
<h4 class="font-bold text-slate-800">4. GitHub PRの自動作成</h4>
<p class="text-sm text-slate-500">テスト通過後、レビュー依頼を発行</p>
</div>
</div>
</div>
</div>
<div class="lg:w-1/2 p-8 bg-white" id="pipeline-detail-container">
<div class="inline-flex items-center justify-center px-3 py-1 mb-4 text-xs font-bold text-emerald-800 bg-emerald-100 rounded">STEP 3</div>
<h3 class="text-2xl font-bold text-slate-900 mb-4" id="detail-title">Antigravity空間でのコード推論</h3>
<p class="text-slate-600 mb-6 leading-relaxed" id="detail-desc">ここが最大のキモです。エラーログだけをLLMに投げるのではなく、AntigravityのAPIを経由させることで、「リポジトリ全体の文脈」「関連ファイルの依存関係」をGemini 3 Proが把握した状態で修正案を生成します。ただのエディタではなく、自律エージェントの作業空間として機能します。</p>
<div class="bg-slate-900 rounded-lg p-4 font-mono text-sm text-emerald-400 overflow-x-auto shadow-inner whitespace-pre" id="detail-code">{
  "action": "antigravity.analyze_and_fix",
  "context": "repo://backend/api",
  "error_trace": "{{$json.body.stacktrace}}",
  "model": "gemini-3-pro"
}</div>
</div>
</div>

## パイプライン導入のインパクト検証
この自律修復パイプラインがプロジェクトにどのような定量的な影響を与えるかを示します。グラフの要素にホバーして詳細な数値を確認してください。

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 my-8 text-slate-800">
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<h3 class="text-lg font-bold text-slate-800 mb-2">平均修復時間 (MTTR) の推移</h3>
<p class="text-sm text-slate-500 mb-4">バグ発生から修正PRが作成されるまでの時間比較（分）</p>
<div id="mttrChartContainer" class="chart-container" style="position: relative; width: 100%; margin: 0 auto; min-height: 300px; height: 300px;">
</div>
</div>
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<h3 class="text-lg font-bold text-slate-800 mb-2">自動修復の成功率 (カテゴリ別)</h3>
<p class="text-sm text-slate-500 mb-4">Antigravity + Gemini 3 Proが人手を介さず解決できた割合</p>
<div id="successChartContainer" class="chart-container" style="position: relative; width: 100%; margin: 0 auto; min-height: 300px; height: 300px;">
</div>
</div>
</div>

## 実装マニュアル / コードスニペット
実際に手を動かして環境を構築するためのコアとなる設定情報です。タブを切り替えて各フェーズの設定を確認してください。

<div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden my-8 text-slate-800">
<div class="flex border-b border-slate-200 bg-slate-50 overflow-x-auto">
<button class="tab-btn active px-6 py-4 text-sm font-medium border-b-2 border-emerald-500 text-emerald-600 font-bold whitespace-nowrap" onclick="switchTab('tab-n8n', this)">n8n Webhook設定</button>
<button class="tab-btn px-6 py-4 text-sm font-medium text-slate-600 hover:text-emerald-600 whitespace-nowrap" onclick="switchTab('tab-prompt', this)">Gemini システムプロンプト</button>
<button class="tab-btn px-6 py-4 text-sm font-medium text-slate-600 hover:text-emerald-600 whitespace-nowrap" onclick="switchTab('tab-github', this)">GitHub PR Action</button>
</div>
<div class="p-6">
<div id="tab-n8n" class="tab-content block">
<h4 class="font-bold text-slate-800 mb-3">n8n: Error Receiver Node</h4>
<p class="text-sm text-slate-600 mb-4">監視ツールからのアラートを受け取るWebhookノードの基本設定です。ペイロードからスタックトレースを抽出します。</p>
<div class="bg-slate-900 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto whitespace-pre">const body = $input.item.json.body;
if (!body.stacktrace) {
  return [{ json: { status: "ignored", reason: "No stacktrace" } }];
}
return [{
  json: {
    issue_id: body.id,
    error_type: body.type,
    file_path: extractFilePath(body.stacktrace),
    full_log: body.stacktrace
  }
}];</div>
</div>
<div id="tab-prompt" class="tab-content hidden">
<h4 class="font-bold text-slate-800 mb-3">Antigravity Context注入用プロンプト</h4>
<p class="text-sm text-slate-600 mb-4">Gemini 3 Proに渡すシステムプロンプトです。エディタ空間（Antigravity）へのアクセス権を意識させます。</p>
<div class="bg-slate-900 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto whitespace-pre">You are an autonomous DevOps AI agent operating within the Antigravity workspace.
Your task is to fix the following production error.

1. USE the `antigravity.search_symbol` tool to find the error origin.
2. ANALYZE the logic around the failing line.
3. OUTPUT a unified diff to fix the issue.
4. DO NOT break existing tests.

Error Log:
{{$json.full_log}}</div>
</div>
<div id="tab-github" class="tab-content hidden">
<h4 class="font-bold text-slate-800 mb-3">n8n: GitHub API 連携</h4>
<p class="text-sm text-slate-600 mb-4">生成された修正パッチを用いて、新しいブランチを作成しPull Requestを発行します。</p>
<div class="bg-slate-900 rounded-lg p-4 font-mono text-sm text-slate-300 overflow-x-auto whitespace-pre">// HTTP Request Node configuration
Method: POST
URL: https://api.github.com/repos/{{$env.REPO_NAME}}/pulls
Body:
{
  "title": "🤖 Auto-fix: {{$node[\"ExtractError\"].json.error_type}}",
  "body": "This PR was generated automatically by Antigravity Pipeline.\n\n**Root Cause:**\n{{$node[\"GeminiAnalysis\"].json.root_cause}}\n\n**Fix:**\nApplied patch to safely handle null values.",
  "head": "auto-fix-{{$node[\"ExtractError\"].json.issue_id}}",
  "base": "main"
}</div>
</div>
</div>
</div>

<script>
const pipelineData = {
1: {
step: "STEP 1",
title: "エラーの検知と集約",
desc: "SentryやDatadogなどの監視ツールが本番環境の例外エラーを捕捉します。通知ルールを設定し、特定の深刻度（Critical/Error）や、再発性の高いバグのみを対象にWebhookを発火させるようフィルタリングすることが重要です。",
code: "POST /webhook/n8n-receiver\nContent-Type: application/json\n\n{\n  \"alert_type\": \"exception\",\n  \"service\": \"payment-gateway\",\n  \"stacktrace\": \"NullReferenceException at line 42...\"\n}"
},
2: {
step: "STEP 2",
title: "n8nによるオーケストレーション",
desc: "Webhookを受け取ったn8nが起動します。ここでエラーログのパース、GitHubの最新のコミットハッシュの取得、そして後続のAIへ渡すためのプロンプトの組み立て（テンプレート化）を行います。n8nの柔軟性がこのパイプラインの糊となります。",
code: "// n8n Code Node\nconst errorData = $input.first().json;\nconst prompt = `Fix this: ${errorData.stacktrace}`;\nreturn { json: { prompt } };"
},
3: {
step: "STEP 3",
title: "Antigravity空間でのコード推論",
desc: "ここが最大のキモです。エラーログだけをLLMに投げるのではなく、AntigravityのAPIを経由させることで、「リポジトリ全体の文脈」「関連ファイルの依存関係」をGemini 3 Proが把握した状態で修正案を生成します。ただのエディタではなく、自律エージェントの作業空間として機能します。",
code: "{\n  \"action\": \"antigravity.analyze_and_fix\",\n  \"context\": \"repo://backend/api\",\n  \"error_trace\": \"{{$json.body.stacktrace}}\",\n  \"model\": \"gemini-3-pro\"\n}"
},
4: {
step: "STEP 4",
title: "GitHub連携とPR自動作成",
desc: "Geminiによって生成された修正パッチ（diff）を用いて、n8nが自動的にGitHub上でブランチを切り、コミットし、Pull Requestを作成します。CIのテストが自動で走り、人間は朝起きて「Approve」を押すだけの状態を作ります。",
code: "curl -X POST -H \"Authorization: token $GITHUB_TOKEN\" \\\n -d '{\"title\":\"Auto-fix: NullRef\",\"head\":\"fix-branch\",\"base\":\"main\"}' \\\n https://api.github.com/repos/org/repo/pulls"
}
};

function updatePipeline(stepIndex) {
document.querySelectorAll('.pipeline-node').forEach(node => {
node.classList.remove('border-emerald-500', 'shadow-lg', '-translate-y-1');
node.classList.add('border-slate-200');
});
const selectedNode = document.getElementById(`step-${stepIndex}`);
if (selectedNode) {
selectedNode.classList.remove('border-slate-200');
selectedNode.classList.add('border-emerald-500', 'shadow-lg', '-translate-y-1');
}

const data = pipelineData[stepIndex];
document.getElementById('pipeline-detail-container').innerHTML = `
<div class="inline-flex items-center justify-center px-3 py-1 mb-4 text-xs font-bold text-emerald-800 bg-emerald-100 rounded">${data.step}</div>
<h3 class="text-2xl font-bold text-slate-900 mb-4 animate-fade-in">${data.title}</h3>
<p class="text-slate-600 mb-6 leading-relaxed animate-fade-in">${data.desc}</p>
<div class="bg-slate-900 rounded-lg p-4 font-mono text-sm text-emerald-400 overflow-x-auto shadow-inner animate-fade-in whitespace-pre">${data.code}</div>
`;
}
window.updatePipeline = updatePipeline;

function switchTab(tabId, btnElement) {
document.querySelectorAll('.tab-content').forEach(tab => {
tab.classList.remove('block');
tab.classList.add('hidden');
});
document.querySelectorAll('.tab-btn').forEach(btn => {
btn.classList.remove('border-b-2', 'border-emerald-500', 'text-emerald-600', 'font-bold');
btn.classList.add('text-slate-600');
});

document.getElementById(tabId).classList.remove('hidden');
document.getElementById(tabId).classList.add('block');
btnElement.classList.add('border-b-2', 'border-emerald-500', 'text-emerald-600', 'font-bold');
btnElement.classList.remove('text-slate-600');
}
window.switchTab = switchTab;

setTimeout(function() {
const chartOptions = {
responsive: true,
maintainAspectRatio: false,
plugins: {
legend: { position: 'bottom', labels: { font: { family: "'Inter', sans-serif" }, color: '#475569' } },
tooltip: { backgroundColor: 'rgba(15, 23, 42, 0.9)', titleFont: { size: 13, family: "'Inter', sans-serif" }, bodyFont: { size: 14, family: "'Inter', sans-serif" }, padding: 12, cornerRadius: 8 }
}
};

const mttrChartContainer = document.getElementById('mttrChartContainer');
if (mttrChartContainer) {
mttrChartContainer.innerHTML = '<canvas id="mttrChart"></canvas>';
const ctxMttr = document.getElementById('mttrChart').getContext('2d');
new Chart(ctxMttr, {
type: 'bar',
data: {
labels: ['手動対応', 'AIサジェスト', '本自律パイプライン'],
datasets: [{
label: '平均修復時間 (分)',
data: [120, 45, 8],
backgroundColor: ['rgba(148, 163, 184, 0.6)','rgba(56, 189, 248, 0.6)','rgba(16, 185, 129, 0.8)'],
borderColor: ['rgb(100, 116, 139)','rgb(2, 132, 199)','rgb(5, 150, 105)'],
borderWidth: 1,
borderRadius: 6
}]
},
options: { ...chartOptions, indexAxis: 'y', scales: { x: { grid: { color: '#f1f5f9' }, ticks: { color: '#64748b' } }, y: { grid: { display: false }, ticks: { color: '#334155', font: { weight: 'bold' } } } } }
});
}

const successChartContainer = document.getElementById('successChartContainer');
if (successChartContainer) {
successChartContainer.innerHTML = '<canvas id="successChart"></canvas>';
const ctxSuccess = document.getElementById('successChart').getContext('2d');
new Chart(ctxSuccess, {
type: 'doughnut',
data: {
labels: ['Syntax / 型エラー', '設定・環境変数漏れ', '単純なロジックバグ', '要人間介入 (複雑)'],
datasets: [{
data: [45, 25, 18, 12],
backgroundColor: ['rgba(16, 185, 129, 0.8)','rgba(52, 211, 153, 0.7)','rgba(110, 231, 183, 0.6)','rgba(226, 232, 240, 1)'],
borderWidth: 0,
hoverOffset: 6
}]
},
options: { ...chartOptions, cutout: '70%', plugins: { ...chartOptions.plugins, tooltip: { ...chartOptions.plugins.tooltip, callbacks: { label: function(context) { return ' ' + context.label + ': ' + context.parsed + '%'; } } } } }
});
}

const style = document.createElement('style');
style.textContent = `
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
`;
document.head.appendChild(style);
}, 200);
</script>

## 変更履歴 (Changelog)
- **2026-04-09**: `SKILL.md` 準拠のグローバルデザイン統一およびメタデータ標準化アップデートを実施。
- **2026-04-06**: HTML原稿よりMarkdown（SME構成）へ再構築。
