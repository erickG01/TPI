const CACHE_NAME = 'repartidor-cache-v1';
const urlsToCache = [
  '/repartidor/',
  '/static/imagenes/Repartidor/app-icon-512x512.png',
  '/static/imagenes/screenshots/screenshot3.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
