import os
from PIL import Image

IMG_DIR = 'assets/img'
MAX_WIDTH = 1200
QUALITY = 75

def compress_jpg(filename):
    if not filename.lower().endswith(('.jpg', '.jpeg')):
        return
        
    filepath = os.path.join(IMG_DIR, filename)
    
    try:
        with Image.open(filepath) as img:
            # 1. Resize if too large
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / float(img.width)
                new_h = int(float(img.height) * ratio)
                img = img.resize((MAX_WIDTH, new_h), Image.Resampling.LANCZOS)
                print(f"Resized {filename}")
            
            # 2. Compress and save
            img.save(filepath, 'JPEG', quality=QUALITY, optimize=True)
            print(f"Compressed {filename} (quality={QUALITY})")
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    files = [f for f in os.listdir(IMG_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
    for f in files:
        compress_jpg(f)
    print("Optimization Complete.")
