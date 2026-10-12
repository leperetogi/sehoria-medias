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
    src = ASSETS / "decoupes" / f"{code}.png"
    if not src.exists():
        src = next((ASSETS / "decoupes").glob(code + ".*"))
    im = Image.open(src).convert("RGBA")
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
    """Style actuel (violet + terracotta) : cadran découpé, note à la main « 18 h, on prépare… »."""
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
    """Style affiche : « VENDREDI SOIR. » géant, la pendule en dessous : les deux mots se lisent en entier (Togi, 12/10)."""
    p = A2[0]
    debut, fin = p["titre"].split("[[")
    fin = fin.replace("]]", "")
    boite, rot, pos = (450, 480), -5, {"gauche": 560, "haut": 800}
    (centre,), _ = point("U13", [REPERES["U13"]["centre"]], boite, rot=rot, pad=0, **pos)
    mots = fin.rstrip(".").split()
    c = [
        texte(debut.strip(), 56, 84, 76, maxw=990, classe="affiche-texte"),
        mono("01/07", 60, 1268, 28),
        geant([(mots[0].upper(), 230), (mots[1].upper() + ".", 465)], 50, 210, z=6),
        decoupe_nue("U13", boite, rot=rot, z=10, **pos),
        main(p["main"], 70, 930, 70, r=-6, ident="note", maxw=360),
    ]
    plan = [
        {"t": "fleche", "de": [300, 1134], "a": [round(centre[0] - 225), round(centre[1] + 50)], "courbe": 0.35,
         "c": "accent", "ep": 6, "tete": 26, "graine": 32},
        fleche_defiler(900, 1290),
    ]
    return page("A2-01b", c, plan, palette="affiche", fond=fond_encre(), grille=False)



# ---------------- pages communes ----------------

def titre_bloc(titre, texte_html="", x=54, y=84, largeur=960, maxw_titre=790, taille=88, taille_texte=50, maxw_texte=900):
    """Titre (bandeau clair) puis texte, empilés : un titre sur deux lignes pousse le texte, sans chevauchement."""
    t = (f'<div class="texte entete-texte" style="font-size:{taille_texte}px;max-width:{maxw_texte}px">{md(texte_html)}</div>'
         if texte_html else "")
    return (f'<div class="bloc colonne" style="left:{x}px;top:{y}px;width:{largeur}px">'
            f'<div class="bandeau clair titre" style="font-size:{taille}px;--r:-1.5deg;max-width:{maxw_titre}px">{md(titre)}</div>'
            f'{t}</div>')


def citation_feuille(citation, x=64, y=120, largeur=950, taille=70, r=-1.2):
    cit = f'<div class="texte" style="font-size:{taille}px;font-style:italic;font-weight:700;color:#26203A">{md(citation)}</div>'
    return feuille(cit, x, y, largeur, r=r, padding="34px 52px 40px")


def page_cta(ident, palette, fond, souligne, ligne1=CTA_MARQUE_1, ligne2=CTA_MARQUE_2, a_souligner="compte les ventes."):
    """Dernière page : accroche de marque (ou phrase de pont), une seule action, le frein, la signature (charte §3)."""
    c = [
        bandeau(ligne1, 52, 160, 80 if len(ligne1) > 30 else 84, r=-2, variante="clair titre", maxw=980),
        texte(couleur_soulignes(marquer(ligne2, a_souligner), souligne), 76, 380, 92, maxw=960, classe="chute"),
        bandeau(CTA_ACTION, 58, 590, 62, r=-2, variante="titre", ident="action"),
        texte(CTA_FREIN.replace("sans engagement", "sans~engagement"), 80, 768, 44, maxw=900, couleur="#3A3350"),
        logo(342, 1010, 140),
        mono(CTA_SIGNATURE, 60, 1196, 28, couleur="#6E6782", largeur=960, align="center"),
    ]
    plan = [{"t": "fleche", "de": [930, 500], "a": [980, 590], "courbe": -0.45, "c": "accent", "ep": 5.5, "graine": 4, "tete": 28}]
    return page(ident, c, plan, palette=palette, fond=fond, miroir=True)


