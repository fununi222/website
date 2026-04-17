import os
import re

CATEGORIES = ['infra', 'dev', 'ai', 'finance', 'lpo', 'other']
BASE_DIR = r'c:\Users\fumiy\.openclaw\workspace\website'
ABSOLUTE_URL_BASE = 'https://fununi222.github.io/website/'

def process_file(filepath):
    is_markdown = filepath.endswith('.md')
    is_html = filepath.endswith('.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Global Branding Replacements
    content = content.replace('Synthetic Edition', 'Technical Archive')
    content = content.replace('FunUni-lab.js', 'FunUni-lab')
    content = content.replace('Synthetic_Research_Feed', 'Latest_Research_Feed')
    content = content.replace('SYNTHETIC_NODE', 'TECHNICAL_ARCHIVE')
    content = content.replace('SYNTHETIC_EDITION', 'TECHNICAL_ARCHIVE')

    # 2. Markdown-specific structural changes
    if is_markdown:
        # Layout standardizations (my-10 -> mb-10)
        content = content.replace('my-10 max-w-4xl mx-auto cyber-glow', 'mb-10 max-w-4xl mx-auto cyber-glow')

        # Move figure to top and remove ## 超要約
        figure_pattern = re.compile(r'(<figure class=".*?>[\s\S]*?</figure>)', re.MULTILINE)
        figure_match = figure_pattern.search(content)
        
        summary_pattern = re.compile(r'^## 超要約\s*$', re.MULTILINE)
        
        if figure_match:
            figure_block = figure_match.group(1)
            content = content.replace(figure_block, '')
            content = summary_pattern.sub('', content)
            
            # Insert at the top
            header_pattern = re.compile(r'(Research Log: v.*?\n\n|# .*?\n\n)', re.MULTILINE)
            header_match = header_pattern.search(content)
            if header_match:
                insert_pos = header_match.end()
                content = content[:insert_pos] + figure_block + '\n\n' + content[insert_pos:]

    # 3. Link Normalization (Fixed Regex to avoid double prefixing)
    # This regex looks for article.html?md=... but NOT preceded by ABSOLUTE_URL_BASE
    # Also handles both markdown links [text](path) and HTML href="path"
    
    # First, handle already absolute links (do nothing)
    # Then handle relative links (../article.html... or article.html...)
    
    # Pattern to find links that should be absolute but aren't
    # Matches: (../)article.html?md=xxx
    # Does NOT match: https://...article.html?md=xxx
    rel_link_pattern = re.compile(r'(?<!https://fununi222\.github\.io/website/)(\.\.\/)?article\.html\?md=([a-zA-Z0-9_\-\.\/]+)(#:[~a-zA-Z0-9%\.\"\=_\-]*)?')
    
    def normalize_link(match):
        rel_prefix = match.group(1) # ../ or None
        md_path = match.group(2)
        fragment = match.group(3) or ''
        return f"{ABSOLUTE_URL_BASE}article.html?md={md_path}{fragment}"

    content = rel_link_pattern.sub(normalize_link, content)

    # 4. Clean up any accidental double prefixes from previous run
    content = content.replace(ABSOLUTE_URL_BASE + ABSOLUTE_URL_BASE, ABSOLUTE_URL_BASE)

    # 5. Whitespace cleanup
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    modified_count = 0
    # Walk through the whole website directory
    for root, dirs, files in os.walk(BASE_DIR):
        for filename in files:
            if filename.endswith(('.md', '.html')):
                filepath = os.path.join(root, filename)
                try:
                    process_file(filepath)
                    modified_count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"Successfully brushed up {modified_count} files (MD & HTML).")

if __name__ == '__main__':
    main()
