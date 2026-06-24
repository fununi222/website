import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEAD_LINKS = {
    'infra/aws-minimal-iac-patterns.md': 'aws-minimal-iac-patterns.png',
    'infra/rubrik-api-code-capture.md': 'rubrik-api-code-capture.png',
    'infra/rubrik-backup-load-balancing.md': 'rubrik-backup-load-balancing.png',
    'infra/rubrik-graphql-xsoar-automation.md': 'rubrik-graphql-xsoar-automation.png',
    'infra/rubrik-m365-alert-tuning.md': 'rubrik-m365-alert-tuning.png',
    'infra/rubrik-max-objects-limits.md': 'rubrik-max-objects-limits.png',
    'infra/rubrik-scaling-strategy-nodes.md': 'rubrik-scaling-strategy-nodes.png',
    'infra/rubrik-threat-log-extraction.md': 'rubrik-threat-log-extraction.png',
    'infra/rubrik-threat-monitoring-fp.md': 'rubrik-threat-monitoring-fp.png',
    'infra/vast-recovery-validation.md': 'vast-recovery-validation.png',
    'dev/devcontainer-harbor-intro.md': 'devcontainer-harbor-intro.png',
    'dev/devcontainer-harbor-operations.md': 'devcontainer-harbor-operations.png',
    'dev/devcontainer-harbor-security.md': 'devcontainer-harbor-security.png',
    'other/kamakura-cospa-gourmet.md': 'kamakura-cospa-gourmet.png',
    'other/kamakura-zushi-lunch-hub.md': 'kamakura-cospa-gourmet.png',
    'other/kutchan-local-foods.md': 'kutchan-local-foods.png',
    'other/niseko-accommodation-tax.md': 'niseko-accommodation-tax.png',
    'other/niseko-cospa-travel.md': 'niseko-cospa-travel.png',
    'other/niseko-gourmet-cospa.md': 'niseko-gourmet-cospa.png',
    'other/niseko-onsen-activity.md': 'niseko-onsen-activity.png',
    'other/niseko-transport-guide.md': 'niseko-transport-guide.png',
    'other/yakitori-cospa-yokohama-kannai.md': 'yakitori-cospa-yokohama-kannai.png',
    'other/zushi-cospa-gourmet.md': 'zushi-cospa-gourmet.png'
}

def remove_dead_figure(filepath, img_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find a <figure> block that contains the specific image name
    # This pattern captures the whole figure block including the img tag
    pattern = re.compile(rf'(<figure.*?>[\s\S]*?{re.escape(img_name)}[\s\S]*?</figure>)', re.MULTILINE)
    
    new_content = pattern.sub('', content)
    
    # Clean up potentially multiple newlines
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    cleaned_count = 0
    for rel_path, img_name in DEAD_LINKS.items():
        abs_path = os.path.join(BASE_DIR, rel_path.replace('/', os.sep))
        if os.path.exists(abs_path):
            if remove_dead_figure(abs_path, img_name):
                cleaned_count += 1
                print(f"Cleaned: {rel_path}")
            else:
                print(f"Warning: Figure not found in {rel_path} for {img_name}")
        else:
            print(f"Error: File not found: {abs_path}")
            
    print(f"\nSuccessfully cleaned up {cleaned_count} articles.")

if __name__ == '__main__':
    main()
