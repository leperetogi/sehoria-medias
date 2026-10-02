/* Dessins « à la main » du gabarit Sehoria (rough.js) : soulignés, flèches, gribouillis, bâtons, tableau, icônes.
   Chaque page porte un <script type="application/json" class="plan"> : liste de commandes en coordonnées de page. */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  const ENCRE = "#26203A";

  function aleat(graine) { // mulberry32 : dessins reproductibles
    let a = graine >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function varCss(el, nom, def) { const v = getComputedStyle(el).getPropertyValue(nom).trim(); return v || def; }
  function couleur(page, c) {
    if (!c || c === "accent") return varCss(page, "--accent", "#4120CF");
    if (c === "violet") return "#4120CF";
    if (c === "terracotta") return "#C06B3E";
    if (c === "encre") return ENCRE;
    if (c === "creme") return "#FBF5EF";
    return c;
  }
  function calque(parent) {
    let s = parent.querySelector(":scope > svg.local");
    if (!s) { s = document.createElementNS(NS, "svg"); s.setAttribute("class", "local"); parent.appendChild(s); }
    return s;
  }
  function boiteDe(page, sel) {
    const el = page.querySelector(sel);
    const r = el.getBoundingClientRect(), p = page.getBoundingClientRect();
    return [r.left - p.left, r.top - p.top, r.width, r.height];
  }

  /* ---- soulignés sous [[mot]] : tracés dans le repère local du bloc (suivent sa rotation) ---- */
  function soulignes(page) {
    page.querySelectorAll(".souligne").forEach((sp, i) => {
      const svg = calque(sp.offsetParent);
      const rc = rough.svg(svg);
      const x0 = sp.offsetLeft - 6, x1 = sp.offsetLeft + sp.offsetWidth + 8;
      const y = sp.offsetTop + sp.offsetHeight * (parseFloat(sp.dataset.y || "0.93"));
      const c = couleur(page, sp.dataset.couleur);
      const ep = parseFloat(sp.dataset.ep || "6");
      svg.appendChild(rc.curve([[x0, y + 3], [(x0 + x1) / 2, y + 7], [x1, y - 3]],
        { stroke: c, strokeWidth: ep, roughness: 1.1, bowing: 1.2, seed: 17 + i * 13 }));
    });
  }

  /* ---- primitives ---- */
  function fleche(rc, svg, o, page) {
    if (o.apres) {  // dans la marge droite de l'élément (pastille « suite »)
      const [bx, by, bw, bh] = boiteDe(page, o.apres);
      o = { ...o, de: [bx + bw - 100, by + bh * 0.55], a: [bx + bw - 22, by + bh * 0.45], courbe: -0.35 };
    }
    const [x1, y1] = o.de, [x2, y2] = o.a;
    const c = couleur(page, o.c), ep = o.ep || 5, k = (o.courbe === undefined ? 0.25 : o.courbe);
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1;
    const cx = mx - dy * k, cy = my + dx * k;
    const pts = [];
    for (let t = 0; t <= 1.0001; t += 0.08) {
      const a = (1 - t) * (1 - t), b = 2 * (1 - t) * t, d = t * t;
      pts.push([a * x1 + b * cx + d * x2, a * y1 + b * cy + d * y2]);
    }
    const opt = { stroke: c, strokeWidth: ep, roughness: 1.0, bowing: 0.8, seed: o.graine || 3 };
    svg.appendChild(rc.curve(pts, opt));
    const ang = Math.atan2(y2 - cy, x2 - cx), s = o.tete || 28;
    [0.5, -0.5].forEach((d, j) => svg.appendChild(
      rc.line(x2, y2, x2 - s * Math.cos(ang + d), y2 - s * Math.sin(ang + d), { ...opt, seed: (o.graine || 3) + 5 + j })));
  }

  function gribouillis(rc, svg, o, page) {
    const [x, y, w, h] = o.boite, rnd = aleat(o.graine || 7);
    let px = x + w * 0.5, py = y + h * 0.5, ang = rnd() * 6.28;
    const pts = [[px, py]], n = o.points || 110, cx = x + w / 2, cy = y + h / 2;
    for (let i = 0; i < n; i++) {
      ang += 0.55 + (rnd() - 0.5) * 1.3;
      const pas = (o.pas || 34) * (0.6 + rnd() * 0.8);
      let nx = px + Math.cos(ang) * pas, ny = py + Math.sin(ang) * pas * 0.85;
      if (nx < x || nx > x + w || ny < y || ny > y + h) {
        ang = Math.atan2(cy - py, cx - px) + (rnd() - 0.5) * 0.9;
        nx = px + Math.cos(ang) * pas; ny = py + Math.sin(ang) * pas;
      }
      px = nx; py = ny; pts.push([px, py]);
    }
    svg.appendChild(rc.curve(pts, { stroke: couleur(page, o.c), strokeWidth: o.ep || 5, roughness: 0.7, bowing: 0.4, seed: o.graine || 7 }));
  }

  function ellipse(rc, svg, o, page) {
    let [x, y, w, h] = o.boite || boiteDe(page, o.autour);
    const m = o.marge === undefined ? 18 : o.marge;
    x -= m; y -= m; w += 2 * m; h += 2 * m;
    const opt = { stroke: couleur(page, o.c), strokeWidth: o.ep || 5, roughness: 1.3, bowing: 1, seed: o.graine || 9 };
    if (o.remplir) { opt.fill = couleur(page, o.remplir); opt.fillStyle = o.style || "solid"; }
    const el = rc.ellipse(x + w / 2, y + h / 2, w, h, opt);
    if (o.rot) el.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
    svg.appendChild(el);
  }

  function bulle(rc, svg, o, page) {
    let [x, y, w, h] = boiteDe(page, o.autour);
    const mx = o.marge || 30, my = o.margeY || 26;
    const cx = x + w / 2, cy = y + h / 2, W = w + 2 * mx, H = h + 2 * my;
    const opt = { stroke: couleur(page, o.c), strokeWidth: o.ep || 4.5, roughness: 1.4, bowing: 1, seed: o.graine || 21 };
    const g = document.createElementNS(NS, "g");
    g.appendChild(rc.ellipse(cx, cy, W, H, opt));
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${cx} ${cy})`);
    svg.appendChild(g);
    if (o.queue) { // petite queue de bulle vers la cible
      const [tx, ty] = o.queue, ang = Math.atan2(ty - cy, tx - cx);
      const bx = cx + (W / 2) * Math.cos(ang) * 0.96, by = cy + (H / 2) * Math.sin(ang) * 0.96;
      const perp = ang + Math.PI / 2, e = 16;
      svg.appendChild(rc.linearPath([[bx + e * Math.cos(perp), by + e * Math.sin(perp)], [tx, ty],
        [bx - e * Math.cos(perp), by - e * Math.sin(perp)]], { ...opt, seed: opt.seed + 1 }));
    }
  }

  function groupeBatons(rc, g, x, y, n, h, pas, opt, rnd) {
    const verticales = Math.min(n, 4);
    for (let i = 0; i < verticales; i++) {
      const xx = x + i * pas + (rnd() - 0.5) * 4;
      g.appendChild(rc.line(xx + (rnd() - 0.5) * 6, y + (rnd() - 0.5) * 6, xx + (rnd() - 0.5) * 6, y + h + (rnd() - 0.5) * 6,
        { ...opt, seed: Math.floor(rnd() * 1e6) }));
    }
    if (n >= 5) g.appendChild(rc.line(x - pas * 0.6, y + h * 0.82, x + pas * 3.6, y + h * 0.12, { ...opt, seed: Math.floor(rnd() * 1e6) }));
    return x + (Math.min(n, 4) - 1) * pas + pas * 2.4;
  }

  function batons(rc, svg, o, page) {
    const rnd = aleat(o.graine || 31);
    const opt = { stroke: couleur(page, o.c || "encre"), strokeWidth: o.ep || 7, roughness: 1.1, bowing: 1.2 };
    let x = o.x;
    const g = document.createElementNS(NS, "g");
    (o.groupes || [5]).forEach(n => { x = groupeBatons(rc, g, x, o.y, n, o.h || 90, o.pas || 24, opt, rnd); });
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${o.x} ${o.y})`);
    svg.appendChild(g);
  }

  function forme(rc, g, nom, cx, cy, s, opt) {
    if (nom === "rond") g.appendChild(rc.circle(cx, cy, s, opt));
    else if (nom === "carre") g.appendChild(rc.rectangle(cx - s / 2, cy - s / 2, s, s, opt));
    else if (nom === "triangle") g.appendChild(rc.polygon([[cx, cy - s / 2], [cx + s / 2, cy + s / 2], [cx - s / 2, cy + s / 2]], opt));
    else g.appendChild(rc.polygon([[cx, cy - s / 2], [cx + s / 2, cy], [cx, cy + s / 2], [cx - s / 2, cy]], opt));
  }

  /* ---- tableau à bâtons dessiné ---- */
  function tableau(rc, svg, o, page) {
    const rnd = aleat(o.graine || 41);
    const { x, y, w, h } = o;
    const g = document.createElementNS(NS, "g");
    g.appendChild(rc.rectangle(x, y, w, h, { stroke: "#8E88A3", strokeWidth: 10, roughness: 0.7, bowing: 0.6,
      fill: "#FFFFFF", fillStyle: "solid", seed: 5 }));
    // auget et feutre
    g.appendChild(rc.rectangle(x + w * 0.08, y + h + 10, w * 0.84, 16, { stroke: "#8E88A3", strokeWidth: 5, roughness: 0.6, seed: 6 }));
    g.appendChild(rc.rectangle(x + w * 0.62, y + h - 4, 150, 22, { stroke: ENCRE, strokeWidth: 4, roughness: 0.8, fill: ENCRE, fillStyle: "solid", seed: 7 }));
    g.appendChild(rc.rectangle(x + w * 0.62 + 150, y + h - 1, 34, 16, { stroke: ENCRE, strokeWidth: 4, roughness: 0.8, fill: "#FFFFFF", fillStyle: "solid", seed: 8 }));
    const lignes = o.lignes, pad = 34, hl = (h - 2 * pad) / lignes.length;
    const formes = ["rond", "triangle", "carre", "losange"];
    const optT = { stroke: ENCRE, strokeWidth: 6.5, roughness: 1.1, bowing: 1.2 };
    let ancre = null;
    lignes.forEach((grp, i) => {
      const yl = y + pad + i * hl, hb = hl * 0.62, yb = yl + (hl - hb) / 2;
      forme(rc, g, formes[i % 4], x + 58, yl + hl / 2, 34, { stroke: couleur(page, "violet"), strokeWidth: 5, roughness: 1, seed: 60 + i });
      g.appendChild(rc.line(x + 96, yl + 6, x + 96, yl + hl - 6, { stroke: "#C9C5D6", strokeWidth: 3, roughness: 1, seed: 70 + i }));
      let xx = x + 128;
      grp.forEach((n, j) => {
        const efface = o.efface && o.efface[0] === i && o.efface[1] === j;
        const gg = efface ? document.createElementNS(NS, "g") : g;
        const x0 = xx;
        xx = groupeBatons(rc, gg, xx, yb, n, hb, 22, efface ? { ...optT, stroke: "#B9B4C7" } : optT, rnd);
        if (efface) {
          gg.setAttribute("opacity", "0.55"); g.appendChild(gg);
          g.appendChild(rc.ellipse((x0 + xx) / 2 - 18, yb + hb / 2, (xx - x0) + 10, hb * 1.05,
            { stroke: "none", fill: "#DAD6E4", fillStyle: "zigzag", hachureGap: 7, fillWeight: 3, hachureAngle: 20, roughness: 2, seed: 90 }));
        }
        if (o.entoure && o.entoure[0] === i && o.entoure[1] === j) ancre = [(x0 + xx) / 2 - 14, yb + hb / 2, (xx - x0) + 26, hb * 1.35];
      });
    });
    if (ancre) {
      g.appendChild(rc.ellipse(ancre[0], ancre[1], ancre[2], ancre[3],
        { stroke: couleur(page, "accent"), strokeWidth: 6, roughness: 1.4, bowing: 1.2, seed: 99 }));
    }
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
    svg.appendChild(g);
  }

  /* ---- icônes métier dessinées ---- */
  function lunettesTrait(rc, g, cx, cy, r, opt, pleines) {
    const e = r * 0.34;
    [cx - r - e, cx + r + e].forEach((lx, i) => {
      const o = { ...opt, seed: opt.seed + i };
      if (pleines) { o.fill = ENCRE; o.fillStyle = "solid"; }
      g.appendChild(rc.ellipse(lx, cy, r * 2, r * 1.72, o));
    });
    g.appendChild(rc.curve([[cx - e, cy - r * 0.15], [cx, cy - r * 0.42], [cx + e, cy - r * 0.15]], { ...opt, seed: opt.seed + 5 }));
    g.appendChild(rc.line(cx - 2 * r - e, cy - r * 0.35, cx - 2 * r - e - r * 0.45, cy - r * 0.62, { ...opt, seed: opt.seed + 6 }));
    g.appendChild(rc.line(cx + 2 * r + e, cy - r * 0.35, cx + 2 * r + e + r * 0.45, cy - r * 0.62, { ...opt, seed: opt.seed + 7 }));
  }
  function icone(rc, svg, o, page) {
    const g = document.createElementNS(NS, "g");
    const opt = { stroke: couleur(page, o.c || "encre"), strokeWidth: o.ep || 4.5, roughness: 1.0, bowing: 1, seed: o.graine || 50 };
    const { x, y, w } = o, cx = x + w / 2, cy = y + w / 2;
    if (o.nom === "progressif") {
      // une paire dont le bas des verres (zone de près) est hachuré
      const r = w * 0.19, e = r * 0.34;
      lunettesTrait(rc, g, cx, cy, r, opt, false);
      [cx - r - e, cx + r + e].forEach((lx, i) => g.appendChild(rc.ellipse(lx, cy + r * 0.42, r * 1.55, r * 0.72,
        { ...opt, stroke: "none", fill: couleur(page, "accent"), fillStyle: "hachure", hachureGap: 6, hachureAngle: -35, fillWeight: 2.5, seed: opt.seed + 20 + i })));
    } else if (o.nom === "deuxpaires") {
      lunettesTrait(rc, g, cx + w * 0.07, cy - w * 0.14, w * 0.16, { ...opt, stroke: "#8E88A3" }, false);
      lunettesTrait(rc, g, cx - w * 0.04, cy + w * 0.12, w * 0.17, opt, false);
    } else if (o.nom === "solaire") {
      lunettesTrait(rc, g, cx, cy + w * 0.12, w * 0.17, opt, true);
      const sx = cx + w * 0.26, sy = cy - w * 0.26, sr = w * 0.09;
      g.appendChild(rc.circle(sx, sy, sr * 2, { ...opt, seed: opt.seed + 9 }));
      for (let i = 0; i < 8; i++) {
        const a = i * Math.PI / 4;
        g.appendChild(rc.line(sx + Math.cos(a) * sr * 1.45, sy + Math.sin(a) * sr * 1.45, sx + Math.cos(a) * sr * 2.1, sy + Math.sin(a) * sr * 2.1, { ...opt, strokeWidth: 3.5, seed: opt.seed + 10 + i }));
      }
    } else if (o.nom === "photochromique") {
      // un verre clair, un verre teinté, le soleil au-dessus du verre teinté
      const r = w * 0.17, e = r * 0.34, yy = cy + w * 0.12;
      lunettesTrait(rc, g, cx, yy, r, opt, false);
      g.appendChild(rc.ellipse(cx + r + e, yy, r * 2, r * 1.72, { ...opt, stroke: "none", fill: "#3A3350", fillStyle: "solid", seed: opt.seed + 30 }));
      g.appendChild(rc.ellipse(cx - r - e, yy, r * 1.3, r * 1.05, { ...opt, stroke: "none", fill: "#8E88A3", fillStyle: "hachure", hachureGap: 7, hachureAngle: -40, fillWeight: 2, seed: opt.seed + 31 }));
      const sx = cx + r + e + w * 0.06, sy = cy - w * 0.25, sr = w * 0.085;
      g.appendChild(rc.circle(sx, sy, sr * 2, { ...opt, seed: opt.seed + 9 }));
      for (let i = 0; i < 8; i++) {
        const a = i * Math.PI / 4;
        g.appendChild(rc.line(sx + Math.cos(a) * sr * 1.45, sy + Math.sin(a) * sr * 1.45, sx + Math.cos(a) * sr * 2.1, sy + Math.sin(a) * sr * 2.1, { ...opt, strokeWidth: 3.5, seed: opt.seed + 10 + i }));
      }
    } else if (o.nom === "polarisant2") {
      // deux paires ; la seconde, devant, porte des verres polarisants (lignes parallèles)
      const r = w * 0.155, e = r * 0.34;
      lunettesTrait(rc, g, cx + w * 0.08, cy - w * 0.16, r * 0.95, { ...opt, stroke: "#8E88A3" }, false);
      const px = cx - w * 0.04, py = cy + w * 0.12;
      lunettesTrait(rc, g, px, py, r, opt, false);
      [px - r - e, px + r + e].forEach((lx, i) => g.appendChild(rc.ellipse(lx, py, r * 1.75, r * 1.45,
        { ...opt, stroke: "none", fill: couleur(page, "accent"), fillStyle: "hachure", hachureGap: 6.5, hachureAngle: 90, fillWeight: 2.4, seed: opt.seed + 20 + i })));
    } else if (o.nom === "antireflet") {
      // verre gauche : reflets barrés d'une petite croix ; verre droit : net
      const r = w * 0.18, e = r * 0.34, yy = cy + w * 0.04, lx = cx - r - e;
      lunettesTrait(rc, g, cx, yy, r, opt, false);
      g.appendChild(rc.line(lx - r * 0.5, yy + r * 0.05, lx - r * 0.1, yy - r * 0.45, { ...opt, stroke: "#9A95A8", strokeWidth: 4, seed: opt.seed + 50 }));
      g.appendChild(rc.line(lx - r * 0.2, yy + r * 0.3, lx + r * 0.25, yy - r * 0.22, { ...opt, stroke: "#9A95A8", strokeWidth: 4, seed: opt.seed + 55 }));
      const k = r * 0.42, ox = lx + r * 0.05, oy = yy - r * 0.05;
      g.appendChild(rc.line(ox - k, oy - k, ox + k, oy + k, { ...opt, stroke: couleur(page, "accent"), strokeWidth: 5, seed: opt.seed + 60 }));
      g.appendChild(rc.line(ox - k, oy + k, ox + k, oy - k, { ...opt, stroke: couleur(page, "accent"), strokeWidth: 5, seed: opt.seed + 61 }));
    }
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${cx} ${cy})`);
    svg.appendChild(g);
  }

  /* ---- lignes d'écriture sur une note (la règle) ---- */
  function ecriture(rc, svg, o, page) {
    const rnd = aleat(o.graine || 61);
    const [x, y, w, h] = o.boite, n = o.lignes || 6, pas = h / n;
    const g = document.createElementNS(NS, "g");
    const opt = { stroke: couleur(page, o.c || "encre"), strokeWidth: o.ep || 3.2, roughness: 0.9, bowing: 0.6 };
    for (let i = 0; i < n; i++) {
      const yy = y + i * pas + pas * 0.55;
      let xx = x + (o.coches && o.coches.includes(i) ? 62 : 0);
      if (o.coches && o.coches.includes(i)) {
        g.appendChild(rc.rectangle(x, yy - 20, 34, 34, { ...opt, seed: 200 + i }));
        g.appendChild(rc.linearPath([[x + 4, yy - 4], [x + 15, yy + 10], [x + 42, yy - 30]], { ...opt, stroke: couleur(page, "accent"), strokeWidth: 5, seed: 220 + i }));
      }
      const fin = x + w * (0.55 + rnd() * 0.45);
      const pts = [];
      for (let px = xx; px < fin; px += 9) pts.push([px, yy + Math.sin(px * 0.21 + i) * 6 + (rnd() - 0.5) * 7]);
      if (pts.length > 2) g.appendChild(rc.curve(pts, { ...opt, seed: 240 + i }));
    }
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
    svg.appendChild(g);
  }

  /* ---- bandeaux serrés sur leur plus longue ligne (text-wrap: balance ne réduit pas la boîte) ---- */
  function serrerBandeaux(page) {
    page.querySelectorAll(".bandeau").forEach(b => {
      b.style.transform = "none";
      const r = document.createRange(); r.selectNodeContents(b);
      const rects = [...r.getClientRects()].filter(q => q.width > 1);
      if (rects.length > 1 || b.scrollWidth > b.clientWidth) {
        const gauche = Math.min(...rects.map(q => q.left)), droite = Math.max(...rects.map(q => q.right));
        const cs = getComputedStyle(b);
        const largeur = Math.ceil(droite - gauche + parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight) + 3);
        if (largeur < b.offsetWidth) b.style.width = largeur + "px";
      }
      b.style.transform = "";
    });
  }


  /* ---- feutre (pointe en (x, y), corps vers la droite puis rotation) ---- */
  function feutre(rc, svg, o, page) {
    const { x, y } = o, L = o.longueur || 300, e = o.epaisseur || 46, g = document.createElementNS(NS, "g");
    const base = { roughness: 0.9, bowing: 0.6, seed: o.graine || 81 };
    g.appendChild(rc.polygon([[x, y - e * 0.12], [x + 30, y - e * 0.36], [x + 30, y + e * 0.36], [x, y + e * 0.12]],
      { ...base, stroke: ENCRE, strokeWidth: 3, fill: ENCRE, fillStyle: "solid" }));
    g.appendChild(rc.rectangle(x + 30, y - e / 2, L, e, { ...base, stroke: ENCRE, strokeWidth: 4, fill: "#FBF5EF", fillStyle: "solid", seed: base.seed + 1 }));
    g.appendChild(rc.rectangle(x + 30 + L * 0.58, y - e / 2 - 5, L * 0.44, e + 10,
      { ...base, stroke: ENCRE, strokeWidth: 4, fill: couleur(page, o.c || "encre"), fillStyle: "solid", seed: base.seed + 2 }));
    g.appendChild(rc.line(x + 30 + L * 0.1, y, x + 30 + L * 0.45, y, { ...base, stroke: "#9A95A8", strokeWidth: 3, seed: base.seed + 3 }));
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x} ${y})`);
    svg.appendChild(g);
  }

  /* ---- porte-bloc (bon de commande) ---- */
  function presse(rc, svg, o, page) {
    const { x, y } = o, w = o.w || 170, h = o.h || 220, g = document.createElementNS(NS, "g");
    const opt = { stroke: ENCRE, strokeWidth: 4.5, roughness: 1, bowing: 0.8, seed: o.graine || 91 };
    if (o.vide) {  // devis absent : contour en pointillés
      g.appendChild(rc.rectangle(x, y, w, h, { ...opt, stroke: "#9A95A8", strokeLineDash: [12, 10] }));
      if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
      svg.appendChild(g);
      return;
    }
    g.appendChild(rc.rectangle(x, y, w, h, { ...opt, fill: "#FFFFFF", fillStyle: "solid" }));
    g.appendChild(rc.rectangle(x + w * 0.32, y - 16, w * 0.36, 32, { ...opt, fill: ENCRE, fillStyle: "solid", seed: opt.seed + 1 }));
    for (let i = 0; i < 5; i++) {
      const yy = y + 48 + i * (h - 70) / 5, fin = x + w * (i === 4 ? 0.5 : 0.84);
      g.appendChild(rc.line(x + w * 0.16, yy, fin, yy, { ...opt, strokeWidth: 3, stroke: "#8E88A3", seed: opt.seed + 2 + i }));
    }
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
    svg.appendChild(g);
  }

  /* ---- étui à lunettes (remise de l'équipement) ---- */
  function etui(rc, svg, o, page) {
    const { x, y } = o, w = o.w || 230, h = o.h || 96, r = h / 2, g = document.createElementNS(NS, "g");
    const opt = { stroke: ENCRE, strokeWidth: 4.5, roughness: 1, bowing: 0.8, seed: o.graine || 101 };
    const d = `M ${x + r} ${y} L ${x + w - r} ${y} A ${r} ${r} 0 0 1 ${x + w - r} ${y + h} L ${x + r} ${y + h} A ${r} ${r} 0 0 1 ${x + r} ${y} Z`;
    g.appendChild(rc.path(d, { ...opt, fill: couleur(page, o.c || "accent"), fillStyle: "solid" }));
    g.appendChild(rc.line(x + r * 0.6, y + h * 0.5, x + w - r * 0.6, y + h * 0.5, { ...opt, stroke: "#FBF5EF", strokeWidth: 3, seed: opt.seed + 1 }));
    lunettesTrait(rc, g, x + w / 2, y - h * 0.62, h * 0.36, { ...opt, seed: opt.seed + 5 }, false);
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
    svg.appendChild(g);
  }

  /* ---- coche ---- */
  function coche(rc, svg, o, page) {
    const { x, y } = o, t = o.taille || 40;
    svg.appendChild(rc.linearPath([[x, y], [x + t * 0.35, y + t * 0.38], [x + t, y - t * 0.55]],
      { stroke: couleur(page, o.c || "accent"), strokeWidth: o.ep || 6, roughness: 1.1, bowing: 1, seed: o.graine || 111 }));
  }

  /* ---- case vide en pointillés (la vente oubliée) ---- */
  function manque(rc, svg, o, page) {
    const { x, y } = o, h = o.h || 90;
    svg.appendChild(rc.line(x, y, x, y + h, { stroke: couleur(page, o.c || "accent"), strokeWidth: o.ep || 5, roughness: 0.8,
      strokeLineDash: [9, 9], seed: o.graine || 121 }));
  }


  /* ---- croix (refus) ---- */
  function croix(rc, svg, o, page) {
    const { x, y } = o, t = o.taille || 60, opt = { stroke: couleur(page, o.c || "accent"), strokeWidth: o.ep || 7, roughness: 1.2, bowing: 1 };
    svg.appendChild(rc.line(x - t, y - t, x + t, y + t, { ...opt, seed: (o.graine || 131) }));
    svg.appendChild(rc.line(x - t, y + t, x + t, y - t, { ...opt, seed: (o.graine || 131) + 1 }));
  }

  /* ---- montée en marches (la prime qui monte) ---- */
  function montee(rc, svg, o, page) {
    const { x, y } = o, w = o.w || 160, h = o.h || 110, n = o.marches || 4, g = document.createElementNS(NS, "g");
    const opt = { stroke: couleur(page, o.c || "accent"), strokeWidth: o.ep || 6, roughness: 1, bowing: 0.8, seed: o.graine || 151 };
    const pts = [[x, y + h]];
    for (let i = 0; i < n; i++) {
      const px = x + (w * (i + 1)) / n, py = y + h - (h * (i + 1)) / n;
      pts.push([px - w / n, py], [px, py]);
    }
    g.appendChild(rc.linearPath(pts, opt));
    const [ex, ey] = pts[pts.length - 1];
    g.appendChild(rc.line(ex, ey, ex - 20, ey - 14, { ...opt, seed: opt.seed + 1 }));
    g.appendChild(rc.line(ex, ey, ex - 20, ey + 14, { ...opt, seed: opt.seed + 2 }));
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${x + w / 2} ${y + h / 2})`);
    svg.appendChild(g);
  }

  function infini(rc, svg, o, page) {
    const { x, y, w } = o, h = o.h || w * 0.42, cx = x + w / 2, cy = y + h / 2, pts = [];
    for (let t = 0; t <= Math.PI * 2 + 0.3; t += 0.12) {
      const d = 1 + Math.sin(t) ** 2;
      pts.push([cx + (w / 2) * Math.cos(t) / d, cy + h * 1.1 * Math.sin(t) * Math.cos(t) / d]);
    }
    const g = document.createElementNS(NS, "g");
    g.appendChild(rc.curve(pts, { stroke: couleur(page, o.c), strokeWidth: o.ep || 9, roughness: 1.1, bowing: 1, seed: o.graine || 77 }));
    g.appendChild(rc.curve(pts.map(([a, b]) => [a + 3, b + 2]), { stroke: couleur(page, o.c), strokeWidth: (o.ep || 9) * 0.45, roughness: 1.4, bowing: 1, seed: (o.graine || 77) + 1 }));
    if (o.rot) g.setAttribute("transform", `rotate(${o.rot} ${cx} ${cy})`);
    svg.appendChild(g);
  }

  const PRIMITIVES = { fleche, gribouillis, ellipse, bulle, batons, tableau, icone, ecriture, infini, feutre, presse, etui, coche, manque, croix, montee };

  async function dessiner() {
    await document.fonts.ready;
    document.querySelectorAll(".page").forEach(page => {
      serrerBandeaux(page);
      soulignes(page);
      const plan = page.querySelector("script.plan");
      if (!plan) return;
      const svg = page.querySelector("svg.dessins");
      const rc = rough.svg(svg);
      JSON.parse(plan.textContent).forEach(cmd => {
        const g = document.createElementNS(NS, "g");
        g.setAttribute("data-t", cmd.t);
        svg.appendChild(g);
        PRIMITIVES[cmd.t](rc, g, cmd, page);
      });
    });
    document.body.dataset.pret = "1";
  }
  window.addEventListener("load", dessiner);
})();
