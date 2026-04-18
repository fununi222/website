import os
import re

# Categories for matching
CATS = ['ai', 'dev', 'finance', 'infra', 'lpo', 'other', 'glossary']
CAT_PATTERN = '|'.join(CATS)

# 1. Regex to match links that need prefixing
# Matches: cat/name.md, cat/name.html
# Excludes: html/cat/..., md/cat/..., cat/index.html
# Uses negative lookbehind to ensure no html/ or md/ prefix
# Uses negative lookahead to ensure not index.html
LINK_RE = re.compile(rf'(?<!html/)(?<!md/)\b({CAT_PATTERN})/((?!index)[a-zA-Z0-9_-]+)\.(md|html)')

# 2. Regex to clean up any leftover duplications (just in case)
CLEANUP_RE = re.compile(r'html/html/')

def get_target_files():
    targets = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html') and not file.endswith('google63a1e682d08df09d.html') and 'md' not in root.split(os.sep):
                targets.append(os.path.join(root, file))
    return targets

def migrate_links():
    print("Executing Idempotent Link Migration...")
    target_files = get_target_files()
    
    for path in target_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # First: Clean up any duplications
        content = CLEANUP_RE.sub('html/', content)
        
        # Second: Prefix valid article links
        # \1: Category, \2: Basename, \3: Extension
        def link_replacer(match):
            return f"html/{match.group(1)}/{match.group(2)}.html"

        new_content = LINK_RE.sub(link_replacer, content)
        
        if content != new_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [FIXED] {path}")

if __name__ == "__main__":
    migrate_links()
