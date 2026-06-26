"""
Build estatico do site Gomes & Dutra Advocacia (sem blog, sem admin).
Gera as landings (1 por chave em assets/landings-content.json) + sitemap + robots.

Uso:
  py scripts/build_site.py            -> escreve direto nas pastas <slug>/ na raiz
"""
import json, datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
LAYOUTS = ROOT / '_layouts'
SITE_URL = 'https://vejaseusite.github.io/GomesEDutra'

LANDINGS_PATH = ROOT / 'assets' / 'landings-content.json'
try:
    LANDINGS = json.loads(LANDINGS_PATH.read_text(encoding='utf-8'))
except json.JSONDecodeError as e:
    print(f'ERRO: landings-content.json invalido (linha {e.lineno}, col {e.colno}): {e.msg}')
    raise SystemExit(2)

env = Environment(
    loader=FileSystemLoader(str(LAYOUTS)),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True,
)

landing_tpl = env.get_template('landing.html')
for slug, page in LANDINGS.items():
    out = ROOT / slug / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(landing_tpl.render(
        page=page,
        related_posts=[],
        page_title=page['page_title'],
        page_description=page['page_description'],
        canonical=f"{SITE_URL}/{slug}/",
        og_image=f"{SITE_URL}/assets/og-banner.jpg",
        site_url=SITE_URL,
    ), encoding='utf-8')
    print('landing:', slug)

# sitemap.xml
today = datetime.date.today().isoformat()
urls = [(f'{SITE_URL}/', '1.0', today)]
for slug in LANDINGS.keys():
    urls.append((f'{SITE_URL}/{slug}/', '0.9', today))
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, p, l in urls:
    sm += f'  <url><loc>{u}</loc><lastmod>{l}</lastmod><priority>{p}</priority></url>\n'
sm += '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sm, encoding='utf-8')

# robots.txt
(ROOT / 'robots.txt').write_text(
    f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n', encoding='utf-8')

print(f'\nDone. {len(LANDINGS)} landings + sitemap ({len(urls)} URLs) + robots.')
