"""
Filter RERA properties within 4km of Namma Metro Purple Line stations.
Uses hardcoded locality → coordinate mapping for Bangalore South areas
(no external API needed).

Outputs:
  rera_near_purple_line.csv
  rera_purple_line_map.html   (open in any browser)
"""

import math, re, csv
import pandas as pd

# ── Purple Line station coordinates ─────────────────────────────────────────
PURPLE_LINE_STATIONS = [
    ("Vijayanagar",        12.9617, 77.5293),
    ("Attiguppe",          12.9448, 77.5201),
    ("Deepanjali Nagar",   12.9491, 77.5261),
    ("Mysore Road",        12.9576, 77.5353),
    ("Yelachenahalli",     12.9063, 77.5765),
    ("Konanakunte Cross",  12.8919, 77.5634),
    ("Doddakallasandra",   12.8774, 77.5483),
    ("Vajrahalli",         12.8618, 77.5309),
    ("Thalaghattapura",    12.8479, 77.5147),
    ("Silk Institute",     12.8373, 77.5014),
    ("Kengeri",            12.8274, 77.4822),
]

THRESHOLD_KM = 4.0

# ── Known locality → (lat, lon) for Bangalore South ─────────────────────────
# Covers every distinct area that appears in the dataset
LOCALITY_COORDS = {
    # JP Nagar / Jayanagar – near Yelachenahalli
    "jayanagar":                  (12.9279, 77.5848),
    "jp nagar":                   (12.9063, 77.5765),
    "j p nagar":                  (12.9063, 77.5765),
    "puttenahalli":               (12.9022, 77.5796),
    "sarakki":                    (12.9068, 77.5755),
    "arekere":                    (12.8990, 77.5820),
    "kothanur":                   (12.8989, 77.5780),
    "kothanuru":                  (12.8989, 77.5780),
    "banashankari":               (12.9267, 77.5609),
    "subramanyapura":             (12.9100, 77.5530),
    "raghuvanahalli":             (12.8873, 77.5588),
    "talagattapura":              (12.8479, 77.5147),
    "talaghattapura":             (12.8479, 77.5147),
    "thalaghattapura":            (12.8479, 77.5147),
    "tallaghattapura":            (12.8479, 77.5147),

    # Uttarahalli Hobli (central belt – near Doddakallasandra/Vajrahalli)
    "uttarahalli":                (12.8900, 77.5500),
    "uttrahalli":                 (12.8900, 77.5500),
    "uttarahali":                 (12.8900, 77.5500),
    "kembattahalli":              (12.8802, 77.5463),
    "kembathahalli":              (12.8802, 77.5463),
    "kembathalli":                (12.8802, 77.5463),
    "hosakerehalli":              (12.8862, 77.5408),
    "gollahalli":                 (12.8650, 77.5295),
    "tharalu":                    (12.8510, 77.5170),
    "areahalli":                  (12.8860, 77.5540),
    "channasandra":               (12.8930, 77.5480),
    "channsandra":                (12.8930, 77.5480),
    "sarakkikere":                (12.9068, 77.5755),
    "thurahalli":                 (12.9050, 77.5540),
    "mallasandra":                (12.8590, 77.5050),
    "gottigere":                  (12.8692, 77.5927),   # near Bannerghatta, outside 4km
    "jaranganahalli":             (12.8740, 77.5300),
    "gublala":                    (12.8790, 77.5400),
    "javaregowda doddi":          (12.8862, 77.5408),
    "vajarahalli":                (12.8618, 77.5309),
    "vajrahalli":                 (12.8618, 77.5309),
    "kaggalipura":                (12.8120, 77.5020),   # far south on Kanakapura
    "ragam gardens":              (12.8700, 77.6100),

    # Kengeri Hobli – near Silk Institute/Kengeri
    "kengeri":                    (12.8274, 77.4822),
    "hemmigepura":                (12.8500, 77.5050),
    "mylasandra":                 (12.8400, 77.4950),
    "patanagere":                 (12.8430, 77.5030),
    "kenchanapura":               (12.8438, 77.5005),
    "kenchenahalli":              (12.8570, 77.5020),
    "doddabele":                  (12.8500, 77.4720),
    "kumbalgodu":                 (12.8630, 77.4680),
    "kumbalagodu":                (12.8630, 77.4680),
    "sulikere":                   (12.8350, 77.4800),
    "gnanabharathi":              (12.9100, 77.5150),
    "r.r.nagar":                  (12.9290, 77.5150),
    "rr nagar":                   (12.9290, 77.5150),
    "rajarajeshwari nagar":       (12.9600, 77.5000),
    "rajarajeshwarinagar":        (12.9600, 77.5000),
    "maligondanahalli":           (12.8380, 77.4950),
    "kambipura":                  (12.8830, 77.5040),
    "venkatapura":                (12.8480, 77.4850),
    "gangasandra":                (12.8400, 77.4900),
    "chudenapura":                (12.8450, 77.4840),
    "thagachiguppe":              (12.8200, 77.4700),
    "ganakallu":                  (12.8350, 77.4900),
    "haralukunte":                (12.8850, 77.6180),   # Begur Hobli, far
    "singasandra":                (12.8730, 77.6170),   # far

    # Begur Hobli – southeast, generally outside 4km Purple Line
    "begur":                      (12.8700, 77.6180),
    "naganathapura":              (12.8760, 77.6100),
    "doddanagamangala":           (12.8580, 77.6530),
    "basapura":                   (12.8780, 77.6150),
    "konappana agrahara":         (12.8780, 77.6150),
    "kammanahalli":               (12.8850, 77.6130),
    "yelenahalli":                (12.8870, 77.6210),   # Begur Hobli yelenahalli ≠ yelachenahalli station
    "bilekahalli":                (12.8890, 77.6050),
    "parappana agrahara":         (12.8720, 77.6270),
    "bommanahalli":               (12.8960, 77.6220),
    "jakkasandra":                (12.9120, 77.6280),   # near Sarjapura, far
    "roopena agrahara":           (12.8800, 77.6140),
    "yellukunte":                 (12.8730, 77.6190),
    "beretena agrahara":          (12.8740, 77.6100),

    # Tavarekere Hobli – far south/west
    "tavarekere":                 (12.8300, 77.5550),
    "taverekere":                 (12.8300, 77.5550),
    "dodderi":                    (12.8350, 77.5650),
    "byalalu":                    (12.8150, 77.5580),
    "muddayanapalya":             (12.8400, 77.5470),
    "muddayyanapalya":            (12.8400, 77.5470),

    # Far southeast – Sarjapura, Anekal, Attibele
    "sarjapura":                  (12.8800, 77.7100),
    "attibele":                   (12.7900, 77.7500),
    "anekal":                     (12.7100, 77.6900),
    "kudlu":                      (12.8770, 77.6600),

    # Bidarahalli – east Bangalore
    "bidarahalli":                (12.9850, 77.7450),

    # Other specific places
    "koramangala":                (12.9279, 77.6271),
    "btm layout":                 (12.9140, 77.6101),
    "electronic city":            (12.8399, 77.6770),
    "hulimavu":                   (12.8900, 77.6080),
    "adugodi":                    (12.9313, 77.6098),
    "sudamanagara":               (12.9200, 77.5750),
    "indiranagar":                (12.9719, 77.6412),
    "whitefield":                 (12.9698, 77.7499),
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d = math.radians
    a = math.sin(d(lat2-lat1)/2)**2 + math.cos(d(lat1))*math.cos(d(lat2))*math.sin(d(lon2-lon1)/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def nearest_station(lat, lon):
    best = min(PURPLE_LINE_STATIONS, key=lambda s: haversine(lat, lon, s[1], s[2]))
    return best[0], round(haversine(lat, lon, best[1], best[2]), 2)

def resolve_coords(address):
    """
    Match the address string against known localities (longest match wins).
    Returns (lat, lon, matched_locality) or (None, None, None).
    """
    addr_lower = address.lower()
    best_match, best_coords, best_len = None, None, 0
    for locality, coords in LOCALITY_COORDS.items():
        if locality in addr_lower and len(locality) > best_len:
            best_match = locality
            best_coords = coords
            best_len = len(locality)
    if best_coords:
        return best_coords[0], best_coords[1], best_match
    return None, None, None

def parse_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            p = line.split("\t")
            while len(p) < 10:
                p.append("")
            rows.append({
                "Sl No":           p[0].strip(),
                "Project Name":    p[1].strip(),
                "Promoter":        p[2].strip(),
                "Completion Date": p[3].strip(),
                "Extension 1":     p[4].strip(),
                "Extension 2":     p[5].strip(),
                "Extension 3":     p[6].strip(),
                "Address":         p[7].strip(),
                "Area (sqm)":      p[8].strip(),
                "Units":           p[9].strip(),
            })
    return rows

def main():
    rows = parse_tsv("rera_raw.tsv")
    print(f"[*] {len(rows)} properties loaded.\n")

    all_results, no_match = [], []

    for row in rows:
        addr = row["Address"]
        lat, lon, matched = resolve_coords(addr)
        if lat is None:
            no_match.append(row)
            continue
        station, dist_km = nearest_station(lat, lon)
        within = dist_km <= THRESHOLD_KM
        row.update({
            "Matched Locality": matched,
            "Lat": lat, "Lon": lon,
            "Nearest Metro Station": station,
            "Distance to Metro (km)": dist_km,
            "Within 4km": "Yes" if within else "No",
            "Google Maps": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}",
        })
        status = "✓" if within else "✗"
        print(f"  {status} {row['Project Name'][:42]:42s} | {matched:22s} | {station} ({dist_km:.1f} km)")
        all_results.append(row)

    qualified = [r for r in all_results if r["Within 4km"] == "Yes"]

    # ── CSV output ────────────────────────────────────────────────────────
    cols = ["Sl No","Project Name","Promoter","Completion Date","Extension 1",
            "Extension 2","Extension 3","Address","Area (sqm)","Units",
            "Matched Locality","Nearest Metro Station","Distance to Metro (km)",
            "Within 4km","Google Maps"]

    df_all = pd.DataFrame(all_results, columns=[c for c in cols if c in all_results[0]])
    df_all.to_csv("rera_all_with_distances.csv", index=False, encoding="utf-8-sig")

    df_near = pd.DataFrame(qualified, columns=[c for c in cols if c in qualified[0]])
    df_near = df_near.sort_values("Distance to Metro (km)")
    df_near.to_csv("rera_near_purple_line.csv", index=False, encoding="utf-8-sig")

    print(f"\n[+] {len(qualified)} / {len(all_results)} properties within 4km of Purple Line")
    print(f"    rera_near_purple_line.csv saved ({len(qualified)} rows)")

    if no_match:
        print(f"\n[!] {len(no_match)} addresses had no locality match:")
        for r in no_match:
            print(f"    {r['Sl No']:4s} {r['Project Name'][:45]} | {r['Address'][:70]}")

    # ── HTML map ──────────────────────────────────────────────────────────
    pins = qualified   # only show qualifying properties
    markers_js = ""
    for p in pins:
        popup = (f"<b>{p['Project Name']}</b><br>"
                 f"<i>{p['Promoter']}</i><br>"
                 f"Completion: {p['Completion Date']}<br>"
                 f"Nearest Metro: <b>{p['Nearest Metro Station']}</b> ({p['Distance to Metro (km)']} km)<br>"
                 f"<small>{p['Address'][:120]}</small>")
        popup = popup.replace("'", "\\'").replace("\n", " ").replace('"', '&quot;')
        lat, lon = p["Lat"], p["Lon"]
        markers_js += (
            f"  L.marker([{lat},{lon}],{{icon:propIcon}})"
            f".addTo(map).bindPopup('{popup}');\n"
        )

    for name, slat, slon in PURPLE_LINE_STATIONS:
        markers_js += (
            f"  L.circleMarker([{slat},{slon}],{{radius:9,color:'#7b2fbe',"
            f"fillColor:'#7b2fbe',fillOpacity:0.9,weight:2}})"
            f".addTo(map).bindPopup('<b>🚇 {name}</b>');\n"
        )
        markers_js += (
            f"  L.circle([{slat},{slon}],{{radius:4000,color:'#7b2fbe',"
            f"fillOpacity:0.04,weight:1,dashArray:'6'}}).addTo(map);\n"
        )

    avg_lat = sum(p["Lat"] for p in pins) / len(pins) if pins else 12.87
    avg_lon = sum(p["Lon"] for p in pins) / len(pins) if pins else 77.54

    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>RERA Properties within 4km of Purple Line Metro</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body{{margin:0;font-family:Arial,sans-serif}}
  #map{{height:100vh;width:100%}}
  #panel{{position:absolute;top:10px;left:50px;z-index:1000;background:white;
          padding:12px 16px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.25);
          max-width:320px;font-size:13px}}
  #panel h3{{margin:0 0 6px;font-size:15px}}
  .legend-dot{{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:5px}}
</style>
</head><body>
<div id="panel">
  <h3>RERA Projects near Purple Line</h3>
  <span class="legend-dot" style="background:#e63946"></span>{len(pins)} qualifying projects<br>
  <span class="legend-dot" style="background:#7b2fbe"></span>Metro stations (4km circle shown)<br>
  <small style="color:#666">Click any marker for details</small>
</div>
<div id="map"></div>
<script>
var map = L.map('map').setView([{avg_lat:.4f},{avg_lon:.4f}],12);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{
  attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}}).addTo(map);
var propIcon = L.icon({{
  iconUrl:'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl:'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize:[25,41],iconAnchor:[12,41],popupAnchor:[1,-34]
}});
{markers_js}
</script>
</body></html>"""

    with open("rera_purple_line_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("    rera_purple_line_map.html saved  (open in any browser)")

    # Google Maps URL (up to 10 waypoints)
    if pins:
        wps = "/".join(f"{p['Lat']},{p['Lon']}" for p in pins[:10])
        print(f"\n    Google Maps (first 10 pins):")
        print(f"    https://www.google.com/maps/dir/{wps}")

main()
