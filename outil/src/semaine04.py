# -*- coding: utf-8 -*-
"""Semaine 04 — publications du 27 au 31/10. Textes validés par Togi le 20/10 à 23 h 29 (« je valide »),
photos validées le 21/10 à 8 h 19. Seule source du texte des pages.

Nouveautés de la semaine (vidéo YouTube sur les carrousels, proposition acceptée par Togi le 20/10) :
- types de carrousel : A1 en avant/après, A2 en liste de cas (style « dossier », à tester) ;
- relance écrite à la main en bas des pages 2 à 5 (cliffhanger), sans couper de phrase : chaque page reste lisible seule ;
- page 1 : petit libellé « À ENREGISTRER » ou « À PARTAGER » ; page 6 : une demande d'enregistrement (A1) ou de
  partage (A2) ; la dernière page Sehoria (« Demander un accès ») ne change pas.

Balisage : [[mot]] souligné à la main · {{mot}} surligné · ~ espace insécable.
Règles d'or (charte §0) : la valeur dans chaque publication ; un enfant de 10 ans comprend tout.
« Table de vente », jamais « comptoir » ; « chamoisine », jamais « chiffon ». Opticiens vouvoyés ; phrase B sans « tu » ni « vous ».
Léa et Karim (A2) : prénoms inventés.
"""

SEMAINE = "04"

# Photos validées par Togi le 21/10 (téléchargées par GitHub — photos.py)
PHOTOS = {
    "U45": {"sujet": "Le Cri, Edvard Munch, 1893 (A1-01) — domaine public, reproduction Wikimedia Commons ; "
                     "en trois tons de la charte, signature et date hors cadre (choix de Togi du 21/10)",
            "id": "Commons : Edvard_Munch,_1893,_The_Scream,…_National_Gallery_of_Norway.jpg", "auteur": "Edvard Munch",
            "url": "https://commons.wikimedia.org/wiki/File:Edvard_Munch,_1893,_The_Scream,_oil,_tempera_and_pastel_on_cardboard,_91_x_73_cm,_National_Gallery_of_Norway.jpg"},
    "U33": {"sujet": "Le David de Michel-Ange — remplacé par le Cri le 21/10 (pas reconnu au premier coup d'œil), non utilisé",
            "id": "1L4E_lsIb9Q", "auteur": "Jack Hunter",
            "url": "https://unsplash.com/photos/marble-statue-of-man-looking-away-1L4E_lsIb9Q"},
    "U34": {"sujet": "Étiquette kraft vierge et sa ficelle (A1-02 : le prix qu'on baisse, dessiné)",
            "id": "B9N22h2s0to", "auteur": "Brett Jordan", "url": "https://unsplash.com/photos/gray-tag-B9N22h2s0to"},
    "U35": {"sujet": "Lunettes posées sur un ordinateur portable (A1-05 : sur écran toute la journée) ; marquage de "
                     "branche effacé, écran hors cadre",
            "id": "r87zX1RWECQ", "auteur": "K8",
            "url": "https://unsplash.com/photos/silver-framed-eyeglasses-on-white-table-r87zX1RWECQ"},
    "U36": {"sujet": "Balance ancienne à deux plateaux (A1-06 : on garde quoi, on enlève quoi)",
            "id": "UptDrWmASK0", "auteur": "Eric Prouzet",
            "url": "https://unsplash.com/photos/a-large-metal-object-sitting-on-top-of-a-wooden-table-UptDrWmASK0"},
    "U37": {"sujet": "Paire noire sur une table en bois, la pièce à conviction (A2-01) ; écran avec un visage hors cadre",
            "id": "KFG_WwhQm7s", "auteur": "Rainier Ridao",
            "url": "https://unsplash.com/photos/black-framed-eyeglasses-on-brown-wooden-table-KFG_WwhQm7s"},
    "U38": {"sujet": "Deux mains qui se tendent (A2-02 : chacun veut la vente)",
            "id": "1KkhQ8uL28g", "auteur": "lilartsy",
            "url": "https://unsplash.com/photos/two-hands-reaching-on-grey-background-1KkhQ8uL28g"},
    "U39": {"sujet": "Une main sur une porte vitrée (A2-03 : le client qui revient)",
            "id": "RTRAptk-iLk", "auteur": "Meg", "url": "https://unsplash.com/photos/person-holding-slide-door-RTRAptk-iLk"},
    "U40": {"sujet": "Une monture seule (A2-04 : la vente à deux)",
            "id": "Mv7kokwzIMw", "auteur": "Jocelyn Morales",
            "url": "https://unsplash.com/photos/silver-framed-eyeglasses-on-white-table-Mv7kokwzIMw"},
    "U41": {"sujet": "Boîte en carton ouverte (A2-05 : la paire rendue)",
            "id": "fYH4ShNxuQ8", "auteur": "Harper Sunday",
            "url": "https://unsplash.com/photos/an-open-cardboard-box-sitting-on-top-of-a-table-fYH4ShNxuQ8"},
    "U42": {"sujet": "Porte-bloc, feuille blanche et crayon (A2-06 : la règle écrite) ; feutre de marque hors cadre",
            "id": "zQCDJZLS-Ms", "auteur": "Kelly Sikkema",
            "url": "https://unsplash.com/photos/clipboard-pencil-and-pen-on-a-wooden-surface-zQCDJZLS-Ms"},
    "U43": {"sujet": "Clé ancienne (A2-07 : la carte d'accès)",
            "id": "GJY1eAw6tn8", "auteur": "Everyday basics",
            "url": "https://unsplash.com/photos/black-and-silver-skeleton-key-GJY1eAw6tn8"},
    "U44": {"sujet": "Porte-monnaie en cuir (B1)",
            "id": "9g7jaMTpgxo", "auteur": "Emrullah Ses", "url": "https://unsplash.com/photos/a-brown-leather-purse-9g7jaMTpgxo"},
}

