# -*- coding: utf-8 -*-
"""Semaine 06 — carrousel du samedi 14/11 (12 h 30) et phrase du samedi 14/11 (8 h 30). Seule source du texte des pages.

09/11 : Togi refuse le sujet proposé d'abord (Delfin, « un sujet de journaliste d'optique ») : « l'objectif
principal de Sehoria, c'est de donner de la valeur, un maximum de valeur aux opticiens ». Sujet choisi par Claude
le 10/11 (Togi : « choisis ») : « Je vais réfléchir. », pilier « Vendre à la table de vente », type avant / après.
Vérifié : aucune vidéo de Togi sur ce sujet depuis le 12/10 (brief du matin le 16/10, d'où l'écart du sujet 2).
Texte et photos envoyés le 10/11 à 8 h ; sans réponse, rien n'est parti le jeudi 12/11. Le 13/11 à 15 h 50, Togi
accepte la règle des 24 h (sans réponse 24 h après l'envoi du texte, Claude publie tel quel) et le samedi 14/11.
Seul changement : « samedi, chacun aura les mots » devient « au prochain « je vais réfléchir », chacun aura les
mots » (le carrousel sort un samedi).
Page 1 : La Jeune Fille à la perle (Vermeer, domaine public) : elle se retourne, comme un client à la porte.

S06-A1s : version « signature » du profil LinkedIn de Togi (charte §3) : pages 1 à 6 sans logo, page 7 à son nom,
sans visage connu derrière (l'écriture à la plume).

Balisage : [[mot]] souligné · ~ espace insécable.  Opticiens vouvoyés ; phrase B sans « tu » ni « vous »."""

SEMAINE = "06"

PHOTOS = {
    "U52": {"sujet": "Johannes Vermeer, La Jeune Fille à la perle, vers 1665 (Mauritshuis), domaine public "
                     "(A1-01, A1-03, A1-06, A1-07)",
            "id": "Commons : 1665_Girl_with_a_Pearl_Earring.jpg", "auteur": "Johannes Vermeer"},
    "U53": {"sujet": "Boîte en bois pleine de papiers et de notes (A1-02)", "id": "8bdwkFmieIs",
            "auteur": "Nguyen Phuc Hau", "url": "https://unsplash.com/photos/8bdwkFmieIs"},
    "U55": {"sujet": "Femme à lunettes qui prend une photo avec son téléphone (A1-04)", "id": "44hLIm8apFw",
            "auteur": "Helena Lopes", "url": "https://unsplash.com/photos/44hLIm8apFw"},
    "U56": {"sujet": "Stylo plume qui écrit sur une feuille lignée, marque de la plume effacée (A1-05, A1s-07)",
            "id": "y02jEX_B0O0", "auteur": "Aaron Burden", "url": "https://unsplash.com/photos/y02jEX_B0O0"},
    "U57": {"sujet": "Stylo plume doré, détouré (B1)", "id": "8XddFc6NkBY", "auteur": "Art Lasovsky",
            "url": "https://unsplash.com/photos/8XddFc6NkBY"},
    "U54": {"sujet": "Téléchargée, non utilisée : deux personnes à une table, minuscules, en bas de l'image",
            "id": "PNWp1dZ7sO0", "auteur": "Christin Hume"},
}

CREDIT_P1 = "Vermeer · La Jeune Fille à la perle"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

SUIVRE_TITRE = "Un conseil pour votre magasin, chaque semaine."
SUIVRE_BANDE = "chaque semaine."
SUIVRE_ACTION = "Suivez Sehoria"
SUIVRE_RAISON = "Pour ne pas rater le prochain."
SUIVRE_IG = "Un conseil pour votre magasin, chaque semaine~: suivez @sehoria.fr."
SUIVRE_FB = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."
SUIVRE_LI = "Un conseil pour votre magasin, chaque semaine~: suivez la page Sehoria."

ENVOYER = "Envoyez-le à votre équipe~: au prochain «~je vais réfléchir~», chacun aura les mots."

