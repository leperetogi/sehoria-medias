# -*- coding: utf-8 -*-
"""Composants HTML du gabarit Sehoria (blocs de texte, papiers, découpes, logo) et assemblage des pages."""
import hashlib
import html
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from decoupes import sticker, hex2rgb

RACINE = Path(__file__).resolve().parent.parent
ASSETS = RACINE / "assets"
STICKERS = RACINE / "build" / "stickers"
STICKERS.mkdir(parents=True, exist_ok=True)

def url(p: Path) -> str:
    return "file://" + str(Path(p).resolve())

# ---------- texte ----------

def md(txt: str) -> str:
    """[[mot]] ou [[mot|couleur]] -> souligné à la main ; {{mot}} -> surligné ; ~ -> espace insécable."""
    t = html.escape(txt, quote=False)
    def _soul(m):
        mot, _, coul = m.group(1).partition("|")
        attr = f' data-couleur="{coul}"' if coul else ""
        return f'<span class="souligne"{attr}>{mot}</span>'
    t = re.sub(r"\[\[(.+?)\]\]", _soul, t)
    t = re.sub(r"\{\{(.+?)\}\}", r'<span class="surligne">\1</span>', t)
    t = re.sub(r"\^(\w+)", r"<sup>\1</sup>", t)
    return t.replace("~", "\u00a0").replace("\n", "<br>")

def marquer(txt: str, morceau: str, couleur: str = "") -> str:
    """Ajoute un souligné à la main sur un morceau du texte validé (sans changer les mots)."""
    assert morceau in txt, (morceau, txt)
    return txt.replace(morceau, f"[[{morceau}{'|' + couleur if couleur else ''}]]", 1)

def une_phrase_par_ligne(txt: str) -> str:
    """Met chaque phrase sur sa ligne (mêmes mots, même ponctuation)."""
    import re as _re
    return _re.sub(r"(?<=[.!?…])\s+(?=[A-ZÀ-ÖØ-Þ«])", "\n", txt)

def couleur_soulignes(txt: str, couleur: str) -> str:
    """Donne une couleur aux soulignés déjà prévus dans le texte validé ([[mot]] -> [[mot|couleur]])."""
    import re as _re
    return _re.sub(r"\[\[([^|\]]+)\]\]", lambda m: f"[[{m.group(1)}|{couleur}]]", txt)

def _style(**kw):
    return ";".join(f"{k.replace('_', '-')}:{v}" for k, v in kw.items() if v is not None)

def bloc(contenu, x, y, maxw=None, largeur=None, align=None, z=None, ident=None, extra=""):
    st = _style(left=f"{x}px", top=f"{y}px", max_width=f"{maxw}px" if maxw else None,
                width=f"{largeur}px" if largeur else None, text_align=align, z_index=z)
    i = f' id="{ident}" data-id="{ident}"' if ident else ""
    return f'<div class="bloc"{i} style="{st}{extra}">{contenu}</div>'

def bandeau(txt, x, y, taille, r=-2.0, variante="", maxw=None, ident=None, align=None):
    st = _style(font_size=f"{taille}px", **{"--r": f"{r}deg"}, max_width=f"{maxw}px" if maxw else None)
    return bloc(f'<div class="bandeau {variante}" style="{st}">{md(txt)}</div>', x, y, ident=ident, align=align)

def texte(txt, x, y, taille, maxw=None, classe="texte", r=0, align=None, ident=None, couleur=None, poids=None):
    st = _style(font_size=f"{taille}px", transform=f"rotate({r}deg)" if r else None, color=couleur, font_weight=poids)
    return bloc(f'<div class="{classe}" style="{st}">{md(txt)}</div>', x, y, maxw=maxw, align=align, ident=ident)

def mono(txt, x, y, taille=28, couleur=None, maxw=None, align=None, largeur=None, ident=None):
    st = _style(font_size=f"{taille}px", color=couleur)
    return bloc(f'<div class="mono" style="{st}">{md(txt)}</div>', x, y, maxw=maxw, align=align, largeur=largeur, ident=ident)

def pastille(txt, x, y, taille=28, r=-1.5, ident=None):
    """Petit libellé JetBrains Mono sur une bande crème (lisible posé sur une photo)."""
    st = _style(font_size=f"{taille}px", **{"--r": f"{r}deg"})
    return bloc(f'<div class="bandeau clair pastille" style="{st}">{md(txt)}</div>', x, y, ident=ident)

