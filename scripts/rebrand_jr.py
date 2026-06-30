# -*- coding: utf-8 -*-
"""Rebrand global GomesEDutra -> Joao Rocha (UTF-8 seguro)."""
from pathlib import Path

ROOT = Path('C:/Users/gabri/GomesEDutra')

FILES = [
    'index.html',
    '_layouts/base.html',
    '_layouts/landing.html',
    'scripts/build_site.py',
    'README.md',
    'assets/analytics.js',
    'assets/tracker.js',
    'robots.txt',
    'sitemap.xml',
]

# ordem importa: do mais especifico para o mais geral
PAIRS = [
    ('GomesEDutra', 'JoaoRochaAdvogado'),
    ('Gomes & Dutra Advocacia', 'João Rocha Advocacia'),
    ('Gomes & Dutra', 'João Rocha'),
    ('Gomes%20%26%20Dutra', 'Jo%C3%A3o%20Rocha'),
    ('5533999547938', '5500000000000'),
    ('escritoriogomesedutra@gmail.com', 'contato@seudominio.com.br'),
    ('seal-gd', 'seal-jr'),
    ('logo-gd', 'logo-jr'),
    ('favicon-gd', 'favicon-jr'),
    ('Manhuaçu/MG e região', 'todo o Brasil'),
    ('Manhuaçu/MG', 'todo o Brasil'),
    ('Manhuaçu', 'todo o Brasil'),
]

total = 0
for rel in FILES:
    p = ROOT / rel
    if not p.exists():
        print('  (pulado, nao existe)', rel)
        continue
    txt = p.read_text(encoding='utf-8')
    before = txt
    n = 0
    for a, b in PAIRS:
        c = txt.count(a)
        if c:
            txt = txt.replace(a, b)
            n += c
    if txt != before:
        p.write_text(txt, encoding='utf-8')
    total += n
    print(f'  {rel}: {n} trocas')

print('total de trocas:', total)