# ============ A1 · Une option se propose avec une question (violet + crème) ============

def a1_02():
    """Le problème, qui accroche seul : le dialogue que tout opticien a déjà entendu ; l'étiquette de prix qui pend."""
    p = A1[1]
    c = [
        texte(p["citation1"], 130, 150, 58, maxw=520, ident="q1", poids="700"),
        decoupe("U15", (230, 560), gauche=815, haut=-170, rot=-7, recadrage=(0, 350, 246, 1147)),
        texte(p["citation2"].replace(" ", "~"), 470, 470, 76, ident="q2", classe="chute"),
        texte(p["texte"], 72, 880, 54, maxw=940),
        texte(couleur_soulignes(p["chute"], "violet"), 72, 1050, 76, maxw=940, classe="chute"),
    ]
    plan = [
        {"t": "bulle", "autour": "#q1", "queue": [230, 480], "c": "encre", "graine": 11, "marge": 74, "margeY": 58, "rot": -3},
        {"t": "visage", "cx": 220, "cy": 610, "r": 100, "c": "encre", "graine": 731},
        {"t": "bulle", "autour": "#q2", "queue": [800, 660], "c": "accent", "graine": 12, "marge": 64, "margeY": 48, "rot": 3},
        {"t": "visage", "cx": 840, "cy": 750, "r": 86, "sourire": False, "lunettes": True, "c": "encre", "graine": 732},
    ]
    return page("A1-02", c, plan, palette="creme", fond="papier-creme-1.png")


def a1_03():
    p = A1[2]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=800, taille=88, taille_texte=58),
         main("?", 752, 630, 210, r=6, ident="question"),
         texte(couleur_soulignes(p["chute"], "violet"), 72, 1076, 76, maxw=940, classe="chute")]
    plan = [
        {"t": "bulleVide", "cx": 265, "cy": 770, "w": 380, "h": 220, "queue": [190, 920], "c": "encre", "points": True, "graine": 907},
        {"t": "croix", "x": 265, "y": 770, "taille": 120, "ep": 11, "c": "accent", "graine": 135},
        {"t": "fleche", "de": [480, 760], "a": [590, 760], "courbe": -0.25, "c": "accent", "ep": 6, "tete": 26, "graine": 14},
        {"t": "bulleVide", "cx": 805, "cy": 770, "w": 380, "h": 220, "queue": [880, 920], "c": "accent", "graine": 908},
    ]
    return page("A1-03", c, plan, palette="creme", fond="papier-creme-3.png")


def a1_valeur(ident, p, fond, images=(), dessin=(), y_texte=960, y_chute=1060):
    """Pages 4 à 6 : la question à poser (feuille), la photo de la situation, ce qu'on dit ensuite."""
    c = [numero(p["numero"], droite=64, haut=18, taille=220),
         citation_feuille(p["citation"], y=236, taille=72), *images,
         texte(p["texte"], 72, y_texte, 56, maxw=940, poids="600")]
    if p.get("chute"):
        c.append(texte(couleur_soulignes(p["chute"], "violet"), 72, y_chute, 78, maxw=940, classe="chute"))
    return page(ident, c, list(dessin), palette="creme", fond=fond)


def a1_04():
    """« Vous conduisez la nuit ? » : la route mouillée, les reflets des lampadaires."""
    images = [decoupe("U16", (860, 380), gauche=86, haut=528, rot=-2, dechire=True, recadrage=(0, 250, 1600, 1000)),
              ruban(440, 528, r=-5)]
    return a1_valeur("A1-04", A1[3], "papier-creme-4.png", images, y_texte=1046)


