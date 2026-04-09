import os
import re

def sync_quotes():
    # 1. Update Glossary Data
    glossary_path = 'glossary/system-glossary.md'
    if os.path.exists(glossary_path):
        with open(glossary_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        table_started = False
        for line in lines:
            if '|---|' in line:
                table_started = True
                new_lines.append(line)
                continue
            
            if table_started and line.strip().startswith('|'):
                parts = line.split('|')
                if len(parts) >= 3:
                    term = parts[1].strip().replace('"', '') # Strip existing spaces/quotes
                    parts[1] = f' "{term}" '
                    new_lines.append('|'.join(parts))
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        with open(glossary_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("Updated Glossary Data with quotes.")

    # 2. Update Article Links
    # Regex to catch glossary links with any fragment
    # Matches: ...article.html?md=glossary/system-glossary.md#:~:text=TERM (or variations)
    link_pattern = re.compile(r'(article\.html\?md=glossary/system-glossary\.md)(#\:~\:text=([^ )\]]*))')
    
    cat_dirs = ['ai', 'dev', 'finance', 'infra', 'lpo', 'other']
    for cat in cat_dirs:
        if not os.path.exists(cat): continue
        for file in os.listdir(cat):
            if file.endswith('.md'):
                filepath = os.path.join(cat, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                def link_replacer(match):
                    base_url = match.group(1)
                    raw_text = match.group(3)
                    
                    # Clean the term (remove %22, %20, quotes, pipes, etc)
                    # We want the clean term to wrap it in clean quotes
                    from urllib.parse import unquote
                    term = unquote(raw_text).replace('"', '').replace('|', '').replace('-', '').strip()
                    
                    # Use unencoded raw quotes for the Markdown link
                    return f'{base_url}#:~:text="{term}"'

                new_content = link_pattern.sub(link_replacer, content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Synced Link: {filepath}")

if __name__ == "__main__":
    sync_quotes()
