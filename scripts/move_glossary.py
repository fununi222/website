import os
import re

# 1. Create directory
os.makedirs('glossary', exist_ok=True)

# 2. Update global HTML navigation links from glossary.html to glossary/index.html
def update_nav_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # replace 'href="glossary.html"' -> 'href="glossary/index.html"'
    # replace 'href="../glossary.html"' -> 'href="../glossary/index.html"'
    content = content.replace('href="glossary.html"', 'href="glossary/index.html"')
    content = content.replace('href="../glossary.html"', 'href="../glossary/index.html"')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html') and not f.startswith('tmp_'):
            update_nav_links(os.path.join(root, f))

# 3. Move and rename files
if os.path.exists('glossary.html'):
    os.rename('glossary.html', 'glossary/index.html')
if os.path.exists('glossary.md'):
    os.rename('glossary.md', 'glossary/glossary.md')

# 4. Fix paths inside glossary/index.html now that it's moved
with open('glossary/index.html', 'r', encoding='utf-8') as f:
    g_content = f.read()

# Since it was in root, its assets were 'assets/css/...'. Now it is in 'glossary/', so they become '../assets/'
g_content = g_content.replace('src="assets/js/sme.js"', 'src="../assets/js/sme.js"')
g_content = g_content.replace('href="assets/css/synthetic.css"', 'href="../assets/css/synthetic.css"')
g_content = g_content.replace('src="assets/js/tw-config.js"', 'src="../assets/js/tw-config.js"')
g_content = g_content.replace('data-src="glossary.md"', 'data-src="glossary.md"') # same because markdown is in same dir

with open('glossary/index.html', 'w', encoding='utf-8') as f:
    f.write(g_content)
print('Moved glossary and updated links')
