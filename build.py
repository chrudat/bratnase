import os
import re
import unicodedata
from datetime import datetime
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MENU_DIR = os.path.join(BASE_DIR, "menus")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")

if not os.path.exists(MENU_DIR):
    os.makedirs(MENU_DIR)

files = [f for f in os.listdir(MENU_DIR) if f.lower().endswith(".pdf")]
files.sort()

cards_html = ""
categories = set()

def clean_text(text: str) -> str:
    """Normalisiert Unicode (NFC), entfernt überflüssige Leerzeichen und formatiert Umlaute sauber."""
    text = unicodedata.normalize("NFC", text)
    # Mehrfache Leerzeichen oder Unterstriche bereinigen
    text = re.sub(r"[\s_]+", " ", text).strip()
    return text

if not files:
    cards_html = "<div class='no-cards'>Aktuell sind keine Speisekarten hinterlegt.</div>"
else:
    for f in files:
        # Dateiname ohne Endung & Unicode normalisieren
        filename_raw = unicodedata.normalize("NFC", f.rsplit(".", 1)[0])
        parts = filename_raw.split("_")
        
        # Segmente auswerten: [Kategorie]_[Name]_[Telefonnummer]
        if len(parts) >= 3:
            raw_cat = parts[0]
            phone = parts[-1]
            raw_name = "_".join(parts[1:-1])
        elif len(parts) == 2:
            raw_cat = parts[0]
            raw_name = parts[1]
            phone = None
        else:
            raw_cat = "Sonstiges"
            raw_name = filename_raw
            phone = None

        # Formatierung von Kategorie & Name
        category = clean_text(raw_cat).capitalize()
        name = clean_text(raw_name)
        
        if not category:
            category = "Sonstiges"
        categories.add(category)
        
        # URL-safe Pfad für HTML-Verlinkung
        filepath_encoded = f"menus/{quote(f)}"
        
        full_filepath = os.path.join(MENU_DIR, f)
        mod_time = datetime.fromtimestamp(os.path.getmtime(full_filepath)).strftime("%d.%m.%Y")
        
        # Anrufen-Button erzeugen, falls eine Nummer vorhanden ist
        phone_button_html = ""
        if phone:
            clean_phone = re.sub(r"[^\d+]", "", phone)
            if clean_phone:
                phone_button_html = f"""
                <a href="tel:{clean_phone}" class="btn btn-phone">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.5 19.5 0 0 1-3-3 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                    <span>Anrufen</span>
                </a>
                """
        
        cards_html += f"""
        <article class="card" data-category="{category}">
            <div class="card-body">
                <span class="badge">{category}</span>
                <h2 class="card-title">{name}</h2>
                <p class="card-meta">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    Stand: {mod_time}
                </p>
            </div>
            <div class="actions">
                <a href="{filepath_encoded}" target="_blank" rel="noopener" class="btn btn-pdf">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                    <span>Karte</span>
                </a>
                {phone_button_html}
            </div>
        </article>
        """

# Filter-Buttons HTML dynamisch erzeugen
sorted_categories = sorted(list(categories))
filter_buttons_html = '<button class="filter-btn active" onclick="filterCategory(\'all\', event)">Alle</button>'
for cat in sorted_categories:
    filter_buttons_html += f'<button class="filter-btn" onclick="filterCategory(\'{cat}\', event)">{cat}</button>'

html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mittagspause – Speisekarten</title>
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --success: #16a34a;
            --success-hover: #15803d;
            --accent-bg: #eff6ff;
            --border-color: #e2e8f0;
            --radius: 16px;
            --shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 24px 16px 40px;
            -webkit-font-smoothing: antialiased;
        }}

        header {{
            max-width: 600px;
            margin: 0 auto 20px;
            text-align: center;
        }}

        header h1 {{
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }}

        header p {{
            margin-top: 4px;
            font-size: 0.95rem;
            color: var(--text-muted);
        }}

        .filter-container {{
            display: flex;
            gap: 8px;
            max-width: 600px;
            margin: 0 auto 24px;
            overflow-x: auto;
            padding-bottom: 8px;
            -webkit-overflow-scrolling: touch;
        }}

        .filter-btn {{
            background: #ffffff;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }}

        .filter-btn.active {{
            background: var(--primary);
            color: #ffffff;
            border-color: var(--primary);
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            max-width: 600px;
            margin: 0 auto;
        }}

        @media (min-width: 640px) {{
            .grid, .filter-container {{
                max-width: 900px;
            }}
            .grid {{
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            }}
            header h1 {{
                font-size: 2rem;
            }}
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 20px;
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .card.hidden {{
            display: none;
        }}

        .card-body {{
            margin-bottom: 16px;
        }}

        .badge {{
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: var(--accent-bg);
            color: var(--primary);
            padding: 3px 8px;
            border-radius: 6px;
            margin-bottom: 10px;
        }}

        .card-title {{
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 8px;
        }}

        .card-meta {{
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .actions {{
            display: flex;
            gap: 10px;
        }}

        .btn {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            padding: 10px 12px;
            border-radius: 10px;
            transition: background-color 0.15s ease;
            -webkit-tap-highlight-color: transparent;
        }}

        .btn-pdf {{
            background-color: var(--primary);
        }}

        .btn-pdf:hover {{
            background-color: var(--primary-hover);
        }}

        .btn-phone {{
            background-color:
