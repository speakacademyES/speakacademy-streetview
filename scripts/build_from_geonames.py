#!/usr/bin/env python3
"""
Build Street View location database from GeoNames cities15000.txt
Target: ~450 globally balanced locations across 7 themed packs
Avoids over-indexing on famous capitals; prefers variety.
"""
import csv, json, os, random

GEONAMES_FILE = "/tmp/cities1000.txt"

# GeoNames tab-separated columns (0-indexed)
# 0:id 1:name 2:asciiname 3:altnames 4:lat 5:lng 6:feat_class 7:feat_code
# 8:country 9:cc2 10:admin1 11:admin2 12:admin3 13:admin4
# 14:population 15:elevation 16:dem 17:timezone 18:modification_date

# Country → continent mapping
CONTINENT = {
    # Europe
    "AD":"EU","AL":"EU","AT":"EU","BA":"EU","BE":"EU","BG":"EU","BY":"EU",
    "CH":"EU","CY":"EU","CZ":"EU","DE":"EU","DK":"EU","EE":"EU","ES":"EU",
    "FI":"EU","FR":"EU","GB":"EU","GR":"EU","HR":"EU","HU":"EU","IE":"EU",
    "IS":"EU","IT":"EU","LI":"EU","LT":"EU","LU":"EU","LV":"EU","MC":"EU",
    "MD":"EU","ME":"EU","MK":"EU","MT":"EU","NL":"EU","NO":"EU","PL":"EU",
    "PT":"EU","RO":"EU","RS":"EU","RU":"EU","SE":"EU","SI":"EU","SK":"EU",
    "SM":"EU","UA":"EU","VA":"EU","XK":"EU","GE":"EU","AM":"EU","AZ":"EU",
    # Asia
    "AE":"AS","AF":"AS","BD":"AS","BH":"AS","BN":"AS","BT":"AS","CN":"AS",
    "HK":"AS","ID":"AS","IL":"AS","IN":"AS","IQ":"AS","IR":"AS","JO":"AS",
    "JP":"AS","KG":"AS","KH":"AS","KP":"AS","KR":"AS","KW":"AS","KZ":"AS",
    "LA":"AS","LB":"AS","LK":"AS","MM":"AS","MN":"AS","MO":"AS","MV":"AS",
    "MY":"AS","NP":"AS","OM":"AS","PH":"AS","PK":"AS","PS":"AS","QA":"AS",
    "SA":"AS","SG":"AS","SY":"AS","TH":"AS","TJ":"AS","TL":"AS","TM":"AS",
    "TR":"AS","TW":"AS","UZ":"AS","VN":"AS","YE":"AS",
    # Africa
    "AO":"AF","BF":"AF","BI":"AF","BJ":"AF","BW":"AF","CD":"AF","CF":"AF",
    "CG":"AF","CI":"AF","CM":"AF","CV":"AF","DJ":"AF","DZ":"AF","EG":"AF",
    "ER":"AF","ET":"AF","GA":"AF","GH":"AF","GM":"AF","GN":"AF","GQ":"AF",
    "GW":"AF","KE":"AF","KM":"AF","LR":"AF","LS":"AF","LY":"AF","MA":"AF",
    "MG":"AF","ML":"AF","MR":"AF","MU":"AF","MW":"AF","MZ":"AF","NA":"AF",
    "NE":"AF","NG":"AF","RE":"AF","RW":"AF","SC":"AF","SD":"AF","SL":"AF",
    "SN":"AF","SO":"AF","SS":"AF","ST":"AF","SZ":"AF","TD":"AF","TG":"AF",
    "TN":"AF","TZ":"AF","UG":"AF","ZA":"AF","ZM":"AF","ZW":"AF","EH":"AF",
    # North America
    "AG":"NA","BB":"NA","BL":"NA","BS":"NA","BZ":"NA","CA":"NA","CR":"NA",
    "CU":"NA","DM":"NA","DO":"NA","GD":"NA","GL":"NA","GT":"NA","HN":"NA",
    "HT":"NA","JM":"NA","KN":"NA","LC":"NA","MF":"NA","MX":"NA","NI":"NA",
    "PA":"NA","PM":"NA","PR":"NA","SV":"NA","TT":"NA","US":"NA","VC":"NA",
    "VG":"NA","VI":"NA",
    # South America
    "AR":"SA","BO":"SA","BR":"SA","CL":"SA","CO":"SA","EC":"SA","FK":"SA",
    "GF":"SA","GY":"SA","PE":"SA","PY":"SA","SR":"SA","UY":"SA","VE":"SA",
    # Oceania
    "AU":"OC","FJ":"OC","FM":"OC","GU":"OC","KI":"OC","MH":"OC","MP":"OC",
    "NC":"OC","NR":"OC","NZ":"OC","PF":"OC","PG":"OC","PW":"OC","SB":"OC",
    "TO":"OC","TV":"OC","VU":"OC","WF":"OC","WS":"OC",
}

