# 💩 Poop Patrol — GPS Yard Cleanup App

A Progressive Web App (PWA) for marking and collecting dog poop in your yard using real GPS, with a nearest-neighbour shortest-path routing algorithm.

---

## Features

- 📍 **Real GPS tracking** — uses device geolocation with high accuracy mode
- 🗺️ **Live map** — OpenStreetMap via Leaflet.js
- 💩 **Mark poop zones** — tap anywhere on the map to pin a location
- 🧤 **Pickup mode** — calculates the optimal route using Nearest Neighbour TSP
- 📏 **Live distance** — shows real-time metres to the next target
- ✅ **Auto-collect** — removes pin automatically when you walk within 2.5m
- 🔗 **Shareable maps** — encode all pins into a URL to share with helpers
- 📴 **Offline support** — service worker caches map tiles and app shell
- 📱 **Installable** — add to home screen on iOS/Android like a native app

---

## Files

```
poop-patrol/
├── index.html      ← Full app (single file, no build step)
├── manifest.json   ← PWA manifest (icons, name, theme)
├── sw.js           ← Service worker (offline + tile caching)
├── icon-192.png    ← App icon (replace with 💩 emoji icon)
├── icon-512.png    ← App icon large
└── README.md
```

---

## Deployment Options

### Option 1 — Netlify (recommended, free)
1. Go to [netlify.com](https://netlify.com) → "Add new site" → "Deploy manually"
2. Drag and drop the `poop-patrol/` folder
3. Done — you get a live HTTPS URL instantly

> **HTTPS is required** for GPS/geolocation to work in browsers.

### Option 2 — Vercel
```bash
npm i -g vercel
cd poop-patrol
vercel --prod
```

### Option 3 — GitHub Pages
1. Push folder contents to a GitHub repo
2. Settings → Pages → Deploy from main branch `/root`
3. Visit `https://yourusername.github.io/poop-patrol`

### Option 4 — Any static host
Upload all files to any web server that serves over HTTPS.  
Apache/Nginx — no special config needed, it's all static files.

---

## Replace the Icons

The included icons are solid green placeholders. To make a proper 💩 icon:

1. Open `icon-192.svg` in a browser or design tool
2. Export as PNG at 192×192 and 512×512
3. Replace `icon-192.png` and `icon-512.png`

Or use a free tool like [favicon.io](https://favicon.io/emoji-favicons/pile-of-poo/) to generate emoji-based icons.

---

## How the algorithm works

**Nearest Neighbour Travelling Salesman heuristic:**

1. Start at the user's current GPS position
2. Find the closest unvisited poop pin (haversine distance)
3. Move there, mark it as next in route
4. Repeat from that position until all pins are ordered

This gives a near-optimal route for typical yard-scale distances. It runs in O(n²) time — perfect for the expected number of poop zones (1–50).

---

## Browser Support

| Browser | GPS | Install as app |
|---------|-----|----------------|
| Chrome (Android) | ✅ | ✅ |
| Safari (iOS 16.4+) | ✅ | ✅ |
| Firefox (Android) | ✅ | ⚠️ partial |
| Chrome (desktop) | ✅ | ✅ |
| Safari (macOS) | ✅ | ✅ |

> GPS accuracy indoors is poor. Use outdoors for best results.

---

## Privacy

All data stays on your device. No server, no database, no analytics.  
Poop locations are only shared when you explicitly tap "Share" and send the link.
