# -*- coding: utf-8 -*-
"""Hors-série S03h — lundi 19/10. Rebond sur le buzz d'une voiture de sport promise il y a près de neuf ans et montrée
le 15/10. Texte validé par Togi le 17/10 à 14 h 14 (« Ok je valide »). Seule source du texte des pages.

La marque, son patron et ses images ne paraissent nulle part (charte §5 et §6) : la page 1 évoque le buzz par le texte
et une voiture anonyme sous sa housse. `controle.py` bloque désormais ces noms.
Balisage : [[mot]] souligné à la main · {{mot}} surligné · ~ espace insécable.
"""

SEMAINE = "03h"

# Exception au §6 décidée par Togi le 17/10 à 15 h 06 : le nom de la marque paraît une fois, dans le libellé
# d'actualité de la page 1, écrit en texte simple (ni logo, ni image, ni photo officielle : refusées).
EXCEPTIONS_MARQUES = {"tesla"}

# Photos (téléchargées par GitHub — photos.py 03)
PHOTOS = {
    # Refonte du 17/10 à 15 h (Togi : « pas assez pro », « trop de dessins ») : photos de mise en situation, validées
    "U27": {"sujet": "Voiture sous une housse, garée devant une maison (p. 1, pleine page) ; plaque effacée",
            "id": "QJWk6LLOMdQ", "auteur": "Zachary Keimig",
            "url": "https://unsplash.com/photos/blue-car-covered-with-blue-textile-QJWk6LLOMdQ"},
    "U28": {"sujet": "Un client de dos à la porte d'un magasin d'optique, le soir (p. 2) ; enseigne, marques et affiches hors cadre",
            "id": "rOC-_ssUw2o", "auteur": "Isaac Owens",
            "url": "https://unsplash.com/photos/person-in-doorway-of-optician-shop-rOC-_ssUw2o"},
    "U29": {"sujet": "Calendrier en gros plan, une date entourée (p. 3) ; mois, année et jours anglais hors cadre",
            "id": "P1kP-BfIelI", "auteur": "Glen Carrie",
            "url": "https://unsplash.com/photos/a-close-up-of-a-calendar-with-a-red-marker-P1kP-BfIelI"},
    "U30": {"sujet": "Mains qui écrivent un message sur un téléphone (p. 4)", "id": "BjhUu6BpUZA",
            "auteur": "Priscilla Du Preez", "url": "https://unsplash.com/photos/person-using-smartphone-BjhUu6BpUZA"},
    "U25": {"sujet": "Tasse de café et carnet (p. 5) ; recadrée sous le mot « NOTES »", "id": "ibYL9nBsNNw",
            "auteur": "Suzanne Skeen", "url": "https://unsplash.com/photos/ibYL9nBsNNw"},
    "U31": {"sujet": "Une main tend une paire de lunettes (p. 6)", "id": "fI0_v1y6rGE", "auteur": "GlassesShop",
            "url": "https://unsplash.com/photos/a-person-holding-a-pair-of-glasses-in-their-hand-fI0_v1y6rGE"},
    "U26": {"sujet": "Petit tournevis à manche transparent (p. 6)", "id": "lH-UZuoG-aY", "auteur": "Steve A Johnson",
            "url": "https://unsplash.com/photos/red-and-silver-screw-driver-lH-UZuoG-aY"},
    # Écartées après la première version : U24/U24b voitures bâchées en découpe (page jugée « pas assez pro »)
}

CTA_MARQUE_1 = "Lancez vos challenges."
CTA_MARQUE_2 = "L’app compte les ventes."
CTA_ACTION = "Demander un accès — sehoria.fr"
CTA_FREIN = "Premier mois offert, sans engagement, résiliable à tout moment"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"

LIEN = "https://sehoria.fr"
FREIN_LEGENDE = "Premier mois offert, sans engagement, résiliable à tout moment."

