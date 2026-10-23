# -*- coding: utf-8 -*-
"""Mise en page de la semaine 04 : une fonction par page. Les mots viennent de semaine04.py (seule source du texte).
A1 « C'est trop cher. » : page 1 en style affiche, pages 2 à 7 en collage violet + crème (avant / après, tampons).
A2 « Qui a vendu cette paire ? » : essai du style « dossier » (fond encre rayé, fiches crème à double filet,
polaroïds en couleur réchauffée, trombones, tampons terracotta).
B1 : la phrase qui porte, sur fond violet."""
import hashlib
import json

import numpy as np
from PIL import Image, ImageOps

from composants import (bloc, bandeau, texte, mono, feuille, decoupe, logo, page, md, marquer, couleur_soulignes, url,
                        ASSETS, STICKERS)
from decoupes import gris_collage
from semaine04 import (PUBLICATIONS, CTA_MARQUE_1, CTA_MARQUE_2, CTA_ACTION, CTA_FREIN, CTA_SIGNATURE, PARTAGE,
                       SUIVRE_1, SUIVRE_2, SUIVRE_ACTION, SUIVRE_RAISON)

A1 = PUBLICATIONS[0]["pages"]
A2 = PUBLICATIONS[1]["pages"]
B1 = PUBLICATIONS[2]["pages"]

VIOLET, TERRA, ENCRE, CREME = "#4120CF", "#C06B3E", "#26203A", "#FBF5EF"
PAD = 14 + 11 + 13 + 6  # marge ajoutée par le sticker (contour blanc + contour décalé)
_REPERES = ASSETS / "decoupes" / "reperes_s04.json"   # absent quand on ne refait qu'une page sans photo (23/10)
REPERES = json.loads(_REPERES.read_text()) if _REPERES.exists() else {}


# ---------------- fonds (générés, aucune image tierce) ----------------

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


def fond_dossier():
    """Fond du style dossier : l'encre de la charte, de fines rayures verticales (tissu de classeur), grain fin."""
    cible = ASSETS / "fond-dossier.png"
    if not cible.exists():
        base = np.asarray(Image.open(ASSETS / fond_encre()).convert("RGB")).astype(np.float32)
        xx = np.arange(1080, dtype=np.float32)[None, :]
        rayure = (np.mod(xx, 11) < 1.6).astype(np.float32) * 7.0 - (np.mod(xx + 5, 11) < 1.2).astype(np.float32) * 3.0
        rng = np.random.default_rng(44)
        ondule = 1 + 0.25 * np.sin(np.arange(1350, dtype=np.float32)[:, None] / 37.0 + rng.uniform(0, 6))
        im = base + (rayure * ondule)[..., None] * np.array([1.0, 0.95, 1.15])
        im += rng.normal(0, 2.2, im.shape[:2] + (1,))
        Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(cible)
    return cible.name


# ---------------- petits composants de la semaine ----------------

