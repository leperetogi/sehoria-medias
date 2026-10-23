# -*- coding: utf-8 -*-
"""Refaire une seule page d'une semaine déjà livrée, sans les photos des autres pages (elles ne sont pas sur main).
usage : python3 src/une_page.py 04 S04-A1 7     → livraison/S04/une_page/S04-A1_<slug>_07.png + contrôles
Ajouté le 23/10 pour la dernière page « Suivez » de S04-A1."""
import importlib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rendu import rendre, resume, RACINE

num, pid, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
txt = importlib.import_module(f"semaine{num}")
mep = importlib.import_module(f"mep_s{num}")
pub = next(p for p in txt.PUBLICATIONS if p["id"] == pid)
fonction = mep.PUBLICATIONS_MEP[pid][n - 1]
travail = RACINE / "build" / "une_page" / f"{pid}-{n:02d}"
bilan = rendre([fonction()], pub["titre"], travail, f"{pid}-{n:02d}", formats=[pub["format"]])
print(resume(bilan))
dest = RACINE / "livraison" / f"S{txt.SEMAINE}" / "une_page"
dest.mkdir(parents=True, exist_ok=True)
cible = dest / f"{pid}_{txt.SLUGS[pid]}_{n:02d}.png"
shutil.copy(bilan["pages"][0]["png"], cible)
print(cible)
