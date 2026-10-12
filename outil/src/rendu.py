# -*- coding: utf-8 -*-
"""Rendu réel (Chromium) : PNG 1080 × 1350 par page + PDF, puis contrôles §3, §5, §6, §8 sur les fichiers produits."""
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from composants import document, RACINE
from controle import verifier, compter_mots, normaliser

POLICES_ATTENDUES = ("Fraunces", "JetBrainsMono", "JetBrains", "GochiHand", "Gochi", "Anton")  # Anton : essai « affiche » S03

JS_CONTROLES = r"""
() => {
  const res = [];
  document.querySelectorAll('.page').forEach(page => {
    const pr = page.getBoundingClientRect();
    let minSize = 999, minTxt = '';
    const lignes = [], hors = [];
    const tw = document.createTreeWalker(page, NodeFilter.SHOW_TEXT);
    while (tw.nextNode()) {
      const n = tw.currentNode, t = n.textContent.trim();
      if (!t) continue;
      const el = n.parentElement;
      if (el.closest('script') || el.closest('[aria-hidden="true"]')) continue;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const fs = parseFloat(cs.fontSize);
      if (fs < minSize) { minSize = fs; minTxt = t.slice(0, 40); }
      const r = document.createRange(); r.selectNodeContents(n);
      const bloc = el.closest('.bloc,.feuille,.carte');
      const libre = !el.closest('.bandeau,.feuille,.carte,.polaroid');
      const dessus = !!el.closest('[data-z]');
      for (const q of r.getClientRects()) {
        if (q.width < 1) continue;
        const hq = q.bottom - q.top;
        const b = {t: t.slice(0, 32), x0: q.left - pr.left, y0: q.top - pr.top + 0.22 * hq, x1: q.right - pr.left, y1: q.bottom - pr.top - 0.18 * hq,
                   bloc: bloc ? (bloc.id || bloc.className + '@' + Math.round(bloc.offsetLeft) + ',' + Math.round(bloc.offsetTop)) : '',
                   libre, dessus};
        lignes.push(b);
        if (b.x0 < 40 || b.y0 < 40 || b.x1 > 1040 || b.y1 > 1310) hors.push(b);
      }
    }
    const debord = [];
    page.querySelectorAll('.feuille,.carte,[data-cadre]').forEach(b => {
      if (b.scrollWidth > b.clientWidth + 2 || b.scrollHeight > b.clientHeight + 2)
        debord.push({el: b.className, sw: b.scrollWidth, cw: b.clientWidth, sh: b.scrollHeight, ch: b.clientHeight});
    });
    const chev = [];
    for (let i = 0; i < lignes.length; i++) for (let j = i + 1; j < lignes.length; j++) {
      const a = lignes[i], b = lignes[j];
      if (a.bloc === b.bloc) continue;
      const w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
      if (w > 0 && h > 0) {
        const aire = w * h, mini = Math.min((a.x1 - a.x0) * (a.y1 - a.y0), (b.x1 - b.x0) * (b.y1 - b.y0));
        if (aire > 0.12 * mini) chev.push([a.t, b.t, Math.round(100 * aire / mini)]);
      }
    }
    const utilisees = new Set();
    page.querySelectorAll('*').forEach(el => {
      if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
      const cs = getComputedStyle(el);
      utilisees.add(`${cs.fontStyle} ${cs.fontWeight} 40px ${cs.fontFamily.split(',')[0]}`);
    });
    const polices = [...utilisees].map(f => [f, document.fonts.check(f)]);
    const images = [...page.querySelectorAll('img.decoupe')].map(im => {
      const q = im.getBoundingClientRect();
      return {src: decodeURIComponent(im.src.replace('file://', '')), x0: q.left - pr.left, y0: q.top - pr.top, x1: q.right - pr.left, y1: q.bottom - pr.top};
    });
    const dessins = [...page.querySelectorAll('svg.dessins > g[data-t]')].map(g => {
      const q = g.getBoundingClientRect();
      return {t: g.dataset.t, x0: q.left - pr.left, y0: q.top - pr.top, x1: q.right - pr.left, y1: q.bottom - pr.top};
    });
    res.push({id: page.id, texte: page.innerText, minSize, minTxt, hors, debord, chev, polices,
              libres: lignes.filter(l => l.libre), images, dessins});
  });
  return res;
}
"""

