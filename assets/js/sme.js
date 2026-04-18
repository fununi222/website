/** 
 * Static Metadata Engine (SME) v1.0.0
 * Dynamically renders Markdown files into the Technical Archive shell.
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

        // 3.5 Extract Scripts, Styles, and SVGs to bypass DOMPurify stripping their contents
        const extractedElements = [];
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = rawHtml;
        
        Array.from(tempDiv.querySelectorAll('script, style, svg')).forEach(el => {
            extractedElements.push({
                tagName: el.tagName.toLowerCase(),
                content: el.innerHTML,
                attributes: Array.from(el.attributes)
            });
            el.parentNode.removeChild(el);
        });

        // 4. Resolve Relative Paths for Assets (Images, Links, Styles)
        resolveRelativePaths(tempDiv, mdPath);

        // 5. Sanitize the HTML (scripts/styles securely extracted)
        const cleanHtml = DOMPurify.sanitize(tempDiv.innerHTML, { 
            ADD_TAGS: ['canvas', 'button', 'iframe'], 
            ADD_ATTR: ['target', 'data-dataset', 'data-metric', 'id', 'class', 'style', 'width', 'height', 'onclick'] 
        });

        // 6. Inject Content
        contentArea.innerHTML = cleanHtml;


        // 7. Re-inject and Execute Scripts/Styles (Resolve paths inside scripts/styles too)
        extractedElements.forEach(item => {
            const newEl = document.createElement(item.tagName);
            item.attributes.forEach(attr => newEl.setAttribute(attr.name, attr.value));
            
            let content = item.content;
            if (item.tagName === 'style' || item.tagName === 'script') {
                content = resolveStringPaths(content, mdPath);
            }
            
            newEl.appendChild(document.createTextNode(content));
            contentArea.appendChild(newEl);
        });



        // Handle dynamic metadata (Title, Category, Date) from frontmatter
        if (metadata.title) document.title = `${metadata.title} | FunUni-lab Technical Archive`;
        
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

        // 7. Handle Scroll to Text Fragment (for Cloud latency issues)
        handleTextFragments();

        // 8. Initialize Lightbox for all images
        initLightbox();

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
        
        // Ensure "FunUni-lab" absolute root doesn't get swept
        if (a.textContent.includes('FunUni-lab')) return;

        if (a.href.includes(category + '/index.html')) {
            a.classList.remove(...inactiveNavClass);
            a.classList.add(...activeNavClass);
        } else {
            a.classList.remove(...activeNavClass);
            a.classList.add(...inactiveNavClass);
        }
    });
}

// Handle Scroll to Text Fragments (#:~:text=...) in a dynamic SPA context
function handleTextFragments() {
    const hash = window.location.hash;
    if (!hash || !hash.includes(':~:text=')) return;

    // Small delay to ensure browser rendering and library (Prism/Mermaid) stabilization
    setTimeout(() => {
        const textParam = hash.split(':~:text=')[1];
        if (!textParam) return;
        
        const decodedText = decodeURIComponent(textParam);
        const contentArea = document.getElementById('sme-content');

        // Strategy A: Try Native window.find (if available)
        // This is non-standard but Chrome/Edge support it well for simple text
        if (typeof window.find === 'function') {
            const found = window.find(decodedText, false, false, true, false, true, false);
            if (found) {
                // Flash the container
                if (window.getSelection().rangeCount > 0) {
                    const range = window.getSelection().getRangeAt(0);
                    const parent = range.commonAncestorContainer.parentElement;
                    parent.classList.add('sme-highlight-target');
                }
                return;
            }
        }

        // Strategy B: Fallback DOM Walk with Smart Priority
        const walker = document.createTreeWalker(contentArea, NodeFilter.SHOW_TEXT, null, false);
        let node;
        let firstSubstringMatch = null;

        while (node = walker.nextNode()) {
            const text = node.textContent;

            // 1. Priority: Exact Match (Matches cell content exactly)
            // This handles the "Trailing Space Trick" e.g. "LLM " matches exactly "LLM " cell
            if (text.trim() === decodedText.trim() && text.includes(decodedText)) {
                targetElement = node.parentElement;
                break; // Found perfect match, exit loop
            }

            // 2. Secondary: First Substring Match (Fallback)
            if (!firstSubstringMatch && text.includes(decodedText)) {
                firstSubstringMatch = node.parentElement;
            }
        }

        const finalTarget = targetElement || firstSubstringMatch;
        if (finalTarget) {
            finalTarget.scrollIntoView({ behavior: 'smooth', block: 'center' });
            finalTarget.classList.add('sme-highlight-target');
        }
    }, 200); 
}

// Synthetic Lightbox: Unified Image Magnification System
function initLightbox() {
    let lightbox = document.querySelector('.sme-lightbox');
    
    // Create lightbox if it doesn't exist
    if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.className = 'sme-lightbox';
        lightbox.innerHTML = `
            <span class="sme-lightbox-close material-symbols-outlined">close</span>
            <img src="" alt="Lightbox Image">
        `;
        document.body.appendChild(lightbox);

        // Close on click (anywhere on the overlay/image)
        lightbox.addEventListener('click', () => {
            lightbox.classList.remove('active');
        });

        // Close on Esc key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && lightbox.classList.contains('active')) {
                lightbox.classList.remove('active');
            }
        });
    }

    const contentArea = document.getElementById('sme-content');
    const lightboxImg = lightbox.querySelector('img');

    // Use event delegation on the content area for high performance
    contentArea.removeEventListener('click', handleImageClick); // Clear previous if any
    contentArea.addEventListener('click', handleImageClick);

    function handleImageClick(e) {
        const target = e.target;
        if (target.tagName === 'IMG' && !target.closest('a')) {
            e.preventDefault();
            lightboxImg.src = target.src;
            lightboxImg.alt = target.alt || 'Magnified View';
            lightbox.classList.add('active');
        }
    }
}

document.addEventListener('DOMContentLoaded', loadMarkdown);

/**
 * Resolves relative paths in the rendered HTML fragments against the Markdown source path.
 */
