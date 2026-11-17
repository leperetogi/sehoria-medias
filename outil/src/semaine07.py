# -*- coding: utf-8 -*-
"""Semaine 07 — le carrousel Sehoria du mois, jeudi 19/11 (12 h 30 ; page LinkedIn 8 h 30), et la phrase du samedi 21/11
(8 h 30). Seule source du texte des pages.

Sujet choisi par Claude (piste du journal, « Tu choisis » de Togi le 15/11) : pourquoi les challenges s'essoufflent au bout
de dix jours. Type liste, pilier « Lancer ses challenges ». Texte, légendes et photos envoyés à Togi le 15/11 à 16 h 40 ;
sans réponse, publiés selon la règle des 24 h. Le 15/11, la landing a changé : la page d'accès et les légendes reprennent
ses mots (« Essayer 30 jours », « Sans carte bancaire. Au mois, sans engagement, résiliable à tout moment. »).
Carrousel Sehoria du mois : il finit sur la page d'accès et ne part pas sur le profil LinkedIn de Togi (charte §3).
Page 1 : Le Désespéré de Courbet (domaine public), le visage du « jour 10 ».

Balisage : [[mot]] souligné · ~ espace insécable.  Opticiens vouvoyés ; phrase B sans « tu » ni « vous »."""

SEMAINE = "07"

PHOTOS = {
    "U58": {"sujet": "Gustave Courbet, Le Désespéré, 1843-1845, domaine public (A1-01, A1-06)",
            "id": "Commons : Gustave_Courbet_-_Le_Désespéré_(1843).jpg", "auteur": "Gustave Courbet"},
    "U65": {"sujet": "Deux bougies qu'on vient de souffler (A1-02)", "id": "y0w7tf6khI4",
            "auteur": "Kier in Sight Archives", "url": "https://unsplash.com/photos/y0w7tf6khI4"},
    "U60": {"sujet": "Calendrier mural, mois et année effacés (A1-03)", "id": "tG4waP7YiAg", "auteur": "Nathan Dumlao",
            "url": "https://unsplash.com/photos/tG4waP7YiAg"},
    "U61": {"sujet": "Trophée doré (A1-04)", "id": "bIiSTFBZEgQ", "auteur": "Gabriela Testa",
            "url": "https://unsplash.com/photos/bIiSTFBZEgQ"},
    "U62": {"sujet": "Trois femmes qui se tapent dans la main, enseigne du fond floutée (A1-05)", "id": "LIs-2xpMOHA",
            "auteur": "Ashford Marx", "url": "https://unsplash.com/photos/LIs-2xpMOHA"},
    "U63": {"sujet": "Clé dans une serrure (A1-07, page d'accès)", "id": "0juktkOTkpU", "auteur": "Amol Tyagi",
            "url": "https://unsplash.com/photos/0juktkOTkpU"},
    "U64": {"sujet": "Solaires sur table blanche, détourées (B1)", "id": "ODhxNCO8XHY", "auteur": "Anton Be",
            "url": "https://unsplash.com/photos/ODhxNCO8XHY"},
}

CREDIT_P1 = "Courbet · Le Désespéré"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

# Page d'accès (charte §3, carrousel Sehoria du mois) — mots de la landing relue le 15/11, ne se reformulent pas
PONT = "Vous dites bravo. L’app compte les ventes."
ACTION = "Essayer 30~jours — sehoria.fr"
FREIN = "Sans carte bancaire. Au mois, sans engagement, résiliable à tout moment."
LIEN = "https://sehoria.fr"

ENREGISTRER = "Enregistrez-le~: au dixième jour de votre prochain challenge, relisez-le."

