# -*- coding: utf-8 -*-
"""Mise en page de la semaine 01 : une fonction par page. Les mots viennent de semaine01.py (seule source du texte)."""
from composants import (entete, centres_zones, polaroid, pastille, une_phrase_par_ligne, couleur_soulignes, bandeau, texte, mono, main, numero, feuille, carte, ruban, decoupe, logo,
                        page, md, marquer, bloc)
from semaine01 import PUBLICATIONS, CTA_ACTION, CTA_FREIN, CTA_SIGNATURE, PARTAGE

A1 = PUBLICATIONS[0]["pages"]
A2 = PUBLICATIONS[1]["pages"]
B1 = PUBLICATIONS[2]["pages"]

VIOLET, TERRA, ENCRE, CREME = "#4120CF", "#C06B3E", "#26203A", "#FBF5EF"

def fleche_defiler(x=384, y=1266, c="accent"):
    return {"t": "fleche", "de": [x, y], "a": [x + 92, y - 4], "courbe": -0.35, "c": c, "ep": 4.5, "tete": 20, "graine": 5}

def au_dessus(html_bloc, z=50):
    """Bloc de texte posé au-dessus des dessins (ex. annotation dans le tableau dessiné)."""
    return html_bloc.replace('class="bloc"', f'class="bloc" data-z="{z}"', 1).replace('style="', f'style="z-index:{z};', 1)

# ============ A1 · Votre premier challenge en 5 étapes (violet + crème) ============

def a1_01():
    p = A1[0]
    c = [
        decoupe("U1", (900, 1230), droite=-120, bas=-70, eclaircir=True),
        main(p["main"], 92, 390, 64, r=-6, ident="bulle"),
        main("?", 452, 196, 92, r=-8),
        main("?", 528, 132, 66, r=10),
        bandeau(p["bandeau1"], 60, 742, 60, r=-3),
        bandeau(p["titre"], 38, 830, 138, r=1.5, variante="clair geant"),
        bandeau(couleur_soulignes(p["bandeau2"], "creme"), 96, 1024, 64, r=-1.5),
        pastille(p["label"], 60, 1226, ident="suite"),
    ]
    plan = [
        {"t": "bulle", "autour": "#bulle", "queue": [478, 436], "c": "accent", "graine": 3, "marge": 50, "margeY": 38, "rot": -6},
        {"t": "fleche", "apres": "#suite", "c": "accent", "ep": 4.5, "tete": 20, "graine": 5},
    ]
    return page("A1-01", c, plan, palette="creme", fond="papier-creme-1.png")

def a1_02():
    p = A1[1]
    cit = f'<div class="texte" style="font-size:62px;font-style:italic;font-weight:600">{md(p["citation"])}</div>'
    c = [
        feuille(cit, 62, 92, 956, r=-1.2, padding="46px 58px 54px"),
        ruban(452, 64, r=-4, variante="violet"),
        decoupe("U2-buee", (880, 480), gauche=86, haut=380, rot=-57),
        main(p["main"], 614, 888, 60, r=5, ident="qui"),
        bandeau(couleur_soulignes(p["texte"], "creme"), 64, 1060, 56, r=-1.5, maxw=950),
    ]
    plan = [
        {"t": "fleche", "de": [604, 912], "a": [470, 812], "courbe": -0.3, "c": "accent", "ep": 4.5, "graine": 7, "tete": 22},
    ]
    return page("A1-02", c, plan, palette="creme", fond="papier-creme-2.png")

def _entete_etape(p, n, texte=None, taille=50, maxw=940):
    t = ""
    if texte:
        t = f'<div style="font-size:{taille}px;max-width:{maxw}px">{md(texte)}</div>'
    return [numero(n, droite=64, haut=60, taille=280), entete(p["label"], p["titre"], t)]

def a1_03():
    p = A1[2]
    icones = ["photochromique", "polarisant2", "antireflet"]
    cartes = [(52, 566, -4), (388, 540, 3), (722, 578, -2)]
    c = _entete_etape(p, "1", p["texte"], 50, 700)
    plan = []
    for i, ((x, y, r), icone, etiquette) in enumerate(zip(cartes, icones, p["cartes"])):
        c.append(carte(x, y, 306, 340, r=r, ident=f"c{i + 1}"))
        c.append(au_dessus(bloc(f'<div class="main etiquette" style="font-size:40px;color:#26203A;--r:{r}deg">{md(etiquette)}</div>',
                                x + 14, y + 218, largeur=278), 45))
        plan.append({"t": "icone", "nom": icone, "x": x + 58, "y": y + 16, "w": 190, "graine": 51 + 10 * i, "rot": r})
    c.append(texte(une_phrase_par_ligne(p["chute"]), 72, 1030, 72, maxw=940, classe="chute"))
    plan += [{"t": "ellipse", "boite": [52, 566, 306, 340], "marge": 28, "c": "accent", "ep": 7, "graine": 9, "rot": -6}]
    return page("A1-03", c, plan, palette="creme", fond="papier-creme-3.png")

