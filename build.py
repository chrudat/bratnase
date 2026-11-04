import os
import re
import unicodedata
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MENU_DIR = os.path.join(BASE_DIR, "menus")
TEMPLATE_FILE = os.path.join(BASE_DIR, "template.html")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")

if not os.path.exists(MENU_DIR):
    os.makedirs(MENU_DIR)

files = [f for f in os.listdir(MENU_DIR) if f.lower().endswith((".pdf", ".url"))]
files.sort()

cards_html = ""
categories = set()

def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\s_]+", " ", text).strip()
    return text

def is_phone_number(text: str) -> bool:
    clean = re.sub(r"[^\d+]", "", text)
    return len(clean) >= 3 and (text.startswith("+") or text.startswith("0") or text.isdigit())

if not files:
    cards_html = "<div class='no-cards'>Aktuell sind keine Speisekarten hinterlegt.</div>"
else:
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        filename_raw = unicodedata.normalize("NFC", f.rsplit(".", 1)[0])
        parts = filename_raw.split("_")
        
        phone = None
        location = None
        
        # Segmente flexibel auswerten
        if len(parts) >= 4:
            raw_cat = parts[0]
            raw_name = "_".join(parts[1:-2])
            location = parts[-2]
            phone = parts[-1]
        elif len(parts) == 3:
            raw_cat = parts[0]
            raw_name = parts[1]
            last_part = parts[2]
            if is_phone_number(last_part):
                phone = last_part
            else:
                location = last_part
        elif len(parts) == 2:
            raw_cat = parts[0]
            raw_name = parts[1]
        else:
            raw_cat = "Sonstiges"
            raw_name = filename_raw

        # Mehrere Kategorien verarbeiten (getrennt durch '+' oder ',')
        raw_cat_list = [c.strip() for c in re.split(r'[\+,]', raw_cat) if c.strip()]
        card_categories = []
        for c in raw_cat_list:
            cat_clean = clean_text(c).capitalize()
            if cat_clean:
                card_categories.append(cat_clean)
                categories.add(cat_clean)

        if not card_categories:
            card_categories = ["Sonstiges"]
            categories.add("Sonstiges")

        name = clean_text(raw_name)
        full_filepath = os.path.join(MENU_DIR, f)
        
        # Link-Ziel und Button-Bezeichnung bestimmen (.pdf oder .url)
        if ext == ".url":
            with open(full_filepath, "r", encoding="utf-8") as url_file:
                target_url = url_file.read().strip()
            button_label = "Webseite"
        else:
            target_url = f"menus/{quote(f)}"
            button_label = "Speisekarte"

        # Ortsanzeige aufbauen
        location_html = ""
        if location:
            clean_loc = clean_text(location)
            if clean_loc:
                location_html = (
                    f'<p class="card-meta">'
                    f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>'
                    f' {clean_loc}'
                    f'</p>'
                )

        # Telefon-Button aufbauen
        phone_button_html = ""
        if phone:
            clean_phone = re.sub(r"[^\d+]", "", phone)
            display_phone = clean_text(phone)
            if clean_phone:
                phone_button_html = (
                    f'<a href="tel:{clean_phone}" class="btn btn-phone" title="Anrufen: {display_phone}">'
                    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3-3 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>'
                    f'<span>{display_phone}</span></a>'
                )
        
        # HTML-Badges für alle Kategorien erzeugen
        badges_html = "".join([f'<span class="badge">{cat}</span>' for cat in card_categories])
        data_categories = ",".join(card_categories)

        cards_html += (
            f'<article class="card" data-category="{data_categories}">'
            f'<div class="card-body">'
            f'<div class="badges-container" style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;">{badges_html}</div>'
            f'<h2 class="card-title">{name}</h2>'
            f'{location_html}'
            f'</div>'
            f'<div class="actions">'
            f'<a href="{target_url}" target="_blank" rel="noopener" class="btn btn-pdf">'
            f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
            f'<span>{button_label}</span></a>'
            f'{phone_button_html}'
            f'</div></article>'
        )

sorted_categories = sorted(list(categories))
filter_buttons_html = '<button class="filter-btn active" onclick="filterCategory(\'all\', event)">Alle</button>'
for cat in sorted_categories:
    filter_buttons_html += f'<button class="filter-btn" onclick="filterCategory(\'{cat}\', event)">{cat}</button>'

# Template einlesen & Platzhalter ersetzen
with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template_content = f.read()

final_html = template_content.replace("<!--FILTER_BUTTONS-->", filter_buttons_html)
final_html = final_html.replace("<!--CARDS_HTML-->", cards_html)

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(final_html)

print("index.html erfolgreich mit Mehrfachkategorien generiert.")
