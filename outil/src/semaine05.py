# -*- coding: utf-8 -*-
"""Semaine 05 — publications du jeudi 5/11 et du samedi 7/11. Seule source du texte des pages.

Bilan Metricool du 03/11 : vidéo la plus vue des 26, 28 et 30/10 = « Ray-Ban Meta Display » (30/10, 2 293 personnes
touchées) ; écartée par Togi le 03/11 (noms de marque et de produit, §5-6). Fiche faite sur la suivante,
« Conduite de nuit » (28/10 : 1 432 personnes touchées, 8 enregistrements, le meilleur score de la semaine).
Textes et photos validés par Togi le 03/11 à 13 h 27 (« on y va ») : phrase B option A.

Carrousel du jeudi = fiche de la vidéo (charte v2.2), ses phrases ; format test « photo plein cadre » (maquette du
25/10, accepté par Togi le 27/10).
03/11, 18 h 26 — Togi refuse son visage en page principale : « la valeur de ces images, c'est une photo de quelqu'un
que l'on reconnaît, une photo impactante » ; objectif : un maximum d'abonnés et d'interactions ; références
@mindshifter__ et @_mind__vision_. Claude ne met pas de photo de vraie célébrité (presse, films, mèmes) : Togi choisit
l'autoportrait de Van Gogh (page 1) et La Nuit étoilée (halos). Règles levées le même jour : noms de marques permis
dans le texte, citations sourcées permises, sujet libre chaque semaine.
Changements par rapport à la vidéo : « Depuis dimanche » retiré (le carrousel sort dix jours après) ; la réplique du
Corniaud retirée (extrait de film, §5) ; « comptoir » nulle part (§6).
Vérifié le 03/11 : permis B, acuité binoculaire ≥ 5/10 avec correction, arrêté du 28 mars 2022 (service-public).

S05-A1s : la version « signature » pour le profil LinkedIn de Togi (charte §3, test lancé à partir de S05) : pages
1 à 6 identiques mais sans logo Sehoria (son profil ne vend rien), page 7 = son nom, « opticien », « À partager ».

Balisage : [[mot]] souligné · ~ espace insécable.  Opticiens vouvoyés ; phrase B sans « tu » ni « vous »."""

SEMAINE = "05"

PHOTOS = {
    "U50": {"sujet": "Vincent van Gogh, Autoportrait, 1887 (Art Institute of Chicago), domaine public (A1-01, A1-03, A1-07)",
            "id": "Commons : Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project_(454045).jpg", "auteur": "Vincent van Gogh"},
    "U51": {"sujet": "Vincent van Gogh, La Nuit étoilée, 1889 (MoMA), domaine public (A1-05, A1-06, A1s-07)",
            "id": "Commons : Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg", "auteur": "Vincent van Gogh"},
    "U49": {"sujet": "Route de montagne en hiver à la tombée de la nuit, phares allumés (A1-02)", "id": "O1KiClaHi2A",
            "auteur": "Emmanuel Mavely", "url": "https://unsplash.com/photos/cars-driving-on-a-winding-road-in-winter-O1KiClaHi2A"},
    "U47": {"sujet": "Feux flous vus à travers un pare-brise sale, la nuit (A1-04)", "id": "bZe2MgfOURE",
            "auteur": "Teresa", "url": "https://unsplash.com/photos/blurred-traffic-lights-through-car-windshield-bZe2MgfOURE"},
    "U48": {"sujet": "Phare de Yaquina Head, 1873, détouré (B1)", "id": "XdiNTvxhDVI", "auteur": "Clay Banks",
            "url": "https://unsplash.com/photos/lighthouse-under-blue-sky-XdiNTvxhDVI"},
    "U46": {"sujet": "Téléchargée, non utilisée : 4×4 de face, plaque lisible, tours récentes en fond (§5)",
            "id": "Par7efrq8Tw", "auteur": "Sam Tsonis"},
}

CREDIT_P1 = "Van Gogh · autoportrait"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

SUIVRE_TITRE = "Un conseil pour votre magasin, chaque semaine."
SUIVRE_BANDE = "chaque semaine."
SUIVRE_ACTION = "Suivez Sehoria"
SUIVRE_RAISON = "Pour ne pas rater le prochain."
SUIVRE_IG = "Un conseil pour votre magasin, chaque semaine~: suivez @sehoria.fr."
SUIVRE_FB = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."
SUIVRE_LI = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."

PAGES = [
    {"type": "accroche", "photo": "S05-VG1", "coin": "À enregistrer", "credit": CREDIT_P1,
     "titre": "Certains de vos clients n’ont plus le droit de conduire. Et ils ne le savent pas.",
     "bande": "ne le savent pas.", "glisser": "Faites glisser"},
    {"type": "probleme", "photo": "S05-P2", "titre": "La nuit tombe une heure plus tôt.", "bande": "plus tôt.",
     "corps": "Vos clients rentrent en voiture dans le noir. Certains n’y voient plus assez pour conduire.",
     "relance": "Quoi leur dire~?"},
    {"type": "point", "photo": "S05-VG3", "titre": "1. La loi des 5/10.", "bande": "1.",
     "corps": "Moins de 5/10 avec les deux yeux et ses lunettes~: pas le droit de conduire. Mesurez, et dites-le-lui.",
     "relance": "Ce n’est pas sa vue~?"},
    {"type": "point", "photo": "S05-P4", "titre": "2. Le pare-brise.", "bande": "2.",
     "corps": "Avant d’accuser ses lunettes, accusez son pare-brise~: le film gras à l’intérieur fait des halos "
              "autour des phares.",
     "relance": "Et si les halos restent~?"},
    {"type": "point", "photo": "S05-NE5", "titre": "3. Les halos qui restent.", "bande": "3.",
     "corps": "Pare-brise propre, lunettes propres, et toujours des halos~? C’est peut-être une cataracte qui commence. "
              "Envoyez-le chez l’ophtalmo.",
     "relance": "À retenir"},
    {"type": "chute", "photo": "S05-NE6",
     "titre": "Après le permis, personne ne fait attention à ces 5~dixièmes. À part vous.", "bande": "À part vous.",
     "enregistrer": "Enregistrez-le~: cet hiver, vous aurez les trois points sous la main."},
    {"type": "suivre", "photo": "S05-VG7"},
]

