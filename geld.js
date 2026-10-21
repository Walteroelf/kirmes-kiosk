/*
 * Spielgeld zum Ziehen (Entwurf B "fotorealistisch"): Münzen und Scheine als SVG.
 * Farben, Aufbau und Größenverhältnisse wie echtes Euro-Geld, Motive selbst gezeichnet,
 * Scheine mit "SPIELGELD" beschriftet – nicht mit echtem Geld zu verwechseln.
 *
 *   KirmesGeld.bild(cent, groesse)  ->  SVG-Text
 *     cent:    Wert in Cent (10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)
 *     groesse: Pixel pro mm Münzdurchmesser (z. B. 3); Scheine werden 52-mal so breit gezeichnet.
 */
(function (global) {
'use strict';
// Echte Durchmesser in mm (Größenverhältnis), Farben nah am echten Geld
const MUENZEN = [
  { w: 10, mm: 19.75, art: 'gold' }, { w: 20, mm: 22.25, art: 'gold' }, { w: 50, mm: 24.25, art: 'gold' },
  { w: 100, mm: 23.25, art: 'bi1' }, { w: 200, mm: 25.75, art: 'bi2' },
];
const SCHEINE = [
  { w: 5, farbe: ['#c9cfc6', '#8f9a8c'], akzent: '#5e6b5b', motiv: 'tor' },
  { w: 10, farbe: ['#f1b2a8', '#c9675c'], akzent: '#8e2f27', motiv: 'bogen' },
  { w: 20, farbe: ['#b9cff0', '#5d84c4'], akzent: '#22457e', motiv: 'fenster' },
  { w: 50, farbe: ['#f8cf98', '#e08a32'], akzent: '#8a4a10', motiv: 'tor' },
  { w: 100, farbe: ['#bfe3b4', '#5fae5a'], akzent: '#245f22', motiv: 'bogen' },
];
let uid = 0;
const id = p => p + (++uid);
const sterne = (cx, cy, r, n, gr, farbe) => Array.from({ length: n }, (_, k) => {
  const a = -Math.PI / 2 + k * 2 * Math.PI / n, x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
  return stern(x, y, gr, farbe);
}).join('');
function stern(x, y, r, farbe) {
  let d = '';
  for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .45 : r; d += (i ? 'L' : 'M') + (x + rr * Math.cos(a)).toFixed(2) + ' ' + (y + rr * Math.sin(a)).toFixed(2); }
  return `<path d="${d}Z" fill="${farbe}"/>`;
}
const METALL = {
  gold:   ['#fff2b8', '#e9c158', '#b8892a', '#7a5a14'],
  silber: ['#ffffff', '#d9dde1', '#a3abb2', '#6e767d'],
};

// --- Münze ------------------------------------------------------------------
// stil: 'a' realistisch, 'b' fotorealistisch (Rändelung, starkes Licht), 'c' klar & groß
function muenze(m, stil, px) {
  const g = id('g'), g2 = id('h'), sch = id('s');
  const aussen = m.art === 'bi2' ? 'silber' : 'gold', innen = m.art === 'bi1' ? 'silber' : m.art === 'bi2' ? 'gold' : 'gold';
  const A = METALL[aussen], I = METALL[innen];
  const zahl = m.w >= 100 ? String(m.w / 100) : String(m.w);
  const einheit = m.w >= 100 ? 'EURO' : 'CENT';
  const bi = m.art !== 'gold';
  const rIn = m.art === 'bi1' ? 33 : m.art === 'bi2' ? 34.5 : 44;   // echter Innenteil ca. 70 % des Durchmessers
  const stark = stil === 'b';
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="${px}" height="${px}" role="img" aria-label="${zahl} ${einheit}">
  <defs>
    <radialGradient id="${g}" cx="${stark ? .3 : .38}" cy="${stark ? .26 : .32}" r="${stark ? .85 : .75}"><stop offset="0" stop-color="${A[0]}"/><stop offset=".45" stop-color="${A[1]}"/><stop offset=".85" stop-color="${A[2]}"/><stop offset="1" stop-color="${A[3]}"/></radialGradient>
    <radialGradient id="${g2}" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="${I[0]}"/><stop offset=".5" stop-color="${I[1]}"/><stop offset="1" stop-color="${I[2]}"/></radialGradient>
    <filter id="${sch}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="1.5" dy="2.5" stdDeviation="${stark ? 2 : 1.4}" flood-opacity="${stark ? .45 : .3}"/></filter>
  </defs>
  <g filter="url(#${sch})"><circle cx="50" cy="50" r="47" fill="url(#${g})" stroke="${A[3]}" stroke-width="1.2"/></g>`;
  if (stark) {  // Rändelung am Rand
    for (let k = 0; k < 90; k++) { const a = k * Math.PI / 45; s += `<path d="M${50 + 46.5 * Math.cos(a)} ${50 + 46.5 * Math.sin(a)} L${50 + 44 * Math.cos(a)} ${50 + 44 * Math.sin(a)}" stroke="${A[3]}" stroke-width=".7" opacity=".55"/>`; }
  }
  s += `<circle cx="50" cy="50" r="42.5" fill="none" stroke="${A[3]}" stroke-width=".8" opacity=".55"/>`;
  if (bi) s += `<circle cx="50" cy="50" r="${rIn}" fill="url(#${g2})" stroke="${I[3] || '#555'}" stroke-width="1"/>`;
  const tf = bi ? (innen === 'silber' ? '#4b5258' : '#6a4a0e') : '#6a4a0e';
  if (stil === 'c') {
    s += `<text x="50" y="${m.w >= 100 ? 62 : 58}" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, sans-serif" font-weight="800" font-size="${m.w >= 100 ? 38 : 32}" fill="${tf}">${zahl}${m.w >= 100 ? '€' : ''}</text>`;
    if (m.w < 100) s += `<text x="50" y="76" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="12" fill="${tf}">CENT</text>`;
  } else {
    // Sterne im Außenring, großer Wert, EURO/CENT, Prägung (heller Schatten unter der Schrift)
    s += sterne(50, 50, bi ? 40 : 38, 12, stark ? 2.4 : 2.3, bi ? (aussen === 'gold' ? '#8a6418' : '#5e666c') : '#8a6418');
    const fs = bi ? 30 : 30, y = bi ? 57 : 55;
    s += `<text x="50.8" y="${y + .8}" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="${fs}" fill="#fff" opacity=".55">${zahl}</text>`;
    s += `<text x="50" y="${y}" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="${fs}" fill="${tf}">${zahl}</text>`;
    s += `<text x="50" y="${bi ? 70 : 70}" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="${bi ? 7 : 8}" letter-spacing="1" fill="${tf}">${einheit}</text>`;
    // feine Linien ("Landkarte") wie auf der Wertseite – frei gezeichnet
    s += `<path d="M${bi ? 34 : 28} 38 C 40 30, 52 34, 58 28 M${bi ? 40 : 34} 76 C 48 80, 56 74, ${bi ? 64 : 70} 78" fill="none" stroke="${tf}" stroke-width=".8" opacity=".45"/>`;
  }
  // Glanzlicht
  s += `<path d="M22 32 A 32 32 0 0 1 44 16" fill="none" stroke="#fff" stroke-width="${stark ? 4 : 3}" stroke-linecap="round" opacity="${stark ? .75 : .5}"/>`;
  return s + '</svg>';
}

