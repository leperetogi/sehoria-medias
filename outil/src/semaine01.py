# -*- coding: utf-8 -*-
"""Semaine 01 — textes (brouillon à valider par Togi), photos, légendes.

Balisage dans les textes :
  [[mot]]  -> souligné à la main
  {{mot}}  -> surligné
  ~        -> espace insécable (avant : ; ! ? », après «, entre nombre et mot)
"""

SEMAINE = "01"

PHOTOS = {
    "U1": {"sujet": "Le Penseur (Rodin), sur ciel bleu",
           "id": "gYYy_b3DFK4", "auteur": "Alvin David",
           "url": "https://unsplash.com/photos/a-bronze-statue-of-the-thinker-against-a-blue-sky-gYYy_b3DFK4",
           "alt": "https://unsplash.com/photos/bronze-sculpture-of-a-man-in-deep-thought-DIZWO326kzc"},
    "U2": {"sujet": "Lunettes noires sur fond blanc",
           "id": "7WUQO_Dz0e8", "auteur": "pawan kumar",
           "url": "https://unsplash.com/photos/a-pair-of-black-glasses-sitting-on-top-of-a-white-table-7WUQO_Dz0e8",
           "alt": "https://unsplash.com/photos/a-pair-of-glasses-sitting-on-top-of-a-table--CqbjEPj6Q8"},
    "U3": {"sujet": "Vitrine de montures — ÉCARTÉE (§5 : marques et prix lisibles), remplacée par des cartes dessinées",
           "id": "ZdAopzAlj_g", "auteur": "Jan Kotlík",
           "url": "https://unsplash.com/photos/several-pairs-of-eyeglasses-on-a-lit-display-ZdAopzAlj_g"},
    "U4": {"sujet": "Sablier",
           "id": "5Hl5reICevY", "auteur": "Nathan Dumlao",
           "url": "https://unsplash.com/photos/clear-hour-glass-5Hl5reICevY"},
    "U5": {"sujet": "Paquet cadeau kraft",
           "id": "So6FM-ojMJM", "auteur": "Raymond Petrik",
           "url": "https://unsplash.com/photos/brown-gift-box-tied-with-white-string-and-red-seal-So6FM-ojMJM",
           "alt": "https://unsplash.com/photos/brown-gift-box-on-white-surface-mTkXSSScrzw"},
    "U6": {"sujet": "Le Stryge de Notre-Dame, gravure d'Auguste Lepère (Cleveland Museum of Art, domaine public)",
           "id": "nCmPWDkoI8Y", "auteur": "The Cleveland Museum of Art",
           "url": "https://unsplash.com/photos/gargoyle-overlooking-a-snowy-cityscape-with-birds-flying-nCmPWDkoI8Y"},
    "U7": {"sujet": "Tour Eiffel de jour, ciel bleu",
           "id": "w7riMytN6Wk", "auteur": "Pedro Gandra",
           "url": "https://unsplash.com/photos/eiffel-tower-paris-w7riMytN6Wk",
           "alt": "https://unsplash.com/photos/eiffel-tower-under-blue-sky-j-BaAX0opdw"},
}

CTA_ACTION = "Demander un accès — sehoria.fr"
CTA_FREIN = "Premier mois offert, sans engagement, résiliable à tout moment"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

