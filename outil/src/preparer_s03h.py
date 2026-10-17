# -*- coding: utf-8 -*-
"""Hors-série S03h (lundi 19/10) — préparation des photos : filtre §5, détourage.
Entrée : assets/photos/U24b-bache.jpg — sortie : assets/decoupes/U24.png (+ reperes_s03h.json).

U24 (-ZIfQqO1K1o) et U24b (ezBhFaOL6BY, le secours proposé à Togi) ont été téléchargées.
Retenue : U24b, la voiture entière sous sa housse (silhouette complète, lisible d'un coup d'œil en découpe) ;
U24 ne montre que l'avant, coupé par le cadre. Aucune marque, aucun logo, aucune plaque visible (vérifié au zoom)."""
import json

import numpy as np
from PIL import Image

from preparer_photos import SRC, OUT
from preparer_s03 import masque_rembg, garder_plus_grand, enregistrer


def voiture_bachee():
    """U24 : voiture sous sa housse, vue de trois quarts arrière ; on garde la voiture, rien de la rue."""
    im = Image.open(SRC / "U24b-bache.jpg").convert("RGB").crop((0, 1470, 1300, 2070))
    alpha = garder_plus_grand(masque_rembg(im), aire_min=40000)
    bb = enregistrer(im, alpha, "U24")
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "source": "U24b-bache (ezBhFaOL6BY)"}


def cafe():
    """U25 : tasse de café et carnet (p. 5). Recadrage sous le mot « NOTES » imprimé sur le carnet et sous les
    inscriptions des crayons : aucune lettre ne reste dans le cadre."""
    im = Image.open(SRC / "U25-cafe.jpg").convert("RGB").crop((360, 900, 2400, 2300))
    im.save(OUT / "U25.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": [360, 900, 2400, 2300],
            "carnet": [1110 - 360, 900 - 900, 2290 - 360, 1890 - 900]}   # couverture du carnet, dans le recadrage


def tournevis():
    """U26 : petit tournevis à manche transparent sur une table en bois (p. 6) ; aucune inscription.
    Le manche transparent se détoure mal (reflets) : on garde un morceau de photo rectangulaire, bords déchirés."""
    im = Image.open(SRC / "U26-tournevis.jpg").convert("RGB").crop((400, 320, 1940, 660))
    im.save(OUT / "U26.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": [400, 320, 1940, 660]}


# ---------------- 17/10, 15 h : refonte « plus de photos de mise en situation » (photos validées par Togi) ----------------

ENCRE, CREME = (38, 32, 58), (251, 245, 239)


def fond_h1():
    """Page 1, pleine page : U27, voiture sous sa housse (Zachary Keimig, QJWk6LLOMdQ). Plaque d'immatriculation
    effacée (§5), noir et blanc passé en bichromie encre / crème, haut assombri pour le titre, bas fondu dans l'encre
    pour le texte. Sortie : assets/decoupes/H1-fond.jpg (1080 × 1350)."""
    import cv2
    from decoupes import gris_collage
    im = np.asarray(Image.open(SRC / "U27-housse-nuit.jpg").convert("RGB")).copy()
    m = np.zeros(im.shape[:2], np.uint8)
    m[1525:1685, 570:815] = 255                       # la plaque
    im = cv2.inpaint(im, m, 11, cv2.INPAINT_TELEA)
    im = Image.fromarray(im).crop((0, 300, 1600, 2300)).resize((1080, 1350), Image.LANCZOS)
    g = np.asarray(gris_collage(im, gamma=1.05, contraste=1.25)).astype(np.float32) / 255.0
    yy = np.arange(1350, dtype=np.float32)[:, None]
    haut = np.clip(1 - yy / 540, 0, 1) ** 1.2 * 0.8           # assombrit la maison derrière le titre
    bas = np.clip((yy - 860) / 230, 0, 1) ** 1.2              # fondu vers l'encre sous la voiture
    g = g * (1 - haut) * (1 - bas)
    xx = np.arange(1080, dtype=np.float32)[None, :]
    vign = 1 - 0.25 * np.clip(((xx - 540) / 600) ** 2 + ((yy - 640) / 800) ** 2, 0, 1)
    g = np.clip(g * vign, 0, 1)[..., None]
    out = np.array(ENCRE, np.float32) * (1 - g) + np.array(CREME, np.float32) * g
    grain = np.random.default_rng(5).normal(0, 4.0, (1350, 1080, 1)).astype(np.float32)
    Image.fromarray(np.clip(out + grain, 0, 255).astype(np.uint8)).save(OUT / "H1-fond.jpg", quality=94)
    return {"taille": [1080, 1350], "plaque_effacee": [570, 1525, 815, 1685]}


