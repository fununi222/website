import os
import re

# Regex to match the old article links
# 1. Matches dynamic links: article.html?md=category/name.md
# 2. Matches previous static links: category/name.html (WITHOUT the html/ prefix)
# Group 1: Optional base URL
# Group 2: Category
# Group 3: Basename
# Group 4: Extension (.md or .html)
LINK_RE = re.compile(r'(https://fununi222\.github\.io/website/)?(?:article\.html\?md=)?(?!(?:md/|html/|assets/|index\.html|article\.html|404\.html))([a-z]+)/([a-zA-Z0-9_-]+)\.(md|html)')

def get_target_files():
    targets = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            # Exclude source MD files (which are in md/) and system files
            if file.endswith('.html') and not file.endswith('google63a1e682d08df09d.html') and 'md' not in root.split(os.sep):
                targets.append(os.path.join(root, file))
    return targets

def migrate_links():
    print("Migrating links to html/ directory in all HTML files...")
    target_files = get_target_files()
    
    for path in target_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Internal replacement
        # \1: URL (optional), \2: Category, \3: Basename, \4: ext
        def link_replacer(match):
            base = match.group(1) if match.group(1) else ""
            return f"{base}html/{match.group(2)}/{match.group(3)}.html"

        new_content = LINK_RE.sub(link_replacer, content)
        
        if content != new_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [UPDATED] {path}")

if __name__ == "__main__":
    migrate_links()