def a1_04():
    p = A1[3]
    c = _entete_etape(p, "2", une_phrase_par_ligne(p["texte"]), 46, 940) + [
        decoupe("U4", (370, 660), gauche=650, haut=624),
        texte(une_phrase_par_ligne(p["chute"]), 72, 1060, 72, maxw=540, classe="chute"),
    ]
    plan = [{"t": "infini", "x": 86, "y": 730, "w": 440, "h": 190, "c": "accent", "ep": 10, "graine": 77, "rot": -4}]
    return page("A1-04", c, plan, palette="creme", fond="papier-creme-4.png")

def a1_05():
    p = A1[4]
    c = _entete_etape(p, "3", p["texte"], 50, 700) + [
        decoupe("U5", (520, 500), gauche=290, haut=520, dechire=True, rot=-4),
        ruban(500, 500, r=-3, variante="violet"),
        texte(p["chute"], 72, 1118, 64, maxw=940, classe="chute"),
    ]
    return page("A1-05", c, [], palette="creme", fond="papier-creme-2.png")

def a1_06():
    p = A1[5]
    c = _entete_etape(p, "4", une_phrase_par_ligne(p["texte"]), 50, 940) + [
        carte(150, 590, 640, 440, r=2.5, ident="regle"),
        ruban(390, 568, r=-4, variante="violet"),
        texte(p["chute"], 72, 1138, 78, maxw=940, classe="chute"),
    ]
    plan = [
        {"t": "ecriture", "boite": [214, 636, 520, 350], "lignes": 6, "coches": [0, 2], "graine": 63, "rot": 2.5},
        {"t": "feutre", "x": 700, "y": 1030, "rot": -28, "longueur": 300, "epaisseur": 44, "c": "accent", "graine": 83},
    ]
    return page("A1-06", c, plan, palette="creme", fond="papier-creme-3.png")

