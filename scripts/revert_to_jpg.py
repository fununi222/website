import os
import re
from PIL import Image

IMG_DIR = 'assets/img'

def convert_webp_to_jpg():
    for f in os.listdir(IMG_DIR):
        if f.endswith('.webp'):
            base_name = os.path.splitext(f)[0]
            # Skip mascot icons if they were converted (they shouldn't have been)
            if base_name.startswith(('mascot-', 'pet-bg-')):
                continue
                
            input_path = os.path.join(IMG_DIR, f)
            output_path = os.path.join(IMG_DIR, f"{base_name}.jpg")
            
            try:
                with Image.open(input_path) as img:
                    img = img.convert('RGB')
                    img.save(output_path, 'JPEG', quality=90)
                print(f"Converted {f} -> {base_name}.jpg")
                os.remove(input_path)
            except Exception as e:
                print(f"Error converting {f}: {e}")

def update_refs():
    pattern = re.compile(r'assets/img/([a-zA-Z0-9_-]+)\.webp')
    
    for root, dirs, files in os.walk('.'):
        if '.openclaw' in root or '.git' in root or 'scripts' in root:
            continue
            
        for f in files:
            if f.endswith(('.md', '.html')):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = pattern.sub(r'assets/img/\1.jpg', content)
                
                if content != new_content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Updated references in {filepath}")

if __name__ == "__main__":
    convert_webp_to_jpg()
    update_refs()
    print("Reverted to JPG and updated references.")
