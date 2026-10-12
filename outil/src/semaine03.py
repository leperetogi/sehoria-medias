# -*- coding: utf-8 -*-
"""Semaine 03 — publications du 20 au 24/10. Textes, photos et fiche « Commentez SAMEDI » validés par Togi le 12/10 (corrections du soir : antireflet, chamoisine, message privé).
Seule source du texte des pages.

Balisage : [[mot]] souligné à la main · {{mot}} surligné · ~ espace insécable.
Règles d'or (charte §0) : la valeur dans chaque publication ; un enfant de 10 ans comprend tout.
« Table de vente », jamais « comptoir ». Opticiens vouvoyés ; phrase B sans « tu » ni « vous ».
"""

SEMAINE = "03"

# Photos validées par Togi le 12/10 (téléchargées par GitHub — photos.py)
PHOTOS = {
    "U12": {"sujet": "Buste d'homme drapé, style portrait romain, de face, fond noir (lunettes dessinées dessus)",
            "id": "cnpwUiZ44Wk", "auteur": "Sam",
            "url": "https://unsplash.com/photos/a-bust-of-a-man-with-a-cape-around-his-neck-cnpwUiZ44Wk",
            "raw": "https://images.unsplash.com/photo-1739323146734-3bf80c8d7ed1?ixid=M3wxMDE3MjIwfDB8MXxzZWFyY2h8NHx8cm9tYW4lMjBidXN0JTIwbXVzZXVtJTIwYmxhY2slMjBiYWNrZ3JvdW5kfGVufDB8fHx8MTc5MTc1NjcwNnwy&ixlib=rb-4.1.0"},
    "U13": {"sujet": "Pendule ancienne en bronze, fond sombre (inscription éventuelle du cadran effacée)",
            "id": "3jM3BCQAtVA", "auteur": "LVL9 Studio",
            "url": "https://unsplash.com/photos/black-wooden-analog-clock-at-10-00-3jM3BCQAtVA",
            "raw": "https://images.unsplash.com/photo-1627307284579-327ea0c7de14?ixid=M3wxMDE3MjIwfDB8MXxzZWFyY2h8Nnx8YW50aXF1ZSUyMGNsb2NrJTIwZmFjZXxlbnwwfHx8fDE3OTE3NTY2Nzd8Mg&ixlib=rb-4.1.0"},
    "U14": {"sujet": "Fauteuil bistrot en bois courbé, vide (pommes de pin du siège effacées)",
            "id": "Rp9WWWkj5aQ", "auteur": "valentin ciccarone",
            "url": "https://unsplash.com/photos/a-light-grey-chair-with-three-pinecones-on-the-seat-Rp9WWWkj5aQ",
            "raw": "https://images.unsplash.com/photo-1776461845017-ef3019ad9047?ixid=M3wxMDE3MjIwfDB8MXxzZWFyY2h8Nnx8YmVudHdvb2QlMjBjaGFpcnxlbnwwfHx8fDE3OTE3NTY3MDV8Mg&ixlib=rb-4.1.0"},
    # Ajoutées le 12/10 au soir (« plus de photos dans les carrousels », liste validée par Togi)
    "U15": {"sujet": "Étiquette kraft vierge et sa ficelle (A1-02 : « un prix en plus »)",
            "id": "KaeaUITiWnc", "auteur": "Angèle Kamp",
            "url": "https://unsplash.com/photos/four-paper-card-tags-KaeaUITiWnc"},
    "U16": {"sujet": "Route mouillée la nuit, reflets des lampadaires (A1-04 : conduire la nuit)",
            "id": "EDGwCAOM_HA", "auteur": "Pavel Orange",
            "url": "https://unsplash.com/photos/wet-asphalt-road-at-night-EDGwCAOM_HA"},
    "U17": {"sujet": "Soleil et halo dans un ciel clair, en rond (A1-05 : souvent dehors)",
            "id": "zjoydJb17mE", "auteur": "Grooveland Designs",
            "url": "https://unsplash.com/photos/blue-sky-with-white-sun-zjoydJb17mE"},
    "U18": {"sujet": "Lunettes de soleil enveloppantes sans marque (A1-06 : la deuxième paire) ; marquage de branche effacé",
            "id": "Ag2o4j9jh4s", "auteur": "Barry A",
            "url": "https://unsplash.com/photos/a-pair-of-sunglasses-sitting-on-top-of-a-white-table-Ag2o4j9jh4s",
            "ecartee": "YSyUbJm5BR8 (Michael C) : forme d'un modèle de marque connu, logo sur la branche"},
    "U19": {"sujet": "Téléphone à cadran noir (A2-02 : le téléphone sonne) ; étiquette du cadran vidée",
            "id": "8gWEAAXJjtI", "auteur": "Quino Al",
            "url": "https://unsplash.com/photos/black-rotary-dial-phone-on-white-surface-8gWEAAXJjtI"},
    "U20": {"sujet": "Lunettes rangées dans leur étui ouvert (A2-03 : les lunettes prêtes)",
            "id": "bdD0JVklJJ0", "auteur": "Danny Greenberg",
            "url": "https://unsplash.com/photos/eyeglasses-in-a-case-on-a-gray-surface-bdD0JVklJJ0"},
    "U21": {"sujet": "Feuille blanche punaisée sur un liège, une main la fixe (A2-04 : le planning affiché)",
            "id": "ZT9gjcJog6U", "auteur": "Volodymyr Hryshchenko",
            "url": "https://unsplash.com/photos/shallow-focus-photo-of-white-paper-sheet-mounted-on-cork-board-ZT9gjcJog6U"},
    "U22": {"sujet": "Étui en cuir et lunettes rondes (A2-05 : la table de vente prête) ; logo et marquages effacés",
            "id": "Q0nZtBqpQbA", "auteur": "Kofi Nartey",
            "url": "https://unsplash.com/photos/round-eyeglasses-next-to-a-brown-glasses-case-Q0nZtBqpQbA"},
    "U23": {"sujet": "Montures anciennes en présentoir (A2-06 : la vitrine) ; lettres d'un dos de livre effacées",
            "id": "JA21BnjBtvo", "auteur": "mdreza jalali",
            "url": "https://unsplash.com/photos/collection-of-vintage-eyeglasses-displayed-in-a-shop-JA21BnjBtvo"},
}