PAGES = [
    {"type": "accroche", "photo": "S07-D1", "coin": "À enregistrer", "credit": CREDIT_P1,
     "titre": "Votre challenge démarre fort. Dix jours plus tard, plus personne n’y pense.",
     "bande": "plus personne n’y pense.", "glisser": "Faites glisser"},
    {"type": "point", "photo": "S07-P2", "titre": "Ce n’est pas l’équipe qui lâche. C’est le challenge.",
     "bande": "C’est le challenge.",
     "corps": "Il s’éteint presque toujours pour trois raisons. Chacune se répare dès demain.",
     "relance": "La première~?"},
    {"type": "point", "photo": "S07-P3", "titre": "Raison~1~: on compte en fin de mois.", "bande": "Raison~1~:",
     "corps": "Personne ne sait où il en est. Chaque soir, dites à chacun son total.",
     "relance": "Et la récompense~?"},
    {"type": "point", "photo": "S07-P4", "titre": "Raison~2~: un seul gagnant.", "bande": "Raison~2~:",
     "corps": "Au dixième jour, ceux qui sont derrière savent qu’ils ont perdu. Une prime par vente, pour chacun.",
     "relance": "La troisième, c’est vous."},
    {"type": "point", "photo": "S07-P5", "titre": "Raison~3~: vous n’en parlez plus.", "bande": "Raison~3~:",
     "corps": "Lancé lundi, oublié mardi. Chaque matin, une minute~: «~Hier~: trois deuxièmes paires. Bravo à tous.~»",
     "relance": "À retenir"},
    {"type": "chute", "photo": "S07-D6",
     "titre": "Un challenge ne meurt pas d’un coup. Il s’éteint quand plus personne ne compte.",
     "bande": "quand plus personne ne compte.", "enregistrer": ENREGISTRER},
    {"type": "acces", "photo": "S07-P7"},
]

LISTE_LI = (
    "Trois raisons, et quoi faire dès demain~:\n"
    "→ On compte en fin de mois~: personne ne sait où il en est. Chaque soir, dites à chacun son total.\n"
    "→ Un seul gagnant~: au dixième jour, ceux qui sont derrière savent qu’ils ont perdu. Une prime par vente, "
    "pour chacun.\n"
    "→ Vous n’en parlez plus~: lancé lundi, oublié mardi. Chaque matin, une minute~: «~Hier~: trois deuxièmes paires. "
    "Bravo à tous.~»\n\n")

PUBLICATIONS = [
    {
        "id": "S07-A1", "format": "A", "pilier": "Lancer ses challenges (carrousel Sehoria du mois)",
        "type": "liste, format photo plein cadre", "slug": "votre-challenge-s-eteint",
        "titre": "Votre challenge s’éteint", "palette": "photo", "pages": PAGES, "fin": "acces",
        "legendes": {
            "instagram": (
                ENREGISTRER + "\n"
                "Un challenge s’éteint pour trois raisons~: on compte en fin de mois, il n’y a qu’un gagnant, plus "
                "personne n’en parle. Le soir, dites à chacun son total. Une prime par vente, pour chacun. Le matin, "
                "une minute et un bravo.\n\n"
                "Essayer 30~jours~: lien en bio\n\n"
                "#opticien #opticienne #magasindoptique #challengevente #equipedevente"),
            "linkedin": (
                ENREGISTRER + "\n\n"
                "Votre challenge démarre fort. Dix jours plus tard, plus personne n’y pense. Ce n’est pas l’équipe "
                "qui lâche, c’est le challenge.\n\n" + LISTE_LI +
                "Un challenge ne meurt pas d’un coup. Il s’éteint quand plus personne ne compte.\n\n"
                + PONT + "\nEssayer 30~jours~: " + LIEN + "\n" + FREIN),
        },
        "musique": "intégrée au Reel (musique originale, sans paroles)",
    },
    {
        "id": "S07-B1", "format": "B", "pilier": "Vendre à la table de vente (phrase)", "slug": "premiere-fois",
        "titre": "La phrase qui porte — la première fois", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U64", "phrase": "La deuxième paire, on l’a proposée cent fois.",
             "chute": "Le client, lui, l’entend pour la première fois."},
        ],
        "legendes": {
            "instagram": (
                "La deuxième paire, on l’a proposée cent fois. Le client, lui, l’entend pour la première fois.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Samedi, à la table de vente~: la deuxième paire, c’est peut-être la vingtième fois qu’on la propose "
                "dans la journée. Pour le client assis en face, c’est la première. Même question, même sourire.\n\n"
                "À partager avec votre équipe."),
        },
        "musique": "Reel Facebook : musique originale, sans paroles",
    },
]


def legende_facebook(pub):
    """Charte §3 : la légende Instagram sans mots-clés ; « lien en bio » devient le lien suivi du frein."""
    t = pub["legendes"]["instagram"]
    t = "\n".join(l for l in t.split("\n") if not l.startswith("#")).rstrip()
    return t.replace("Essayer 30~jours~: lien en bio", f"Essayer 30~jours~: {LIEN}\n{FREIN}")


for _p in PUBLICATIONS:
    _p["legendes"]["facebook"] = legende_facebook(_p)

SLUGS = {p["id"]: p["slug"] for p in PUBLICATIONS}
