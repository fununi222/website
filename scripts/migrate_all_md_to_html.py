import os
import re
import sys
import json
import markdown

ROOT_DIR = '.'
MD_DIR = 'md'
JSON_OUT_PATH = 'assets/data/article_index.json'

CATEGORY_THEMES = {
    'infra': {'color': '#aaa4ff', 'name': 'Infrastructure', 'badge': 'Domain_01 / Infra'},
    'dev': {'color': '#00d2ff', 'name': 'Development', 'badge': 'Domain_02 / Dev'},
    'ai': {'color': '#00ffca', 'name': 'AI Research', 'badge': 'Domain_03 / AI'},
    'finance': {'color': '#fbbf24', 'name': 'Finance', 'badge': 'Domain_04 / Finance'},
    'lpo': {'color': '#c084fc', 'name': 'Optimization', 'badge': 'Domain_05 / LPO'},
    'other': {'color': '#34d399', 'name': 'Strategic Life', 'badge': 'Domain_06 / Life'},
    'youtube': {'color': '#ef4444', 'name': 'YouTube Lab', 'badge': 'Domain_07 / Media'},
    'glossary': {'color': '#aaa4ff', 'name': 'Glossary', 'badge': 'System Glossary'}
}

HTML_PAGE_TEMPLATE = """<!DOCTYPE html>
<html class="dark" lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | FunUni-lab</title>
  
  <!-- SEO & OGP -->
  <meta name="description" content="{description}" />
  <meta property="og:title" content="{title} | FunUni-lab" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="FunUni-lab" />
  <meta name="twitter:card" content="summary_large_image" />

  <!-- Styling & Typography -->
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
  
  <!-- Code Highlighting & Diagrams -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <link rel="stylesheet" href="{rel_root}assets/css/synthetic.css">
  <style>
    :root {{
      --obsidian: #0a0c14;
      --surface-glass: rgba(255, 255, 255, 0.03);
      --border-glass: rgba(255, 255, 255, 0.08);
      --accent-theme: {theme_color};
    }}
    
    body {{ background-color: var(--obsidian); color: #e2e8f0; font-family: 'Inter', 'Noto Sans JP', sans-serif; }}
    .glass-card {{ background: var(--surface-glass); backdrop-filter: blur(20px); border: 1px solid var(--border-glass); border-radius: 20px; }}
    .bg-mesh {{ position: fixed; inset: 0; z-index: -1; background: radial-gradient(circle at 80% 20%, {theme_color}0f 0%, transparent 60%), radial-gradient(circle at 20% 80%, rgba(6, 182, 212, 0.04) 0%, transparent 60%); }}
    
    /* Article Typography */
    .article-body h1 {{ display: none; }} /* Title rendered in header */
    .article-body h2 {{ font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif; font-size: 1.75rem; font-weight: 700; color: #fff; margin-top: 3rem; margin-bottom: 1.25rem; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); }}
    .article-body h3 {{ font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif; font-size: 1.25rem; font-weight: 600; color: {theme_color}; margin-top: 2rem; margin-bottom: 0.75rem; }}
    .article-body h4 {{ font-size: 1.05rem; font-weight: 600; color: #e2e8f0; margin-top: 1.5rem; margin-bottom: 0.5rem; }}
    .article-body p {{ margin-bottom: 1.25rem; line-height: 1.85; color: #94a3b8; }}
    .article-body ul {{ list-style-type: disc; padding-left: 1.5rem; margin-bottom: 1.25rem; color: #94a3b8; }}
    .article-body ol {{ list-style-type: decimal; padding-left: 1.5rem; margin-bottom: 1.25rem; color: #94a3b8; }}
    .article-body li {{ margin-bottom: 0.4rem; line-height: 1.75; }}
    .article-body a {{ color: {theme_color}; text-decoration: none; border-bottom: 1px solid transparent; transition: all 0.2s; }}
    .article-body a:hover {{ filter: brightness(1.2); border-bottom-color: {theme_color}; }}
    .article-body hr {{ border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 2.5rem 0; }}
    
    /* Table Styling */
    .table-wrap {{ width: 100%; margin: 1.5rem 0; overflow-x: auto; -webkit-overflow-scrolling: touch; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; background: rgba(255,255,255,0.02); }}
    table {{ width: 100%; border-collapse: collapse; min-width: 540px; font-size: 0.92rem; }}
    thead {{ background: {theme_color}14; border-bottom: 1px solid rgba(255,255,255,0.1); }}
    th {{ color: #e2e8f0; font-family: 'Space Grotesk', sans-serif; font-weight: 700; padding: 0.9rem 1.2rem; text-align: left; letter-spacing: 0.05em; }}
    td {{ color: #94a3b8; padding: 0.9rem 1.2rem; border-bottom: 1px solid rgba(255,255,255,0.05); }}
    tr:hover td {{ background-color: rgba(255,255,255,0.02); }}
    
    /* Code styling */
    pre[class*="language-"] {{ background: #0f172a !important; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.25rem; margin: 1.5rem 0; overflow-x: auto; }}
    code:not([class*="language-"]) {{ background: rgba(255,255,255,0.1); padding: 0.2rem 0.4rem; border-radius: 4px; font-family: monospace; font-size: 0.875em; color: {theme_color}; }}
    
    /* Custom Callouts */
    .callout-note {{ background: rgba(255, 255, 255, 0.03); border-left: 4px solid {theme_color}; border-radius: 0 12px 12px 0; padding: 1.25rem; margin: 1.75rem 0; }}
    .callout-tip {{ background: rgba(52, 211, 153, 0.05); border-left: 4px solid #34d399; border-radius: 0 12px 12px 0; padding: 1.25rem; margin: 1.75rem 0; }}
    .callout-warning {{ background: rgba(245, 158, 11, 0.05); border-left: 4px solid #f59e0b; border-radius: 0 12px 12px 0; padding: 1.25rem; margin: 1.75rem 0; }}
    .callout-caution {{ background: rgba(239, 68, 68, 0.05); border-left: 4px solid #ef4444; border-radius: 0 12px 12px 0; padding: 1.25rem; margin: 1.75rem 0; }}
    
    /* Mermaid diagram container */
    .mermaid {{ background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 1.5rem; margin: 1.5rem 0; display: flex; justify-content: center; }}
  </style>
</head>
<body class="selection:bg-slate-700 overflow-x-hidden">
  <div class="bg-mesh"></div>
  
  <!-- Global Navigation -->
  <nav class="fixed top-0 z-[100] w-full h-20 border-b border-white/5 bg-obsidian/80 backdrop-blur-md">
    <div class="max-w-7xl mx-auto h-full px-6 md:px-8 flex justify-between items-center">
      <div class="flex items-center gap-12">
        <a href="{rel_root}index.html" class="text-2xl font-bold font-headline tracking-tighter text-white">FunUni-lab<span class="text-secondary text-sm ml-1 opacity-50">.v2</span></a>
        <div class="hidden lg:flex items-center gap-8 text-[11px] font-bold uppercase tracking-widest text-slate-400">
          <a href="{rel_root}infra/index.html" class="hover:text-primary transition-colors {nav_active_infra}">Infrastructure</a>
          <a href="{rel_root}dev/index.html" class="hover:text-secondary transition-colors {nav_active_dev}">Development</a>
          <a href="{rel_root}ai/index.html" class="hover:text-tertiary transition-colors {nav_active_ai}">AI Research</a>
          <a href="{rel_root}finance/index.html" class="hover:text-amber-400 transition-colors {nav_active_finance}">Finance</a>
          <a href="{rel_root}lpo/index.html" class="hover:text-purple-400 transition-colors {nav_active_lpo}">Optimization</a>
          <a href="{rel_root}other/index.html" class="hover:text-emerald-400 transition-colors {nav_active_other}">Strategic Life</a>
          <a href="{rel_root}youtube/index.html" class="hover:text-red-500 transition-colors {nav_active_youtube}">YouTube Lab</a>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 rounded-full bg-surface-container border border-white/10 flex items-center justify-center" style="color: {theme_color};">
          <span class="material-symbols-outlined">{category_icon}</span>
        </div>
      </div>
    </div>
  </nav>

  <main class="pt-32 pb-24 max-w-4xl mx-auto px-6 md:px-8">
    
    <!-- Breadcrumbs -->
    <nav class="mb-8 flex items-center gap-2 text-[11px] font-bold tracking-widest uppercase text-slate-500">
      <a href="{rel_root}index.html" class="hover:text-white transition-colors">Home</a>
      <span class="text-slate-600">/</span>
      <a href="{rel_root}{category}/index.html" class="hover:text-white transition-colors" style="color: {theme_color};">{category_name}</a>
      {sub_breadcrumb}
    </nav>

    <!-- Header Meta -->
    <header class="mb-12">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border text-[10px] font-bold tracking-widest uppercase mb-4" style="background: {theme_color}1a; color: {theme_color}; border-color: {theme_color}33;">
        <span class="material-symbols-outlined text-xs">{category_icon}</span> {badge_label}
      </div>
      <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold font-headline text-white leading-tight mb-6">
        {title}
      </h1>
      <div class="flex flex-wrap items-center gap-6 text-xs text-slate-400 font-mono border-b border-white/5 pb-6">
        <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm" style="color: {theme_color};">calendar_today</span> 公開: {date}</span>
        {updated_badge}
        <span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm" style="color: {theme_color};">schedule</span> 読了目安: 約{reading_time}分</span>
      </div>
    </header>

    <!-- Article Content -->
    <article class="article-body">
      {article_html}
    </article>

  </main>

  <footer class="py-16 border-t border-white/5 bg-obsidian/50 mt-auto">
    <div class="max-w-7xl mx-auto px-6 md:px-8 flex flex-col md:flex-row justify-between items-center gap-8 text-slate-500 font-mono text-[10px] uppercase tracking-widest">
      <div class="flex flex-col gap-2">
        <span>© 2026 FunUni-lab Strategic Archive</span>
        <span class="opacity-40">Direct Static HTML Architecture.</span>
      </div>
      <div class="flex gap-8">
        <a href="{rel_root}index.html" class="hover:text-white">Dashboard</a>
        <a href="{rel_root}{category}/index.html" class="hover:text-white">{category_name}</a>
      </div>
    </div>
  </footer>

  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      }}
    }});
  </script>
</body>
</html>
"""

