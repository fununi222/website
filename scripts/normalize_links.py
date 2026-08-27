import os
import re

ROOT_DIR = '.'

def fix_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Determine depth relative to root
    rel_path = os.path.relpath(file_path, ROOT_DIR).replace('\\', '/')
    depth = rel_path.count('/')
    rel_root = '../' * depth if depth > 0 else ''
    
    # Replace absolute fununi222 github links to local relative links
    # https://fununi222.github.io/website/html/glossary/system-glossary.html -> {rel_root}glossary/system-glossary.html
    # https://fununi222.github.io/website/article.html?md=glossary/system-glossary.md -> {rel_root}glossary/system-glossary.html
    new_content = re.sub(
        r'https?://fununi222\.github\.io/website/(?:html/)?glossary/system-glossary\.html',
        f'{rel_root}glossary/system-glossary.html',
        content
    )
    new_content = re.sub(
        r'https?://fununi222\.github\.io/website/article\.html\?md=glossary/system-glossary\.md',
        f'{rel_root}glossary/system-glossary.html',
        new_content
    )
    new_content = re.sub(
        r'/website/article\.html\?md=glossary/system-glossary\.md',
        f'{rel_root}glossary/system-glossary.html',
        new_content
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [FIXED LINKS] {rel_path}")

def main():
    print("Normalizing all internal links...")
    for root, dirs, files in os.walk(ROOT_DIR):
        if '.git' in root or 'node_modules' in root or '.agents' in root:
            continue
        for filename in files:
            if filename.endswith('.html') or filename.endswith('.js'):
                file_path = os.path.join(root, filename)
                fix_links_in_file(file_path)

if __name__ == '__main__':
    main()