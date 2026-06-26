# -*- coding: utf-8 -*-
"""Gera os assets de marca do Gomes & Dutra Advocacia a partir do screenshot da logo.
- Remove o fundo dourado (preto sobre dourado -> separavel por luminancia)
- Recolore o logo para dourado (tema escuro do template)
- Upscale LANCZOS pra ficar nitido no hero
- Extrai o monograma GD (selo) + favicon
- Gera OG banner 1200x630
- Recorta os retratos dos dois advogados
"""
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps
from pathlib import Path

SRC = Path(r"C:\Users\gabri\OneDrive\Pictures\Screenshots 1")
OUT = Path(r"C:\Users\gabri\GomesEDutra\assets")
LOGO_PNG = SRC / "Captura de tela 2026-06-26 151013.png"
GUSTAVO = SRC / "Captura de tela 2026-06-26 150943.png"
PALOMA = SRC / "Captura de tela 2026-06-26 151049.png"

GOLD = (216, 177, 78)        # dourado do template (~ --gold)
GOLD_LIGHT = (230, 200, 105)

def lum(px):
    return 0.299*px[0] + 0.587*px[1] + 0.114*px[2]

def logo_to_alpha(im, color, hi=145.0, lo=70.0):
    """preto sobre dourado -> alpha por luminancia, recolorido para `color`."""
    im = im.convert("RGB")
    w, h = im.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    src = im.load()
    dst = out.load()
    for y in range(h):
        for x in range(w):
            L = lum(src[x, y])
            if L >= hi:
                a = 0
            elif L <= lo:
                a = 255
            else:
                a = int(round((hi - L) / (hi - lo) * 255))
            dst[x, y] = (color[0], color[1], color[2], a)
    return out

def content_bbox(rgba, athresh=40):
    """bbox dos pixels com alpha > athresh."""
    a = rgba.split()[3]
    mask = a.point(lambda p: 255 if p > athresh else 0)
    return mask.getbbox()

def upscale(im, factor):
    w, h = im.size
    big = im.resize((w*factor, h*factor), Image.LANCZOS)
    return big

# ---------- 1. LOGO COMPLETO (wordmark + monograma) ----------
logo = Image.open(LOGO_PNG).convert("RGB")
alpha = logo_to_alpha(logo, GOLD)
bb = content_bbox(alpha)
print("bbox logo:", bb)
alpha = alpha.crop(bb)
# margem
pad = 14
w, h = alpha.size
canvas = Image.new("RGBA", (w + 2*pad, h + 2*pad), (0, 0, 0, 0))
canvas.paste(alpha, (pad, pad), alpha)
logo_full = upscale(canvas, 4)
# suaviza levemente os degraus do upscale
logo_full = logo_full.filter(ImageFilter.GaussianBlur(0.6))
logo_full.save(OUT / "logo-gd.png")
print("logo-gd.png", logo_full.size)

# ---------- 2. SELO = monograma GD (quadrado a esquerda) ----------
# detecta o intervalo vazio (coluna de alpha~0) entre o monograma e o wordmark
cw, ch = alpha.size
acc = alpha.split()[3].load()
col_has = []
for x in range(cw):
    s = 0
    for y in range(ch):
        if acc[x, y] > 40:
            s += 1
    col_has.append(s)
# acha o primeiro vale apos o monograma: comeca depois da 1a regiao com conteudo
gap_start = None
seen_content = False
run_empty = 0
for x in range(cw):
    if col_has[x] > 1:
        seen_content = True
        run_empty = 0
    else:
        if seen_content:
            run_empty += 1
            if run_empty >= 4:        # 4 colunas seguidas vazias = fim do monograma
                gap_start = x - run_empty + 1
                break
sq = gap_start if gap_start else int(ch * 1.1)
print("seal cut col:", sq, "of", cw)
mono = alpha.crop((0, 0, sq, ch))
mbb = content_bbox(mono)
mono = mono.crop(mbb)
mw, mh = mono.size
side = max(mw, mh) + 24
seal = Image.new("RGBA", (side, side), (0, 0, 0, 0))
seal.paste(mono, ((side-mw)//2, (side-mh)//2), mono)
seal = upscale(seal, 4).filter(ImageFilter.GaussianBlur(0.6))
seal.save(OUT / "seal-gd.png")
print("seal-gd.png", seal.size)

# ---------- 3. FAVICON ----------
fav = seal.resize((256, 256), Image.LANCZOS)
fav.save(OUT / "favicon-gd.png")
print("favicon-gd.png", fav.size)

# ---------- 4. OG BANNER 1200x630 ----------
og = Image.new("RGB", (1200, 630), (10, 10, 10))
d = ImageDraw.Draw(og)
# moldura dourada fina
d.rectangle([28, 28, 1171, 601], outline=(140, 112, 44), width=2)
# logo dourado centralizado em cima
lw, lh = logo_full.size
scale = min(760/lw, 250/lh)
lg = logo_full.resize((int(lw*scale), int(lh*scale)), Image.LANCZOS)
og.paste(lg, ((1200-lg.size[0])//2, 150), lg)
# tagline
try:
    f1 = ImageFont.truetype("georgiai.ttf", 30)
except Exception:
    f1 = ImageFont.load_default()
tag = "Regularizacao de Imoveis  -  Familia e Sucessoes  -  Manhuacu/MG"
tb = d.textbbox((0, 0), tag, font=f1)
d.text(((1200-(tb[2]-tb[0]))//2, 440), tag, fill=(200, 174, 110), font=f1)
og.save(OUT / "og-banner.jpg", quality=88)
print("og-banner.jpg saved")

# ---------- 5. RETRATOS (circulares, mascarados) ----------
def circle_portrait(path, box, name, centering, out=560):
    im = Image.open(path).convert("RGB")
    c = im.crop(box)
    c = ImageOps.fit(c, (out, out), Image.LANCZOS, centering=centering)
    # mascara circular com anel dourado fino
    mask = Image.new("L", (out*4, out*4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, out*4-1, out*4-1], fill=255)
    mask = mask.resize((out, out), Image.LANCZOS)
    res = Image.new("RGBA", (out, out), (0, 0, 0, 0))
    res.paste(c, (0, 0), mask)
    # anel dourado
    ring = Image.new("RGBA", (out*4, out*4), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([6, 6, out*4-7, out*4-7], outline=GOLD+(255,), width=10)
    ring = ring.resize((out, out), Image.LANCZOS)
    res = Image.alpha_composite(res, ring)
    res.save(OUT / name)
    print(name, "from", im.size, "box", box, "->", res.size)

# Gustavo: rosto centro-direita do card (410x395), corta moldura e fundo
circle_portrait(GUSTAVO, (150, 55, 410, 360), "socio-gustavo.png", (0.55, 0.42))
# Paloma: rosto na direita do card (377x397), evita texto a esquerda e telefone embaixo
circle_portrait(PALOMA, (150, 18, 377, 335), "socio-paloma.png", (0.55, 0.30))

print("OK")