# Continent targets (~1,400 from GeoNames + 193 curated = ~1,600 total)
TARGETS = {
    "EU": 420,  # excellent Street View coverage
    "AS": 310,
    "NA": 180,
    "SA": 180,
    "AF": 230,
    "OC": 100,
}

# Country → flag emoji
FLAGS = {
    "AD":"🇦🇩","AE":"🇦🇪","AF":"🇦🇫","AL":"🇦🇱","AM":"🇦🇲","AO":"🇦🇴","AR":"🇦🇷",
    "AT":"🇦🇹","AU":"🇦🇺","AZ":"🇦🇿","BA":"🇧🇦","BB":"🇧🇧","BD":"🇧🇩","BE":"🇧🇪",
    "BF":"🇧🇫","BG":"🇧🇬","BH":"🇧🇭","BI":"🇧🇮","BJ":"🇧🇯","BL":"🇧🇱","BN":"🇧🇳",
    "BO":"🇧🇴","BR":"🇧🇷","BS":"🇧🇸","BT":"🇧🇹","BW":"🇧🇼","BY":"🇧🇾","BZ":"🇧🇿",
    "CA":"🇨🇦","CD":"🇨🇩","CF":"🇨🇫","CG":"🇨🇬","CH":"🇨🇭","CI":"🇨🇮","CL":"🇨🇱",
    "CM":"🇨🇲","CN":"🇨🇳","CO":"🇨🇴","CR":"🇨🇷","CU":"🇨🇺","CV":"🇨🇻","CY":"🇨🇾",
    "CZ":"🇨🇿","DE":"🇩🇪","DJ":"🇩🇯","DK":"🇩🇰","DO":"🇩🇴","DZ":"🇩🇿","EC":"🇪🇨",
    "EG":"🇪🇬","EH":"🇪🇭","ER":"🇪🇷","ES":"🇪🇸","ET":"🇪🇹","FI":"🇫🇮","FJ":"🇫🇯",
    "FR":"🇫🇷","GA":"🇬🇦","GB":"🇬🇧","GE":"🇬🇪","GH":"🇬🇭","GL":"🇬🇱","GM":"🇬🇲",
    "GN":"🇬🇳","GQ":"🇬🇶","GR":"🇬🇷","GT":"🇬🇹","GW":"🇬🇼","GY":"🇬🇾","HK":"🇭🇰",
    "HN":"🇭🇳","HR":"🇭🇷","HT":"🇭🇹","HU":"🇭🇺","ID":"🇮🇩","IE":"🇮🇪","IL":"🇮🇱",
    "IN":"🇮🇳","IQ":"🇮🇶","IR":"🇮🇷","IS":"🇮🇸","IT":"🇮🇹","JM":"🇯🇲","JO":"🇯🇴",
    "JP":"🇯🇵","KE":"🇰🇪","KG":"🇰🇬","KH":"🇰🇭","KR":"🇰🇷","KW":"🇰🇼","KZ":"🇰🇿",
    "LA":"🇱🇦","LB":"🇱🇧","LK":"🇱🇰","LR":"🇱🇷","LS":"🇱🇸","LT":"🇱🇹","LU":"🇱🇺",
    "LV":"🇱🇻","LY":"🇱🇾","MA":"🇲🇦","MD":"🇲🇩","ME":"🇲🇪","MG":"🇲🇬","MK":"🇲🇰",
    "ML":"🇲🇱","MM":"🇲🇲","MN":"🇲🇳","MO":"🇲🇴","MR":"🇲🇷","MT":"🇲🇹","MU":"🇲🇺",
    "MV":"🇲🇻","MW":"🇲🇼","MX":"🇲🇽","MY":"🇲🇾","MZ":"🇲🇿","NA":"🇳🇦","NE":"🇳🇪",
    "NG":"🇳🇬","NI":"🇳🇮","NL":"🇳🇱","NO":"🇳🇴","NP":"🇳🇵","NR":"🇳🇷","NZ":"🇳🇿",
    "OM":"🇴🇲","PA":"🇵🇦","PE":"🇵🇪","PG":"🇵🇬","PH":"🇵🇭","PK":"🇵🇰","PL":"🇵🇱",
    "PR":"🇵🇷","PS":"🇵🇸","PT":"🇵🇹","PW":"🇵🇼","PY":"🇵🇾","QA":"🇶🇦","RE":"🇷🇪",
    "RO":"🇷🇴","RS":"🇷🇸","RU":"🇷🇺","RW":"🇷🇼","SA":"🇸🇦","SB":"🇸🇧","SC":"🇸🇨",
    "SD":"🇸🇩","SE":"🇸🇪","SG":"🇸🇬","SI":"🇸🇮","SK":"🇸🇰","SL":"🇸🇱","SN":"🇸🇳",
    "SO":"🇸🇴","SR":"🇸🇷","SS":"🇸🇸","ST":"🇸🇹","SV":"🇸🇻","SY":"🇸🇾","SZ":"🇸🇿",
    "TD":"🇹🇩","TG":"🇹🇬","TH":"🇹🇭","TJ":"🇹🇯","TL":"🇹🇱","TM":"🇹🇲","TN":"🇹🇳",
    "TR":"🇹🇷","TT":"🇹🇹","TV":"🇹🇻","TW":"🇹🇼","TZ":"🇹🇿","UA":"🇺🇦","UG":"🇺🇬",
    "US":"🇺🇸","UY":"🇺🇾","UZ":"🇺🇿","VA":"🇻🇦","VE":"🇻🇪","VN":"🇻🇳","VU":"🇻🇺",
    "WS":"🇼🇸","XK":"🇽🇰","YE":"🇾🇪","ZA":"🇿🇦","ZM":"🇿🇲","ZW":"🇿🇼",
}

