# -*- coding: utf-8 -*-
"""Mise en page de la semaine 03 : une fonction par page. Les mots viennent de semaine03.py (seule source du texte).
Page 1 des carrousels en deux styles : « actuel » (papier crème, bandeaux) et « affiche » (fond encre, titre géant
étroit derrière la découpe, une seule couleur vive), pour que Togi choisisse."""
import hashlib
import json
import math

import numpy as np
from PIL import Image

from composants import (numero, bandeau, texte, mono, main, feuille, carte, ruban, decoupe, logo, page, md, marquer, bloc,
                        une_phrase_par_ligne, couleur_soulignes, url, ASSETS, STICKERS)
from decoupes import gris_collage
from semaine03 import (PUBLICATIONS, CTA_MARQUE_1, CTA_MARQUE_2, CTA_ACTION, CTA_FREIN, CTA_SIGNATURE, PARTAGE)

A1 = PUBLICATIONS[0]["pages"]
A2 = PUBLICATIONS[1]["pages"]
B1 = PUBLICATIONS[2]["pages"]

VIOLET, TERRA, ENCRE, CREME = "#4120CF", "#C06B3E", "#26203A", "#FBF5EF"
PAD = 14 + 11 + 13 + 6  # marge ajoutée par le sticker (contour blanc + contour décalé)
REPERES = json.loads((ASSETS / "decoupes" / "reperes_s03.json").read_text())


# ---------------- outils ----------------

def fond_encre():
    """Fond du style affiche : encre de la charte, grain fin, halo doux derrière l'objet (généré, aucune image tierce)."""
    cible = ASSETS / "fond-encre.png"
    if not cible.exists():
        from textures import papier
        im = np.asarray(papier(1080, 1350, "#26203A", 9, force=2.2, grain_f=3.0, vignette=0.0,
                               teinte=(1.0, 0.95, 1.1))).astype(np.float32)
        yy, xx = np.mgrid[0:1350, 0:1080]
        halo = np.exp(-(((xx - 540) / 520) ** 2 + ((yy - 760) / 560) ** 2))
        bord = np.clip(np.sqrt(((xx - 540) / 760) ** 2 + ((yy - 675) / 900) ** 2) - 0.45, 0, 1)
        im = im + halo[..., None] * np.array([16, 13, 22]) - bord[..., None] * 26
        Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(cible)
    return cible.name


def placer(taille_src, boite, rot=0, gauche=None, haut=None, droite=None, bas=None, pad=0):
    """Taille affichée et coin haut-gauche d'une image (même calcul que decoupe())."""
    w, h = taille_src
    if rot:
        a = math.radians(rot)
        w, h = abs(w * math.cos(a)) + abs(h * math.sin(a)), abs(w * math.sin(a)) + abs(h * math.cos(a))
    ratio = min(boite[0] / w, boite[1] / h)
    sw, sh = round(w * ratio) + 2 * pad, round(h * ratio) + 2 * pad
    x0 = gauche if gauche is not None else 1080 - droite - sw
    y0 = haut if haut is not None else 1350 - bas - sh
    return ratio, x0, y0, sw, sh


def point(code, pts, boite, rot=0, pad=PAD, **pos):
    """Où tombent, sur la page, des points de la découpe source (après rotation, mise à l'échelle, contour)."""
    im = Image.open(ASSETS / "decoupes" / f"{code}.png").convert("RGBA")
    W, H = im.size
    if rot:
        r = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        bb = r.getbbox()
        a = math.radians(rot)
        res = []
        for x, y in pts:
            dx, dy = x - W / 2, y - H / 2
            res.append((dx * math.cos(a) + dy * math.sin(a) + r.width / 2 - bb[0],
                        -dx * math.sin(a) + dy * math.cos(a) + r.height / 2 - bb[1]))
        pts, taille = res, (bb[2] - bb[0], bb[3] - bb[1])
    else:
        taille = (W, H)
    ratio = min(boite[0] / taille[0], boite[1] / taille[1])
    sw, sh = round(taille[0] * ratio) + 2 * pad, round(taille[1] * ratio) + 2 * pad
    x0 = pos["gauche"] if pos.get("gauche") is not None else 1080 - pos["droite"] - sw
    y0 = pos["haut"] if pos.get("haut") is not None else 1350 - pos["bas"] - sh
    return [(x0 + pad + x * ratio, y0 + pad + y * ratio) for x, y in pts], ratio