def a1_05():
    """« Vous êtes souvent dehors ? » : le soleil (photo) au-dessus du verre qui fonce."""
    images = [decoupe("U17", (280, 280), droite=80, haut=530)]
    cx, cy, r = 1080 - 80 - (280 + 2 * PAD) + PAD + 140, 530 + PAD + 140, 140
    rayons = [{"t": "fleche", "de": [round(cx + math.cos(a) * (r + 40)), round(cy + math.sin(a) * (r + 40))],
               "a": [round(cx + math.cos(a) * (r + (66 if i % 2 else 80))), round(cy + math.sin(a) * (r + (66 if i % 2 else 80)))],
               "courbe": 0, "c": "accent", "ep": 6, "tete": 0.1, "graine": 300 + i}
              for i, a in enumerate(math.radians(-90 + k * 30) for k in range(12))]
    dessin = rayons + [
        {"t": "icone", "nom": "photochromique", "sansSoleil": True, "x": 60, "y": 540, "w": 520, "c": "encre", "ep": 7,
         "graine": 562},
        {"t": "fleche", "de": [628, 905], "a": [540, 888], "courbe": 0.3, "c": "accent", "ep": 6, "tete": 22, "graine": 19},
    ]
    return a1_valeur("A1-05", A1[4], "papier-creme-2.png", images, dessin)


def a1_06():
    """« Et au soleil, vous mettez quoi ? » : la paire de tous les jours (dessin), la paire de soleil (photo) entourée."""
    boite, pos = (520, 260), {"gauche": 420, "haut": 528}
    _, ratio = point("U18", [(0, 0)], boite, **pos)
    im = Image.open(ASSETS / "decoupes" / "U18.png")
    w, h = round(im.width * ratio), round(im.height * ratio)
    images = [decoupe("U18", boite, **pos)]
    dessin = [
        {"t": "lunettes", "cx": 220, "cy": 640, "r": 56, "rot": -6, "c": "encre", "ep": 6, "graine": 451},
        {"t": "fleche", "de": [330, 700], "a": [430, 720], "courbe": -0.3, "c": "accent", "ep": 6, "tete": 24, "graine": 20},
        {"t": "ellipse", "boite": [pos["gauche"] + PAD, pos["haut"] + PAD, w, h], "marge": 26, "c": "accent", "ep": 7,
         "graine": 23, "rot": 3},
    ]
    return a1_valeur("A1-06", A1[5], "papier-creme-1.png", images, dessin, y_texte=910)


def a1_07():
    p = A1[6]
    return page_cta("A1-07", "creme", "papier-creme-3.png", "violet", ligne1=p["pont1"], ligne2=p["pont2"])


# ============ A2 · Le samedi se prépare le vendredi (violet + terracotta) ============

def a2_02():
    """Le problème : samedi matin, tout arrive en même temps (le téléphone en photo, le reste dessiné)."""
    p = A2[1]
    boite, pos = (430, 312), {"gauche": 70, "haut": 596}
    sonne, _ = point("U19", [(1240, 60), (1290, 230), (1250, 400)], boite, **pos)
    c = [
        bandeau(p["texte"], 54, 92, 54, r=-1.2, variante="clair", maxw=970),
        decoupe("U19", boite, contour="#FFFFFF", couleur=TERRA, **pos),
        main("?", 790, 560, 200, r=8, ident="cherche"),
        texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1040, 76, maxw=940, classe="chute"),
    ]
    plan = [
        {"t": "visage", "cx": 150, "cy": 440, "r": 74, "sourire": False, "c": "encre", "graine": 741},
        {"t": "visage", "cx": 310, "cy": 480, "r": 74, "sourire": False, "lunettes": True, "c": "encre", "graine": 742},
        {"t": "visage", "cx": 470, "cy": 440, "r": 74, "sourire": False, "c": "encre", "graine": 743},
    ]
    for i, ((x, y), (dx, dy)) in enumerate(zip(sonne, [(44, -26), (54, 0), (44, 26)])):
        plan.append({"t": "fleche", "de": [round(x + 14), round(y)], "a": [round(x + 14 + dx), round(y + dy)], "courbe": 0,
                     "c": "accent", "ep": 5, "tete": 0.1, "graine": 15 + i})
    plan += [
        {"t": "lunettes", "cx": 700, "cy": 880, "r": 34, "rot": -18, "c": "encre", "ep": 4.5, "graine": 431},
        {"t": "lunettes", "cx": 850, "cy": 950, "r": 30, "rot": 22, "c": "encre", "ep": 4.5, "graine": 432},
        {"t": "lunettes", "cx": 960, "cy": 860, "r": 28, "rot": -6, "c": "accent", "ep": 4.5, "graine": 433},
    ]
    return page("A2-02", c, plan, palette="terracotta", fond="papier-creme-2.png")


