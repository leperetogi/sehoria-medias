# -*- coding: utf-8 -*-
"""Textures du gabarit Sehoria : papier crème froissé, fond violet, feuille froissée.
Générées ici (aucune image tierce), graines fixes pour un rendu reproductible."""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

def hex2rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)

def relief_plis(w, h, seed, echelles=((9, 0.9, 0.050), (50, 0.45, 0.040), (160, 0.16, 0.030))):
    """Papier froissé puis déplié : somme de plis en V (droites qui s'estompent), à trois échelles."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    H = np.zeros((h, w), np.float32)
    M = max(w, h)
    for n, longueur, pente in echelles:
        for _ in range(n):
            px, py = rng.uniform(-0.1, 1.1) * w, rng.uniform(-0.1, 1.1) * h
            th = rng.uniform(0, np.pi)
            nx, ny = np.cos(th), np.sin(th)
            d = (xx - px) * nx + (yy - py) * ny
            t = (xx - px) * (-ny) + (yy - py) * nx
            L = rng.uniform(0.5, 1.0) * longueur * M
            a = rng.uniform(0.4, 1.0) * pente * M * rng.choice([-1.0, 1.0])
            H += a * np.sqrt(d * d / (M * M) + 1e-6) * np.exp(-(t / L) ** 2)
    # bosses douces
    H += gaussian_filter(rng.normal(0, 1, (h, w)).astype(np.float32), 60) * 0.25
    return H

def ombrage(H, lum=(-0.5, -0.7, 0.9)):
    gy, gx = np.gradient(H)
    n = np.stack([-gx, -gy, np.ones_like(H) * 0.02], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    l = np.array(lum, np.float32); l /= np.linalg.norm(l)
    s = n @ l
    return (s - np.median(s)) / (s.std() + 1e-9)

def papier(w, h, base, seed, force=6.0, grain_f=2.0, vignette=6.0, teinte=(1.0, 0.98, 1.04)):
    b = hex2rgb(base)
    s = ombrage(relief_plis(w, h, seed))
    s = gaussian_filter(s, 0.7)
    s = np.tanh(s * 0.9)                                   # plis nets, pas de brûlures
    rng = np.random.default_rng(seed + 5)
    g = gaussian_filter(rng.normal(0, 1, (h, w)), 0.6)
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - 0.45 * w) / w) ** 2 + ((yy - 0.35 * h) / h) ** 2)
    delta = s * force + g * grain_f - r * vignette
    img = b[None, None, :] + delta[..., None] * np.array(teinte)[None, None, :]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")

if __name__ == "__main__":
    import sys
    seeds = [11, 23, 37, 41]
    for i, seed in enumerate(seeds):
        papier(1080, 1350, "#F9F2E9", seed, force=8.0, grain_f=1.8, vignette=7.0).save(OUT / f"papier-creme-{i + 1}.png")
    papier(1080, 1350, "#4120CF", 5, force=7.0, grain_f=2.6, vignette=16.0, teinte=(0.8, 0.7, 1.0)).save(OUT / "fond-violet.png")
    papier(1000, 900, "#FBF5EF", 7, force=15.0, grain_f=2.2, vignette=4.0).save(OUT / "feuille-froissee.png")
    papier(760, 860, "#FFFBF4", 8, force=13.0, grain_f=2.0, vignette=3.0).save(OUT / "note-froissee.png")
    print("ok")
