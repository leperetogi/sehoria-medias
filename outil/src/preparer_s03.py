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


# ---------------- photos ajoutées le 12/10 au soir (plus de photos, accord de Togi) ----------------

def recadrer(code, boite, nom):
    im = Image.open(SRC / f"{code}.jpg").convert("RGB").crop(boite)
    im.save(OUT / f"{nom}.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": list(boite)}


def detourer_zone(code, boite, nom, aire_min=3000, prep=None):
    im = Image.open(SRC / f"{code}.jpg").convert("RGB")
    if prep:
        im = prep(im)
    im = im.crop(boite)
    alpha = garder_plus_grand(masque_rembg(im), aire_min=aire_min)
    bb = enregistrer(im, alpha, nom)
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "decalage": [boite[0] + bb[0], boite[1] + bb[1]]}


def effacer_boites(im, boites, rayon=6, critere=None):
    a = np.asarray(im.convert("RGB")).copy()
    m = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boites:
        m[y0:y1, x0:x1] = 255
    if critere is not None:
        m = np.where(critere(a), m, 0).astype(np.uint8)
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    return Image.fromarray(cv2.inpaint(a, m, rayon, cv2.INPAINT_TELEA))


def etiquette():
    """U15 : l'étiquette kraft et sa ficelle (étiquettes vierges : aucun texte)."""
    return detourer_zone("U15-etiquettes", (870, 0, 1200, 1170), "U15")


def route():
    """U16 : route mouillée la nuit, partie basse (reflets des lampadaires et des feux)."""
    return recadrer("U16-route-nuit", (0, 640, 1600, 1840), "U16")


def soleil_halo():
    """U17 : le soleil et son halo, en rond."""
    im = Image.open(SRC / "U17-soleil.jpg").convert("RGB")
    cx, cy, r = 1166, 893, 880
    f = 4
    grand = np.zeros((im.height * f, im.width * f), np.uint8)
    cv2.circle(grand, (cx * f, cy * f), r * f, 255, -1, cv2.LINE_AA)
    alpha = cv2.resize(grand, (im.width, im.height), interpolation=cv2.INTER_AREA)
    bb = enregistrer(im, alpha, "U17")
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]]}


def solaires():
    """U18b : lunettes de soleil enveloppantes (petit marquage gravé sur la branche droite effacé).
    U18 écartée : forme d'un modèle de marque connu, logo sur la branche et le verre."""
    prep = lambda im: effacer_boites(im, [(1560, 480, 1625, 545)], rayon=5)
    return detourer_zone("U18b-solaires", (350, 300, 2050, 1250), "U18", prep=prep)


def vider_disque(a, c, r, plume=3):
    """Remplace une étiquette ronde imprimée par un papier uni : ombrage lissé + grain (aucune lettre ne reste)."""
    af = a.astype(np.float32)
    lum = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    disque = np.zeros(lum.shape, np.uint8)
    cv2.circle(disque, c, r, 255, -1)
    encre = ((lum < 175) & (disque > 0)).astype(np.uint8) * 255
    encre = cv2.dilate(encre, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    lisse = cv2.GaussianBlur(cv2.inpaint(a, encre, 7, cv2.INPAINT_TELEA).astype(np.float32), (0, 0), 12)
    grain = np.random.default_rng(3).normal(0, 3.0, lum.shape).astype(np.float32)[..., None]
    w = cv2.GaussianBlur((disque > 0).astype(np.float32), (0, 0), plume)[..., None]
    return (af * (1 - w) + np.clip(lisse + grain, 0, 255) * w).astype(np.uint8)


def telephone():
    """U19 : téléphone à cadran ; l'étiquette du cadran (nom de la compagnie, consignes) devient un papier uni."""
    prep = lambda im: Image.fromarray(vider_disque(np.asarray(im).copy(), (1238, 578), 76))
    return detourer_zone("U19-telephone", (380, 120, 2400, 1600), "U19", prep=prep, aire_min=20000)


def etui():
    """U20 : lunettes rangées dans leur étui ouvert (le gris clair du couvercle, pris pour du fond, est rebouché)."""
    from scipy.ndimage import binary_fill_holes
    im = Image.open(SRC / "U20-etui.jpg").convert("RGB").crop((300, 760, 820, 1160))
    alpha = garder_plus_grand(masque_rembg(im))
    plein = binary_fill_holes(alpha > 127)
    alpha = np.where(plein & (alpha < 255), 255, alpha).astype(np.uint8)
    bb = enregistrer(im, alpha, "U20")
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]]}


