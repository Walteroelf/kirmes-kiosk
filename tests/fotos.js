/*
 * Test der Geld-Erkennung mit echten Spielgeld-Fotos aus tests/fotos/.
 *   npm install --no-save jpeg-js@0.4.4 && node tests/fotos.js   (läuft automatisch auf GitHub)
 *
 * Der richtige Betrag steht vorn im Dateinamen (z. B. 33euro_foto14.jpg, Cent zählen nicht).
 * Die Fotos sind schon auf höchstens 900 Pixel verkleinert – genau wie in der App.
 * Neue Fotos: hineinlegen und in fotos/liste.txt eintragen (für tests/pruefen.html).
 * Bitte nur Fotos mit Spielgeld, keine Kinder, keine Hände.
 *
 * Bestanden, wenn kein Foto FALSCH erkannt wird (falscher Betrag, ohne nachzufragen).
 */
'use strict';
const fs = require('fs'), path = require('path');
const jpeg = require('jpeg-js');
require('../erkennung.js');
const { erkenne } = globalThis.KirmesErkennung;

const ordner = path.join(__dirname, 'fotos');
const dateien = fs.readdirSync(ordner).filter(n => /\.jpe?g$/i.test(n)).sort((a, b) => parseInt(a) - parseInt(b) || a.localeCompare(b));
const liste = fs.readFileSync(path.join(ordner, 'liste.txt'), 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
const g = { richtig: 0, nachfrage: 0, falsch: 0 }, fehler = [];
for (const n of dateien) {
  const bild = jpeg.decode(fs.readFileSync(path.join(ordner, n)), { useTArray: true, formatAsRGBA: true });
  const soll = parseInt(n, 10);
  const r = erkenne(bild.data, bild.width, bild.height);
  const urteil = r.summe === soll ? 'richtig' : r.unsicher ? 'nachfrage' : 'falsch';
  g[urteil]++;
  console.log(`${urteil === 'falsch' ? 'FALSCH ' : urteil.padEnd(9)} ${n.padEnd(22)} erkannt ${String(r.summe).padStart(3)} €  [${r.objekte.map(o => (o.art === 'schein' ? 'S' : o.art === 'unklar' ? '?' : '') + (o.wert === null ? '' : o.wert) + (o.sicher === false ? '?' : '')).join(' ')}]`);
  if (urteil === 'falsch') fehler.push(n);
}
const fehlend = dateien.filter(n => !liste.includes(n));
console.log(`\nECHTE FOTOS: ${g.richtig}/${dateien.length} richtig, ${g.nachfrage}x neues Foto, ${g.falsch}x falsch`);
if (fehlend.length) console.log('Hinweis: nicht in fotos/liste.txt eingetragen: ' + fehlend.join(', '));
if (fehler.length) { console.log('Nicht bestanden: ' + fehler.join(', ')); process.exit(1); }
console.log('Alle Fotos bestanden.');
