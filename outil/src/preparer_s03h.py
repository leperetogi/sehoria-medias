# -*- coding: utf-8 -*-
"""Hors-série S03h (lundi 19/10) — préparation des photos : filtre §5, détourage.
Entrée : assets/photos/U24b-bache.jpg — sortie : assets/decoupes/U24.png (+ reperes_s03h.json).

U24 (-ZIfQqO1K1o) et U24b (ezBhFaOL6BY, le secours proposé à Togi) ont été téléchargées.
Retenue : U24b, la voiture entière sous sa housse (silhouette complète, lisible d'un coup d'œil en découpe) ;
U24 ne montre que l'avant, coupé par le cadre. Aucune marque, aucun logo, aucune plaque visible (vérifié au zoom)."""
import json

from PIL import Image

from preparer_photos import SRC, OUT
from preparer_s03 import masque_rembg, garder_plus_grand, enregistrer


def voiture_bachee():
    """U24 : voiture sous sa housse, vue de trois quarts arrière ; on garde la voiture, rien de la rue."""
    im = Image.open(SRC / "U24b-bache.jpg").convert("RGB").crop((0, 1470, 1300, 2070))
    alpha = garder_plus_grand(masque_rembg(im), aire_min=40000)
    bb = enregistrer(im, alpha, "U24")
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "source": "U24b-bache (ezBhFaOL6BY)"}


def cafe():
    """U25 : tasse de café et carnet (p. 5). Recadrage sous le mot « NOTES » imprimé sur le carnet et sous les
    inscriptions des crayons : aucune lettre ne reste dans le cadre."""
    im = Image.open(SRC / "U25-cafe.jpg").convert("RGB").crop((360, 900, 2400, 2300))
    im.save(OUT / "U25.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": [360, 900, 2400, 2300],
            "carnet": [1110 - 360, 900 - 900, 2290 - 360, 1890 - 900]}   # couverture du carnet, dans le recadrage


def tournevis():
    """U26 : petit tournevis à manche transparent sur une table en bois (p. 6) ; aucune inscription.
    Le manche transparent se détoure mal (reflets) : on garde un morceau de photo rectangulaire, bords déchirés."""
    im = Image.open(SRC / "U26-tournevis.jpg").convert("RGB").crop((400, 320, 1940, 660))
    im.save(OUT / "U26.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": [400, 320, 1940, 660]}


if __name__ == "__main__":
    import sys
    fichier = OUT / "reperes_s03h.json"
    reperes = json.loads(fichier.read_text()) if fichier.exists() else {}
    for code, f in {"U24": voiture_bachee, "U25": cafe, "U26": tournevis}.items():
        if not sys.argv[1:] or code in sys.argv[1:]:
            reperes[code] = f()
    fichier.write_text(json.dumps(reperes, indent=1), encoding="utf-8")
    print(json.dumps(reperes, indent=1))
