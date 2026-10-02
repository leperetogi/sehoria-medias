# -*- coding: utf-8 -*-
"""Planche d'essai du gabarit : 8 pages types, textes en attente de validation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mep_s01 import ESSAI
from rendu import rendre, resume, RACINE

pages = [f() for f in ESSAI]
formats = ["B" if f.__name__.startswith("b") else "A" for f in ESSAI]
bilan = rendre(pages, "Sehoria — essai du gabarit", RACINE / "build" / "essai", "essai", formats=formats, essai=True)
print(resume(bilan))
