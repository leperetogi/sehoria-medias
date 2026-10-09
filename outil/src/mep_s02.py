# -*- coding: utf-8 -*-
"""Mise en page de la semaine 02 : une fonction par page. Les mots viennent de semaine02.py (seule source du texte)."""
import json
import math

import numpy as np
from PIL import Image

from composants import (numero, bandeau, texte, mono, main, feuille, carte, ruban, decoupe, logo, page, md, marquer, bloc,
                        une_phrase_par_ligne, couleur_soulignes, ASSETS)
from semaine02 import (PUBLICATIONS, CTA_MARQUE_1, CTA_MARQUE_2, CTA_ACTION, CTA_FREIN, CTA_SIGNATURE, PARTAGE)

A1 = PUBLICATIONS[0]["pages"]
A2 = PUBLICATIONS[1]["pages"]
B1 = PUBLICATIONS[2]["pages"]

VIOLET, TERRA, ENCRE, CREME = "#4120CF", "#C06B3E", "#26203A", "#FBF5EF"
PAD = 14 + 11 + 13 + 6  # marge ajoutée par le sticker (contour blanc + contour décalé)
REPERES = json.loads((ASSETS / "decoupes" / "reperes_s02.json").read_text())

# ---------------- outils ----------------

def point_decoupe(code, boite, pts, rot=0, gauche=None, haut=None, droite=None, bas=None):
    """Où tombent, sur la page, des points de l'image source après rotation, mise à l'échelle et contour (cf. decoupe())."""
    src = next((ASSETS / "decoupes").glob(code + ".*"))
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    off = (0, 0)
    if rot:
        r = im.rotate(rot, resample=Image.BICUBIC, expand=True)
        bb = r.getbbox()
        a = math.radians(rot)
        res = []
        for x, y in pts:
            dx, dy = x - W / 2, y - H / 2
            res.append((dx * math.cos(a) + dy * math.sin(a) + r.width / 2 - bb[0], -dx * math.sin(a) + dy * math.cos(a) + r.height / 2 - bb[1]))
        pts = res
        w, h = bb[2] - bb[0], bb[3] - bb[1]
    else:
        w, h = W, H
    ratio = min(boite[0] / w, boite[1] / h)
    sw, sh = round(w * ratio) + 2 * PAD, round(h * ratio) + 2 * PAD
    x0 = gauche if gauche is not None else 1080 - droite - sw
    y0 = haut if haut is not None else 1350 - bas - sh
    return [(x0 + PAD + x * ratio, y0 + PAD + y * ratio) for x, y in pts], ratio

def titre_bloc(titre, texte_html="", x=54, y=84, largeur=960, maxw_titre=790, taille=88, taille_texte=50, maxw_texte=900):
    """Titre (bandeau clair) puis texte, empilés : un titre sur deux lignes pousse le texte, sans chevauchement."""
    t = (f'<div class="texte entete-texte" style="font-size:{taille_texte}px;max-width:{maxw_texte}px">{md(texte_html)}</div>'
         if texte_html else "")
    return (f'<div class="bloc colonne" style="left:{x}px;top:{y}px;width:{largeur}px">'
            f'<div class="bandeau clair titre" style="font-size:{taille}px;--r:-1.5deg;max-width:{maxw_titre}px">{md(titre)}</div>'
            f'{t}</div>')

def au_dessus(html_bloc, z=50):
    return html_bloc.replace('class="bloc"', f'class="bloc" data-z="{z}"', 1).replace('style="', f'style="z-index:{z};', 1)

def fleche_defiler(x=70, y=1262):
    return {"t": "fleche", "de": [x, y], "a": [x + 120, y - 6], "courbe": -0.35, "c": "accent", "ep": 5, "tete": 22, "graine": 5}

def page_cta(ident, palette, fond, souligne):
    c = [
        bandeau(CTA_MARQUE_1, 52, 160, 84, r=-2, variante="clair titre"),
        texte(couleur_soulignes(marquer(CTA_MARQUE_2, "compte les ventes."), souligne), 76, 330, 92, maxw=960, classe="chute"),
        bandeau(CTA_ACTION, 58, 560, 62, r=-2, variante="titre", ident="action"),
        texte(CTA_FREIN.replace("sans engagement", "sans~engagement"), 80, 738, 44, maxw=900, couleur="#3A3350"),
        logo(342, 1000, 140),
        mono(CTA_SIGNATURE, 60, 1190, 28, couleur="#6E6782", largeur=960, align="center"),
    ]
    plan = [{"t": "fleche", "de": [930, 470], "a": [980, 560], "courbe": -0.45, "c": "accent", "ep": 5.5, "graine": 4, "tete": 28}]
    return page(ident, c, plan, palette=palette, fond=fond, miroir=True)

