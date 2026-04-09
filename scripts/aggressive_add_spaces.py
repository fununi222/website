import os

def aggressive_add_spaces():
    filepath = 'glossary/system-glossary.md'
    if not os.path.exists(filepath):
        print("File not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
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
                # Force " Term  " format
                term = parts[1].strip()
                if term:
                    # One leading space, Two trailing spaces
                    parts[1] = f" {term}  "
                    new_line = '|'.join(parts)
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Forced double spaces onto glossary terms.")

if __name__ == "__main__":
    aggressive_add_spaces()