FLECHE_SVG = ('<svg aria-hidden="true" width="96" height="44" viewBox="0 0 96 44" style="vertical-align:-.05em;'
              'margin-left:.25em;overflow:visible"><path d="M4 28 C 28 14, 52 34, 84 20" stroke="currentColor" '
              'stroke-width="5" fill="none" stroke-linecap="round"/><path d="M66 7 L86 20 L69 35" stroke="currentColor" '
              'stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def relance(txt, droite=64, haut=1190, taille=60, r=-3, ident=None):
    """Cliffhanger écrit à la main en bas de page, aligné à droite, avec sa flèche (la phrase reste complète)."""
    i = f' id="{ident}" data-id="{ident}"' if ident else ""
    return (f'<div class="bloc"{i} style="right:{droite}px;top:{haut}px;text-align:right">'
            f'<div class="relance" style="font-size:{taille}px;--r:{r}deg">{md(txt)}{FLECHE_SVG}</div></div>')


def signet(droite=92):
    return f'<div class="signet" aria-hidden="true" style="right:{droite}px"></div>'


def tampon(entete, x, y, taille=40, q=None, taille_q=48, r=-6, maxw=None, ident=None, couleur=None, z=None):
    st = f"--r:{r}deg;font-size:{taille}px"
    st += (f";max-width:{maxw}px" if maxw else "") + (f";color:{couleur}" if couleur else "")
    corps = f'<div class="entete">{md(entete)}</div>'
    if q:
        st += ";padding:.55em .8em .6em"
        corps += f'<div class="q" style="font-size:{taille_q}px">{md(q)}</div>'
    i = f' id="{ident}" data-id="{ident}"' if ident else ""
    zz = f";z-index:{z}" if z else ""
    return f'<div class="bloc"{i} style="left:{x}px;top:{y}px{zz}"><div class="tampon" style="{st}">{corps}</div></div>'


def geant(lignes, x, y, z=6, interligne=0.84):
    html = "".join(f'<div class="geant-affiche" style="font-size:{t}px;line-height:{interligne}">{md(m)}</div>'
                   for m, t in lignes)
    return f'<div class="bloc" style="left:{x}px;top:{y}px;z-index:{z}">{html}</div>'


def decoupe_nue(code, boite, gauche=None, haut=None, droite=None, bas=None, rot=0, miroir=False, contraste=1.12,
                gamma=0.95, eclaircir=False, z=None):
    """Découpe noir et blanc sans contour (style affiche)."""
    src = ASSETS / "decoupes" / f"{code}.png"
    cle = hashlib.md5(json.dumps([str(src), src.stat().st_mtime, boite, rot, miroir, contraste, gamma, eclaircir]).encode()).hexdigest()[:12]
    cible = STICKERS / f"{code}-nue-{cle}.png"
    if not cible.exists():
        im = Image.open(src).convert("RGBA")
        if miroir:
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


def photo_chaude(code, w, h, cadrage=(0.5, 0.5)):
    """Photo en couleur, réchauffée pour la palette (moins saturée, ombres tirées vers l'encre, hautes lumières vers
    le crème, grain fin), recadrée « cover » à w × h. cadrage : point gardé au centre (fractions de l'image)."""
    src = next((ASSETS / "decoupes").glob(code + ".jpg"))
    cle = hashlib.md5(json.dumps([str(src), src.stat().st_mtime, w, h, cadrage, 3]).encode()).hexdigest()[:12]
    cible = STICKERS / f"{code}-chaude-{cle}.jpg"
    if not cible.exists():
        im = Image.open(src).convert("RGB")
        r = max(w / im.width, h / im.height)
        im = im.resize((max(w, round(im.width * r)), max(h, round(im.height * r))), Image.LANCZOS)
        x0 = int(min(max(0, im.width * cadrage[0] - w / 2), im.width - w))
        y0 = int(min(max(0, im.height * cadrage[1] - h / 2), im.height - h))
        a = np.asarray(im.crop((x0, y0, x0 + w, y0 + h))).astype(np.float32) / 255.0
        lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]
        a = lum + (a - lum) * 0.72                                   # moins saturée
        a = a * np.array([1.05, 1.0, 0.9])                           # plus chaude
        ombre, lumiere = np.array([38, 32, 58]) / 255.0, np.array([251, 240, 226]) / 255.0
        a = a * 0.86 + 0.14 * (ombre * (1 - lum) + lumiere * lum)    # ombres encre, hautes lumières crème
        a = np.clip((a - 0.5) * 1.05 + 0.5, 0, 1)
        a = a + np.random.default_rng(7).normal(0, 0.012, a.shape[:2] + (1,))
        Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).save(cible, quality=94)
    return cible


def polaroid_photo(code, x, y, w, h, r=3.0, cadrage=(0.5, 0.5), ident=None, z=None, contenu=""):
    """Tirage instantané : w × h = zone photo ; cadre blanc 26 px (96 px en bas)."""
    i = f' id="{ident}"' if ident else ""
    zz = f";z-index:{z}" if z else ""
    return (f'<div class="polaroid"{i} style="left:{x}px;top:{y}px;width:{w + 52}px;height:{h + 122}px;--r:{r}deg{zz}">'
            f'<img class="photo" alt="" src="{url(photo_chaude(code, w, h, cadrage))}">{contenu}</div>')


def trombone(x, y, r=0, echelle=1.0):
    """Trombone dessiné en vecteur (métal gris, reflet clair)."""
    d = "M12 34 L12 118 A19 19 0 0 0 50 118 L50 24 A13.5 13.5 0 0 0 23 24 L23 104 A8 8 0 0 0 39 104 L39 40"
    return (f'<svg class="trombone" aria-hidden="true" width="{62 * echelle:.0f}" height="{150 * echelle:.0f}" '
            f'viewBox="0 0 62 150" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">'
            f'<path d="{d}" stroke="#8F8B9C" stroke-width="6.5" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#E6E3EC" stroke-width="2" fill="none" stroke-linecap="round" transform="translate(-1.2,-1.2)"/>'
            f'</svg>')


