# -*- coding: utf-8 -*-
"""Semaine 02 — textes validés par Togi le 09/10, photos, légendes. Seule source du texte des pages.

Balisage : [[mot]] souligné à la main · {{mot}} surligné · ~ espace insécable.
Règle de Togi (09/10) : un enfant de 10 ans doit comprendre chaque page ; « table de vente », jamais « comptoir ».
"""

SEMAINE = "02"

PHOTOS = {
    "U8": {"sujet": "La Joconde (Léonard de Vinci, domaine public) dans son cadre, photographiée au Louvre ; tableau seul, redressé",
           "id": "KHLTkeVtC3w", "auteur": "Oscar Nord",
           "url": "https://unsplash.com/photos/mona-lisa-painting-by-leonardo-da-vinci-KHLTkeVtC3w"},
    "U9": {"sujet": "Trois montures sur un plateau transparent (inscriptions des branches effacées : taille, modèle, nom du vendeur)",
           "id": "9AArXaWnKFQ", "auteur": "GlassesShop",
           "url": "https://unsplash.com/photos/a-pair-of-glasses-sitting-on-top-of-a-white-table-9AArXaWnKFQ"},
    "U10": {"sujet": "Girouette coq sur ciel bleu (toit retiré)",
            "id": "F6zRUXe9KEo", "auteur": "Yikai Sun",
            "url": "https://unsplash.com/photos/rooster-weather-vane-on-red-roof-F6zRUXe9KEo"},
    "U11": {"sujet": "Monture noire et dorée sur fond blanc (marque gravée sur la branche droite effacée)",
            "id": "PnsfHpDrY5o", "auteur": "Franco Antonio Giovanella",
            "url": "https://unsplash.com/photos/brown-framed-eyeglasses-on-white-surface-PnsfHpDrY5o"},
}

CTA_MARQUE_1 = "Lancez vos challenges."
CTA_MARQUE_2 = "L’app compte les ventes."
CTA_ACTION = "Demander un accès — sehoria.fr"
CTA_FREIN = "Premier mois offert, sans engagement, résiliable à tout moment"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

LIEN = "https://sehoria.fr"
FREIN_LEGENDE = "Premier mois offert, sans engagement, résiliable à tout moment."

