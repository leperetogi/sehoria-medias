# -*- coding: utf-8 -*-
"""Mise en page de la semaine 05. Les mots viennent de semaine05.py (seule source du texte).
S05-A1 / S05-A1s : format test « photo plein cadre » (maquette outil/maquettes/format-photo, 25/10) — photo sur toute
la page, dégradé encre en bas, titre Poppins 800 en capitales avec un passage en bandeau violet, « Faites glisser »
en page 1, numéro de page, relance écrite à la main (Gochi Hand) en bas des pages 2 à 5.
S05-A1s (profil LinkedIn de Togi) : aucun logo Sehoria, dernière page à son nom.
S05-B1 : la phrase qui porte, même ossature que S04-B1 (tuile au S officiel, feuille, découpe, fond violet)."""
from composants import md, page, url, logo, feuille, decoupe, mono, STICKERS
from mep_s04 import FLECHE_SVG, relance, s_officiel
from semaine05 import (PUBLICATIONS, SUIVRE_TITRE, SUIVRE_BANDE, SUIVRE_ACTION, SUIVRE_RAISON, CTA_SIGNATURE, PARTAGE)

A1 = PUBLICATIONS[0]["pages"]
A1S = PUBLICATIONS[1]["pages"]
B1 = PUBLICATIONS[2]["pages"]
N = len(A1)
ENCRE, CREME = "#26203A", "#FBF5EF"


def logo_creme():
    logo(0, 0, 40, "creme")          # crée build/stickers/logo-creme.png si besoin
    return url(STICKERS / "logo-creme.png")


def bande(txt, morceau):
    """Le texte validé, un passage en bandeau violet (mêmes mots)."""
    assert morceau in txt, (morceau, txt)
    avant, _, apres = txt.partition(morceau)
    return f'{md(avant)}<span class="b">{md(morceau)}</span>{md(apres)}'


def fleche(largeur=100):
    return FLECHE_SVG.replace('width="96"', f'width="{largeur}"').replace('<svg ', '<svg class="fleche-photo" ', 1)


def pied(n, marque=True, gauche_html=None):
    gauche = gauche_html if gauche_html is not None else (
        f'<img alt="Sehoria" src="{logo_creme()}" style="height:34px;display:block">' if marque else "")
    return (f'<div class="bloc ph-pied" id="pied" style="left:60px;right:60px;bottom:52px">'
            f'<div class="g">{gauche}</div><div class="g">{n:02d}/{N:02d}</div></div>')


def pile(contenu, bas, ident="pile"):
    return f'<div class="bloc ph-pile" id="{ident}" style="left:60px;bottom:{bas}px;width:960px">{contenu}</div>'


def titre(p, taille):
    return f'<div class="ph-titre" style="font-size:{taille}px">{bande(p["titre"], p["bande"])}</div>'


def corps(txt, taille=42, extra=""):
    return f'<div class="ph-corps" style="font-size:{taille}px{extra}">{md(txt)}</div>'


def page_photo(ident, photo, contenu, v0="30%"):
    c = ['<div class="ph-haut"></div>', f'<div class="ph-voile" style="--v0:{v0}"></div>'] + contenu
    return page(ident, c, [], palette="photo", fond=f"decoupes/{photo}.jpg", grille=False)


# ============ pages 1 à 6 (communes aux deux versions) ============

def p01(marque=True):
    p = A1[0]
    sig = (f'<div class="ph-sig">' + (f'<img alt="Sehoria" src="{logo_creme()}">' if marque else "")
           + f'<span>{md(p["sig"])}</span></div>')
    glisser = f'<span>{md(p["glisser"])}</span>{fleche(110)}'
    c = [
        f'<div class="bloc" style="left:60px;top:58px"><div class="ph-puce">{md(p["coin"])}</div></div>',
        pile(sig + titre(p, 64), 150),
        pied(1, gauche_html=glisser),
    ]
    return page_photo("A1-01", p["photo"], c, v0="33%")


