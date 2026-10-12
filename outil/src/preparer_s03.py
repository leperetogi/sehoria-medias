# -*- coding: utf-8 -*-
"""Semaine 03 — préparation des photos : filtre §5, détourage, repères.
Entrée : assets/photos/U12…U14 — sortie : assets/decoupes/U12…U14 (+ reperes_s03.json)."""
import json

import cv2
import numpy as np
from PIL import Image

from preparer_photos import SRC, OUT, reduire, session
from rembg import remove


def masque_rembg(im: Image.Image, seuil_bas=12) -> np.ndarray:
    a = np.asarray(remove(im, session=session(), post_process_mask=True, only_mask=True).convert("L")).copy()
    a[a < seuil_bas] = 0
    return a


def garder_plus_grand(alpha: np.ndarray, aire_min=3000) -> np.ndarray:
    """Retire les petits morceaux détachés (reflets, objets voisins) du masque."""
    n, lab, st, _ = cv2.connectedComponentsWithStats((alpha > 127).astype(np.uint8), 8)
    garde = np.zeros(alpha.shape, bool)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= aire_min:
            garde |= lab == i
    garde = cv2.dilate(garde.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    return np.where(garde, alpha, 0).astype(np.uint8)


def enregistrer(rgb: Image.Image, alpha: np.ndarray, nom: str):
    """Recadre sur l'objet, enregistre le PNG, rend le décalage (pour reporter des repères)."""
    rgba = rgb.convert("RGBA")
    rgba.putalpha(Image.fromarray(alpha))
    bb = rgba.getbbox()
    rgba.crop(bb).save(OUT / f"{nom}.png")
    return bb


def buste():
    """U12 : buste drapé sur fond noir. Détourage, socle sombre retiré (coupe droite sous le drapé : le buste sort
    toujours par le bas de la page). Repères des yeux et de la bouche pour les lunettes et la bulle."""
    im = Image.open(SRC / "U12-buste.jpg").convert("RGB")
    alpha = garder_plus_grand(masque_rembg(im))
    # largeur du masque ligne par ligne : sous le drapé, le masque se resserre avant le socle sombre ; on coupe au plus étroit
    larg = (alpha > 127).sum(axis=1)
    lignes = np.nonzero(larg)[0]
    haut, bas = lignes[0], lignes[-1]
    debut = haut + int(0.68 * (bas - haut))
    lisse = np.convolve(larg, np.ones(15) / 15, mode="same")
    coupe = int(debut + np.argmin(lisse[debut:bas - 20]) - 4)
    alpha[coupe:] = 0
    bb = enregistrer(im, alpha, "U12")
    dx, dy = bb[0], bb[1]
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "coupe_socle": coupe,
            "oeil_g": [700 - dx, 582 - dy], "oeil_d": [900 - dx, 565 - dy], "bouche": [810 - dx, 780 - dy]}


CADRAN = ((854.4, 1043.7), (518.8, 643.0), 3.2)   # ellipse du cadran blanc (ajustée sur 8 points du bord)
BAGUE = 1.16                                       # + la bague de bronze autour


def pendule():
    """U13 : la pendule ne se détoure pas (bronze sombre sur fond sombre, socle mêlé aux objets voisins).
    On garde le cadran et sa bague de bronze, en ovale : l'heure se lit d'un coup d'œil.
    Le cadran ne porte aucune marque (vérifié au zoom)."""
    im = Image.open(SRC / "U13-pendule.jpg").convert("RGB")
    (cx, cy), (w, h), ang = CADRAN
    f = 4  # ellipse tracée à 4× puis réduite : bord lisse
    grand = np.zeros((im.height * f, im.width * f), np.uint8)
    cv2.ellipse(grand, ((cx * f, cy * f), (w * BAGUE * f, h * BAGUE * f), ang), 255, -1, cv2.LINE_AA)
    alpha = cv2.resize(grand, (im.width, im.height), interpolation=cv2.INTER_AREA)
    bb = enregistrer(im, alpha, "U13")
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "centre": [round(cx - bb[0], 1), round(cy - bb[1], 1)],
            "axes_cadran": [round(w / 2, 1), round(h / 2, 1)]}


POMMES = [  # contours des trois pommes de pin (pixels de la photo), tracés large
    [(700, 1116), (732, 1112), (768, 1134), (788, 1162), (788, 1262), (700, 1264), (656, 1264), (652, 1240),
     (680, 1218), (694, 1180), (688, 1148)],
    [(798, 1106), (846, 1104), (882, 1128), (899, 1168), (899, 1260), (780, 1260), (780, 1168)],
    [(898, 1128), (946, 1126), (992, 1158), (1003, 1200), (1003, 1280), (878, 1280), (880, 1200)],
]
BORD_SIEGE = 1225       # bord arrière du cannage (au-dessus : le mur)
POTEAU = (935, 983)     # montant du dossier, caché derrière la troisième pomme
DECALAGE_CANNAGE = 360  # cannage propre, même hauteur, 360 px plus à gauche


def fauteuil():
    """U14 : fauteuil en bois courbé (modèle de 1900 environ, aucune marque visible). Les trois pommes de pin posées
    sur le siège sont effacées, puis détourage : on ne garde que le fauteuil, rien de la maison autour."""
    im = Image.open(SRC / "U14-fauteuil.jpg").convert("RGB")
    a = np.asarray(im).copy()
    af = a.astype(np.float32)
    lum = 0.299 * af[..., 0] + 0.587 * af[..., 1] + 0.114 * af[..., 2]
    rb = af[..., 0] - af[..., 2]
    m = np.zeros(lum.shape, np.uint8)
    for poly in POMMES:
        cv2.fillPoly(m, [np.int32(poly)], 255)
    accoudoir = (rb < 25) & (lum > 120)           # bois peint gris clair : il passe devant la première pomme
    m = (m > 0) & ~accoudoir
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    dessus = yy < BORD_SIEGE
    poteau = m & dessus & (xx >= POTEAU[0]) & (xx <= POTEAU[1])
    siege = m & ~dessus
    mur = m & dessus & ~poteau
    b = a.copy()
    ys, xs = np.nonzero(poteau)
    b[ys, xs] = a[ys - 100, xs]                   # le montant est droit : on le prolonge vers le bas
    ys, xs = np.nonzero(siege)
    b[ys, xs] = a[ys, xs - DECALAGE_CANNAGE]      # cannage recopié, même rangée
    fondu = cv2.GaussianBlur((poteau | siege).astype(np.float32), (0, 0), 1.5)[..., None]
    b = (a * (1 - fondu) + b * fondu).astype(np.uint8)
    b = cv2.inpaint(b, mur.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)
    im2 = Image.fromarray(b)
    im2.save(OUT / "U14-retouche.jpg", quality=92)
    alpha = masque_rembg(im2)
    alpha[cv2.dilate(mur.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0   # derrière les pommes : le mur
    alpha = garder_plus_grand(alpha, aire_min=20000)
    bb = enregistrer(im2, alpha, "U14")
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "pixels_refaits": int(m.sum())}


if __name__ == "__main__":
    import sys
    faire = sys.argv[1:] or ["U12", "U13", "U14"]
    fichier = OUT / "reperes_s03.json"
    reperes = json.loads(fichier.read_text()) if fichier.exists() else {}
    for code, f in {"U12": buste, "U13": pendule, "U14": fauteuil}.items():
        if code in faire:
            reperes[code] = f()
    fichier.write_text(json.dumps(reperes, indent=1), encoding="utf-8")
    print(json.dumps(reperes, indent=1))