PAGES_SIGNATURE = PAGES[:6] + [{"type": "signature", "photo": "S05-NE7", "nom": "Arnaud", "metier": "Opticien depuis 16 ans",
                                "partage": PARTAGE + "."}]

LISTE_LI = (
    "Trois choses à leur dire~:\n"
    "→ La loi des 5/10. Pour le permis B, il faut au moins 5/10 avec les deux yeux, lunettes portées "
    "(arrêté du 28 mars 2022). En dessous, pas le droit de conduire. Mesurez, et dites-le-lui.\n"
    "→ Le pare-brise. Avant d’accuser ses lunettes, accusez son pare-brise~: le film gras à l’intérieur fait des halos "
    "autour des phares.\n"
    "→ Les halos qui restent. Pare-brise propre, lunettes propres, et toujours des halos~? C’est peut-être une cataracte "
    "qui commence. Envoyez-le chez l’ophtalmo.\n\n")

PUBLICATIONS = [
    {
        "id": "S05-A1", "format": "A", "pilier": "La table de vente (la vue au volant) — fiche de la vidéo du 28/10",
        "type": "liste (3 points), format photo plein cadre (test)", "slug": "plus-le-droit-de-conduire",
        "titre": "Plus le droit de conduire", "palette": "photo", "pages": PAGES, "fin": "suivre",
        "legendes": {
            "instagram": (
                "Enregistrez-le~: cet hiver, vous aurez les trois points sous la main.\n"
                "La nuit tombe plus tôt, et certains de vos clients n’ont plus le droit de conduire. La loi des 5/10, "
                "le pare-brise, les halos qui restent~: quoi leur dire.\n\n"
                + SUIVRE_IG + "\n\n"
                "#opticien #opticienne #magasindoptique #conduitedenuit #securiteroutiere"),
            "linkedin": (
                "Enregistrez-le~: cet hiver, vous aurez les trois points sous la main.\n\n"
                "La nuit tombe une heure plus tôt. Vos clients rentrent en voiture dans le noir, et certains n’ont plus "
                "le droit de conduire.\n\n"
                + LISTE_LI
                + "Après le permis, personne ne fait attention à ces 5 dixièmes. À part vous.\n\n"
                + SUIVRE_LI),
        },
        "musique": "nappe calme du soir, sans paroles, volume bas",
    },
    {
        "id": "S05-A1s", "format": "A", "pilier": "Version signature du profil LinkedIn de Togi (marque 7211637)",
        "type": "signature", "slug": "plus-le-droit-de-conduire-signature", "titre": "Plus le droit de conduire",
        "palette": "photo", "pages": PAGES_SIGNATURE, "fin": "signature",
        "legendes": {
            "linkedin": (
                "Ma vidéo de la semaine dernière, en fiche à garder pour l’hiver.\n\n"
                "La nuit tombe une heure plus tôt. Vos clients rentrent en voiture dans le noir, et certains n’ont plus "
                "le droit de conduire.\n\n"
                + LISTE_LI
                + "Après le permis, personne ne fait attention à ces 5 dixièmes. À part nous.\n\n"
                "À partager avec votre équipe."),
        },
    },
    {
        "id": "S05-B1", "format": "B", "pilier": "La table de vente (phrase)", "slug": "et-la-nuit-au-volant",
        "titre": "La phrase qui porte — et la nuit, au volant ?", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U48", "phrase": "Cet hiver, une question de plus à la table de vente~:",
             "chute": "«~Et la nuit, au volant~?~»"},
        ],
        "legendes": {
            "instagram": (
                "Cet hiver, une question de plus à la table de vente~: «~Et la nuit, au volant~?~»\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Cet hiver, les clients rentrent en voiture dans le noir. Une question de plus à la table de vente~: "
                "«~Et la nuit, au volant~?~» Sa réponse dit s’il faut mesurer la vue.\n\n"
                "À partager avec votre équipe."),
        },
        "musique": "au choix de Togi",
    },
]


def legende_facebook(pub):
    """Charte §3 : la légende Instagram sans mots-clés ; « suivez @sehoria.fr » devient « suivez la page Sehoria »."""
    t = pub["legendes"]["instagram"]
    t = "\n".join(l for l in t.split("\n") if not l.startswith("#")).rstrip()
    return t.replace(SUIVRE_IG, SUIVRE_FB)


for _p in PUBLICATIONS:
    if "instagram" in _p["legendes"]:
        _p["legendes"]["facebook"] = legende_facebook(_p)

SLUGS = {p["id"]: p["slug"] for p in PUBLICATIONS}
