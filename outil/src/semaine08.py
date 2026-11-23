# -*- coding: utf-8 -*-
"""Semaine 08 — carrousel du jeudi 26/11 (12 h 30 ; page LinkedIn 8 h 30) et phrase du samedi 28/11 (8 h 30).
Seule source du texte des pages.

Première semaine lancée seule par la tâche hebdomadaire (dimanche 22/11, 19 h 49). Sujet choisi par Claude : le client
qui entre « juste » pour un réglage. Type pas à pas, pilier « Vendre à la table de vente ». Jamais traité, ni en
carrousel ni dans les vidéos de Togi (l'accueil des trente premières secondes, 21/10, et la livraison, 23/10, sont
des vidéos). Texte, légendes et photos envoyés à Togi le 22/11 à 20 h 06 ; sans réponse 24 h après, publiés tel quel
(règle des 24 h).
Page 1 : Louis XIV de Rigaud (domaine public), le regard de haut du client qui demande « juste » un service.
Page 5 : l'Autoportrait aux bésicles de Chardin (domaine public), pour « vos verres, vous les avez depuis quand ? ».
Phrase B : la monture brune de U76 (rechange annoncée le 22/11) : la monture noire de U73 est tenue entre des doigts.

Balisage : [[mot]] souligné · ~ espace insécable. Traits d'union ordinaires : le trait d'union insécable (U+2011)
n'existe pas dans Poppins, Chromium le prenait dans une police hors charte (Liberation Sans) ; aucune coupure à vérifier.
Opticiens vouvoyés ; phrase B sans « tu » ni « vous »."""

SEMAINE = "08"

PHOTOS = {
    "U68g": {"sujet": "Hyacinthe Rigaud, Louis XIV, 1701 (Louvre), domaine public (A1-01, A1-06, A1-07)",
             "id": "Commons : Portrait_of_Louis_XIV_of_France_in_Coronation_Robes_(by_Hyacinthe_Rigaud)_-_Louvre_Museum.jpg",
             "auteur": "Hyacinthe Rigaud"},
    "U69b": {"sujet": "Jean Siméon Chardin, Autoportrait aux bésicles, 1771 (Louvre), domaine public (A1-05) ; "
                      "signature et date hors cadre",
             "id": "Commons : Chardin_pastel_selfportrait.jpg", "auteur": "Jean Siméon Chardin"},
    "U70": {"sujet": "Lunettes tenues à deux mains, visage flou derrière (A1-02)", "id": "VJHb4QPBgV4",
            "auteur": "Nathan Dumlao", "url": "https://unsplash.com/photos/VJHb4QPBgV4"},
    "U71": {"sujet": "Petite table et deux chaises (A1-03, A1s-07)", "id": "OYeJkHjM6ds", "auteur": "Noha Badawi",
            "url": "https://unsplash.com/photos/OYeJkHjM6ds"},
    "U72": {"sujet": "Lunettes couvertes de gouttes d'eau (A1-04)", "id": "jgPcjw2tBVc", "auteur": "Karl Hedin",
            "url": "https://unsplash.com/photos/jgPcjw2tBVc"},
    "U76": {"sujet": "Monture brune sur table blanche, détourée (B1)", "id": "Gr5L64WSYZI",
            "auteur": "Josue Acevedo Maldonado", "url": "https://unsplash.com/photos/Gr5L64WSYZI"},
}

CREDIT_P1 = "Rigaud · Louis XIV"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

SUIVRE_TITRE = "Un conseil pour votre magasin, chaque semaine."
SUIVRE_BANDE = "chaque semaine."
SUIVRE_ACTION = "Suivez Sehoria"
SUIVRE_RAISON = "Pour ne pas rater le prochain."
SUIVRE_IG = "Un conseil pour votre magasin, chaque semaine~: suivez @sehoria.fr."
SUIVRE_FB = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."
SUIVRE_LI = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."

ENVOYER = "Envoyez-le à votre équipe~: au prochain «~juste resserrer~», chacun connaîtra les trois étapes."

PAGES = [
    {"type": "accroche", "photo": "S08-L1", "coin": "À partager", "credit": CREDIT_P1,
     "titre": "«~Vous pouvez juste resserrer mes lunettes~?~» Deux minutes, c’est réglé. Il repart. "
              "Et ses prochaines lunettes, il les achètera ailleurs.",
     "bande": "il les achètera ailleurs.", "glisser": "Faites glisser"},
    {"type": "point", "photo": "S08-P2", "titre": "Il aurait pu aller n’importe où. Il est entré chez vous.",
     "bande": "Il est entré chez vous.",
     "corps": "Le réglage prend deux minutes. Ce qui compte, c’est ce que vous en faites.",
     "relance": "Première étape~?"},
    {"type": "point", "photo": "S08-P3", "titre": "Étape~1~: faites-le asseoir.", "bande": "Étape~1~:",
     "corps": "Pas debout près de la porte~: à la table de vente. «~Asseyez-vous, je m’en occupe.~»",
     "relance": "Et avant de les rendre~?"},
    {"type": "point", "photo": "S08-P4", "titre": "Étape~2~: rendez-les propres.", "bande": "Étape~2~:",
     "corps": "Un coup de chamoisine sur les verres avant de les lui rendre. Il voit la différence tout de suite.",
     "relance": "Et avant qu’il parte~?"},
    {"type": "point", "photo": "S08-C5", "titre": "Étape~3~: une question.", "bande": "Étape~3~:",
     "corps": "«~Vos verres, vous les avez depuis quand~?~» S’il ne s’en souvient pas, proposez-lui de vérifier sa vue.",
     "relance": "À retenir"},
    {"type": "chute", "photo": "S08-L6",
     "titre": "Il est venu pour une vis. Faites qu’il revienne pour une paire.",
     "bande": "Faites qu’il revienne pour une paire.", "enregistrer": ENVOYER},
    {"type": "suivre", "photo": "S08-L7"},
]

