import os
import glob
import re

nav_template = '''        <a class="{cls_infra}" href="{prefix}infra/index.html">Infrastructure</a>
        <a class="{cls_dev}" href="{prefix}dev/index.html">Development</a>
        <a class="{cls_ai}" href="{prefix}ai/index.html">AI & Agents</a>
        <a class="{cls_finance}" href="{prefix}finance/index.html">Finance</a>
        <a class="{cls_lpo}" href="{prefix}lpo/index.html">LPO</a>
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
      </a>'''

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if we are in root or subfolder
    is_root = '\\' not in filepath and '/' not in filepath
    prefix = '' if is_root else '../'

    # Determine active nav
    cls_infra = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_dev = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_ai = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_finance = 'text-on-surface-variant hover:text-secondary transition-colors'
    cls_lpo = 'text-on-surface-variant hover:text-secondary transition-colors'
    
    if '\\infra\\' in filepath or '/infra/' in filepath: cls_infra = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\dev\\' in filepath or '/dev/' in filepath: cls_dev = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\ai\\' in filepath or '/ai/' in filepath: cls_ai = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\finance\\' in filepath or '/finance/' in filepath: cls_finance = 'text-secondary border-b-2 border-secondary pb-1'
    if '\\lpo\\' in filepath or '/lpo/' in filepath: cls_lpo = 'text-secondary border-b-2 border-secondary pb-1'

    # Standardize basic old links just in case
    content = content.replace('href="it/', 'href="infra/')
    content = content.replace('href="../it/', 'href="../infra/')
    content = content.replace('href="points/', 'href="finance/')
    content = content.replace('href="../points/', 'href="../finance/')

    # Replace Nav items block
    # We will look for <div class="hidden md:flex items-center gap-6 text-[10px] uppercase tracking-widest font-bold">
    nav_inner = nav_template.format(cls_infra=cls_infra, cls_dev=cls_dev, cls_ai=cls_ai, cls_finance=cls_finance, cls_lpo=cls_lpo, prefix=prefix)
    content = re.sub(
        r'(<div class="hidden md:flex items-center gap-6[^>]*>).*?(</div>)',
        r'\g<1>\n' + nav_inner + r'\n      \g<2>',
        content,
        flags=re.DOTALL
    )

    # Replace Aside block
    aside_inner = aside_template.format(prefix=prefix)
    content = re.sub(
        r'(<nav class="flex-1 space-y-1">).*?(</nav>)',
        r'\g<1>\n' + aside_inner + r'\n    \g<2>',
        content,
        flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update all html files
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            process_html_file(os.path.join(root, f))

# Update markdown links loosely
def update_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('(/it/', '(/infra/').replace('(it/', '(infra/').replace('(../it/', '(../infra/')
    content = content.replace('(/points/', '(/finance/').replace('(points/', '(finance/').replace('(../points/', '(../finance/')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.md') and not f.startswith('tmp_'):
            update_md(os.path.join(root, f))