CATEGORY_ICONS = {
    'infra': 'database',
    'dev': 'terminal',
    'ai': 'smart_toy',
    'finance': 'account_balance_wallet',
    'lpo': 'show_chart',
    'other': 'explore',
    'youtube': 'play_circle',
    'glossary': 'menu_book'
}

def parse_frontmatter(content):
    match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
    if not match:
        return {}, content
    
    fm_text = match.group(1)
    body = content[match.end():].strip()
    
    data = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            parts = line.split(':', 1)
            data[parts[0].strip()] = parts[1].strip().strip('"').strip("'")
    return data, body

def transform_markdown(md_text, rel_root):
    # Fix links
    # Replace article.html?md=xxx with static HTML path
    def replace_sme_link(m):
        raw_target = m.group(1)
        # e.g. md/infra/backup/article.md -> infra/backup/article.html
        target = raw_target.replace('md/', '').replace('.md', '.html')
        return f'{rel_root}{target}'
    
    md_text = re.sub(r'https?://[^/]+/website/article\.html\?md=([^"\')\s#]+)', replace_sme_link, md_text)
    md_text = re.sub(r'/website/article\.html\?md=([^"\')\s#]+)', replace_sme_link, md_text)
    md_text = re.sub(r'article\.html\?md=([^"\')\s#]+)', replace_sme_link, md_text)
    
    # Replace direct .md links to .html
    md_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\.md\)', r'[\1](\2.html)', md_text)

    # Convert using markdown extensions
    md_extensions = ['extra', 'tables', 'fenced_code', 'toc', 'sane_lists']
    html = markdown.markdown(md_text, extensions=md_extensions)
    
    # Wrap tables in table-wrap
    html = re.sub(r'(<table>.*?</table>)', r'<div class="table-wrap">\1</div>', html, flags=re.DOTALL)
    
    # Replace blockquotes with custom callouts
    # Note / Tip / Warning / Caution / Author memo
    def format_blockquote(match):
        bq_content = match.group(1)
        if '[!NOTE]' in bq_content or '著者の鑑賞メモ' in bq_content or '著者の訪問メモ' in bq_content:
            clean = bq_content.replace('[!NOTE]', '').replace('> ', '')
            return f'<div class="callout-note">{clean}</div>'
        elif '[!TIP]' in bq_content:
            clean = bq_content.replace('[!TIP]', '').replace('> ', '')
            return f'<div class="callout-tip">{clean}</div>'
        elif '[!WARNING]' in bq_content or '[!IMPORTANT]' in bq_content:
            clean = bq_content.replace('[!WARNING]', '').replace('[!IMPORTANT]', '').replace('> ', '')
            return f'<div class="callout-warning">{clean}</div>'
        elif '[!CAUTION]' in bq_content:
            clean = bq_content.replace('[!CAUTION]', '').replace('> ', '')
            return f'<div class="callout-caution">{clean}</div>'
        else:
            return f'<div class="callout-note">{bq_content}</div>'

    html = re.sub(r'<blockquote>(.*?)</blockquote>', format_blockquote, html, flags=re.DOTALL)
    
    # Convert mermaid code blocks
    html = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<div class="mermaid">\1</div>', html, flags=re.DOTALL)
    
    return html

