import os
import re
import sys
import json

# Configuration
ROOT_DIR = '.'
SOURCE_DIR = 'md'  # Markdown sources
OUTPUT_DIR = 'html' # Dedicated folder for HTML articles
JSON_OUT_PATH = 'assets/data/article_index.json' # Global JSON index
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

def main():
    print(f"Generating OGP Proxy Files in {OUTPUT_DIR}/ recursively...")
    count = 0
    
    src_root = os.path.join(ROOT_DIR, SOURCE_DIR)
    
    if not os.path.exists(src_root):
        print(f"Error: {SOURCE_DIR} directory not found.")
        return

    articles_index = []

    for root, dirs, files in os.walk(src_root):
        for filename in files:
            if filename.endswith('.md'):
                # Full path to source file
                src_path = os.path.join(root, filename)
                
                # Relative path from 'md/' directory (e.g. 'infra/backup/article.md')
                rel_path = os.path.relpath(src_path, src_root).replace('\\', '/')
                
                # Metadata extraction
                with open(src_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata = parse_frontmatter(content)
                title = metadata.get('title', 'Technical Archive')
                description = metadata.get('description', 'FunUni-lab Research Log')
                
                # Determine output path in 'html/'
                # e.g. html/infra/backup/article.html
                html_rel_path = rel_path.replace('.md', '.html')
                out_path = os.path.join(ROOT_DIR, OUTPUT_DIR, html_rel_path)
                
                # Ensure output directory exists
                out_dir = os.path.dirname(out_path)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                
                # Calculate relative path to root for 'article.html' redirect
                # Depth is the number of slashes in html_rel_path
                # e.g. 'infra/backup/article.html' -> depth 2 -> '../../'
                depth = html_rel_path.count('/')
                rel_root = '../' * (depth + 1)
                
                # Render template
                output = TEMPLATE.format(
                    title=title,
                    description=description,
                    md_path=rel_path,
                    md_path_html=html_rel_path,
                    rel_root=rel_root
                )
                
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(output)
                
                # Append to JSON index
                articles_index.append({
                    "title": title,
                    "description": description,
                    "date": metadata.get('date', '1970-01-01'),
                    "category": rel_path.split('/')[0] if '/' in rel_path else 'other',
                    "path": html_rel_path
                })
                
                print(f"  [CREATED] {OUTPUT_DIR}/{html_rel_path}")
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

    print(f"\nDone! Generated {count} proxy files and 1 JSON index.")

if __name__ == "__main__":
    main()
