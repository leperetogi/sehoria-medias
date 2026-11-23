# -*- coding: utf-8 -*-
"""Semaine 08 — images du carrousel « Juste resserrer mes lunettes » (photo plein cadre) et de la phrase B.

Entrées (téléchargées par GitHub le 23/11 ; texte et photos envoyés à Togi le 22/11 à 20 h 06, publiés selon la règle
des 24 h) :
- U68g-louis14-hd : Hyacinthe Rigaud, Louis XIV, 1701 (Louvre), reproduction Wikimedia Commons, domaine public,
  2883 × 4018 (option « -hd » du relais, ajoutée le 23/11 : la version 1390 × 1975 annoncée était trop petite pour un
  gros plan) ; la toile seule, sans cadre ;
- U69b-chardin : Jean Siméon Chardin, Autoportrait aux bésicles, 1771 (Louvre), Commons Chardin_pastel_selfportrait.jpg
  (le fichier annoncé, Self-portrait_wearing_Glasses…, est l'autoportrait à l'abat-jour de 1775, daté en bas à droite) ;
  signature et date « 1771 » (vers x 1570-1700, y 2080-2240) hors cadre ;
- U70-lunettes-tendues (Nathan Dumlao, VJHb4QPBgV4) : p. 2, aucune marque visible ;
- U71-table-chaises (Noha Badawi, OYeJkHjM6ds) : p. 3 et page 7 de la version signature ;
- U72-gouttes (Karl Hedin, jgPcjw2tBVc) : p. 4 ;
- U76-monture-table (Josue Acevedo Maldonado, Gr5L64WSYZI) : B1, monture détourée (sans les vis du dessous).
Téléchargées, non utilisées : U68, U68b-f (Louis XIV, plus petites), U69, U69c, U73, U74, U75.
Sorties : assets/decoupes/S08-*.jpg (pages 1080 × 1350) et U76.png."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

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


def haut_puis_encre(im, nom, fondu=200):
    """Photo en largeur : elle occupe le haut de la page, puis se fond dans l'encre (le texte vient dessous)."""
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    fond = Image.new("RGB", (W, H), ENCRE)
    fond.paste(im, (0, 0))
    h = im.height
    a = np.zeros((H, W), np.float32)
    a[:h - fondu] = 1
    a[h - fondu:h] = np.linspace(1, 0, fondu)[:, None]
    out = np.asarray(fond, np.float32) * a[..., None] + np.array(ENCRE, np.float32) * (1 - a[..., None])
    Image.fromarray(out.astype(np.uint8)).save(OUT / f"{nom}.jpg", quality=94)
    print(nom, "en haut", im.size)


def louis():
    im = Image.open(SRC / "U68g-louis14-hd.jpg").convert("RGB")        # 2883 × 4018
    recadrer(im, CADRE_L1, "S08-L1")      # p. 1 : la tête, la perruque, la dentelle, l'hermine
    recadrer(im, CADRE_L6, "S08-L6")      # p. 6 : le regard
    recadrer(im, CADRE_L7, "S08-L7")      # p. 7 : la tête et les épaules


def chardin():
    im = Image.open(SRC / "U69b-chardin.jpg").convert("RGB")           # 1823 × 2400
    recadrer(im, CADRE_C5, "S08-C5")      # p. 5 : les bésicles au-dessus du texte ; signature et date hors cadre


def pages_photos():
    im = Image.open(SRC / "U70-lunettes-tendues.jpg").convert("RGB")   # 1600 × 2400
    recadrer(im, CADRE_P2, "S08-P2")
    im = Image.open(SRC / "U71-table-chaises.jpg").convert("RGB")      # 1600 × 2400
    haut_puis_encre(im.crop(CADRE_P3), "S08-P3")
    haut_puis_encre(im.crop(CADRE_SIG7), "S08-SIG7", fondu=220)
    im = Image.open(SRC / "U72-gouttes.jpg").convert("RGB")            # 2400 × 1382
    haut_puis_encre(im.crop(CADRE_P4), "S08-P4", fondu=180)


def monture():
    """U76 : monture brune sur table blanche, détourée pour la phrase B (les vis du dessous hors cadre)."""
    im = Image.open(SRC / "U76-monture-table.jpg").convert("RGB").crop(CADRE_MONTURE)
    alpha = garder_plus_grand(masque(im), aire_min=20000)
    enregistrer(im, alpha, "U76")
    print("U76")


# Réglés à l'œil sur les photos téléchargées (planches de contrôle du 23/11)
CADRE_L1 = (700, 520, 2000, 2145)        # visage vers y 250-490 de la page
CADRE_L6 = (1020, 760, 1660, 1560)       # le regard et la dentelle, le visage au-dessus du texte
CADRE_L7 = (860, 560, 1860, 1810)        # la tête, la dentelle, le haut de l'hermine
CADRE_C5 = (520, 470, 1720, 1970)        # bésicles vers y 430-640, au-dessus du dégradé ; signature (y ≥ 2080) hors cadre
CADRE_P2 = (100, 650, 1500, 2400)        # les lunettes tendues au-dessus du texte
CADRE_P3 = (100, 1400, 1600, 2400)       # la table et les deux chaises, en haut de page
CADRE_SIG7 = (0, 1000, 1600, 2400)       # idem, plus large (page signature)
CADRE_P4 = (300, 100, 2100, 1250)        # les deux verres mouillés, en haut de page
CADRE_MONTURE = (620, 260, 2100, 760)

if __name__ == "__main__":
    louis()
    chardin()
    pages_photos()
    monture()