def main():
    print("Starting full migration from Markdown to Direct Static HTML...")
    src_root = os.path.join(ROOT_DIR, MD_DIR)
    
    converted_count = 0
    all_articles_index = []
    
    for root, dirs, files in os.walk(src_root):
        for filename in files:
            if filename.endswith('.md'):
                src_path = os.path.join(root, filename)
                rel_path_from_md = os.path.relpath(src_path, src_root).replace('\\', '/')
                
                try:
                    with open(src_path, 'r', encoding='utf-8-sig') as f:
                        raw_content = f.read()
                except Exception:
                    with open(src_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                        raw_content = f.read()
                        
                meta, body = parse_frontmatter(raw_content)
                
                # Determine category and output target
                parts = rel_path_from_md.split('/')
                cat = parts[0] if parts else 'other'
                
                # Destination HTML path in project root
                # e.g. infra/backup/aws-rds-backup.html
                dest_html_rel = rel_path_from_md.replace('.md', '.html')
                dest_html_full = os.path.join(ROOT_DIR, dest_html_rel)
                
                # Create destination directory
                dest_dir = os.path.dirname(dest_html_full)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    
                # Skip if already exists and was custom crafted HTML if needed,
                # but here we ensure all have rich HTML
                depth = dest_html_rel.count('/')
                rel_root = '../' * depth if depth > 0 else './'
                
                cat_info = CATEGORY_THEMES.get(cat, CATEGORY_THEMES['other'])
                theme_color = cat_info['color']
                cat_name = cat_info['name']
                cat_icon = CATEGORY_ICONS.get(cat, 'article')
                
                title = meta.get('title', filename.replace('.md', ''))
                # Strip leading H1 if markdown body starts with it
                body_clean = re.sub(r'^\s*#\s+[^\n]+\n', '', body)
                
                desc = meta.get('description', '')
                if not desc:
                    # extract first paragraph
                    p_match = re.search(r'^(?!#)(.+)$', body_clean, re.MULTILINE)
                    desc = p_match.group(1)[:120] if p_match else 'FunUni-lab Research Log'
                    
                date = meta.get('date', '2026-08-28')
                updated = meta.get('updated', date)
                
                # Calculate reading time (approx 400 chars per min in JP)
                char_count = len(body_clean)
                reading_time = max(1, round(char_count / 400))
                
                # Sub-breadcrumb
                sub_breadcrumb = ''
                if len(parts) > 2:
                    sub_name = parts[1].replace('-', ' ').title()
                    sub_breadcrumb = f'<span class="text-slate-600">/</span><span class="text-slate-400">{sub_name}</span>'
                    
                updated_badge = ''
                if updated and updated != date:
                    updated_badge = f'<span class="flex items-center gap-1.5"><span class="material-symbols-outlined text-sm" style="color: {theme_color};">update</span> 更新: {updated}</span>'
                    
                # Active Nav State
                nav_active = {f'nav_active_{k}': '' for k in CATEGORY_THEMES.keys()}
                nav_active[f'nav_active_{cat}'] = f'text-[{theme_color}] border-b-2 border-[{theme_color}] pb-1'
                
                # Transform body
                body_html = transform_markdown(body_clean, rel_root)
                
                rendered_page = HTML_PAGE_TEMPLATE.format(
                    title=title,
                    description=desc,
                    rel_root=rel_root,
                    theme_color=theme_color,
                    category=cat,
                    category_name=cat_name,
                    category_icon=cat_icon,
                    badge_label=cat_info['badge'],
                    date=date,
                    updated_badge=updated_badge,
                    reading_time=reading_time,
                    sub_breadcrumb=sub_breadcrumb,
                    article_html=body_html,
                    **nav_active
                )
                
                with open(dest_html_full, 'w', encoding='utf-8') as f:
                    f.write(rendered_page)
                    
                all_articles_index.append({
                    "title": title,
                    "description": desc,
                    "date": date,
                    "updated": updated,
                    "category": cat,
                    "path": dest_html_rel,
                    "direct_html": True
                })
                
                converted_count += 1
                if converted_count % 20 == 0:
                    print(f"  Processed {converted_count} articles...")
                    
    # Sort articles
    all_articles_index.sort(key=lambda x: x['date'], reverse=True)
    
    # Save article_index.json
    with open(JSON_OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_articles_index, f, ensure_ascii=False, indent=2)
        
    # Save article-data.js
    js_path = os.path.join(ROOT_DIR, 'assets', 'js', 'article-data.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(f"const window_article_index = {json.dumps(all_articles_index, ensure_ascii=False)};\n")
        
    print(f"\nMigration Complete! Converted {converted_count} Markdown articles to Direct Static HTML.")
    print(f"Updated index at {JSON_OUT_PATH} with {len(all_articles_index)} entries.")

if __name__ == '__main__':
    main()