def fiche(x, y, w, h, r=-1.5, contenu="", ident=None, z=None):
    i = f' id="{ident}"' if ident else ""
    zz = f";z-index:{z}" if z else ""
    return (f'<div class="fiche"{i} style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--r:{r}deg{zz}">'
            f'<div class="contenu">{contenu}</div></div>')


def dans_fiche(classe, txt, x, y, taille, maxw=None, ident=None, extra=""):
    """Texte posé dans une fiche (repère : le coin de la fiche ; il tourne avec elle)."""
    i = f' id="{ident}" data-id="{ident}"' if ident else ""
    mw = f";max-width:{maxw}px" if maxw else ""
    return (f'<div class="bloc"{i} style="left:{x}px;top:{y}px{mw}"><div class="{classe}" '
            f'style="font-size:{taille}px{extra}">{md(txt)}</div></div>')


def fleche_defiler(x=70, y=1262, c="accent"):
    return {"t": "fleche", "de": [x, y], "a": [x + 120, y - 6], "courbe": -0.35, "c": c, "ep": 5, "tete": 22, "graine": 5}


def citation_feuille(citation, x=64, y=300, largeur=950, taille=74, r=-1.2, ident=None):
    cit = f'<div class="texte" style="font-size:{taille}px;font-style:italic;font-weight:700;color:#26203A">{md(citation)}</div>'
    return feuille(cit, x, y, largeur, r=r, padding="34px 52px 40px", ident=ident)


def page_cta(ident, palette, fond, souligne, ligne1=CTA_MARQUE_1, ligne2=CTA_MARQUE_2, a_souligner="compte les ventes."):
    """Dernière page fixe (charte §3) : accroche de marque, une seule action, le frein, la signature."""
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


# ============ A1 · « C'est trop cher. » (avant / après, violet + crème) ============

def a1_01():
    """Style affiche : « C'EST TROP CHER. » géant ; dessous, le Cri de Munch (domaine public) en trois tons de la charte,
    morceau de tableau au bord déchiré, posé en biais (choix de Togi du 21/10 : un élément que tout le monde reconnaît)."""
    p = A1[0]
    mots = p["geant"].upper().split()
    c = [
        signet(96),
        mono(p["coin"], 60, 62, 30),
        geant([(" ".join(mots[:2]), 216), (mots[2], 452)], 44, 150, z=6),
        decoupe("U45", (560, 760), droite=26, haut=706, rot=4, dechire=True, garder_couleur=True, contour=CREME,
                couleur="#0E0B18", z=10),
        texte(couleur_soulignes(p["texte"], "terracotta"), 58, 925, 58, maxw=420, classe="affiche-texte"),
        mono("01/07", 60, 1268, 28),
    ]
    return page("A1-01", c, [fleche_defiler(170, 1282)], palette="affiche", fond=fond_encre(), grille=False)


def a1_02():
    """Le problème, qui accroche seul : la phrase du client, l'étiquette de prix, et ce que la remise lui dit."""
    p = A1[1]
    c = [
        texte(p["citation"].replace(" ", "~"), 110, 150, 96, ident="q", classe="chute"),
        decoupe("U34", (440, 300), gauche=560, haut=370, rot=-16),
        texte(p["texte"], 72, 700, 64, maxw=940, poids="600"),
        texte(couleur_soulignes(p["chute"], "violet"), 72, 890, 84, maxw=940, classe="chute"),
        relance(p["relance"]),
    ]
    plan = [
        {"t": "bulle", "autour": "#q", "queue": [180, 400], "c": "encre", "graine": 41, "marge": 58, "margeY": 44, "rot": -3},
        {"t": "fleche", "de": [470, 380], "a": [520, 610], "courbe": 0.35, "c": "accent", "ep": 7, "tete": 30, "graine": 42},
    ]
    return page("A1-02", c, plan, palette="creme", fond="papier-creme-1.png")


