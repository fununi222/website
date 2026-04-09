import os
import re
from urllib.parse import quote

def encode_glossary_links():
    pattern = re.compile(r'(article\.html\?md=glossary/system-glossary\.md#:~:text=)([^)\s"\'>]+)')
    
    # Target all markdown and html files
    for root, dirs, files in os.walk('.'):
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith(('.md', '.html')):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all matches
                # Note: We only encode if the fragment contains non-ASCII characters
                def replace_func(match):
                    base = match.group(1)
                    fragment = match.group(2)
                    
                    # If it's already encoded (starts with %), keep it as is
                    if '%' in fragment:
                        return match.group(0)
                    
                    # Encode if it contains Japanese characters
                    try:
                        fragment.encode('ascii')
                        return match.group(0) # ASCII only, no change
                    except UnicodeEncodeError:
                        encoded_fragment = quote(fragment)
                        print(f"Encoding '{fragment}' to '{encoded_fragment}' in {filepath}")
                        return f"{base}{encoded_fragment}"
                
                new_content = pattern.sub(replace_func, content)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {filepath}")

if __name__ == "__main__":
    encode_glossary_links()
