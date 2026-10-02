# -*- coding: utf-8 -*-
"""Préparation des photos de la semaine : filtre §5 (retouches), détourage, recadrage.
Entrée : assets/photos/U*.jpg — sortie : assets/decoupes/U*.png"""
import numpy as np
import cv2
from PIL import Image
from pathlib import Path
from rembg import new_session, remove

RACINE = Path(__file__).resolve().parent.parent
SRC = RACINE / "assets" / "photos"
OUT = RACINE / "assets" / "decoupes"
OUT.mkdir(parents=True, exist_ok=True)
SESSION = None

def session():
    global SESSION
    if SESSION is None:
        SESSION = new_session("isnet-general-use")
    return SESSION

def reduire(im: Image.Image, maxi=2200) -> Image.Image:
    r = maxi / max(im.size)
    return im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS) if r < 1 else im

def detourer(im: Image.Image, seuil_bas=12, remplir_trous=False) -> Image.Image:
    masque = remove(im, session=session(), post_process_mask=True, only_mask=True)
    a = np.asarray(masque.convert("L")).copy()
    a[a < seuil_bas] = 0
    if remplir_trous:  # ex. verres des lunettes : on garde ce qu'on voit à travers
        from scipy.ndimage import binary_fill_holes
        plein = binary_fill_holes(a > 127)
        a = np.where(plein & (a < 255), 255, a).astype(np.uint8)
    rgba = im.convert("RGBA")
    rgba.putalpha(Image.fromarray(a))
    return rgba.crop(rgba.getbbox())

def retouche_lunettes(im: Image.Image) -> Image.Image:
    """§5 : effacer le liseré rouge/gris des branches et le marquage imprimé (signes distinctifs d'une marque)."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    sombre = (lum < 75).astype(np.uint8)
    rouge = ((a[..., 0] > 90) & (a[..., 0] - a[..., 1] > 35) & (a[..., 0] - a[..., 2] > 25)).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    ferme = cv2.morphologyEx(np.maximum(sombre, rouge), cv2.MORPH_CLOSE, k)
    a_combler = (ferme == 1) & (sombre == 0)
    # uniquement les petites zones enfermées dans la monture (liserés, marquages), pas les verres
    n, lab, stats, _ = cv2.connectedComponentsWithStats(a_combler.astype(np.uint8), 8)
    masque = np.zeros_like(sombre)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] < 60000:
            masque[lab == i] = 1
    masque = np.maximum(masque, cv2.dilate(rouge, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))))
    masque = cv2.dilate(masque, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    masque[lum > 215] = 0  # ne jamais toucher le fond ni les verres
    couleur_monture = np.median(a[sombre == 1], axis=0)
    b = a.copy()
    b[masque == 1] = couleur_monture
    b = cv2.inpaint(b.astype(np.uint8), (masque * 255).astype(np.uint8), 3, cv2.INPAINT_TELEA)
    return Image.fromarray(b)

def retouche_cachet(im: Image.Image, boite) -> Image.Image:
    """§5 : effacer le nom de marque embossé sur le cachet de cire (zone reprise puis fondue dans la cire)."""
    a = np.asarray(im.convert("RGB")).copy()
    x0, y0, x1, y1 = boite
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = 255
    b = cv2.inpaint(a, m, 31, cv2.INPAINT_TELEA).astype(np.float32)
    rng = np.random.default_rng(3)
    b += cv2.GaussianBlur(rng.normal(0, 6, a.shape[:2]).astype(np.float32), (0, 0), 1.4)[..., None]
    fondu = cv2.GaussianBlur(m.astype(np.float32) / 255.0, (0, 0), 14)[..., None]
    fondu = np.clip(fondu * 1.6, 0, 1)
    c = a.astype(np.float32) * (1 - fondu) + b * fondu
    return Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))

def principal():
    # U1 — Le Penseur (ciel) : détourage
    im = reduire(Image.open(SRC / "U1-penseur.jpg"))
    detourer(im).save(OUT / "U1.png")
    # U2 — Lunettes : retouche puis détourage
    im = Image.open(SRC / "U2-lunettes.jpg")
    im = retouche_lunettes(im)
    im.save(OUT / "U2-retouche.jpg", quality=92)
    detourer(reduire(im), remplir_trous=True).save(OUT / "U2.png")
    # U4 — Sablier : détourage
    detourer(reduire(Image.open(SRC / "U4-sablier.jpg")), remplir_trous=True).save(OUT / "U4.png")
    # U5 — Cadeau : texte du cachet effacé, puis recadrage sur le nœud (image rectangulaire)
    im = Image.open(SRC / "U5-cadeau.jpg")
    im = retouche_cachet(im, (1860, 2400, 2300, 2620))
    im.save(OUT / "U5-retouche.jpg", quality=92)
    im.crop((700, 1500, 3700, 5000)).save(OUT / "U5.jpg", quality=92)
    # U6 — Stryge : gravure entière (rectangulaire) + essai de détourage de la chimère
    im = Image.open(SRC / "U6-stryge.jpg")
    im.save(OUT / "U6.jpg", quality=92)
    detourer(reduire(im.crop((1750, 250, 3374, 3694)))).save(OUT / "U6-chimere.png")
    # U7 — Tour Eiffel : détourage
    detourer(reduire(Image.open(SRC / "U7-tour-eiffel.jpg"), 2600)).save(OUT / "U7.png")
    print("ok")

if __name__ == "__main__":
    principal()