PAGES_SIGNATURE = PAGES[:6] + [{"type": "signature", "photo": "S08-SIG7", "nom": "Arnaud",
                                "metier": "Opticien depuis 16 ans", "partage": PARTAGE + "."}]

HABITUDE = ("«~Vous pouvez juste resserrer mes lunettes~?~» On le fait en deux minutes, il dit merci, il repart. "
            "Et ses prochaines lunettes, il les achètera ailleurs.\n\n")
LISTE_LI = (
    "Trois étapes pour que ces deux minutes comptent~:\n"
    "→ Faites-le asseoir à la table de vente, pas debout près de la porte~: «~Asseyez-vous, je m’en occupe.~»\n"
    "→ Rendez-les propres~: un coup de chamoisine sur les verres avant de les lui rendre. Il voit la différence "
    "tout de suite.\n"
    "→ Posez une question~: «~Vos verres, vous les avez depuis quand~?~» S’il ne s’en souvient pas, proposez-lui "
    "de vérifier sa vue.\n\n")
CHUTE = "Il est venu pour une vis. Faites qu’il revienne pour une paire.\n\n"

PUBLICATIONS = [
    {
        "id": "S08-A1", "format": "A", "pilier": "Vendre à la table de vente (le client qui vient pour un réglage)",
        "type": "pas à pas, format photo plein cadre", "slug": "juste-resserrer",
        "titre": "Juste resserrer mes lunettes", "palette": "photo", "pages": PAGES, "fin": "suivre",
        "legendes": {
            "instagram": (
                ENVOYER.replace("‑", "-") + "\n"
                "«~Vous pouvez juste resserrer mes lunettes~?~» Faites-le asseoir à la table de vente, rendez ses "
                "verres propres, et demandez-lui depuis quand il les a.\n\n"
                + SUIVRE_IG + "\n\n"
                "#opticien #opticienne #magasindoptique #tabledevente #conseilclient"),
            "linkedin": ENVOYER.replace("‑", "-") + "\n\n" + HABITUDE + LISTE_LI + CHUTE + SUIVRE_LI,
        },
        "musique": "intégrée au Reel (musique originale, sans paroles)",
    },
    {
        "id": "S08-A1s", "format": "A", "pilier": "Version signature du profil LinkedIn de Togi (marque 7211637)",
        "type": "signature", "slug": "juste-resserrer-signature", "titre": "Juste resserrer mes lunettes",
        "palette": "photo", "pages": PAGES_SIGNATURE, "fin": "signature",
        "legendes": {
            "linkedin": ("La demande qu’on entend plusieurs fois par jour à la table de vente.\n\n" + HABITUDE
                         + LISTE_LI + CHUTE + "À partager avec votre équipe."),
        },
    },
    {
        "id": "S08-B1", "format": "B", "pilier": "Vendre à la table de vente (phrase)", "slug": "sur-le-nez",
        "titre": "La phrase qui porte — sur le nez", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U76", "phrase": "Une monture au mur, on la regarde.",
             "chute": "Sur le nez, on la choisit."},
        ],
        "legendes": {
            "instagram": (
                "Une monture au mur, on la regarde. Sur le nez, on la choisit.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Samedi, devant le mur de montures~: un client peut regarder dix minutes sans rien choisir. Le choix "
                "commence quand une monture est sur son nez, devant le miroir.\n\n"
                "À partager avec votre équipe."),
        },
        "musique": "Reel Facebook de 8 s (musique originale) ; image seule sur Instagram et LinkedIn",
    },
]


def legende_facebook(pub):
    """Charte §3 : la légende Instagram sans mots-clés ; « suivez @sehoria.fr » devient « suivez la page Sehoria ».
    Depuis le 22/11 : aucun lien dans la légende d'un Reel Facebook (le Reel S07 avec lien : 1 vue)."""
    t = pub["legendes"]["instagram"]
    t = "\n".join(l for l in t.split("\n") if not l.startswith("#")).rstrip()
    t = t.replace(SUIVRE_IG, SUIVRE_FB)
    assert "http" not in t and "sehoria.fr" not in t.replace("@sehoria.fr", ""), pub["id"]
    return t


for _p in PUBLICATIONS:
    if "instagram" in _p["legendes"]:
        _p["legendes"]["facebook"] = legende_facebook(_p)

SLUGS = {p["id"]: p["slug"] for p in PUBLICATIONS}
