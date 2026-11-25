"""Limited, dependency-free public repository structural checks."""
from pathlib import Path
import json
import hashlib
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    'README.md', 'profile/README.md', 'SECURITY.md', 'CONTRIBUTING.md',
    'CODE_OF_CONDUCT.md', 'ACCESSIBILITY.md', 'SUPPORT.md',
    'assets/brand/azvela-corporate-banner.png', 'docs/PRINCIPLES.md',
    'assets/brand/azvela-origin-film.mp4', 'assets/brand/azvela-origin-poster.jpg',
    'assets/brand/azvela-origin-preview.gif', 'assets/brand/media-manifest.json',
    'docs/ORIGIN.md', 'docs/ES.md',
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
    root = root.resolve()
    errors = []
    if not (root / 'profile/README.md').is_file() or not (root / '.github/workflows/validate-public-docs.yml').is_file() or root == Path.home().resolve():
        return ['Refusing to scan: expected Azvela repository root, not HOME or an unrelated directory']
    for name in REQUIRED:
        path = root / name
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f'missing or empty: {name}')
    markdown = [root / name for name in REQUIRED if name.endswith('.md')]
    markdown.extend((root / 'docs').glob('*.md'))
    markdown.extend((root / 'workflow-templates').glob('*.md'))
    for path in sorted(set(markdown)):
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root):
            continue
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', path.read_text(encoding='utf-8')):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                prefixes = ('https://github.com/Azvelahq/.github/blob/main/', 'https://raw.githubusercontent.com/Azvelahq/.github/main/')
                prefix = next((item for item in prefixes if target.startswith(item)), None)
                if prefix and not (root / unquote(urlsplit(target[len(prefix):]).path)).is_file():
                    errors.append(f'{path.relative_to(root)}: missing repository link {target}')
                continue
            if not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f'{path.relative_to(root)}: broken local link {target}')
    brand = root / 'assets/brand'
    try:
        data = json.loads((brand / 'media-manifest.json').read_text(encoding='utf-8'))
        limits = {'azvela-origin-film.mp4': 10_000_000, 'azvela-origin-poster.jpg': 150_000, 'azvela-origin-preview.gif': 3_000_000}
        if set(data['assets']) != set(limits):
            errors.append('media manifest must enumerate exactly the three origin assets')
        for name, limit in limits.items():
            p = brand / name
            if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):
                errors.append(f'unsafe or missing media: {name}')
                continue
            raw = p.read_bytes()
            item = data['assets'][name]
            if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256'] or len(raw) > limit:
                errors.append(f'media integrity or budget failure: {name}')
        profile = (root / 'profile/README.md').read_text(encoding='utf-8')
        if 'azvela-origin-poster.jpg' not in profile or 'azvela-origin-preview.gif' in profile or '<video' in profile.lower():
            errors.append('profile must use static origin poster, not automatic motion/video')
        origin = (root / 'docs/ORIGIN.md').read_text(encoding='utf-8')
        if 'azvela-origin-preview.gif' not in origin or 'azvela-origin-film.mp4' not in origin or '<details>' not in origin:
            errors.append('origin page must provide opt-in preview and film')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'media manifest: {exc}')
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