def decoupe_nue(code, boite, gauche=None, haut=None, droite=None, bas=None, rot=0, degrade=0, eclaircir=False,
                contraste=1.12, gamma=0.95, ident=None, z=None):
    """Découpe noir et blanc sans contour (style affiche). degrade : fondu vers le bas, en px affichés."""
    src = ASSETS / "decoupes" / f"{code}.png"
    cle = hashlib.md5(json.dumps([str(src), src.stat().st_mtime, boite, rot, degrade, eclaircir, contraste, gamma])
                      .encode()).hexdigest()[:12]
    cible = STICKERS / f"{code}-nue-{cle}.png"
    if not cible.exists():
        im = Image.open(src).convert("RGBA")
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
            im = im.crop(im.getbbox())
        ratio = min(boite[0] / im.width, boite[1] / im.height)
        im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.LANCZOS)
        g = gris_collage(im.convert("RGB"), gamma=gamma, contraste=contraste, eclaircir=eclaircir)
        a = np.asarray(im.split()[-1]).astype(np.float32)
        if degrade:
            rampe = np.clip(np.arange(im.height)[::-1] / degrade, 0, 1) ** 1.4
            a = a * rampe[:, None]
        out = g.convert("RGBA")
        out.putalpha(Image.fromarray(a.astype(np.uint8)))
        out.save(cible)
    w, h = Image.open(cible).size
    st = ";".join(f"{k}:{v}" for k, v in {
        "left": f"{gauche}px" if gauche is not None else None, "top": f"{haut}px" if haut is not None else None,
        "right": f"{droite}px" if droite is not None else None, "bottom": f"{bas}px" if bas is not None else None,
        "width": f"{w}px", "height": f"{h}px", "z-index": z}.items() if v is not None)
    i = f' id="{ident}"' if ident else ""
    return f'<img class="decoupe nue"{i} alt="" src="{url(cible)}" style="{st}">'


def geant(lignes, x, y, z=6, couleur=None, ident=None, interligne=0.84):
    """Titre géant Anton, une taille par ligne (chaque ligne remplit la même largeur) ; z bas : il passe derrière."""
    html = "".join(f'<div class="geant-affiche" style="font-size:{t}px;line-height:{interligne}' +
                   (f';color:{couleur}' if couleur else "") + f'">{md(m)}</div>' for m, t in lignes)
    i = f' id="{ident}" data-id="{ident}"' if ident else ""
    return f'<div class="bloc"{i} style="left:{x}px;top:{y}px;z-index:{z}">{html}</div>'


def fleche_defiler(x=70, y=1262, c="accent"):
    return {"t": "fleche", "de": [x, y], "a": [x + 120, y - 6], "courbe": -0.35, "c": c, "ep": 5, "tete": 22, "graine": 5}


def lunettes_sur(code, boite, rot, c, ep, graine, pad=PAD, **pos):
    (og, od), _ = point(code, [REPERES[code]["oeil_g"], REPERES[code]["oeil_d"]], boite, rot=rot, pad=pad, **pos)
    cx, cy = (og[0] + od[0]) / 2, (og[1] + od[1]) / 2
    ecart = math.dist(og, od)
    incl = math.degrees(math.atan2(od[1] - og[1], od[0] - og[0]))
    return {"t": "lunettes", "cx": round(cx, 1), "cy": round(cy, 1), "r": round(ecart / 2.68 * 1.12, 1),
            "rot": round(incl, 1), "c": c, "ep": ep, "graine": graine}


# ============ A1 · Une option se propose avec une question ============