async def _rendre(html_path: Path, dossier: Path, prefixe: str):
    async with async_playwright() as p:
        nav = await p.chromium.launch()
        pg = await nav.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        await pg.goto("file://" + str(html_path))
        await pg.wait_for_function("document.body.dataset.pret === '1'", timeout=30000)
        await pg.wait_for_timeout(200)
        rapport = await pg.evaluate(JS_CONTROLES)
        pngs = []
        for i, sec in enumerate(await pg.query_selector_all(".page"), 1):
            f = dossier / f"{prefixe}-{i:02d}.png"
            await sec.screenshot(path=str(f))
            pngs.append(f)
        pdf = dossier / f"{prefixe}.pdf"
        await pg.pdf(path=str(pdf), width="1080px", height="1350px", print_background=True, prefer_css_page_size=True)
        await nav.close()
    return rapport, pngs, pdf

def recadrer_pdf(pdf: Path, largeur_pt=810.0, hauteur_pt=1012.5):
    """Chromium arrondit la hauteur au 1/100 de pouce (1013,04 pt) : on ramène chaque page à 1080 × 1350 px exactement."""
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(str(pdf))
    w = PdfWriter()
    for pg in r.pages:
        haut = float(pg.mediabox.top)
        for boite in (pg.mediabox, pg.cropbox):
            boite.lower_left = (0, haut - hauteur_pt)
            boite.upper_right = (largeur_pt, haut)
        w.add_page(pg)
    w.add_metadata({"/Title": r.metadata.title if r.metadata and r.metadata.title else pdf.stem, "/Author": "Sehoria"})
    tmp = pdf.with_suffix(".tmp.pdf")
    with open(tmp, "wb") as f:
        w.write(f)
    tmp.replace(pdf)

def texte_pdf(pdf: Path, n: int):
    """Texte extrait du PDF (pdfium : garde l'ordre de lecture, y compris dans les blocs inclinés)."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(pdf))
    out = [doc[i].get_textpage().get_text_range().replace("\r\n", "\n") for i in range(min(n, len(doc)))]
    doc.close()
    return out

def meme_texte(a: str, b: str) -> bool:
    """Mêmes caractères (hors espaces), quel que soit l'ordre : le PDF porte exactement le texte de la page."""
    norm = lambda t: sorted(ch for ch in normaliser(t).lower() if not ch.isspace())
    return norm(a) == norm(b)

def polices_pdf(pdf: Path):
    t = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
    return [ligne.split()[0] for ligne in t if ligne.strip()]

