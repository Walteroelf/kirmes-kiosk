/*
 * Service Worker: macht die App offline nutzbar (z. B. bei wackligem Schul-WLAN).
 * Programmdateien: zuerst aus dem Netz (damit Änderungen sofort ankommen), sonst aus dem Speicher.
 * Bilder und Schriften: aus dem Speicher (ändern sich nicht).
 * Bei einer neuen Version VERSION erhöhen – dann wird alles neu geladen.
 */
const VERSION = '2.3.0';
const CACHE = 'kirmes-kiosk-' + VERSION;
const DATEIEN = [
  './',
  'index.html',
  'erkennung.js',
  'worker.js',
  'manifest.webmanifest',
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
  const fest = /\/(bilder|schriften|icons)\//.test(url.pathname);
  if (fest) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(antwort => {
      const kopie = antwort.clone(); caches.open(CACHE).then(c => c.put(e.request, kopie)); return antwort;
    })));
  } else {
    e.respondWith(fetch(e.request).then(antwort => {
      if (antwort.ok) { const kopie = antwort.clone(); caches.open(CACHE).then(c => c.put(e.request, kopie)); }
      return antwort;
    }).catch(() => caches.match(e.request, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
  }
});
