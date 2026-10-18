/* Rechnet die Geld-Erkennung im Hintergrund, damit die Oberfläche nicht einfriert. */
importScripts('erkennung.js');
self.onmessage = function (e) {
  const { id, puffer, breite, hoehe } = e.data;
  try {
    const rgba = new Uint8ClampedArray(puffer);
    const ergebnis = KirmesErkennung.erkenne(rgba, breite, hoehe);
    const qualitaet = KirmesErkennung.qualitaet(rgba, breite, hoehe);
    self.postMessage({ id, ergebnis, qualitaet });
  } catch (fehler) {
    self.postMessage({ id, fehler: String(fehler && fehler.message || fehler) });
  }
};