def lunettes_en_vrac(n, zone, graine, rmin=24, rmax=34, dmin=150):
    """n paires dessinées, posées en désordre dans zone (x0, y0, x1, y1), sans se recouvrir."""
    rng = np.random.default_rng(graine)
    x0, y0, x1, y1 = zone
    pos = []
    essais = 0
    while len(pos) < n and essais < 20000:
        essais += 1
        r = rng.uniform(rmin, rmax)
        cx, cy = rng.uniform(x0 + 2.9 * r, x1 - 2.9 * r), rng.uniform(y0 + 1.2 * r, y1 - 1.2 * r)
        if all((cx - a) ** 2 + ((cy - b) * 1.9) ** 2 > dmin ** 2 for a, b, _ in pos):
            pos.append((cx, cy, r))
    assert len(pos) == n, f"seulement {len(pos)} paires placées"
    plan = []
    for i, (cx, cy, r) in enumerate(pos):
        plan.append({"t": "lunettes", "cx": round(cx), "cy": round(cy), "r": round(r, 1), "rot": round(float(rng.uniform(-28, 28)), 1),
                     "c": "accent" if i % 4 == 0 else "encre", "ep": 4.5, "pleines": i % 5 == 2, "graine": 300 + 7 * i})
    return plan

# ============ A1 · Aider un client à choisir sa monture (violet + terracotta) ============

def a1_01():
    p = A1[0]
    boite, rot, droite, bas = (900, 1268), 2, -170, -430
    (og, od), ratio = point_decoupe("U8", boite, [REPERES["U8"]["oeil_g"], REPERES["U8"]["oeil_d"]], rot=rot, droite=droite, bas=bas)
    cx, cy = (og[0] + od[0]) / 2, (og[1] + od[1]) / 2
    ecart = math.dist(og, od)
    c = [
        decoupe("U8", boite, droite=droite, bas=bas, rot=rot, eclaircir=True),
        bandeau(p["bandeau1"], 60, 100, 66, r=-3),
        bandeau(p["titre"], 38, 194, 108, r=1.5, variante="clair geant"),
        bandeau(couleur_soulignes(p["bandeau2"], "creme"), 96, 352, 72, r=-1.5),
        main(p["main"], 78, 650, 52, r=-6, ident="bulle", maxw=230),
    ]
    plan = [
        {"t": "lunettes", "cx": round(cx, 1), "cy": round(cy, 1), "r": round(ecart / 2.68 * 1.08, 1), "rot": -rot,
         "c": "violet", "ep": 6, "graine": 41},
        {"t": "bulle", "autour": "#bulle", "queue": [round(og[0] - 70), round(og[1] + 20)], "c": "accent", "graine": 3,
         "marge": 42, "margeY": 32, "rot": -6},
        fleche_defiler(),
    ]
    return page("A1-01", c, plan, palette="terracotta", fond="papier-creme-1.png")

def a1_02():
    p = A1[1]
    c = [
        bandeau(p["texte"], 54, 92, 60, r=-1.2, variante="clair", maxw=970),
        texte(p["texte2"], 72, 958, 62, maxw=940, poids="700"),
        texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1050, 74, maxw=940, classe="chute"),
    ]
    plan = lunettes_en_vrac(15, (60, 290, 1020, 915), graine=12, rmin=28, rmax=40, dmin=172)
    return page("A1-02", c, plan, palette="terracotta", fond="papier-creme-2.png")

def a1_03():
    p = A1[2]
    c = [
        numero(p["numero"], droite=64, haut=60, taille=280),
        titre_bloc(p["titre"], maxw_titre=800, taille=90),
        decoupe("U9", (820, 640), gauche=88, haut=410, dechire=True, rot=-3),
        ruban(430, 392, r=-4, variante="terracotta"),
        texte(p["chute"], 72, 1150, 70, maxw=940, classe="chute"),
    ]
    return page("A1-03", c, [], palette="terracotta", fond="papier-creme-3.png")

def a1_04():
    p = A1[3]
    cit = (f'<div class="texte" style="font-size:44px;font-weight:600">{md(p["texte"])}</div>'
           f'<div class="texte" style="font-size:66px;font-style:italic;font-weight:700;color:#26203A;margin-top:4px;white-space:nowrap">{md(p["citation"])}</div>')
    cartes = [(70, 716, -4), (390, 694, 3), (710, 724, -2)]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], maxw_titre=780, taille=84),
         feuille(cit, 64, 400, 950, r=-1.2, padding="30px 52px 36px")]
    plan = []
    for i, (x, y, r) in enumerate(cartes):
        c.append(carte(x, y, 300, 220, r=r))
        plan.append({"t": "lunettes", "cx": x + 150, "cy": y + 116, "r": 40, "rot": r, "c": "encre", "ep": 5,
                     "pleines": i == 2, "graine": 510 + 9 * i})
    plan.append({"t": "croix", "x": 390 + 150, "y": 694 + 112, "taille": 92, "ep": 10, "c": "accent", "graine": 133})
    c.append(texte(une_phrase_par_ligne(p["chute"]), 72, 1070, 72, maxw=940, classe="chute"))
    return page("A1-04", c, plan, palette="terracotta", fond="papier-creme-4.png")

