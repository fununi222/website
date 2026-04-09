import os
import re
from urllib.parse import unquote

def robust_sync():
    # Regex designed to capture the entire fragment inside the Markdown link parentheses
    # Matches: [...](article.html?md=glossary/system-glossary.md#:~:text=ANYTHING)
    # We capture EVERYTHING from #:~:text= until the first )
    pattern = re.compile(r'(\?md=glossary/system-glossary\.md#\:~\:text=)([^)]+)(\))')
    
    cat_dirs = ['ai', 'dev', 'finance', 'infra', 'lpo', 'other']
    for cat in cat_dirs:
        if not os.path.exists(cat): continue
        for file in os.listdir(cat):
            if file.endswith('.md'):
                filepath = os.path.join(cat, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                def replacer(match):
                    prefix = match.group(1)
                    raw_val = match.group(2)
                    suffix = match.group(3)
                    
                    # Clean the value (remove existing quotes, spaces, etc)
                    clean_val = unquote(raw_val).replace('"', '').replace('|', '').strip()
                    
                    # Return with raw quotes
                    return f'{prefix}"{clean_val}"{suffix}'

                new_content = pattern.sub(replacer, content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    robust_sync()
