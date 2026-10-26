/*
 * Service Worker: macht die App offline nutzbar (z. B. bei wackligem Schul-WLAN).
 * Programmdateien: zuerst aus dem Netz (damit Änderungen sofort ankommen), sonst aus dem Speicher.
 * Bilder, Schriften und Ansagen (ton/): aus dem Speicher (ändern sich nicht).
 * Die Ansagen liegen in einem eigenen Speicher 'kirmes-ton', den die App selbst im Hintergrund
 * füllt (index.html, ansagenSpeichern). Er bleibt bei neuen Versionen erhalten.
 * Bei einer neuen Version VERSION erhöhen – dann wird alles neu geladen.
 */
const VERSION = '4.9.1';
const CACHE = 'kirmes-kiosk-' + VERSION;
const DATEIEN = [
  './',
  'index.html',
  'erkennung.js',
  'worker.js',
  'geld.js',
  'aufkleber.js',
  'laeden/kirmes.svg',
  'laeden/baeckerei.svg',
  'laeden/spielwaren.svg',
  'manifest.webmanifest',
  'ton/index.json',
  'bilder/baeckerei/amerikaner.svg',
  'bilder/baeckerei/apfelkuchen.svg',
  'bilder/baeckerei/apfelschorle.svg',
  'bilder/baeckerei/baguette.svg',
  'bilder/baeckerei/belegtes-broetchen.svg',
  'bilder/baeckerei/berliner.svg',
  'bilder/baeckerei/brezel.svg',
  'bilder/baeckerei/broetchen.svg',
  'bilder/baeckerei/brot.svg',
  'bilder/baeckerei/croissant.svg',
  'bilder/baeckerei/erdbeertoertchen.svg',
  'bilder/baeckerei/kaesekuchen.svg',
  'bilder/baeckerei/kakao.svg',
  'bilder/baeckerei/keks.svg',
  'bilder/baeckerei/laugenstange.svg',
  'bilder/baeckerei/mohnbroetchen.svg',
  'bilder/baeckerei/rosinenbroetchen.svg',
  'bilder/baeckerei/schokocroissant.svg',
  'bilder/baeckerei/vollkornbrot.svg',
  'bilder/baeckerei/zimtschnecke.svg',
  'bilder/brezel.svg',
  'bilder/burger.svg',
  'bilder/cola.svg',
  'bilder/donut.svg',
  'bilder/falaffel.svg',
  'bilder/hotdog.svg',
  'bilder/kaffee.svg',
  'bilder/kirschkuchen.svg',
  'bilder/lebkuchen.svg',
  'bilder/limo.svg',
  'bilder/muffin.svg',
  'bilder/pizza.svg',
  'bilder/pommes.svg',
  'bilder/popcorn.svg',
  'bilder/saft.svg',
  'bilder/schoko-kuchen.svg',
  'bilder/schokolade.svg',
  'bilder/spielwaren/ball.svg',
  'bilder/spielwaren/bausteine.svg',
  'bilder/spielwaren/bilderbuch.svg',
  'bilder/spielwaren/brettspiel.svg',
  'bilder/spielwaren/drachen.svg',
  'bilder/spielwaren/eisenbahn.svg',
  'bilder/spielwaren/fahrrad.svg',
  'bilder/spielwaren/jojo.svg',
  'bilder/spielwaren/kuscheltier.svg',
  'bilder/spielwaren/malkasten.svg',
  'bilder/spielwaren/puppe.svg',
  'bilder/spielwaren/puppenhaus.svg',
  'bilder/spielwaren/puzzle.svg',
  'bilder/spielwaren/rc-auto.svg',
  'bilder/spielwaren/roller.svg',
  'bilder/spielwaren/seifenblasen.svg',
  'bilder/spielwaren/skateboard.svg',
  'bilder/spielwaren/spielzeugauto.svg',
  'bilder/spielwaren/springseil.svg',
  'bilder/spielwaren/xylophon.svg',
  'bilder/tee.svg',
  'bilder/wurst.svg',
  'bilder/zuckerwatte.svg',
  'schriften/andika-400.woff2',
  'schriften/andika-700.woff2',
  'schriften/grandstander.woff2',
  'icons/icon-180.png',
  'icons/icon-192.png',
  'icons/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(DATEIEN)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(namen => Promise.all(namen.filter(n => n.startsWith('kirmes-kiosk-') && n !== CACHE).map(n => caches.delete(n))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  const fest = /\/(bilder|schriften|icons|ton)\//.test(url.pathname) && !url.pathname.endsWith('index.json');
  if (fest) {
    const ziel = url.pathname.includes('/ton/') ? 'kirmes-ton' : CACHE;
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(antwort => {
      if (antwort.ok) { const kopie = antwort.clone(); caches.open(ziel).then(c => c.put(e.request, kopie)); }
      return antwort;
    })));
  } else {
    e.respondWith(fetch(e.request).then(antwort => {
      if (antwort.ok) { const kopie = antwort.clone(); caches.open(CACHE).then(c => c.put(e.request, kopie)); }
      return antwort;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
  }
});
