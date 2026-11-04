import os
from datetime import datetime

# Absoluten Pfad des Skript-Verzeichnisses ermitteln
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MENU_DIR = os.path.join(BASE_DIR, "menus")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")

# Ordner 'menus' anlegen, falls er lokal nicht existiert
if not os.path.exists(MENU_DIR):
    os.makedirs(MENU_DIR)

# Alle PDFs auslesen
files = [f for f in os.listdir(MENU_DIR) if f.lower().endswith(".pdf")]
files.sort()

cards_html = ""
if not files:
    cards_html = "<p class='no-cards'>Aktuell sind keine Speisekarten hinterlegt.</p>"
else:
    for f in files:
        name = f.rsplit(".", 1)[0].replace("_", " ")
        filepath = f"menus/{f}"
        full_filepath = os.path.join(MENU_DIR, f)
        mod_time = datetime.fromtimestamp(os.path.getmtime(full_filepath)).strftime("%d.%m.%Y")
        
        cards_html += f"""
        <div class="card">
            <h2>{name}</h2>
            <p class="updated">Stand: {mod_time}</p>
            <div class="actions">
                <a href="{filepath}" target="_blank" class="btn">Speisekarte (PDF) öffnen</a>
            </div>
        </div>
        """

html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mittagspause – Speisekarten</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #f4f5f7; margin: 0; padding: 20px; color: #333; }}
        h1 {{ text-align: center; margin-bottom: 30px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1000px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; }}
        .card h2 {{ margin-top: 0; font-size: 1.25rem; }}
        .updated {{ font-size: 0.85rem; color: #666; }}
        .btn {{ display: inline-block; background: #0066cc; color: white; text-decoration: none; padding: 10px 15px; border-radius: 6px; text-align: center; font-weight: bold; margin-top: 15px; }}
        .btn:hover {{ background: #0052a3; }}
        .no-cards {{ grid-column: 1 / -1; text-align: center; color: #777; font-style: italic; }}
    </style>
</head>
<body>
    <h1>🍕 Mittagspause Speisekarten</h1>
    <div class="grid">
        {cards_html}
    </div>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(html_content)

print(f"index.html erfolgreich mit {len(files)} Speisekarte(n) erstellt.")
