"""Package the reviewed static dashboard for Cloudflare Pages; no external dependencies."""
from pathlib import Path
import base64
import hashlib
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist'
MAX_FILE_SIZE = 25 * 1024 * 1024


def build():
    html = (ROOT / 'index.html').read_text()
    headers = (ROOT / '_headers').read_text()
    scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
    if len(scripts) != 2:
        raise ValueError('Expected the two reviewed inline application scripts.')
    for script in scripts:
        digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
        if f"'sha256-{digest}'" not in headers:
            raise ValueError('Stale CSP hashes. Run python scripts/build-v3.py first.')
    manifest = ROOT / 'data/manifest.json'
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ['index.html', '404.html', '_headers']:
        shutil.copy2(ROOT / name, OUTPUT / name)
    shutil.copytree(ROOT / 'data', OUTPUT / 'data', ignore=shutil.ignore_patterns('.gitkeep'))
    files = [path for path in OUTPUT.rglob('*') if path.is_file()]
    oversized = [str(path.relative_to(OUTPUT)) for path in files if path.stat().st_size > MAX_FILE_SIZE]
    if oversized:
        raise ValueError('Files exceed the Pages 25 MiB asset limit: ' + ', '.join(oversized))
    if len(files) > 20000:
        raise ValueError('The static bundle exceeds 20,000 files.')
    print(f'Cloudflare Pages bundle ready: {len(files)} files, {sum(p.stat().st_size for p in files):,} bytes in dist/.')


if __name__ == '__main__':
    build()
