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
        let response = await fetch(mdPath);
        
        // Backward compatibility: If the file isn't found at the root-relative path,
        // it might have been moved to the md/ directory.
        if (!response.ok && !mdPath.startsWith('md/')) {
            const fallbackPath = 'md/' + mdPath;
            console.log(`[SME] Path not found: ${mdPath}. Trying fallback: ${fallbackPath}`);
            response = await fetch(fallbackPath);
            if (response.ok) {
                mdPath = fallbackPath; // Update mdPath for correct relative asset resolution
            }
        }

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
        
        // 7. Handle Breadcrumbs & Article Dates Metadata
        updateBreadcrumbs(mdPath, metadata.title);
        renderArticleHeaderMeta(metadata);

        // Emit Custom Event for and-hoc scripts
        const event = new CustomEvent('sme-loaded', { 
            detail: { metadata, element: contentArea } 
        });
        window.dispatchEvent(event);

        // 7. Handle Scroll to Text Fragment (for Cloud latency issues)
        handleTextFragments();

        // 8. Initialize Lightbox for all images
        initLightbox();

        // 9. Generate Table of Contents
        generateTableOfContents();

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
    
    // Support paths like "md/infra/backup/article.md" or "infra/article.md"
    const parts = mdPath.split('/').filter(p => p !== '');
    let category = parts[0];
    if (category === 'md' && parts.length > 1) {
        category = parts[1];
    }
    
    if (!category || category === mdPath) return; 

    // Classes
    const activeNavClass = 'text-secondary border-b-2 border-secondary pb-1'.split(' ');
    const inactiveNavClass = 'text-on-surface-variant hover:text-secondary transition-colors'.split(' ');

    // Patch Nav (Navbar & Sidebar)
    const links = document.querySelectorAll('nav a, aside a');
    links.forEach(a => {
        if (!a.href) return;
        
        // Match either category/index.html or the category directory exactly
        const isMatch = a.href.includes(category + '/index.html');
        
        // Ensure "FunUni-lab" absolute root doesn't get swept
        if (a.textContent.includes('FunUni-lab')) return;

        if (isMatch) {
            a.classList.remove(...inactiveNavClass);
            a.classList.add(...activeNavClass);
            // If it's a sidebar link, also ensure active state
            if (a.closest('aside')) {
                a.classList.add('bg-surface-container', 'text-secondary', 'border-r-2');
                a.classList.remove('text-slate-500');
            }
        } else {
            a.classList.remove(...activeNavClass);
            a.classList.add(...inactiveNavClass);
            if (a.closest('aside')) {
                a.classList.remove('bg-surface-container', 'text-secondary', 'border-r-2');
                a.classList.add('text-slate-500');
            }
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

    // 3. Responsive Table Wrapping
    const tables = container.querySelectorAll('table');
    tables.forEach(table => {
        // Skip if already wrapped
        if (table.parentElement.classList.contains('table-wrap')) return;
        
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrap';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
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
    // Converts internal source links (md/category/name.md) to public links (html/category/name.html)
    if (result.startsWith('md/') && result.endsWith('.md')) {
        const baseArticle = result.substring(3).replace('.md', '.html');
        result = 'html/' + baseArticle;
    }
    
    return result;
}

/**
 * Updates the breadcrumb navigation based on the article path.
 */
function updateBreadcrumbs(mdPath, title) {
    const breadcrumbArea = document.getElementById('sme-breadcrumbs');
    if (!breadcrumbArea) return;

    const parts = mdPath.split('/').filter(p => p !== '');
    let currentPath = '';
    const breadcrumbs = [];

    // Home
    breadcrumbs.push(`<a href="index.html" class="hover:text-primary transition-colors">Home</a>`);

    // Category / Subcategory
    let mdFound = false;
    parts.forEach((part, index) => {
        if (part === 'md') {
            mdFound = true;
            return;
        }
        if (index === parts.length - 1) return; // Last part is the filename

        currentPath += (currentPath ? '/' : '') + part;
        
        // Humanize category names
        const label = part.charAt(0).toUpperCase() + part.slice(1);
        
        // Link to the index page of the category (e.g. infra/index.html)
        const isCategory = (mdFound && index === 1) || (!mdFound && index === 0);
        const link = isCategory ? `${part}/index.html` : '#';
        
        breadcrumbs.push(`<span class="text-slate-700">/</span>`);
        if (link !== '#') {
            breadcrumbs.push(`<a href="${link}" class="hover:text-primary transition-colors">${label}</a>`);
        } else {
            breadcrumbs.push(`<span>${label}</span>`);
        }
    });

    // Current Article
    breadcrumbs.push(`<span class="text-slate-700">/</span>`);
    breadcrumbs.push(`<span class="text-primary truncate max-w-[200px]">${title || 'Article'}</span>`);

    breadcrumbArea.innerHTML = breadcrumbs.join(' ');
}

/**
 * Renders publication date and updated date badges below breadcrumbs.
 */
function renderArticleHeaderMeta(metadata) {
    const breadcrumbArea = document.getElementById('sme-breadcrumbs');
    if (!breadcrumbArea) return;

    let metaArea = document.getElementById('sme-article-meta-banner');
    if (!metaArea) {
        metaArea = document.createElement('div');
        metaArea.id = 'sme-article-meta-banner';
        metaArea.className = 'flex flex-wrap items-center gap-3 my-4 pb-4 border-b border-white/10 text-xs font-mono text-slate-400';
        breadcrumbArea.parentNode.insertBefore(metaArea, breadcrumbArea.nextSibling);
    }

    const pubDate = metadata.date || '2026-04-09';
    const updDate = metadata.updated || metadata.updated_date || '2026-08-02';

    metaArea.innerHTML = `
        <div class="flex items-center gap-1.5 bg-white/5 border border-white/10 px-3 py-1 rounded-full text-slate-300">
            <span class="material-symbols-outlined text-sm text-slate-400">calendar_today</span>
            <span>公開日: ${pubDate}</span>
        </div>
        <div class="flex items-center gap-1.5 bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 px-3 py-1 rounded-full font-semibold">
            <span class="material-symbols-outlined text-sm text-cyan-400">update</span>
            <span>最終更新日: ${updDate}</span>
        </div>
    `;
}

/**
 * Dynamically generates a Table of Contents (TOC) sidebar and sets up scroll tracking.
 */
function generateTableOfContents() {
    const tocList = document.getElementById('sme-toc-list');
    const mobileTocList = document.getElementById('sme-mobile-toc-list');
    const tocWrapper = document.getElementById('sme-toc-wrapper');
    const mobileTocWrapper = document.getElementById('sme-mobile-toc-wrapper');
    const contentArea = document.getElementById('sme-content');
    if (!contentArea) return;

    const headings = contentArea.querySelectorAll('h2, h3');
    if (headings.length < 2) {
        if (tocWrapper) {
            tocWrapper.classList.add('hidden');
            tocWrapper.style.display = '';
        }
        if (mobileTocWrapper) {
            mobileTocWrapper.classList.add('hidden');
        }
        return;
    }

    if (tocWrapper) {
        tocWrapper.classList.remove('hidden');
        tocWrapper.style.display = '';
    }
    if (mobileTocWrapper) {
        mobileTocWrapper.classList.remove('hidden');
    }

    if (tocList) tocList.innerHTML = '';
    if (mobileTocList) mobileTocList.innerHTML = '';

    headings.forEach((heading, idx) => {
        if (!heading.id) {
            heading.id = 'sme-toc-heading-' + idx;
        }

        const createNavItem = (isMobile = false) => {
            const li = document.createElement('li');
            li.className = 'w-full min-w-0';
            const a = document.createElement('a');
            a.href = '#' + heading.id;
            a.textContent = heading.textContent.replace(/^#+\s*/, '');
            
            if (isMobile) {
                if (heading.tagName === 'H2') {
                    a.className = 'block text-xs font-semibold text-slate-300 hover:text-cyan-400 transition-colors py-1.5 break-words whitespace-normal leading-relaxed';
                } else {
                    a.className = 'block text-xs text-slate-400 hover:text-cyan-400 transition-colors pl-3 border-l border-white/10 py-1 break-words whitespace-normal leading-relaxed';
                }
            } else {
                if (heading.tagName === 'H2') {
                    a.className = 'block text-xs font-semibold text-slate-300 hover:text-cyan-400 transition-colors truncate py-1';
                } else {
                    a.className = 'block text-xs text-slate-400 hover:text-cyan-400 transition-colors truncate pl-3 border-l border-white/10 py-1';
                }
            }

            a.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.getElementById(heading.id);
                if (target) {
                    // Tab support: if heading is inside a tab-content container, trigger tab click
                    const tabParent = target.closest('.tab-content, [id^="sec-"]');
                    if (tabParent && tabParent.classList.contains('hide-content')) {
                        const btn = document.querySelector(`[data-target="${tabParent.id}"]`);
                        if (btn) btn.click();
                    }

                    const navHeight = 90;
                    const bodyRect = document.body.getBoundingClientRect().top;
                    const elementRect = target.getBoundingClientRect().top;
                    const elementPosition = elementRect - bodyRect;
                    const offsetPosition = elementPosition - navHeight;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    // Close mobile TOC details if opened
                    if (isMobile && mobileTocWrapper && mobileTocWrapper.open) {
                        mobileTocWrapper.open = false;
                    }
                }
            });
            li.appendChild(a);
            return li;
        };

        if (tocList) tocList.appendChild(createNavItem(false));
        if (mobileTocList) mobileTocList.appendChild(createNavItem(true));
    });

    // Active heading tracking on scroll
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    const highlightLinks = (container) => {
                        if (!container) return;
                        container.querySelectorAll('a').forEach(link => {
                            if (link.getAttribute('href') === '#' + id) {
                                link.classList.add('text-cyan-400', 'font-bold');
                                link.classList.remove('text-slate-300', 'text-slate-400');
                            } else {
                                link.classList.remove('text-cyan-400', 'font-bold');
                                if (link.classList.contains('pl-3')) {
                                    link.classList.add('text-slate-400');
                                } else {
                                    link.classList.add('text-slate-300');
                                }
                            }
                        });
                    };
                    highlightLinks(tocList);
                    highlightLinks(mobileTocList);
                }
            });
        }, { rootMargin: '-90px 0px -70% 0px' });

        headings.forEach(heading => observer.observe(heading));
    }
}
