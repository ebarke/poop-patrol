const CACHE = 'poop-patrol-v4';
const ASSETS = [
    '/',
    '/index.html',
    '/manifest.json',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE && k !== CACHE + '-tiles').map(k => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', e => {
    // Overpass water queries: always network, never cache (must be fresh)
    if (e.request.url.includes('overpass-api.de')) {
        e.respondWith(fetch(e.request));
        return;
    }
    // Tile requests: network first, cache fallback for offline use
    if (e.request.url.includes('arcgisonline.com') || e.request.url.includes('tile.openstreetmap.org')) {
        e.respondWith(
            fetch(e.request).then(res => {
                const clone = res.clone();
                caches.open(CACHE + '-tiles').then(c => c.put(e.request, clone));
                return res;
            }).catch(() => caches.match(e.request))
        );
        return;
    }
    // App shell: cache first, network fallback
    e.respondWith(
        caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
            if (res.ok) {
                const clone = res.clone();
                caches.open(CACHE).then(c => c.put(e.request, clone));
            }
            return res;
        }))
    );
});