/*
 * Geld-Erkennung für den Kirmes-Kiosk
 * -----------------------------------
 * Erkennt auf einem Foto (Geld auf hellem Papier) Euro-Münzen und -Scheine
 * ohne Server und ohne KI-Dienst – alles läuft im Browser.
 *
 * Idee:
 *  1. Alles, was sich deutlich vom hellen Papier abhebt, ist "Vordergrund".
 *  2. Zusammenhängende Flächen werden einzeln vermessen (Größe, Form, Farbe).
 *     Sich berührende Münzen werden vorher getrennt.
 *  3. Runde/ovale Flächen = Münzen. 1 € und 2 € unterscheiden sich daran,
 *     ob die Mitte silbern und der Ring golden ist (1 €) oder umgekehrt (2 €).
 *     Einfarbig goldene Münzen sind Cent-Münzen (zählen 0 €).
 *  4. Große rechteckige Flächen = Scheine, die Farbe entscheidet:
 *     5 € grau-grün, 10 € rot, 20 € blau, 50 € orange.
 *  Vorher: Weißabgleich über das Papier (gleicht Farbstich und Schatten aus).
 *  Farben werden als Median gemessen, Glanzlichter zählen nicht mit.
 *  Was golden schimmert, aber keiner Münze sicher zugeordnet werden kann,
 *  kommt als art:'unklar' zurück; dann ist `unsicher` true.
 *
 * Schnittstelle:  KirmesErkennung.erkenne(rgba, breite, hoehe, optionen)
 *   rgba: Uint8ClampedArray (4 Byte pro Pixel), z. B. aus canvas.getImageData
 *   Rückgabe: { objekte: [{art:'muenze'|'schein'|'unklar', wert, x, y, a, b, winkel, sicher}], summe, unsicher }
 */
