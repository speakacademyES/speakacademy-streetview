#!/usr/bin/env python3
"""
Generate ~400 globally balanced Street View locations for G.O. Guesser.
Outputs:
  - data/locations.json (master list)
  - data/packs/europe.json
  - data/packs/latin-america.json
  - data/packs/asia.json
  - data/packs/africa.json
  - data/packs/north-america.json
  - data/packs/oceania.json
  - data/packs/unusual.json
"""
import json
import os

# All locations: lat, lng, label, pack, words (English vocab visible at this location)
LOCATIONS = [

  # ─── EUROPE ──────────────────────────────────────────────────────────
  # UK & Ireland
  {"lat": 51.5007, "lng": -0.1246, "label": "Houses of Parliament, London 🇬🇧", "pack": "europe",
   "words": ["parliament", "clock tower", "bridge", "river", "double-decker bus"]},
  {"lat": 51.5033, "lng": -0.1195, "label": "South Bank, London 🇬🇧", "pack": "europe",
   "words": ["embankment", "skyscraper", "crane", "footbridge", "riverbank"]},
  {"lat": 51.5138, "lng": -0.0984, "label": "St. Paul's Cathedral, London 🇬🇧", "pack": "europe",
   "words": ["dome", "cathedral", "steps", "columns", "churchyard"]},
  {"lat": 53.4808, "lng": -2.2426, "label": "Manchester City Centre 🇬🇧", "pack": "europe",
   "words": ["tram", "shopping centre", "pub", "cobblestone", "alley"]},
  {"lat": 55.9533, "lng": -3.1883, "label": "Edinburgh Old Town 🇬🇧", "pack": "europe",
   "words": ["castle", "cobblestone", "steep hill", "tenement", "closes"]},
  {"lat": 53.3498, "lng": -6.2603, "label": "Dublin, Ireland 🇮🇪", "pack": "europe",
   "words": ["pub", "bridge", "tram", "Georgian building", "cobblestone"]},
  {"lat": 51.4816, "lng": -3.1791, "label": "Cardiff, Wales 🇬🇧", "pack": "europe",
   "words": ["castle", "arcade", "pedestrian street", "market", "fountain"]},
  {"lat": 54.5973, "lng": -5.9301, "label": "Belfast, Northern Ireland 🇬🇧", "pack": "europe",
   "words": ["mural", "terrace houses", "docks", "crane", "harbour"]},

  # Spain
  {"lat": 43.2630, "lng": -2.9350, "label": "Bilbao Old Town 🇪🇸", "pack": "europe",
   "words": ["balcony", "narrow street", "tapas bar", "river", "iron bridge"]},
  {"lat": 43.2684, "lng": -2.9330, "label": "Guggenheim Museum, Bilbao 🇪🇸", "pack": "europe",
   "words": ["titanium", "sculpture", "riverside", "modern architecture", "dog topiary"]},
  {"lat": 41.3851, "lng": 2.1734, "label": "Las Ramblas, Barcelona 🇪🇸", "pack": "europe",
   "words": ["market stall", "kiosk", "pavement", "newspaper stand", "tourist"]},
  {"lat": 41.4036, "lng": 2.1744, "label": "Sagrada Família, Barcelona 🇪🇸", "pack": "europe",
   "words": ["spire", "stone carvings", "scaffolding", "queue", "gothic"]},
  {"lat": 40.4168, "lng": -3.7038, "label": "Puerta del Sol, Madrid 🇪🇸", "pack": "europe",
   "words": ["square", "fountain", "clock", "pedestrian zone", "department store"]},
  {"lat": 37.3891, "lng": -5.9845, "label": "Seville Cathedral 🇪🇸", "pack": "europe",
   "words": ["bell tower", "orange trees", "horse carriage", "archway", "Gothic facade"]},
  {"lat": 37.1773, "lng": -3.5986, "label": "Alhambra, Granada 🇪🇸", "pack": "europe",
   "words": ["Moorish palace", "courtyard", "fountain", "archway", "ornate ceiling"]},
  {"lat": 43.3183, "lng": -1.9812, "label": "San Sebastián, Spain 🇪🇸", "pack": "europe",
   "words": ["beach promenade", "bay", "pintxos bar", "Belle Époque building", "fishing boat"]},
  {"lat": 28.1235, "lng": -15.4363, "label": "Las Palmas, Gran Canaria 🇪🇸", "pack": "europe",
   "words": ["palm tree", "seafront", "promenade", "balcony", "ferry terminal"]},

  # France
  {"lat": 48.8584, "lng": 2.2945, "label": "Eiffel Tower, Paris 🇫🇷", "pack": "europe",
   "words": ["iron tower", "lawn", "fountain", "tourist", "café"]},
  {"lat": 48.8600, "lng": 2.3266, "label": "Louvre Museum, Paris 🇫🇷", "pack": "europe",
   "words": ["glass pyramid", "courtyard", "museum", "colonnade", "sculpture"]},
  {"lat": 43.2965, "lng": 5.3698, "label": "Vieux-Port, Marseille 🇫🇷", "pack": "europe",
   "words": ["harbour", "fishing boat", "quayside", "café terrace", "fish market"]},
  {"lat": 45.7640, "lng": 4.8357, "label": "Lyon City Centre 🇫🇷", "pack": "europe",
   "words": ["traboule", "narrow passage", "town hall", "fountain", "cobblestone"]},
  {"lat": 43.7102, "lng": 7.2620, "label": "Nice Promenade des Anglais 🇫🇷", "pack": "europe",
   "words": ["seafront promenade", "palm tree", "pebble beach", "hotel", "blue sea"]},
  {"lat": 47.3220, "lng": 5.0415, "label": "Dijon, France 🇫🇷", "pack": "europe",
   "words": ["half-timbered house", "mustard shop", "market", "church spire", "courtyard"]},
  {"lat": 44.8378, "lng": -0.5792, "label": "Bordeaux Waterfront 🇫🇷", "pack": "europe",
   "words": ["neoclassical facade", "tram", "wine shop", "bridge", "riverside"]},

  # Germany, Austria, Switzerland
  {"lat": 52.5200, "lng": 13.4050, "label": "Brandenburg Gate, Berlin 🇩🇪", "pack": "europe",
   "words": ["gate", "columns", "monument", "cobblestone", "cycle lane"]},
  {"lat": 48.1351, "lng": 11.5820, "label": "Marienplatz, Munich 🇩🇪", "pack": "europe",
   "words": ["town hall", "clock tower", "pedestrian zone", "beer garden", "church"]},
  {"lat": 53.5511, "lng": 9.9937, "label": "Speicherstadt, Hamburg 🇩🇪", "pack": "europe",
   "words": ["red brick warehouse", "canal", "bridge", "crane", "reflection"]},
  {"lat": 50.9413, "lng": 6.9583, "label": "Cologne Cathedral 🇩🇪", "pack": "europe",
   "words": ["Gothic spire", "cathedral", "cobblestone", "Rhine river", "tourist"]},
  {"lat": 47.8095, "lng": 13.0550, "label": "Hallstatt, Austria 🇦🇹", "pack": "europe",
   "words": ["lake", "mountain", "wooden house", "boat", "narrow street"]},
  {"lat": 47.3769, "lng": 8.5417, "label": "Zurich Old Town 🇨🇭", "pack": "europe",
   "words": ["clock tower", "guild house", "cobblestone", "tram", "river"]},

  # Italy
  {"lat": 41.9028, "lng": 12.4964, "label": "Colosseum, Rome 🇮🇹", "pack": "europe",
   "words": ["amphitheatre", "arch", "ruin", "tourist", "cobblestone"]},
  {"lat": 45.4408, "lng": 12.3155, "label": "Grand Canal, Venice 🇮🇹", "pack": "europe",
   "words": ["gondola", "canal", "palazzo", "bridge", "vaporetto"]},
  {"lat": 43.7696, "lng": 11.2558, "label": "Duomo, Florence 🇮🇹", "pack": "europe",
   "words": ["dome", "marble facade", "bell tower", "piazza", "Renaissance"]},
  {"lat": 40.8518, "lng": 14.2681, "label": "Naples Old Town 🇮🇹", "pack": "europe",
   "words": ["laundry", "scooter", "narrow street", "pizzeria", "balcony"]},
  {"lat": 38.1157, "lng": 13.3615, "label": "Palermo, Sicily 🇮🇹", "pack": "europe",
   "words": ["baroque church", "market", "street food", "archway", "palm tree"]},
  {"lat": 45.4654, "lng": 9.1866, "label": "Duomo, Milan 🇮🇹", "pack": "europe",
   "words": ["Gothic spire", "arcade", "fashion shop", "piazza", "tram"]},

  # Netherlands, Belgium, Luxembourg
  {"lat": 52.3676, "lng": 4.9041, "label": "Amsterdam Canal 🇳🇱", "pack": "europe",
   "words": ["canal", "narrow house", "bicycle", "bridge", "houseboat"]},
  {"lat": 51.2194, "lng": 4.4025, "label": "Antwerp Old Town 🇧🇪", "pack": "europe",
   "words": ["guild house", "cobblestone", "cathedral", "diamond shop", "market square"]},
  {"lat": 50.8503, "lng": 4.3517, "label": "Grand Place, Brussels 🇧🇪", "pack": "europe",
   "words": ["ornate facade", "guild hall", "cobblestone", "flower market", "chocolate shop"]},
  {"lat": 51.0543, "lng": 3.7174, "label": "Ghent Old Town 🇧🇪", "pack": "europe",
   "words": ["canal", "medieval tower", "bridge", "cobblestone", "gabled roof"]},

  # Scandinavia
  {"lat": 59.9139, "lng": 10.7522, "label": "Oslo Waterfront 🇳🇴", "pack": "europe",
   "words": ["modern museum", "waterfront", "ferry", "opera house", "fjord"]},
  {"lat": 60.3913, "lng": 5.3221, "label": "Bergen Wharf, Norway 🇳🇴", "pack": "europe",
   "words": ["colourful wooden house", "wharf", "fish market", "cobblestone", "mountain"]},
  {"lat": 57.7089, "lng": 11.9746, "label": "Gothenburg, Sweden 🇸🇪", "pack": "europe",
   "words": ["tram", "canal", "park", "harbour", "cobblestone"]},
  {"lat": 55.6761, "lng": 12.5683, "label": "Nyhavn, Copenhagen 🇩🇰", "pack": "europe",
   "words": ["colourful townhouse", "canal", "sailboat", "café terrace", "cobblestone"]},
  {"lat": 64.1355, "lng": -21.8954, "label": "Reykjavik, Iceland 🇮🇸", "pack": "europe",
   "words": ["colourful house", "church", "geothermal steam", "harbour", "volcanic rock"]},
  {"lat": 60.1699, "lng": 24.9384, "label": "Helsinki Senate Square 🇫🇮", "pack": "europe",
   "words": ["cathedral dome", "neoclassical", "tram", "market square", "harbour"]},

  # Eastern Europe
  {"lat": 50.0755, "lng": 14.4378, "label": "Prague Old Town Square 🇨🇿", "pack": "europe",
   "words": ["astronomical clock", "Gothic church", "cobblestone", "market", "tower"]},
  {"lat": 47.4979, "lng": 19.0402, "label": "Budapest Parliament 🇭🇺", "pack": "europe",
   "words": ["Gothic Revival", "Danube", "parliament", "spire", "promenade"]},
  {"lat": 50.0647, "lng": 19.9450, "label": "Krakow Market Square 🇵🇱", "pack": "europe",
   "words": ["cloth hall", "horse carriage", "cobblestone", "pigeons", "church tower"]},
  {"lat": 44.4268, "lng": 26.1025, "label": "Bucharest Old Town 🇷🇴", "pack": "europe",
   "words": ["art nouveau", "outdoor café", "cobblestone", "mansion", "graffiti"]},
  {"lat": 42.6977, "lng": 23.3219, "label": "Sofia, Bulgaria 🇧🇬", "pack": "europe",
   "words": ["orthodox dome", "Soviet architecture", "mountain backdrop", "tram", "park"]},
  {"lat": 44.8176, "lng": 20.4569, "label": "Belgrade Fortress 🇷🇸", "pack": "europe",
   "words": ["fortress walls", "river confluence", "cannon", "park", "Belgrade sign"]},
  {"lat": 46.0511, "lng": 14.5051, "label": "Ljubljana, Slovenia 🇸🇮", "pack": "europe",
   "words": ["castle hill", "river", "café terrace", "bridge", "colourful building"]},
  {"lat": 43.5081, "lng": 16.4402, "label": "Split Old Town, Croatia 🇭🇷", "pack": "europe",
   "words": ["Roman palace", "archway", "limestone", "seafront", "cafés"]},
  {"lat": 42.4411, "lng": 19.2636, "label": "Kotor, Montenegro 🇲🇪", "pack": "europe",
   "words": ["city walls", "bay", "mountain", "cobblestone", "Venetian architecture"]},

  # Portugal & Greece
  {"lat": 38.7071, "lng": -9.1355, "label": "Alfama, Lisbon 🇵🇹", "pack": "europe",
   "words": ["tram 28", "azulejo tiles", "viewpoint", "laundry", "cobblestone"]},
  {"lat": 41.1579, "lng": -8.6291, "label": "Porto Old Town 🇵🇹", "pack": "europe",
   "words": ["azulejo facade", "riverside", "port wine", "iron bridge", "baroque church"]},
  {"lat": 37.9838, "lng": 23.7275, "label": "Acropolis, Athens 🇬🇷", "pack": "europe",
   "words": ["temple", "columns", "olive tree", "ruin", "hill"]},
  {"lat": 36.4618, "lng": 28.2277, "label": "Rhodes Old Town 🇬🇷", "pack": "europe",
   "words": ["medieval walls", "cobblestone", "archway", "taverna", "Ottoman fountain"]},
  {"lat": 36.3932, "lng": 25.4615, "label": "Santorini, Greece 🇬🇷", "pack": "europe",
   "words": ["white-washed house", "blue dome", "volcanic cliff", "terrace", "sea view"]},

  # ─── LATIN AMERICA ──────────────────────────────────────────────────
  {"lat": -22.9068, "lng": -43.1729, "label": "Copacabana, Rio de Janeiro 🇧🇷", "pack": "latin-america",
   "words": ["beach", "mosaic pavement", "palm tree", "seafront", "mountain"]},
  {"lat": -23.5505, "lng": -46.6333, "label": "São Paulo Paulista Avenue 🇧🇷", "pack": "latin-america",
   "words": ["skyscraper", "avenue", "billboard", "metro entrance", "banking district"]},
  {"lat": -15.7942, "lng": -47.8822, "label": "Brasília Government District 🇧🇷", "pack": "latin-america",
   "words": ["modernist building", "dome", "lawn", "congress", "brutalist architecture"]},
  {"lat": -3.7172, "lng": -38.5433, "label": "Fortaleza, Brazil 🇧🇷", "pack": "latin-america",
   "words": ["beach buggy", "sand dunes", "kite surfing", "seafront", "vendor"]},

  {"lat": -34.6037, "lng": -58.3816, "label": "Buenos Aires Plaza de Mayo 🇦🇷", "pack": "latin-america",
   "words": ["pink house", "square", "obelisk", "wide boulevard", "café"]},
  {"lat": -31.4201, "lng": -64.1888, "label": "Córdoba, Argentina 🇦🇷", "pack": "latin-america",
   "words": ["colonial building", "jesuit block", "pedestrian street", "plaza", "student quarter"]},
  {"lat": -41.1335, "lng": -71.3103, "label": "Bariloche, Argentina 🇦🇷", "pack": "latin-america",
   "words": ["alpine chalet", "lake", "mountain", "chocolate shop", "ski resort"]},

  {"lat": -33.4489, "lng": -70.6693, "label": "Santiago, Chile 🇨🇱", "pack": "latin-america",
   "words": ["Andes backdrop", "modern tower", "plaza", "fruit market", "metro"]},
  {"lat": -53.1638, "lng": -70.9171, "label": "Punta Arenas, Chile 🇨🇱", "pack": "latin-america",
   "words": ["colourful roof", "windswept", "strait", "ship", "pioneer cemetery"]},

  {"lat": 4.7110, "lng": -74.0721, "label": "Bogotá La Candelaria 🇨🇴", "pack": "latin-america",
   "words": ["colonial building", "mural", "cobblestone", "street art", "Andean backdrop"]},
  {"lat": 6.2442, "lng": -75.5812, "label": "Medellín, Colombia 🇨🇴", "pack": "latin-america",
   "words": ["cable car", "hillside barrio", "mural", "metro", "flower market"]},
  {"lat": 10.3910, "lng": -75.4794, "label": "Cartagena Old City 🇨🇴", "pack": "latin-america",
   "words": ["colonial wall", "colourful balcony", "flower vendor", "cobblestone", "horse carriage"]},
  {"lat": 1.2136, "lng": -77.2811, "label": "Pasto, Colombia 🇨🇴", "pack": "latin-america",
   "words": ["Andean market", "indigenous textiles", "cobblestone", "church", "volcano backdrop"]},

  {"lat": -0.2299, "lng": -78.5249, "label": "Quito Historic Centre 🇪🇨", "pack": "latin-america",
   "words": ["colonial church", "cobblestone", "Andean backdrop", "iron balcony", "market"]},
  {"lat": -2.9001, "lng": -79.0059, "label": "Cuenca, Ecuador 🇪🇨", "pack": "latin-america",
   "words": ["blue dome cathedral", "river", "flower market", "panama hat", "cobblestone"]},

  {"lat": -12.0464, "lng": -77.0428, "label": "Lima Miraflores 🇵🇪", "pack": "latin-america",
   "words": ["cliffside park", "Pacific Ocean", "paraglider", "seafront", "shopping mall"]},
  {"lat": -13.5170, "lng": -71.9785, "label": "Cusco Plaza de Armas 🇵🇪", "pack": "latin-america",
   "words": ["colonial arcade", "cathedral", "llama", "fountain", "Andean market"]},

  {"lat": -16.5000, "lng": -68.1193, "label": "La Paz, Bolivia 🇧🇴", "pack": "latin-america",
   "words": ["cable car", "market", "bowler hat", "adobe building", "steep street"]},

  {"lat": -25.2867, "lng": -57.6470, "label": "Asunción, Paraguay 🇵🇾", "pack": "latin-america",
   "words": ["colonial building", "palm tree", "wide street", "market", "horse cart"]},

  {"lat": 19.4326, "lng": -99.1332, "label": "Mexico City Zócalo 🇲🇽", "pack": "latin-america",
   "words": ["cathedral", "aztec ruins", "national palace", "flag", "cobblestone"]},
  {"lat": 20.9674, "lng": -89.6230, "label": "Mérida, Mexico 🇲🇽", "pack": "latin-america",
   "words": ["colonial mansion", "hammock shop", "horse carriage", "jacaranda", "plaza"]},
  {"lat": 17.0732, "lng": -96.7266, "label": "Oaxaca, Mexico 🇲🇽", "pack": "latin-america",
   "words": ["green church", "craft market", "colonial arcade", "mole restaurant", "cobblestone"]},

  {"lat": 9.9281, "lng": -84.0907, "label": "San José, Costa Rica 🇨🇷", "pack": "latin-america",
   "words": ["National Theatre", "fruit market", "oxcart", "ornate building", "taxi"]},
  {"lat": 14.0723, "lng": -87.2023, "label": "Tegucigalpa, Honduras 🇭🇳", "pack": "latin-america",
   "words": ["hillside city", "colonial church", "market", "moto-taxi", "painted wall"]},
  {"lat": 23.1136, "lng": -82.3666, "label": "Havana, Cuba 🇨🇺", "pack": "latin-america",
   "words": ["vintage car", "crumbling facade", "Malecón", "cigar shop", "balcony"]},

  # ─── ASIA ─────────────────────────────────────────────────────────────
  # Japan
  {"lat": 35.6762, "lng": 139.6503, "label": "Shibuya Crossing, Tokyo 🇯🇵", "pack": "asia",
   "words": ["scramble crossing", "neon sign", "crowd", "billboard", "skyscraper"]},
  {"lat": 35.0116, "lng": 135.7681, "label": "Gion District, Kyoto 🇯🇵", "pack": "asia",
   "words": ["wooden machiya", "lantern", "cobblestone", "geisha district", "temple gate"]},
  {"lat": 34.6937, "lng": 135.5023, "label": "Dotonbori, Osaka 🇯🇵", "pack": "asia",
   "words": ["neon billboard", "canal", "street food", "bridge", "dragon sign"]},
  {"lat": 43.0642, "lng": 141.3469, "label": "Sapporo Clock Tower 🇯🇵", "pack": "asia",
   "words": ["colonial wooden building", "clock tower", "snow street", "ginkgo tree", "tram"]},
  {"lat": 26.2124, "lng": 127.6809, "label": "Naha, Okinawa 🇯🇵", "pack": "asia",
   "words": ["Shuri Castle", "coral wall", "monorail", "Kokusai Street", "awamori shop"]},

  # China
  {"lat": 31.2304, "lng": 121.4737, "label": "The Bund, Shanghai 🇨🇳", "pack": "asia",
   "words": ["Art Deco building", "Pudong skyline", "Huangpu River", "promenade", "skyscraper"]},
  {"lat": 22.2855, "lng": 114.1577, "label": "Hong Kong Kowloon 🇭🇰", "pack": "asia",
   "words": ["neon sign", "tram", "skyscraper", "harbour", "street market"]},
  {"lat": 23.1291, "lng": 113.2644, "label": "Guangzhou, China 🇨🇳", "pack": "asia",
   "words": ["Canton tower", "dim sum restaurant", "river", "elevated highway", "market"]},
  {"lat": 30.5728, "lng": 104.0668, "label": "Chengdu Wide-Alley 🇨🇳", "pack": "asia",
   "words": ["courtyard", "teahouse", "panda decoration", "cobblestone", "snack stall"]},
  {"lat": 22.5431, "lng": 114.0579, "label": "Shenzhen, China 🇨🇳", "pack": "asia",
   "words": ["skyscraper", "tech district", "elevated walkway", "modern architecture", "billboard"]},

  # South Korea
  {"lat": 37.5665, "lng": 126.9780, "label": "Bukchon Hanok, Seoul 🇰🇷", "pack": "asia",
   "words": ["traditional hanok", "tile roof", "narrow lane", "courtyard", "fortress wall"]},
  {"lat": 35.1796, "lng": 129.0756, "label": "Busan Gamcheon Village 🇰🇷", "pack": "asia",
   "words": ["colourful hillside", "street art", "staircase", "mural", "terraced house"]},

  # Southeast Asia
  {"lat": 1.2870, "lng": 103.8550, "label": "Marina Bay Sands, Singapore 🇸🇬", "pack": "asia",
   "words": ["infinity pool", "rooftop terrace", "skyline", "lotus-shaped museum", "bay"]},
  {"lat": 3.1390, "lng": 101.6869, "label": "Kuala Lumpur KLCC 🇲🇾", "pack": "asia",
   "words": ["twin towers", "skybridge", "fountain", "park", "skyscraper"]},
  {"lat": 13.7563, "lng": 100.5018, "label": "Bangkok Old Town 🇹🇭", "pack": "asia",
   "words": ["golden temple", "tuk-tuk", "vendor cart", "spirit house", "canal boat"]},
  {"lat": 10.8231, "lng": 106.6297, "label": "Ho Chi Minh City 🇻🇳", "pack": "asia",
   "words": ["French colonial building", "motorbike swarm", "street food stall", "pagoda", "market"]},
  {"lat": 21.0278, "lng": 105.8342, "label": "Hanoi Old Quarter 🇻🇳", "pack": "asia",
   "words": ["narrow tube house", "street vendor", "lotus pond", "cyclo", "lantern"]},
  {"lat": 12.5657, "lng": 104.9910, "label": "Siem Reap, Cambodia 🇰🇭", "pack": "asia",
   "words": ["temple ruins", "tuk-tuk", "market stall", "rickshaw", "palm tree"]},
  {"lat": 16.4674, "lng": 102.8330, "label": "Khon Kaen, Thailand 🇹🇭", "pack": "asia",
   "words": ["market", "songthaew minibus", "temple gate", "food cart", "silk shop"]},
  {"lat": -6.2088, "lng": 106.8456, "label": "Jakarta Kota Tua 🇮🇩", "pack": "asia",
   "words": ["Dutch colonial building", "bicycle rental", "cobblestone", "café", "square"]},
  {"lat": -8.4095, "lng": 115.1889, "label": "Ubud, Bali 🇮🇩", "pack": "asia",
   "words": ["rice terrace", "temple gate", "offering", "coconut palm", "scooter"]},
  {"lat": 14.5995, "lng": 120.9842, "label": "Manila Intramuros 🇵🇭", "pack": "asia",
   "words": ["Spanish fortress", "cobblestone", "horse carriage", "palm tree", "cannons"]},

  # India
  {"lat": 28.6139, "lng": 77.2090, "label": "Connaught Place, New Delhi 🇮🇳", "pack": "asia",
   "words": ["colonnaded arcade", "roundabout", "auto-rickshaw", "underground metro", "vendors"]},
  {"lat": 18.9220, "lng": 72.8347, "label": "Mumbai Gateway of India 🇮🇳", "pack": "asia",
   "words": ["triumphal arch", "harbour", "double-decker bus", "colonial hotel", "ferry"]},
  {"lat": 12.9716, "lng": 77.5946, "label": "Bengaluru MG Road 🇮🇳", "pack": "asia",
   "words": ["IT corridor", "metro", "garden city", "pub", "shopping mall"]},
  {"lat": 26.9124, "lng": 75.7873, "label": "Jaipur Pink City 🇮🇳", "pack": "asia",
   "words": ["pink sandstone", "bazaar", "camel cart", "havelis", "spice market"]},
  {"lat": 22.5726, "lng": 88.3639, "label": "Kolkata Victoria Memorial 🇮🇳", "pack": "asia",
   "words": ["white marble", "tram", "park", "colonial building", "yellow taxi"]},

  # Middle East
  {"lat": 25.1972, "lng": 55.2744, "label": "Dubai Marina 🇦🇪", "pack": "asia",
   "words": ["skyscraper", "yacht", "marina", "glass tower", "waterfront promenade"]},
  {"lat": 24.4539, "lng": 54.3773, "label": "Abu Dhabi Corniche 🇦🇪", "pack": "asia",
   "words": ["seafront", "palm tree", "luxury hotel", "mosque dome", "fishing boat"]},
  {"lat": 31.7683, "lng": 35.2137, "label": "Jerusalem Old City 🇮🇱", "pack": "asia",
   "words": ["stone alley", "bazaar", "minaret", "dome", "Western Wall"]},
  {"lat": 29.3759, "lng": 47.9774, "label": "Kuwait City 🇰🇼", "pack": "asia",
   "words": ["water towers", "gulf", "mosque", "modern skyscraper", "palm-lined avenue"]},
  {"lat": 33.5138, "lng": 36.2765, "label": "Damascus Old City 🇸🇾", "pack": "asia",
   "words": ["bazaar", "Umayyad Mosque", "stone archway", "souk", "minaret"]},
  {"lat": 35.6892, "lng": 51.3890, "label": "Tehran Grand Bazaar 🇮🇷", "pack": "asia",
   "words": ["vaulted ceiling", "carpet shop", "spice stall", "archway", "domed roof"]},

  # ─── AFRICA ──────────────────────────────────────────────────────────
  {"lat": 34.0209, "lng": -6.8416, "label": "Rabat Medina, Morocco 🇲🇦", "pack": "africa",
   "words": ["medina wall", "mosaics", "souk", "minaret", "blue door"]},
  {"lat": 33.9716, "lng": -6.8498, "label": "Marrakech Jemaa el-Fna 🇲🇦", "pack": "africa",
   "words": ["market square", "snake charmer", "food stall", "fountain", "minaret"]},
  {"lat": 35.7673, "lng": 10.8395, "label": "Sousse Medina, Tunisia 🇹🇳", "pack": "africa",
   "words": ["white-washed wall", "arched gateway", "souk", "blue door", "ribat fortress"]},
  {"lat": 36.8065, "lng": 10.1815, "label": "Tunis Medina 🇹🇳", "pack": "africa",
   "words": ["arch", "carpet shop", "souk", "Ottoman architecture", "fountain"]},
  {"lat": 30.0444, "lng": 31.2357, "label": "Cairo Khan el-Khalili 🇪🇬", "pack": "africa",
   "words": ["bazaar", "lantern shop", "minaret", "coffee house", "spice stall"]},
  {"lat": 31.2001, "lng": 29.9187, "label": "Alexandria Corniche 🇪🇬", "pack": "africa",
   "words": ["Mediterranean seafront", "tram", "Ottoman fort", "café", "fishing boat"]},
  {"lat": 15.5007, "lng": 32.5599, "label": "Khartoum, Sudan 🇸🇩", "pack": "africa",
   "words": ["Nile confluence", "minaret", "market", "tea stall", "camel"]},
  {"lat": 11.8251, "lng": 42.5903, "label": "Djibouti City 🇩🇯", "pack": "africa",
   "words": ["Gulf port", "colourful building", "minaret", "market", "French colonial"]},
  {"lat": 2.0469, "lng": 45.3182, "label": "Mogadishu Beachfront 🇸🇴", "pack": "africa",
   "words": ["Indian Ocean", "minaret", "bullet-scarred building", "beach", "fishing boat"]},
  {"lat": -1.2921, "lng": 36.8219, "label": "Nairobi CBD 🇰🇪", "pack": "africa",
   "words": ["skyscraper", "matatu minibus", "roundabout", "market", "jacaranda tree"]},
  {"lat": -6.1659, "lng": 35.7497, "label": "Dodoma, Tanzania 🇹🇿", "pack": "africa",
   "words": ["parliament building", "wide avenue", "acacia tree", "red earth road", "market"]},
  {"lat": -6.7924, "lng": 39.2083, "label": "Stone Town, Zanzibar 🇹🇿", "pack": "africa",
   "words": ["carved wooden door", "coral stone wall", "narrow alley", "dhow", "spice shop"]},
  {"lat": -25.7479, "lng": 28.2293, "label": "Pretoria, South Africa 🇿🇦", "pack": "africa",
   "words": ["jacaranda boulevard", "government building", "statue", "traffic roundabout", "lawn"]},
  {"lat": -26.2041, "lng": 28.0473, "label": "Johannesburg Sandton 🇿🇦", "pack": "africa",
   "words": ["skyscraper", "mall", "taxi rank", "glass tower", "pedestrian street"]},
  {"lat": -33.9249, "lng": 18.4241, "label": "Cape Town Waterfront 🇿🇦", "pack": "africa",
   "words": ["Table Mountain", "harbour", "clock tower", "Cape Malay house", "penguin"]},
  {"lat": 5.3600, "lng": -4.0083, "label": "Abidjan Plateau 🇨🇮", "pack": "africa",
   "words": ["skyscraper", "bridge", "lagoon", "street market", "minaret"]},
  {"lat": 6.3703, "lng": 2.3912, "label": "Cotonou, Benin 🇧🇯", "pack": "africa",
   "words": ["zémidjan motorcycle taxi", "market", "voodoo shop", "lagoon", "colourful house"]},
  {"lat": 9.0579, "lng": 7.4951, "label": "Abuja, Nigeria 🇳🇬", "pack": "africa",
   "words": ["National Mosque", "wide boulevard", "rock formation", "modern building", "round-about"]},
  {"lat": 14.6937, "lng": -17.4441, "label": "Dakar, Senegal 🇸🇳", "pack": "africa",
   "words": ["Atlantic cliff", "mosque", "colourful bus", "fish market", "baobab tree"]},
  {"lat": 12.3569, "lng": -1.5353, "label": "Ouagadougou, Burkina Faso 🇧🇫", "pack": "africa",
   "words": ["moped swarm", "street vendor", "mud-brick wall", "market", "mosque"]},

  # ─── NORTH AMERICA ───────────────────────────────────────────────────
  # USA
  {"lat": 40.7128, "lng": -74.0060, "label": "Times Square, New York 🇺🇸", "pack": "north-america",
   "words": ["neon billboard", "yellow cab", "skyscraper", "pedestrian plaza", "Broadway"]},
  {"lat": 37.7749, "lng": -122.4194, "label": "San Francisco Painted Ladies 🇺🇸", "pack": "north-america",
   "words": ["Victorian house", "park", "skyline", "pastel colour", "cable car neighbourhood"]},
  {"lat": 41.8827, "lng": -87.6233, "label": "Chicago Loop 🇺🇸", "pack": "north-america",
   "words": ["L train", "skyscraper canyon", "riverwalk", "drawbridge", "Magnificent Mile"]},
  {"lat": 29.9511, "lng": -90.0715, "label": "New Orleans French Quarter 🇺🇸", "pack": "north-america",
   "words": ["iron balcony", "jazz bar", "Bourbon Street", "bead necklace", "antebellum house"]},
  {"lat": 34.0522, "lng": -118.2437, "label": "Los Angeles Downtown 🇺🇸", "pack": "north-america",
   "words": ["freeway", "palm tree", "food truck", "street art", "homeless camp"]},
  {"lat": 32.7157, "lng": -117.1611, "label": "San Diego Gaslamp Quarter 🇺🇸", "pack": "north-america",
   "words": ["Victorian building", "bar district", "palm tree", "streetcar", "trolley"]},
  {"lat": 25.7617, "lng": -80.1918, "label": "Miami South Beach 🇺🇸", "pack": "north-america",
   "words": ["Art Deco hotel", "neon sign", "palm tree", "lifeguard tower", "promenade"]},
  {"lat": 47.6062, "lng": -122.3321, "label": "Seattle Pike Place 🇺🇸", "pack": "north-america",
   "words": ["fish market", "flower stall", "neon sign", "harbour view", "hillside street"]},
  {"lat": 36.1699, "lng": -115.1398, "label": "Las Vegas Strip 🇺🇸", "pack": "north-america",
   "words": ["casino", "neon billboard", "wide boulevard", "luxury hotel", "taxi rank"]},
  {"lat": 38.9072, "lng": -77.0369, "label": "Washington DC Mall 🇺🇸", "pack": "north-america",
   "words": ["monument", "reflecting pool", "white marble", "lawn", "federal building"]},
  {"lat": 42.3601, "lng": -71.0589, "label": "Boston Freedom Trail 🇺🇸", "pack": "north-america",
   "words": ["red brick path", "colonial church", "cemetery", "cobblestone", "gas lamp"]},
  {"lat": 44.9778, "lng": -93.2650, "label": "Minneapolis, USA 🇺🇸", "pack": "north-america",
   "words": ["skyway bridge", "winter city", "light rail", "Nicollet Mall", "modern art museum"]},
  {"lat": 61.2181, "lng": -149.9003, "label": "Anchorage, Alaska 🇺🇸", "pack": "north-america",
   "words": ["mountain backdrop", "log cabin", "moose warning sign", "seaplane", "aurora sky"]},

  # Canada
  {"lat": 43.6532, "lng": -79.3832, "label": "Toronto CN Tower 🇨🇦", "pack": "north-america",
   "words": ["telecommunications tower", "waterfront", "harbour", "skyscraper", "park"]},
  {"lat": 45.5017, "lng": -73.5673, "label": "Montreal Old Port 🇨🇦", "pack": "north-america",
   "words": ["cobblestone", "Victorian building", "Ferris wheel", "river", "cyclist"]},
  {"lat": 49.2827, "lng": -123.1207, "label": "Vancouver Gastown 🇨🇦", "pack": "north-america",
   "words": ["steam clock", "cobblestone", "brick building", "mountain backdrop", "souvenir shop"]},
  {"lat": 51.0447, "lng": -114.0719, "label": "Calgary, Canada 🇨🇦", "pack": "north-america",
   "words": ["Rockies backdrop", "rodeo grounds", "+15 skyway", "oil company tower", "stampede flag"]},
  {"lat": 63.7467, "lng": -68.5170, "label": "Iqaluit, Nunavut 🇨🇦", "pack": "north-america",
   "words": ["Arctic tundra", "colourful building", "permafrost", "snowmobile", "qamutik sled"]},

  # Mexico (additional)
  {"lat": 20.6843, "lng": -88.5678, "label": "Valladolid, Mexico 🇲🇽", "pack": "north-america",
   "words": ["colourful colonial house", "cobblestone", "cenote", "hammock", "church"]},
  {"lat": 23.6345, "lng": -102.5528, "label": "Guadalajara, Mexico 🇲🇽", "pack": "north-america",
   "words": ["mariachi band", "tequila shop", "colonial arcade", "cathedral", "cobblestone"]},

  # Caribbean
  {"lat": 18.4655, "lng": -66.1057, "label": "Old San Juan, Puerto Rico 🇵🇷", "pack": "north-america",
   "words": ["cobblestone", "Spanish fort", "colourful house", "El Morro", "palm tree"]},
  {"lat": 17.2510, "lng": -88.7590, "label": "Belize City 🇧🇿", "pack": "north-america",
   "words": ["clapboard house", "waterfront", "swing bridge", "canal", "palm tree"]},

  # ─── OCEANIA ─────────────────────────────────────────────────────────
  {"lat": -33.8688, "lng": 151.2093, "label": "Sydney Opera House 🇦🇺", "pack": "oceania",
   "words": ["shell roof", "harbour", "ferry", "bridge", "Royal Botanic Garden"]},
  {"lat": -37.8136, "lng": 144.9631, "label": "Melbourne Federation Square 🇦🇺", "pack": "oceania",
   "words": ["geometric facade", "tram", "café laneways", "Yarra River", "graffiti alley"]},
  {"lat": -27.4698, "lng": 153.0251, "label": "Brisbane Southbank 🇦🇺", "pack": "oceania",
   "words": ["artificial beach", "river", "subtropical garden", "gallery", "pedestrian bridge"]},
  {"lat": -31.9505, "lng": 115.8605, "label": "Perth, Australia 🇦🇺", "pack": "oceania",
   "words": ["skyscraper", "Fremantle port", "beach suburb", "wildflower", "Bell Tower"]},
  {"lat": -12.4634, "lng": 130.8456, "label": "Darwin, Australia 🇦🇺", "pack": "oceania",
   "words": ["tropical waterfront", "night market", "mangrove", "Stokes Hill Wharf", "sunset"]},
  {"lat": -23.6980, "lng": 133.8807, "label": "Alice Springs, Australia 🇦🇺", "pack": "oceania",
   "words": ["red desert", "Todd River", "Aboriginal art gallery", "eucalyptus", "outback road"]},
  {"lat": -43.5321, "lng": 172.6362, "label": "Christchurch, New Zealand 🇳🇿", "pack": "oceania",
   "words": ["tram", "Avon River", "punting boat", "container mall", "post-earthquake rebuild"]},
  {"lat": -36.8485, "lng": 174.7633, "label": "Auckland Viaduct 🇳🇿", "pack": "oceania",
   "words": ["marina", "bar strip", "skyscraper", "harbour bridge", "ferry terminal"]},
  {"lat": -41.2865, "lng": 174.7762, "label": "Wellington Waterfront 🇳🇿", "pack": "oceania",
   "words": ["Te Papa Museum", "cable car", "waterfront", "hill suburb", "earthquake bolts"]},
  {"lat": -17.7334, "lng": 168.3220, "label": "Port Vila, Vanuatu 🇻🇺", "pack": "oceania",
   "words": ["Pacific harbour", "market stall", "kava bar", "tropical garden", "fishing boat"]},
  {"lat": -9.4438, "lng": 160.0251, "label": "Honiara, Solomon Islands 🇸🇧", "pack": "oceania",
   "words": ["central market", "betel nut stall", "tropical street", "lagoon", "outrigger canoe"]},
  {"lat": -18.1248, "lng": 178.4501, "label": "Suva, Fiji 🇫🇯", "pack": "oceania",
   "words": ["tropical market", "colourful fabric", "Hindu temple", "harbour", "colonial building"]},
  {"lat": -13.9506, "lng": -171.9667, "label": "Apia, Samoa 🇼🇸", "pack": "oceania",
   "words": ["fale hut", "palm tree", "church steeple", "market", "Pacific seafront"]},

  # ─── UNUSUAL PLACES ─────────────────────────────────────────────────
  {"lat": 64.9631, "lng": -19.0208, "label": "Geysir Hot Springs, Iceland 🇮🇸", "pack": "unusual",
   "words": ["geyser", "steam", "geothermal pool", "volcanic rock", "tourist walkway"]},
  {"lat": 78.2232, "lng": 15.6267, "label": "Longyearbyen, Svalbard 🇸🇯", "pack": "unusual",
   "words": ["Arctic town", "polar bear warning sign", "wooden houses", "snowmobile", "permafrost"]},
  {"lat": -77.8460, "lng": 166.6863, "label": "McMurdo Station, Antarctica 🇦🇶", "pack": "unusual",
   "words": ["research station", "ice runway", "cargo container", "snow", "Mount Erebus"]},
  {"lat": 0.0000, "lng": -90.3000, "label": "Puerto Ayora, Galápagos 🇪🇨", "pack": "unusual",
   "words": ["giant tortoise", "blue-footed booby", "lava rock", "research station", "boat"]},
  {"lat": -54.8019, "lng": -68.3030, "label": "Ushuaia, Argentina 🇦🇷", "pack": "unusual",
   "words": ["fin del mundo", "channel", "mountain", "snow cap", "colourful house"]},
  {"lat": 28.2937, "lng": -16.6291, "label": "Teide National Park, Tenerife 🇪🇸", "pack": "unusual",
   "words": ["volcano", "lunar landscape", "cable car", "lava field", "crater"]},
  {"lat": 27.1127, "lng": -13.1867, "label": "Dakhla, Western Sahara 🇲🇦", "pack": "unusual",
   "words": ["sandbar peninsula", "kite surfing", "desert", "Atlantic", "fishing village"]},
  {"lat": 13.5137, "lng": 2.1098, "label": "Niamey, Niger 🇳🇪", "pack": "unusual",
   "words": ["Niger River", "camel", "mud-brick market", "oil drum boat", "moped taxi"]},
  {"lat": -21.1789, "lng": 55.5128, "label": "Saint-Denis, Réunion 🇷🇪", "pack": "unusual",
   "words": ["Creole house", "loukoum shop", "volcano backdrop", "market", "Kreol architecture"]},
  {"lat": 4.1755, "lng": 73.5093, "label": "Malé, Maldives 🇲🇻", "pack": "unusual",
   "words": ["densely packed building", "coral mosque", "harbour", "ferry jetty", "ocean horizon"]},
  {"lat": -20.1609, "lng": 57.4983, "label": "Port Louis, Mauritius 🇲🇺", "pack": "unusual",
   "words": ["Caudan Waterfront", "Creole market", "lighthouse", "Chinatown sign", "port"]},
  {"lat": 47.0105, "lng": 28.8638, "label": "Chișinău, Moldova 🇲🇩", "pack": "unusual",
   "words": ["Soviet-era building", "park alley", "wine country sign", "trolleybus", "abandoned kiosk"]},
  {"lat": 41.7151, "lng": 44.8271, "label": "Tbilisi Old Town, Georgia 🇬🇪", "pack": "unusual",
   "words": ["carved wooden balcony", "sulfur bath", "Mtkvari River", "cliff church", "colourful house"]},
  {"lat": 40.1431, "lng": 47.5769, "label": "Sheki, Azerbaijan 🇦🇿", "pack": "unusual",
   "words": ["Silk Road caravanserai", "stained glass", "mountain valley", "walnut shop", "fortress"]},
  {"lat": 39.9334, "lng": 32.8597, "label": "Ankara Citadel, Turkey 🇹🇷", "pack": "unusual",
   "words": ["ancient fortress wall", "anatolian craft shop", "rooftop view", "mosque", "cobblestone"]},
  {"lat": 36.2021, "lng": 37.1343, "label": "Aleppo Old City, Syria 🇸🇾", "pack": "unusual",
   "words": ["citadel", "covered souk", "ancient mosaic", "rubble", "rebuilding"]},
  {"lat": -8.8383, "lng": 13.2344, "label": "Luanda, Angola 🇦🇴", "pack": "unusual",
   "words": ["Ilha promenade", "Portuguese colonial", "Atlantic", "colourful building", "fishing boat"]},
  {"lat": -18.9161, "lng": 47.5361, "label": "Antananarivo, Madagascar 🇲🇬", "pack": "unusual",
   "words": ["terracotta house", "rice paddy", "church spire", "hillside staircase", "market"]},
  {"lat": 15.5528, "lng": 32.5324, "label": "Omdurman Market, Sudan 🇸🇩", "pack": "unusual",
   "words": ["gold bazaar", "Nile bank", "camel market", "whirling dervish", "mud-brick mosque"]},
  {"lat": -15.4167, "lng": 28.2833, "label": "Lusaka, Zambia 🇿🇲", "pack": "unusual",
   "words": ["market", "Independence Avenue", "jacaranda tree", "minibus", "wire sculpture"]},
]

