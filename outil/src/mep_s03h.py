# -*- coding: utf-8 -*-
"""Mise en page du hors-série S03h (lundi 19/10) : une fonction par page. Les mots viennent de semaine03h.py.
Page 1 en style affiche (fond encre, « 9 ANS » géant derrière la voiture bâchée, terracotta seule couleur vive) ;
pages 2 à 7 en collage violet + terracotta."""
import hashlib
import json

import numpy as np
from PIL import Image

from composants import (numero, bandeau, texte, mono, main, carte, decoupe, logo, page, md, marquer, une_phrase_par_ligne,
                        couleur_soulignes, url, ASSETS, STICKERS)
from decoupes import gris_collage
from semaine03h import PUBLICATIONS, CTA_MARQUE_1, CTA_MARQUE_2, CTA_ACTION, CTA_FREIN, CTA_SIGNATURE

H1 = PUBLICATIONS[0]["pages"]
TERRA = "#C06B3E"


# ---------------- outils (repris de mep_s03) ----------------

def fond_encre():
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


def decoupe_nue(code, boite, gauche=None, haut=None, droite=None, bas=None, rot=0, miroir=False, contraste=1.12,
                gamma=0.95, eclaircir=False, z=None):
    """Découpe noir et blanc sans contour (style affiche)."""
    src = ASSETS / "decoupes" / f"{code}.png"
    cle = hashlib.md5(json.dumps([str(src), src.stat().st_mtime, boite, rot, miroir, contraste, gamma, eclaircir]).encode()).hexdigest()[:12]
    cible = STICKERS / f"{code}-nue-{cle}.png"
    if not cible.exists():
        im = Image.open(src).convert("RGBA")
        if miroir:
            from PIL import ImageOps
            im = ImageOps.mirror(im)
        if rot:
            im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
            im = im.crop(im.getbbox())
        ratio = min(boite[0] / im.width, boite[1] / im.height)
        im = im.resize((round(im.width * ratio), round(im.height * ratio)), Image.LANCZOS)
        g = gris_collage(im.convert("RGB"), gamma=gamma, contraste=contraste, eclaircir=eclaircir)
        out = g.convert("RGBA")
        out.putalpha(im.split()[-1])
        out.save(cible)
    w, h = Image.open(cible).size
    st = ";".join(f"{k}:{v}" for k, v in {
        "left": f"{gauche}px" if gauche is not None else None, "top": f"{haut}px" if haut is not None else None,
        "right": f"{droite}px" if droite is not None else None, "bottom": f"{bas}px" if bas is not None else None,
        "width": f"{w}px", "height": f"{h}px", "z-index": z}.items() if v is not None)
    return f'<img class="decoupe nue" alt="" src="{url(cible)}" style="{st}">'


def fumee(traines, ident, z=8, couleur=(251, 245, 239), graine=7):
    """Traînées de fumée générées (aucune image tierce) : nuages gaussiens le long de courbes de Bézier, texturés
    par un bruit flou. traines : [(départ, contrôle, arrivée, rayon début, rayon fin, opacité), …] en px de page."""
    import cv2
    cle = hashlib.md5(json.dumps([traines, couleur, graine]).encode()).hexdigest()[:10]
    cible = STICKERS / f"fumee-{ident}-{cle}.png"
    if not cible.exists():
        rng = np.random.default_rng(graine)
        a = np.zeros((1350, 1080), np.float32)
        for (x1, y1), (cx, cy), (x2, y2), r0, r1, op in traines:
            couche = np.zeros_like(a)
            for t in np.linspace(0, 1, 160):
                x = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2
                y = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2
                r = r0 + (r1 - r0) * t ** 0.9
                for _ in range(2):
                    px, py = x + rng.normal(0, r * 0.22), y + rng.normal(0, r * 0.22)
                    cv2.circle(couche, (int(px), int(py)), max(2, int(r * rng.uniform(0.7, 1.0))), 1.0, -1, cv2.LINE_AA)
            couche = cv2.GaussianBlur(couche, (0, 0), 7)
            a = np.maximum(a, np.clip(couche, 0, 1) * op)
        bruit = cv2.GaussianBlur(rng.random(a.shape).astype(np.float32), (0, 0), 11)
        bruit = (bruit - bruit.min()) / (bruit.max() - bruit.min())
        fin = cv2.GaussianBlur(rng.random(a.shape).astype(np.float32), (0, 0), 1.6)
        fin = (fin - fin.min()) / (fin.max() - fin.min())
        a = a * (0.35 + 0.65 * bruit) * (0.85 + 0.15 * fin)
        a = cv2.GaussianBlur(a, (0, 0), 2.2)
        rgba = np.zeros((1350, 1080, 4), np.uint8)
        rgba[..., :3] = couleur
        rgba[..., 3] = np.clip(a * 255, 0, 255).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(cible)
    return (f'<img class="decoupe" alt="" src="{url(cible)}" '
            f'style="left:0;top:0;width:1080px;height:1350px;z-index:{z}">')


