# Branche `photos` — téléchargement automatique

L'espace de travail de Claude ne peut pas joindre Unsplash, Pexels ni Wikimedia. Les serveurs de GitHub, si.
Cette branche sert de relais : Claude y dépose la liste des photos retenues, GitHub les télécharge, Claude les récupère.

1. `demandes/SNN.txt` : une photo par ligne, `nom source` (voir `.github/telecharger.py`).
   La source est un identifiant Unsplash (11 caractères), un lien `unsplash.com/photos/…`, un lien Pexels ou un lien `upload.wikimedia.org`.
2. Le dépôt de la liste lance le robot (`.github/workflows/telecharger-photos.yml`) : chaque photo arrive en `SNN/<nom>.jpg`
   (2400 px de large au plus), et `SNN/_rapport.md` dit ce qui a marché ou échoué.
3. Côté Claude : `python3 src/photos.py NN nom=source …` dans `outil/` fait les trois étapes d'un coup (branche `main`).

Ce sont les photos brutes, telles que publiées sur les banques d'images libres : les retouches du §5 de la charte
(marques effacées, etc.) se font ensuite dans `outil/`. Rien ici ne part chez Metricool.