def greffer_texture(a, boite, dy, sigma_bas=18, plume=10):
    """Efface un marquage en relief : grain du cuir pris dy px plus haut, ombrage de la zone conservé."""
    x0, y0, x1, y1 = boite
    af = a.astype(np.float32)
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = 255
    bas = cv2.GaussianBlur(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA).astype(np.float32), (0, 0), sigma_bas)
    src = np.roll(af, dy, axis=0)
    detail = src - cv2.GaussianBlur(src, (0, 0), sigma_bas)
    w = np.clip(cv2.GaussianBlur((m > 0).astype(np.float32), (0, 0), plume)[..., None] * 1.6, 0, 1)
    return (af * (1 - w) + np.clip(bas + detail, 0, 255) * w).astype(np.uint8)


def gommer_branche(a, boite, seuil=28):
    """Efface les inscriptions claires d'une branche sombre (top-hat), sans toucher au fil doré."""
    x0, y0, x1, y1 = boite
    z = a[y0:y1, x0:x1]
    lum = cv2.cvtColor(z, cv2.COLOR_RGB2GRAY)
    th = cv2.morphologyEx(lum, cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    branche = cv2.morphologyEx((lum < 90).astype(np.uint8), cv2.MORPH_CLOSE,
                               cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    branche = cv2.erode(branche, np.ones((3, 3), np.uint8))
    rouge_moins_bleu = z[..., 0].astype(int) - z[..., 2].astype(int)
    texte = ((th > seuil) & (branche > 0) & (rouge_moins_bleu < 25)).astype(np.uint8) * 255
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = cv2.dilate(texte, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    return cv2.inpaint(a, m, 4, cv2.INPAINT_TELEA)


def lunettes_etui_table():
    """U22 : étui en cuir et lunettes ; logo en relief de l'étui et inscriptions des branches effacés."""
    def prep(im):
        a = greffer_texture(np.asarray(im).copy(), (430, 1350, 675, 1540), 210)
        a = gommer_branche(a, (1218, 1355, 1302, 1442))
        a = gommer_branche(a, (1178, 1424, 1226, 1464))
        return Image.fromarray(a)
    return detourer_zone("U22-table", (300, 600, 1759, 2400), "U22", prep=prep, aire_min=20000)


def liege():
    """U21 : feuille blanche punaisée sur un tableau en liège (notes écrites et date coupées du cadre)."""
    r = recadrer("U21-liege", (250, 250, 1660, 1250), "U21")
    r["feuille"] = [605, 45, 1365, 955]   # dans le recadrage
    return r


def vitrine():
    """U23 : montures anciennes en présentoir ; silhouette floue (reflet) hors cadre, lettres du dos du livre effacées."""
    im = Image.open(SRC / "U23-vitrine.jpg").convert("RGB")
    clair = lambda a: cv2.cvtColor(a, cv2.COLOR_RGB2GRAY) > 75
    im = effacer_boites(im, [(850, 910, 940, 1005)], rayon=7, critere=clair)
    im.crop((0, 690, 1650, 1230)).save(OUT / "U23.jpg", quality=93)
    return {"taille": [1650, 540]}


if __name__ == "__main__":
    import sys
    faire = sys.argv[1:] or ["U12", "U13", "U14", "U15", "U16", "U17", "U18", "U19", "U20", "U21", "U22", "U23"]
    fichier = OUT / "reperes_s03.json"
    reperes = json.loads(fichier.read_text()) if fichier.exists() else {}
    for code, f in {"U12": buste, "U13": pendule, "U14": fauteuil, "U15": etiquette, "U16": route, "U17": soleil_halo,
                    "U18": solaires, "U19": telephone, "U20": etui, "U21": liege, "U22": lunettes_etui_table,
                    "U23": vitrine}.items():
        if code in faire:
            reperes[code] = f()
    fichier.write_text(json.dumps(reperes, indent=1), encoding="utf-8")
    print(json.dumps(reperes, indent=1))
