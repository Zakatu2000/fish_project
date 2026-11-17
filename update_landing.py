"""Apply the approved landing-page content changes to the static snapshot."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'

def remove_platform_badge(html):
    html = re.sub(r'<style>\s*#lovable-badge\s*\{.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<aside\b[^>]*id="lovable-badge"[^>]*>.*?</aside>', '', html, flags=re.S)
    html = re.sub(r'<script>\s*\(\(\) => \{.*?lovable-badge.*?</script>', '', html, flags=re.S)
    return html

def apply_updates():
    partner_markup = (ROOT / 'source/partners.html').read_text().strip()
    (DIST / 'assets/partners-content.js').write_text('export const partnersMarkup = ' + json.dumps(partner_markup, ensure_ascii=False) + ';\n')
    html_path = DIST / 'index.html'
    html = remove_platform_badge(html_path.read_text())
    html = re.sub(r'<section id="partners".*?</section>', '', html, flags=re.S)
    section = '<section id="partners" aria-label="Рекламодателям и партнёрам">' + partner_markup + '</section>'
    assert '<section id="team"' in html
    html = html.replace('<section id="team"', section + '<section id="team"', 1)
    if 'href="#partners"' not in html:
        html = re.sub(r'(<a href="#team"([^>]+)>Команда</a>)', r'<a href="#partners"\2>Партнёрам</a>\1', html)
    html = html.replace('Бесплатно на этапе MVP', 'Бесплатно для рыбаков')
    html_path.write_text(html)

    route = DIST / 'assets/routes-Ck51385J.js'
    js = route.read_text()
    if './partners-content.js' not in js:
        js = 'import {partnersMarkup} from "./partners-content.js";' + js
    if '[`partners`,`Партнёрам`]' not in js:
        js = js.replace('[`team`,`Команда`]', '[`partners`,`Партнёрам`],[`team`,`Команда`]', 1)
    marker = '(0,T.jsxs)(Q,{id:`team`'
    insertion = '(0,T.jsx)(`section`,{id:`partners`,"aria-label":`Рекламодателям и партнёрам`,dangerouslySetInnerHTML:{__html:partnersMarkup}}),'
    if insertion not in js:
        assert marker in js
        js = js.replace(marker, insertion + marker, 1)
    js = js.replace('Бесплатно на этапе MVP', 'Бесплатно для рыбаков')
    js = js.replace('На этапе MVP сервис бесплатный.', 'Базовый доступ для рыбаков планируем оставить бесплатным. Основной источник дохода проекта — рекламные размещения рыболовных магазинов, производителей снастей, платных водоёмов и баз отдыха. Сейчас партнёрское направление находится на этапе подготовки.')
    route.write_text(js)
    print('Updated: platform badge removed; partner section, navigation and business model added.')

if __name__ == '__main__':
    apply_updates()