// --- Schein -----------------------------------------------------------------
function schein(n, stil) {
  const g = id('p'), sch = id('q'), holo = id('o');
  const [hell, dunkel] = n.farbe, ak = n.akzent, stark = stil === 'b';
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 128" role="img" aria-label="${n.w} Euro Spielgeld">
  <defs>
    <linearGradient id="${g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${hell}"/><stop offset=".55" stop-color="${dunkel}"/><stop offset="1" stop-color="${hell}"/></linearGradient>
    <linearGradient id="${holo}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f8"/><stop offset=".25" stop-color="#c7f0ff"/><stop offset=".5" stop-color="#ffe0f4"/><stop offset=".75" stop-color="#e4ffd6"/><stop offset="1" stop-color="#d9dde1"/></linearGradient>
    <filter id="${sch}" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="2" dy="3" stdDeviation="${stark ? 2.5 : 1.8}" flood-opacity="${stark ? .4 : .28}"/></filter>
  </defs>
  <g filter="url(#${sch})"><rect x="4" y="4" width="232" height="120" rx="6" fill="url(#${g})"/></g>`;
  if (stil === 'c') {
    s += `<rect x="12" y="12" width="216" height="104" rx="4" fill="none" stroke="${ak}" stroke-width="2" opacity=".5"/>`;
    s += `<text x="120" y="86" text-anchor="middle" font-family="Arial Rounded MT Bold, Arial, sans-serif" font-weight="800" font-size="64" fill="${ak}">${n.w}</text>`;
    s += `<text x="120" y="108" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="16" letter-spacing="2" fill="${ak}">EURO</text>`;
    s += `<text x="226" y="22" text-anchor="end" font-family="Arial, sans-serif" font-size="8" fill="${ak}" opacity=".8">SPIELGELD</text>`;
    return s + '</svg>';
  }
  // Guilloche-Linien (feine Wellen) als Untergrund
  for (let k = 0; k < 9; k++) {
    let d = `M4 ${20 + k * 11}`;
    for (let x = 4; x <= 236; x += 8) d += ` L${x} ${(20 + k * 11 + 3 * Math.sin(x / 11 + k)).toFixed(1)}`;
    s += `<path d="${d}" fill="none" stroke="#fff" stroke-width=".7" opacity=".35"/>`;
  }
  // Motiv: frei gezeichnetes Tor / Bogen / Fenster (Architektur-Stil)
  const mx = 92, my = 22;
  if (n.motiv === 'tor') s += `<path d="M${mx} ${my + 84} L${mx} ${my + 30} C ${mx} ${my + 6}, ${mx + 56} ${my + 6}, ${mx + 56} ${my + 30} L${mx + 56} ${my + 84}" fill="none" stroke="${ak}" stroke-width="5" opacity=".75"/><path d="M${mx + 12} ${my + 84} L${mx + 12} ${my + 34} C ${mx + 12} ${my + 18}, ${mx + 44} ${my + 18}, ${mx + 44} ${my + 34} L${mx + 44} ${my + 84}" fill="none" stroke="${ak}" stroke-width="2" opacity=".55"/>`;
  if (n.motiv === 'bogen') s += [0, 1, 2].map(i => `<path d="M${mx - 12 + i * 30} ${my + 84} L${mx - 12 + i * 30} ${my + 46} C ${mx - 12 + i * 30} ${my + 30}, ${mx + 12 + i * 30} ${my + 30}, ${mx + 12 + i * 30} ${my + 46} L${mx + 12 + i * 30} ${my + 84}" fill="none" stroke="${ak}" stroke-width="3.5" opacity=".7"/>`).join('') + `<path d="M${mx - 18} ${my + 30} L${mx + 72} ${my + 30}" stroke="${ak}" stroke-width="3" opacity=".6"/>`;
  if (n.motiv === 'fenster') s += `<path d="M${mx} ${my + 84} L${mx} ${my + 36} L${mx + 28} ${my + 8} L${mx + 56} ${my + 36} L${mx + 56} ${my + 84} Z" fill="none" stroke="${ak}" stroke-width="4.5" opacity=".7"/><circle cx="${mx + 28}" cy="${my + 40}" r="11" fill="none" stroke="${ak}" stroke-width="2.5" opacity=".6"/><path d="M${mx + 28} ${my + 29} L${mx + 28} ${my + 51} M${mx + 17} ${my + 40} L${mx + 39} ${my + 40}" stroke="${ak}" stroke-width="1.5" opacity=".6"/>`;
  // Sternenkreis, Wertzahlen, EURO, Spielgeld-Hinweis
  s += sterne(44, 44, 16, 12, 2.6, '#fff8c4');
  s += `<text x="16" y="114" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="34" fill="${ak}">${n.w}</text>`;
  s += `<text x="${stark ? 196 : 226}" y="${stark ? 44 : 34}" text-anchor="end" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="26" fill="#fff" opacity=".85">${n.w}</text>`;
  s += `<text x="120" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" font-size="11" letter-spacing="3" fill="${ak}" opacity=".85">EURO</text>`;
  s += `<text x="${stark ? 196 : 226}" y="${stark ? 20 : 114}" text-anchor="end" font-family="Arial, sans-serif" font-size="7.5" letter-spacing="1" fill="${stark ? '#fff' : ak}" opacity=".85">SPIELGELD</text>`;
  if (stark) {
    // Hologramm-Streifen, Wasserzeichen-Feld, Papierstruktur
    s += `<rect x="204" y="4" width="18" height="120" fill="url(#${holo})" opacity=".9"/>`;
    s += [20, 44, 68, 92, 112].map(y => stern(213, y, 4.5, '#ffffff')).join('');
    s += `<ellipse cx="176" cy="74" rx="18" ry="24" fill="#fff" opacity=".22"/>`;
    for (let k = 0; k < 140; k++) s += `<circle cx="${(4 + ((k * 73) % 230)).toFixed(0)}" cy="${(6 + ((k * 37) % 116)).toFixed(0)}" r=".5" fill="#000" opacity=".08"/>`;
  }
  s += `<path d="M10 10 L60 10" stroke="#fff" stroke-width="2" opacity=".5"/>`;
  return s + '</svg>';
}


function bild(cent, groesse) {
  const m = MUENZEN.find(x => x.w === cent);
  if (m) return muenze(m, 'b', Math.round(m.mm * groesse));
  const n = SCHEINE.find(x => x.w * 100 === cent);
  if (!n) return '';
  return schein(n, 'b').replace('<svg ', `<svg width="${Math.round(52 * groesse)}" height="${Math.round(52 * groesse * 128 / 240)}" `);
}
global.KirmesGeld = { bild, muenzeMm: cent => (MUENZEN.find(x => x.w === cent) || {}).mm };
})(typeof globalThis !== 'undefined' ? globalThis : this);
