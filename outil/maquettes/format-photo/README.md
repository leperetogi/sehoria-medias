# Format « photo plein cadre » — maquette du 25/10, test S05

Inspiré de la méthode des grands comptes de carrousels (vidéo envoyée par Togi le 25/10), sans copier leur mise en page :
photo sur toute la page, dégradé encre en bas, titre Poppins 800 en majuscules avec un mot en bandeau violet,
« Faites glisser » + flèche en page 1, numéro de page, logo crème. Page 1 : le visage de Togi, image tirée de sa vidéo
(charte v2.3). Test accepté par Togi le 27/10, sur une semaine (S05).

- `maquette.html` : pages 1 et 2 (textes provisoires tirés de la vidéo du 21/10). Rendu : Chromium (Playwright), 1080 × 1350.
- `p1.jpg`, `p2.jpg` : images de `video/2026-10-21-premieres-secondes.mp4` (18 s et 22 s), recadrées 1080 × 1350,
  logo de marque de la chaise flouté. Pour une autre vidéo : `ffmpeg -ss <s> -i video/<fichier>.mp4 -frames:v 1`,
  puis recadrer `(0, 500, 1080, 1850)` (au-dessus des sous-titres incrustés).
- Polices : `npm i @fontsource/poppins@5 --no-save` dans `outil/`.