def main(txt, x, y, taille=54, r=-4, ident=None, couleur=None, maxw=None):
    st = _style(font_size=f"{taille}px", **{"--r": f"{r}deg"}, color=couleur)
    return bloc(f'<div class="main" style="{st}">{md(txt)}</div>', x, y, ident=ident, maxw=maxw)

def numero(n, droite=60, haut=26, taille=380, couleur=None):
    st = _style(right=f"{droite}px", top=f"{haut}px", font_size=f"{taille}px",
                **({"-webkit-text-stroke": f"5px {couleur}"} if couleur else {}))
    return f'<div class="num" aria-hidden="true" style="{st}">{n}</div>'

def entete(label, titre, texte_html="", x=54, y=84, largeur=960, maxw_titre=790):
    """Libellé + titre + texte empilés : un titre sur deux lignes pousse le texte, sans chevauchement."""
    t = f'<div class="texte entete-texte">{texte_html}</div>' if texte_html else ""
    return (f'<div class="bloc colonne" style="left:{x}px;top:{y}px;width:{largeur}px">'
            f'<div class="mono" style="font-size:28px;margin-left:18px">{md(label)}</div>'
            f'<div class="bandeau clair titre" style="font-size:92px;--r:-1.5deg;max-width:{maxw_titre}px;margin-top:34px">{md(titre)}</div>'
            f'{t}</div>')

def feuille(contenu, x, y, largeur, hauteur=None, r=-1.5, padding="44px 56px 50px", ident=None, z=None):
    st = _style(left=f"{x}px", top=f"{y}px", width=f"{largeur}px", height=f"{hauteur}px" if hauteur else None,
                padding=padding, **{"--r": f"{r}deg"}, z_index=z)
    i = f' id="{ident}" data-id="{ident}"' if ident else ""
    return f'<div class="feuille"{i} style="{st}">{contenu}</div>'

def carte(x, y, largeur, hauteur, r=2.0, ident=None, contenu=""):
    st = _style(left=f"{x}px", top=f"{y}px", width=f"{largeur}px", height=f"{hauteur}px", **{"--r": f"{r}deg"})
    i = f' id="{ident}"' if ident else ""
    return f'<div class="carte"{i} style="{st}">{contenu}</div>'

def polaroid(x, y, largeur, hauteur, r=3.0, ident=None):
    """Tirage instantané : largeur × hauteur = zone photo ; le cadre blanc (26 px, 96 px en bas) s'ajoute autour."""
    i = f' id="{ident}"' if ident else ""
    return (f'<div class="polaroid"{i} style="left:{x}px;top:{y}px;width:{largeur + 52}px;height:{hauteur + 122}px;--r:{r}deg">'
            f'<div class="photo"></div></div>')

def ruban(x, y, r=-6, variante="", largeur=170):
    return f'<div class="ruban {variante}" style="left:{x}px;top:{y}px;width:{largeur}px;--r:{r}deg"></div>'

# ---------- images ----------

def _dechirer(im: Image.Image, seed=0, amp=9) -> Image.Image:
    rng = np.random.default_rng(seed)
    w, h = im.size
    m = Image.new("L", (w, h), 0)
    pts = [(x, rng.uniform(0, amp)) for x in np.linspace(0, w, 70)]
    pts += [(w - rng.uniform(0, amp), y) for y in np.linspace(0, h, 80)]
    pts += [(x, h - rng.uniform(0, amp)) for x in np.linspace(w, 0, 70)]
    pts += [(rng.uniform(0, amp), y) for y in np.linspace(h, 0, 80)]
    ImageDraw.Draw(m).polygon(pts, fill=255)
    out = im.convert("RGBA")
    out.putalpha(m)
    return out

