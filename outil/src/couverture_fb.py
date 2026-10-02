# -*- coding: utf-8 -*-
"""Photo de couverture Facebook 1640 × 624 (affichée 820 × 312 sur ordinateur, côtés rognés sur mobile)."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from composants import bandeau, mono, page, document, RACINE
from playwright.async_api import async_playwright

L, H = 1640, 624
ACCROCHE_1, ACCROCHE_2 = "Lancez vos challenges.", "L’app compte les ventes."

def html():
    c = [
        bandeau(ACCROCHE_1, 0, 132, 82, r=-2.5, ident="b1", align="center"),
        bandeau(ACCROCHE_2, 0, 282, 82, r=1.5, variante="clair", ident="b2", align="center"),
        mono("sehoria.fr", 0, 480, 36, largeur=L, align="center", ident="site"),
    ]
    plan = [
        {"t": "batons", "x": 232, "y": 236, "groupes": [5], "h": 112, "pas": 24, "c": "accent", "ep": 7, "graine": 3, "rot": -6},
        {"t": "presse", "x": 1318, "y": 190, "w": 104, "h": 140, "graine": 7, "rot": 5},
        {"t": "coche", "x": 1330, "y": 404, "taille": 62, "ep": 8, "graine": 9},
    ]
    p = page("couv", c, plan, palette="creme", fond="papier-creme-1.png")
    p = p.replace('viewBox="0 0 1080 1350"', f'viewBox="0 0 {L} {H}"')
    doc = document("Couverture Facebook Sehoria", [p])
    css = (f"<style>#couv{{width:{L}px;height:{H}px}} #couv .dessins{{width:{L}px;height:{H}px}}"
           f" #couv .bloc[style*='left:0px']{{width:{L}px;text-align:center}} #site .mono{{text-transform:none;letter-spacing:.06em}}</style>")
    return doc.replace("</head>", css + "</head>")

async def rendre(sortie):
    f = RACINE / "build/couverture/couverture.html"; f.write_text(html(), encoding="utf-8")
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": L, "height": H})
        await pg.goto(f.as_uri()); await pg.wait_for_selector("body[data-pret='1']")
        await pg.wait_for_timeout(300)
        await pg.locator("#couv").screenshot(path=str(sortie))
        await b.close()

if __name__ == "__main__":
    asyncio.run(rendre(RACINE / "livraison/Sehoria_couverture-facebook_1640x624.png"))
