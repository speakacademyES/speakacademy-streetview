# SpeakAcademy — Where in the World? 🌍

A Street View guessing game for English vocabulary lessons. Teacher-controlled, projector-ready.

## Setup (5 minutes)

### 1. Get a Google Maps API Key
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Enable **Maps JavaScript API** + **Street View Static API**
- Create an API key → restrict to your GitHub Pages domain: `https://yourusername.github.io`

### 2. Add the key to index.html
Open `index.html` and replace line:
```js
const MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY';
```
with your real key.

### 3. Deploy to GitHub Pages
```bash
cd streetview-game
git init
git add .
git commit -m "initial"
git remote add origin https://github.com/YOUR_USERNAME/speakacademy-streetview.git
git push -u origin main
```
Then in GitHub repo Settings → Pages → Source: main branch → Save.

Your game will be live at: `https://YOUR_USERNAME.github.io/speakacademy-streetview/`

## How to Play

1. Open on projector/big screen
2. Select a **category** (City, Transport, Nature, Food & Shops, Landmarks)
3. Press **▶ Start** — 60-second timer begins
4. Students call out what they see in English
5. Press **👁 Reveal** to show the location name + vocabulary list
6. Award points with Team A / Team B score cards (click to +1, ▼ to -1)
7. Press **⏭ Next** for a new location

## Adding More Locations

Edit the `LOCATIONS` object in `index.html`. Each entry needs:
```js
{ lat: 48.8566, lng: 2.3522, label: 'Paris, France 🇫🇷',
  words: ['café', 'boulevard', 'pavement', ...] }
```

## Categories Included
| Category | Locations |
|----------|-----------|
| 🏙️ City | Paris, London, Madrid, Berlin, Rome, Bilbao, Tokyo, New York |
| 🚌 Transport | Waterloo Station, Gare de Lyon, Port, Amsterdam Cycle Lanes |
| 🌿 Nature | Basque Coast, Swiss Alps, Phoenix Park, Oslo Fjord |
| 🍽️ Food & Shops | Marseille Market, La Boqueria, Borough Market, Paris Café |
| 🏛️ Landmarks | Eiffel Tower, Vatican, Houses of Parliament, Guggenheim Bilbao |