def decoupe(code, boite, gauche=None, haut=None, droite=None, bas=None, rot=0, contour="#FFFFFF",
            couleur="#4120CF", devant=False, dechire=False, recadrage=None, garder_couleur=False, ident=None, z=None,
            eclaircir=False):
    """Prépare la découpe à la taille d'affichage exacte (net, pas de mise à l'échelle navigateur)."""
    src = ASSETS / "decoupes" / code
    if not src.exists():
        src = next((ASSETS / "decoupes").glob(code + ".*"))
    cle = hashlib.md5(json.dumps([str(src), src.stat().st_mtime, boite, rot, contour, couleur, dechire, recadrage,
                                  garder_couleur, eclaircir]).encode()).hexdigest()[:12]
    cible = STICKERS / f"{Path(code).stem}-{cle}.png"
    if not cible.exists():
        im = Image.open(src)
        if recadrage:
            im = im.crop(recadrage)
        if dechire:
            im = _dechirer(im.convert("RGB"), seed=len(code))
        im = im.convert("RGBA")
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
            im = im.crop(im.getbbox())
        sticker(im, boite, contour=contour, couleur=couleur, garder_couleur=garder_couleur, eclaircir=eclaircir).save(cible)
    w, h = Image.open(cible).size
    st = _style(left=f"{gauche}px" if gauche is not None else None, top=f"{haut}px" if haut is not None else None,
                right=f"{droite}px" if droite is not None else None, bottom=f"{bas}px" if bas is not None else None,
                width=f"{w}px", height=f"{h}px", z_index=z)
    i = f' id="{ident}"' if ident else ""
    return f'<img class="decoupe{" devant" if devant else ""}"{i} alt="" src="{url(cible)}" style="{st}">'

def logo(x, y, hauteur, variante="couleur", ident=None):
    cible = STICKERS / f"logo-{variante}.png"
    if not cible.exists():
        im = Image.open(ASSETS / "logo-sehoria.png").convert("RGBA")
        if variante == "creme":
            a = im.split()[-1]
            im = Image.new("RGBA", im.size, hex2rgb("#FBF5EF") + (255,))
            im.putalpha(a)
        im.crop(im.getbbox()).save(cible)
    w0, h0 = Image.open(cible).size
    largeur = round(hauteur * w0 / h0)
    i = f' id="{ident}"' if ident else ""
    return f'<img class="logo"{i} alt="Sehoria" src="{url(cible)}" style="left:{x}px;top:{y}px;width:{largeur}px;height:{hauteur}px">'

# ---------- pages ----------

def page(ident, contenu, plan=None, palette="creme", fond="papier-creme-1.png", grille=True, miroir=False):
    st = f"background-image:url('{url(ASSETS / fond)}')" + (";transform:scaleX(-1)" if miroir else "")
    parties = [f'<section class="page pal-{palette}" id="{ident}">', f'<div class="fond" style="{st}"></div>']
    if grille:
        parties.append('<div class="grille"></div>')
    parties += contenu if isinstance(contenu, list) else [contenu]
    parties.append('<svg class="dessins" viewBox="0 0 1080 1350" xmlns="http://www.w3.org/2000/svg"></svg>')
    if plan:
        parties.append(f'<script type="application/json" class="plan">{json.dumps(plan, ensure_ascii=False)}</script>')
    parties.append("</section>")
    return "\n".join(parties)

def document(titre, pages, essai=False):
    g = RACINE / "gabarit"
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{html.escape(titre)}</title>
<link rel="stylesheet" href="{url(g / 'gabarit.css')}">
<script src="{url(RACINE / 'node_modules/roughjs/bundled/rough.js')}"></script>
<script src="{url(g / 'dessins.js')}"></script>
</head><body class="{'essai' if essai else ''}">
{chr(10).join(pages)}
</body></html>"""

def centres_zones(code_image, code_masque, boite, rot, gauche, haut):
    """Où tombent, sur la page, les zones d'un masque (ex. les verres) après rotation et mise à l'échelle de la découpe."""
    import cv2
    im = Image.open(ASSETS / "decoupes" / f"{code_image}.png").convert("RGBA")
    mk = Image.open(ASSETS / "decoupes" / f"{code_masque}.png").convert("L")
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        mk = mk.rotate(rot, resample=Image.NEAREST, expand=True)
        b = im.getbbox()
        im, mk = im.crop(b), mk.crop(b)
    ratio = min(boite[0] / im.width, boite[1] / im.height)
    pad = 14 + 11 + 13 + 6
    a = (np.asarray(mk) > 127).astype(np.uint8)
    n, lab, st, cent = cv2.connectedComponentsWithStats(a, 8)
    zones = []
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 500:
            continue
        cx, cy = cent[i]
        zones.append({"cx": gauche + pad + cx * ratio, "cy": haut + pad + cy * ratio,
                      "l": st[i, cv2.CC_STAT_WIDTH] * ratio, "h": st[i, cv2.CC_STAT_HEIGHT] * ratio})
    return sorted(zones, key=lambda z: z["cx"])
