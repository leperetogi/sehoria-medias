# -*- coding: utf-8 -*-
"""Hors-série S03h, page 1 : rendu de la rampe 3D (gabarit/rampe3d.html, three.js) dans Chromium, par Playwright.
Deux passes : « photo » (la scène éclairée) et « masque » (les liserés lumineux seuls, pour les teinter en terracotta).
La scène est entièrement construite dans le gabarit : aucune image, aucun modèle 3D tiers.

    python3 src/rampe3d.py [clé=valeur …]     → assets/photos/R1-rampe.png et R1-rampe-masque.png
    python3 src/preparer_s03h.py H1piste      → assets/decoupes/H1-piste.png (bichromie, liserés terracotta, bord déchiré)
"""
import functools
import http.server
import socketserver
import sys
import threading
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "assets" / "photos"

# Cadrage retenu pour S03-H1 (17/10, 21 h) : la rampe à droite, le ciel libre à gauche pour « 9 ANS ».
PARAMS_H1 = {"fov": 42, "plat": 16, "cx": 34, "cy": 3.0, "cz": 18, "vx": -6, "vy": 9, "vz": -2}


def servir():
    gestion = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(RACINE))
    gestion.log_message = lambda *a, **k: None
    srv = socketserver.TCPServer(("127.0.0.1", 0), gestion)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def rendre(params=None, echelle=2, nom="R1-rampe", hauteur=1010):
    params = dict(params or {})
    srv = servir()
    port = srv.server_address[1]
    sorties = {}
    try:
        with sync_playwright() as pw:
            nav = pw.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                                           "--ignore-gpu-blocklist"])
            for mode in ("photo", "masque"):
                p = dict(params, mode=mode, l=1080 * echelle, h=hauteur * echelle)
                page = nav.new_page(viewport={"width": 1080 * echelle, "height": hauteur * echelle})
                erreurs = []
                page.on("pageerror", lambda e: erreurs.append(str(e)))
                page.on("console", lambda m: erreurs.append(m.text) if m.type == "error" else None)
                page.goto(f"http://127.0.0.1:{port}/gabarit/rampe3d.html?{urllib.parse.urlencode(p)}")
                page.wait_for_function("window.__fini === true", timeout=240000)
                if erreurs:
                    print("\n".join(erreurs), file=sys.stderr)
                cible = SORTIE / (f"{nom}.png" if mode == "photo" else f"{nom}-masque.png")
                page.locator("canvas").screenshot(path=str(cible))
                sorties[mode] = cible
                page.close()
            nav.close()
    finally:
        srv.shutdown()
    return sorties


if __name__ == "__main__":
    kv = dict(PARAMS_H1, **dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a))
    print(rendre(kv))