def a1_03():
    """AVANT : la remise donnée tout de suite."""
    p = A1[2]
    c = [
        tampon(p["tampon"], 72, 90, taille=96, r=-7, couleur=ENCRE),
        citation_feuille(p["citation"], y=330, taille=80, r=-1.4),
        texte(couleur_soulignes(p["texte"], "violet"), 72, 720, 66, maxw=940, poids="600"),
        relance(p["relance"]),
    ]
    plan = [{"t": "croix", "x": 900, "y": 170, "taille": 64, "ep": 11, "c": "accent", "graine": 43}]
    return page("A1-03", c, plan, palette="creme", fond="papier-creme-3.png")


def a1_04():
    """APRÈS · 1 : une question, puis on écoute."""
    p = A1[3]
    c = [
        tampon(p["tampon"], 72, 90, taille=80, r=-6),
        citation_feuille(p["citation"], y=320, taille=80, r=1.2),
        # une ligne, sans couper « laissez-le » au trait d'union (Fraunces n'a pas le trait d'union insécable)
        bloc(f'<div class="texte" style="font-size:64px;font-weight:600;white-space:nowrap">{md(p["texte"])}</div>', 72, 690),
        texte(couleur_soulignes(p["chute"], "violet"), 72, 900, 80, maxw=940, classe="chute"),
        relance(p["relance"]),
    ]
    plan = [{"t": "bulleVide", "cx": 900, "cy": 650, "w": 230, "h": 130, "queue": [840, 740], "c": "accent",
             "points": True, "graine": 44}]
    return page("A1-04", c, plan, palette="creme", fond="papier-creme-4.png")


def a1_05():
    """APRÈS · 2 : reprendre ses mots ; l'écran (photo) est sa journée."""
    p = A1[4]
    c = [
        tampon(p["tampon"], 72, 70, taille=62, r=-6),
        texte(p["intro"], 72, 236, 58, poids="600"),
        citation_feuille(p["citation"], y=330, taille=60, r=-1),
        decoupe("U35", (800, 290), gauche=120, haut=650, rot=-2, dechire=True),
        texte(couleur_soulignes(p["chute"], "violet"), 72, 1010, 68, maxw=940, classe="chute"),
        relance(p["relance"], haut=1222, taille=50),
    ]
    return page("A1-05", c, [], palette="creme", fond="papier-creme-2.png")


def a1_06():
    """APRÈS · 3 : le client choisit ce qu'on garde (la balance), et la demande d'enregistrement."""
    p = A1[5]
    c = [
        tampon(p["tampon"], 72, 70, taille=62, r=-6),
        texte(p["intro"], 72, 236, 58, poids="600"),
        citation_feuille(p["citation"], y=330, taille=72, r=1.2),
        decoupe("U36", (330, 420), gauche=80, haut=560, rot=3, dechire=True),
        texte(couleur_soulignes(p["chute"], "violet"), 520, 700, 86, maxw=500, classe="chute"),
        bandeau(p["enregistrer"].replace("c’est trop cher", "c’est~trop~cher"), 64, 1070, 54, r=-1.5, variante="titre", maxw=950, ident="enregistrer"),
    ]
    return page("A1-06", c, [], palette="creme", fond="papier-creme-1.png")


def page_suivre(ident, palette, fond, souligne):
    """Dernière page « Suivez » (décision de Togi du 23/10) : la promesse du compte, une seule action (suivre),
    la raison, la signature. Pas de lien d'accès : il reste dans la bio. Même ossature que page_cta."""
    c = [
        bandeau(SUIVRE_1, 52, 170, 74, r=-2, variante="clair titre", maxw=980),
        texte(couleur_soulignes(marquer(SUIVRE_2, SUIVRE_2), souligne), 76, 360, 104, maxw=960, classe="chute"),
        bandeau(SUIVRE_ACTION, 58, 600, 84, r=-2, variante="titre", ident="action"),
        texte(SUIVRE_RAISON, 80, 790, 52, maxw=900, couleur="#3A3350"),
        logo(342, 1010, 140),
        mono(CTA_SIGNATURE, 60, 1196, 28, couleur="#6E6782", largeur=960, align="center"),
    ]
    plan = [{"t": "fleche", "de": [830, 500], "a": [690, 640], "courbe": -0.45, "c": "accent", "ep": 5.5, "graine": 4, "tete": 28}]
    return page(ident, c, plan, palette=palette, fond=fond, miroir=True)


def a1_07():
    # 23/10 : la page « Demander un accès » (page_cta) est remplacée par la page « Suivez » (fin du test v1.5)
    return page_suivre("A1-07", "creme", "papier-creme-3.png", "violet")


# ============ A2 · Qui a vendu cette paire ? (style dossier, encre + crème + terracotta) ============

