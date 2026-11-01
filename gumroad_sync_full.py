import os
import sys
import json
import time
import requests

TOKEN = "NmAVsoonEH0obGU4uRTWh-4I0iyQ94dwGaFjwMOnQmg"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 1. Fetch existing products to avoid duplicating
r = requests.get("https://api.gumroad.com/v2/products", headers=HEADERS)
existing_names = set()
existing_map = {}
if r.status_code == 200:
    for p in r.json().get("products", []):
        existing_names.add(p.get("name"))
        existing_map[p.get("name")] = p.get("short_url")

print(f"Produits déjà existants sur Gumroad: {len(existing_names)}")

# 2. Check Bundle
bundle_name = "Pack Intégral EDN 2026 — 28 Référentiels Médicaux"
if bundle_name not in existing_names:
    print("\nCréation du Pack Intégral (Bundle 28 Modules)...")
    b_data = {
        "name": bundle_name,
        "price": 7900,
        "currency": "eur",
        "description": (
            "L'intégralité des 28 volumes officiels EDN / ECN au format Word (.docx) et PDF imprimable.\n"
            "Conforme aux recommandations des Collèges d'Enseignants universitaires.\n"
            "Plus de 4 800 tableaux cliniques, fiches réflexes et schémas sans déformation.\n"
            "Application Android hors-ligne incluse."
        )
    }
    rb = requests.post("https://api.gumroad.com/v2/products", headers=HEADERS, data=b_data)
    if rb.status_code in (200, 201):
        p_obj = rb.json().get("product", {})
        existing_map[bundle_name] = p_obj.get("short_url")
        print(f" -> Pack Intégral créé: {p_obj.get('short_url')}")
    else:
        print(f" -> Statut création bundle: {rb.status_code}")
else:
    print(f" -> Pack Intégral déjà présent: {existing_map.get(bundle_name)}")

# 3. Create missing books
with open(r"C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json", "r", encoding="utf-8") as f:
    books = json.load(f)

for b in books:
    p_name = f"EDN — {b['title']}"
    if p_name in existing_names:
        print(f" -> Déjà présent: {p_name} ({existing_map.get(p_name)})")
        b["gumroad_url"] = existing_map.get(p_name)
        continue

    print(f"Création de: {p_name}...")
    p_data = {
        "name": p_name,
        "price": int(b["ebook"] * 100),
        "currency": "eur",
        "description": (
            f"Référentiel médical complet : {b['title']} ({b['pages']} pages).\n"
            "Conforme aux Collèges d'Enseignants universitaires pour l'EDN & ECOS.\n"
            "Format Word .docx haute qualité, rigueur académique et clinique certifiée."
        )
    }
    time.sleep(2) # Respect Gumroad rate limits
    rp = requests.post("https://api.gumroad.com/v2/products", headers=HEADERS, data=p_data)
    if rp.status_code in (200, 201):
        p_obj = rp.json().get("product", {})
        url = p_obj.get("short_url")
        b["gumroad_url"] = url
        existing_map[p_name] = url
        print(f" -> Succès: {url}")
    else:
        print(f" -> Réponse ({rp.status_code}): {rp.text[:120]}")

# 4. Save updated books_data with exact live short_urls
with open(r"C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print("\n--- SYNCHRONISATION TERMINÉE AVEC SUCCÈS ---")
