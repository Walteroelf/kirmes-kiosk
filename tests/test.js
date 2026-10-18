/*
 * Automatischer Test der Geld-Erkennung mit künstlichen Szenen.
 *   node tests/test.js            (läuft auch automatisch auf GitHub bei jeder Änderung)
 *   node tests/test.js --details  (jede Szene einzeln ausgeben)
 *
 * Bewertet wird wie in der App:
 *   richtig        – erkannter Betrag stimmt
 *   neues Foto     – Betrag stimmt nicht, aber die App ist unsicher und bittet um ein neues Foto
 *   FALSCH         – Betrag stimmt nicht und die App ist sich sicher (das darf kaum vorkommen)
 */
'use strict';
const istNode = typeof require === 'function' && typeof process !== 'undefined';
const ausgabe = istNode ? console.log : print;
const argumente = istNode ? process.argv.slice(2) : (typeof arguments !== 'undefined' ? Array.from(arguments) : []);
if (istNode) {
  require('../erkennung.js'); require('./szenen.js');
} else {
  const ordner = argumente[0] || '.';
  load(ordner + '/../erkennung.js'); load(ordner + '/szenen.js');
}
const details = argumente.includes('--details');
const { erkenne, qualitaet } = globalThis.KirmesErkennung;
const { szene } = globalThis.KirmesSzenen;

// Gruppen von Szenen: [Name, Anzahl, Optionen, höchstens erlaubte FALSCH-Urteile]
const gruppen = [
  ['normal',           12, {}, 0],
  ['mit 5-€-Schein',    6, { scheine: [5] }, 0],
  ['mit 10-€-Schein',   6, { scheine: [10] }, 0],
  ['mit 20-€-Schein',   6, { scheine: [20] }, 0],
  ['zwei Scheine',      4, { scheine: [5, 10], muenzen: 4, groesse: 18 }, 1],
  ['Scheine überlappen', 4, { scheine: [5, 10], muenzen: 3, groesse: 18, scheineUeberlappen: true }, 1],
  ['Münze auf Schein',  6, { scheine: [5], aufSchein: true, muenzen: 4 }, 1],
  ['Münzen berühren',   8, { beruehren: true }, 1],
  ['warmes Licht',      6, { kanal: [1.12, 0.97, 0.72] }, 0],
  ['kaltes Licht',      6, { kanal: [0.82, 0.95, 1.12] }, 0],
  ['Schattenverlauf',   6, { verlauf: 0.5 }, 0],
  ['Schattenkante',     6, { schattenkante: 0.45 }, 1],
  ['Spiegelungen',      8, { glanz: 0.7 }, 1],
  ['dunkel',            6, { dunkel: 0.55, rauschen: 12 }, 1],
  ['leicht unscharf',   6, { unschaerfe: 1 }, 1],
  ['viele Münzen',      6, { muenzen: 10, groesse: 20 }, 1],
];

let gesamt = { richtig: 0, nachfrage: 0, falsch: 0, n: 0 }, fehlgeschlagen = [];
let nr = 100;
for (const [name, anzahl, opt, erlaubt] of gruppen) {
  const g = { richtig: 0, nachfrage: 0, falsch: 0 };
  for (let k = 0; k < anzahl; k++) {
    const s = szene(nr++, opt);
    const r = erkenne(s.rgba, s.w, s.h);
    let urteil;
    if (r.summe === s.summe) urteil = 'richtig'; else if (r.unsicher) urteil = 'nachfrage'; else urteil = 'falsch';
    g[urteil]++; gesamt[urteil]++; gesamt.n++;
    if (details || urteil === 'falsch') ausgabe(`  ${urteil === 'falsch' ? 'FALSCH ' : urteil.padEnd(7)} ${name} #${nr - 1}: erkannt ${r.summe} €, richtig ${s.summe} €  [${r.objekte.map(o => (o.art === 'schein' ? 'S' : o.art === 'unklar' ? '?' : '') + (o.wert === null ? '' : o.wert)).join(' ')}]`);
  }
  const ok = g.falsch <= erlaubt;
  if (!ok) fehlgeschlagen.push(name);
  ausgabe(`${ok ? 'ok  ' : 'FEHL'} ${name.padEnd(18)} richtig ${String(g.richtig).padStart(2)}/${anzahl}  neues Foto ${g.nachfrage}  falsch ${g.falsch} (erlaubt ${erlaubt})`);
}

// Fotocheck
const q = [
  ['scharf und hell', szene(900, {}), null],
  ['unscharf',        szene(901, { unschaerfe: 6 }), 'unscharf'],
  ['zu dunkel',       szene(902, { dunkel: 0.22, rauschen: 3 }), 'dunkel'],
  ['ohne Papier',     szene(903, { ohnePapier: true }), 'kein_papier'],
];
for (const [name, s, soll] of q) {
  const r = qualitaet(s.rgba, s.w, s.h);
  const ok = r.grund === soll;
  if (!ok) fehlgeschlagen.push('Fotocheck ' + name);
  ausgabe(`${ok ? 'ok  ' : 'FEHL'} Fotocheck ${name.padEnd(16)} -> ${r.grund || 'ok'}  ${JSON.stringify(r.werte)}`);
}

ausgabe(`\nGESAMT: ${gesamt.richtig}/${gesamt.n} richtig, ${gesamt.nachfrage}x neues Foto, ${gesamt.falsch}x falsch`);
if (fehlgeschlagen.length) {
  ausgabe('Nicht bestanden: ' + fehlgeschlagen.join(', '));
  if (istNode) process.exit(1);
} else ausgabe('Alle Tests bestanden.');
