# -*- coding: utf-8 -*-
"""Semaine 05 — préparation des images du format « photo plein cadre » (test S05) et de la phrase B.

Entrées :
- la vidéo de Togi du 28/10 « Conduite de nuit » : ../video/2026-10-30-changement-heure.mp4 (Reel publié le 28/10) ;
- assets/photos/U47-parebrise, U48-phare, U49-route-hiver (Unsplash, téléchargées par GitHub le 03/11,
  validées par Togi le 03/11 à 13 h 27 « on y va »). U46-route (téléchargée) n'est pas utilisée : 4×4 vu de face,
  plaque lisible et tours récentes en fond (§5).
Sorties : assets/decoupes/S05-*.jpg (pages pleine photo 1080 × 1350) et U48.png (phare détouré).

Images tirées de la vidéo (charte v2.3, visage de Togi) : seulement des moments sans incrustation (ni mème, ni
carte, ni gros mot animé) ; les sous-titres incrustés passent sous le dégradé du bas. L'arrière-plan est flouté
(masque de personne) : logo du fauteuil, objets de l'étagère et affiche du mur deviennent illisibles (§5)."""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from preparer_photos import SRC, OUT
from preparer_s03 import garder_plus_grand, enregistrer
from preparer_s04 import masque

RACINE = Path(__file__).resolve().parent.parent
VIDEO = RACINE.parent / "video" / "2026-10-30-changement-heure.mp4"
W, H = 1080, 1350

# page → (instant en s, haut du recadrage, hauteur du recadrage) ; largeur = hauteur × 0,8, centrée
IMAGES_VIDEO = {
    "S05-P1": (44.4, 520, 1350),   # regard caméra, sourire léger (« Après le permis »)
    "S05-P3": (23.5, 650, 1270),   # « pas le droit » ; la carte « Acuité » du haut reste hors cadre
    "S05-P5": (42.6, 800, 1120),   # « Envoyez-le » ; la fiche « Halos la nuit ? » (et son œil rond) hors cadre
    "S05-P6": (29.6, 520, 1350),   # il pointe la caméra (« à part vous »)
    "S05-P7": (5.3, 520, 1350),    # grand sourire
}


def image_video(t):
    tmp = OUT / f"_video_{t}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(VIDEO), "-frames:v", "1", "-y", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    return im


def flou_arriere_plan(im, rayon=16, assombrir=0.86, eclaircir=1.14):
    """Garde la personne nette et un peu éclaircie (la vidéo est tournée le soir) ; l'arrière-plan est flouté et
    assombri (effet portrait)."""
    m = masque(im, "u2net_human_seg").astype(np.float32) / 255.0
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255.0
    net = np.asarray(ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(eclaircir)).enhance(1.05)).astype(np.float32)
    flou = np.asarray(im.filter(ImageFilter.GaussianBlur(rayon))).astype(np.float32) * assombrir
    out = net * m[..., None] + flou * (1 - m[..., None])
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def pages_video():
    for nom, (t, y0, h) in IMAGES_VIDEO.items():
        im = image_video(t)
        w = round(h * 0.8)
        x0 = (im.width - w) // 2
        im = im.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.LANCZOS)
        flou_arriere_plan(im).save(OUT / f"{nom}.jpg", quality=94)
        print(nom, f"{t} s")


def pages_photos():
    # U49 : route de montagne en hiver, à la tombée de la nuit, phares allumés (Emmanuel Mavely, O1KiClaHi2A).
    # Voitures minuscules : aucune plaque ni marque lisible. Le virage et les voitures en haut, la neige en dessous.
    im = Image.open(SRC / "U49-route-hiver.jpg").convert("RGB")
    im.crop((0, 0, 1350, 1688)).resize((W, H), Image.LANCZOS).save(OUT / "S05-P2.jpg", quality=94)
    # U47 : feux flous vus à travers un pare-brise sale, la nuit (Teresa, bZe2MgfOURE). Aucune plaque, aucun texte.
    im = Image.open(SRC / "U47-parebrise.jpg").convert("RGB")
    im.crop((450, 0, 1730, 1600)).resize((W, H), Image.LANCZOS).save(OUT / "S05-P4.jpg", quality=94)
    print("S05-P2, S05-P4")


def phare():
    """U48 : phare de Yaquina Head, 1873 (Clay Banks, XdiNTvxhDVI) : auteur mort depuis plus de 70 ans (§5).
    Détouré avec sa maison de gardien, sans les herbes."""
    im = Image.open(SRC / "U48-phare.jpg").convert("RGB").crop((620, 940, 1140, 1880))
    alpha = garder_plus_grand(masque(im), aire_min=20000)
    enregistrer(im, alpha, "U48")
    print("U48")


if __name__ == "__main__":
    pages_video()
    pages_photos()
    phare()