PAGES = [
    {"type": "accroche", "photo": "S06-JF1", "coin": "À partager", "credit": CREDIT_P1,
     "titre": "«~Je vais réfléchir.~» Le client s’en va. Et souvent, il ne revient pas.",
     "bande": "il ne revient pas.", "glisser": "Faites glisser"},
    {"type": "point", "photo": "S06-P2", "titre": "Avant~: «~D’accord, je vous garde le devis.~»", "bande": "Avant~:",
     "corps": "Il a dit~: «~Je vais réfléchir.~» Et le devis finit dans un tiroir.",
     "relance": "Et à la place~?"},
    {"type": "point", "photo": "S06-JF3", "titre": "Après~1~: «~Bien sûr. Qu’est‑ce qui vous fait hésiter~?~»",
     "bande": "Après~1~:",
     "corps": "Écoutez sa réponse jusqu’au bout. Le prix~? La monture~? L’avis de quelqu’un~?",
     "relance": "Il attend un avis~?"},
    {"type": "point", "photo": "S06-P4", "titre": "Après~2~: la photo.", "bande": "Après~2~:",
     "corps": "Il attend l’avis de quelqu’un~? Prenez la photo avec son téléphone, monture sur le nez. "
              "Il l’envoie avant de partir.",
     "relance": "Il part quand même~?"},
    {"type": "point", "photo": "S06-P5", "titre": "Après~3~: votre prénom.", "bande": "Après~3~:",
     "corps": "Il part quand même~? Écrivez votre prénom sur le devis. Et mettez la monture de côté~: "
              "«~Je vous la garde jusqu’à samedi.~»",
     "relance": "À retenir"},
    {"type": "chute", "photo": "S06-JF6",
     "titre": "Il ne revient pas pour un devis. Il revient pour quelqu’un.", "bande": "Il revient pour quelqu’un.",
     "enregistrer": ENVOYER},
    {"type": "suivre", "photo": "S06-JF7"},
]

PAGES_SIGNATURE = PAGES[:6] + [{"type": "signature", "photo": "S06-SIG7", "nom": "Arnaud",
                                "metier": "Opticien depuis 16 ans", "partage": PARTAGE + "."}]

LISTE_LI = (
    "Trois réponses à la place~:\n"
    "→ «~Bien sûr. Qu’est-ce qui vous fait hésiter~?~» Puis écoutez sa réponse jusqu’au bout~: le prix, la monture, "
    "l’avis de quelqu’un~?\n"
    "→ Il attend l’avis de quelqu’un~? Prenez la photo avec son téléphone, monture sur le nez. Il l’envoie avant de "
    "partir.\n"
    "→ Il part quand même~? Écrivez votre prénom sur le devis, et mettez la monture de côté~: «~Je vous la garde "
    "jusqu’à samedi.~»\n\n")

HABITUDE = ("«~Je vais réfléchir.~» La réponse habituelle~: «~D’accord, je vous garde le devis.~» Et le devis finit "
            "dans un tiroir.\n\n")
CHUTE = "Il ne revient pas pour un devis. Il revient pour quelqu’un.\n\n"

PUBLICATIONS = [
    {
        "id": "S06-A1", "format": "A", "pilier": "Vendre à la table de vente (« Je vais réfléchir »)",
        "type": "avant / après, format photo plein cadre", "slug": "je-vais-reflechir",
        "titre": "« Je vais réfléchir. »", "palette": "photo", "pages": PAGES, "fin": "suivre",
        "legendes": {
            "instagram": (
                ENVOYER + "\n"
                "«~Je vais réfléchir.~» Au lieu de «~je vous garde le devis~»~: demandez ce qui le fait hésiter, "
                "faites la photo avec son téléphone, écrivez votre prénom sur le devis.\n\n"
                + SUIVRE_IG + "\n\n"
                "#opticien #opticienne #magasindoptique #tabledevente #conseilvente"),
            "linkedin": ENVOYER + "\n\n" + HABITUDE + LISTE_LI + CHUTE + SUIVRE_LI,
        },
        "musique": "intégrée au Reel (musique originale, sans paroles)",
    },
    {
        "id": "S06-A1s", "format": "A", "pilier": "Version signature du profil LinkedIn de Togi (marque 7211637)",
        "type": "signature", "slug": "je-vais-reflechir-signature", "titre": "« Je vais réfléchir. »",
        "palette": "photo", "pages": PAGES_SIGNATURE, "fin": "signature",
        "legendes": {
            "linkedin": ("La phrase qu’on entend tous les samedis à la table de vente.\n\n" + HABITUDE + LISTE_LI
                         + CHUTE + "À partager avec votre équipe."),
        },
    },
    {
        "id": "S06-B1", "format": "B", "pilier": "Vendre à la table de vente (phrase)", "slug": "un-prenom",
        "titre": "La phrase qui porte — un prénom", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U57", "phrase": "Le client repart avec un devis.",
             "chute": "Qu’il reparte aussi avec un prénom."},
        ],
        "legendes": {
            "instagram": (
                "Le client repart avec un devis. Qu’il reparte aussi avec un prénom.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Samedi, un client hésite et repart avec son devis. Le prénom du vendeur écrit dessus, c’est celui "
                "qu’il aura en tête en revenant.\n\n"
                "À partager avec votre équipe."),
        },
        "musique": "aucune (image fixe)",
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
