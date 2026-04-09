import os
import re

def add_space_to_glossary():
    filepath = 'glossary/system-glossary.md'
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    # Table rows start with |
    # We want to target lines like | Term | Category | Desc |
    # But skip headers and separators
    
    table_started = False
    for line in lines:
        if '|---|' in line:
            table_started = True
            new_lines.append(line)
            continue
        
        if table_started and line.startswith('|') and '|' in line[1:]:
            # Split the row by |
            parts = line.split('|')
            if len(parts) >= 3:
                # parts[0] is empty (before first |)
                # parts[1] is the Term
                term = parts[1]
                # If term doesn't already end with a space, add it
                # Note: we add a space BEFORE the closing | of that cell
                if not term.endswith(' '):
                    parts[1] = term + ' '
                
                new_line = '|'.join(parts)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Added spaces to glossary terms.")

if __name__ == "__main__":
    add_space_to_glossary()
