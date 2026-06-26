# -*- coding: utf-8 -*-
"""Recria o logo Gomes & Dutra de forma NITIDA (vetorial via fonte Playfair),
em vez de ampliar o screenshot de baixa resolucao. Gera:
- logo-gd.png  (monograma GD + 'Gomes' / '& Dutra' + 'ADVOCACIA') horizontal
- seal-gd.png  (so o monograma GD, quadrado) p/ navbar
- favicon-gd.png
- og-banner.jpg
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

OUT = Path(r"C:\Users\gabri\GomesEDutra\assets")
FONT = Path(__file__).resolve().parent / "fonts" / "Playfair.ttf"
GOLD = (216, 178, 92)          # dourado quente, legivel no escuro
GOLD2 = (232, 200, 120)

def pf(size, wght=600):
    f = ImageFont.truetype(str(FONT), size)
    try:
        f.set_variation_by_axes([wght])
    except Exception:
        pass
    return f

def trim(img):
    bb = img.split()[3].getbbox()
    return img.crop(bb) if bb else img

def text_img(txt, font, fill, tracking=0):
    """renderiza texto (com tracking opcional) num canvas generoso e recorta.
    Usa anchor='lt' (canto superior-esquerdo) -> previsivel, sem corte."""
    big = Image.new("RGBA", (5000, 700), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    if tracking == 0:
        d.text((30, 30), txt, font=font, fill=fill, anchor="lt")
    else:
        x = 30
        for ch in txt:
            d.text((x, 30), ch, font=font, fill=fill, anchor="lt")
            x += d.textlength(ch, font=font) + tracking
    return trim(big)

# ---------- MONOGRAMA GD ----------
def make_monogram(side=560):
    img = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # moldura retangular fina (portrait, centralizada)
    fw, fh = int(side*0.62), int(side*0.86)
    fx, fy = (side-fw)//2, (side-fh)//2
    d.rectangle([fx, fy, fx+fw, fy+fh], outline=GOLD, width=max(3, side//120))
    # G e D entrelacados
    fg = pf(int(side*0.62), 560)
    g = trim(text_img("G", fg, GOLD))
    dd = trim(text_img("D", fg, GOLD))
    # posiciona G em cima-esquerda, D embaixo-direita, sobrepostos
    gx = int(side*0.16); gy = int(side*0.14)
    img.alpha_composite(g, (gx, gy))
    dx = int(side*0.40); dy = int(side*0.40)
    img.alpha_composite(dd, (dx, dy))
    return img

mono = make_monogram(560)
seal = mono.copy()
seal.save(OUT / "seal-gd.png")
print("seal-gd.png", seal.size)
seal.resize((256, 256), Image.LANCZOS).save(OUT / "favicon-gd.png")
print("favicon-gd.png salvo")

# ---------- LOGO HORIZONTAL ----------
line1 = trim(text_img("Gomes", pf(210, 600), GOLD2))
line2 = trim(text_img("& Dutra", pf(210, 600), GOLD2))
advtxt = trim(text_img("ADVOCACIA", pf(74, 720), GOLD2, tracking=32))
# tira ADVOCACIA com reguas flanqueando (pre-composta -> alinhamento garantido)
rule_len = 120; rgap = 34
strip_w = advtxt.width + 2*(rule_len + rgap)
strip_h = advtxt.height
strip = Image.new("RGBA", (strip_w, strip_h), (0, 0, 0, 0))
strip.alpha_composite(advtxt, (rule_len + rgap, 0))
ds = ImageDraw.Draw(strip)
ry = strip_h // 2
ds.line([(0, ry), (rule_len, ry)], fill=GOLD, width=4)
ds.line([(strip_w - rule_len, ry), (strip_w, ry)], fill=GOLD, width=4)

# bloco de texto (wordmark)
gap = 18
adv_gap = 54
tw = max(line1.width, line2.width, strip.width)
th = line1.height + gap + line2.height + adv_gap + strip.height
wordmark = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
wordmark.alpha_composite(line1, (0, 0))
y2 = line1.height + gap
wordmark.alpha_composite(line2, (0, y2))
ystrip = y2 + line2.height + adv_gap
wordmark.alpha_composite(strip, ((tw - strip.width)//2, ystrip))

# monograma redimensionado p/ altura do wordmark
mh = int(th*1.02)
mono_r = mono.resize((mh, mh), Image.LANCZOS)
# compoe: [mono] espaco [wordmark]
pad = 40
space = 56
W = mono_r.width + space + wordmark.width + pad*2
H = max(mono_r.height, wordmark.height) + pad*2
logo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
logo.alpha_composite(mono_r, (pad, (H-mono_r.height)//2))
logo.alpha_composite(wordmark, (pad+mono_r.width+space, (H-wordmark.height)//2))
logo = trim(logo)
# leve respiro
canvas = Image.new("RGBA", (logo.width+60, logo.height+60), (0, 0, 0, 0))
canvas.alpha_composite(logo, (30, 30))
canvas.save(OUT / "logo-gd.png")
print("logo-gd.png", canvas.size)
# crop de checagem da base (ADVOCACIA)
cb = canvas.crop((0, int(canvas.height*0.62), canvas.width, canvas.height))
cb.save(OUT / "__advcheck.png")

# ---------- OG BANNER ----------
og = Image.new("RGB", (1200, 630), (11, 19, 34))
d = ImageDraw.Draw(og)
d.rectangle([26, 26, 1173, 603], outline=(120, 96, 44), width=2)
lw, lh = canvas.size
scale = min(820/lw, 250/lh)
lg = canvas.resize((int(lw*scale), int(lh*scale)), Image.LANCZOS)
og.paste(lg, ((1200-lg.size[0])//2, 150), lg)
tagf = pf(30, 500)
tag = text_img("Regularizacao de Imoveis  -  Familia e Sucessoes  -  Manhuacu/MG", tagf, (198, 176, 120), tracking=2)
tag = trim(tag)
ts = min(900/tag.width, 1)
tag = tag.resize((int(tag.width*ts), int(tag.height*ts)), Image.LANCZOS)
og.paste(tag, ((1200-tag.width)//2, 450), tag)
og.save(OUT / "og-banner.jpg", quality=90)
print("og-banner.jpg salvo")
print("OK")