def a1_07():
    p = A1[6]
    c = _entete_etape(p, "5", p["texte"], 50, 940)
    plan = []
    jours = [[1], [2], [3], [4], [5], [5, 1]]
    for i, g in enumerate(jours):
        x, y = 70 + (i % 3) * 318, 520 + (i // 3) * 256
        r = [-3, 2, -1.5, 2.5, -2, 1.5][i]
        c.append(carte(x, y, 290, 222, r=r))
        plan.append({"t": "batons", "x": x + 60, "y": y + 62, "groupes": g, "h": 96, "pas": 22, "c": "encre", "ep": 6,
                     "graine": 30 + i, "rot": r})
        plan.append({"t": "coche", "x": x + 214, "y": y + 42, "taille": 42, "graine": 140 + i})
    c.append(texte(p["chute"], 72, 1084, 64, maxw=940, classe="chute"))
    return page("A1-07", c, plan, palette="creme", fond="papier-creme-4.png")

def a1_08():
    p = A1[7]
    c = [
        bandeau(p["pont"], 52, 160, 88, r=-2, variante="clair titre"),
        texte(marquer(p["chute"], "c’est l’app."), 76, 330, 94, maxw=960, classe="chute"),
        bandeau(CTA_ACTION, 58, 560, 62, r=-2, variante="titre", ident="action"),
        texte(CTA_FREIN.replace("sans engagement", "sans~engagement"), 80, 738, 44, maxw=900, couleur="#3A3350"),
        logo(342, 1000, 140),
        mono(CTA_SIGNATURE, 60, 1190, 28, couleur="#6E6782", largeur=960, align="center"),
    ]
    plan = [
        {"t": "fleche", "de": [930, 470], "a": [980, 560], "courbe": -0.45, "c": "accent", "ep": 5.5, "graine": 4, "tete": 28},
    ]
    return page("A1-08", c, plan, palette="creme", fond="papier-creme-1.png", miroir=True)

# ============ A2 · Le tableau à bâtons (violet + terracotta) ============

def a2_01():
    p = A2[0]
    c = [
        decoupe("U6-chimere", (660, 890), droite=-70, bas=-70),
        bandeau(p["bandeau1"], 72, 116, 64, r=-3),
        bandeau(p["titre"], 50, 204, 138, r=1.5, variante="clair geant"),
        bandeau(couleur_soulignes(p["bandeau2"], "terracotta"), 84, 408, 60, r=-1.5),
        main(p["main"], 128, 648, 64, r=-6, ident="bulle"),
        mono(p["label"], 72, 1246),
    ]
    plan = [
        {"t": "bulle", "autour": "#bulle", "queue": [452, 704], "c": "accent", "graine": 5, "marge": 50, "margeY": 36, "rot": -6},
        {"t": "batons", "x": 110, "y": 950, "groupes": [5, 5, 2], "h": 92, "pas": 24, "c": "accent", "ep": 7, "graine": 3, "rot": -4},
        fleche_defiler(),
    ]
    return page("A2-01", c, plan, palette="terracotta", fond="papier-creme-2.png")

def a2_02():
    p = A2[1]
    phrase1, phrase2 = p["chute"].split(". ", 1)
    c = [
        bandeau(p["texte"], 54, 96, 52, r=-1, variante="clair", maxw=970),
        au_dessus(main(p["main"], 700, 590, 50, r=-5, ident="qui")),
        texte(phrase1 + ".", 72, 1030, 66, maxw=940, poids="700"),
        texte(couleur_soulignes(marquer(phrase2, "ouvre le débat."), "terracotta"), 72, 1116, 70, maxw=940, classe="chute"),
    ]
    plan = [
        {"t": "tableau", "x": 100, "y": 330, "w": 880, "h": 540, "rot": -2, "graine": 44,
         "lignes": [[5, 5, 3], [5, 4], [5, 5, 5, 1], [3, 5]], "efface": [1, 1], "entoure": [2, 3]},
        {"t": "fleche", "de": [712, 656], "a": [664, 672], "courbe": 0.3, "c": "accent", "ep": 4.5, "graine": 6, "tete": 18},
    ]
    return page("A2-02", c, plan, palette="terracotta", fond="papier-creme-3.png")

def a2_03():
    p = A2[2]
    c = _entete_etape(p, "1", une_phrase_par_ligne(p["texte"]), 46, 940) + [
        texte(p["chute"], 72, 1140, 70, maxw=940, classe="chute"),
    ]
    plan = [
        # un bâton avec son devis : il compte
        {"t": "batons", "x": 110, "y": 590, "groupes": [1], "h": 270, "pas": 30, "c": "encre", "ep": 17, "graine": 7, "rot": 3},
        {"t": "presse", "x": 190, "y": 570, "w": 240, "h": 300, "rot": -3, "graine": 91},
        {"t": "coche", "x": 270, "y": 960, "taille": 76, "ep": 9, "graine": 111},
        # un bâton sans devis : il ne compte pas
        {"t": "batons", "x": 610, "y": 590, "groupes": [1], "h": 270, "pas": 30, "c": "encre", "ep": 17, "graine": 8, "rot": -3},
        {"t": "presse", "x": 690, "y": 570, "w": 240, "h": 300, "rot": 3, "vide": True, "graine": 92},
        {"t": "croix", "x": 770, "y": 985, "taille": 40, "ep": 9, "graine": 131},
    ]
    return page("A2-03", c, plan, palette="terracotta", fond="papier-creme-4.png")

def a2_04():
    p = A2[3]
    c = _entete_etape(p, "2", p["texte"], 50, 860) + [
        au_dessus(main(p["main"], 470, 1080, 56, r=-4, ident="manque", maxw=560)),
    ]
    plan = [
        {"t": "batons", "x": 150, "y": 640, "groupes": [1], "h": 250, "pas": 30, "c": "accent", "ep": 15, "graine": 17, "rot": 6},
        {"t": "feutre", "x": 168, "y": 896, "rot": -52, "longueur": 330, "epaisseur": 50, "c": "accent", "graine": 85},
        {"t": "batons", "x": 560, "y": 700, "groupes": [5, 3], "h": 110, "pas": 25, "c": "encre", "ep": 7, "graine": 44, "rot": -2},
        {"t": "manque", "x": 771, "y": 698, "h": 110, "c": "accent", "ep": 6, "graine": 45},
        {"t": "fleche", "de": [700, 1076], "a": [768, 840], "courbe": -0.2, "c": "accent", "ep": 5, "graine": 46, "tete": 24},
    ]
    return page("A2-04", c, plan, palette="terracotta", fond="papier-creme-1.png")

def a2_05():
    p = A2[4]
    c = _entete_etape(p, "3", p["texte"], 50, 900) + [
        texte(p["chute"], 72, 1130, 78, maxw=940, classe="chute"),
    ]
    plan = []
    for i, (x, r) in enumerate([(84, -4), (318, 2), (552, -2), (786, 3)]):
        y = 640 + (i % 2) * 36
        plan.append({"t": "presse", "x": x, "y": y, "w": 190, "h": 240, "rot": r, "graine": 93 + i})
        plan.append({"t": "coche", "x": x + 118, "y": y + 206, "taille": 56, "ep": 7, "graine": 112 + i})
    return page("A2-05", c, plan, palette="terracotta", fond="papier-creme-2.png")

def a2_06():
    p = A2[5]
    boite, rot, gx, gy = (880, 480), -57, 86, 500
    gauche, droite = centres_zones("U2", "U2-verres", boite, rot, gx, gy)
    c = _entete_etape(p, "4", p["texte"], 46, 900) + [
        decoupe("U2", boite, gauche=gx, haut=gy, rot=rot),
        texte(p["chute"], 72, 1130, 64, maxw=940, classe="chute"),
    ]
    plan = [
        {"t": "montee", "x": round(gauche["cx"] - 80), "y": round(gauche["cy"] - 52), "w": 160, "h": 104, "marches": 4,
         "c": "accent", "ep": 7, "graine": 151, "rot": -8},
        {"t": "montee", "x": round(droite["cx"] - 66), "y": round(droite["cy"] - 44), "w": 132, "h": 88, "marches": 3,
         "c": "accent", "ep": 7, "graine": 152, "rot": -8},
    ]
    return page("A2-06", c, plan, palette="terracotta", fond="papier-creme-3.png")

def a2_07():
    p = A2[6]
    c = [
        bandeau(p["pont"], 52, 160, 80, r=-2, variante="clair titre"),
        texte(couleur_soulignes(marquer(p["chute"], "non."), "terracotta"), 76, 330, 96, maxw=960, classe="chute"),
        bandeau(CTA_ACTION, 58, 560, 62, r=-2, variante="titre", ident="action"),
        texte(CTA_FREIN.replace("sans engagement", "sans~engagement"), 80, 738, 44, maxw=900, couleur="#3A3350"),
        logo(342, 1000, 140),
        mono(CTA_SIGNATURE, 60, 1190, 28, couleur="#6E6782", largeur=960, align="center"),
    ]
    plan = [
        {"t": "fleche", "de": [930, 470], "a": [980, 560], "courbe": -0.45, "c": "accent", "ep": 5.5, "graine": 4, "tete": 28},
    ]
    return page("A2-07", c, plan, palette="terracotta", fond="papier-creme-4.png", miroir=True)

# ============ B1 · La phrase qui porte ============

def b1_01():
    p = B1[0]
    phrase = f'<div class="texte" style="font-size:68px;font-weight:700;line-height:1.1;text-align:center">{md(p["phrase"])}</div>'
    chute = f'<div class="chute" style="font-size:76px;text-align:center;margin-top:34px">{md(marquer(p["chute"], "aussi."))}</div>'
    guill = ('<div class="bloc" aria-hidden="true" style="left:465px;top:100px;width:150px;height:150px;background:#26203A;'
             'transform:rotate(-4deg);z-index:22;box-shadow:8px 8px 0 rgba(0,0,0,.18)">'
             '<div style="font:800 210px/1 Fraunces;font-variation-settings:\'opsz\' 144,\'SOFT\' 100;color:#FBF5EF;'
             'text-align:center;margin-top:-18px">«</div></div>')
    c = [
        feuille(phrase + chute, 88, 170, 904, hauteur=560, r=-2, padding="128px 48px 60px"),
        guill,
        decoupe("U7", (460, 700), gauche=316, bas=-58, contour=CREME, couleur=ENCRE, devant=True),
        mono(PARTAGE, 72, 1182, 28, couleur=CREME, maxw=250),
        logo(826, 1194, 46, "creme"),
        mono("sehoria.fr", 826, 1252, 28, couleur=CREME),
    ]
    return page("B1-01", c, [], palette="violet", fond="fond-violet.png", grille=False)

ESSAI = [a1_01, a1_02, a1_03, a1_04, a1_08, a2_01, a2_02, b1_01]

PUBLICATIONS_MEP = {
    "S01-A1": [a1_01, a1_02, a1_03, a1_04, a1_05, a1_06, a1_07, a1_08],
    "S01-A2": [a2_01, a2_02, a2_03, a2_04, a2_05, a2_06, a2_07],
    "S01-B1": [b1_01],
}
