# -*- coding: utf-8 -*-
"""Semaine 02 — préparation des photos : filtre §5 (marques effacées), redressement, détourage.
Entrée : assets/photos/U8…U11 — sortie : assets/decoupes/U8…U11 (+ repères JSON)."""
import json

import cv2
import numpy as np
from PIL import Image

from rembg import remove

from preparer_photos import SRC, OUT, detourer, reduire, session

def effacer(im: Image.Image, zones, rayon=7, dilate=5) -> Image.Image:
    """zones : liste de (boite, critère) ; critère(a, lum, sat) -> masque booléen des pixels à effacer dans la boîte."""
    a = np.asarray(im.convert("RGB")).copy()
    af = a.astype(np.float32)
    lum = 0.299 * af[..., 0] + 0.587 * af[..., 1] + 0.114 * af[..., 2]
    sat = af.max(axis=2) - af.min(axis=2)
    m = np.zeros(a.shape[:2], np.uint8)
    for (x0, y0, x1, y1), crit in zones:
        sous = crit(af[y0:y1, x0:x1], lum[y0:y1, x0:x1], sat[y0:y1, x0:x1])
        m[y0:y1, x0:x1][sous] = 255
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilate + 1, 2 * dilate + 1)))
    return Image.fromarray(cv2.inpaint(a, m, rayon, cv2.INPAINT_TELEA)), int((m > 0).sum())

def joconde():
    """U8 : le tableau et son cadre, redressés (la photo est prise légèrement de biais)."""
    im = Image.open(SRC / "U8-joconde.jpg").convert("RGB")
    coins = np.float32([[1158, 1992], [1967, 2027], [1969, 3148], [1147, 3165]])  # HG, HD, BD, BG du cadre
    W, H = 816, 1150
    cible = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
    M = cv2.getPerspectiveTransform(coins, cible)
    a = cv2.warpPerspective(np.asarray(im), M, (W, H), flags=cv2.INTER_LANCZOS4)
    Image.fromarray(a).save(OUT / "U8.png")
    yeux = np.float32([[[1511, 2351]], [[1577, 2350]]])
    y = cv2.perspectiveTransform(yeux, M)[:, 0, :].tolist()
    return {"taille": [W, H], "oeil_g": y[0], "oeil_d": y[1]}

def trois_montures():
    """U9 : inscriptions des branches effacées (taille, modèle, nom du vendeur), puis détourage."""
    clair = lambda a, lum, sat: lum > 120
    blanc = lambda a, lum, sat: (lum > 110) & (sat < 45)  # lettres gris-bleu, neutres ; l'écaille est saturée
    im, n = effacer(Image.open(SRC / "U9-trois-montures.jpg"), [
        ((3100, 1380, 3360, 1490), clair),   # « …0 47□21-145 C1 » sur la branche noire
        ((3610, 1990, 3805, 2090), blanc),   # « □22-145 C2 » sur la branche écaille
        ((3440, 2100, 3565, 2172), lambda a, lum, sat: (lum > 75) & (sat < 35)),   # « HC-10… » (lettres plus sombres)
        ((2870, 2340, 2975, 2410), blanc),   # « Glas… » (nom du vendeur)
    ])
    im.save(OUT / "U9-retouche.jpg", quality=92)
    # photo gardée rectangulaire (bord déchiré à la mise en page) : le plateau transparent ne se détoure pas proprement
    reduire(im.crop((1950, 950, 5150, 3850)), 2400).save(OUT / "U9.jpg", quality=92)
    return {"pixels_effaces": n}