def a2_01():
    p = A2[0]
    contenu = (dans_fiche("titre-fiche", p["titre"], 76, 96, 98, maxw=800, ident="titre")
               + dans_fiche("ital", p["sous_titre"], 80, 370, 60, maxw=760, ident="sous-titre"))
    c = [
        signet(96),
        mono(p["coin"], 60, 62, 30),
        fiche(60, 180, 960, 600, r=-2, contenu=contenu),
        polaroid_photo("U37", 486, 690, 500, 340, r=5, cadrage=(0.45, 0.5), z=18),
        trombone(600, 650, r=-10),
        mono("01/07", 60, 1268, 28),
    ]
    return page("A2-01", c, [fleche_defiler(170, 1282)], palette="dossier", fond=fond_dossier(), grille=False)


def a2_02():
    p = A2[1]
    contenu = (dans_fiche("corps", p["texte"], 74, 72, 58, maxw=820, ident="t1", extra=";font-weight:650")
               + dans_fiche("corps", p["suite"], 74, 236, 50, maxw=820, ident="t2")
               + dans_fiche("ital", p["citation"].replace(" ", "~"), 70, 390, 82, maxw=840, ident="cit"))
    c = [
        polaroid_photo("U38", 70, 70, 640, 410, r=-3, cadrage=(0.5, 0.42), z=18),
        trombone(600, 36, r=12),
        fiche(66, 586, 948, 560, r=1.5, contenu=contenu),
        relance(p["relance"]),
    ]
    plan = [{"t": "lunettes", "cx": 402, "cy": 262, "r": 30, "rot": -6, "c": "terracotta", "ep": 5, "graine": 46}]
    return page("A2-02", c, plan, palette="dossier", fond=fond_dossier(), grille=False)


def a2_cas(ident, p, cadrage=(0.5, 0.5), sur_photo=""):
    """Pages 3 à 5 : un cas par fiche ; la photo en polaroïd ; la question à trancher, au tampon."""
    contenu = (dans_fiche("mono", p["numero"], 76, 70, 34, ident="num", extra=";color:#C06B3E")
               + dans_fiche("titre-fiche", p["titre"], 72, 124, 64, maxw=440, ident="titre")
               + dans_fiche("corps", p["texte"], 72, 300, 58, maxw=820, ident="texte")
               + tampon(p["tampon"], 64, 472, taille=36, q=p["question"], taille_q=58, r=-4, maxw=840, ident="tampon"))
    c = [
        fiche(56, 300, 968, 730, r=-1.2, contenu=contenu),
        polaroid_photo(p["photo"], 560, 60, 420, 300, r=4, cadrage=cadrage, z=18, contenu=sur_photo),
        trombone(860, 30, r=14),
        relance(p["relance"], haut=1170),
    ]
    return page(ident, c, [], palette="dossier", fond=fond_dossier(), grille=False)


def a2_03():
    return a2_cas("A2-03", A2[2], cadrage=(0.52, 0.5))


def a2_04():
    return a2_cas("A2-04", A2[3], cadrage=(0.5, 0.5))


def a2_05():
    rendue = ('<div style="position:absolute;left:36px;top:150px">'
              f'<div class="tampon" style="--r:-12deg;font-size:44px;color:#C06B3E;background:rgba(251,245,239,.82);">'
              '<div class="entete">Rendue</div></div></div>')
    return a2_cas("A2-05", A2[4], cadrage=(0.55, 0.5), sur_photo=rendue)


def a2_06():
    """La règle : le porte-bloc (photo) où la règle s'écrit à la main ; la phrase ; la demande de partage."""
    p = A2[5]
    w, h, x, y = 560, 392, 70, 66
    fx0, fy0, fx1, fy1 = REPERES["U42"]["feuille"]
    k = w / REPERES["U42"]["taille"][0]
    bx, by, bw, bh = x + 26 + fx0 * k, y + 26 + fy0 * k, (fx1 - fx0) * k, (fy1 - fy0) * k
    contenu = (dans_fiche("corps", p["phrase1"], 72, 74, 60, maxw=760, ident="p1", extra=";font-weight:650")
               + dans_fiche("ital", couleur_soulignes(p["phrase2"], "terracotta"), 72, 180, 82, maxw=760, ident="p2"))
    c = [
        polaroid_photo("U42", x, y, w, h, r=-4, z=18),
        trombone(520, 30, r=10),
        fiche(110, 560, 910, 400, r=1.8, contenu=contenu),
        bandeau(p["partager"], 64, 1050, 56, r=-1.5, variante="titre", maxw=950, ident="partager"),
    ]
    plan = [{"t": "ecriture", "boite": [round(bx + bw * 0.16), round(by + bh * 0.18), round(bw * 0.62), round(bh * 0.6)],
             "lignes": 4, "c": "encre", "ep": 3.6, "graine": 47, "rot": -4}]
    return page("A2-06", c, plan, palette="dossier", fond=fond_dossier(), grille=False)