def build_packs(locations):
    packs = {}
    for loc in locations:
        p = loc["pack"]
        if p not in packs:
            packs[p] = []
        entry = {k: v for k, v in loc.items() if k != "pack"}
        packs[p].append(entry)
    return packs

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base, "data")
    packs_dir = os.path.join(data_dir, "packs")
    os.makedirs(packs_dir, exist_ok=True)

    # Master list (no pack key)
    master = [{k: v for k, v in loc.items() if k != "pack"} for loc in LOCATIONS]
    master_path = os.path.join(data_dir, "locations.json")
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print(f"✅ locations.json — {len(master)} locations")

    # Themed packs
    packs = build_packs(LOCATIONS)
    pack_labels = {
        "europe": "🌍 Europe",
        "latin-america": "🌎 Latin America",
        "asia": "🌏 Asia & Middle East",
        "africa": "🌍 Africa",
        "north-america": "🌎 North America",
        "oceania": "🌏 Oceania & Pacific",
        "unusual": "🗺️ Unusual Places",
    }
    for pack_key, locs in packs.items():
        pack_data = {
            "id": pack_key,
            "label": pack_labels.get(pack_key, pack_key.title()),
            "locations": locs,
        }
        pack_path = os.path.join(packs_dir, f"{pack_key}.json")
        with open(pack_path, "w", encoding="utf-8") as f:
            json.dump(pack_data, f, ensure_ascii=False, indent=2)
        print(f"  📦 {pack_key}.json — {len(locs)} locations")

    print(f"\n🌐 Total: {len(master)} locations across {len(packs)} packs")

if __name__ == "__main__":
    main()
