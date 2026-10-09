# -*- coding: utf-8 -*-
"""Contrôles de la charte Sehoria (§3, §4 bis, §6) sur du texte brut ou extrait des fichiers."""
import re
import unicodedata

APOS = "'’ʼ"

def normaliser(t: str) -> str:
    t = t.replace("[[", "").replace("]]", "").replace("{{", "").replace("}}", "")
    t = t.replace("~", " ").replace(" ", " ").replace(" ", " ").replace(" ", " ")
    for a in APOS:
        t = t.replace(a, "'")
    t = unicodedata.normalize("NFC", t)
    return re.sub(r"[ \t]+", " ", t).strip()

PONCT_SEULE = re.compile(r"^[«»\"“”'’:;!?.,…—–\-→·/()\[\]*]+$")

def compter_mots(t: str) -> int:
    return sum(1 for tok in normaliser(t).split() if not PONCT_SEULE.match(tok))

ENSEIGNES = [
    "atol", "krys", "optic 2000", "optic2000", "afflelou", "grand optical", "generale d'optique",
    "générale d'optique", "lissac", "optical center", "opticiens mutualistes", "ecouter voir", "écouter voir",
    "carlance", "vision plus", "optical discount", "visual", "optique lafayette", "nouvel optic",
    "essilor", "luxottica", "essilorluxottica", "zeiss", "hoya", "nikon", "rodenstock", "bbgr", "novacel",
    "shamir", "seiko", "ray-ban", "rayban", "oakley", "safilo", "marcolin", "kering", "persol", "lindberg",
    "carrera", "tom ford", "prada", "gucci", "chanel", "dior", "sharpie", "excel", "lyleoo",
]

REGLES_GENERALES = [
    ("ERREUR", r"gamif|ludifi", "« gamification » interdit (§6)"),
    ("ERREUR", r"\d+\s?%|pour ?cent", "statistique de performance interdite (§6)"),
    ("ERREUR", r"\bmarges?\b", "aucune promesse sur la marge (§6)"),
    ("ERREUR", r"ind[ée]pendants?", "aucune restriction aux « indépendants » (§6)"),
    ("ERREUR", r"\bHT\b", "jamais « HT » (§6)"),
    ("ERREUR", r"plus choisi", "aucun badge « le plus choisi » (§6)"),
    ("ERREUR", r"2\s?000\s+opticiens", "formule interdite (§6)"),
    ("ERREUR", r"t[ée]moign", "aucun témoignage (§6)"),
    ("ERREUR", r"prix r[ée]seau|conditions? n[ée]goci", "aucun prix réseau ni condition négociée (§6)"),
    ("ERREUR", r"€|\beuros?\b", "montant : grille publique seulement, si le sujet l'exige (§6)"),
    ("ERREUR", r"\bmeilleur(e|s|es)?\b|n°\s?1\b|num[ée]ro un|\bleader\b|r[ée]volutionnaire|incontournable|\bn[o°]\s?1\b",
     "superlatif invérifiable (§6)"),
    ("ALERTE", r"\b(le|la|les) plus\b", "superlatif possible : à relire (§6)"),
    ("ALERTE", r"\bclassement\b", "l'écran Classement ne se montre pas : vérifier le contexte (§5)"),
    ("ALERTE", r"\b(1\d{3}|20[01]\d|202[0-6])\b", "année : aucune date antérieure au 8 août 2026 (§6)"),
    ("ALERTE", r"\b\d{1,2}\s+(janvier|f[ée]vrier|mars|avril|mai|juin|juillet|ao[uû]t|septembre|octobre|novembre|d[ée]cembre)\b",
     "date : vérifier (§6)"),
]

VOUVOIEMENT = ("ERREUR", r"\btu\b|\bt'[a-zéèêàâîôûh]|\bton\b|\btes\b|\btoi\b|\bta\b", "tutoiement : les opticiens sont vouvoyés")

REGLES_PHRASE_B = [
    ("ERREUR", r"\btu\b|\bt'[a-zéèêàâîôûh]|\bton\b|\bta\b|\btes\b|\btoi\b|\bvous\b|\bvotre\b|\bvos\b",
     "phrase de motivation : ni « tu » ni « vous » (instructions du projet)"),
    ("ERREUR", r"meilleur|champion|podium|\bbatt|gagnant|vainqueur|concurren|rival|classement|premier du",
     "aucune mise en compétition (§4 bis)"),
    ("ALERTE", r"\bpremi[eè]re?\b", "« premier » : vérifier qu'il n'y a pas de classement (§4 bis)"),
    ("ALERTE", r"vendre plus|plus de ventes|augment|doubl|tripl", "aucune promesse de ventes (§4 bis)"),
    ("ALERTE", r"\d", "chiffre dans la phrase : invérifiable ? (§4 bis)"),
]

MOTS_AUTORISES = {
    "Sehoria", "Eiffel", "Instagram", "LinkedIn", "Paris", "Notre-Dame", "Mont-Saint-Michel", "Rodin",
    "Penseur", "Stryge", "Lepère", "Unsplash",
}

def verifier(texte: str, contexte: str = "A"):
    """contexte : 'A' (carrousel), 'B-phrase', 'B' (reste de la phrase qui porte), 'legende'."""
    t = normaliser(texte)
    low = t.lower()
    constats = []
    for niveau, motif, msg in REGLES_GENERALES:
        for m in re.finditer(motif, t if motif == r"\bHT\b" else low):
            constats.append((niveau, msg, m.group(0)))
    for e in ENSEIGNES:
        if re.search(r"(?<![a-zà-ÿ])" + re.escape(e) + r"(?![a-zà-ÿ])", low):
            constats.append(("ERREUR", "nom d'enseigne, de fournisseur ou de marque (§5, §6)", e))
    niveau, motif, msg = VOUVOIEMENT
    for m in re.finditer(motif, low):
        constats.append((niveau, msg, m.group(0)))
    if contexte == "B-phrase":
        for niveau, motif, msg in REGLES_PHRASE_B:
            for m in re.finditer(motif, low):
                constats.append((niveau, msg, m.group(0)))
    if "lancez vos challenges" in low and "lancez vos challenges. l'app compte les ventes." not in re.sub(r"\s+", " ", low):
        constats.append(("ERREUR", "l'accroche de marque ne se reformule pas (§4)", "Lancez vos challenges…"))
    # Relevés à relire : nombres et noms propres
    nombres = sorted(set(re.findall(r"\d+(?:[.,/]\d+)?", t)))
    noms = set()
    for phrase in re.split(r"(?<=[.!?…:])\s+|\n", t):
        mots = phrase.split()
        for i, w in enumerate(mots):
            w2 = w.strip("«»\"“”'’:;!?.,…()")
            if i > 0 and w2[:1].isupper() and w2 not in MOTS_AUTORISES and not w2.isupper():
                noms.add(w2)
    return constats, nombres, sorted(noms)
