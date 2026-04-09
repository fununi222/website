import os
import re

def final_audit():
    # Matches glossary links that do NOT have a double quote immediately after text=
    pattern = re.compile(r'glossary/system-glossary\.md#\:~\:text=(?!\")')
    
    found_any = False
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if pattern.search(content):
                        print(f"UNQUOTED LINK FOUND: {filepath}")
                        found_any = True
                except:
                    pass
    
    if not found_any:
        print("ALL LINKS VERIFIED: 100% QUOTED")

if __name__ == "__main__":
    final_audit()