def geant(lignes, x, y, z=6, interligne=0.84):
    html = "".join(f'<div class="geant-affiche" style="font-size:{t}px;line-height:{interligne}">{md(m)}</div>'
                   for m, t in lignes)
    return f'<div class="bloc" style="left:{x}px;top:{y}px;z-index:{z}">{html}</div>'


def fleche_defiler(x=70, y=1262, c="accent"):
    return {"t": "fleche", "de": [x, y], "a": [x + 120, y - 6], "courbe": -0.35, "c": c, "ep": 5, "tete": 22, "graine": 5}


def titre_bloc(titre, texte_html="", x=54, y=84, largeur=960, maxw_titre=790, taille=88, taille_texte=50, maxw_texte=900):
    t = (f'<div class="texte entete-texte" style="font-size:{taille_texte}px;max-width:{maxw_texte}px">{md(texte_html)}</div>'
         if texte_html else "")
    return (f'<div class="bloc colonne" style="left:{x}px;top:{y}px;width:{largeur}px">'
            f'<div class="bandeau clair titre" style="font-size:{taille}px;--r:-1.5deg;max-width:{maxw_titre}px">{md(titre)}</div>'
            f'{t}</div>')


def page_cta(ident, palette, fond, souligne, ligne1=CTA_MARQUE_1, ligne2=CTA_MARQUE_2, a_souligner="compte les ventes."):
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


# ============ H1 · Un délai qu'on tient (violet + terracotta) ============
# Refonte du 17/10 à 15 h (Togi : « pas assez pro », « trop de dessins ») : une photo de mise en situation par page,
# grande, en noir et blanc ; les dessins se limitent aux annotations à la main.

PAD = 14 + 11 + 13 + 6  # marge ajoutée par le sticker (contour blanc + contour décalé)


def h1_01():
    """Affiche pleine page : la voiture sous sa housse (photo en bichromie encre / crème), le libellé d'actualité
    (« ACTU · TESLA · 15/10 », accord de Togi), « 9 ANS » géant au-dessus, le buzz dit en trois lignes, la chute à la main."""
    p = H1[0]
    libelle = ('<div class="bloc" style="left:60px;top:58px;z-index:30"><div class="mono" style="font-size:30px;'
               'background:#C06B3E;color:#FBF5EF;opacity:1;padding:.34em .72em .3em;letter-spacing:.16em;'
               f'box-shadow:6px 6px 0 #0E0B18">{md(p["libelle"])}</div></div>')
    c = [
        libelle,
        geant([(p["geant"].upper(), 300)], 46, 128, z=6),
        texte(une_phrase_par_ligne(p["bandeau"]), 56, 958, 46, maxw=980, classe="affiche-texte"),
        main(couleur_soulignes(p["main"], "terracotta"), 56, 1118, 60, r=-2, maxw=980),
        mono("01/07", 60, 1272, 28),
    ]
    return page("H1-01", c, [fleche_defiler(900, 1292)], palette="affiche", fond="decoupes/H1-fond.jpg", grille=False)


def h1_02():
    """Le problème, qui accroche seul : le client à la porte du magasin (photo), sa question, la réponse."""
    p = H1[1]
    c = [
        decoupe("U28", (380, 960), gauche=36, haut=120, rot=-2, dechire=True, contour="#FFFFFF", couleur=TERRA),
        bandeau(p["citation1"], 540, 150, 54, r=-1.5, variante="clair", maxw=480, ident="q1"),
        bandeau(p["citation2"].replace(" ", "~"), 536, 420, 52, r=2, ident="q2", maxw=480),
        texte(p["texte"], 548, 640, 48, maxw=470, poids="600"),
        texte(couleur_soulignes(p["chute"], "terracotta"), 548, 820, 60, maxw=480, classe="chute"),
    ]
    plan = [{"t": "fleche", "de": [560, 330], "a": [420, 470], "courbe": 0.35, "c": "accent", "ep": 6, "tete": 24,
             "graine": 27}]
    return page("H1-02", c, plan, palette="terracotta", fond="papier-creme-2.png")