def a1_05():
    p = A1[4]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=780, taille=84, taille_texte=50, maxw_texte=920)]
    plan = [
        {"t": "visage", "cx": 268, "cy": 890, "r": 170, "lunettes": True, "flou": 9, "c": "encre", "ep": 6, "graine": 711},
        {"t": "fleche", "de": [470, 800], "a": [600, 806], "courbe": -0.3, "c": "accent", "ep": 6, "tete": 26, "graine": 12},
        {"t": "telephone", "x": 640, "y": 560, "w": 330, "h": 640, "rot": 4, "c": "encre", "graine": 812},
        {"t": "visage", "cx": 805, "cy": 860, "r": 118, "lunettes": True, "c": "encre", "clunettes": "accent", "ep": 5.5,
         "rot": 4, "graine": 712},
        {"t": "coche", "x": 870, "y": 1090, "taille": 62, "ep": 9, "graine": 113},
    ]
    return page("A1-05", c, plan, palette="terracotta", fond="papier-creme-1.png")

def a1_06():
    p = A1[5]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=780, taille=92, taille_texte=52)]
    plan = []
    for i, (x, y, r) in enumerate([(110, 560, -3), (580, 548, 3)]):
        c.append(carte(x, y, 380, 300, r=r, ident=f"choix{i}"))
        plan.append({"t": "lunettes", "cx": x + 190, "cy": y + 150, "r": 52, "rot": r, "c": "encre", "ep": 5.5,
                     "pleines": i == 1, "graine": 610 + 11 * i})
    plan += [
        {"t": "ellipse", "boite": [580, 548, 380, 300], "marge": 26, "c": "accent", "ep": 7, "graine": 19, "rot": 4},
        {"t": "coche", "x": 860, "y": 900, "taille": 70, "ep": 10, "graine": 114},
        {"t": "bulleVide", "cx": 300, "cy": 960, "w": 220, "h": 120, "queue": [360, 1046], "c": "accent", "points": True, "graine": 905},
    ]
    c.append(texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1110, 74, maxw=940, classe="chute"))
    return page("A1-06", c, plan, palette="terracotta", fond="papier-creme-2.png")

def a1_07():
    return page_cta("A1-07", "terracotta", "papier-creme-4.png", "terracotta")

# ============ A2 · La météo de l'équipe (violet + crème) ============

def a2_01():
    p = A2[0]
    c = [
        decoupe("U10", (700, 660), droite=10, haut=560, rot=-3),
        bandeau(p["bandeau1"], 60, 100, 66, r=-3),
        bandeau(p["titre"], 38, 194, 100, r=1.5, variante="clair geant"),
        bandeau(couleur_soulignes(p["bandeau2"], "creme"), 96, 344, 72, r=-1.5),
    ]
    plan = [
        {"t": "soleil", "cx": 180, "cy": 640, "r": 64, "c": "accent", "graine": 501},
        {"t": "nuage", "cx": 210, "cy": 930, "w": 260, "c": "encre", "gris": True, "pluie": 4, "graine": 601},
        fleche_defiler(),
    ]
    return page("A2-01", c, plan, palette="creme", fond="papier-creme-3.png")

def a2_02():
    p = A2[1]
    c = [
        bandeau(p["texte"], 54, 92, 56, r=-1.2, variante="clair", maxw=970),
        texte(couleur_soulignes(p["chute"], "violet"), 72, 1010, 74, maxw=940, classe="chute"),
    ]
    plan = [
        {"t": "nuage", "cx": 540, "cy": 450, "w": 500, "c": "encre", "ep": 7, "gris": True, "pluie": 6, "graine": 602},
        {"t": "visage", "cx": 560, "cy": 868, "r": 80, "sourire": False, "c": "encre", "graine": 723},
    ]
    return page("A2-02", c, plan, palette="creme", fond="papier-creme-1.png")

def a2_03():
    p = A2[2]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=800, taille=84, taille_texte=60)]
    plan = []
    cartes = [(70, 610, -4), (390, 588, 3), (710, 616, -2)]
    for i, (x, y, r) in enumerate(cartes):
        c.append(carte(x, y, 300, 300, r=r))
    plan += [
        {"t": "soleil", "cx": 220, "cy": 760, "r": 58, "graine": 511},
        {"t": "nuage", "cx": 540, "cy": 742, "w": 220, "c": "encre", "graine": 611},
        {"t": "nuage", "cx": 860, "cy": 730, "w": 220, "c": "encre", "gris": True, "pluie": 4, "graine": 612},
    ]
    c.append(texte(p["chute"], 72, 1060, 76, maxw=940, classe="chute"))
    return page("A2-03", c, plan, palette="creme", fond="papier-creme-2.png")

