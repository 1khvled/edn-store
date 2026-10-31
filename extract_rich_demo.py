import docx
import json
import glob
import os

files = sorted(glob.glob(r'C:\Users\Abdelli\Desktop\SIDE PROJECTS\EDN\EDN-DOCX\*.docx'))

with open(r'C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

for idx, b in enumerate(books):
    fpath = files[idx]
    doc = docx.Document(fpath)
    
    # Extract rich blocks (paragraphs, callout boxes, and tables)
    rich_demo = []
    
    # Skip frontmatter, grab realistic medical content
    p_idx = 0
    in_content = False
    
    for p in doc.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if 'PARTIE 1' in t or 'Chapitre 01' in t or 'Chapitre 1' in t:
            in_content = True
        if not in_content:
            continue
        
        # Determine element kind
        if t.startswith('PARTIE'):
            rich_demo.append({'type': 'part', 'text': t})
        elif t.startswith('Chapitre'):
            rich_demo.append({'type': 'chapter', 'text': t})
        elif p.style.name.startswith('Heading 3'):
            rich_demo.append({'type': 'h3', 'text': t})
        elif t.startswith('•') or t.startswith('–'):
            rich_demo.append({'type': 'bullet', 'text': t.lstrip('•– ')})
        elif t.startswith('💡') or 'POINT CLÉ' in t.upper() or 'PIÈGE' in t.upper():
            rich_demo.append({'type': 'callout', 'text': t})
        else:
            rich_demo.append({'type': 'p', 'text': t})
            
        if len(rich_demo) >= 35:
            break
            
    # Also extract up to 2 clinical tables for this module demo
    demo_tables = []
    for tbl in doc.tables:
        if len(tbl.rows) >= 2 and len(tbl.columns) >= 2:
            t_data = []
            for row in tbl.rows[:6]: # first 6 rows
                row_cells = [cell.text.strip() for cell in row.cells]
                t_data.append(row_cells)
            demo_tables.append(t_data)
            if len(demo_tables) >= 2:
                break
                
    b['rich_demo'] = rich_demo
    b['demo_tables'] = demo_tables

with open(r'C:\Users\Abdelli\Desktop\SIDE PROJECTS\edn-store\books_data.json', 'w', encoding='utf-8') as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print('Generated rich demo content with structured headings, bullets, and clinical tables for all 28 books.')