def h1_03():
    """Annoncer un délai qu'on tient : le calendrier (photo), la date entourée."""
    p = H1[2]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=800, taille=88, taille_texte=58),
         decoupe("U29", (720, 590), gauche=180, haut=430, rot=2, dechire=True, contour="#FFFFFF", couleur=TERRA),
         texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1124, 70, maxw=940, classe="chute")]
    return page("H1-03", c, [], palette="terracotta", fond="papier-creme-3.png")


def h1_04():
    """Prévenir avant : les mains qui écrivent le message (photo), une bulle « … » à la main."""
    p = H1[3]
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=780, taille=88, taille_texte=52, maxw_texte=900),
         decoupe("U30", (740, 560), gauche=150, haut=450, rot=-1.5, dechire=True, contour="#FFFFFF", couleur=TERRA),
         texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1126, 76, maxw=940, classe="chute")]
    plan = [{"t": "bulleVide", "cx": 800, "cy": 560, "w": 190, "h": 106, "queue": [730, 650], "c": "accent",
             "points": True, "remplir": "creme", "graine": 912}]
    return page("H1-04", c, plan, palette="terracotta", fond="papier-creme-4.png")


def h1_05():
    """Chaque matin : le café et le carnet (photo, plus grande) ; la liste du lendemain cochée sur la couverture."""
    p = H1[4]
    boite, gauche, haut = (840, 560), 80, 450
    im = Image.open(ASSETS / "decoupes" / "U25.jpg")
    r = min(boite[0] / im.width, boite[1] / im.height)
    x0, y0, x1, y1 = json.loads((ASSETS / "decoupes" / "reperes_s03h.json").read_text())["U25"]["carnet"]
    cx0, cy0, cx1, cy1 = (gauche + PAD + x0 * r, haut + PAD + y0 * r, gauche + PAD + x1 * r, haut + PAD + y1 * r)
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], p["texte"], maxw_titre=760, taille=88, taille_texte=52, maxw_texte=900),
         decoupe("U25", boite, gauche=gauche, haut=haut, dechire=True, contour="#FFFFFF", couleur=TERRA),
         texte(couleur_soulignes(p["chute"], "terracotta"), 72, 1124, 70, maxw=940, classe="chute")]
    lw, lh = cx1 - cx0, cy1 - cy0
    plan = [{"t": "ecriture", "boite": [round(cx0 + lw * 0.14), round(cy0 + lh * 0.22), round(lw * 0.72), round(lh * 0.6)],
             "lignes": 4, "coches": [0, 1, 2, 3], "c": "encre", "ep": 4, "graine": 81, "rot": -2}]
    return page("H1-05", c, plan, palette="terracotta", fond="papier-creme-1.png")


def h1_06():
    """La solution : la main qui rend les lunettes (photo) et le tournevis ; les trois réponses en liste."""
    p = H1[5]
    lignes = "".join(f'<div style="margin-bottom:22px"><span style="color:#C06B3E;font-weight:800">—</span>\u00a0{md(l)}</div>'
                     for l in p["liste"])
    liste = (f'<div class="bloc" style="left:64px;top:968px;max-width:960px"><div class="texte" '
             f'style="font-size:50px;font-weight:600;line-height:1.15">{lignes}</div></div>')
    c = [numero(p["numero"], droite=64, haut=60, taille=280),
         titre_bloc(p["titre"], maxw_titre=780, taille=88),
         decoupe("U31", (590, 520), gauche=40, haut=330, rot=-2, dechire=True, contour="#FFFFFF", couleur=TERRA),
         decoupe("U26", (340, 76), gauche=600, haut=820, rot=-9, dechire=True, contour="#FFFFFF", couleur=TERRA,
                 devant=True),
         liste]
    return page("H1-06", c, [], palette="terracotta", fond="papier-creme-2.png")


def h1_07():
    return page_cta("H1-07", "terracotta", "papier-creme-3.png", "terracotta")


PUBLICATIONS_MEP = {"S03-H1": [h1_01, h1_02, h1_03, h1_04, h1_05, h1_06, h1_07]}
