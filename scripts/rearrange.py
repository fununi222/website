import os
import re

html_blocks = {}
categories = {
    'infra': ['2026-04-03-win-110-scaling-fancyzones.html', '2026-04-02-ctk-auto-remediation.html', '2026-04-03-oss-research-operation.html', '2026-04-04-openclaw-vps-network-troubleshoot.html'],
    'dev': ['2026-04-05-freeman-project-hp-retrospective.html', '2026-04-05-altra-recommender-retrospective.html'],
    'ai': ['2026-04-05-1bit-llm-bonsai-8b.html', '2026-04-05-ai-hallucination.html', '2026-04-04-universe-spec-debug.html', '2026-04-03-agent-orchestration.html', '2026-04-05-openclaw-google-calendar-automation.html', '2026-04-03-operation-automation.html', '2026-04-03-oss-automation-tools.html'],
    'finance': ['2026-04-04-high-return-payment-routes.html', '2026-04-05-smbc-million-challenge-revolut-route.html']
}

# 1. Extract all grid blocks from the index files
for folder in ['infra', 'dev', 'ai', 'finance', 'lpo']:
    path = os.path.join(folder, 'index.html')
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple extraction block
    # Regex format: <a href="202...html" class="... cyber-glow">...</a> matches all article links in grid
    blocks = re.findall(r'(<a href="202.*?" class="group block p-6 bg-surface-container.*?</a>)', content, flags=re.DOTALL)
    for block in blocks:
        filename = re.search(r'href="([^"]+)"', block).group(1)
        # Avoid duplicate additions (dev is a copy of infra so it might have dupes)
        if filename not in html_blocks:
            html_blocks[filename] = block

# Ensure all needed blocks exist. Wait! Some might be named differently or missed by regex.
# Let's count them
print(f"Extracted {len(html_blocks)} blocks.")
for file in [f for items in categories.values() for f in items]:
    if file not in html_blocks:
        print(f"Missing block for: {file}")

# 2. Re-write each index.html grid with proper items
titles = {
    'infra': ('IT & Infrastructure', 'インフラ運用・ネットワーク・監視システムに関するノート。'),
    'dev': ('Development & Architecture', 'フロントエンド・バックエンドの実装設計、推薦システム等のアーキテクチャ。'),
    'ai': ('AI, Agents & Automation', 'LLM、エージェントワークフロー、業務自動化プロセスに関する研究ログ。'),
    'finance': ('Finance & Points', '経済圏ハック、効率的なポイント還元ルートとアセット管理。'),
    'lpo': ('LPO Dashboard', 'コンバージョン最適化のためのダッシュボード。')
}

for folder in ['infra', 'dev', 'ai', 'finance']:
    path = os.path.join(folder, 'index.html')
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_grid = ''
    for article in categories[folder]:
        if article in html_blocks:
            new_grid += '\n                ' + html_blocks[article] + '\n'

    title, desc = titles[folder]
    
    # Replace the title block
    content = re.sub(
        r'<h2 class="text-4xl font-bold font-headline tracking-tighter text-on-surface mb-2">.*?</h2>',
        f'<h2 class="text-4xl font-bold font-headline tracking-tighter text-on-surface mb-2">{title}</h2>',
        content, flags=re.DOTALL
    )
    content = re.sub(
        r'<p class="text-on-surface-variant font-body text-sm tracking-wide leading-relaxed max-w-2xl text-slate-400">.*?</p>',
        f'<p class="text-on-surface-variant font-body text-sm tracking-wide leading-relaxed max-w-2xl text-slate-400">\n                    {desc}\n                </p>',
        content, flags=re.DOTALL
    )

    # Replace the grid block content
    content = re.sub(
        r'(<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"[^>]*>).*?(</section>)',
        r'\g<1>' + new_grid.replace('\\', '\\\\') + r'\n            </div>\n        \g<2>',
        content, flags=re.DOTALL
    )
    
    # Fix the footer title
    content = re.sub(
        r'© 2026 FunUni-lab Synthetic Edition\. [^<]*</div>',
        f'© 2026 FunUni-lab Synthetic Edition. {title} Division.</span>\n            </div>',
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
         f.write(content)
print("Updated all grids")
