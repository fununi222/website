import os
import re
import sys
import json

# Configuration
ROOT_DIR = '.'
SOURCE_DIR = 'md'  # Markdown sources
OUTPUT_DIR = 'html' # Dedicated folder for HTML articles
JSON_OUT_PATH = 'assets/data/article_index.json' # Global JSON index
CATEGORIES = ['infra', 'dev', 'ai', 'finance', 'other', 'lpo', 'youtube']

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO & OGP -->
    <title>{title} | FunUni-lab</title>
    <meta name="description" content="{description}" />
    <meta property="og:title" content="{title} | FunUni-lab" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="https://fununi222.github.io/website/html/{md_path_html}" />
    <meta property="og:site_name" content="FunUni-lab" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title} | FunUni-lab" />
    <meta name="twitter:description" content="{description}" />
    <link rel="canonical" href="https://fununi222.github.io/website/html/{md_path_html}" />
    <meta http-equiv="refresh" content="0;url={rel_root}article.html?md=md/{md_path}">

    <!-- Redirect to the dynamic viewer -->
    <script>
        window.location.href = '{rel_root}article.html?md=md/{md_path}';
    </script>
    
    <style>
        body {{ background: #0f172a; color: #a3aac4; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
        .loading {{ text-align: center; }}
        .spinner {{ border: 2px solid rgba(255,255,255,0.1); border-left-color: #aaa4ff; border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; margin: 0 auto 10px; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="loading">
        <div class="spinner"></div>
        <p>Redirecting to Research Log...</p>
    </div>
</body>
</html>
"""

def parse_frontmatter(content):
    match = re.search(r'^---\s*(.*?)\s*---', content, re.DOTALL)
    if not match:
        return {}
    
    data = {}
    fm_text = match.group(1)
    for line in fm_text.split('\n'):
        if ':' in line:
            parts = line.split(':', 1)
            data[parts[0].strip()] = parts[1].strip().strip('"').strip("'")
    return data

def parse_html_metadata(html_content):
    """Extract metadata from direct HTML article"""
    meta = {}
    
    # Title
    t_match = re.search(r'<title>(.*?)(?:\|.*?)?</title>', html_content, re.IGNORECASE)
    if t_match:
        meta['title'] = t_match.group(1).strip()
    
    # Description
    d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE)
    if not d_match:
        d_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html_content, re.IGNORECASE)
    if d_match:
        meta['description'] = d_match.group(1).strip()
        
    # Date (e.g. 2026-08-28)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html_content)
    if date_match:
        meta['date'] = date_match.group(1)
        
    return meta

def main():
    print(f"Generating Article Index and OGP Proxy Files...")
    count = 0
    articles_index = []
    seen_titles = set()

    # 1. Process direct HTML articles in category directories
    for cat in CATEGORIES:
        cat_dir = os.path.join(ROOT_DIR, cat)
        if not os.path.exists(cat_dir):
            continue
        for root, dirs, files in os.walk(cat_dir):
            for filename in files:
                if filename.endswith('.html') and filename != 'index.html':
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, ROOT_DIR).replace('\\', '/')
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8-sig') as f:
                            content = f.read()
                    except Exception:
                        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                            content = f.read()
                    
                    meta = parse_html_metadata(content)
                    title = meta.get('title', filename.replace('.html', ''))
                    desc = meta.get('description', 'FunUni-lab Direct HTML Log')
                    date = meta.get('date', '2026-08-28')
                    
                    articles_index.append({
                        "title": title,
                        "description": desc,
                        "date": date,
                        "updated": date,
                        "category": cat,
                        "path": rel_path,
                        "direct_html": True
                    })
                    seen_titles.add(title)
                    print(f"  [DIRECT HTML] {rel_path}")

    # 2. Process Markdown sources in 'md/'
    src_root = os.path.join(ROOT_DIR, SOURCE_DIR)
    if os.path.exists(src_root):
        for root, dirs, files in os.walk(src_root):
            for filename in files:
                if filename.endswith('.md'):
                    src_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(src_path, src_root).replace('\\', '/')
                    
                    try:
                        with open(src_path, 'r', encoding='utf-8-sig') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        with open(src_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                            content = f.read()
                    
                    metadata = parse_frontmatter(content)
                    title = metadata.get('title', 'Technical Archive')
                    description = metadata.get('description', 'FunUni-lab Research Log')
                    
                    html_rel_path = rel_path.replace('.md', '.html')
                    out_path = os.path.join(ROOT_DIR, OUTPUT_DIR, html_rel_path)
                    
                    out_dir = os.path.dirname(out_path)
                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)
                    
                    depth = html_rel_path.count('/')
                    rel_root = '../' * (depth + 1)
                    
                    output = TEMPLATE.format(
                        title=title,
                        description=description,
                        md_path=rel_path,
                        md_path_html=html_rel_path,
                        rel_root=rel_root
                    )
                    
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(output)
                    
                    # If not already added as direct HTML, add to index
                    if title not in seen_titles:
                        articles_index.append({
                            "title": title,
                            "description": description,
                            "date": metadata.get('date', '1970-01-01'),
                            "updated": metadata.get('updated', metadata.get('date', '2026-08-02')),
                            "category": rel_path.split('/')[0] if '/' in rel_path else 'other',
                            "path": html_rel_path,
                            "direct_html": False
                        })
                        seen_titles.add(title)
                    
                    count += 1

    # Sort articles by date descending
    articles_index.sort(key=lambda x: x['date'], reverse=True)
    
    # Write JSON index
    json_path = os.path.join(ROOT_DIR, JSON_OUT_PATH)
    json_dir = os.path.dirname(json_path)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles_index, f, ensure_ascii=False, indent=2)
    print(f"  [CREATED] {JSON_OUT_PATH} with {len(articles_index)} entries.")

    # Generate skill data for offline/local view without CORS
    skill_md_path = os.path.join(ROOT_DIR, 'SKILL.md')
    if os.path.exists(skill_md_path):
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            skill_content = f.read()
            
        scores = {}
        matches = re.findall(r'- \*\*([^:*]+)\*\*: (\d+)', skill_content)
        for key, val in matches:
            clean_key = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', key).strip()
            scores[clean_key] = int(val)
            
        js_dir = os.path.join(ROOT_DIR, 'assets', 'js')
        if not os.path.exists(js_dir):
            os.makedirs(js_dir)
            
        js_out_path = os.path.join(js_dir, 'skill-data.js')
        with open(js_out_path, 'w', encoding='utf-8') as f:
            f.write(f"const window_skill_data = {json.dumps(scores, ensure_ascii=False)};\n")
        print(f"  [CREATED] assets/js/skill-data.js with {len(scores)} skills.")

    # Generate article data for offline/local view
    if articles_index:
        js_dir = os.path.join(ROOT_DIR, 'assets', 'js')
        js_article_path = os.path.join(js_dir, 'article-data.js')
        with open(js_article_path, 'w', encoding='utf-8') as f:
            f.write(f"const window_article_index = {json.dumps(articles_index, ensure_ascii=False)};\n")
        print(f"  [CREATED] assets/js/article-data.js with {len(articles_index)} entries.")

    print(f"\nDone! Processed {len(articles_index)} total articles.")

if __name__ == "__main__":
    main()