def a2_03():
    """Les lunettes prêtes : la paire rangée dans son étui (photo), cochée."""
    p = A2[2]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=820, taille=86, taille_texte=60),
         decoupe("U20", (560, 410), gauche=210, haut=650, rot=-3, contour="#FFFFFF", couleur=TERRA)]
    plan = [{"t": "coche", "x": 790, "y": 1010, "taille": 140, "ep": 13, "graine": 150}]
    return page("A2-03", c, plan, palette="terracotta", fond="papier-creme-4.png")


def a2_04():
    """Le planning affiché : la feuille punaisée (photo), qui fait quoi dessiné dessus."""
    p = A2[3]
    boite, pos = (700, 480), {"gauche": 150, "haut": 500}
    x0, y0, x1, y1 = REPERES["U21"]["feuille"]
    (a, b), ratio = point("U21", [(x0, y0), (x1, y1)], boite, **pos)
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=780, taille=86, taille_texte=52, maxw_texte=920),
         decoupe("U21", boite, rot=0, dechire=True, contour="#FFFFFF", couleur=TERRA, **pos),
         texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1090, 76, maxw=940, classe="chute")]
    lw, lh = b[0] - a[0], b[1] - a[1]
    plan = []
    for i in range(3):
        y = a[1] + lh * (0.36 + i * 0.22)
        plan.append({"t": "visage", "cx": round(a[0] + lw * 0.2), "cy": round(y), "r": round(lw * 0.085), "c": "encre",
                     "ep": 4, "graine": 750 + i})
        plan.append({"t": "ecriture", "boite": [round(a[0] + lw * 0.34), round(y - lw * 0.07), round(lw * 0.56),
                                                 round(lw * 0.13)], "lignes": 1, "c": "encre", "ep": 4, "graine": 70 + i,
                     "rot": -2})
    plan.append({"t": "ecriture", "boite": [round(a[0] + lw * 0.3), round(a[1] + lh * 0.15), round(lw * 0.5),
                                             round(lw * 0.12)], "lignes": 1, "c": "accent", "ep": 6, "graine": 69, "rot": -2})
    return page("A2-04", c, plan, palette="terracotta", fond="papier-creme-1.png")


def a2_05():
    """La table de vente prête : étui et lunettes (photo), la chamoisine et le cordon dessinés à côté."""
    p = A2[4]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=780, taille=88, taille_texte=56, maxw_texte=920),
         carte(70, 620, 940, 400, r=1.5, ident="table"),
         decoupe("U22", (360, 360), gauche=84, haut=590, rot=-8, contour="#FFFFFF", couleur=TERRA, devant=True),
         texte(p["chute"], 72, 1090, 70, maxw=940, classe="chute")]
    plan = [
        {"t": "chamoisine", "x": 540, "y": 700, "w": 200, "h": 190, "rot": -9, "c": "accent", "graine": 601},
        {"t": "cordon", "cx": 870, "cy": 720, "r": 36, "chute": 200, "rot": 4, "c": "accent", "lunettes": "encre", "graine": 621},
    ]
    return page("A2-05", c, plan, palette="terracotta", fond="papier-creme-3.png")