def porte():
    """U28 : un client à la porte d'un magasin d'optique, le soir (Isaac Owens, rOC-_ssUw2o). Recadrage serré sur la
    porte : l'enseigne du magasin, les marques des présentoirs et les affiches à visages restent hors du cadre (§5).
    Le client est de dos, les mains devant le visage : pas reconnaissable."""
    return recadrer_photo("U28-porte", (1690, 380, 2055, 1300), "U28")


def calendrier():
    """U29 : calendrier en gros plan, une date entourée (Glen Carrie, P1kP-BfIelI). Recadré sous le mois, l'année
    et les jours de la semaine (texte anglais, année antérieure au 8/8/2026, §6) : seuls les chiffres restent."""
    return recadrer_photo("U29-calendrier", (0, 680, 1350, 2000), "U29")


def message():
    """U30 : des mains qui écrivent un message sur un téléphone (Priscilla Du Preez, BjhUu6BpUZA) ; aucun visage,
    aucune marque visible."""
    return recadrer_photo("U30-message", (420, 120, 2040, 1380), "U30")


def lunettes_main():
    """U31 : une main tend une paire de lunettes (GlassesShop, fI0_v1y6rGE) ; aucun visage, aucune inscription."""
    return recadrer_photo("U31-lunettes-main", (500, 0, 2100, 1450), "U31")


def bande_h1(src, recadrage, nom="H1-bande.png", hauteur=800, effacer=(), haut_sombre=0.75, bas_sombre=0.7):
    """Page 1, version 3 (« le parallèle », 17/10 au soir) : bandeau photo du haut, 1080 × hauteur, en bichromie
    encre / crème, haut et bas assombris pour le texte, bord inférieur déchiré (le papier crème du bas apparaît
    dessous), ombre portée douce. effacer : boîtes à retoucher avant tout (plaques, logos), en pixels de la photo."""
    import cv2
    from decoupes import gris_collage
    im = np.asarray(Image.open(SRC / f"{src}.jpg").convert("RGB")).copy()
    for x0, y0, x1, y1 in effacer:
        m = np.zeros(im.shape[:2], np.uint8)
        m[y0:y1, x0:x1] = 255
        im = cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)
    im = Image.fromarray(im).crop(recadrage).resize((1080, hauteur), Image.LANCZOS)
    g = np.asarray(gris_collage(im, gamma=1.0, contraste=1.22)).astype(np.float32) / 255.0
    yy = np.arange(hauteur, dtype=np.float32)[:, None]
    xx = np.arange(1080, dtype=np.float32)[None, :]
    haut = np.clip(1 - yy / (hauteur * 0.45), 0, 1) ** 1.2 * haut_sombre
    bas = np.clip((yy - hauteur * 0.74) / (hauteur * 0.26), 0, 1) ** 1.3 * bas_sombre
    vign = 1 - 0.3 * np.clip(((xx - 540) / 620) ** 2 + ((yy - hauteur * 0.55) / (hauteur * 0.7)) ** 2, 0, 1)
    g = np.clip(g * (1 - haut) * (1 - bas) * vign, 0, 1)[..., None]
    rgb = np.array(ENCRE, np.float32) * (1 - g) + np.array(CREME, np.float32) * g
    rgb += np.random.default_rng(7).normal(0, 4.0, rgb.shape[:2] + (1,)).astype(np.float32)
    H = dechirer_bas(rgb, hauteur, nom)
    return {"taille": [1080, H], "source": src, "recadrage": list(recadrage)}


