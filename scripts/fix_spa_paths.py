import os

def fix_spa_paths():
    # 1. Update Markdown files in categories
    target_str = '../article.html?md='
    replacement_str = 'article.html?md='
    cat_dirs = ['ai', 'dev', 'finance', 'infra', 'lpo', 'other', 'glossary']
    
    for cat in cat_dirs:
        if not os.path.exists(cat):
            continue
        for file in os.listdir(cat):
            if file.endswith('.md'):
                filepath = os.path.join(cat, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content.replace(target_str, replacement_str)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed MD: {filepath}")

    # 2. Re-verify index.html
    # (Just in case something weird happened there)
    index_path = 'index.html'
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure it doesn't have / or ../
        new_content = content.replace('"/article.html?', '"article.html?')
        new_content = new_content.replace('"../article.html?', '"article.html?')
        
        if new_content != content:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed HTML: {index_path}")

if __name__ == "__main__":
    fix_spa_paths()