# Vocabulary words by continent (generic urban Street View vocabulary)
VOCAB_BY_CONTINENT = {
    "EU": [
        ["cobblestone street", "tram", "café terrace", "church spire", "bicycle lane"],
        ["old town square", "market stall", "apartment block", "pedestrian zone", "fountain"],
        ["canal", "bridge", "baroque church", "bell tower", "colourful facade"],
        ["railway station", "tramline", "roundabout", "castle", "town hall"],
        ["medieval wall", "arch", "monastery", "vineyard hillside", "waterfront"],
    ],
    "AS": [
        ["temple", "street food stall", "motorbike", "neon sign", "market"],
        ["skyscraper", "harbour", "rickshaw", "lantern", "traditional roof"],
        ["mosque", "bazaar", "alley", "spice market", "minaret"],
        ["rice field", "palm tree", "wooden house", "canal boat", "vendor cart"],
        ["elevated highway", "cable car", "fish market", "pagoda", "street art"],
    ],
    "NA": [
        ["pickup truck", "strip mall", "gas station", "parking lot", "wide boulevard"],
        ["colonial building", "cobblestone", "plaza", "horse carriage", "market stall"],
        ["beach promenade", "palm tree", "surf shop", "seafront hotel", "ice cream stand"],
        ["downtown skyscraper", "yellow cab", "fire hydrant", "walk signal", "diner"],
        ["wooden house", "church steeple", "grain silo", "railroad crossing", "small-town diner"],
    ],
    "SA": [
        ["colonial church", "cobblestone", "plaza", "market", "mural"],
        ["hillside barrio", "cable car", "colourful house", "street vendor", "bus terminal"],
        ["beach promenade", "fishing boat", "seafront", "palm tree", "kiosk"],
        ["Andean village", "adobe wall", "market", "llama", "mountain backdrop"],
        ["favela staircase", "bougainvillea", "football court", "moto-taxi", "concrete block"],
    ],
    "AF": [
        ["market stall", "minaret", "mud-brick wall", "motorbike taxi", "colourful bus"],
        ["fish market", "beach", "fishing boat", "palm tree", "corrugated iron roof"],
        ["colonial building", "wide boulevard", "jacaranda tree", "roundabout", "taxi rank"],
        ["souk", "carved door", "arch", "carpet shop", "narrow alley"],
        ["village hut", "red earth road", "baobab tree", "water pump", "children playing"],
    ],
    "OC": [
        ["beach", "surf shop", "blue sky", "bungalow", "garden"],
        ["harbour", "ferry", "skyscraper", "park", "botanic garden"],
        ["outback road", "eucalyptus", "red earth", "roadhouse", "cattle grid"],
        ["island seafront", "palm tree", "coral reef", "diving shop", "beach bar"],
        ["vineyard", "winery", "rolling hills", "farmhouse", "sheep paddock"],
    ],
}

