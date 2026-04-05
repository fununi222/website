import os
import re

TARGET_WORDS = {
    'ai/2026-04-03-agent-orchestration.md': ['ハルシネーション'],
    'ai/2026-04-03-operation-automation.md': ['vSphere'],
    'ai/2026-04-03-oss-automation-tools.md': ['IaC', 'Terraform'],
    'ai/2026-04-05-ai-hallucination.md': ['自己回帰モデル'],
    'ai/2026-04-05-openclaw-google-calendar-automation.md': ['API', 'VPS'],
    'dev/2026-04-05-altra-recommender-retrospective.md': ['アルゴリズム'],
    'dev/2026-04-05-freeman-project-hp-retrospective.md': ['レスポンシブ'],
    'finance/2026-04-04-high-return-payment-routes.md': ['ポイ活'],
    'finance/2026-04-05-smbc-million-challenge-revolut-route.md': ['修行'],
    'infra/2026-04-02-ctk-auto-remediation.md': ['CBT'],
    'infra/2026-04-03-oss-research-operation.md': ['PoC'],
    'infra/2026-04-03-win-110-scaling-fancyzones.md': ['カスタムスケーリング'],
    'infra/2026-04-04-openclaw-vps-network-troubleshoot.md': ['トラブルシュート'],
    'lpo/LPO_SYSTEM.md': ['プロジェクトマネジメント']
}

DATE_MARKER = '<div class="text-[10px] text-on-surface-variant opacity-60 text-right mb-6 tracking-widest font-mono mt-2">Last Updated: 2026-04-06</div>'
CHANGELOG_ENTRY = "\n\n## 変更履歴 (Changelog)\n- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデートを実施。\n"

def process_file(filepath, words):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update YAML date
    content = re.sub(r'(?m)^date:\s*".*?"', 'date: "2026-04-06"', content)

    # 2. Inject Last Updated Marker under H1 (if not already there)
    if 'Last Updated: 2026-04-06' not in content:
        # Avoid injecting into early frontmatter #, so we look for ^#\s+.*
        # By standard, the first H1 tag in our standard docs
        # We replace the first occurrence of `# <title>` with `# <title>\n<div...>`
        content = re.sub(r'(^# [^\n]+)', r'\1\n' + DATE_MARKER, content, count=1, flags=re.MULTILINE)

    # 3. Replace target words with dictionary links
    # To avoid replacing inside existing markdown links, we do a very naive but functional replace
    # We will use markdown format [WORD](../glossary/index.html)
    for w in words:
        if f'[{w}]' not in content:
            # simple replace only on first occurrence to avoid destroying markdown
            # negative lookbehind/lookahead to prevent replacing inside URLs or tags
            content = re.sub(f'(?<!\\[){w}(?!\\])', f'[{w}](../glossary/index.html)', content, count=1)

    # 4. Append Changelog if it doesn't already exist for today
    if '2026-04-06**: 用語の自動抽出' not in content:
        if '## 変更履歴' in content:
            # append under the changelog
            content = re.sub(r'(## 変更履歴.*?\n)', r'\1- **2026-04-06**: 用語の自動抽出とクロスリンク（Glossary）の適用、ならびに日付メタデータの統一アップデートを実施。\n', content, count=1)
        else:
            content += CHANGELOG_ENTRY

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Processed {filepath} with words: {words}")

# Execute
for rel_path, words in TARGET_WORDS.items():
    abs_path = os.path.join('.', rel_path.replace('/', os.sep))
    if os.path.exists(abs_path):
        process_file(abs_path, words)
    else:
        print(f"[WARN] File not found: {abs_path}")

print("Mass update complete!")