PUBLICATIONS = [
    {
        "id": "S01-A1", "format": "A", "pilier": "Lancer ses challenges",
        "titre": "Votre premier challenge en 5 étapes", "palette": "creme",
        "pages": [
            {"type": "accroche", "photo": "U1",
             "bandeau1": "Un challenge de vente~?", "titre": "Vous y pensez", "bandeau2": "depuis des [[mois]].",
             "main": "lui aussi…", "label": "Votre premier, en 5~étapes"},
            {"type": "probleme", "photo": "U2",
             "citation": "«~On lance un challenge sur le photochromique~!~»",
             "texte": "Trois semaines plus tard, plus personne [[n’y voit clair]].",
             "main": "qui en est où~?"},
            {"type": "valeur", "dessin": "cartes-options", "label": "Étape 1/5",
             "titre": "Une cible claire.",
             "texte": "L’option que l’équipe ne propose pas naturellement.",
             "cartes": ["photochromique", "polarisant sur la 2^e paire", "anti-reflet"],
             "chute": "Plusieurs cibles~? Plusieurs challenges."},
            {"type": "valeur", "photo": "U4", "dessin": "infini", "label": "Étape 2/5",
             "titre": "Permanent ou périodique~?",
             "texte": "Permanent pour installer un réflexe. Périodique pour un temps fort, avec une date de fin annoncée.",
             "chute": "Décidez-le avant de lancer."},
            {"type": "valeur", "photo": "U5", "label": "Étape 3/5",
             "titre": "Une récompense juste.",
             "texte": "Annoncée avant le départ.",
             "chute": "Une prime par vente, pour chacun. Pas un lot pour un seul."},
            {"type": "valeur", "dessin": "note", "label": "Étape 4/5",
             "titre": "La règle, par écrit.",
             "texte": "Une vente annulée compte-t-elle~? Une vente faite à deux~?",
             "chute": "Tranchez avant, pas pendant."},
            {"type": "valeur", "dessin": "batons", "label": "Étape 5/5",
             "titre": "Un comptage quotidien.",
             "texte": "Chaque jour, pas en fin de mois.",
             "chute": "Chacun voit où il en est, sans attendre le recomptage."},
            {"type": "cta",
             "pont": "Le challenge, c’est vous.", "chute": "Le comptage, c’est l’app."},
        ],
        "legendes": {
            "instagram": (
                "Un premier challenge de vente se prépare avant d’être lancé. Cinq étapes~: une cible claire, "
                "permanent ou périodique, une récompense juste, une règle écrite, un comptage chaque jour.\n\n"
                "Le challenge, c’est vous. Le comptage, c’est l’app.\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #challengevente #equipedevente"),
            "linkedin": (
                "Le photochromique, le polarisant sur la deuxième paire, l’anti-reflet~: ce sont souvent les options "
                "que l’équipe ne propose pas naturellement. Un challenge sert à ça, à condition de le préparer.\n\n"
                "Cinq étapes pour un premier challenge en boutique~:\n"
                "1. Une cible claire~: l’option que l’équipe ne propose pas d’elle-même. Plusieurs cibles, plusieurs challenges.\n"
                "2. Permanent ou périodique~: permanent pour installer un réflexe, périodique pour un temps fort, "
                "avec une date de fin annoncée.\n"
                "3. Une récompense juste~: une prime par vente, pour chacun, annoncée avant le départ.\n"
                "4. Une règle écrite~: vente annulée, vente faite à deux… tranchées avant.\n"
                "5. Un comptage chaque jour, pas en fin de mois.\n\n"
                "Le challenge, c’est vous. Le comptage, c’est l’app.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
    {
        "id": "S01-A2", "format": "A", "pilier": "Le comptage",
        "titre": "Le tableau à bâtons, quinze ans après", "palette": "terracotta",
        "pages": [
            {"type": "accroche", "photo": "U6",
             "bandeau1": "Fin de mois.", "titre": "Qui recompte", "bandeau2": "le [[tableau à bâtons]]~?",
             "main": "encore moi…", "label": "Faites défiler"},
            {"type": "probleme", "dessin": "tableau",
             "texte": "Un bâton oublié, un trait effacé, une vente faite à deux…",
             "chute": "Le tableau ne tranche rien. Il ouvre le débat.",
             "main": "c’est à qui~?"},
            {"type": "valeur", "dessin": "devis", "label": "Réflexe 1/4",
             "titre": "Le devis fait foi.",
             "texte": "Une vente compte si elle a son devis. Le produit, la date, le montant~: tout y est.",
             "chute": "Plus de débat au recomptage."},
            {"type": "valeur", "dessin": "trait", "label": "Réflexe 2/4",
             "titre": "Tout de suite.",
             "texte": "Le bâton se trace au moment de la vente, pas le soir, de mémoire.",
             "main": "le soir, il en manque toujours une"},
            {"type": "valeur", "dessin": "devis-valides", "label": "Réflexe 3/4",
             "titre": "Validez au fil de l’eau.",
             "texte": "Une vente vérifiée le jour même, devis en main, ne revient pas en fin de mois.",
             "chute": "Le recomptage disparaît."},
            {"type": "valeur", "photo": "U2", "label": "Réflexe 4/4",
             "titre": "Chacun voit sa prime.",
             "texte": "Un bâton ne dit rien. Ce qui motive~: voir sa prime monter, pour soi.",
             "chute": "Un compte qu’on voit est un compte qu’on suit."},
            {"type": "cta",
             "pont": "Le challenge reste le vôtre.", "chute": "Le comptage, non."},
        ],
        "legendes": {
            "instagram": (
                "Quinze ans de bâtons sur un tableau. Et chaque fin de mois, la même question~: qui a vendu quoi~?\n"
                "Quatre réflexes pour compter juste~: le devis fait foi, la vente se note tout de suite, "
                "on valide au fil de l’eau, chacun voit sa prime.\n\n"
                "Le challenge reste le vôtre. Le comptage, non.\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #challengevente #equipedevente"),
            "linkedin": (
                "Quinze ans de bâtons sur un tableau. Quelqu’un doit tenir le compte, recompter en fin de mois, "
                "trancher quand deux vendeurs revendiquent la même vente.\n\n"
                "Quatre réflexes pour que le comptage ne soit plus un débat~:\n"
                "→ Le devis fait foi~: une vente compte si elle a son devis.\n"
                "→ La vente se note au moment où elle se fait, pas le soir, de mémoire.\n"
                "→ On valide au fil de l’eau, devis en main.\n"
                "→ Chacun voit sa prime monter, pour lui.\n\n"
                "Le challenge reste le vôtre. Le comptage, non.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
    {
        "id": "S01-B1", "format": "B", "pilier": "Motiver l’équipe",
        "titre": "La phrase qui porte — rivet par rivet", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U7",
             "phrase": "La tour Eiffel s’est montée rivet par rivet.", "chute": "Un mois de ventes aussi."},
        ],
        "legendes": {
            "instagram": (
                "La tour Eiffel s’est montée rivet par rivet. Un mois de ventes aussi.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Un mois de ventes ne se fait pas sur un coup d’éclat. Il se construit vente après vente, "
                "conseil après conseil.\n\n"
                "À partager avec votre équipe."),
        },
    },
]


def texte_visible(page, fmt):
    """Tout le texte qui apparaîtra sur la page, dans l'ordre de lecture (pour le comptage de mots)."""
    t = page["type"]
    if t == "cta":
        return [page["pont"], page["chute"], CTA_ACTION, CTA_FREIN, CTA_SIGNATURE]
    if t == "phrase":
        return [page["phrase"], page["chute"], PARTAGE, "sehoria.fr"]
    keys = ["label", "bandeau1", "titre", "bandeau2", "citation", "texte", "chute", "main"]
    return [page[k] for k in keys if page.get(k)] + [c.replace("^", "") for c in page.get("cartes", [])]