PUBLICATIONS = [
    {
        "id": "S02-A1", "format": "A", "pilier": "Vendre à la table de vente", "slug": "choisir-sa-monture",
        "titre": "Aider un client à choisir sa monture", "palette": "terracotta",
        "pages": [
            {"type": "accroche", "photo": "U8",
             "bandeau1": "Elle sourit.", "titre": "Mais aime-t-elle", "bandeau2": "la [[monture]]~?",
             "main": "cinq siècles qu’elle hésite…"},
            {"type": "probleme", "dessin": "quinze-lunettes",
             "texte": "Quinze montures sur la table de vente.", "texte2": "Il les a toutes essayées.",
             "chute": "Il ne sait plus [[laquelle il préférait.]]"},
            {"type": "valeur", "numero": "1", "photo": "U9",
             "titre": "Trois montures sur la table, pas plus.", "chute": "Les autres retournent à leur place."},
            {"type": "valeur", "numero": "2", "dessin": "trois-cartes-une-croix",
             "titre": "Ne demandez pas laquelle il préfère.", "texte": "Demandez~:", "citation": "«~Laquelle on enlève~?~»",
             "chute": "Choisir, c’est dur. Enlever, c’est facile."},
            {"type": "valeur", "numero": "3", "dessin": "flou-net",
             "titre": "Sans ses lunettes, il voit flou.",
             "texte": "Prenez-le en photo avec son téléphone~: il se voit enfin net."},
            {"type": "valeur", "numero": "4", "dessin": "deux-cartes-une-coche",
             "titre": "Il hésite entre deux~?", "texte": "Donnez votre avis, et dites pourquoi.",
             "chute": "Il est venu pour être [[conseillé.]]"},
            {"type": "cta"},
        ],
        "legendes": {
            "instagram": (
                "Quinze montures essayées, et le client ne sait plus laquelle il préférait.\n"
                "Trois montures sur la table, pas plus. Puis une question~: «~Laquelle on enlève~?~»\n\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #monture #lunettes"),
            "linkedin": (
                "Quinze montures sur la table de vente. Le client les a toutes essayées, et il ne sait plus laquelle "
                "il préférait.\n\n"
                "Quatre réflexes pour l’aider à choisir~:\n"
                "→ Trois montures sur la table, pas plus. Les autres retournent à leur place.\n"
                "→ Ne demandez pas laquelle il préfère, demandez laquelle on enlève. Éliminer est plus facile que choisir.\n"
                "→ Sans ses lunettes, il voit flou. Prenez-le en photo avec son téléphone~: il se voit enfin net.\n"
                "→ S’il hésite entre deux, donnez votre avis et dites pourquoi. Il est venu pour être conseillé.\n\n"
                "Lancez vos challenges. L’app compte les ventes.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
    {
        "id": "S02-A2", "format": "A", "pilier": "Motiver l’équipe", "slug": "meteo-de-l-equipe",
        "titre": "La météo de l’équipe", "palette": "creme",
        "pages": [
            {"type": "accroche", "photo": "U10",
             "bandeau1": "Ce matin,", "titre": "quel temps fait-il", "bandeau2": "dans votre [[équipe]]~?"},
            {"type": "probleme", "dessin": "nuage-pluie",
             "texte": "Un vendeur fatigué ou contrarié, le client le sent à la table de vente.",
             "chute": "Et le responsable est souvent [[le dernier à le savoir.]]"},
            {"type": "valeur", "numero": "1", "dessin": "trois-meteos",
             "titre": "Avant d’ouvrir, chacun donne sa météo~:", "texte": "soleil, nuage ou pluie.",
             "chute": "Un mot, sans se justifier."},
            {"type": "valeur", "numero": "2", "dessin": "pluie-soleil",
             "q1": "Il pleut~?", "r1": "Il commence par l’atelier.",
             "q2": "Il fait beau~?", "r2": "Il accueille les clients."},
            {"type": "valeur", "numero": "3", "dessin": "seul-a-seul",
             "titre": "Un nuage~?", "texte": "Pas de question devant les autres.",
             "chute": "Un mot [[seul à seul]], dans la journée."},
            {"type": "valeur", "numero": "4", "dessin": "soleil-partage",
             "titre": "Le soleil, lui, se partage~:", "chute": "chacun dit une chose qui a bien marché hier."},
            {"type": "cta"},
        ],
        "legendes": {
            "instagram": (
                "Un vendeur fatigué, le client le sent à la table de vente.\n"
                "Avant d’ouvrir, chacun donne sa météo~: soleil, nuage ou pluie. Un mot, une minute.\n\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente #management"),
            "linkedin": (
                "Un vendeur fatigué ou contrarié, le client le sent à la table de vente. Et le responsable est souvent "
                "le dernier à le savoir.\n\n"
                "La météo de l’équipe, chaque matin avant d’ouvrir~:\n"
                "→ Chacun donne sa météo~: soleil, nuage ou pluie. Un mot, sans se justifier.\n"
                "→ Il pleut~? Il commence par l’atelier. Il fait beau~? Il accueille les clients.\n"
                "→ Un nuage~? Pas de question devant les autres~: un mot seul à seul, dans la journée.\n"
                "→ Le soleil se partage~: chacun dit une chose qui a bien marché hier.\n\n"
                "Lancez vos challenges. L’app compte les ventes.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
    {
        "id": "S02-B1", "format": "B", "pilier": "Motiver l’équipe", "slug": "oublie-le-prix",
        "titre": "La phrase qui porte — le prix et le conseil", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U11",
             "phrase": "Le client oublie le prix.", "chute": "Il se souvient du conseil."},
        ],
        "legendes": {
            "instagram": (
                "Le client oublie le prix. Il se souvient du conseil.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Le prix s’oublie. Le temps pris pour expliquer, pour essayer, pour dire franchement ce qui va~: "
                "ça, le client s’en souvient.\n\n"
                "À partager avec votre équipe."),
        },
    },
]


def legende_facebook(pub):
    """Charte §3 : la légende Instagram sans mots-clés ; « lien en bio » devient le lien suivi du frein (phrase B : sans lien)."""
    t = pub["legendes"]["instagram"]
    t = "\n".join(l for l in t.split("\n") if not l.startswith("#")).rstrip()
    if pub["format"] == "A":
        t = t.replace("Demander un accès~: lien en bio.", f"Demander un accès~: {LIEN}\n{FREIN_LEGENDE}")
    return t


for _p in PUBLICATIONS:
    _p["legendes"]["facebook"] = legende_facebook(_p)

SLUGS = {p["id"]: p["slug"] for p in PUBLICATIONS}