# Countries with known poor/no Street View coverage (skip or reduce weight)
LOW_COVERAGE = {
    "SO","SS","CF","TD","ER","KP","TM","NR","TV","KI","MH","PW",
    "GW","SL","LR","GN","GM","MR",
}

# Countries to limit to 1-2 cities max (avoid over-indexing large nations)
CAP_COUNTRIES = {
    "US":60,"CN":40,"IN":40,"RU":30,"BR":45,"AU":28,
    "DE":22,"GB":28,"FR":22,"IT":22,"ES":28,"CA":22,
    "MX":28,"JP":28,"KR":18,"TR":18,"ID":15,"PK":12,
    "NG":12,"ZA":18,"AR":22,"CO":18,"PL":15,"UA":15,
    "NL":12,"BE":9,"PT":12,"GR":12,"SE":12,"NO":9,
    "FI":9,"DK":9,"CZ":9,"HU":9,"RO":12,"TH":12,
    "VN":12,"MY":9,"PH":12,"CL":12,"PE":12,"EC":9,
    "MA":12,"EG":12,"KE":9,"TZ":8,"GH":8,"ET":8,
    "DZ":9,"TN":8,"LY":5,"SD":6,"SN":6,"CM":6,
    "CI":6,"AO":6,"MZ":6,"MW":6,"ZM":6,"ZW":6,
    "BO":8,"PY":6,"UY":8,"VE":12,"CU":8,"DO":6,
    "GT":6,"HN":6,"SV":5,"CR":6,"PA":6,"NI":6,
    "IQ":8,"IR":12,"SA":12,"YE":3,"SY":3,"LB":6,
    "JO":6,"IL":8,"KW":5,"QA":5,"OM":6,"BH":3,
    "KZ":9,"UZ":8,"AZ":6,"GE":6,"AM":5,"TM":3,
    "BD":12,"LK":8,"NP":8,"MM":8,"KH":6,"LA":5,
    "MN":5,"AF":3,"RS":6,"HR":6,"BA":5,"SI":5,
    "BG":6,"SK":5,"EE":4,"LV":4,"LT":4,"IS":4,
    "NZ":9,"SG":4,"HK":4,"TW":6,
}
DEFAULT_CAP = 5

def get_continent(cc):
    return CONTINENT.get(cc, None)

def get_flag(cc):
    return FLAGS.get(cc, "🌍")

VOCAB_BY_FEAT = {
    "PPLC": [["government building", "main square", "national flag", "parliament", "wide avenue"]],
    "PPLS": [["harbour", "beach", "promenade", "fishing boat", "seafront café"]],
    "PPLR": [["village square", "church", "farmhouse", "local market", "country road"]],
}

def get_words(continent, feat="PPL"):
    feat_pool = VOCAB_BY_FEAT.get(feat)
    if feat_pool and random.random() < 0.4:
        return random.choice(feat_pool)
    pool = VOCAB_BY_CONTINENT.get(continent, VOCAB_BY_CONTINENT["EU"])
    return random.choice(pool)

def get_pack_id(continent):
    mapping = {
        "EU": "europe",
        "AS": "asia",
        "NA": "north-america",
        "SA": "latin-america",
        "AF": "africa",
        "OC": "oceania",
    }
    return mapping.get(continent, "unusual")

