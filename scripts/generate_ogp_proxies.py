import os
import re
import sys
import json

ROOT_DIR = '.'
JSON_OUT_PATH = 'assets/data/article_index.json'
CATEGORIES = ['infra', 'dev', 'ai', 'finance', 'other', 'lpo', 'youtube', 'glossary']

def parse_html_metadata(html_content, file_path):
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
    date_match = re.search(r'公開:\s*(\d{4}-\d{2}-\d{2})', html_content)
    if not date_match:
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html_content)
    if date_match:
        meta['date'] = date_match.group(1)
        
    # Updated date
    up_match = re.search(r'更新:\s*(\d{4}-\d{2}-\d{2})', html_content)
    if up_match:
        meta['updated'] = up_match.group(1)
    else:
        meta['updated'] = meta.get('date', '2026-08-28')
        
    return meta

def main():
    print("Building Article Index from Direct Static HTML articles...")
    articles_index = []
    seen_paths = set()

    for cat in CATEGORIES:
        cat_dir = os.path.join(ROOT_DIR, cat)
        if not os.path.exists(cat_dir):
            continue
        for root, dirs, files in os.walk(cat_dir):
            for filename in files:
                if filename.endswith('.html') and filename != 'index.html':
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, ROOT_DIR).replace('\\', '/')
                    
                    if rel_path in seen_paths:
                        continue
                    seen_paths.add(rel_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8-sig') as f:
                            content = f.read()
                    except Exception:
                        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                            content = f.read()
                    
                    meta = parse_html_metadata(content, rel_path)
                    title = meta.get('title', filename.replace('.html', ''))
                    desc = meta.get('description', 'FunUni-lab Research Log')
                    date = meta.get('date', '2026-08-28')
                    updated = meta.get('updated', date)
                    
                    articles_index.append({
                        "title": title,
                        "description": desc,
                        "date": date,
                        "updated": updated,
                        "category": cat,
                        "path": rel_path,
                        "direct_html": True
                    })
                    print(f"  [INDEXED] {rel_path}")

    # Sort articles by date descending
    articles_index.sort(key=lambda x: x['date'], reverse=True)
    
    # Write JSON index
    json_path = os.path.join(ROOT_DIR, JSON_OUT_PATH)
    json_dir = os.path.dirname(json_path)
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles_index, f, ensure_ascii=False, indent=2)
    print(f"  [SAVED] {JSON_OUT_PATH} with {len(articles_index)} entries.")

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
        print(f"  [SAVED] assets/js/skill-data.js with {len(scores)} skills.")

    # Generate article data for offline/local view
    if articles_index:
        js_dir = os.path.join(ROOT_DIR, 'assets', 'js')
        js_article_path = os.path.join(js_dir, 'article-data.js')
        with open(js_article_path, 'w', encoding='utf-8') as f:
            f.write(f"const window_article_index = {json.dumps(articles_index, ensure_ascii=False)};\n")
        print(f"  [SAVED] assets/js/article-data.js with {len(articles_index)} entries.")

    print(f"\nDone! Successfully indexed {len(articles_index)} direct static HTML articles.")

if __name__ == "__main__":
    main()