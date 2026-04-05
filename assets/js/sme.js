/** 
 * Synthetic Content Engine (SME) v1.0.0
 * Dynamically renders Markdown files into the Synthetic Edition shell.
 */

async function loadMarkdown() {
    const contentArea = document.getElementById('sme-content');
    if (!contentArea) return;

    const mdPath = contentArea.getAttribute('data-src');
    if (!mdPath) return;

    try {
        const response = await fetch(mdPath);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const mdText = await response.text();

        // Configure Marked.js
        marked.setOptions({
            gfm: true,
            breaks: true,
            headerIds: true,
            mangle: false
        });

        // Parse and Sanitize
        const rawHtml = marked.parse(mdText);
        const cleanHtml = DOMPurify.sanitize(rawHtml);

        // Inject Content
        contentArea.innerHTML = cleanHtml;

        // Apply Syntax Highlighting (if Prism is loaded)
        if (typeof Prism !== 'undefined') {
            Prism.highlightAllUnder(contentArea);
        }

        // Emit 'sme-loaded' event for custom handlers
        window.dispatchEvent(new CustomEvent('sme-loaded'));

    } catch (error) {
        console.error('SME Error:', error);
        contentArea.innerHTML = `<div class="p-8 border border-red-500/20 bg-red-500/10 rounded-2xl text-red-400 text-xs font-mono">
            [FATAL] FAILED TO FETCH DATA STREAM: ${error.message}<br>
            CHECK ORIGIN AND ENDPOINT PATHS.
        </div>`;
    }
}

document.addEventListener('DOMContentLoaded', loadMarkdown);
