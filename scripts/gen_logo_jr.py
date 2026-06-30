# -*- coding: utf-8 -*-
"""Processa a logo do Joao Rocha: remove fundo navy, corta 'Advocacia Civel',
gera logo (wordmark) + seal (monograma JR) + favicon + og-banner."""
from PIL import Image, ImageFilter
A = 'C:/Users/gabri/GomesEDutra/assets'

src = Image.open('C:/Users/gabri/GomesEDutra/scripts/src-logo-jr.png').convert('RGB')
W, H = src.size


def remove_bg(rgb):
    """Fundo navy (azul dominante) -> transparente. Dourado/branco -> opaco."""
    rgb = rgb.convert('RGB')
    w, h = rgb.size
    px = rgb.load()
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    op = out.load()
    LO, HI = 2, 12  # blueness: <=LO opaco, >=HI transparente
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            blue = b - max(r, g)
            if blue <= LO:
                a = 255
            elif blue >= HI:
                a = 0
            else:
                a = int(255 * (HI - blue) / (HI - LO))
            # mata pixels muito escuros (vinheta) que escaparam
            if r + g + b < 60:
                a = 0
            op[x, y] = (r, g, b, a)
    return out


def trim(img, thr=18):
    a = img.split()[3].point(lambda v: 255 if v > thr else 0)
    bb = a.getbbox()
    return img.crop(bb) if bb else img


def pad_square(img, size, margin=0.12):
    img = trim(img)
    w, h = img.size
    inner = int(size * (1 - 2 * margin))
    sc = min(inner / w, inner / h)
    img = img.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
    canv = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    canv.paste(img, ((size - img.width) // 2, (size - img.height) // 2), img)
    return canv


# --- LOGO (wordmark completo, sem 'Advocacia Civel') : y 0..380 ---
logo = remove_bg(src.crop((0, 0, W, 369)))
logo = trim(logo)
logo.save(f'{A}/logo-jr.png')
print('logo-jr.png', logo.size)

# --- SEAL (so o monograma JR) : y 0..339 ---
seal = remove_bg(src.crop((0, 0, W, 287)))
seal = trim(seal)
seal.save(f'{A}/seal-jr.png')
print('seal-jr.png', seal.size)

# --- FAVICON ---
fav = pad_square(seal, 256, margin=0.06)
fav.save(f'{A}/favicon-jr.png')
print('favicon-jr.png', fav.size)

# --- OG BANNER 1200x630 navy + logo centralizado ---
og = Image.new('RGB', (1200, 630), (13, 27, 56))
# leve degrade radial fake: nada sofisticado, fundo solido navy do tema
lg = logo.copy()
sc = min(820 / lg.width, 420 / lg.height)
lg = lg.resize((int(lg.width * sc), int(lg.height * sc)), Image.LANCZOS)
og.paste(lg, ((1200 - lg.width) // 2, (630 - lg.height) // 2), lg)
og.save(f'{A}/og-banner.jpg', quality=90)
print('og-banner.jpg', og.size)

# previews de inspecao sobre fundo claro e escuro
for bg, nm in [((20, 34, 64), 'dbg-logo-dark.png'), ((244, 234, 210), 'dbg-logo-paper.png')]:
    c = Image.new('RGB', logo.size, bg)
    c.paste(logo, (0, 0), logo)
    c.save(f'C:/Users/gabri/GomesEDutra/scripts/{nm}')
print('previews ok')
