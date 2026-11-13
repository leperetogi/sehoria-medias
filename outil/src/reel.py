# -*- coding: utf-8 -*-
"""Version Reel d'un carrousel (décision du 09-13/11 : Facebook et Instagram montrent les Reels aux non-abonnés).

Les pages 1080 × 1350 défilent, posées sur un fond encre 1080 × 1920 (9:16), placées assez haut pour que le bas de
la page reste au-dessus des boutons et de la légende des Reels. Durée de chaque page selon son nombre de mots
(lisible sans mettre en pause), fondu enchaîné court. Musique : composée ici (accords et arpège synthétisés),
sans paroles, volume bas — aucun droit de tiers (charte §2 : morceau sans paroles, libre de droits).

Usage (depuis outil/) : python3 src/reel.py 06 S06-A1
Sortie : livraison/SNN/<id>_<slug>_reel.mp4 (H.264, 30 i/s, AAC)."""
import importlib
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
RACINE = Path(__file__).resolve().parent.parent
W, H, HAUT = 1080, 1920, 170          # la page commence à 170 px du haut
FONDU = 0.4
SR = 44100


def durees(mots):
    d = []
    for i, m in enumerate(mots):
        if i == 0:
            d.append(4.0)                                  # l'accroche
        elif i == len(mots) - 1:
            d.append(4.5)                                  # « Suivez »
        else:
            d.append(round(2.2 + 0.16 * m, 1))             # ~25 mots → 6 s
    return d


# ---------------- musique ----------------

def note(f, t):
    return 440.0 * 2 ** ((f - 69) / 12) if t is None else 440.0 * 2 ** ((f - 69) / 12)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pluck(freq, dur, amp=0.18):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 3.2) * np.minimum(1, t * 200)
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t) + 0.12 * np.sin(6 * np.pi * freq * t)
    return amp * env * s


def pad(freqs, dur, amp=0.05):
    t = np.arange(int(SR * dur)) / SR
    env = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8)
    s = np.zeros_like(t)
    for f in freqs:
        for det in (-0.6, 0.6):
            s += np.sin(2 * np.pi * (f + det) * t) + 0.2 * np.sin(4 * np.pi * (f + det) * t)
    return amp * env * s / len(freqs)


def musique(duree, chemin):
    bpm = 72
    temps = 60 / bpm
    mesure = 4 * temps
    # la mineur — fa — do — sol : calme, sans tension
    accords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    n = int(SR * (duree + 2))
    out = np.zeros(n)
    t0, k = 0.0, 0
    while t0 < duree + 1:
        acc = accords[k % 4]
        i0 = int(t0 * SR)
        p = pad([mtof(m - 12) for m in acc] + [mtof(acc[0] - 24)], mesure + 0.6)
        out[i0:i0 + len(p)] += p[:max(0, min(len(p), n - i0))]
        motif = [acc[0], acc[1], acc[2], acc[1] + 12, acc[2], acc[1], acc[0] + 12, acc[2]]
        for j, m in enumerate(motif):
            ij = int((t0 + j * temps / 2) * SR)
            pl = pluck(mtof(m + 12), 1.6, amp=0.10 if j % 2 else 0.13)
            out[ij:ij + len(pl)] += pl[:max(0, min(len(pl), n - ij))]
        t0 += mesure
        k += 1
    # réverbération simple
    ir_t = np.arange(int(SR * 1.8)) / SR
    rng = np.random.default_rng(6)
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.0) * 0.035
    ir[0] = 1.0
    out = np.convolve(out, ir)[:n]
    out = out[: int(SR * duree)]
    fondu = int(SR * 1.5)
    out[:fondu] *= np.linspace(0, 1, fondu)
    out[-fondu * 2:] *= np.linspace(1, 0, fondu * 2)
    out = out / np.max(np.abs(out)) * 0.35            # volume bas
    stereo = np.stack([out, np.roll(out, 300)], axis=1)
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((stereo * 32767).astype(np.int16).tobytes())


# ---------------- vidéo ----------------

def reel(semaine, pid):
    txt = importlib.import_module(f"semaine{semaine}")
    slug = txt.SLUGS[pid]
    dossier = RACINE / "livraison" / f"S{semaine}" / f"{pid}_{slug}"
    pages = sorted(dossier.glob(f"{pid}_{slug}_*.png"))
    bilan = json.loads((RACINE / "build" / "final" / "bilan.json").read_text(encoding="utf-8"))[pid]
    mots = [p["mots"] for p in bilan["pages"]]
    assert len(pages) == len(mots), (len(pages), len(mots))
    d = durees(mots)
    total = sum(d) - FONDU * (len(d) - 1)
    son = RACINE / "build" / f"{pid}_musique.wav"
    musique(total, son)

    entrees, filtres = [], []
    for i, (png, di) in enumerate(zip(pages, d)):
        entrees += ["-loop", "1", "-t", str(di), "-i", str(png)]
        filtres.append(f"[{i}:v]scale={W}:-1,pad={W}:{H}:0:{HAUT}:color=0x26203A,setsar=1,fps=30,format=yuv420p[v{i}]")
    courant, t = "v0", d[0]
    for i in range(1, len(pages)):
        off = round(t - FONDU, 2)
        filtres.append(f"[{courant}][v{i}]xfade=transition=fade:duration={FONDU}:offset={off}[x{i}]")
        courant, t = f"x{i}", t + d[i] - FONDU
    sortie = RACINE / "livraison" / f"S{semaine}" / f"{pid}_{slug}_reel.mp4"
    cmd = (["ffmpeg", "-v", "error", "-y"] + entrees + ["-i", str(son), "-filter_complex", ";".join(filtres),
           "-map", f"[{courant}]", "-map", f"{len(pages)}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(sortie)])
    subprocess.run(cmd, check=True)
    print(sortie.name, f"{total:.1f} s", d)
    return sortie


if __name__ == "__main__":
    reel(sys.argv[1], sys.argv[2])