def ecart_png_pdf(pdf: Path, pngs, dossier: Path):
    subprocess.run(["pdftoppm", "-r", "96", "-png", str(pdf), str(dossier / "_pdf")], check=True)
    ecarts = []
    rasters = sorted(dossier.glob("_pdf-*.png"))
    for f_png, f_pdf in zip(pngs, rasters):
        from PIL import ImageFilter
        a = np.asarray(Image.open(f_png).convert("RGB").filter(ImageFilter.GaussianBlur(1.2))).astype(np.int16)
        b = np.asarray(Image.open(f_pdf).convert("RGB").resize((1080, 1350)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.int16)
        ecarts.append(round(float(np.abs(a - b).mean()), 2))
        f_pdf.unlink()
    return ecarts

def texte_sur_image(r):
    """Lignes de texte sans fond posées sur les pixels opaques d'une découpe (illisible)."""
    alertes = []
    for im in r["images"]:
        png = Image.open(im["src"]).split()[-1]
        sx, sy = png.width / max(1, im["x1"] - im["x0"]), png.height / max(1, im["y1"] - im["y0"])
        a = np.asarray(png)
        for l in r["libres"]:
            x0, y0 = max(l["x0"], im["x0"]), max(l["y0"], im["y0"])
            x1, y1 = min(l["x1"], im["x1"]), min(l["y1"], im["y1"])
            if x1 <= x0 or y1 <= y0:
                continue
            zone = a[int((y0 - im["y0"]) * sy):int((y1 - im["y0"]) * sy) + 1, int((x0 - im["x0"]) * sx):int((x1 - im["x0"]) * sx) + 1]
            couvert = (zone > 128).sum() / (sx * sy)
            part = couvert / max(1.0, (l["x1"] - l["x0"]) * (l["y1"] - l["y0"]))
            if part > 0.03:
                alertes.append([l["t"], Path(im["src"]).stem, round(100 * part)])
    return alertes

ENTOURANTS = {"bulle", "ellipse"}  # dessinés autour d'un texte, exprès

def texte_sous_dessin(r):
    alertes = []
    for d in r["dessins"]:
        if d["t"] in ENTOURANTS:
            continue
        for l in r["libres"]:
            if l.get("dessus"):  # annotation posée exprès sur le dessin
                continue
            w = min(l["x1"], d["x1"]) - max(l["x0"], d["x0"]); h = min(l["y1"], d["y1"]) - max(l["y0"], d["y0"])
            if w > 0 and h > 0:
                part = w * h / max(1.0, (l["x1"] - l["x0"]) * (l["y1"] - l["y0"]))
                if part > 0.15:
                    alertes.append([l["t"], d["t"], round(100 * part)])
    return alertes

def rendre(pages_html, titre, dossier: Path, prefixe: str, formats=None, essai=False):
    """pages_html : liste de <section>. formats : liste 'A'/'B' par page (pour le contrôle de la phrase qui porte)."""
    dossier.mkdir(parents=True, exist_ok=True)
    html_path = dossier / f"{prefixe}.html"
    html_path.write_text(document(titre, pages_html, essai=essai), encoding="utf-8")
    rapport, pngs, pdf = asyncio.run(_rendre(html_path, dossier, prefixe))
    recadrer_pdf(pdf)
    textes = texte_pdf(pdf, len(pngs))
    polices = polices_pdf(pdf)
    ecarts = ecart_png_pdf(pdf, pngs, dossier)
    bilan = {"pdf": str(pdf), "polices_pdf": polices,
             "polices_hors_charte": [f for f in polices if not any(k in f for k in POLICES_ATTENDUES)], "pages": []}
    for i, (r, t_pdf) in enumerate(zip(rapport, textes)):
        fmt = (formats or ["A"] * len(pngs))[i]
        mots = compter_mots(r["texte"])
        constats, nombres, noms = verifier(t_pdf, "A" if fmt == "A" else "B")
        c_dom, _, _ = verifier(r["texte"], "A" if fmt == "A" else "B")
        constats += [c for c in c_dom if c not in constats]
        if fmt == "B":  # la phrase elle-même : ni tu ni vous, aucune compétition
            phrase = re.split(r"à\s+partager", normaliser(r["texte"]), flags=re.I)[0]
            c2, _, _ = verifier(phrase, "B-phrase")
            constats += [c for c in c2 if c not in constats]
        bilan["pages"].append({
            "id": r["id"], "png": str(pngs[i]), "mots": mots, "pdf_identique": meme_texte(t_pdf, r["texte"]),
            "taille_min_px": r["minSize"], "texte_plus_petit": r["minTxt"],
            "hors_zone_sure": r["hors"], "debordements": r["debord"], "chevauchements": r["chev"],
            "texte_sur_image": texte_sur_image(r), "texte_sous_dessin": texte_sous_dessin(r),
            "polices_chargees": all(ok for _, ok in r["polices"]),
            "ecart_png_pdf": ecarts[i] if i < len(ecarts) else None,
            "constats": constats, "nombres": nombres, "noms": noms, "texte_pdf": normaliser(t_pdf)})
    (dossier / f"{prefixe}-controle.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")
    return bilan

def resume(bilan):
    lignes = [f"Polices dans le PDF : {', '.join(sorted(set(bilan['polices_pdf'])))}"
              + (f"  ⚠ hors charte : {bilan['polices_hors_charte']}" if bilan["polices_hors_charte"] else "")]
    for p in bilan["pages"]:
        pb = []
        if p["mots"] > 30: pb.append(f"{p['mots']} mots > 30")
        if not p["pdf_identique"]: pb.append("texte du PDF ≠ texte de la page")
        if p["taille_min_px"] < 28: pb.append(f"texte à {p['taille_min_px']} px")
        if p["hors_zone_sure"]: pb.append(f"{len(p['hors_zone_sure'])} ligne(s) hors zone sûre")
        if p["debordements"]: pb.append("débordement")
        if p["chevauchements"]: pb.append(f"chevauchement {p['chevauchements'][:2]}")
        if p["texte_sur_image"]: pb.append(f"texte sur image {p['texte_sur_image'][:3]}")
        if p["texte_sous_dessin"]: pb.append(f"à regarder : texte sous un dessin {p['texte_sous_dessin'][:3]}")
        if not p["polices_chargees"]: pb.append("police non chargée")
        if p["ecart_png_pdf"] is not None and p["ecart_png_pdf"] > 6: pb.append(f"PNG ≠ PDF ({p['ecart_png_pdf']})")
        err = [c for c in p["constats"] if c[0] == "ERREUR"]
        al = [c for c in p["constats"] if c[0] == "ALERTE"]
        if err: pb.append("§6 : " + "; ".join(f"{c[1]} [{c[2]}]" for c in err))
        if al: pb.append("à relire : " + "; ".join(f"{c[1]} [{c[2]}]" for c in al))
        lignes.append(f"{p['id']:6s} {p['mots']:2d} mots · min {p['taille_min_px']:.0f}px · Δ{p['ecart_png_pdf']} · "
                      + ("OK" if not pb else " | ".join(pb)))
    return "\n".join(lignes)
