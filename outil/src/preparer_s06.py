# -*- coding: utf-8 -*-
"""Semaine 06 — images du carrousel « Je vais réfléchir. » (format photo plein cadre) et de la phrase B.

Entrées (téléchargées par GitHub le 13/11 ; texte et photos envoyés à Togi le 10/11, publiés selon sa règle des
24 h acceptée le 13/11) :
- U52 : Johannes Vermeer, La Jeune Fille à la perle, vers 1665 (Mauritshuis), reproduction Wikimedia Commons,
  domaine public ;
- U53-boite-papiers (Nguyen Phuc Hau, 8bdwkFmieIs), U55-photo-telephone (Helena Lopes, 44hLIm8apFw),
  U56-stylo-plume (Aaron Burden, y02jEX_B0O0), U57-stylo-dore (Art Lasovsky, 8XddFc6NkBY) : Unsplash.
- U54-table-deux (Christin Hume, PNWp1dZ7sO0) : téléchargée, non utilisée (les deux personnes sont minuscules,
  en bas de l'image, sous le dégradé et le texte) ; la page 3 prend le regard de la Jeune Fille.
Retouches §5 : la marque gravée sur la plume de U56 est effacée. U57 : « Iridium point Germany » (pas une marque),
illisible une fois détouré. U55 : coque rose, aucun logo visible.
Sorties : assets/decoupes/S06-*.jpg (pages pleine image 1080 × 1350) et U57.png (stylo détouré)."""
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


def recadrer(im, boite, nom):
    x0, y0, x1, y1 = boite
    assert abs((x1 - x0) * 1.25 - (y1 - y0)) <= 2, (nom, boite)        # 4:5
    im.crop(boite).resize((W, H), Image.LANCZOS).save(OUT / f"{nom}.jpg", quality=94)
    print(nom, boite)


def vermeer():
    """Le visage reste au-dessus du dégradé (le bas de la page porte le texte)."""
    im = Image.open(SRC / "U52-vermeer.jpg").convert("RGB")            # 1920 × 2274
    recadrer(im, (200, 300, 1779, 2274), "S06-JF1")    # p. 1 : la tête entière qui se retourne
    recadrer(im, (520, 560, 1160, 1360), "S06-JF3")    # p. 3 : le regard, en gros plan
    recadrer(im, (300, 150, 1700, 1900), "S06-JF6")    # p. 6 : la tête, le turban, la perle
    recadrer(im, (440, 480, 1280, 1530), "S06-JF7")    # p. 7 : le visage, serré


def stylo_sans_marque():
    """U56 : la marque gravée sur la plume (haut de la plume) est effacée (§5)."""
    im = cv2.imread(str(SRC / "U56-stylo-plume.jpg"))
    zone = np.zeros(im.shape[:2], np.uint8)
    x0, y0, x1, y1 = 880, 280, 1140, 580
    gris = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
    zone[y0:y1, x0:x1] = (gris > 95).astype(np.uint8) * 255
    zone = cv2.dilate(zone, np.ones((9, 9), np.uint8))
    net = cv2.inpaint(im, zone, 9, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(net, cv2.COLOR_BGR2RGB))


def pages_photos():
    im = Image.open(SRC / "U53-boite-papiers.jpg").convert("RGB")      # 1600 × 2400
    recadrer(im, (0, 300, 1600, 2300), "S06-P2")
    im = Image.open(SRC / "U55-photo-telephone.jpg").convert("RGB")    # 1600 × 2400
    recadrer(im, (0, 250, 1600, 2250), "S06-P4")
    stylo = stylo_sans_marque()                                         # 2400 × 1802
    stylo.save(OUT / "U56-sans-marque.jpg", quality=95)
    recadrer(stylo, (300, 0, 1740, 1800), "S06-P5")
    recadrer(stylo, (0, 802, 800, 1802), "S06-SIG7")   # p. 7 de la version signature : l'écriture, sans visage


def stylo_dore():
    """U57 : stylo plume doré sur fond blanc, détouré pour la phrase B."""
    im = Image.open(SRC / "U57-stylo-dore.jpg").convert("RGB").crop((600, 700, 2400, 1150))
    alpha = garder_plus_grand(masque(im), aire_min=20000)
    enregistrer(im, alpha, "U57")
    print("U57")


if __name__ == "__main__":
    vermeer()
    pages_photos()
    stylo_dore()
