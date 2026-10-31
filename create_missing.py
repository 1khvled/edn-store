import requests
import json
import time

TOKEN = "NmAVsoonEH0obGU4uRTWh-4I0iyQ94dwGaFjwMOnQmg"
headers = {"Authorization": f"Bearer {TOKEN}"}

with open(r"C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json", "r", encoding="utf-8") as f:
    books = json.load(f)

# Collect existing
existing = set()
url = "https://api.gumroad.com/v2/products"
while url:
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        break
    data = r.json()
    for p in data.get("products", []):
        existing.add(p.get("name"))
    np = data.get("next_page_url")
    url = ("https://api.gumroad.com" + np) if np else None

missing = [b for b in books if f"EDN — {b['title']}" not in existing]
print(f"Missing books count: {len(missing)}")

for b in missing:
    name = f"EDN — {b['title']}"
    print(f"Creating: {name}...")
    p_data = {
        "name": name,
        "price": int(b["ebook"] * 100),
        "currency": "eur",
        "description": (
            f"Référentiel médical complet : {b['title']} ({b['pages']} pages).\n"
            "Conforme aux Collèges des Enseignants universitaires pour l'EDN & ECOS.\n"
            "Format Word .docx haute qualité, zéro hallucination médicale."
        )
    }
    time.sleep(2)
    rp = requests.post("https://api.gumroad.com/v2/products", headers=headers, data=p_data)
    if rp.status_code in (200, 201):
        surl = rp.json().get("product", {}).get("short_url")
        print(f" -> Succès: {surl}")
    else:
        print(f" -> Statut ({rp.status_code}): {rp.text[:100]}")

# Now re-fetch all and map them exactly into books_data.json
final_map = {}
url = "https://api.gumroad.com/v2/products"
while url:
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        break
    data = r.json()
    for p in data.get("products", []):
        final_map[p.get("name")] = p.get("short_url")
    np = data.get("next_page_url")
    url = ("https://api.gumroad.com" + np) if np else None

bundle_url = final_map.get("Pack Intégral EDN 2026 — 28 Référentiels Médicaux")
print(f"\nBundle URL: {bundle_url}")

for b in books:
    name = f"EDN — {b['title']}"
    b["gumroad_url"] = final_map.get(name, "https://gumroad.com/l/pack-integral-28-modules")

with open(r"C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print("Saved updated books_data.json with exact live Gumroad URLs.")