def a2_07():
    """La carte d'accès : le pont, l'action unique, le frein, la signature ; la clé posée en haut à droite."""
    p = A2[6]
    contenu = (dans_fiche("titre-fiche", p["pont1"], 84, 104, 76, maxw=620, ident="pont1")
               + dans_fiche("ital", marquer(p["pont2"], "compte les ventes.", "terracotta"), 80, 340, 80, maxw=840,
                            ident="pont2")
               + f'<div class="bloc" style="left:78px;top:486px">'
               f'<div class="bandeau titre" style="font-size:54px;--r:-1.5deg">{md(CTA_ACTION)}</div></div>'
               + dans_fiche("corps", CTA_FREIN.replace("sans engagement", "sans~engagement"), 84, 630, 42, maxw=800,
                            ident="frein", extra=";color:#3A3350")
               + logo(84, 800, 96)
               + dans_fiche("mono", CTA_SIGNATURE, 84, 950, 28, ident="signature",
                            extra=";color:#6E6782;letter-spacing:.05em;white-space:nowrap"))
    c = [
        fiche(60, 150, 960, 1060, r=-1.5, contenu=contenu),
        decoupe("U43", (200, 470), droite=40, haut=110, rot=-32, garder_couleur=True, contour=CREME, couleur=TERRA,
                devant=True),
    ]
    return page("A2-07", c, [], palette="dossier", fond=fond_dossier(), grille=False)


# ============ B1 · La phrase qui porte ============

def s_officiel():
    """Le S du logo, seul (couleurs d'origine), découpé dans assets/logo-sehoria.png."""
    cible = STICKERS / "logo-S.png"
    if not cible.exists():
        im = Image.open(ASSETS / "logo-sehoria.png").convert("RGBA")
        s = im.crop((0, 0, 487, im.height))
        s.crop(s.getbbox()).save(cible)
    return cible


def b1_01():
    p = B1[0]
    phrase = f'<div class="texte" style="font-size:72px;font-weight:700;line-height:1.1;text-align:center">{md(p["phrase"])}</div>'
    chute = (f'<div class="chute" style="font-size:88px;text-align:center;margin-top:34px">'
             f'{md(marquer(p["chute"], "une question."))}</div>')
    # Le S officiel à la place du « (Togi, 21/10 : le « dans son carré se lisait comme deux petites flèches).
    # Tuile crème, ombre décalée encre (comme les bandeaux), le S dans ses couleurs d'origine.
    tuile = ('<div class="bloc" aria-hidden="true" style="left:458px;top:92px;width:164px;height:164px;background:#FFFCF7;'
             'border-radius:34px;transform:rotate(-4deg);z-index:22;box-shadow:8px 8px 0 #26203A">'
             f'<img alt="" src="{url(s_officiel())}" style="position:absolute;left:50%;top:50%;height:118px;'
             'transform:translate(-50%,-50%)"></div>')
    c = [
        feuille(phrase + chute, 88, 170, 904, hauteur=620, r=-2, padding="140px 52px 56px"),
        tuile,
        decoupe("U44", (560, 380), gauche=262, haut=760, rot=-5, contour=CREME, couleur=ENCRE, devant=True),
        mono(PARTAGE, 72, 1182, 28, couleur=CREME, maxw=250),
        logo(826, 1194, 46, "creme"),
        mono("sehoria.fr", 826, 1252, 28, couleur=CREME),
    ]
    return page("B1-01", c, [], palette="violet", fond="fond-violet.png", grille=False)


PUBLICATIONS_MEP = {
    "S04-A1": [a1_01, a1_02, a1_03, a1_04, a1_05, a1_06, a1_07],
    "S04-A2": [a2_01, a2_02, a2_03, a2_04, a2_05, a2_06, a2_07],
    "S04-B1": [b1_01],
}