def a1_01_actuel():
    """Style actuel (violet + crème) : buste découpé à droite, lunettes dessinées, bulle « Non merci. »."""
    p = A1[0]
    boite, rot, pos = (780, 980), 0, {"droite": -70, "bas": -190}
    (bouche,), _ = point("U12", [REPERES["U12"]["bouche"]], boite, rot=rot, **pos)
    c = [
        decoupe("U12", boite, rot=rot, **pos),
        bandeau(p["titre"], 40, 96, 96, r=1.2, variante="clair geant", maxw=960),
        bandeau(p["bandeau"], 70, 356, 54, r=-1.6, maxw=760),
        main(p["bulle"], 92, 780, 66, r=-5, ident="bulle", maxw=300),
    ]
    plan = [
        lunettes_sur("U12", boite, rot, "violet", 6, 41, **pos),
        {"t": "bulle", "autour": "#bulle", "queue": [round(bouche[0] - 40), round(bouche[1])], "c": "accent", "graine": 3,
         "marge": 44, "margeY": 34, "rot": -5},
        fleche_defiler(),
    ]
    return page("A1-01a", c, plan, palette="creme", fond="papier-creme-2.png")


def a1_01_affiche():
    """Style affiche : « NON MERCI. » géant derrière le buste, fond encre, terracotta seule couleur vive."""
    p = A1[0]
    boite, pos = (980, 1150), {"gauche": 40, "bas": -600}
    c = [
        texte(couleur_soulignes(p["titre"], "terracotta"), 56, 78, 66, maxw=820, classe="affiche-texte"),
        mono("01/07", 60, 1268, 28),
        geant([(p["bulle"].split()[0].upper(), 452), (p["bulle"].split()[1].upper(), 287)], 50, 252, z=6),
        decoupe_nue("U12", boite, z=10, **pos),
        bandeau(p["bandeau"], 56, 1128, 50, r=-1.5, maxw=820),
    ]
    plan = [lunettes_sur("U12", boite, 0, "terracotta", 7, 42, pad=0, **pos),
            fleche_defiler(900, 1290)]
    return page("A1-01b", c, plan, palette="affiche", fond=fond_encre(), grille=False)


# ============ A2 · Le samedi se prépare le vendredi ============

def a2_01_actuel():
    """Style actuel (violet + terracotta) : cadran découpé, note à la main « 19 h, on prépare… »."""
    p = A2[0]
    boite, rot, pos = (600, 760), -6, {"droite": 30, "haut": 470}
    (centre,), _ = point("U13", [REPERES["U13"]["centre"]], boite, rot=rot, **pos)
    c = [
        decoupe("U13", boite, rot=rot, contour=CREME, couleur=TERRA, **pos),
        bandeau(couleur_soulignes(p["titre"], "terracotta"), 40, 100, 104, r=1.2, variante="clair geant", maxw=980),
        main(p["main"], 70, 760, 72, r=-6, ident="note", maxw=360),
    ]
    plan = [
        {"t": "fleche", "de": [300, 930], "a": [round(centre[0] - 250), round(centre[1] + 40)], "courbe": 0.35,
         "c": "accent", "ep": 6, "tete": 26, "graine": 31},
        fleche_defiler(),
    ]
    return page("A2-01a", c, plan, palette="terracotta", fond="papier-creme-3.png")


def a2_01_affiche():
    """Style affiche : « VENDREDI SOIR. » géant derrière le cadran."""
    p = A2[0]
    debut, fin = p["titre"].split("[[")
    fin = fin.replace("]]", "")
    boite, rot, pos = (540, 680), -5, {"gauche": 450, "haut": 560}
    (centre,), _ = point("U13", [REPERES["U13"]["centre"]], boite, rot=rot, pad=0, **pos)
    mots = fin.rstrip(".").split()
    c = [
        texte(debut.strip(), 56, 84, 76, maxw=990, classe="affiche-texte"),
        mono("01/07", 60, 1268, 28),
        geant([(mots[0].upper(), 192), (mots[1].upper() + ".", 388)], 50, 214, z=6),
        decoupe_nue("U13", boite, rot=rot, z=10, **pos),
        main(p["main"], 70, 900, 70, r=-6, ident="note", maxw=360),
    ]
    plan = [
        {"t": "fleche", "de": [300, 1104], "a": [round(centre[0] - 270), round(centre[1] + 90)], "courbe": 0.35,
         "c": "accent", "ep": 6, "tete": 26, "graine": 32},
        fleche_defiler(900, 1290),
    ]
    return page("A2-01b", c, plan, palette="affiche", fond=fond_encre(), grille=False)


ESSAI_PAGE1 = [a1_01_actuel, a1_01_affiche, a2_01_actuel, a2_01_affiche]
