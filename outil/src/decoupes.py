# -*- coding: utf-8 -*-
"""Découpes « collage » : noir et blanc, contour blanc épais, contour de couleur décalé.
Sert aux photos détourées (rembg) et, pour l'essai du gabarit, à des silhouettes de remplacement."""
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageOps, ImageFont, ImageFilter
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FONT_MONO = RACINE / "fonts" / "JetBrainsMono.ttf"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def _dilate_aa(mask01: np.ndarray, rayon: float) -> np.ndarray:
    """Dilatation circulaire anti-crénelée par transformée de distance."""
    bin_ = (mask01 > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(1 - bin_, cv2.DIST_L2, 5)
    return np.clip(rayon + 0.5 - dist, 0, 1)

def gris_collage(rgb: Image.Image, gamma=0.95, contraste=1.12, eclaircir=False) -> Image.Image:
    g = ImageOps.grayscale(rgb)
    if eclaircir:  # contre-jour : contraste local (CLAHE) puis gamma, pour faire ressortir visage et modelé
        cl = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(np.asarray(g))
        g = Image.fromarray(((cl.astype(np.float32) / 255.0) ** 0.7 * 255).astype(np.uint8), "L")
    g = ImageOps.autocontrast(g, cutoff=1)
    a = np.asarray(g).astype(np.float32) / 255.0
    a = np.clip((a - 0.5) * contraste + 0.5, 0, 1) ** gamma
    return Image.fromarray((a * 255).astype(np.uint8), "L")

def sticker(rgba: Image.Image, boite, blanc=14, couleur_ep=11, decal=(13, 13), couleur="#4120CF",
            contour="#FFFFFF", garder_couleur=False, eclaircir=False) -> Image.Image:
    """rgba : image détourée (canal alpha). boite : (largeur, hauteur) max de l'image hors contour."""
    rgba = rgba.convert("RGBA")
    bw, bh = boite
    ratio = min(bw / rgba.width, bh / rgba.height)
    taille = (max(1, round(rgba.width * ratio)), max(1, round(rgba.height * ratio)))
    rgba = rgba.resize(taille, Image.LANCZOS)
    alpha = np.asarray(rgba.split()[-1]).astype(np.float32) / 255.0
    corps = rgba.convert("RGB") if garder_couleur else gris_collage(rgba.convert("RGB"), eclaircir=eclaircir).convert("RGB")
    pad = blanc + couleur_ep + max(abs(decal[0]), abs(decal[1])) + 6
    W, H = taille[0] + 2 * pad, taille[1] + 2 * pad
    A = np.zeros((H, W), np.float32)
    A[pad:pad + taille[1], pad:pad + taille[0]] = alpha
    m_blanc = _dilate_aa(A, blanc)
    m_coul = _dilate_aa(A, blanc + couleur_ep)
    m_coul = np.roll(np.roll(m_coul, decal[1], axis=0), decal[0], axis=1)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c = Image.new("RGBA", (W, H), hex2rgb(couleur) + (255,))
    out.paste(c, (0, 0), Image.fromarray((m_coul * 255).astype(np.uint8), "L"))
    b = Image.new("RGBA", (W, H), hex2rgb(contour) + (255,))
    out.paste(b, (0, 0), Image.fromarray((m_blanc * 255).astype(np.uint8), "L"))
    corps_rgba = corps.convert("RGBA")
    corps_rgba.putalpha(Image.fromarray((alpha * 255).astype(np.uint8), "L"))
    out.alpha_composite(corps_rgba, (pad, pad))
    return out

# ---------- silhouettes de remplacement (essai du gabarit uniquement) ----------

def _police_mono(taille):
    if not FONT_MONO.exists():
        from fontTools.ttLib import TTFont
        f = TTFont(RACINE / "node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2")
        f.flavor = None
        FONT_MONO.parent.mkdir(exist_ok=True)
        f.save(FONT_MONO)
    return ImageFont.truetype(str(FONT_MONO), taille)

def _trame(w, h, fonce=70, clair=150, pas=9, seed=0):
    """Fond gris tramé (demi-teinte) pour évoquer une photo imprimée."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    grad = (yy / h) * 0.55 + (xx / w) * 0.25 + rng.normal(0, 0.02, (h, w))
    base = fonce + (clair - fonce) * np.clip(grad, 0, 1)
    points = (np.sin(xx * np.pi / pas) * np.sin(yy * np.pi / pas)) * 10
    return Image.fromarray(np.clip(base + points, 0, 255).astype(np.uint8), "L")

def remplacement_rect(w, h, texte, seed=0):
    g = _trame(w, h, seed=seed).convert("RGBA")
    d = ImageDraw.Draw(g)
    f = _police_mono(30)
    for i, ligne in enumerate(texte.split("\n")):
        tw = d.textlength(ligne, font=f)
        d.text(((w - tw) / 2, h / 2 - 34 + i * 44), ligne, font=f, fill=(250, 250, 250, 255))
    # bord déchiré léger
    m = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(m)
    rng = np.random.default_rng(seed + 3)
    pts = []
    for x in np.linspace(0, w, 40): pts.append((x, rng.uniform(0, 7)))
    for y in np.linspace(0, h, 50): pts.append((w - rng.uniform(0, 7), y))
    for x in np.linspace(w, 0, 40): pts.append((x, h - rng.uniform(0, 7)))
    for y in np.linspace(h, 0, 50): pts.append((rng.uniform(0, 7), y))
    md.polygon(pts, fill=255)
    g.putalpha(m)
    return g

def remplacement_lunettes(w=1400):
    S = 2
    W, H = w * S, int(w * 0.46) * S
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ep = int(W * 0.022)
    lw, lh = int(W * 0.36), int(H * 0.62)
    y0 = int(H * 0.30)
    gx = int(W * 0.08)
    dx = W - gx - lw
    fonce = (34, 32, 40, 255)
    verre = (190, 190, 196, 150)
    for x in (gx, dx):
        d.rounded_rectangle([x, y0, x + lw, y0 + lh], radius=int(lh * 0.42), fill=verre, outline=fonce, width=ep)
    # pont
    d.arc([gx + lw - ep, y0 + int(lh * 0.05), dx + ep, y0 + int(lh * 0.55)], start=200, end=340, fill=fonce, width=ep)
    # branches (en perspective)
    d.line([(gx + ep // 2, y0 + int(lh * 0.18)), (int(W * 0.01), int(H * 0.05))], fill=fonce, width=int(ep * 0.8))
    d.line([(dx + lw - ep // 2, y0 + int(lh * 0.18)), (int(W * 0.99), int(H * 0.05))], fill=fonce, width=int(ep * 0.8))
    img = img.resize((w, H // S), Image.LANCZOS)
    return img

def remplacement_tour(h=1500):
    S = 2
    H = h * S
    W = int(H * 0.44)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2
    k = 3.54
    def hw(yf):  # demi-largeur en fonction de la hauteur relative (0 = sol)
        return 0.19 * H * np.exp(-k * yf)
    ys = np.linspace(0, 0.86, 120)
    droite = [(cx + hw(y), H - y * H) for y in ys]
    gauche = [(cx - hw(y), H - y * H) for y in ys[::-1]]
    sommet = [(cx + 0.004 * H, H - 0.86 * H), (cx + 0.003 * H, H - 0.985 * H), (cx, H - H + 2),
              (cx - 0.003 * H, H - 0.985 * H), (cx - 0.004 * H, H - 0.86 * H)]
    contour = droite + sommet[1:4] + gauche
    d.polygon(contour, fill=(52, 50, 58, 255))
    # arche entre les piles
    arche = []
    for t in np.linspace(0, np.pi, 60):
        arche.append((cx + 0.125 * H * np.cos(t), H - 0.125 * H * np.sin(t) * 1.0))
    d.polygon(arche, fill=(0, 0, 0, 0))
    # plateformes
    for yf, demi, ep in ((0.175, 0.125, 0.018), (0.35, 0.062, 0.014), (0.845, 0.02, 0.018)):
        d.rectangle([cx - demi * H, H - (yf + ep) * H, cx + demi * H, H - yf * H], fill=(40, 38, 46, 255))
    # treillis
    lat = Image.new("L", (W, H), 0)
    ld = ImageDraw.Draw(lat)
    pas = int(H * 0.018)
    for x in range(-H, W + H, pas):
        ld.line([(x, 0), (x + H, H)], fill=110, width=3)
        ld.line([(x, H), (x + H, 0)], fill=110, width=3)
    masque = img.split()[-1]
    trait = Image.new("RGBA", (W, H), (120, 118, 126, 255))
    trait.putalpha(Image.fromarray(np.minimum(np.asarray(lat), np.asarray(masque)).astype(np.uint8)))
    img.alpha_composite(trait)
    img = img.resize((W // S, h), Image.LANCZOS)
    return img

if __name__ == "__main__":
    out = RACINE / "assets" / "essai"
    out.mkdir(parents=True, exist_ok=True)
    remplacement_rect(620, 860, "PHOTO U1\nLE PENSEUR", seed=1).save(out / "U1.png")
    remplacement_lunettes().save(out / "U2.png")
    remplacement_tour().save(out / "U7.png")
    print("ok")
