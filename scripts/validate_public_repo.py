"""Limited, dependency-free public repository structural checks."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'README.md', 'profile/README.md', 'SECURITY.md', 'CONTRIBUTING.md',
    'CODE_OF_CONDUCT.md', 'ACCESSIBILITY.md', 'SUPPORT.md',
    'assets/brand/azvela-corporate-banner.png', 'docs/PRINCIPLES.md',
    'docs/OPEN_SOURCE.md', 'docs/RESEARCH_PRINCIPLES.md',
    'docs/RESPONSIBLE_AI.md', 'docs/TRUST.md', 'docs/MAINTAINER_SETUP.md',
    '.github/CODEOWNERS', '.github/pull_request_template.md',
    '.github/VULNERABILITY_REPORT.yml', '.github/dependabot.yml',
    '.github/ISSUE_TEMPLATE/config.yml', '.github/ISSUE_TEMPLATE/bug_report.yml',
    '.github/ISSUE_TEMPLATE/feature_proposal.yml',
    '.github/ISSUE_TEMPLATE/research_proposal.yml',
    '.github/ISSUE_TEMPLATE/accessibility_report.yml',
    '.github/ISSUE_TEMPLATE/contact_request.yml',
    '.github/workflows/validate-public-docs.yml',
    'workflow-templates/universal-ci.yml', 'workflow-templates/research-validation.yml',
)

def validate(root):
    errors = []
    for name in REQUIRED:
        path = root / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f'missing or empty: {name}')
    for path in root.rglob('*.md'):
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', path.read_text(encoding='utf-8')):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f'{path.relative_to(root)}: broken local link {target}')
    workflows = sorted((root / '.github/workflows').glob('*.yml')) + sorted((root / 'workflow-templates').glob('*.yml'))
    for path in workflows:
        body = path.read_text(encoding='utf-8')
        if not re.search(r'(?m)^permissions:\s*\n  contents: read\s*$', body):
            errors.append(f'{path.name}: expected read-only top-level permissions')
        if re.search(r'(?m)^\s*pull_request_target\s*:', body):
            errors.append(f'{path.name}: pull_request_target is not allowed in these starter workflows')
        for reference in re.findall(r'(?m)^\s*(?:-\s*)?uses:\s*([^\s#]+)', body):
            if not re.fullmatch(r'[^@]+@[a-f0-9]{40}', reference):
                errors.append(f'{path.name}: unpinned action {reference}')
        if 'persist-credentials: false' not in body:
            errors.append(f'{path.name}: checkout credentials not disabled')
    templates = root / 'workflow-templates'
    for path in templates.glob('*.yml'):
        meta = path.with_suffix('.properties.json')
        try:
            data = json.loads(meta.read_text(encoding='utf-8'))
            if not all(isinstance(data.get(k), str) and data[k] for k in ('name', 'description')):
                errors.append(f'{meta.name}: missing name or description')
        except (OSError, ValueError) as exc:
            errors.append(f'{meta.name}: {exc}')
    for meta in templates.glob('*.properties.json'):
        if not (templates / (meta.name.removesuffix('.properties.json') + '.yml')).is_file():
            errors.append(f'{meta.name}: no matching workflow')
    return errors

if __name__ == '__main__':
    failures = validate(ROOT)
    if failures:
        print('\n'.join(failures), file=sys.stderr)
        sys.exit(1)
    print('PASS: public repository structural checks (limited scope).')
