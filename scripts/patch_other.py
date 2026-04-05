import os
import re

# 1. Create other directory
os.makedirs('other', exist_ok=True)

# 2. Extract standard dev/index.html to use as template
if os.path.exists('dev/index.html'):
    with open('dev/index.html', 'r', encoding='utf-8') as f:
        other_content = f.read()

    # Update title and empty the grid for 'other'
    other_content = re.sub(
        r'<h2 class="text-4xl font-bold font-headline tracking-tighter text-on-surface mb-2">.*?</h2>',
        '<h2 class="text-4xl font-bold font-headline tracking-tighter text-on-surface mb-2">Other / Misc</h2>',
        other_content, flags=re.DOTALL
    )
    other_content = re.sub(
        r'<p class="text-on-surface-variant font-body text-sm tracking-wide leading-relaxed max-w-2xl text-slate-400">.*?</p>',
        '<p class="text-on-surface-variant font-body text-sm tracking-wide leading-relaxed max-w-2xl text-slate-400">\n                    多岐にわたる実験ログ、雑記、および既存のカテゴリに属さない研究ノート。\n                </p>',
        other_content, flags=re.DOTALL
    )
    other_content = re.sub(
        r'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="latest">.*?</div>',
        '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="latest">\n                <!-- 記事データ挿入位置 -->\n            </div>',
        other_content, flags=re.DOTALL
    )
    # Fix active state in dev to inactive
    other_content = other_content.replace('text-secondary border-b-2 border-secondary pb-1" href="../dev/index.html"', 'text-on-surface-variant hover:text-secondary transition-colors" href="../dev/index.html"')
    
    with open('other/index.html', 'w', encoding='utf-8') as f:
        f.write(other_content)

# 3. Patch all HTML files replacing the <nav> items and <aside> items.
nav_template = '''        <a class="{cls_infra}" href="{prefix}infra/index.html">Infrastructure</a>
        <a class="{cls_dev}" href="{prefix}dev/index.html">Development</a>
        <a class="{cls_ai}" href="{prefix}ai/index.html">AI & Agents</a>
        <a class="{cls_finance}" href="{prefix}finance/index.html">Finance</a>
        <a class="{cls_lpo}" href="{prefix}lpo/index.html">LPO</a>
        <a class="{cls_other}" href="{prefix}other/index.html">Other</a>
        <a class="text-on-surface-variant hover:text-secondary transition-colors" href="{prefix}glossary.html">Glossary</a>'''

aside_template = '''      <a class="flex items-center gap-3 py-2.5 px-4 text-slate-500 hover:bg-surface-container hover:text-primary transition-all hover:translate-x-1 duration-200" href="{prefix}infra/index.html">
        <span class="material-symbols-outlined text-lg">history</span>
        <span class="font-headline text-[10px] uppercase tracking-widest">Latest Logs</span>
      </a>
      <a class="flex items-center gap-3 py-2.5 px-4 text-slate-500 hover:bg-surface-container hover:text-primary transition-all hover:translate-x-1 duration-200" href="{prefix}dev/index.html">
        <span class="material-symbols-outlined text-lg">code</span>
        <span class="font-headline text-[10px] uppercase tracking-widest">Development</span>
      </a>
      <a class="flex items-center gap-3 py-2.5 px-4 text-slate-500 hover:bg-surface-container hover:text-primary transition-all hover:translate-x-1 duration-200" href="{prefix}ai/index.html">
        <span class="material-symbols-outlined text-lg">biotech</span>
        <span class="font-headline text-[10px] uppercase tracking-widest">AI Research</span>
      </a>
      <a class="flex items-center gap-3 py-2.5 px-4 text-slate-500 hover:bg-surface-container hover:text-primary transition-all hover:translate-x-1 duration-200" href="{prefix}finance/index.html">
        <span class="material-symbols-outlined text-lg">diamond</span>
        <span class="font-headline text-[10px] uppercase tracking-widest">Finance</span>
      </a>
      <a class="flex items-center gap-3 py-2.5 px-4 text-slate-500 hover:bg-surface-container hover:text-primary transition-all hover:translate-x-1 duration-200" href="{prefix}other/index.html">
        <span class="material-symbols-outlined text-lg">folder_open</span>
        <span class="font-headline text-[10px] uppercase tracking-widest">Other / Misc</span>
      </a>'''

def replace_nav_aside(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    is_root = '\\' not in filepath and '/' not in filepath
    prefix = '' if is_root else '../'

    cls_infra = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_dev = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_ai = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_finance = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_lpo = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_other = 'text-on-surface-variant hover:text-secondary transition-colors'
    
    if '\\infra\\' in filepath or '/infra/' in filepath: cls_infra = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\dev\\' in filepath or '/dev/' in filepath: cls_dev = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\ai\\' in filepath or '/ai/' in filepath: cls_ai = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\finance\\' in filepath or '/finance/' in filepath: cls_finance = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\lpo\\' in filepath or '/lpo/' in filepath: cls_lpo = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\other\\' in filepath or '/other/' in filepath: cls_other = 'text-secondary border-b-2 border-secondary pb-1'

    nav_inner = nav_template.format(cls_infra=cls_infra, cls_dev=cls_dev, cls_ai=cls_ai, cls_finance=cls_finance, cls_lpo=cls_lpo, cls_other=cls_other, prefix=prefix)
    content = re.sub(
        r'(<div class="hidden md:flex items-center gap-6[^>]*>).*?(</div>)',
        r'\g<1>\n' + nav_inner + r'\n      \g<2>',
        content,
        flags=re.DOTALL
    )

    aside_inner = aside_template.format(prefix=prefix)
    content = re.sub(
        r'(<nav class="flex-1 space-y-1">).*?(</nav>)',
        r'\g<1>\n' + aside_inner + r'\n    \g<2>',
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            replace_nav_aside(os.path.join(root, f))