(function (global) {
  'use strict';
  let MIN_GOLD = 0.09;
  let RING = { innen: 0.45, von: 0.75, bis: 0.93 };

  function erkenne(rgba, w, h, opt) {
    opt = opt || {};
    MIN_GOLD = opt.minGold || 0.09;
    if (opt.ring) RING = opt.ring;
    const n = w * h, minDim = Math.min(w, h);
    // Weißabgleich über das Papier: gleicht Farbstich (Glühbirne, Neonröhre)
    // und Schatten aus, bevor irgendetwas gemessen wird.
    if (opt.weissabgleich !== false) rgba = weissabgleich(rgba, w, h);
    const L = new Float32Array(n), S = new Float32Array(n);
    for (let i = 0, p = 0; i < n; i++, p += 4) {
      const r = rgba[p], g = rgba[p + 1], b = rgba[p + 2];
      const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
      L[i] = 0.299 * r + 0.587 * g + 0.114 * b;
      S[i] = mx > 0 ? (mx - mn) / mx : 0;
    }

    // --- 1. Papierhelligkeit lokal schätzen (robust gegen Schatten) --------
    const kachel = Math.max(16, Math.round(minDim / 8));
    const kx = Math.ceil(w / kachel), ky = Math.ceil(h / kachel);
    const kHell = new Float32Array(kx * ky);
    for (let ty = 0; ty < ky; ty++) for (let tx = 0; tx < kx; tx++) {
      const werte = [];
      for (let y = ty * kachel; y < Math.min(h, (ty + 1) * kachel); y += 2)
        for (let x = tx * kachel; x < Math.min(w, (tx + 1) * kachel); x += 2) werte.push(L[y * w + x]);
      werte.sort((a, b) => a - b);
      kHell[ty * kx + tx] = werte[Math.floor(werte.length * 0.85)] || 255;
    }
    function papier(x, y) {
      const fx = Math.min(kx - 1, Math.max(0, x / kachel - 0.5)), fy = Math.min(ky - 1, Math.max(0, y / kachel - 0.5));
      const x0 = Math.floor(fx), y0 = Math.floor(fy), x1 = Math.min(kx - 1, x0 + 1), y1 = Math.min(ky - 1, y0 + 1);
      const ax = fx - x0, ay = fy - y0;
      return (kHell[y0 * kx + x0] * (1 - ax) + kHell[y0 * kx + x1] * ax) * (1 - ay) +
             (kHell[y1 * kx + x0] * (1 - ax) + kHell[y1 * kx + x1] * ax) * ay;
    }

    // --- 2. Vordergrund-Maske ------------------------------------------------
    const dunkel = opt.dunkel || 0.80, satGrenze = opt.saettigung || 0.28;
    let fg = new Uint8Array(n);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x, P = papier(x, y);
      if (L[i] < P * dunkel || (S[i] > satGrenze && L[i] < P * 0.98)) fg[i] = 1;
    }
    const roh = fg.slice();
    // Dünne Linien (Rahmen der Unterlage, Schrift) entfernen, Löcher füllen.
    fg = oeffneScheibe(fg, w, h, Math.max(1, Math.round(minDim / 260)));
    fuelleLoecher(fg, w, h, n * 0.03);

    // --- 3. Typische Münzgröße aus einem ersten Durchgang ------------------
    const probe = vermesse(fg, roh, w, h).filter(istMuenzform).filter(o => muenzFarbe(rgba, w, h, o));
    const medB = probe.length ? median(probe.map(o => o.b)) : minDim * 0.035;
    const medN = probe.length ? median(probe.map(o => o.n)) : Math.PI * Math.pow(minDim * 0.04, 2);

    // --- 4. Scheine: empfindlichere Maske, Textur zusammenziehen, Münzen wegöffnen
    const objekte = [];
    let fgS = new Uint8Array(n);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x, P = papier(x, y);
      if (L[i] < P * (opt.sHell || 0.87) || (S[i] > 0.2 && L[i] < P * 0.98)) fgS[i] = 1;
    }
    const rZu = Math.max(2, Math.round(medB * (opt.sZu || 0.25)));
    fgS = erodiere(dilatiere(fgS, w, h, rZu), w, h, rZu);
    fuelleLoecher(fgS, w, h, n * 0.05);
    fgS = oeffneScheibe(fgS, w, h, Math.round(medB * (opt.sAuf || 1.2)));
    const scheinMaske = new Uint8Array(n);
    const sk = vermesse(fgS, roh, w, h);
    for (const o of sk) {
      o.rahmen = rahmenAnteil(sk.lab, o, L, papier, w, h);
      if (o.n < Math.max(medN * 3, n * 0.012) || o.n > n * 0.5) continue;
      if (o.rechteckig < 0.65 || o.seiten < 1.2 || o.seiten > 4) continue;
      if (o.dichte < 0.33) continue;  // fast nur helles Papier (z. B. Preisschild)
      if (o.rahmen > 0.2) continue;   // schwarzer Rand: Preisschild, kein Geldschein
      const f = scheinFarbe(rgba, roh, w, h, sk.lab, o);
      if (!f) continue;
      objekte.push(Object.assign({ art: 'schein' }, lage(o), f));
      for (let i = 0; i < n; i++) if (sk.lab[i] === o.k) scheinMaske[i] = 1;
    }
    const scheinRand = dilatiere(scheinMaske, w, h, 2);
    for (let i = 0; i < n; i++) if (scheinRand[i]) fg[i] = 0;

    // --- 5. Münzen: Berührungen trennen, verschmolzene Flächen aufteilen ----
    const fg2 = oeffneScheibe(fg, w, h, Math.max(2, Math.round(medB * 0.5)));
    const kand = vermesse(fg2, roh, w, h);
    let muenzen = kand.filter(istMuenzform);
    if (muenzen.length) {
      const med = median(muenzen.map(o => o.a));
      muenzen = muenzen.filter(o => o.a > med * 0.6 && o.a < med * 1.6);
    }
    const geteilt = [], erledigt = new Set(muenzen);
    for (const o of kand) {
      if (muenzen.indexOf(o) >= 0 || o.rand) continue;
      if ((o.n < medN * 1.2 && o.seiten < 2.2) || o.n > medN * 7 || o.dichte < 0.8) continue;
      const teil = teile(fg2, kand.lab, o, w, h, medB, muenzen);
      if (teil.length) erledigt.add(o);
      for (const t of teil) geteilt.push(t);
    }
    for (const m of muenzen.concat(geteilt)) {
      const f = muenzFarbe(rgba, w, h, m);
      if (f) objekte.push(Object.assign({ art: 'muenze' }, lage(m), f, m.geteilt ? { geteilt: true } : {}));
      else if (!m.geteilt && goldAnteil(rgba, kand.lab, m, w, h) > 0.12) objekte.push(Object.assign({ art: 'unklar', wert: null }, lage(m)));
    }
    klaereUnsichere(objekte);

    // Unklare Stellen: Flächen in Münzgröße oder größer, die golden schimmern, aber
    // keiner Münze sicher zugeordnet werden konnten (verschmolzen, starker Glanz …).
    for (const o of kand) {
      if (erledigt.has(o) || o.rand || o.n < medN * 0.5 || o.n > medN * 10) continue;
      if (objekte.some(m => Math.hypot(m.x - o.x, m.y - o.y) < Math.max(m.a, o.b))) continue;
      if (goldAnteil(rgba, kand.lab, o, w, h) > 0.12) objekte.push(Object.assign({ art: 'unklar', wert: null }, lage(o)));
    }

    const summe = objekte.reduce((s, o) => s + (o.wert || 0), 0);
    const unsicher = objekte.some(o => o.art === 'unklar' || o.sicher === false);
    const erg = { objekte, summe, unsicher };
    if (opt.debug) erg.debug = { kandidaten: kand, maske: fg2, scheine: fgS, scheinKand: sk, geteilt, medB };
    return erg;
  }

  // Anteil deutlich goldener Pixel in einer Fläche.
  function goldAnteil(rgba, lab, o, w, h) {
    const R = Math.ceil(o.a * 1.2); let z = 0, g = 0;
    for (let y = Math.max(0, Math.round(o.y - R)); y < Math.min(h, o.y + R); y++)
      for (let x = Math.max(0, Math.round(o.x - R)); x < Math.min(w, o.x + R); x++) {
        if (o.k !== undefined && lab[y * w + x] !== o.k) continue;
        if (o.k === undefined && Math.hypot(x - o.x, y - o.y) > o.b) continue;
        const p = (y * w + x) * 4; z++;
        if (gold(rgba[p], rgba[p + 1], rgba[p + 2]) > 0.18) g++;
      }
    return z ? g / z : 0;
  }

  // Anteil sehr dunkler Pixel im Saum einer Fläche (±3 px um ihren Rand).
  // Preisschilder haben einen schwarzen Rahmen, Geldscheine nicht.
  function rahmenAnteil(lab, o, L, papier, w, h) {
    const R = Math.ceil(o.a * 1.5) + 4, d = 3;
    const x0 = Math.max(0, Math.floor(o.x - R)), x1 = Math.min(w - 1, Math.ceil(o.x + R));
    const y0 = Math.max(0, Math.floor(o.y - R)), y1 = Math.min(h - 1, Math.ceil(o.y + R));
    const bw = x1 - x0 + 1, bh = y1 - y0 + 1, m = new Uint8Array(bw * bh);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) m[(y - y0) * bw + (x - x0)] = lab[y * w + x] === o.k ? 1 : 0;
    const innen = erodiere(m, bw, bh, d), aussen = dilatiere(m, bw, bh, d);
    let z = 0, dunkel = 0;
    for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) {
      const i = y * bw + x; if (!aussen[i] || innen[i]) continue;
      z++; if (L[(y + y0) * w + x + x0] < papier(x + x0, y + y0) * 0.55) dunkel++;
    }
    return z ? dunkel / z : 0;
  }

  // Eine Fläche aus mehreren verschmolzenen Münzen anhand der "dicksten Stellen"
  // (Maxima der Abstandstransformation) in einzelne Münzen zerlegen.
  function teile(fg, lab, o, w, h, medB, muenzen) {
    const R = Math.ceil(o.a * 1.6);
    const x0 = Math.max(0, Math.floor(o.x - R)), x1 = Math.min(w - 1, Math.ceil(o.x + R));
    const y0 = Math.max(0, Math.floor(o.y - R)), y1 = Math.min(h - 1, Math.ceil(o.y + R));
    const bw = x1 - x0 + 1, bh = y1 - y0 + 1, m = new Uint8Array(bw * bh);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) m[(y - y0) * bw + (x - x0)] = lab[y * w + x] === o.k ? 1 : 0;
    const D = abstand(m, bw, bh);
    const spitzen = [], rad = Math.max(2, Math.round(medB * 0.8));
    for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) {
      const d = D[y * bw + x]; if (d < medB * 0.6) continue;
      let max = true;
      for (let dy = -rad; dy <= rad && max; dy++) for (let dx = -rad; dx <= rad; dx++) {
        const xx = x + dx, yy = y + dy;
        if (xx < 0 || yy < 0 || xx >= bw || yy >= bh) continue;
        if (D[yy * bw + xx] > d) { max = false; break; }
      }
      if (max) spitzen.push({ x: x + x0, y: y + y0, d });
    }
    spitzen.sort((p, q) => q.d - p.d);
    const gewaehlt = [];
    for (const p of spitzen) if (gewaehlt.every(q => Math.hypot(p.x - q.x, p.y - q.y) > medB * 1.4)) gewaehlt.push(p);
    if (gewaehlt.length < 2) return [];
    // Jedes Pixel der Fläche der nächstgelegenen Spitze zuordnen und jeden Teil
    // einzeln als Ellipse vermessen.
    const teileSt = gewaehlt.map(() => ({ n: 0, sx: 0, sy: 0, sxx: 0, syy: 0, sxy: 0 }));
    for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) {
      if (!m[y * bw + x]) continue;
      const gx = x + x0, gy = y + y0;
      let best = 0, bd = 1e9;
      gewaehlt.forEach((p, i) => { const d = (p.x - gx) * (p.x - gx) + (p.y - gy) * (p.y - gy); if (d < bd) { bd = d; best = i; } });
      const s = teileSt[best]; s.n++; s.sx += gx; s.sy += gy; s.sxx += gx * gx; s.syy += gy * gy; s.sxy += gx * gy;
    }
    return teileSt.filter(s => s.n > 10).map(s => Object.assign(ellipse(s), { n: s.n, geteilt: true }));
  }

  function ellipse(s) {
    const mx = s.sx / s.n, my = s.sy / s.n;
    const cxx = s.sxx / s.n - mx * mx, cyy = s.syy / s.n - my * my, cxy = s.sxy / s.n - mx * my;
    const tr = cxx + cyy, det = cxx * cyy - cxy * cxy, d = Math.sqrt(Math.max(0, tr * tr / 4 - det));
    return { x: mx, y: my, a: 2 * Math.sqrt(tr / 2 + d), b: 2 * Math.sqrt(Math.max(1e-6, tr / 2 - d)),
             winkel: 0.5 * Math.atan2(2 * cxy, cxx - cyy) };
  }

  function istMuenzform(o) {
    return !o.rand && o.n >= o.minFlaeche && o.seiten < 2.6 && o.rechteckig > 0.66 && o.rechteckig < 0.875 &&
           o.fuell > 0.86 && o.dichte > 0.8;
  }

  function lage(o) { return { x: o.x, y: o.y, a: o.a, b: o.b, winkel: o.winkel }; }

  // Vermisst alle Flächen einer Maske: Schwerpunkt, Ellipse, Rechteckigkeit …
  function vermesse(fg, roh, w, h) {
    const { lab, anzahl } = beschrifte(fg, w, h);
    const st = [];
    for (let k = 0; k <= anzahl; k++) st.push({ n: 0, sx: 0, sy: 0, sxx: 0, syy: 0, sxy: 0, roh: 0, x0: w, y0: h, x1: 0, y1: 0, rand: false });
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const k = lab[y * w + x]; if (!k) continue;
      const s = st[k];
      s.n++; s.sx += x; s.sy += y; s.sxx += x * x; s.syy += y * y; s.sxy += x * y; s.roh += roh[y * w + x];
      if (x < s.x0) s.x0 = x; if (x > s.x1) s.x1 = x; if (y < s.y0) s.y0 = y; if (y > s.y1) s.y1 = y;
      if (x === 0 || y === 0 || x === w - 1 || y === h - 1) s.rand = true;
    }
    const minFlaeche = Math.PI * Math.pow(Math.min(w, h) * 0.022, 2);
    const liste = [];
    for (let k = 1; k <= anzahl; k++) {
      const s = st[k];
      if (s.n < minFlaeche * 0.5) continue;
      const mx = s.sx / s.n, my = s.sy / s.n;
      const cxx = s.sxx / s.n - mx * mx, cyy = s.syy / s.n - my * my, cxy = s.sxy / s.n - mx * my;
      const tr = cxx + cyy, det = cxx * cyy - cxy * cxy, d = Math.sqrt(Math.max(0, tr * tr / 4 - det));
      const l1 = tr / 2 + d, l2 = Math.max(1e-6, tr / 2 - d);
      const winkel = 0.5 * Math.atan2(2 * cxy, cxx - cyy);
      const a = 2 * Math.sqrt(l1), b = 2 * Math.sqrt(l2);
      const c = Math.cos(winkel), si = Math.sin(winkel);
      let u0 = 1e9, u1 = -1e9, v0 = 1e9, v1 = -1e9;
      for (let y = s.y0; y <= s.y1; y++) for (let x = s.x0; x <= s.x1; x++) {
        if (lab[y * w + x] !== k) continue;
        const u = (x - mx) * c + (y - my) * si, v = -(x - mx) * si + (y - my) * c;
        if (u < u0) u0 = u; if (u > u1) u1 = u; if (v < v0) v0 = v; if (v > v1) v1 = v;
      }
      liste.push({ k, n: s.n, x: mx, y: my, a, b, winkel, seiten: a / b,
        rechteckig: s.n / ((u1 - u0 + 1) * (v1 - v0 + 1)), fuell: s.n / (Math.PI * a * b),
        dichte: s.roh / s.n, rand: s.rand, minFlaeche });
    }
    liste.lab = lab;
    return liste;
  }

  // Goldton eines Pixels: Gold hat deutlich mehr Rot/Grün als Blau.
  function gold(r, g, b) { return ((r + g) / 2 - b) / (Math.max(r, g, b) + 20); }

  function muenzFarbe(rgba, w, h, m) {
    const c = Math.cos(m.winkel), s = Math.sin(m.winkel);
    const innen = [], ring = [];
    const R = Math.ceil(m.a);
    for (let dy = -R; dy <= R; dy++) for (let dx = -R; dx <= R; dx++) {
      const x = Math.round(m.x + dx), y = Math.round(m.y + dy);
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const u = (dx * c + dy * s) / m.a, v = (-dx * s + dy * c) / m.b;
      const rho = Math.sqrt(u * u + v * v);
      const bereich = rho < RING.innen ? innen : (rho > RING.von && rho < RING.bis ? ring : null);
      if (!bereich) continue;
      const p = (y * w + x) * 4, r = rgba[p], g = rgba[p + 1], b = rgba[p + 2];
      const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
      // Glanzlichter (fast weiß) und tiefe Schatten verfälschen die Farbe: weglassen.
      if (mx > 228 && (mx - mn) / mx < 0.16) continue;
      if (mx < 28) continue;
      bereich.push(gold(r, g, b));
    }
    // Median statt Mittelwert: einzelne Ausreißer (Glanz, Prägung) zählen nicht.
    // Ist ein Bereich fast ganz von Glanz verdeckt, entscheidet der andere allein:
    // goldener Ring = 1 €, silberner Ring = 2 € (bei der Mitte umgekehrt).
    const genug = Math.max(6, (innen.length + ring.length) * 0.08);
    if (innen.length < genug && ring.length < genug) return null;
    if (innen.length < genug || ring.length < genug) {
      const nurRing = innen.length < genug, g = median(nurRing ? ring : innen);
      if (g > 0.2) return { wert: nurRing ? 1 : 2, sicher: true, goldInnen: nurRing ? null : +g.toFixed(3), goldRing: nurRing ? +g.toFixed(3) : null };
      if (g < 0.09) return { wert: nurRing ? 2 : 1, sicher: true, goldInnen: nurRing ? null : +g.toFixed(3), goldRing: nurRing ? +g.toFixed(3) : null };
      return null;
    }
    const gi = median(innen), ga = median(ring);
    if (Math.max(gi, ga) < MIN_GOLD) return null;       // nirgends golden: keine Münze (Schrift, Schatten …)
    const diff = gi - ga;                            // >0: Mitte goldener -> 2 €, <0: Ring goldener -> 1 €
    const grenze = 0.06;
    let wert, sicher = true;
    if (diff > grenze) wert = 2;
    else if (diff < -grenze) wert = 1;
    else if (Math.min(gi, ga) > 0.17) { wert = 0; sicher = false; } // ganz golden: Cent-Münze – oder Glanz; lieber nachfragen
    else { wert = diff >= 0 ? 2 : 1; sicher = false; }
    return { wert, sicher, goldInnen: +gi.toFixed(3), goldRing: +ga.toFixed(3) };
  }

  // Unklare Münzen über die Größe zuordnen: 2 € ist ca. 11 % größer als 1 €.
  function klaereUnsichere(objekte) {
    const s1 = objekte.filter(o => o.sicher && o.wert === 1).map(o => o.a);
    const s2 = objekte.filter(o => o.sicher && o.wert === 2).map(o => o.a);
    if (!s1.length && !s2.length) return;
    const m1 = s1.length ? median(s1) : median(s2) / 1.11;
    const m2 = s2.length ? median(s2) : median(s1) * 1.11;
    for (const o of objekte) if (o.art === 'muenze' && !o.sicher && o.wert !== 0) o.wert = Math.abs(o.a - m1) < Math.abs(o.a - m2) ? 1 : 2;
  }

  // Mittlere Farbe der bedruckten (nicht weißen) Teile eines Scheins.
  function scheinFarbe(rgba, roh, w, h, lab, o) {
    let r = 0, g = 0, b = 0, z = 0;
    const R = Math.ceil(o.a * 1.3);
    for (let y = Math.max(0, Math.round(o.y - R)); y < Math.min(h, o.y + R); y++)
      for (let x = Math.max(0, Math.round(o.x - R)); x < Math.min(w, o.x + R); x++) {
        if (lab[y * w + x] !== o.k || !roh[y * w + x]) continue;
        const p = (y * w + x) * 4; r += rgba[p]; g += rgba[p + 1]; b += rgba[p + 2]; z++;
      }
    if (!z) return null;
    r /= z; g /= z; b /= z;
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b), sat = (mx - mn) / (mx || 1);
    let hue = 0;
    if (mx !== mn) {
      if (mx === r) hue = 60 * (((g - b) / (mx - mn)) % 6);
      else if (mx === g) hue = 60 * ((b - r) / (mx - mn) + 2);
      else hue = 60 * ((r - g) / (mx - mn) + 4);
    }
    if (hue < 0) hue += 360;
    let wert;
    if (sat < 0.16) wert = 5;                        // grau
    else if (hue >= 330 || hue < 20) wert = 10;      // rot
    else if (hue < 45) wert = 50;                    // orange
    else if (hue >= 190 && hue < 290) wert = 20;     // blau
    else if (hue < 190) wert = 5;                    // grünlich-grau
    else wert = 10;                                  // pink/magenta
    return { wert, sicher: sat >= 0.16 || wert === 5, farbton: Math.round(hue), saettigung: +sat.toFixed(2) };
  }

  // --- Weißabgleich ---------------------------------------------------------
  // Papierfarbe an jeder Stelle schätzen: Graustufen-"Schließen" (erst Maximum-,
  // dann Minimumfilter) entfernt alles, was dunkler als das Papier und kleiner als
  // das Fenster ist (Münzen, Scheine) – Schattenkanten bleiben dabei scharf.
  // Danach wird jedes Pixel durch die Papierfarbe an seiner Stelle geteilt.
  function weissabgleich(rgba, w, h) {
    const f = Math.max(1, Math.round(Math.min(w, h) / 160));          // auf ~160 px verkleinern
    const sw = Math.ceil(w / f), sh = Math.ceil(h / f);
    const r = Math.max(4, Math.round(Math.min(sw, sh) * 0.13));       // Fenster > halbe Scheinbreite
    const papier = [0, 1, 2].map(c => {
      const klein = new Float32Array(sw * sh);
      for (let y = 0; y < sh; y++) for (let x = 0; x < sw; x++) {
        let s = 0, z = 0;
        for (let yy = y * f; yy < Math.min(h, (y + 1) * f); yy++)
          for (let xx = x * f; xx < Math.min(w, (x + 1) * f); xx++) { s += rgba[(yy * w + xx) * 4 + c]; z++; }
        klein[y * sw + x] = s / z;
      }
      let k = filter1d(klein, sw, sh, r, Math.max, true); k = filter1d(k, sw, sh, r, Math.max, false);
      k = filter1d(k, sw, sh, r, Math.min, true); k = filter1d(k, sw, sh, r, Math.min, false);
      return k;
    });
    const out = new Uint8ClampedArray(rgba.length);
    for (let y = 0; y < h; y++) {
      const fy = Math.min(sh - 1, Math.max(0, (y + 0.5) / f - 0.5)), y0 = Math.floor(fy), y1 = Math.min(sh - 1, y0 + 1), ay = fy - y0;
      for (let x = 0; x < w; x++) {
        const fx = Math.min(sw - 1, Math.max(0, (x + 0.5) / f - 0.5)), x0 = Math.floor(fx), x1 = Math.min(sw - 1, x0 + 1), ax = fx - x0;
        const i = (y * w + x) * 4;
        for (let c = 0; c < 3; c++) {
          const k = papier[c];
          const p = (k[y0 * sw + x0] * (1 - ax) + k[y0 * sw + x1] * ax) * (1 - ay) + (k[y1 * sw + x0] * (1 - ax) + k[y1 * sw + x1] * ax) * ay;
          out[i + c] = rgba[i + c] * 235 / Math.max(25, p);
        }
        out[i + 3] = 255;
      }
    }
    return out;
  }
  // Gleitendes Maximum/Minimum über 2r+1 Pixel, zeilen- oder spaltenweise.
  function filter1d(a, w, h, r, fn, zeilen) {
    const out = new Float32Array(a.length);
    const len = zeilen ? w : h, anz = zeilen ? h : w;
    for (let j = 0; j < anz; j++) for (let i = 0; i < len; i++) {
      let v = fn === Math.max ? -Infinity : Infinity;
      for (let d = Math.max(0, i - r); d <= Math.min(len - 1, i + r); d++) {
        const q = zeilen ? a[j * w + d] : a[d * w + j];
        v = fn(v, q);
      }
      out[zeilen ? j * w + i : i * w + j] = v;
    }
    return out;
  }

  // --- Hilfsfunktionen ------------------------------------------------------
  function median(a) { const s = a.slice().sort((x, y) => x - y); return s.length ? s[Math.floor(s.length / 2)] : 0; }

  // Abstandstransformation (Chamfer 3-4): Abstand jedes Pixels zum nächsten Pixel mit m==0.
  function abstand(m, w, h) {
    const D = new Float32Array(w * h), INF = 1e9;
    for (let i = 0; i < w * h; i++) D[i] = m[i] ? INF : 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x; if (!D[i]) continue;
      let v = D[i];
      if (x > 0) v = Math.min(v, D[i - 1] + 3); else v = Math.min(v, 3);
      if (y > 0) { v = Math.min(v, D[i - w] + 3); if (x > 0) v = Math.min(v, D[i - w - 1] + 4); if (x < w - 1) v = Math.min(v, D[i - w + 1] + 4); }
      else v = Math.min(v, 3);
      D[i] = v;
    }
    for (let y = h - 1; y >= 0; y--) for (let x = w - 1; x >= 0; x--) {
      const i = y * w + x; if (!D[i]) continue;
      let v = D[i];
      if (x < w - 1) v = Math.min(v, D[i + 1] + 3); else v = Math.min(v, 3);
      if (y < h - 1) { v = Math.min(v, D[i + w] + 3); if (x < w - 1) v = Math.min(v, D[i + w + 1] + 4); if (x > 0) v = Math.min(v, D[i + w - 1] + 4); }
      else v = Math.min(v, 3);
      D[i] = v;
    }
    for (let i = 0; i < w * h; i++) D[i] /= 3;
    return D;
  }

  function erodiere(m, w, h, r) {
    const D = abstand(m, w, h), out = new Uint8Array(w * h);
    for (let i = 0; i < w * h; i++) out[i] = D[i] > r ? 1 : 0;
    return out;
  }
  function dilatiere(m, w, h, r) {
    const inv = new Uint8Array(w * h);
    for (let i = 0; i < w * h; i++) inv[i] = m[i] ? 0 : 1;
    const D = abstand(inv, w, h), out = new Uint8Array(w * h);
    for (let i = 0; i < w * h; i++) out[i] = D[i] <= r + 0.5 ? 1 : 0;
    return out;
  }
  // Öffnen mit einer Scheibe vom Radius r: entfernt alles, was schmaler als 2r ist
  // (Linien, Schrift, schmale Verbindungen zwischen Münzen).
  function oeffneScheibe(m, w, h, r) { return dilatiere(erodiere(m, w, h, r), w, h, r); }

  function beschrifte(m, w, h, wert) {
    wert = wert === undefined ? 1 : wert;
    const lab = new Int32Array(w * h); let anzahl = 0;
    const stapel = new Int32Array(w * h);
    for (let i = 0; i < w * h; i++) {
      if (m[i] !== wert || lab[i]) continue;
      anzahl++; let sp = 0; stapel[sp++] = i; lab[i] = anzahl;
      while (sp) {
        const j = stapel[--sp], x = j % w;
        if (x > 0 && m[j - 1] === wert && !lab[j - 1]) { lab[j - 1] = anzahl; stapel[sp++] = j - 1; }
        if (x < w - 1 && m[j + 1] === wert && !lab[j + 1]) { lab[j + 1] = anzahl; stapel[sp++] = j + 1; }
        if (j >= w && m[j - w] === wert && !lab[j - w]) { lab[j - w] = anzahl; stapel[sp++] = j - w; }
        if (j < w * (h - 1) && m[j + w] === wert && !lab[j + w]) { lab[j + w] = anzahl; stapel[sp++] = j + w; }
      }
    }
    return { lab, anzahl };
  }

  function fuelleLoecher(m, w, h, maxLoch) {
    const { lab, anzahl } = beschrifte(m, w, h, 0);
    const groesse = new Int32Array(anzahl + 1), rand = new Uint8Array(anzahl + 1);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const k = lab[y * w + x]; if (!k) continue;
      groesse[k]++; if (x === 0 || y === 0 || x === w - 1 || y === h - 1) rand[k] = 1;
    }
    for (let i = 0; i < w * h; i++) { const k = lab[i]; if (k && !rand[k] && groesse[k] < maxLoch) m[i] = 1; }
  }

  global.KirmesErkennung = { erkenne };
})(typeof window !== 'undefined' ? window : this);