def a2_06():
    """La vitrine : les montures en présentoir (photo), celle qu'on change entourée."""
    p = A2[5]
    boite, rot, pos = (940, 330), -1.5, {"gauche": 26, "haut": 462}
    (a, b), _ = point("U23", [(990, 95), (1625, 335)], boite, rot=rot, **pos)
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], maxw_titre=820, taille=80),
         decoupe("U23", boite, rot=rot, dechire=True, contour="#FFFFFF", couleur=TERRA, **pos),
         texte(p["chute"], 72, 904, 66, maxw=940, classe="chute"),
         bandeau(p["bulle"], 300, 1090, 50, r=-2.5, variante="titre", maxw=700, ident="commentez")]
    plan = [
        {"t": "ellipse", "boite": [round(a[0]), round(min(a[1], b[1]) - 6), round(b[0] - a[0]), round(abs(b[1] - a[1]) + 12)],
         "marge": 22, "c": "accent", "ep": 7, "graine": 24, "rot": -2},
        {"t": "fleche", "de": [960, 360], "a": [round((a[0] + b[0]) / 2 + 120), round(min(a[1], b[1]) - 30)], "courbe": -0.4,
         "c": "accent", "ep": 6, "tete": 26, "graine": 18},
        {"t": "presse", "x": 110, "y": 1080, "w": 150, "h": 190, "rot": -6, "graine": 92},
    ]
    return page("A2-06", c, plan, palette="terracotta", fond="papier-creme-2.png")


def a2_07():
    return page_cta("A2-07", "terracotta", "papier-creme-4.png", "terracotta")


# ============ B1 · La phrase qui porte ============

def b1_01():
    p = B1[0]
    phrase = f'<div class="texte" style="font-size:70px;font-weight:700;line-height:1.1;text-align:center">{md(p["phrase"])}</div>'
    chute = f'<div class="chute" style="font-size:80px;text-align:center;margin-top:30px">{md(marquer(p["chute"], "d’un bonjour."))}</div>'
    guill = ('<div class="bloc" aria-hidden="true" style="left:465px;top:100px;width:150px;height:150px;background:#26203A;'
             'transform:rotate(-4deg);z-index:22;box-shadow:8px 8px 0 rgba(0,0,0,.18)">'
             '<div style="font:800 210px/1 Fraunces;font-variation-settings:\'opsz\' 144,\'SOFT\' 100;color:#FBF5EF;'
             'text-align:center;margin-top:-18px">«</div></div>')
    c = [
        feuille(phrase + chute, 88, 170, 904, hauteur=600, r=-2, padding="130px 52px 56px"),
        guill,
        decoupe("U14", (520, 560), gauche=300, haut=690, rot=4, contour=CREME, couleur=ENCRE, devant=True),
        mono(PARTAGE, 72, 1182, 28, couleur=CREME, maxw=250),
        logo(826, 1194, 46, "creme"),
        mono("sehoria.fr", 826, 1252, 28, couleur=CREME),
    ]
    return page("B1-01", c, [], palette="violet", fond="fond-violet.png", grille=False)


ESSAI_PAGE1 = [a1_01_actuel, a1_01_affiche, a2_01_actuel, a2_01_affiche]
PAGE1 = {"S03-A1": {"actuel": a1_01_actuel, "affiche": a1_01_affiche},
         "S03-A2": {"actuel": a2_01_actuel, "affiche": a2_01_affiche}}
CHOIX_PAGE1 = {"S03-A1": "affiche", "S03-A2": "affiche"}   # choix du 12/10 : les deux en style affiche

PUBLICATIONS_MEP = {
    "S03-A1": [lambda: PAGE1["S03-A1"][CHOIX_PAGE1["S03-A1"]](), a1_02, a1_03, a1_04, a1_05, a1_06, a1_07],
    "S03-A2": [lambda: PAGE1["S03-A2"][CHOIX_PAGE1["S03-A2"]](), a2_02, a2_03, a2_04, a2_05, a2_06, a2_07],
    "S03-B1": [b1_01],
}