def dechirer_bas(rgb, hauteur, nom):
    """Bord inférieur déchiré : la photo s'arrête sur une ligne irrégulière, un liseré de papier blanc (le cœur du
    papier déchiré) dépasse dessous, puis une ombre douce tombe sur la page. rgb : tableau float (hauteur, 1080, 3).
    Écrit OUT/nom (PNG avec transparence, hauteur + 40 px) ; renvoie la hauteur de l'image."""
    import cv2 as _cv2
    H = hauteur + 40
    rng = np.random.default_rng(11)

    def ligne(base, amp, pas, graine):
        r = np.random.default_rng(graine)
        p = np.cumsum(r.normal(0, pas, 1081))
        p = p - np.linspace(p[0], p[-1], 1081)
        p = p / max(1e-6, np.abs(p).max()) * amp
        return (base + p + r.uniform(-1.6, 1.6, 1081)).astype(np.float32)[:1080]

    bord_photo = ligne(hauteur - 26, 12, 2.4, 11)
    liseré = np.convolve(rng.uniform(3, 13, 1080), np.ones(9) / 9, mode="same").astype(np.float32)
    bord_papier = bord_photo + liseré + rng.uniform(-1.2, 1.2, 1080).astype(np.float32)
    Y = np.arange(H, dtype=np.float32)[:, None]
    a_photo = np.clip(bord_photo[None, :] - Y + 0.5, 0, 1)
    a_papier = np.clip(bord_papier[None, :] - Y + 0.5, 0, 1)
    ombre = np.clip(bord_papier[None, :] + 8 - Y + 0.5, 0, 1) * (1 - a_papier)
    ombre = _cv2.GaussianBlur(ombre.astype(np.float32), (0, 0), 5) * 0.38
    photo = np.zeros((H, 1080, 3), np.float32)
    photo[:hauteur] = rgb
    papier = np.array((247, 243, 236), np.float32)
    col = photo * a_photo[..., None] + papier * (1 - a_photo[..., None])
    col = np.where(a_papier[..., None] > 0, col, 14.0)
    alpha = a_papier + ombre * (1 - a_papier)
    res = np.dstack([np.clip(col, 0, 255), np.clip(alpha, 0, 1) * 255]).astype(np.uint8)
    Image.fromarray(res, "RGBA").save(OUT / nom)
    return H


def rampe_h1(rendu="R1-rampe", nom="H1-piste.png", hauteur=1010, contraste=1.15, gamma=0.95, liseres=1.0):
    """Page 1, version 4 : la rampe 3D vide (rendue par rampe3d.py, aucune image tierce), passée dans la bichromie
    encre / crème des autres pages, liserés lumineux teintés terracotta (seule couleur vive), grain, bord déchiré."""
    im = Image.open(SRC / f"{rendu}.png").convert("RGB").resize((1080, hauteur), Image.LANCZOS)
    mq = Image.open(SRC / f"{rendu}-masque.png").convert("L").resize((1080, hauteur), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    g = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    g = np.clip((g - 0.5) * contraste + 0.5, 0, 1) ** gamma
    m = np.clip(np.asarray(mq).astype(np.float32) / 255.0 * 1.6 * liseres, 0, 1)[..., None]
    g = g[..., None]
    rgb = np.array(ENCRE, np.float32) * (1 - g) + np.array(CREME, np.float32) * g
    terra = np.array((192, 107, 62), np.float32)
    coeur = np.clip((m - 0.75) / 0.25, 0, 1)                       # le cœur du liseré reste clair, le halo est terracotta
    rgb = rgb * (1 - m) + (terra * (1 - coeur) + np.array((255, 214, 190), np.float32) * coeur) * m
    rgb += np.random.default_rng(13).normal(0, 4.5, rgb.shape[:2] + (1,)).astype(np.float32)
    H = dechirer_bas(rgb, hauteur, nom)
    return {"taille": [1080, H], "source": f"{rendu} (rendu 3D, gabarit/rampe3d.html)"}


def recadrer_photo(src, boite, nom):
    im = Image.open(SRC / f"{src}.jpg").convert("RGB").crop(boite)
    im.save(OUT / f"{nom}.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": list(boite)}



if __name__ == "__main__":
    import sys
    fichier = OUT / "reperes_s03h.json"
    reperes = json.loads(fichier.read_text()) if fichier.exists() else {}
    for code, f in {"U24": voiture_bachee, "U25": cafe, "U26": tournevis, "H1": fond_h1, "U28": porte,
                    "U29": calendrier, "U30": message, "U31": lunettes_main, "H1piste": rampe_h1}.items():
        if not sys.argv[1:] or code in sys.argv[1:]:
            reperes[code] = f()
    fichier.write_text(json.dumps(reperes, indent=1), encoding="utf-8")
    print(json.dumps(reperes, indent=1))
