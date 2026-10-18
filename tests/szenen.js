/*
 * Künstliche Testbilder für die Geld-Erkennung (ohne echte Fotos, ohne Personen).
 * Zeichnet ein Blatt Papier mit Spielgeld: zweifarbige 1-€- und 2-€-Münzen,
 * 5-/10-/20-€-Scheine, schräge Perspektive, Schatten, Glanz, Farbstich, Unschärfe.
 *
 * szene(nr, optionen) -> { rgba, w, h, summe, beschreibung }
 */
(function (global) {
  'use strict';

  function zufallsquelle(seed) {
    let s = (seed * 2654435761) % 2147483647 || 1;
    return () => (s = (s * 16807) % 2147483647) / 2147483647;
  }

  const GOLD = [196, 156, 66], SILBER = [168, 170, 174];
  const SCHEIN = { 5: [150, 162, 150], 10: [205, 122, 116], 20: [118, 152, 206] };

  function szene(nr, o) {
    o = Object.assign({ w: 800, h: 600, muenzen: 6, scheine: [], beruehren: false, aufSchein: false,
      kanal: [1, 1, 1], verlauf: 0, schattenkante: 0, glanz: 0, unschaerfe: 0, rauschen: 6, dunkel: 1,
      ohnePapier: false, perspektive: null, groesse: null, scheineUeberlappen: false,
      nah: false, tischkante: 0, tisch: [132, 118, 100], linien: true, kopfzeile: false, preisschild: false }, o);
    const R = zufallsquelle(nr + 1), w = o.w, h = o.h;
    const rgba = new Float32Array(w * h * 4);
    const persp = o.perspektive || (0.68 + R() * 0.3);       // b/a der Münzen
    const a1 = o.groesse || (20 + R() * 10);                  // Halbachse 1 €
    // Tisch und Papier
    const rand = o.ohnePapier ? 0 : o.nah ? -1 : 0.06;          // nah: Blatt füllt das ganze Bild
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4, aufPapier = !o.ohnePapier && x > w * Math.max(rand, o.tischkante) && x < w * (1 - rand) && y > h * rand && y < h * (1 - rand);
      const c = aufPapier ? [240, 240, 236] : o.tisch;
      for (let k = 0; k < 3; k++) rgba[i + k] = c[k];
    }
    // Linien der Unterlage
    if (!o.ohnePapier && o.linien) for (let x = Math.round(w * 0.1); x < w * 0.9; x++) for (const y of [Math.round(h * 0.16), Math.round(h * 0.85)]) {
      const i = (y * w + x) * 4; rgba[i] = rgba[i + 1] = rgba[i + 2] = 40;
    }

    const plaetze = [];
    // Kopfzeile der Unterlage: gedruckte (flache) gelbe Münz-Bildchen und ein kleines Schein-Bildchen
    if (o.kopfzeile) {
      const r0 = a1 * 0.45, y0 = h * 0.08;
      for (const [k, cx] of [0.08, 0.13, 0.85, 0.9].entries()) {
        for (let y = Math.floor(y0 - r0); y <= y0 + r0; y++) for (let x = Math.floor(w * cx - r0); x <= w * cx + r0; x++) {
          const d = Math.hypot(x - w * cx, y - y0) / r0; if (d > 1) continue;
          const i = (y * w + x) * 4, c = d > 0.88 ? [60, 50, 20] : [236, 200, 70];
          for (let q = 0; q < 3; q++) rgba[i + q] = c[q];
        }
      }
      for (let y = Math.round(y0 - r0); y < y0 + r0; y++) for (let x = Math.round(w * 0.16); x < w * 0.16 + r0 * 3; x++) {
        const i = (y * w + x) * 4; rgba[i] = 170; rgba[i + 1] = 190; rgba[i + 2] = 215;
      }
      plaetze.push({ x: w * 0.12, y: y0, r: r0 * 4 }, { x: w * 0.87, y: y0, r: r0 * 3 });
    }
    // Preisschild: hellgrüne Karte mit schwarzem Rahmen und großer Zahl
    if (o.preisschild) {
      const pw = w * 0.32, ph = h * 0.16, px = w * 0.34, py = h * 0.78;
      for (let y = Math.round(py); y < py + ph; y++) for (let x = Math.round(px); x < px + pw; x++) {
        const rnd = x - px < 4 || px + pw - x < 4 || y - py < 4 || py + ph - y < 4;
        const ziffer = x > px + pw * 0.4 && x < px + pw * 0.48 && y > py + ph * 0.35 && y < py + ph * 0.85;
        const i = (y * w + x) * 4, c = rnd || ziffer ? [25, 25, 25] : [214, 236, 196];
        for (let q = 0; q < 3; q++) rgba[i + q] = c[q];
      }
      plaetze.push({ x: px + pw / 2, y: py + ph / 2, r: Math.max(pw, ph) / 2 });
    }
    function frei(x, y, r) { return plaetze.every(p => Math.hypot(p.x - x, p.y - y) > p.r + r + 6); }
    let summe = 0;
    const scheinFlaechen = [];
    // Scheine
    for (const wert of o.scheine) {
      const sw = a1 * 2 * 5.2, sh = sw * 0.52 * persp;  // Spielgeld 120 x 62 mm, Münze 23 mm
      let x, y, t = 0;
      const ueberlappt = (x, y) => scheinFlaechen.some(f => x < f.x + f.sw + 12 && x + sw + 12 > f.x && y < f.y + f.sh + 12 && y + sh + 12 > f.y);
      if (o.scheineUeberlappen && scheinFlaechen.length) { const f = scheinFlaechen[0]; x = f.x + f.sw * 0.4; y = f.y + f.sh * 0.15; }
      else do { x = w * 0.08 + R() * (w * 0.84 - sw); y = h * 0.18 + R() * (h * 0.64 - sh); t++; } while (ueberlappt(x, y) && t < 400);
      plaetze.push({ x: x + sw / 2, y: y + sh / 2, r: Math.max(sw, sh) / 2 });
      scheinFlaechen.push({ x, y, sw, sh });
      const c = SCHEIN[wert];
      for (let yy = Math.round(y); yy < y + sh; yy++) for (let xx = Math.round(x); xx < x + sw; xx++) {
        const i = (yy * w + xx) * 4, u = (xx - x) / sw, v = (yy - y) / sh;
        let f = 0.9 + 0.12 * Math.sin(u * 40 + v * 9) * Math.sin(v * 25);
        if (u > 0.78 && u < 0.95 && v > 0.2 && v < 0.8) f = 1.25;               // helles Fenster
        if (u > 0.08 && u < 0.3 && v > 0.45 && v < 0.85) f = 0.7;               // Ziffer
        for (let k = 0; k < 3; k++) rgba[i + k] = Math.min(250, c[k] * f);
      }
      summe += wert;
    }
    // Münzen
    const liste = [];
    for (let m = 0; m < o.muenzen; m++) {
      const wert = R() < 0.5 ? 1 : 2, a = wert === 2 ? a1 * 1.11 : a1, b = a * persp;
      let x, y, t = 0;
      if (o.aufSchein && m === 0 && scheinFlaechen.length) {
        const s = scheinFlaechen[0]; x = s.x + s.sw * 0.45; y = s.y + s.sh * 0.5;
      } else if (o.beruehren && m === 1 && liste.length) {
        x = liste[0].x + liste[0].a + a - 1; y = liste[0].y;
      } else {
        const x0 = Math.max(w * 0.12, w * o.tischkante + a + 10), y0 = o.nah ? b + 10 : h * 0.22;
        const bx = Math.max(10, (o.nah ? w - a - 10 : w * 0.88) - x0), by = Math.max(10, (o.nah ? h - b - 10 : h * 0.8) - y0);
        do { x = x0 + R() * bx; y = y0 + R() * by; t++; } while (!frei(x, y, a) && t < 400);
      }
      plaetze.push({ x, y, r: a }); liste.push({ x, y, a, b, wert }); summe += wert;
    }
    for (const c of liste) zeichneMuenze(rgba, w, h, c, R);
    // Licht
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      let f = o.dunkel;
      if (o.verlauf) f *= 1 - o.verlauf * (x / w + y / h) / 2;
      if (o.schattenkante && x / w + 0.3 * y / h < 0.5) f *= 1 - o.schattenkante;
      for (let k = 0; k < 3; k++) rgba[i + k] *= f * o.kanal[k];
    }
    if (o.glanz) for (const c of liste) if (R() < o.glanz) {
      const gx = c.x + (R() - 0.5) * c.a, gy = c.y + (R() - 0.5) * c.b, r = c.b * (0.25 + R() * 0.3);
      for (let y = Math.floor(gy - r); y <= gy + r; y++) for (let x = Math.floor(gx - r * 1.5); x <= gx + r * 1.5; x++) {
        if (x < 0 || y < 0 || x >= w || y >= h) continue;
        const d = Math.hypot((x - gx) / 1.5, y - gy) / r; if (d > 1) continue;
        const al = 0.8 * (1 - d * d), i = (y * w + x) * 4;
        for (let k = 0; k < 3; k++) rgba[i + k] += (255 - rgba[i + k]) * al;
      }
    }
    let bild = rgba;
    if (o.unschaerfe) bild = weichzeichnen(rgba, w, h, o.unschaerfe);
    const out = new Uint8ClampedArray(w * h * 4);
    for (let i = 0; i < w * h * 4; i += 4) {
      const n = (R() - 0.5) * o.rauschen * 2;
      out[i] = bild[i] + n; out[i + 1] = bild[i + 1] + n; out[i + 2] = bild[i + 2] + n; out[i + 3] = 255;
    }
    return { rgba: out, w, h, summe, muenzen: liste };
  }

  function zeichneMuenze(rgba, w, h, c, R) {
    const grenze = c.wert === 2 ? 0.73 : 0.70;
    const innen = c.wert === 2 ? GOLD : SILBER, ring = c.wert === 2 ? SILBER : GOLD;
    // Schatten
    for (let y = Math.floor(c.y - c.b - 8); y <= c.y + c.b + 8; y++) for (let x = Math.floor(c.x - c.a - 8); x <= c.x + c.a + 8; x++) {
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const u = (x - c.x - 4) / c.a, v = (y - c.y - 5) / c.b; if (u * u + v * v > 1) continue;
      const i = (y * w + x) * 4; for (let k = 0; k < 3; k++) rgba[i + k] *= 0.72;
    }
    const phase = R() * 6;
    for (let y = Math.floor(c.y - c.b); y <= c.y + c.b; y++) for (let x = Math.floor(c.x - c.a); x <= c.x + c.a; x++) {
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const u = (x - c.x) / c.a, v = (y - c.y) / c.b, rho = Math.sqrt(u * u + v * v);
      if (rho > 1) continue;
      const farbe = rho < grenze ? innen : ring;
      let f = 0.82 + 0.25 * (1 - rho) + 0.08 * Math.sin(u * 14 + phase) * Math.cos(v * 11);   // Prägung, Wölbung
      if (rho > 0.95 || Math.abs(rho - grenze) < 0.025) f *= 0.55;                            // Kanten
      const i = (y * w + x) * 4;
      for (let k = 0; k < 3; k++) rgba[i + k] = farbe[k] * f;
    }
  }

  function weichzeichnen(rgba, w, h, r) {
    let a = rgba;
    for (const zeilen of [true, false]) {
      const b = new Float32Array(a.length);
      for (let j = 0; j < (zeilen ? h : w); j++) for (let i = 0; i < (zeilen ? w : h); i++) {
        let s0 = 0, s1 = 0, s2 = 0, z = 0;
        for (let d = -r; d <= r; d++) {
          const q = i + d; if (q < 0 || q >= (zeilen ? w : h)) continue;
          const p = (zeilen ? j * w + q : q * w + j) * 4; s0 += a[p]; s1 += a[p + 1]; s2 += a[p + 2]; z++;
        }
        const p = (zeilen ? j * w + i : i * w + j) * 4; b[p] = s0 / z; b[p + 1] = s1 / z; b[p + 2] = s2 / z; b[p + 3] = 255;
      }
      a = b;
    }
    return a;
  }

  global.KirmesSzenen = { szene };
})(typeof globalThis !== 'undefined' ? globalThis : this);
