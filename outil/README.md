# Outil de production Sehoria — carrousels 1080 × 1350

Gabarit et scripts qui fabriquent les publications hebdomadaires du projet « Sehoria — Communication ».
Référence : `Charte_Communication_Sehoria.md` (dans le projet claude.ai). État et historique : `claude/journal-publications.md`.

## Démarrer une session (espace de travail vide)
```
cd /home/claude/sehoria-medias/outil
npm install                                   # polices (Fraunces, JetBrains Mono, Gochi Hand) + rough.js
pip install rembg brotli pypdf pypdfium2 --break-system-packages   # playwright, numpy, pillow, opencv : déjà présents en général
python3 src/textures.py                       # seulement si assets/*.png manquent (papiers générés, aucune image tierce)
```
Le logo est dans `assets/logo-sehoria.png`. Les photos de la semaine (Unsplash, téléchargées par Togi) vont dans `assets/photos/U*.jpg`, puis `python3 src/preparer_photos.py` (filtre §5 + détourage) et `src/decoupes.py`.

## Fabriquer une semaine
1. Copier `src/semaine01.py` → `src/semaineNN.py` (textes, photos, légendes : seule source du texte) et `src/mep_s01.py` → `src/mep_sNN.py` (une fonction par page).
2. Adapter les imports dans `src/semaine.py` (SEMAINE, PUBLICATIONS, PUBLICATIONS_MEP, SLUGS).
3. `python3 src/essai.py` (planche d'essai), puis `python3 src/semaine.py` → `livraison/SNN/` : PNG par page, PDF exact 810 × 1012,5 pt, légendes contrôlées.
4. Contrôles automatiques : ≤ 30 mots par page, rien sous 28 px, zone de sécurité, chevauchements, polices chargées, texte du PDF = texte de la page, interdits du §6 (`src/controle.py`).

## Programmer (Metricool)
- Convertir les pages en JPEG qualité 95 dans `../SNN/` (dossier racine du dépôt), pousser, puis donner à Metricool les liens
  `https://raw.githubusercontent.com/leperetogi/sehoria-medias/main/SNN/<fichier>.jpg` (Metricool recopie les images chez lui).
- Marque Metricool : 7194477, fuseau Europe/Paris.

## Fichiers
- `gabarit/gabarit.css` — papier, bandeaux, typo, rubans, feuilles, polaroïds.
- `gabarit/dessins.js` — dessins « à la main » (rough.js) : soulignés, flèches, bulles, bâtons, tableau, icônes, devis, coche, croix, montée.
- `src/composants.py` — blocs de page. `src/rendu.py` — rendu Chromium + contrôles. `src/controle.py` — interdits §6, mots, vouvoiement.
- `src/couverture_fb.py` — couverture Facebook 1640 × 624.
