# -*- coding: utf-8 -*-
"""Hors-série S03h — lundi 19/10. Rebond sur le buzz d'une voiture de sport promise il y a près de neuf ans et montrée
le 15/10. Texte validé par Togi le 17/10 à 14 h 14 (« Ok je valide »). Seule source du texte des pages.

La marque, son patron et ses images ne paraissent nulle part (charte §5 et §6) : la page 1 évoque le buzz par le texte
et une voiture anonyme sous sa housse. `controle.py` bloque désormais ces noms.
Balisage : [[mot]] souligné à la main · {{mot}} surligné · ~ espace insécable.
"""

SEMAINE = "03h"

# Photos (téléchargées par GitHub — photos.py 03)
PHOTOS = {
    "U24": {"sujet": "Voiture entière sous une housse, trois quarts arrière (page 1) ; aucune marque ni plaque visible",
            "id": "ezBhFaOL6BY", "auteur": "JP Peluffo",
            "url": "https://unsplash.com/photos/a-car-covered-in-a-white-tarp-parked-on-the-side-of-the-road-ezBhFaOL6BY",
            "ecartee": "-ZIfQqO1K1o (Matthew Woinarowicz) : téléchargée, l'avant seul de la voiture, coupé par le cadre"},
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
            {"type": "accroche", "photo": "U24", "geant": "9 ans",
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