def a2_04():
    p = A2[3]
    c = [
        numero(p["numero"], droite=64, haut=40, taille=230),
        bandeau(p["q1"], 70, 280, 80, r=-2, variante="titre"),
        texte(une_phrase_par_ligne(p["r1"]), 74, 790, 58, maxw=420, poids="700"),
        bandeau(p["q2"], 580, 280, 80, r=1.5, variante="titre"),
        texte(p["r2"], 584, 790, 58, maxw=420, poids="700"),
    ]
    plan = [
        {"t": "nuage", "cx": 270, "cy": 545, "w": 330, "c": "encre", "gris": True, "pluie": 5, "graine": 613},
        {"t": "soleil", "cx": 790, "cy": 575, "r": 92, "graine": 512},
        {"t": "visage", "cx": 270, "cy": 1075, "r": 92, "sourire": False, "c": "encre", "graine": 724},
        {"t": "visage", "cx": 790, "cy": 1075, "r": 92, "c": "encre", "graine": 725},
    ]
    return page("A2-04", c, plan, palette="creme", fond="papier-creme-4.png")

def a2_05():
    p = A2[4]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=780, taille=96, taille_texte=56, maxw_texte=700),
         texte(couleur_soulignes(p["chute"], "violet"), 72, 1060, 76, maxw=940, classe="chute")]
    plan = [
        {"t": "visage", "cx": 300, "cy": 760, "r": 120, "sourire": False, "c": "encre", "graine": 721},
        {"t": "nuage", "cx": 250, "cy": 560, "w": 170, "c": "encre", "gris": True, "graine": 614},
        {"t": "visage", "cx": 780, "cy": 760, "r": 120, "c": "encre", "graine": 722},
        {"t": "bulleVide", "cx": 540, "cy": 640, "w": 190, "h": 110, "queue": [640, 700], "c": "accent", "points": True, "graine": 906},
    ]
    return page("A2-05", c, plan, palette="creme", fond="papier-creme-3.png")

def a2_06():
    p = A2[5]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], maxw_titre=780, taille=88),
         texte(p["chute"], 72, 1070, 70, maxw=940, classe="chute")]
    plan = [{"t": "soleil", "cx": 540, "cy": 690, "r": 110, "rayons": 12, "graine": 513}]
    for i, (x, y) in enumerate([(200, 520), (880, 520), (200, 880), (880, 880)]):
        plan.append({"t": "visage", "cx": x, "cy": y, "r": 70, "c": "encre", "ep": 4.5, "graine": 730 + i})
    return page("A2-06", c, plan, palette="creme", fond="papier-creme-1.png")

def a2_07():
    return page_cta("A2-07", "creme", "papier-creme-2.png", "violet")

# ============ B1 · La phrase qui porte ============

def b1_01():
    p = B1[0]
    phrase = f'<div class="texte" style="font-size:76px;font-weight:700;line-height:1.1;text-align:center">{md(p["phrase"])}</div>'
    chute = f'<div class="chute" style="font-size:80px;text-align:center;margin-top:34px">{md(marquer(p["chute"], "du conseil."))}</div>'
    guill = ('<div class="bloc" aria-hidden="true" style="left:465px;top:100px;width:150px;height:150px;background:#26203A;'
             'transform:rotate(-4deg);z-index:22;box-shadow:8px 8px 0 rgba(0,0,0,.18)">'
             '<div style="font:800 210px/1 Fraunces;font-variation-settings:\'opsz\' 144,\'SOFT\' 100;color:#FBF5EF;'
             'text-align:center;margin-top:-18px">«</div></div>')
    c = [
        feuille(phrase + chute, 88, 170, 904, hauteur=560, r=-2, padding="138px 48px 60px"),
        guill,
        decoupe("U11", (720, 450), gauche=170, haut=700, rot=8, contour=CREME, couleur=ENCRE, devant=True),
        mono(PARTAGE, 72, 1182, 28, couleur=CREME, maxw=250),
        logo(826, 1194, 46, "creme"),
        mono("sehoria.fr", 826, 1252, 28, couleur=CREME),
    ]
    return page("B1-01", c, [], palette="violet", fond="fond-violet.png", grille=False)

PUBLICATIONS_MEP = {
    "S02-A1": [a1_01, a1_02, a1_03, a1_04, a1_05, a1_06, a1_07],
    "S02-A2": [a2_01, a2_02, a2_03, a2_04, a2_05, a2_06, a2_07],
    "S02-B1": [b1_01],
}
