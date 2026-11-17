"""Prepare the static site for GitHub Pages at /fish_project/."""
from pathlib import Path
from html.parser import HTMLParser
import re
import shutil

ROOT = Path(__file__).resolve().parent
BASE = '/fish_project'
OUTPUT = ROOT / 'docs'

def build():
    source = ROOT / 'dist'
    if not (source / 'index.html').is_file():
        raise SystemExit('dist/index.html is missing')
    OUTPUT.mkdir(exist_ok=True)
    shutil.copytree(source, OUTPUT, dirs_exist_ok=True)
    for file in OUTPUT.rglob('*'):
        if file.is_file() and file.suffix in {'.html', '.css', '.js'}:
            text = file.read_text()
            text = text.replace('/assets/', BASE + '/assets/')
            text = text.replace('/favicon.ico', BASE + '/favicon.ico')
            if file.name == 'index-DIdQpKfk.js':
                assert text.count('e.update({basepath:``') == 1
                text = text.replace('e.update({basepath:``', 'e.update({basepath:`' + BASE + '`')
                text = text.replace('Z=function(e){return`/`+e}', 'Z=function(e){return`' + BASE + '/`+e}')
                text = text.replace('`html`,{lang:`en`', '`html`,{lang:`ru`')
            file.write_text(text)
    (OUTPUT / '.nojekyll').touch()
    validate()
    print('GitHub Pages files are ready in docs/.')

def validate():
    refs = []
    class Assets(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key in ('href', 'src') and value and value.startswith(BASE + '/'):
                    refs.append(value)
    html = (OUTPUT / 'index.html').read_text()
    Assets().feed(html)
    for file in OUTPUT.rglob('*.css'):
        refs.extend(re.findall(r'url\([\"\x27]?(' + BASE + r'/[^)\"\x27]+)', file.read_text()))
    for ref in refs:
        assert (OUTPUT / ref.removeprefix(BASE + '/')).is_file(), ref
    assert '/assets/' not in html.replace(BASE + '/assets/', '')
    assert 'lovable-badge' not in html
    assert 'id="partners"' in html
    assert f'basepath:`{BASE}`' in (OUTPUT / 'assets/index-DIdQpKfk.js').read_text()
    print(f'Validated {len(refs)} asset references, route base and partner content.')

if __name__ == '__main__':
    build()