# Le commentaire de Togi quand il repartage depuis son profil (sans lien ni appel, charte §2)
REPARTAGE_ARNAUD = ("Neuf ans pour une voiture, on en sourit. Deux jours de retard sur des lunettes sans prévenir, "
                    "le client s’en souvient.")

PUBLICATIONS = [
    {
        "id": "S03-H1", "format": "A", "pilier": "Les astuces (le délai des lunettes)", "slug": "delai-tenu",
        "titre": "Un délai qu’on tient", "palette": "terracotta",
        "pages": [
            {"type": "accroche", "photo": "U27", "geant": "9 ans", "libelle": "Actu · Tesla · 15/10",
             "bandeau": "Une voiture promise il y a près de neuf ans. Enfin montrée. Fabriquée dans deux ans.",
             "main": "Votre client, lui, attend ses lunettes [[jeudi.]]"},
            {"type": "probleme",
             "citation1": "«~Elles sont prêtes, mes lunettes~?~»", "citation2": "«~Ah… pas encore.~»",
             "texte": "Le client a fait le trajet pour rien.",
             "chute": "Le retard, il le comprend. Venir pour rien, [[beaucoup moins.]]"},
            {"type": "valeur", "numero": "1",
             "titre": "Annoncez un délai que vous tiendrez.", "texte": "Le verre arrive en 5~jours~? Dites~7.",
             "chute": "Si elles sont prêtes plus tôt, c’est une [[bonne surprise.]]"},
            {"type": "valeur", "numero": "2",
             "titre": "Prévenez avant qu’il se déplace.",
             "texte": "Un retard, le client l’apprend par vous, au téléphone ou par message.",
             "chute": "Jamais en arrivant [[au magasin.]]"},
            {"type": "valeur", "numero": "3",
             "titre": "Regardez demain dès ce matin.",
             "texte": "Chaque matin, vérifiez les lunettes promises pour le lendemain.",
             "chute": "Pas arrivées~? Il vous reste [[un jour pour prévenir.]]"},
            {"type": "valeur", "numero": "4",
             "titre": "L’excuse vient avec une solution.",
             "liste": ["Ses anciennes lunettes bien réglées,", "une paire de prêt,", "un rendez-vous à l’heure qui l’arrange."]},
            {"type": "cta"},
        ],
        "legendes": {
            "instagram": (
                "Une voiture peut se faire attendre neuf ans. Une paire de lunettes, pas un jour de plus que prévu.\n"
                "Annoncez un délai que vous tiendrez, et prévenez avant que le client se déplace.\n\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique"),
            "linkedin": (
                "Une voiture peut se faire attendre neuf ans. Une paire de lunettes, pas un jour de plus que prévu.\n\n"
                "«~Elles sont prêtes, mes lunettes~?~» «~Ah… pas encore.~» Le retard, le client le comprend. "
                "Venir pour rien, beaucoup moins.\n\n"
                "→ Annoncez un délai que vous tiendrez. Le verre arrive en 5 jours~? Dites 7.\n"
                "→ Prévenez avant qu’il se déplace, au téléphone ou par message.\n"
                "→ Chaque matin, vérifiez les lunettes promises pour le lendemain.\n"
                "→ L’excuse vient avec une solution~: ses anciennes lunettes bien réglées, une paire de prêt, "
                "un rendez-vous à l’heure qui l’arrange.\n\n"
                "Lancez vos challenges. L’app compte les ventes.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
]


def legende_facebook(pub):
    """Charte §3 : la légende Instagram sans mots-clés ; « lien en bio » devient le lien suivi du frein."""
    t = pub["legendes"]["instagram"]
    t = "\n".join(l for l in t.split("\n") if not l.startswith("#")).rstrip()
    return t.replace("Demander un accès~: lien en bio.", f"Demander un accès~: {LIEN}\n{FREIN_LEGENDE}")


for _p in PUBLICATIONS:
    _p["legendes"]["facebook"] = legende_facebook(_p)

SLUGS = {p["id"]: p["slug"] for p in PUBLICATIONS}
