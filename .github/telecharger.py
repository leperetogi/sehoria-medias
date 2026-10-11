# -*- coding: utf-8 -*-
"""Télécharge les photos demandées dans demandes/SNN.txt vers SNN/<nom>.jpg.

Tourne sur GitHub Actions (les serveurs de GitHub, eux, peuvent joindre Unsplash,
Pexels et Wikimedia ; l'espace de travail de Claude, non).

Format d'une demande, une photo par ligne :
    U12-tour-eiffel  w7riMytN6Wk
    U13-penseur      https://unsplash.com/photos/le-penseur-gYYy_b3DFK4
    U16-penseur      https://images.unsplash.com/photo-1763936783251-4a3eb135f07f?ixid=…   (urls.raw du connecteur : le plus sûr)
    U14-gravure      https://upload.wikimedia.org/wikipedia/commons/a/ab/Fichier.jpg
    U15-montures     https://www.pexels.com/photo/lunettes-123456/
Les lignes vides et celles qui commencent par # sont ignorées.
Une photo déjà téléchargée n'est jamais retéléchargée.
Résultat de chaque ligne : SNN/_rapport.md.
"""
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
LARGEUR = 2400            # assez pour un découpage pleine page 1080 × 1350
MAX_OCTETS = 40 * 1024 * 1024
MAX_PAR_DEMANDE = 30
UA = "sehoria-medias/1.0 (telechargement de photos libres de droits; https://github.com/leperetogi/sehoria-medias)"

NOM = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,60}$")
ID_UNSPLASH = re.compile(r"^[A-Za-z0-9_-]{11}$")
HOTES = {"unsplash.com", "www.unsplash.com", "images.unsplash.com", "upload.wikimedia.org",
         "www.pexels.com", "pexels.com", "images.pexels.com"}


def url_source(source: str) -> str:
    """Transforme ce qui a été demandé en adresse de téléchargement."""
    if ID_UNSPLASH.match(source):
        return adresse_unsplash(source)
    m = re.match(r"^https://([^/]+)(/[^?#]*)?", source)
    if not m or m.group(1).lower() not in HOTES:
        raise ValueError("source non reconnue (ID Unsplash, ou lien Unsplash, Pexels, upload.wikimedia.org)")
    hote, chemin = m.group(1).lower(), (m.group(2) or "").rstrip("/")
    if hote.endswith("unsplash.com") and hote != "images.unsplash.com":
        chemin = re.sub(r"^/[a-z]{2}(-[A-Z]{2})?(?=/photos/)", "", chemin)   # unsplash.com/fr/photos/…
        if not chemin.startswith("/photos/"):
            raise ValueError("lien Unsplash attendu sous la forme unsplash.com/photos/…")
        ident = chemin.split("/")[2][-11:]   # l'identifiant est toujours les 11 derniers caractères
        if not ID_UNSPLASH.match(ident):
            raise ValueError("identifiant Unsplash introuvable dans le lien")
        return adresse_unsplash(ident)
    if hote.endswith("pexels.com") and hote != "images.pexels.com":
        m2 = re.search(r"(\d+)$", chemin)
        if not m2:
            raise ValueError("numéro de photo Pexels introuvable dans le lien")
        n = m2.group(1)
        return f"https://images.pexels.com/photos/{n}/pexels-photo-{n}.jpeg?auto=compress&cs=tinysrgb&w={LARGEUR}"
    if hote == "images.unsplash.com":
        return taille_unsplash(source)
    return source


def taille_unsplash(url: str) -> str:
    """Lien images.unsplash.com (urls.raw du connecteur) : on demande 2400 px en JPEG."""
    url = re.sub(r"[?&](w|q|fm)=[^&]*", "", url)
    if "?" not in url and "&" in url:
        url = url.replace("&", "?", 1)
    return url + ("&" if "?" in url else "?") + f"w={LARGEUR}&q=90&fm=jpg"