function resolveRelativePaths(container, mdPath) {
    if (!mdPath) return;

    // 1. Fix Images and Links
    const elements = container.querySelectorAll('img[src], a[href], source[src], video[src]');
    elements.forEach(el => {
        const attr = el.tagName === 'A' ? 'href' : 'src';
        const val = el.getAttribute(attr);
        
        // Only resolve internal relative paths
        if (val && !val.startsWith('http') && !val.startsWith('/') && !val.startsWith('#') && !val.startsWith('mailto:') && !val.startsWith('tel:')) {
            el.setAttribute(attr, resolvePath(val, mdPath));
        }
    });

    // 2. Fix Inline Styles (background-image: url(...))
    const styledElements = container.querySelectorAll('[style*="url("]');
    styledElements.forEach(el => {
        let style = el.getAttribute('style');
        style = resolveStringPaths(style, mdPath);
        el.setAttribute('style', style);
    });
}

/**
 * Resolves paths inside a string (CSS or JS) using the ResolvePath logic.
 */
function resolveStringPaths(str, mdPath) {
    if (!str) return str;
    // Matches url('./path') or url("../path") or url(path)
    return str.replace(/url\(['"]?([^'"\)]+)['"]?\)/g, (match, path) => {
        if (path.startsWith('http') || path.startsWith('/') || path.startsWith('data:')) return match;
        return `url('${resolvePath(path, mdPath)}')`;
    }).replace(/src=["']\.\/([^"']+)["']/g, (match, path) => {
        // Matches src="./path" specifically for JS/HTML snippets
        return `src="${resolvePath('./' + path, mdPath)}"`;
    });
}

/**
 * Core Path Resolution Logic (Pure Function)
 */
function resolvePath(relPath, mdPath) {
    if (!relPath || relPath.startsWith('http') || relPath.startsWith('/') || relPath.startsWith('data:')) return relPath;
    
    // Normalize mdPath dir
    const mdDirParts = mdPath.split('/').slice(0, -1).filter(p => p !== '');
    const relParts = relPath.split('/');
    const stack = [...mdDirParts];
    
    for (const part of relParts) {
        if (part === '..') {
            if (stack.length > 0) stack.pop();
        } else if (part !== '.' && part !== '') {
            stack.push(part);
        }
    }

    let result = stack.join('/');
    
    // Conversion Logic for Standard HTML entry points
    if (result.startsWith('md/') && result.endsWith('.md')) {
        // Strip the md/ prefix and change extension to .html, moving to html/ folder
        result = 'html/' + result.substring(3).replace('.md', '.html');
    }
    
    return result;
}
