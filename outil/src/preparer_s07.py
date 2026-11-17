# -*- coding: utf-8 -*-
"""Semaine 07 — images du carrousel Sehoria du mois « Votre challenge s'éteint » (photo plein cadre) et de la phrase B.

Entrées (téléchargées par GitHub le 17/11 ; texte et photos envoyés à Togi le 15/11 à 16 h 40, publiés selon la règle
des 24 h) :
- U58 : Gustave Courbet, Le Désespéré, 1843-1845, reproduction Wikimedia Commons, domaine public (1500 × 1228, en largeur) ;
- U65-bougies (Kier in Sight Archives, y0w7tf6khI4) : p. 2 (le ballon U59 n'était pas dégonflé : non utilisé) ;
- U60-calendrier (Nathan Dumlao, tG4waP7YiAg) : p. 3, « JAN 1 », l'année et la marque du bandeau effacés (§5, §6) ;
- U61-trophee (Gabriela Testa, bIiSTFBZEgQ) : p. 4, recadré sur la coupe (la plaque et la roue de moto hors cadre) ;
- U62-bravo (Ashford Marx, LIs-2xpMOHA) : p. 5, l'enseigne du fond floutée ;
- U63-cle (Amol Tyagi, 0juktkOTkpU) : p. 7, page d'accès ;
- U64-solaires (Anton Be, ODhxNCO8XHY) : B1, détourées.
Sorties : assets/decoupes/S07-*.jpg (pages 1080 × 1350) et U64.png."""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preparer_photos import SRC, OUT
from preparer_s03 import garder_plus_grand, enregistrer
from preparer_s04 import masque

W, H = 1080, 1350
ENCRE = (38, 32, 58)


def recadrer(im, boite, nom):
    x0, y0, x1, y1 = boite
    assert abs((x1 - x0) * 1.25 - (y1 - y0)) <= 2, (nom, boite)        # 4:5
    im.crop(boite).resize((W, H), Image.LANCZOS).save(OUT / f"{nom}.jpg", quality=94)
    print(nom, boite)


def haut_puis_encre(im, nom):
    """Le tableau est en largeur : il occupe le haut de la page, puis se fond dans l'encre (le texte vient dessous).
    Le visage reste ainsi au-dessus du dégradé."""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    fond = Image.new("RGB", (W, H), ENCRE)
    fond.paste(im, (0, 0))
    h = im.height
    fondu = 220
    a = np.zeros((H, W), np.float32)
    a[:h - fondu] = 1
    a[h - fondu:h] = np.linspace(1, 0, fondu)[:, None]
    out = (np.asarray(fond, np.float32) * a[..., None] + np.array(ENCRE, np.float32) * (1 - a[..., None]))
    Image.fromarray(out.astype(np.uint8)).save(OUT / f"{nom}.jpg", quality=94)
    print(nom, "tableau", im.size)


def desespere():
    im = Image.open(SRC / "U58-desespere.jpg").convert("RGB")         # 1500 × 1228
    haut_puis_encre(im.crop((130, 0, 1370, 1130)), "S07-D1")          # p. 1 : le tableau presque entier, signature hors cadre
    recadrer(im, (420, 220, 1100, 1070), "S07-D6")                     # p. 6 : les yeux et les mains dans les cheveux


def effacer(im, zones):
    """Remplit les zones (texte, marques) à partir du papier ou du mur autour."""
    a = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    m = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in zones:
        m[y0:y1, x0:x1] = 255
    a = cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))


def nettoyer_calendrier(im):
    """Le bandeau noir (logo, « 2020 ») repeint de sa couleur ; « JAN 1 » repeint de la couleur du papier (§5, §6)."""
    from PIL import ImageDraw
    a = np.asarray(im)
    noir = tuple(int(v) for v in np.median(a[715:735, 600:1000].reshape(-1, 3), axis=0))
    papier = tuple(int(v) for v in np.median(a[860:890, 650:950].reshape(-1, 3), axis=0))
    d = ImageDraw.Draw(im)
    d.rectangle((462, 700, 1145, 748), fill=noir)
    d.rectangle((690, 890, 935, 950), fill=papier)
    return im


def flouter(im, zones, r=25):
    """Flou à bords fondus : l'enseigne devient illisible sans laisser de rectangle visible."""
    from PIL import ImageDraw
    flou = im.filter(ImageFilter.GaussianBlur(r))
    m = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(m)
    for z in zones:
        d.rectangle(z, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(40))
    return Image.composite(flou, im, m)


def pages_photos():
    im = Image.open(SRC / "U65-bougies.jpg").convert("RGB")           # 1799 × 2400
    recadrer(im, (250, 700, 1450, 2200), "S07-P2")          # la fumée et le haut des bougies au-dessus du texte
    im = Image.open(SRC / "U60-calendrier.jpg").convert("RGB")        # 1600 × 2400
    im = nettoyer_calendrier(im)
    im.save(OUT / "U60-propre.jpg", quality=95)
    recadrer(im, (200, 500, 1400, 2000), "S07-P3")
    im = Image.open(SRC / "U61-trophee.jpg").convert("RGB")           # 1600 × 2400
    recadrer(im, CADRE_TROPHEE, "S07-P4")
    im = Image.open(SRC / "U62-bravo.jpg").convert("RGB")             # 1600 × 2400
    im = flouter(im, ZONES_BRAVO)
    recadrer(im, CADRE_BRAVO, "S07-P5")
    im = Image.open(SRC / "U63-cle.jpg").convert("RGB")               # 1920 × 2400
    recadrer(im, (0, 0, 1920, 2400), "S07-P7")


def solaires():
    """U64 : solaires sur table blanche, détourées pour la phrase B."""
    im = Image.open(SRC / "U64-solaires.jpg").convert("RGB").crop(CADRE_SOLAIRES)
    alpha = garder_plus_grand(masque(im), aire_min=20000)
    enregistrer(im, alpha, "U64")
    print("U64")


# Réglés à l'œil sur les photos téléchargées (voir planche de contrôle)
ZONES_CALENDRIER = [(475, 690, 540, 758), (1040, 690, 1140, 758), (695, 895, 930, 945)]   # logo, « 2020 », « JAN 1 »
CADRE_TROPHEE = (200, 300, 1550, 1988)
ZONES_BRAVO = [(760, 1140, 1100, 1340), (950, 1230, 1110, 1600)]   # enseigne et affiche du fond
CADRE_BRAVO = (200, 650, 1600, 2400)
CADRE_SOLAIRES = (350, 550, 1950, 1200)

if __name__ == "__main__":
    desespere()
    pages_photos()
    solaires()
