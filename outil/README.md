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
Le logo est dans `assets/logo-sehoria.png`. Les photos de la semaine vont dans `assets/photos/U*.jpg`, puis `python3 src/preparer_photos.py` (filtre §5 + détourage) et `src/decoupes.py`.

## Photos : téléchargement par GitHub (depuis le 11/10)
L'espace de travail ne joint pas Unsplash ; GitHub, si. Une fois les photos validées par Togi :
```
python3 src/photos.py 02 "U12-penseur=<urls.raw du connecteur Unsplash>" "U13-gravure=<lien upload.wikimedia.org>"
```
Le script pousse la liste sur la branche `photos`, attend le robot GitHub (moins d'une minute en général) et copie
les photos réussies dans `assets/photos/`. Un échec s'affiche avec sa raison. Pour Unsplash, toujours le lien
`images.unsplash.com/photo-…` (champ `urls.raw`) : un identifiant seul échoue (401). Chercher avec `plus: none`
(jamais de photo Unsplash+). Détail : README de la branche `photos`.

## Fabriquer une semaine
1. Copier `src/semaine02.py` → `src/semaineNN.py` (textes, photos, légendes Instagram / Facebook / LinkedIn, SLUGS : seule source du texte) et `src/mep_s02.py` → `src/mep_sNN.py` (une fonction par page).
2. Photos : un script `src/preparer_sNN.py` par semaine (retouches §5, redressement, détourage ; modèle : `preparer_s02.py`).
3. `python3 src/semaine.py NN [S0N-A1 …]` → `livraison/SNN/` : PNG par page, PDF exact 810 × 1012,5 pt, légendes contrôlées.
   Dessins disponibles (`gabarit/dessins.js`) : en plus de ceux de S01, `lunettes`, `soleil`, `nuage` (option `pluie`), `visage` (dessiné, option `flou`), `telephone`, `bulleVide`.
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
