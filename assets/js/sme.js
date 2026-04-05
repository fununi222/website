/** 
 * Synthetic Content Engine (SME) v1.0.0
 * Dynamically renders Markdown files into the Synthetic Edition shell.
 */

async function loadMarkdown() {
    const contentArea = document.getElementById('sme-content');
    if (!contentArea) return;

    // Support for ?md= param rendering
    const urlParams = new URLSearchParams(window.location.search);
    let mdPath = urlParams.get('md') || contentArea.getAttribute('data-src');

    if (!mdPath) return;

    // Decorate Active UI from mdPath (e.g., ai/xxxx.md)
    decorateActiveUI(mdPath);

    try {
        const response = await fetch(mdPath);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        let mdText = await response.text();

        // 1. Extract Frontmatter (Simple Regex)
        const fmMatch = mdText.match(/^---\s*([\s\S]*?)\s*---\n?/);
        const metadata = {};
        if (fmMatch) {
            const fm = fmMatch[1];
            
            // Basic Key-Value Parsing (YAML-ish)
            fm.split('\n').forEach(line => {
                const parts = line.split(':');
                if (parts.length >= 2) {
                    const key = parts[0].trim();
                    const value = parts.slice(1).join(':').trim().replace(/^["']|["']$/g, '');
                    metadata[key] = value;
                }
            });
            
            // Remove frontmatter from the text to be parsed by Marked
            mdText = mdText.replace(/^---\s*([\s\S]*?)\s*---\n?/, '');
        }

        // 2. Configure Marked.js
        marked.setOptions({
            gfm: true,
            breaks: true,
            headerIds: true,
            mangle: false
        });

        // 3. Parse Markdown
        const rawHtml = marked.parse(mdText);

        // 3.5 Extract Scripts to bypass DOMPurify stripping their contents
        const scripts = [];
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = rawHtml;
        Array.from(tempDiv.querySelectorAll('script')).forEach(scriptEl => {
            scripts.push({
                content: scriptEl.innerHTML,
                attributes: Array.from(scriptEl.attributes)
            });
            scriptEl.parentNode.removeChild(scriptEl);
        });

        // 4. Sanitize the HTML (scripts securely extracted)
        const cleanHtml = DOMPurify.sanitize(tempDiv.innerHTML, { 
            ADD_TAGS: ['canvas', 'button', 'iframe'], 
            ADD_ATTR: ['target', 'data-dataset', 'data-metric', 'id', 'class', 'style', 'width', 'height', 'onclick'] 
        });

        // 5. Inject Content
        contentArea.innerHTML = cleanHtml;

        // 6. Re-inject and Execute Scripts
        scripts.forEach(scriptObj => {
            const newScript = document.createElement('script');
            scriptObj.attributes.forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(scriptObj.content));
            contentArea.appendChild(newScript);
        });

        // Handle dynamic metadata (Title, Category, Date) from frontmatter
        if (metadata.title) document.title = `${metadata.title} | FunUni-lab Synthetic Edition`;
        
        // Trigger library re-initialization (Prism, Mermaid, etc.)
        if (typeof Prism !== 'undefined') {
            Prism.highlightAllUnder(contentArea);
        }
        
        // Mermaid initialization and rendering
        if (typeof mermaid !== 'undefined') {
            // Find all mermaid code blocks and convert them to divs for the engine
            const mermaidBlocks = contentArea.querySelectorAll('code.language-mermaid');
            mermaidBlocks.forEach(block => {
                const pre = block.parentElement;
                const div = document.createElement('div');
                div.className = 'mermaid';
                div.textContent = block.textContent;
                pre.replaceWith(div);
            });
            
            mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'loose' });
            mermaid.run({
                nodes: document.querySelectorAll('.mermaid'),
            });
        }
        
        // Emit Custom Event for and-hoc scripts
        const event = new CustomEvent('sme-loaded', { 
            detail: { metadata, element: contentArea } 
        });
        window.dispatchEvent(event);

    } catch (error) {
        console.error('SME Error:', error);
        contentArea.innerHTML = `<div class="p-8 border border-red-500/20 bg-red-500/10 rounded-2xl text-red-400 text-xs font-mono">
            [FATAL] FAILED TO FETCH DATA STREAM: ${error.message}<br>
            CHECK ORIGIN AND ENDPOINT PATHS.
        </div>`;
    }
}

// Helper to dynamically decorate Sidebar and Navbar based on Category
function decorateActiveUI(mdPath) {
    if (!mdPath) return;
    const category = mdPath.split('/')[0];
    if (!category || category === mdPath) return; // e.g. root items

    // Classes
    const activeNavClass = 'text-secondary border-b-2 border-secondary pb-1'.split(' ');
    const inactiveNavClass = 'text-on-surface-variant hover:text-secondary transition-colors'.split(' ');

    // Patch Nav
    document.querySelectorAll('nav:first-of-type a').forEach(a => {
        if (!a.href) return;
        const hrefSplit = a.href.split('/');
        const hrefCat = hrefSplit[hrefSplit.length - 2]; // either folder or filename
        
        // Ensure "FunUni-lab.js" absolute root doesn't get swept
        if (a.textContent.includes('FunUni-lab.js')) return;

        if (a.href.includes(category + '/index.html')) {
            a.classList.remove(...inactiveNavClass);
            a.classList.add(...activeNavClass);
        } else {
            a.classList.remove(...activeNavClass);
            a.classList.add(...inactiveNavClass);
        }
    });
}

document.addEventListener('DOMContentLoaded', loadMarkdown);
