"""Create a self-contained snapshot of the public fishing landing page."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
import hashlib
import re
import subprocess

ORIGIN = 'https://project-42307b.lovable.app/'
ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
FONT_URL = 'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Unbounded:wght@500;700&display=swap'

def fetch(url):
    return subprocess.check_output(['curl', '-fsSL', '--max-time', '45', '--retry', '1', url])

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ('src', 'href') and value and value.startswith(('/assets/', '/favicon')):
                self.paths.add(value)

def main():
    DIST.mkdir(exist_ok=True)
    html = fetch(ORIGIN).decode()
    # Platform analytics are specific to the original hosting account.
    html = re.sub(r'<script\b[^>]*src="/__l5e/[^>]*></script>', '', html)
    html = html.replace('<html lang="en">', '<html lang="ru">')
    parser = Assets()
    parser.feed(html)
    pending, saved = list(parser.paths), set()
    while pending:
        path = pending.pop()
        if path in saved:
            continue
        data = fetch(urljoin(ORIGIN, path))
        target = DIST / path.lstrip('/')
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.endswith(('.css', '.js')):
            content = data.decode()
            refs = re.findall(r'[\"\x27`]((?:\./|/assets/)[^\"\x27`\s]{1,180}\.(?:js|css|jpg|png|svg|webp|woff2))[\"\x27`]', content)
            refs += re.findall(r'url\([\"\x27]?([^\s)\"\x27]+)', content) if path.endswith('.css') else []
            for ref in refs:
                full = urljoin(urljoin(ORIGIN, path), ref)
                if full.startswith(ORIGIN):
                    pending.append(urlsplit(full).path)
            data = content.replace(FONT_URL, '/assets/fonts.css').encode()
        target.write_bytes(data)
        saved.add(path)
        print('Saved', path, len(data))

    font_css = fetch(FONT_URL).decode()
    font_paths = set()
    for url in set(re.findall(r'url\((https://[^)]+)\)', font_css)):
        extension = Path(urlsplit(url).path).suffix or '.woff2'
        filename = hashlib.sha256(url.encode()).hexdigest()[:20] + extension
        path = DIST / 'assets' / 'fonts' / filename
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(fetch(url))
        font_css = font_css.replace(url, '/assets/fonts/' + filename)
        font_paths.add(path)
    (DIST / 'assets' / 'fonts.css').write_text(font_css)
    html = html.replace(FONT_URL.replace('&', '&amp;'), '/assets/fonts.css')
    html = re.sub(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>', '', html)
    (DIST / 'index.html').write_text(html)
    from update_landing import apply_updates
    apply_updates()
    print('Complete:', len(saved), 'site assets and', len(font_paths), 'font files')

if __name__ == '__main__':
    main()
