# -*- coding: utf-8 -*-
"""Rendu final de la semaine : une publication = un dossier (PNG par page + PDF), contrôles, légendes."""
import importlib
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rendu import rendre, resume, RACINE
from controle import verifier, normaliser

# usage : python3 src/semaine.py NN [S0N-A1 …]   (NN = numéro de semaine ; par défaut la dernière)
_args = sys.argv[1:]
_num = _args.pop(0) if _args and re.match(r"^\d+[a-z]?$", _args[0]) else "02"   # « 03h » : hors-série
_txt = importlib.import_module(f"semaine{_num}")
PUBLICATIONS, SEMAINE = _txt.PUBLICATIONS, _txt.SEMAINE
PUBLICATIONS_MEP = importlib.import_module(f"mep_s{_num}").PUBLICATIONS_MEP
SLUGS = getattr(_txt, "SLUGS", {"S01-A1": "votre-premier-challenge", "S01-A2": "tableau-a-batons", "S01-B1": "rivet-par-rivet"})
LIVRAISON = RACINE / "livraison" / f"S{SEMAINE}"

def legende_propre(t: str) -> str:
    return t.replace("~", " ")

def principal(seulement=None):
    LIVRAISON.mkdir(parents=True, exist_ok=True)
    bilans = {}
    for pub in PUBLICATIONS:
        pid = pub["id"]
        if seulement and pid not in seulement:
            continue
        fonctions = PUBLICATIONS_MEP[pid]
        assert len(fonctions) == len(pub["pages"]), pid
        pages = [f() for f in fonctions]
        formats = [pub["format"]] * len(pages)
        travail = RACINE / "build" / "final" / pid
        bilan = rendre(pages, pub["titre"], travail, pid, formats=formats)
        bilans[pid] = bilan
        print(f"\n=== {pid} — {pub['titre']} ({len(pages)} p.)\n" + resume(bilan))
        # livraison : PNG numérotés + PDF nommé
        dest = LIVRAISON / f"{pid}_{SLUGS[pid]}"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        for i, pg in enumerate(bilan["pages"], 1):
            shutil.copy(pg["png"], dest / f"{pid}_{SLUGS[pid]}_{i:02d}.png")
        shutil.copy(bilan["pdf"], dest / f"{pid}_{SLUGS[pid]}.pdf")
    # légendes (contrôlées elles aussi)
    lignes = [f"SEHORIA — SEMAINE {SEMAINE} — LÉGENDES", "=" * 40, ""]
    for pub in PUBLICATIONS:
        lignes += [f"{pub['id']} — {pub['titre']}", "-" * 40]
        for reseau in [r for r in ("instagram", "facebook", "linkedin") if r in pub["legendes"]]:
            leg = legende_propre(pub["legendes"][reseau])
            constats, _, _ = verifier(leg, "legende")
            erreurs = [c for c in constats if c[0] == "ERREUR"]
            assert not erreurs, (pub["id"], reseau, erreurs)
            if pub["format"] == "B":
                assert "Demander un accès" not in leg and "À partager avec votre équipe" in leg, pub["id"]
            else:
                assert ("lien en bio" in leg) if reseau == "instagram" else ("sehoria.fr" in leg), (pub["id"], reseau)
                if reseau != "instagram":
                    assert "#" not in leg and "Premier mois offert" in leg, (pub["id"], reseau)
            lignes += [f"[{reseau.upper()}]", leg, ""]
        lignes.append("")
    (LIVRAISON / f"S{SEMAINE}_legendes.txt").write_text("\n".join(lignes), encoding="utf-8")
    (RACINE / "build" / "final" / "bilan.json").write_text(json.dumps(bilans, ensure_ascii=False, indent=1), encoding="utf-8")
    return bilans

if __name__ == "__main__":
    principal(_args or None)