def p_point(i, marque=True, taille_corps=42):
    p = A1[i - 1]
    c = [
        pile(titre(p, 62) + corps(p["corps"], taille_corps), 228),
        relance(p["relance"], droite=60, haut=1140, taille=54, r=-3),
        pied(i, marque),
    ]
    return page_photo(f"A1-{i:02d}", p["photo"], c, v0="26%")


def p06(marque=True):
    p = A1[5]
    enr = f'<div class="ph-corps" style="font-size:40px;color:{CREME}">{md(p["enregistrer"])}</div>'
    c = [
        pile(titre(p, 62) + enr, 150),
        pied(6, marque),
    ]
    return page_photo("A1-06", p["photo"], c, v0="28%")


# ============ page 7 ============

def p07_suivre():
    p = A1[6]
    t = f'<div class="ph-titre" style="font-size:56px">{bande(SUIVRE_TITRE, SUIVRE_BANDE)}</div>'
    bouton = (f'<div style="display:flex;align-items:center;gap:26px">'
              f'<div class="ph-bouton" style="font-size:70px">{md(SUIVRE_ACTION)}</div></div>')
    raison = corps(SUIVRE_RAISON, 38, ";color:#E9E3F5")
    sig = (f'<div class="ph-sig" style="margin-top:6px">'
           f'<span style="white-space:nowrap">{md(CTA_SIGNATURE)}</span></div>')
    c = [
        pile(t + bouton + raison + sig, 130),
        pied(7, True),
    ]
    return page_photo("A1-07", p["photo"], c, v0="27%")


def p07_signature():
    p = A1S[6]
    nom = f'<div class="ph-titre" style="font-size:118px;line-height:1">{md(p["nom"])}</div>'
    metier = f'<div class="ph-sig" style="margin-top:-8px"><span>{md(p["metier"])}</span></div>'
    partage = f'<div class="ph-corps" style="font-size:44px;color:{CREME};margin-top:18px">{md(p["partage"])}</div>'
    c = [
        pile(nom + metier + partage, 150),
        pied(7, False),
    ]
    return page_photo("A1-07", p["photo"], c, v0="34%")


# ============ B1 · La phrase qui porte ============

def b1_01():
    p = B1[0]
    phrase = f'<div class="texte" style="font-size:66px;font-weight:700;line-height:1.1;text-align:center">{md(p["phrase"])}</div>'
    chute = (f'<div class="chute" style="font-size:84px;text-align:center;margin-top:34px">'
             f'{md("[[" + p["chute"] + "]]")}</div>')
    tuile = ('<div class="bloc" aria-hidden="true" style="left:458px;top:92px;width:164px;height:164px;background:#FFFCF7;'
             'border-radius:34px;transform:rotate(-4deg);z-index:22;box-shadow:8px 8px 0 #26203A">'
             f'<img alt="" src="{url(s_officiel())}" style="position:absolute;left:50%;top:50%;height:118px;'
             'transform:translate(-50%,-50%)"></div>')
    c = [
        feuille(phrase + chute, 88, 170, 904, hauteur=600, r=-2, padding="140px 52px 56px"),
        tuile,
        decoupe("U48", (420, 520), gauche=330, haut=700, rot=3, contour=CREME, couleur="#26203A", devant=True),
        mono(PARTAGE, 72, 1182, 28, couleur=CREME, maxw=250),
        logo(826, 1194, 46, "creme"),
        mono("sehoria.fr", 826, 1252, 28, couleur=CREME),
    ]
    return page("B1-01", c, [], palette="violet", fond="fond-violet.png", grille=False)


PUBLICATIONS_MEP = {
    "S05-A1": [p01, lambda: p_point(2), lambda: p_point(3), lambda: p_point(4), lambda: p_point(5), p06, p07_suivre],
    "S05-A1s": [lambda: p01(False), lambda: p_point(2, False), lambda: p_point(3, False), lambda: p_point(4, False),
                lambda: p_point(5, False), lambda: p06(False), p07_signature],
    "S05-B1": [b1_01],
}
