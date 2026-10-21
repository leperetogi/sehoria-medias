# -*- coding: utf-8 -*-
"""Semaine 04 — préparation des photos : filtre §5 (retouches), recadrages, détourages.
Entrée : assets/photos/U33…U44 (téléchargées par GitHub le 21/10, photos validées par Togi le 21/10 à 8 h 19).
Sortie : assets/decoupes/U33…U44 (.png détourées, .jpg recadrées) + reperes_s04.json.

Vérifié au zoom le 21/10 :
- U35 (lunettes sur un ordinateur) : marquage gravé sur la branche gauche (effacé) ; icônes floues de l'écran
  (barre d'applications) et logo éventuel : hors cadre (recadrage sous l'écran).
- U37 (paire sur une table) : un visage réel sur l'écran de l'ordinateur, en haut à droite : hors cadre (§5).
- U42 (porte-bloc) : marque imprimée sur le feutre : hors cadre.
- Les autres : aucune marque, aucun texte, aucun visage."""
import json

import cv2
import numpy as np
from PIL import Image

from preparer_photos import SRC, OUT
from preparer_s03 import masque_rembg, garder_plus_grand, enregistrer


def recadrer_photo(src, boite, nom):
    im = Image.open(SRC / f"{src}.jpg").convert("RGB").crop(boite)
    im.save(OUT / f"{nom}.jpg", quality=93)
    return {"taille": list(im.size), "recadrage": list(boite)}


_SESSIONS = {}


def masque(im, modele=None):
    """Masque de détourage ; modele=None : celui des semaines précédentes (isnet-general-use)."""
    if modele is None:
        return masque_rembg(im)
    from rembg import new_session, remove
    if modele not in _SESSIONS:
        _SESSIONS[modele] = new_session(modele)
    a = np.asarray(remove(im, session=_SESSIONS[modele], post_process_mask=True, only_mask=True).convert("L")).copy()
    a[a < 12] = 0
    return a


def detourer(src, boite, nom, aire_min=20000, prep=None, modele=None):
    im = Image.open(SRC / f"{src}.jpg").convert("RGB").crop(boite)
    if prep:
        im = prep(im)
    alpha = garder_plus_grand(masque(im, modele), aire_min=aire_min)
    bb = enregistrer(im, alpha, nom)
    return {"taille": [bb[2] - bb[0], bb[3] - bb[1]], "recadrage": list(boite), "decalage": [boite[0] + bb[0], boite[1] + bb[1]]}


# ---------------- A1 · « C'est trop cher. » (noir et blanc, découpes) ----------------

def david():
    """U33 : le David de Michel-Ange, tête et buste (Jack Hunter, 1L4E_lsIb9Q). Œuvre du domaine public (§5)."""
    return detourer("U33-david", (0, 0, 1350, 1900), "U33")


def etiquette():
    """U34 : étiquette kraft vierge et sa ficelle (Brett Jordan, B9N22h2s0to) ; le prix barré est dessiné à la main."""
    return detourer("U34-etiquette", (300, 150, 2400, 1700), "U34")


def ecran():
    """U35 : lunettes transparentes posées sur un ordinateur portable (K8, r87zX1RWECQ).
    Marquage gravé sur la branche gauche effacé ; recadré sous l'écran (icônes de la barre d'applications hors cadre)."""
    a = np.asarray(Image.open(SRC / "U35-ecran.jpg").convert("RGB")).copy()
    m = np.zeros(a.shape[:2], np.uint8)
    cv2.fillPoly(m, [np.array([(312, 944), (326, 966), (468, 892), (456, 866)], np.int32)], 255)
    a = cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA)
    boite = (0, 690, 2400, 1600)
    Image.fromarray(a).crop(boite).save(OUT / "U35.jpg", quality=93)
    return {"taille": [boite[2] - boite[0], boite[3] - boite[1]], "recadrage": list(boite),
            "marquage_efface": [312, 866, 468, 966]}


def balance():
    """U36 : balance ancienne à deux plateaux (Eric Prouzet, UptDrWmASK0). Le détourage casse les fils fins des
    plateaux : on garde un morceau de photo (mur crème), bords déchirés à la mise en page."""
    return recadrer_photo("U36-balance", (0, 180, 1600, 2160), "U36")


# ---------------- A2 · « Qui a vendu cette paire ? » (polaroïds en couleur) ----------------

def paire():
    """U37 : paire noire sur une table en bois (Rainier Ridao, KFG_WwhQm7s). L'écran de l'ordinateur, où l'on voit
    un visage réel, reste hors du cadre (§5)."""
    return recadrer_photo("U37-paire", (180, 560, 1560, 1520), "U37")


def mains():
    """U38 : deux mains qui se tendent sur fond gris (lilartsy, 1KkhQ8uL28g) ; aucun visage."""
    return recadrer_photo("U38-mains", (0, 560, 1489, 1520), "U38")


def porte():
    """U39 : une main sur une porte vitrée qui s'ouvre (Meg, RTRAptk-iLk) ; aucun visage."""
    return recadrer_photo("U39-porte", (560, 0, 2400, 1596), "U39")


def monture():
    """U40 : monture ronde en métal, sur fond blanc (Jocelyn Morales, Mv7kokwzIMw) ; aucun marquage."""
    return recadrer_photo("U40-monture", (0, 520, 1603, 1880), "U40")


def carton():
    """U41 : boîte en carton ouverte (Harper Sunday, fYH4ShNxuQ8) ; aucun texte."""
    return recadrer_photo("U41-carton", (0, 0, 2400, 1600), "U41")


def porte_bloc():
    """U42 : porte-bloc, feuille blanche et crayon (Kelly Sikkema, zQCDJZLS-Ms). Le feutre (marque imprimée) reste
    hors du cadre."""
    r = recadrer_photo("U42-porte-bloc", (400, 300, 2000, 1420), "U42")
    # la feuille blanche, dans le recadrage (pour écrire la règle à la main dessus)
    r["feuille"] = [540 - 400, 440 - 300, 1880 - 400, 1365 - 300]
    return r


def cle():
    """U43 : clé ancienne sur fond clair (Everyday basics, GJY1eAw6tn8) ; détourée, pour la carte d'accès."""
    return detourer("U43-cle", (300, 300, 1300, 2300), "U43")


# ---------------- B · la phrase ----------------

def porte_monnaie():
    """U44 : porte-monnaie en cuir (Emrullah Ses, 9g7jaMTpgxo) ; détouré sans le bois flotté derrière
    (u2net : isnet ne garde que le rabat, le bas se confond avec le fond sombre)."""
    return detourer("U44-porte-monnaie", (340, 140, 1800, 1251), "U44", aire_min=40000, modele="u2net")


ETAPES = {"U33": david, "U34": etiquette, "U35": ecran, "U36": balance, "U37": paire, "U38": mains, "U39": porte,
          "U40": monture, "U41": carton, "U42": porte_bloc, "U43": cle, "U44": porte_monnaie}

if __name__ == "__main__":
    import sys
    fichier = OUT / "reperes_s04.json"
    reperes = json.loads(fichier.read_text()) if fichier.exists() else {}
    for code, f in ETAPES.items():
        if not sys.argv[1:] or code in sys.argv[1:]:
            reperes[code] = f()
            print(code, reperes[code])
    fichier.write_text(json.dumps(reperes, indent=1), encoding="utf-8")
