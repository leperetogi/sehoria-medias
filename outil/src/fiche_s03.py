# -*- coding: utf-8 -*-
"""S03 — fiche « Commentez SAMEDI » : A4 à imprimer (PDF) et image pour l'envoyer depuis un téléphone (JPEG).
Texte : semaine03.FICHE (validé par Togi le 12/10). Fond blanc : elle part à l'imprimante du magasin."""
import asyncio
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from playwright.async_api import async_playwright
from PIL import Image
from composants import md, url, RACINE, ASSETS, STICKERS
from controle import verifier, compter_mots, normaliser
from semaine03 import FICHE, SEMAINE

DEST = RACINE / "livraison" / f"S{SEMAINE}" / f"S{SEMAINE}-fiche_samedi"
G = RACINE / "gabarit"


def construire():
    logo = STICKERS / "logo-couleur.png"
    if not logo.exists():
        im = Image.open(ASSETS / "logo-sehoria.png").convert("RGBA")
        im.crop(im.getbbox()).save(logo)
    titre = md(FICHE["titre"].replace("samedi", "[[samedi|terracotta]]", 1))
    cases = "".join(f'<li><span class="case" data-i="{i}"></span><span class="ligne">{md(t)}</span></li>'
                    for i, t in enumerate(FICHE["cases"]))
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Vendredi soir</title>
<link rel="stylesheet" href="{url(G / 'gabarit.css')}">
<script src="{url(RACINE / 'node_modules/roughjs/bundled/rough.js')}"></script>
<style>
@page {{ size: A4; margin: 0 }}
html, body {{ margin: 0; background: #fff }}
.a4 {{ position: relative; width: 210mm; height: 297mm; box-sizing: border-box; padding: 22mm 20mm 18mm; background: #fff;
       font-family: "Fraunces", serif; color: #26203A; overflow: hidden }}
.haut {{ font-family: "JetBrains Mono", monospace; font-weight: 600; font-size: 10pt; letter-spacing: .14em; color: #C06B3E;
         text-transform: uppercase }}
h1 {{ font-weight: 800; font-variation-settings: "opsz" 144, "SOFT" 100, "WONK" 1; font-size: 34pt; line-height: 1.05;
      margin: 6mm 0 12mm; letter-spacing: -.01em; text-wrap: balance }}
ul {{ list-style: none; margin: 0; padding: 0 }}
li {{ display: flex; align-items: center; gap: 7mm; padding: 4.6mm 0; border-bottom: 1.2px dashed #CFC8DA; font-size: 15pt;
      font-weight: 500; font-variation-settings: "opsz" 48, "SOFT" 50; line-height: 1.25 }}
.case {{ flex: 0 0 11mm; height: 11mm; position: relative }}
.case svg {{ position: absolute; inset: -2mm; width: 15mm; height: 15mm; overflow: visible }}
.pied {{ position: absolute; left: 20mm; right: 20mm; bottom: 14mm; display: flex; align-items: center; justify-content: space-between;
         font-family: "JetBrains Mono", monospace; font-weight: 600; font-size: 8.5pt; letter-spacing: .1em; color: #6E6782;
         text-transform: uppercase }}
.pied img {{ height: 9mm }}
.souligne {{ position: relative; white-space: nowrap }}
</style></head><body>
<section class="a4">
  <h1>{titre}</h1>
  <ul>{cases}</ul>
  <div class="pied"><img src="{url(logo)}" alt="Sehoria"><span>{html.escape(FICHE['pied'])}</span></div>
</section>
<script>
document.fonts.ready.then(() => {{
  document.querySelectorAll('.case').forEach((c, i) => {{
    const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); c.appendChild(s);
    const rc = rough.svg(s), mm = s.getBoundingClientRect().width / 15;
    s.appendChild(rc.rectangle(2 * mm, 2 * mm, 11 * mm, 11 * mm, {{ stroke: '#C06B3E', strokeWidth: 2.2, roughness: 1.3, bowing: 1.2, seed: 300 + i }}));
  }});
  document.querySelectorAll('.souligne').forEach((u, i) => {{
    const r = u.getBoundingClientRect(), a = u.closest('.a4').getBoundingClientRect();
    const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('style', `position:absolute;left:${{r.left - a.left - 4}}px;top:${{r.bottom - a.top - 10}}px;width:${{r.width + 8}}px;height:24px;overflow:visible`);
    u.closest('.a4').appendChild(s);
    s.appendChild(rough.svg(s).curve([[0, 10], [r.width * .5, 15], [r.width + 8, 8]], {{ stroke: '#C06B3E', strokeWidth: 4, roughness: 1, seed: 7 }}));
  }});
  document.body.dataset.pret = '1';
}});
</script></body></html>"""


async def rendre():
    DEST.mkdir(parents=True, exist_ok=True)
    h = DEST / "fiche.html"
    h.write_text(construire(), encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=1240 / 794)
        await pg.goto("file://" + str(h))
        await pg.wait_for_function("document.body.dataset.pret === '1'")
        await pg.wait_for_timeout(200)
        texte = await pg.evaluate("document.querySelector('.a4').innerText")
        await pg.screenshot(path=str(DEST / "fiche.png"), clip={"x": 0, "y": 0, "width": 794, "height": 1123})
        await pg.pdf(path=str(DEST / f"S{SEMAINE}-fiche_samedi.pdf"), format="A4", print_background=True)
        await b.close()
    Image.open(DEST / "fiche.png").convert("RGB").save(DEST / f"S{SEMAINE}-fiche_samedi.jpg", quality=92)
    (DEST / "fiche.png").unlink()
    h.unlink()
    constats, nombres, noms = verifier(texte, "A")
    print(f"{compter_mots(texte)} mots · constats : {constats or 'aucun'} · noms : {noms}")
    print(DEST)


if __name__ == "__main__":
    asyncio.run(rendre())