def adresse_unsplash(ident: str) -> str:
    """Identifiant Unsplash → adresse de l'image (le bouton « Télécharger » refuse les robots : 401)."""
    req = urllib.request.Request(f"https://unsplash.com/napi/photos/{ident}", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            infos = json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} sur la fiche de la photo : donner plutôt son lien images.unsplash.com (urls.raw)")
    if infos.get("premium") or infos.get("plus"):
        raise ValueError("photo Unsplash+ (payante) : à écarter")
    return taille_unsplash(infos["urls"]["raw"])


def telecharger(url: str) -> bytes:
    derniere = None
    for essai in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                donnees = r.read(MAX_OCTETS + 1)
            if len(donnees) > MAX_OCTETS:
                raise ValueError("fichier trop lourd (> 40 Mo)")
            return donnees
        except urllib.error.HTTPError as e:
            derniere = f"HTTP {e.code}"
            if e.code in (401, 403, 404, 410):
                break   # inutile d'insister (photo premium, supprimée ou privée)
        except Exception as e:  # réseau
            derniere = str(e)
        time.sleep(3 * (essai + 1))
    raise RuntimeError(derniere or "échec du téléchargement")


def enregistrer(donnees: bytes, dest: Path) -> str:
    im = Image.open(io.BytesIO(donnees))
    im.load()
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    if max(im.size) > LARGEUR:   # Wikimedia renvoie souvent l'original, parfois énorme
        r = LARGEUR / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=93)
    return f"{im.width} × {im.height}, {dest.stat().st_size // 1024} Ko"


def traiter(demande: Path) -> None:
    semaine = demande.stem.upper()
    if not re.match(r"^S\d{2}$", semaine):
        print(f"{demande.name} ignoré : le nom doit être SNN.txt")
        return
    dossier = RACINE / semaine
    dossier.mkdir(exist_ok=True)
    rapport = dossier / "_rapport.md"
    deja = rapport.read_text(encoding="utf-8").splitlines() if rapport.exists() else []
    # un échec n'est retenté que si la source a changé (sinon le rapport se remplirait de doublons)
    echecs = {}
    for l in deja:
        m = re.match(r"^- (\S+) ÉCHEC — .* — (\S+)$", l)
        if m:
            echecs[m.group(1)] = m.group(2)
    lignes = [l.strip() for l in demande.read_text(encoding="utf-8").splitlines()]
    lignes = [l for l in lignes if l and not l.startswith("#")][:MAX_PAR_DEMANDE]
    nouvelles = []

    def signaler(texte):
        if texte not in deja and texte not in nouvelles:
            nouvelles.append(texte)

    for ligne in lignes:
        morceaux = ligne.split()
        if len(morceaux) != 2:
            signaler(f"- ? — ligne illisible : « {ligne[:80]} » (attendu : nom source)")
            continue
        nom, source = morceaux
        if not NOM.match(nom):
            signaler(f"- ? — nom refusé : « {nom[:40]} » (lettres, chiffres, - et _)")
            continue
        dest = dossier / f"{nom}.jpg"
        if dest.exists() or echecs.get(nom) == source:
            continue
        try:
            infos = enregistrer(telecharger(url_source(source)), dest)
            nouvelles.append(f"- {nom} ok — {infos} — {source}")
        except Exception as e:
            raison = " ".join(str(e).split())[:200] or type(e).__name__
            nouvelles.append(f"- {nom} ÉCHEC — {raison} — {source}")
        print(nouvelles[-1])
    if nouvelles:
        entete = [] if deja else [f"# {semaine} — photos téléchargées", ""]
        rapport.write_text("\n".join(entete + deja + nouvelles) + "\n", encoding="utf-8")


if __name__ == "__main__":
    demandes = sorted((RACINE / "demandes").glob("*.txt"))
    for d in demandes:
        traiter(d)
    sys.exit(0)
