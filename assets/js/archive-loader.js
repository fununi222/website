/**
 * Archive Loader
 * Dynamically fetches and renders the complete list of articles for a category.
 */
document.addEventListener('DOMContentLoaded', async () => {
    const archiveContainer = document.getElementById('archive-list');
    if (!archiveContainer) return;

    // Determine category from URL more robustly
    const path = window.location.pathname.replace(/\\/g, '/');
    const pathParts = path.split('/').filter(p => p !== '');
    
    let category = 'other';
    // If the path ends in 'index.html', the category is the parent dir
    // file:///C:/path/website/other/index.html -> parts: [..., 'website', 'other', 'index.html']
    // https://domain.com/website/other/ -> parts: [..., 'website', 'other']
    if (pathParts.length > 0) {
        const lastPart = pathParts[pathParts.length - 1].toLowerCase();
        if (lastPart === 'index.html' || lastPart === 'index.htm') {
            category = pathParts.length >= 2 ? pathParts[pathParts.length - 2] : 'other';
        } else {
            category = lastPart;
        }
    }
    
    // Safety check for known categories
    const validCategories = ['infra', 'dev', 'ai', 'finance', 'other', 'lpo'];
    if (!validCategories.includes(category)) {
        category = 'other';
    }

    try {
        let articles = [];
        if (typeof window_article_index !== 'undefined') {
            articles = window_article_index;
        } else {
            const response = await fetch('../assets/data/article_index.json');
            if (!response.ok) throw new Error('Failed to load article index');
            articles = await response.json();
        }

        // Filter by category
        let categoryArticles = articles.filter(a => a.category === category);

        // DEDUPLICATION: Exclude articles already linked as "Featured" on the page
        const existingLinks = Array.from(document.querySelectorAll('a')).map(a => {
            try { return new URL(a.href).pathname.replace(/\\/g, '/'); } catch(e) { return a.getAttribute('href'); }
        });
        
        categoryArticles = categoryArticles.filter(article => {
            const artPath = article.path.startsWith('/') ? article.path : '/' + article.path;
            // Check if any existing link ends with the article path (proxy html)
            const isFeatured = existingLinks.some(link => link && link.endsWith(article.path));
            return !isFeatured;
        });

        if (categoryArticles.length === 0) {
            archiveContainer.innerHTML = '<p class="text-slate-500 font-mono text-xs">No additional research logs found for this domain.</p>';
            const countBadge = document.getElementById('archive-count');
            if (countBadge) countBadge.textContent = `0 LOGS`;
            return;
        }

        // Group by sub-category
        const grouped = {};
        categoryArticles.forEach(article => {
            const parts = article.path.split('/');
            let subCategory = parts.length > 2 ? parts[1] : parts[0];
            if (!grouped[subCategory]) grouped[subCategory] = [];
            grouped[subCategory].push(article);
        });

        const iconMap = {
            'backup': '🛡️', 'cloud': '☁️', 'network': '🌐', 'ops': '⚙️',
            'automation': '🤖', 'llm-research': '🧠', 'ai-coding': '💻',
            'container': '⚓', 'modern-js': '⚛️', 'finance': '💰',
            'travel': '✈️', 'gourmet': '🍽️', 'tech-life': '🌌', 'other': '📁'
        };

        const themeMap = {
            'backup': 'primary', 'cloud': 'secondary', 'network': 'tertiary', 'ops': 'primary',
            'automation': 'secondary', 'llm-research': 'tertiary', 'ai-coding': 'secondary',
            'container': 'primary', 'modern-js': 'tertiary', 'finance': 'amber-400',
            'travel': 'emerald-400', 'gourmet': 'emerald-500', 'tech-life': 'slate-400', 'other': 'white'
        };

        let html = '';
        for (const [subCat, arts] of Object.entries(grouped)) {
            const displayCat = subCat.charAt(0).toUpperCase() + subCat.slice(1).replace(/-/g, ' ');
            const theme = themeMap[subCat] || 'primary';
            const icon = iconMap[subCat] || '📄';
            
            html += `
            <section class="mb-24">
              <div class="flex items-center gap-4 mb-12 border-b border-white/5 pb-8">
                <div class="w-1 h-8 bg-${theme} rounded-full"></div>
                <h2 class="text-3xl font-bold font-headline tracking-tighter text-white uppercase">${displayCat}</h2>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            `;
            
            arts.forEach(article => {
                const linkHref = `../html/${article.path}`;
                // Avoid using tailwind arbitrary values inside template literals if possible, but standard colors like text-primary work.
                // Note: emerald-400, amber-400 are valid tailwind colors, but our CSS vars are primary, secondary.
                // We'll use inline styles for the border colors to avoid missing dynamic classes.
                const colorHexMap = {
                    'primary': '#aaa4ff', 'secondary': '#00d2ff', 'tertiary': '#00ffca',
                    'amber-400': '#fbbf24', 'emerald-400': '#34d399', 'emerald-500': '#10b981', 'slate-400': '#94a3b8', 'white': '#ffffff'
                };
                const colorHex = colorHexMap[theme] || '#aaa4ff';

                html += `
                <a href="${linkHref}" class="glass-card p-8 group flex flex-col justify-between" style="--hover-border: ${colorHex}4d;" onmouseover="this.style.borderColor='${colorHex}'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                  <div class="space-y-4">
                    <div class="flex items-center justify-between mb-4">
                      <span class="text-2xl">${icon}</span>
                      <span class="text-[9px] font-bold uppercase tracking-[0.2em] border px-2 py-1 rounded" style="color: ${colorHex}; border-color: ${colorHex}33; background: ${colorHex}0d;">${article.date}</span>
                    </div>
                    <h3 class="text-xl font-bold font-headline leading-tight text-white transition-colors" onmouseover="this.style.color='${colorHex}'" onmouseout="this.style.color='#fff'">
                      ${article.title}
                    </h3>
                    <p class="text-sm text-slate-400 leading-relaxed line-clamp-3">
                      ${article.description}
                    </p>
                  </div>
                </a>
                `;
            });
            html += `</div></section>`;
        }

        archiveContainer.innerHTML = html;

        // Update the count badge if it exists
        const countBadge = document.getElementById('archive-count');
        if (countBadge) {
            countBadge.textContent = `${categoryArticles.length} LOGS`;
        }

    } catch (error) {
        console.error('Archive Loader Error:', error);
        archiveContainer.innerHTML = '<p class="text-red-400 font-mono text-xs">Error loading research archive.</p>';
    }
});