CTA_MARQUE_1 = "Lancez vos challenges."
CTA_MARQUE_2 = "L’app compte les ventes."
CTA_ACTION = "Demander un accès — sehoria.fr"
CTA_FREIN = "Premier mois offert, sans engagement, résiliable à tout moment"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

LIEN = "https://sehoria.fr"
FREIN_LEGENDE = "Premier mois offert, sans engagement, résiliable à tout moment."

# Dernière page « Suivez » (décision de Togi du 23/10, après le bilan Metricool : aucune demande d'accès depuis le 6/10,
# 15 abonnés). Plus de « Demander un accès » sur les carrousels de conseil : la dernière page invite à suivre.
# L'accès reste dans la bio, et un post par mois parle du problème que règle Sehoria (ici S04-A2).
SUIVRE_1 = "Un conseil pour votre magasin,"
SUIVRE_2 = "chaque semaine."
SUIVRE_ACTION = "Suivez Sehoria"
SUIVRE_RAISON = "Pour ne pas rater le prochain."
SUIVRE_IG = "Un conseil pour votre magasin, chaque semaine~: suivez @sehoria.fr."
SUIVRE_FB = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."
SUIVRE_LI = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."

PUBLICATIONS = [
    {
        "id": "S04-A1", "format": "A", "pilier": "Vendre à la table de vente (répondre à « c’est trop cher »)",
        "type": "avant / après", "slug": "c-est-trop-cher", "titre": "« C’est trop cher. »", "palette": "creme",
        "pages": [
            {"type": "accroche", "photo": "U45", "coin": "À enregistrer", "geant": "C’est trop cher.",
             "texte": "Deux réponses possibles. Laquelle est [[la vôtre~?]]"},
            {"type": "probleme", "photo": "U34", "citation": "«~C’est trop cher.~»",
             "texte": "Le premier réflexe~: baisser le prix.",
             "chute": "Pour le client, ça veut dire~: «~J’avais raison.~»",
             "relance": "Ce qu’on répond d’habitude"},
            {"type": "avant", "tampon": "Avant", "citation": "«~Je peux vous faire une remise.~»",
             "texte": "Le client retient la leçon~: la prochaine fois, il demandera [[une remise.]]",
             "relance": "Et à la place~?"},
            {"type": "apres", "tampon": "Après · 1", "citation": "«~Trop cher par rapport à quoi~?~»",
             "texte": "Puis laissez-le parler.",
             "chute": "Sa réponse vous dit ce qui le gêne [[vraiment.]]",
             "relance": "Et ensuite~?"},
            {"type": "apres", "tampon": "Après · 2", "photo": "U35", "intro": "Reprenez ses mots~:",
             "citation": "«~Vous êtes sur écran toute la journée. Ces verres, c’est pour ça.~»",
             "chute": "Il ne voit plus un prix. Il voit [[sa journée.]]",
             "relance": "Il insiste~?"},
            {"type": "apres", "tampon": "Après · 3", "photo": "U36", "intro": "Pas de remise~:",
             "citation": "«~On garde quoi, on enlève quoi~?~»",
             "chute": "C’est lui qui [[choisit.]]",
             "enregistrer": "Enregistrez-le~: au prochain «~c’est trop cher~», vous aurez les mots."},
            {"type": "suivre"},
        ],
        "fin": "suivre",   # 23/10 : dernière page et légendes sans « Demander un accès »
        "legendes": {
            "instagram": (
                "À enregistrer pour le prochain «~c’est trop cher~».\n"
                "Pas de remise tout de suite. Demandez~: «~Trop cher par rapport à quoi~?~», puis reprenez ses mots.\n\n"
                + SUIVRE_IG + "\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente #conseilvente"),
            "linkedin": (
                "À enregistrer pour le prochain «~c’est trop cher~».\n\n"
                "Le premier réflexe, c’est la remise. Et le client retient la leçon~: la prochaine fois, il la demandera.\n\n"
                "Trois phrases à la place, à la table de vente~:\n"
                "→ «~Trop cher par rapport à quoi~?~» Puis laissez-le parler~: sa réponse dit ce qui le gêne vraiment.\n"
                "→ Reprenez ses mots~: «~Vous êtes sur écran toute la journée. Ces verres, c’est pour ça.~» "
                "Il ne voit plus un prix, il voit sa journée.\n"
                "→ Il insiste~? Pas de remise~: «~On garde quoi, on enlève quoi~?~» C’est lui qui choisit.\n\n"
                + SUIVRE_LI),
        },
        "repartage_togi": "Une remise donnée trop vite, le client s’en souvient à sa prochaine visite.",
        "musique": "piano léger, sans paroles, volume bas",
    },
    {
        "id": "S04-A2", "format": "A", "pilier": "Le comptage (Sehoria)", "type": "liste de cas, style dossier (essai)",
        "slug": "qui-a-vendu-cette-paire", "titre": "Qui a vendu cette paire\u00a0?", "palette": "dossier",
        "pages": [
            {"type": "accroche", "photo": "U37", "coin": "À partager", "titre": "Qui a vendu cette paire~?",
             "sous_titre": "Trois cas qui fâchent une équipe."},
            {"type": "probleme", "photo": "U38", "texte": "Une prime par vente, c’est simple.",
             "suite": "Jusqu’au jour où deux vendeurs disent~:", "citation": "«~Cette vente, c’est moi.~»",
             "relance": "Trois cas reviennent toujours"},
            {"type": "cas", "photo": "U39", "numero": "Cas n°~1", "titre": "Le client qui revient",
             "texte": "Lundi, Léa le conseille. Samedi, il achète avec Karim.",
             "tampon": "À décider", "question": "Léa, Karim, ou moitié-moitié~?",
             "relance": "Le cas n°~2, c’est chaque samedi"},
            {"type": "cas", "photo": "U40", "numero": "Cas n°~2", "titre": "La vente à deux",
             "texte": "Léa trouve la monture. Karim s’occupe des verres.",
             "tampon": "À décider", "question": "Une prime chacun, ou une prime partagée~?",
             "relance": "Le 3^e, personne n’y pense"},
            {"type": "cas", "photo": "U41", "numero": "Cas n°~3", "titre": "La paire rendue",
             "texte": "Karim touche sa prime. Puis le client rend ses lunettes.",
             "tampon": "À décider", "question": "La prime reste, ou elle part avec~?",
             "relance": "Alors, quelle règle~?"},
            {"type": "regle", "photo": "U42", "phrase1": "Il n’y a pas de bonne règle.",
             "phrase2": "Il y a une règle écrite [[avant.]]",
             "partager": "Envoyez-le à votre équipe~: la règle se décide ensemble."},
            {"type": "cta", "photo": "U43", "pont1": "Vous écrivez la règle.", "pont2": "L’app compte les ventes."},
        ],
        "legendes": {
            "instagram": (
                "À envoyer à votre équipe avant le prochain challenge.\n"
                "Le client qui revient, la vente à deux, la paire rendue~: trois cas où deux vendeurs disent "
                "«~c’est moi~». La règle s’écrit avant le premier cas.\n\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente #challengevente"),
            "linkedin": (
                "À envoyer à votre équipe avant le prochain challenge.\n\n"
                "Une prime par vente, c’est simple. Jusqu’au jour où deux vendeurs disent~: «~Cette vente, c’est moi.~»\n\n"
                "Trois cas à décider avant qu’ils arrivent~:\n"
                "→ Le client qui revient~: conseillé lundi par l’un, il achète samedi avec l’autre. La prime va à qui~?\n"
                "→ La vente à deux~: l’un trouve la monture, l’autre s’occupe des verres. Une prime chacun, "
                "ou une prime partagée~?\n"
                "→ La paire rendue~: la prime est touchée, puis le client rend ses lunettes. Elle reste, ou elle part avec~?\n\n"
                "Il n’y a pas de bonne règle. Il y a une règle écrite avant.\n\n"
                "Vous écrivez la règle. L’app compte les ventes.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
        "musique": "électro douce, sans paroles, volume bas",
    },
    {
        "id": "S04-B1", "format": "B", "pilier": "Vendre à la table de vente (phrase)", "slug": "une-question",
        "titre": "La phrase qui porte — c’est trop cher", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U44",
             "phrase": "Un «~c’est trop cher~» n’est pas un non.", "chute": "C’est une question."},
        ],
        "legendes": {
            "instagram": (
                "Un «~c’est trop cher~» n’est pas un non. C’est une question.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Samedi, à la table de vente~: «~C’est trop cher.~» Ce n’est pas la fin de la vente. "
                "Le client demande, à sa façon~: «~Pourquoi ce prix-là~?~» On lui répond, sans baisser le prix.\n\n"
                "À partager avec votre équipe."),
        },
        "musique": "au choix de Togi",
    },
]


def legende_facebook(pub):
    """Charte §3 : la légende Instagram sans mots-clés ; « lien en bio » devient le lien suivi du frein (phrase B : sans lien)."""
    t = pub["legendes"]["instagram"]
    t = "\n".join(l for l in t.split("\n") if not l.startswith("#")).rstrip()
    if pub.get("fin") == "suivre":
        t = t.replace(SUIVRE_IG, SUIVRE_FB)
    elif pub["format"] == "A":
        t = t.replace("Demander un accès~: lien en bio.", f"Demander un accès~: {LIEN}\n{FREIN_LEGENDE}")
    return t


for _p in PUBLICATIONS:
    _p["legendes"]["facebook"] = legende_facebook(_p)

SLUGS = {p["id"]: p["slug"] for p in PUBLICATIONS}
