import os
import re

def fix_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the broken links
    # Matches: https://fununi222.github.io/websi../../article.html?md=category/name.md#:~:text="Text"
    # Capture Group 1: category/name
    # Capture Group 2: fragments like #:~:text="..."
    pattern = r'https://fununi222\.github\.io/websi\.\./\.\./article\.html\?md=([^&\s\)]+)\.md([^&\s\)]*)'
    
    def replace_link(match):
        md_path = match.group(1)
        fragment = match.group(2)
        # Convert md/category/name to html/category/name.html
        # Note: some paths might already start with md/
        clean_path = md_path.replace('md/', '', 1) if md_path.startsWith('md/') else md_path
        return f'https://fununi222.github.io/website/html/{clean_path}.html{fragment}'

    # Alternative pattern for simpler relative links if any
    # [Text](../../article.html?md=category/name.md)
    pattern_rel = r'\]\(\.\./\.\./article\.html\?md=([^&\s\)]+)\.md([^&\s\)]*)'
    
    def replace_rel_link(match):
        md_path = match.group(1)
        fragment = match.group(2)
        clean_path = md_path.replace('md/', '', 1) if md_path.startswith('md/') else md_path
        # Use absolute path to be safe, or relative to root
        return f'](html/{clean_path}.html{fragment})'

    new_content = re.sub(pattern, lambda m: f'https://fununi222.github.io/website/html/{m.group(1).replace("md/", "", 1) if m.group(1).startswith("md/") else m.group(1)}.html{m.group(2)}', content)
    new_content = re.sub(pattern_rel, replace_rel_link, new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(scripts_dir)
    md_dir = os.path.join(workspace_dir, 'md')
    count = 0
    for root, dirs, files in os.walk(md_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                if fix_links_in_file(full_path):
                    print(f"Fixed: {full_path}")
                    count += 1
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    main()
