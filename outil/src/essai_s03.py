# -*- coding: utf-8 -*-
"""S03 — page 1 des deux carrousels en deux styles (actuel / affiche), pour le choix de Togi."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw, ImageFont
from mep_s03 import ESSAI_PAGE1
from rendu import rendre, resume, RACINE

pages = [f() for f in ESSAI_PAGE1]
dossier = RACINE / "build" / "essai_s03"
bilan = rendre(pages, "Sehoria S03 — page 1, deux styles", dossier, "page1", formats=["A"] * 4, essai=True)
print(resume(bilan))
# planche comparative 2 × 2 (actuel à gauche, affiche à droite)
ims = [Image.open(p["png"]).convert("RGB") for p in bilan["pages"]]
l, h, m, bandeau = 540, 675, 24, 70
planche = Image.new("RGB", (2 * l + 3 * m, 2 * (h + bandeau) + m), "#F3EEE8")
d = ImageDraw.Draw(planche)
police = RACINE / "node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2"
for i, im in enumerate(ims):
    col, lig = i % 2, i // 2
    x, y = m + col * (l + m), lig * (h + bandeau) + bandeau
    planche.paste(im.resize((l, h), Image.LANCZOS), (x, y))
    d.text((x, y - 44), ["A1 · ACTUEL", "A1 · AFFICHE", "A2 · ACTUEL", "A2 · AFFICHE"][i], fill="#26203A",
           font=ImageFont.load_default(size=30))
planche.save(dossier / "S03_page1_deux-styles.jpg", quality=92)
print(dossier / "S03_page1_deux-styles.jpg")