def girouette():
    """U10 : coq et flèche découpés sur le ciel (seuil : silhouette sombre sur ciel clair), toit retiré."""
    a = np.asarray(Image.open(SRC / "U10-girouette.jpg").convert("RGB"))[:2600]
    af = a.astype(np.float32)
    lum = 0.299 * af[..., 0] + 0.587 * af[..., 1] + 0.114 * af[..., 2]
    m = (lum < 118).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    garde = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 4000:
            garde[lab == i] = 1
    alpha = cv2.GaussianBlur((garde * 255).astype(np.uint8), (0, 0), 1.2)
    rgba = np.dstack([a, alpha])
    im = Image.fromarray(rgba, "RGBA")
    im = im.crop(im.getbbox())
    reduire(im, 2200).save(OUT / "U10.png")
    return {"composantes": int(n - 1)}

def monture():
    """U11 : marque gravée sur la branche droite effacée, puis détourage (verres gardés)."""
    im = Image.open(SRC / "U11-monture.jpg").convert("RGB")
    a = np.asarray(im).copy()
    # bande le long de la branche, de la charnière vers l'arrière
    p0, p1 = np.float32([3428, 2242]), np.float32([3506, 2166])
    d = (p1 - p0) / np.linalg.norm(p1 - p0)
    perp = np.float32([-d[1], d[0]])
    poly = np.int32([p0 + 22 * perp, p1 + 22 * perp, p1 - 22 * perp, p0 - 22 * perp])
    m = np.zeros(a.shape[:2], np.uint8)
    cv2.fillPoly(m, [poly], 255)
    # la branche est droite : on recopie le tronçon lisse situé plus loin le long de la branche (même largeur, même dorure)
    dx, dy = (95 * d).round().astype(int)
    ys, xs = np.nonzero(m)
    b = a.copy()
    b[ys, xs] = a[ys + dy, xs + dx]
    fondu = cv2.GaussianBlur(m.astype(np.float32) / 255.0, (0, 0), 2.5)[..., None]
    a = (a * (1 - fondu) + b * fondu).astype(np.uint8)
    im = Image.fromarray(a)
    im.save(OUT / "U11-retouche.jpg", quality=92)
    # détourage : masque rembg + masque « tout ce qui n'est pas le fond blanc » (les branches fines dorées échappent à rembg)
    zone = im.crop((1250, 900, 4300, 2900))
    zone = reduire(zone, 2400)
    z = np.asarray(zone).astype(np.float32)
    lum = 0.299 * z[..., 0] + 0.587 * z[..., 1] + 0.114 * z[..., 2]
    sat = z.max(axis=2) - z.min(axis=2)
    objet = ((lum < 200) | (sat > 40)).astype(np.uint8)
    objet = cv2.morphologyEx(objet, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    n_, lab, st, _ = cv2.connectedComponentsWithStats(objet, 8)
    garde = np.zeros_like(objet)
    for i in range(1, n_):
        if st[i, cv2.CC_STAT_AREA] > 3000:
            garde[lab == i] = 1
    from scipy.ndimage import binary_fill_holes
    garde = binary_fill_holes(garde).astype(np.uint8)
    rembg_alpha = np.asarray(remove(zone, session=session(), post_process_mask=True, only_mask=True).convert("L"))
    alpha = np.maximum(rembg_alpha, cv2.GaussianBlur(garde * 255, (0, 0), 1.0))
    alpha = np.where(binary_fill_holes(alpha > 127), np.maximum(alpha, 255 * (alpha > 0)), alpha).astype(np.uint8)
    out = zone.convert("RGBA")
    out.putalpha(Image.fromarray(alpha))
    out.crop(out.getbbox()).save(OUT / "U11.png")
    return {"pixels_recopies": int((m > 0).sum())}

if __name__ == "__main__":
    import sys
    faire = sys.argv[1:] or ["U8", "U9", "U10", "U11"]
    fichier = OUT / "reperes_s02.json"
    reperes = json.loads(fichier.read_text()) if fichier.exists() else {}
    for code, f in {"U8": joconde, "U9": trois_montures, "U10": girouette, "U11": monture}.items():
        if code in faire:
            reperes[code] = f()
    fichier.write_text(json.dumps(reperes, indent=1), encoding="utf-8")
    print(json.dumps(reperes, indent=1))
