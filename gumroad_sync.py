import os
import sys
import json
import time
import requests

TOKEN = os.environ.get("GUMROAD_TOKEN")

if not TOKEN:
    print("Veuillez définir la variable d'environnement GUMROAD_TOKEN ou passer le token en argument.")
    print("Usage: python gumroad_sync.py <YOUR_ACCESS_TOKEN>")
    if len(sys.argv) > 1:
        TOKEN = sys.argv[1].strip()
    else:
        sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def verify_account():
    r = requests.get("https://api.gumroad.com/v2/user", headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        user = data.get("user", {})
        print(f"Connexion Gumroad réussie !")
        print(f"Utilisateur: {user.get('name')} (@{user.get('username') or user.get('custom_url')})")
        print(f"Email: {user.get('email')}")
        return user
    else:
        print(f"Erreur de connexion ({r.status_code}): {r.text}")
        return None

def sync_products():
    user = verify_account()
    if not user:
        return

    # Load products
    catalog_path = r"C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json"
    with open(catalog_path, "r", encoding="utf-8") as f:
        books = json.load(f)

    # 1. Create Bundle
    print("\n--- Création / Synchronisation du Pack Intégral (Bundle 28 Modules) ---")
    bundle_data = {
        "name": "Pack Intégral EDN 2026 — 28 Référentiels Médicaux",
        "price": 7900, # 79.00 EUR in cents
        "currency": "eur",
        "url": "pack-integral-28-modules",
        "description": (
            "L'intégralité des 28 volumes officiels EDN / ECN au format Word (.docx) et PDF imprimable.\n"
            "Conforme aux recommandations des Collèges d'Enseignants universitaires.\n"
            "Plus de 4 800 tableaux cliniques, fiches réflexes et schémas sans déformation.\n"
            "Application Android hors-ligne incluse."
        )
    }
    rb = requests.post("https://api.gumroad.com/v2/products", headers=HEADERS, data=bundle_data)
    if rb.status_code in (200, 201):
        print(" -> Pack Intégral créé avec succès sur Gumroad !")
    else:
        print(f" -> Réponse pour Pack Intégral: {rb.status_code} ({rb.json().get('message', rb.text)})")

    # 2. Create 28 Books
    print("\n--- Création / Synchronisation des 28 Volumes Individuels ---")
    for b in books:
        p_data = {
            "name": f"EDN — {b['title']}",
            "price": int(b["ebook"] * 100), # 999 cents
            "currency": "eur",
            "url": b["slug"],
            "description": (
                f"Référentiel médical complet : {b['title']} ({b['pages']} pages).\n"
                "Conforme aux Collèges d'Enseignants universitaires pour l'EDN & ECOS.\n"
                "Format Word .docx haute qualité, rigueur académique et clinique certifiée."
            )
        }
        try:
            rp = requests.post("https://api.gumroad.com/v2/products", headers=HEADERS, data=p_data)
            if rp.status_code in (200, 201):
                print(f" -> OK: {b['title']} (https://gumroad.com/l/{b['slug']})")
            else:
                msg = rp.text
                try:
                    msg = rp.json().get("message", rp.text)
                except Exception:
                    pass
                print(f" -> Info [{b['slug']}]: {rp.status_code} ({msg})")
        except Exception as e:
            print(f" -> Erreur sur {b['slug']}: {e}")
        time.sleep(1)

if __name__ == "__main__":
    sync_products()
