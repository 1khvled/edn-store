import json
import csv

with open(r'C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

# 1. Generate Gumroad batch products listing
gumroad_file = r'C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\gumroad_products.csv'
with open(gumroad_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Product Name', 'Price (EUR)', 'Permalink', 'Description', 'File Path'])
    
    # Bundle first
    writer.writerow([
        'Pack Intégral EDN 2026 — 28 Référentiels Médicaux',
        '79.00',
        'pack-integral-28-modules',
        'L\'intégralité des 28 volumes officiels EDN / ECN au format Word (.docx) et PDF imprimable. Plus de 4800 tableaux, schémas et fiches réflexes. Application Android incluse.',
        r'C:\Users\Abdelli\Desktop\SIDE PROJECTS\EDN\EDN-DOCX'
    ])
    
    # 28 Individual Books
    for b in books:
        writer.writerow([
            f'EDN — {b["title"]}',
            f'{b["ebook"]:.2f}',
            b['slug'],
            f'Référentiel complet pour le module {b["title"]} ({b["pages"]} pages). Conforme aux Collèges des Enseignants. Format Word .docx haute qualité.',
            fr'C:\Users\Abdelli\Desktop\SIDE PROJECTS\EDN\EDN-DOCX\EDN-{b["slug"]}.docx'
        ])

print(f'Successfully generated Gumroad product catalog: {gumroad_file}')
