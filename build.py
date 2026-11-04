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
    text = re.sub(r"[\s_]+", " ", text).strip()
    return text

if not files:
    cards_html = "<div class='no-cards'>Aktuell sind keine Speisekarten hinterlegt.</div>"
else:
    for f in files:
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

        category = clean_text(raw_cat).capitalize()
        name = clean_text(raw_name)
        
        if not category:
            category = "Sonstiges"
        categories.add(category)
        
        # RFC-konformer URL-Pfad für relative Einbindung auf GitHub Pages
        filepath_encoded = f"menus/{quote(f)}"
        
        full_filepath = os.path.join(MENU_DIR, f)
        mod_time = datetime.fromtimestamp(os.path.getmtime(full_filepath)).strftime("%d.%m.%Y")
        
        phone_button_html = ""
        if phone:
            clean_phone = re.sub(r"[^\d+]", "", phone)
            if clean_phone:
                phone_button_html = f"""
                <a href="tel:{clean_phone}" class="btn btn-phone">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
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
        :root