CTA_MARQUE_1 = "Lancez vos challenges."
CTA_MARQUE_2 = "L’app compte les ventes."
CTA_ACTION = "Demander un accès — sehoria.fr"
CTA_FREIN = "Premier mois offert, sans engagement, résiliable à tout moment"
CTA_SIGNATURE = "Construit par un opticien, pour les opticiens"
PARTAGE = "À partager avec votre équipe"

LIEN = "https://sehoria.fr"
FREIN_LEGENDE = "Premier mois offert, sans engagement, résiliable à tout moment."
MOT_FICHE = "SAMEDI"

PUBLICATIONS = [
    {
        "id": "S03-A1", "format": "A", "pilier": "La performance (les options qu’on oublie de proposer)",
        "slug": "option-question", "titre": "Une option se propose avec une question", "palette": "creme",
        "pages": [
            {"type": "accroche", "photo": "U12", "bulle": "Non merci.",
             "titre": "Le client ne demande jamais [[l’option]].",
             "bandeau": "Il attend qu’on lui pose la bonne question."},
            {"type": "probleme",
             "citation1": "«~Vous voulez l’antireflet~?~»", "citation2": "«~Non merci.~»",
             "texte": "Dite comme ça, l’option sonne comme un prix en plus.",
             "chute": "Le client dit non [[avant de comprendre.]]"},
            {"type": "valeur", "numero": "1",
             "titre": "Ne dites pas le nom de l’option.", "texte": "Posez une question sur sa vie.",
             "chute": "Sa réponse vous dit [[quoi proposer.]]"},
            {"type": "valeur", "numero": "2",
             "citation": "«~Vous conduisez la nuit~?~»",
             "texte": "S’il dit oui, parlez de l’antireflet~: moins d’éblouissement et plus de sérénité sur la route de nuit."},
            {"type": "valeur", "numero": "3",
             "citation": "«~Vous êtes souvent dehors~?~»",
             "texte": "Parlez du verre qui fonce au soleil, et redevient clair à l’intérieur."},
            {"type": "valeur", "numero": "4",
             "citation": "«~Et au soleil, vous mettez quoi~?~»",
             "texte": "Souvent, la réponse est~: rien.", "chute": "C’est le moment de la [[deuxième paire.]]"},
            {"type": "cta", "pont1": "L’option oubliée~? Faites-en un challenge.", "pont2": "L’app compte les ventes."},
        ],
        "legendes": {
            "instagram": (
                "«~Vous voulez l’antireflet~?~» Le client dit non avant de comprendre.\n"
                "Ne dites pas le nom de l’option~: posez une question sur sa vie. Sa réponse vous dit quoi proposer.\n\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente #conseilvente"),
            "linkedin": (
                "«~Vous voulez l’antireflet~?~» «~Non merci.~» Dite comme ça, l’option sonne comme un prix en plus. "
                "Le client dit non avant de comprendre.\n\n"
                "Ne dites pas le nom de l’option. Posez une question sur sa vie~:\n"
                "→ «~Vous conduisez la nuit~?~» S’il dit oui, parlez de l’antireflet.\n"
                "→ «~Vous êtes souvent dehors~?~» Parlez du verre qui fonce au soleil.\n"
                "→ «~Et au soleil, vous mettez quoi~?~» Souvent~: rien. C’est le moment de la deuxième paire.\n"
                "Sa réponse vous dit quoi proposer.\n\n"
                "L’option oubliée~? Faites-en un challenge. L’app compte les ventes.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
    {
        "id": "S03-A2", "format": "A", "pilier": "La vitrine et le magasin", "slug": "samedi-se-prepare",
        "titre": "Le samedi se prépare le vendredi", "palette": "terracotta",
        "pages": [
            {"type": "accroche", "photo": "U13",
             "titre": "Votre samedi commence [[vendredi soir]].", "main": "18~h, on prépare…"},
            {"type": "probleme",
             "texte": "Samedi, 10~h. Trois clients attendent, le téléphone sonne… et on cherche une paire de lunettes.",
             "chute": "Ce qu’on n’a pas préparé, on le cherche [[devant le client.]]"},
            {"type": "valeur", "numero": "1",
             "titre": "Les lunettes que les clients viennent chercher~:", "texte": "propres, vérifiées, rangées par nom."},
            {"type": "valeur", "numero": "2",
             "titre": "Le planning de samedi, affiché~:",
             "texte": "qui accueille, qui fait l’atelier, qui part en pause, et à quelle heure.",
             "chute": "Personne ne se demande [[quoi faire.]]"},
            {"type": "valeur", "numero": "3",
             "titre": "La table de vente, prête~:", "texte": "chamoisines, étuis, cordons à portée de main.",
             "chute": "Plus besoin de se lever au milieu d’une vente."},
            {"type": "valeur", "numero": "4",
             "titre": "La vitrine~: un coup de chamoisine, et une monture qu’on change.",
             "chute": "Samedi, tout le monde passe devant.",
             "bulle": "Commentez SAMEDI~: on vous envoie en message privé la check-list à imprimer"},
            {"type": "cta"},
        ],
        "legendes": {
            "instagram": (
                "Samedi, 10~h~: trois clients attendent, et on cherche une paire de lunettes.\n"
                "Le samedi se prépare le vendredi soir~: lunettes prêtes, planning affiché, table de vente rangée, "
                "vitrine qui change.\n\n"
                "Commentez SAMEDI~: on vous envoie en message privé la check-list à imprimer.\n"
                "Demander un accès~: lien en bio.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente #vitrine"),
            "linkedin": (
                "Samedi, 10~h. Trois clients attendent, le téléphone sonne, et on cherche une paire de lunettes. "
                "Ce qu’on n’a pas préparé, on le cherche devant le client.\n\n"
                "Le samedi se prépare le vendredi soir~:\n"
                "→ Les lunettes que les clients viennent chercher~: propres, vérifiées, rangées par nom.\n"
                "→ Le planning affiché~: qui accueille, qui fait l’atelier, qui part en pause, et à quelle heure.\n"
                "→ La table de vente prête~: chamoisines, étuis, cordons à portée de main.\n"
                "→ La vitrine~: un coup de chamoisine, et une monture qu’on change.\n\n"
                "Commentez SAMEDI~: on vous envoie en message privé la check-list à imprimer.\n\n"
                "Lancez vos challenges. L’app compte les ventes.\n"
                "Demander un accès~: https://sehoria.fr\n"
                "Premier mois offert, sans engagement, résiliable à tout moment."),
        },
    },
    {
        "id": "S03-B1", "format": "B", "pilier": "Motiver l’équipe", "slug": "un-bonjour",
        "titre": "La phrase qui porte — le client qui attend", "palette": "violet",
        "pages": [
            {"type": "phrase", "photo": "U14",
             "phrase": "Un client qui attend n’a pas besoin qu’on se dépêche.", "chute": "Il a besoin d’un bonjour."},
        ],
        "legendes": {
            "instagram": (
                "Un client qui attend n’a pas besoin qu’on se dépêche. Il a besoin d’un bonjour.\n"
                "À partager avec votre équipe.\n\n"
                "#opticien #opticienne #magasindoptique #equipedevente"),
            "linkedin": (
                "Samedi, le magasin est plein. Un client entre, tout le monde est occupé. "
                "Un regard, un bonjour, «~je suis à vous dans cinq minutes~»~: il sait qu’on l’a vu.\n\n"
                "À partager avec votre équipe."),
        },
    },
]

# Fiche « Commentez SAMEDI » (A4 à imprimer, envoyée en message privé par Togi)
FICHE = {
    "titre": "Vendredi soir~: votre samedi est prêt~?",
    "cases": [
        "Les lunettes que les clients viennent chercher~: propres, vérifiées, rangées par nom",
        "Les clients dont les lunettes sont prêtes ont été prévenus",
        "Le planning de samedi est affiché~: qui accueille, qui fait l’atelier, les pauses",
        "La table de vente est prête~: chamoisines, étuis, cordons",
        "La vitrine~: un coup de chamoisine, une monture changée",
        "Les rendez-vous de samedi sont relus ensemble",
        "La caisse est prête pour l’ouverture",
        "Un merci à l’équipe pour la semaine",
    ],
    "pied": "sehoria.fr · Construit par un opticien, pour les opticiens",
}


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
