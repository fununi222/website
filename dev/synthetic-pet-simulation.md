---
title: "Development | Synthetic Pet Simulation：合成生命体の自律エージェント試論 2026"
date: "2026-04-13"
category: "dev"
description: "ステートマシンと localStorage を用いた、デジタル生命体の空腹・幸福・エネルギー管理シミュレーション。"
themes: ["dev:webapp", "dev:ux", "ai:agents"]
---

# Development | Synthetic Pet Simulation：合成生命体の自律エージェント試論 2026

<figure class="mb-10 max-w-4xl mx-auto cyber-glow">
<img src="../assets/img/dev/synthetic-pet-simulation.png" alt="Synthetic Pet Handheld Device" class="w-full rounded-2xl shadow-xl border border-white/10 object-cover hover:border-primary/50 transition-colors duration-300">
</figure>

本プロジェクトは、[フロントエンド](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="フロントエンド")技術のみで完結する「たまごっち風」の自律型エージェント・シミュレーターです。単なるゲーム制作にとどまらず、**「時間経過による状態（State）の減衰」**と**「localStorage による永続化」**の実装を通じて、デジタル環境における自律生命体の[UI](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UI")/[UX](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="UX")設計を検証します。

<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono">Last Updated: 2026-04-13</div>

---

## 💻 Simulation Core

以下のシミュレーターは、リアルタイムでペットの状態を計算します。
現在は**ミント・ゴースト・キャット**（デジタル生命体）が稼働しています。

<!-- Game Container -->
<div id="pet-sim-root" class="my-12 flex flex-col items-center">
<div class="relative w-72 h-[450px] bg-surface-container rounded-[50px] border-[6px] border-[#b2f2bb]/30 shadow-2xl p-4 flex flex-col items-center justify-between cyber-glow-mint glass hover:scale-[1.02] transition-transform duration-500">
<div class="w-full flex justify-between px-4 text-[8px] font-mono text-primary/50 uppercase tracking-widest">
<span>SYNTH_OS v4.13-MINT</span>
<span id="pet-battery">100%</span>
</div>
<div id="pet-screen" class="relative w-full h-56 bg-[#0a1a14] rounded-3xl border border-primary/20 overflow-hidden inner-glow flex items-center justify-center" style="background-image: url('../assets/img/dev/pet-bg-spring.png'); background-size: cover; background-position: center;">
<div class="absolute inset-0 bg-black/20 pointer-events-none"></div>
<div id="pet-container" class="relative z-10 w-32 h-32 flex items-center justify-center">
<img id="pet-mascot" src="../assets/img/dev/mascot-v3-idle.png" class="w-24 h-24 object-contain pet-bobbing transition-all duration-300 chromakey-active" style="image-rendering: pixelated;">
</div>
<div id="pet-emotion" class="absolute top-4 right-4 text-2xl animate-bounce"></div>
<div class="absolute bottom-2 left-4 text-[8px] font-mono text-white tracking-widest uppercase bg-black/30 px-1 rounded">
Age: <span id="pet-age">0</span> CYCLES
</div>
<div id="pet-status-msg" class="absolute top-4 left-4 text-[9px] font-mono text-primary font-bold opacity-0 transition-opacity drop-shadow-md">LOW ENERGY</div>
</div>
<div class="w-full px-2 space-y-3">
<div class="space-y-1">
<div class="flex justify-between text-[9px] font-bold uppercase tracking-tighter">
<span>Hunger</span><span id="val-hunger">100%</span>
</div>
<div class="h-1.5 bg-background rounded-full overflow-hidden border border-white/5">
<div id="bar-hunger" class="h-full bg-primary transition-all duration-500" style="width: 100%;"></div>
</div>
</div>
<div class="space-y-1">
<div class="flex justify-between text-[9px] font-bold uppercase tracking-tighter">
<span>Happiness</span><span id="val-happiness">100%</span>
</div>
<div class="h-1.5 bg-background rounded-full overflow-hidden border border-white/5">
<div id="bar-happiness" class="h-full bg-[#b2f2bb] transition-all duration-500" style="width: 100%;"></div>
</div>
</div>
<div class="space-y-1">
<div class="flex justify-between text-[9px] font-bold uppercase tracking-tighter">
<span>Energy</span><span id="val-energy">100%</span>
</div>
<div class="h-1.5 bg-background rounded-full overflow-hidden border border-white/5">
<div id="bar-energy" class="h-full bg-secondary transition-all duration-500" style="width: 100%;"></div>
</div>
</div>
</div>
<div class="grid grid-cols-2 gap-2 w-full mt-4">
<button onclick="petAction('feed')" class="action-btn py-3 rounded-2xl bg-surface-container-high border border-white/5 hover:border-primary/50 text-on-surface text-[10px] font-headline uppercase tracking-widest transition-all active:scale-95 flex flex-col items-center gap-1">
<span class="material-symbols-outlined text-sm">restaurant</span>
<span>Feed</span>
</button>
<button onclick="petAction('play')" class="action-btn py-3 rounded-2xl bg-surface-container-high border border-white/5 hover:border-primary/50 text-on-surface text-[10px] font-headline uppercase tracking-widest transition-all active:scale-95 flex flex-col items-center gap-1">
<span class="material-symbols-outlined text-sm">smart_toy</span>
<span>Play</span>
</button>
<button onclick="petAction('charge')" class="action-btn py-3 rounded-2xl bg-surface-container-high border border-white/5 hover:border-secondary/50 text-on-surface text-[10px] font-headline uppercase tracking-widest transition-all active:scale-95 flex flex-col items-center gap-1">
<span class="material-symbols-outlined text-sm">bolt</span>
<span>Charge</span>
</button>
<button onclick="resetPet()" class="action-btn py-3 rounded-2xl bg-surface-container-high border border-white/5 hover:border-red-400/50 text-on-surface text-[10px] font-headline uppercase tracking-widest transition-all active:scale-95 flex flex-col items-center gap-1">
<span class="material-symbols-outlined text-sm">refresh</span>
<span>Reset</span>
</button>
</div>
<div class="mt-4 text-[10px] font-bold tracking-[0.2em] text-[#b2f2bb] opacity-30">FUNUNI_SYNTH_CORE_MINT</div>
</div>
</div>

<!-- SVG Chromakey Filter -->
<svg width="0" height="0" style="position:absolute">
  <filter id="chromakey">
    <feColorMatrix type="matrix" values="1 0 0 0 0
                                         0 1 0 0 0
                                         0 0 1 0 0
                                         1 -1 1 1 0" />
  </filter>
</svg>

<style>
.inner-glow { box-shadow: inset 0 0 20px rgba(178, 242, 187, 0.1); }
.cyber-glow-mint { box-shadow: 0 0 30px rgba(178, 242, 187, 0.05); }
.action-btn:hover { background: rgba(178, 242, 187, 0.05); }
.pet-bobbing {
animation: sprite-bob 2.5s infinite ease-in-out;
}
@keyframes sprite-bob {
0%, 100% { transform: translateY(0) scale(1, 1); }
50% { transform: translateY(-12px) scale(1.02, 0.98); }
}
.chromakey-active {
filter: url(#chromakey);
}
.pet-sad { opacity: 0.9; }
.pet-sleeping { opacity: 0.7; transform: scale(0.9) translateY(10px) !important; }
</style>

<script>
const PET_STORAGE_KEY = 'fununi_synth_pet_v1';
const SPRITES = {
idle: '../assets/img/dev/mascot-v3-idle.png',
happy: '../assets/img/dev/mascot-v3-happy.png',
sad: '../assets/img/dev/mascot-v3-sad.png',
sleep: '../assets/img/dev/mascot-v3-sleep.png'
};
let petState = {
hunger: 100,
happiness: 100,
energy: 100,
age: 0,
lastUpdate: Date.now(),
isDead: false
};
function initSimulation() {
const saved = localStorage.getItem(PET_STORAGE_KEY);
if (saved) {
const parsed = JSON.parse(saved);
const now = Date.now();
const secondsPassed = Math.floor((now - parsed.lastUpdate) / 1000);
petState = {
...parsed,
hunger: Math.max(0, parsed.hunger - (secondsPassed * 0.05)),
happiness: Math.max(0, parsed.happiness - (secondsPassed * 0.03)),
energy: Math.max(0, parsed.energy - (secondsPassed * 0.02)),
age: parsed.age + Math.floor(secondsPassed / 100),
lastUpdate: now
};
}
startTick();
}
function startTick() {
setInterval(() => {
if (petState.isDead) return;
petState.hunger = Math.max(0, petState.hunger - 0.2);
petState.happiness = Math.max(0, petState.happiness - 0.1);
petState.energy = Math.max(0, petState.energy - 0.05);
petState.lastUpdate = Date.now();
updateUI();
saveState();
}, 1000);
}
function updateUI() {
document.getElementById('bar-hunger').style.width = petState.hunger + '%';
document.getElementById('bar-happiness').style.width = petState.happiness + '%';
document.getElementById('bar-energy').style.width = petState.energy + '%';
document.getElementById('val-hunger').innerText = Math.round(petState.hunger) + '%';
document.getElementById('val-happiness').innerText = Math.round(petState.happiness) + '%';
document.getElementById('val-energy').innerText = Math.round(petState.energy) + '%';
document.getElementById('pet-battery').innerText = Math.round(petState.energy) + '%';
document.getElementById('pet-age').innerText = petState.age;
const mascot = document.getElementById('pet-mascot');
const emotion = document.getElementById('pet-emotion');
const statusMsg = document.getElementById('pet-status-msg');
mascot.classList.remove('pet-sad', 'pet-sleeping');
emotion.innerText = '';
statusMsg.style.opacity = '0';
let currentSprite = SPRITES.idle;
if (petState.hunger < 20 || petState.happiness < 20) {
currentSprite = SPRITES.sad;
mascot.classList.add('pet-sad');
emotion.innerText = '💧';
} else if (petState.energy < 30) {
currentSprite = SPRITES.sleep;
mascot.classList.add('pet-sleeping');
emotion.innerText = '💤';
statusMsg.innerText = 'LOW ENERGY';
statusMsg.style.opacity = '1';
} else if (petState.hunger > 80 && petState.happiness > 80) {
currentSprite = SPRITES.happy;
emotion.innerText = '✨';
}
if (mascot.src.indexOf(currentSprite) === -1) {
mascot.src = currentSprite;
}
}
function petAction(type) {
if (petState.isDead) return;
const feedback = document.createElement('div');
feedback.className = 'absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-2xl animate-ping text-primary z-50 pointer-events-none';
switch(type) {
case 'feed':
petState.hunger = Math.min(100, petState.hunger + 25);
feedback.innerText = '🔋';
break;
case 'play':
petState.happiness = Math.min(100, petState.happiness + 25);
petState.energy = Math.max(0, petState.energy - 10);
feedback.innerText = '🎮';
break;
case 'charge':
petState.energy = Math.min(100, petState.energy + 40);
feedback.innerText = '⚡';
break;
}
document.getElementById('pet-container').appendChild(feedback);
setTimeout(() => feedback.remove(), 1000);
updateUI();
saveState();
}
function saveState() {
localStorage.setItem(PET_STORAGE_KEY, JSON.stringify(petState));
}
function resetPet() {
if (!confirm('RESET SYSTEM? Data will be wiped.')) return;
petState = {
hunger: 100,
happiness: 100,
energy: 100,
age: 0,
lastUpdate: Date.now(),
isDead: false
};
updateUI();
saveState();
}
setTimeout(initSimulation, 500);
</script>

---

## 🛠️ Implementation Details

### Mascot Redesign
最新の設計に基づき、マスコットを[ミント・ゴースト・キャット]へと刷新しました。このデジタル生命体は、透過性のあるボディとサイバーな配色が特徴で、FunUni-lab の Technical Archive の美学を体現しています。

### Mint-Cyber Aesthetic
キャラクターの変更に伴い、ハードウェア（UIフレーム）の配色もミントグリーン（#b2f2bb）ベースへと変更しました。これにより、春の背景とマスコットが視覚的にシームレスに統合されています。従来のクロマキー技術によるリアルタイム透過処理も継続して適用されています。

## 今後の展望
今後は[LLM](https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md#:~:text="LLM")と連携し、特定条件下でマスコットのボディカラーが変化する動的な色彩変化システムや、ユーザーの入力に応じたプロトコル反応の実装を予定しています。

---

## 変更履歴 (Changelog)
- **2026-04-13**: マスコットを「ミント・ゴースト・キャット」へと刷新。UIテーマカラーをミントグリーンへ変更。
- **2026-04-13**: 季節限定背景（春）の追加。クロマキーフィルタによるマスコットの透過実装。
- **2026-04-13**: ビジュアルの全面刷新（さくらみこ風マスコット）。ドット絵スプライトシステムの実装。
- **2026-04-13**: 初回デプロイ。ステート管理と永続化機能を実装。
