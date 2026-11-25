# -*- coding: utf-8 -*-
"""Reel court et animé d'un carrousel (décision de Togi du 25/11, après trois semaines de Reels longs : 1 à 3 s de
visionnage, aucun abonné gagné).

Ce qui change par rapport à reel.py (38 s, pages fixes, fondu) :
- 15 s environ : l'accroche, les étapes en flashs, la chute, « Suivez » ; la page 2 est sautée par défaut ;
- ça bouge dès la première image : la page 1 part en gros plan et recule (la chute du titre apparaît pendant le
  recul), les autres pages avancent doucement ; passage d'une page à l'autre en glissé, comme un carrousel ;
- Instagram : vidéo sans musique (piste muette) : Togi publie depuis la notification Metricool et ajoute le son
  tendance du moment dans Instagram (le catalogue de l'API n'a que les musiques « usage commercial ») ;
  option --musique : la musique composée par reel.py (Facebook, publication automatique).

Usage (depuis outil/, après semaine.py) :
    python3 src/reel_court.py 08 S08-A1                 # pages 1,3,4,5,6,7, muet
    python3 src/reel_court.py 08 S08-A1 --musique       # avec la musique originale
    python3 src/reel_court.py 08 S08-A1 --pages 1,2,4,6,7
Sortie : livraison/SNN/<id>_<slug>_reel-court.mp4 (ou _reel-court-musique.mp4), 1080 × 1920, 30 i/s, H.264, AAC."""
import argparse
import importlib
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reel import musique, RACINE

W, H, HAUT = 1080, 1920, 170           # la page commence à 170 px du haut (au-dessus des boutons des Reels)
PW, PH = 1080, 1350
FPS = 30
ENCRE = (38, 32, 58)
GLISSE = 0.25                          # passage d'une page à l'autre


def lisse(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def vue(page, z, cx, cy):
    """La page vue avec un facteur z (1 = entière), centrée sur (cx, cy) en coordonnées de page."""
    lw, lh = PW / z, PH / z
    x0 = min(max(cx - lw / 2, 0), PW - lw)
    y0 = min(max(cy - lh / 2, 0), PH - lh)
    return page.resize((PW, PH), Image.BICUBIC, box=(x0, y0, x0 + lw, y0 + lh))


def toile(img_page, dx=0):
    t = Image.new("RGB", (W, H), ENCRE)
    t.paste(img_page, (dx, HAUT))
    return t


def plans(pages, durees):
    """Un plan par page : la page 1 recule (1,12 → 1), les autres avancent (1 → 1,05)."""
    out = []
    for k, (p, d) in enumerate(zip(pages, durees)):
        if k == 0:
            out.append((p, d, (1.12, 1.0), (PW / 2, PH * 0.42)))
        else:
            out.append((p, d, (1.0, 1.05), (PW / 2, PH * 0.45)))
    return out


def image_du_plan(plan, t):
    p, d, (z0, z1), (cx, cy) = plan
    a = lisse(t / max(d * 0.75, 0.01))
    return vue(p, z0 + (z1 - z0) * a, cx, cy)


def fabriquer(semaine, pid, numeros, avec_musique):
    txt = importlib.import_module(f"semaine{semaine}")
    slug = txt.SLUGS[pid]
    dossier = RACINE / "livraison" / f"S{semaine}" / f"{pid}_{slug}"
    toutes = sorted(dossier.glob(f"{pid}_{slug}_*.png"))
    pages = [Image.open(toutes[n - 1]).convert("RGB") for n in numeros]
    durees = []
    for i, n in enumerate(numeros):
        if i == 0:
            durees.append(3.2)                      # l'accroche
        elif i == len(numeros) - 1:
            durees.append(2.0)                      # « Suivez »
        elif i == len(numeros) - 2:
            durees.append(3.2)                      # la chute
        else:
            durees.append(2.8)                      # une étape, en flash
    pl = plans(pages, durees)
    ng = int(round(GLISSE * FPS))
    comptes = [int(round((d - (GLISSE if k < len(pl) - 1 else 0)) * FPS)) for k, (_, d, _, _) in enumerate(pl)]
    total = (sum(comptes) + ng * (len(pl) - 1)) / FPS   # durée exacte de la vidéo (le son suit)
    nom = f"{pid}_{slug}_reel-court" + ("-musique" if avec_musique else "") + ".mp4"
    sortie = RACINE / "livraison" / f"S{semaine}" / nom
    if avec_musique:
        son = RACINE / "build" / f"{pid}_musique_court.wav"
        musique(total, son)
        audio = ["-i", str(son)]
    else:
        audio = ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    cmd = (["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-"] + audio + ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.3f}", "-movflags", "+faststart", str(sortie)])
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n_images = 0
    for k, plan in enumerate(pl):
        d = plan[1]
        nb = comptes[k]
        for f in range(nb):
            proc.stdin.write(toile(image_du_plan(plan, f / FPS)).tobytes())
            n_images += 1
        if k < len(pl) - 1:                           # glissé vers la page suivante
            for f in range(ng):
                a = lisse((f + 1) / ng)
                dx = int(round(a * W))
                cur = image_du_plan(plan, (nb + f) / FPS)
                nxt = image_du_plan(pl[k + 1], 0.0)
                t = Image.new("RGB", (W, H), ENCRE)
                t.paste(cur, (-dx, HAUT))
                t.paste(nxt, (W - dx, HAUT))
                proc.stdin.write(t.tobytes())
                n_images += 1
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg a échoué")
    print(sortie.name, f"{n_images / FPS:.1f} s", "pages", numeros, "durées", durees,
          "musique originale" if avec_musique else "muet (son à ajouter dans Instagram)")
    return sortie


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("semaine")
    ap.add_argument("pid")
    ap.add_argument("--pages", default="1,3,4,5,6,7")
    ap.add_argument("--musique", action="store_true")
    a = ap.parse_args()
    fabriquer(a.semaine, a.pid, [int(x) for x in a.pages.split(",")], a.musique)