def load_cities(filepath):
    cities = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 15:
                continue
            try:
                name    = parts[1]
                lat     = float(parts[4])
                lng     = float(parts[5])
                cc      = parts[8]
                pop     = int(parts[14]) if parts[14] else 0
                feat    = parts[7]
            except (ValueError, IndexError):
                continue

            continent = get_continent(cc)
            if not continent:
                continue
            if cc in LOW_COVERAGE:
                continue
            if pop < 10000:
                continue

            cities.append({
                "name": name, "lat": lat, "lng": lng, "cc": cc,
                "pop": pop, "feat": feat, "continent": continent,
            })
    return cities

def select_balanced(cities, targets):
    random.seed(42)

    # Group by continent
    by_continent = {}
    for c in cities:
        cont = c["continent"]
        by_continent.setdefault(cont, []).append(c)

    # Sort each continent group: shuffle within population tiers to avoid
    # always picking the biggest city in each country
    selected = []
    for cont, target in targets.items():
        pool = by_continent.get(cont, [])
        if not pool:
            continue

        # Sort by population descending; take top 5x target as candidates
        pool.sort(key=lambda x: x["pop"], reverse=True)
        candidates = pool[:target * 5]
        random.shuffle(candidates)

        country_counts = {}
        picked = []
        for city in candidates:
            cc = city["cc"]
            cap = CAP_COUNTRIES.get(cc, DEFAULT_CAP)
            if country_counts.get(cc, 0) >= cap:
                continue
            country_counts[cc] = country_counts.get(cc, 0) + 1
            picked.append(city)
            if len(picked) >= target:
                break

        selected.extend(picked)

    return selected

def build_location(city):
    cont = city["continent"]
    flag = get_flag(city["cc"])
    pack = get_pack_id(cont)
    words = get_words(cont, city.get("feat", "PPL"))
    return {
        "lat": round(city["lat"], 4),
        "lng": round(city["lng"], 4),
        "label": f"{city['name']}, {city['cc']} {flag}",
        "pack": pack,
        "words": words,
    }

def main():
    print("Loading GeoNames data…")
    cities = load_cities(GEONAMES_FILE)
    print(f"  Loaded {len(cities):,} eligible cities")

    selected = select_balanced(cities, TARGETS)
    print(f"  Selected {len(selected)} cities")

    locations = [build_location(c) for c in selected]
    random.shuffle(locations)

    base      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir  = os.path.join(base, "data")
    packs_dir = os.path.join(data_dir, "packs")
    os.makedirs(packs_dir, exist_ok=True)

    # --- Merge with handcrafted locations (keep the good manual ones) ---
    manual_path = os.path.join(data_dir, "locations_curated.json")
    manual = []
    if os.path.exists(manual_path):
        with open(manual_path) as f:
            manual = json.load(f)
        print(f"  Merging {len(manual)} curated locations")

    all_locs = manual + locations

    # Master file (no pack key)
    master = [{k: v for k, v in loc.items() if k != "pack"} for loc in all_locs]
    master_path = os.path.join(data_dir, "locations.json")
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print(f"\n✅ locations.json — {len(master)} total locations")

    # Pack files
    pack_labels = {
        "europe":        "🌍 Europe",
        "latin-america": "🌎 Latin America",
        "asia":          "🌏 Asia & Middle East",
        "africa":        "🌍 Africa",
        "north-america": "🌎 North America",
        "oceania":       "🌏 Oceania & Pacific",
        "unusual":       "🗺️ Unusual Places",
    }
    packs = {}
    for loc in all_locs:
        p = loc.get("pack", "unusual")
        packs.setdefault(p, []).append({k: v for k, v in loc.items() if k != "pack"})

    for pack_key, locs in packs.items():
        pack_data = {
            "id":        pack_key,
            "label":     pack_labels.get(pack_key, pack_key.title()),
            "locations": locs,
        }
        pack_path = os.path.join(packs_dir, f"{pack_key}.json")
        with open(pack_path, "w", encoding="utf-8") as f:
            json.dump(pack_data, f, ensure_ascii=False, indent=2)
        print(f"  📦 {pack_key}.json — {len(locs)} locations")

    print(f"\n🌐 Grand total: {len(all_locs)} locations across {len(packs)} packs")

if __name__ == "__main__":
    main()
