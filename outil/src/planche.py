# -*- coding: utf-8 -*-
"""Planche de contrôle : toutes les pages d'une publication côte à côte (usage : python3 src/planche.py dossier sortie.jpg)."""
import sys
from pathlib import Path
from PIL import Image
pngs = sorted(Path(sys.argv[1]).glob("*.png"))
l, h, m = 432, 540, 12
cols = min(4, len(pngs))
rangs = (len(pngs) + cols - 1) // cols
pl = Image.new("RGB", (cols * l + (cols + 1) * m, rangs * h + (rangs + 1) * m), "#E9E4DE")
for i, p in enumerate(pngs):
    pl.paste(Image.open(p).convert("RGB").resize((l, h), Image.LANCZOS), (m + (i % cols) * (l + m), m + (i // cols) * (h + m)))
pl.save(sys.argv[2], quality=90)
