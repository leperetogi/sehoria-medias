# -*- coding: utf-8 -*-
"""Fait télécharger les photos de la semaine par GitHub, puis les range dans assets/photos/.

L'espace de travail de Claude ne peut pas joindre Unsplash, Pexels ni Wikimedia ; GitHub, si.
La branche `photos` du dépôt sert de relais (voir son README) :
  1. la liste est ajoutée à demandes/SNN.txt et poussée ;
  2. le robot GitHub télécharge chaque photo dans SNN/<nom>.jpg et écrit SNN/_rapport.md ;
  3. ce script attend le rapport et copie les photos réussies dans assets/photos/.

Usage (depuis outil/) :
    python3 src/photos.py 02 "U12-penseur=https://images.unsplash.com/photo-1763936783251-4a3eb135f07f?ixid=…"
    python3 src/photos.py 02                 # sans liste : récupère simplement ce qui est déjà téléchargé
La source, pour Unsplash : le lien images.unsplash.com (champ urls.raw du connecteur ; un identifiant seul
ou un lien unsplash.com/photos/… échoue, Unsplash répond 401 aux robots). Sinon : lien Pexels ou upload.wikimedia.org.
Mettre chaque argument entre guillemets (les liens contiennent des « & »).
"""
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent          # outil/
RELAIS = RACINE / "build" / "relais-photos"              # clone partiel de la branche photos (ignoré par git)
DEST = RACINE / "assets" / "photos"
DEPOT = "https://github.com/leperetogi/sehoria-medias"
NOM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,60}$")
ATTENTE_MAX = 600                                        # secondes
PAUSE = 10


def git(*args, check=True):
    return subprocess.run(["git", "-C", str(RELAIS), *args], check=check, capture_output=True, text=True)


def preparer_relais(semaine: str) -> None:
    if not (RELAIS / ".git").exists():
        RELAIS.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse",
                        "--branch", "photos", DEPOT, str(RELAIS)], check=True)
    git("sparse-checkout", "set", "--no-cone", "demandes/", f"{semaine}/")
    git("pull", "-q", "--rebase", "origin", "photos")


def lire_rapport(semaine: str) -> dict:
    """nom → ligne du rapport (ok ou ÉCHEC)."""
    f = RELAIS / semaine / "_rapport.md"
    if not f.exists():
        return {}
    res = {}
    for l in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- (\S+) (ok|ÉCHEC) — ", l)
        if m:
            res[m.group(1)] = l   # la dernière ligne d'un nom l'emporte (nouvel essai)
    return res


def demander(semaine: str, paires: list) -> list:
    demande = RELAIS / "demandes" / f"{semaine}.txt"
    existantes = demande.read_text(encoding="utf-8").splitlines() if demande.exists() else []
    deja = {l.split()[0]: l.split()[1] for l in existantes if len(l.split()) == 2 and not l.startswith("#")}
    ajout = []
    for nom, source in paires:
        if deja.get(nom) == source:
            continue
        if nom in deja:
            sys.exit(f"{nom} est déjà demandé avec une autre source ({deja[nom]}) : choisis un autre nom.")
        ajout.append(f"{nom} {source}")
    if not ajout:
        return []
    demande.parent.mkdir(exist_ok=True)
    demande.write_text("\n".join(existantes + ajout) + "\n", encoding="utf-8")
    git("add", str(demande))
    git("commit", "-q", "-m", f"Demande de photos {semaine}")
    for essai in range(3):
        if git("push", "-q", "origin", "HEAD:photos", check=False).returncode == 0:
            return [l.split()[0] for l in ajout]
        git("pull", "-q", "--rebase", "origin", "photos")
    sys.exit("Impossible de pousser la demande sur la branche photos.")


def main():
    if len(sys.argv) < 2 or not re.match(r"^\d{1,2}$", sys.argv[1]):
        sys.exit(__doc__)
    semaine = f"S{int(sys.argv[1]):02d}"
    paires = []
    for a in sys.argv[2:]:
        nom, _, source = a.partition("=")
        if not NOM.match(nom) or not source:
            sys.exit(f"Argument illisible : {a} (attendu : nom=source, nom en lettres, chiffres, - et _)")
        paires.append((nom, source))

    preparer_relais(semaine)
    nouveaux = demander(semaine, paires)
    attendus = {n for n, _ in paires}
    if nouveaux:
        print(f"Demande poussée ({len(nouveaux)} photo(s)). Le robot GitHub démarre, en général moins de 2 minutes…")
        debut = time.time()
        while not set(nouveaux) <= set(lire_rapport(semaine)):
            if time.time() - debut > ATTENTE_MAX:
                print("Toujours rien après 10 minutes. Relancer plus tard sans liste : python3 src/photos.py "
                      f"{int(sys.argv[1])} — ou vérifier l'onglet Actions du dépôt.")
                break
            time.sleep(PAUSE)
            git("pull", "-q", "--rebase", "origin", "photos")

    rapport = lire_rapport(semaine)
    DEST.mkdir(parents=True, exist_ok=True)
    copies = 0
    for nom, ligne in sorted(rapport.items()):
        if attendus and nom not in attendus:
            continue
        print(ligne)
        src = RELAIS / semaine / f"{nom}.jpg"
        if " ok — " in ligne and src.exists():
            shutil.copy2(src, DEST / src.name)
            copies += 1
    manquants = attendus - set(rapport)
    if manquants:
        print("Pas encore de réponse pour : " + ", ".join(sorted(manquants)))
    print(f"{copies} photo(s) dans {DEST.relative_to(RACINE)}/")
    sys.exit(1 if manquants or any(" ÉCHEC " in rapport.get(n, "") for n in attendus) else 0)


if __name__ == "__main__":
    main()
