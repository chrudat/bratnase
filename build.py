import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MENU_DIR = os.path.join(BASE_DIR, "menus")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")

if not os.path.exists(MENU_DIR):
    os.makedirs(MENU_DIR)

files = [f for f in os.listdir(MENU_DIR) if f.lower().endswith(".pdf")]
files.sort()

cards_html = ""
categories = set()

if not files:
    cards_html = "<div class='no-cards'>Aktuell sind keine Speisekarten hinterlegt.</div>"
else:
    for f in files:
        filename_without_ext = f.rsplit(".", 1)[0]
        
        # Kategorie und Name anhand des ersten Unterstrichs trennen
        if "_" in filename_without_ext:
            category, name = filename_without_ext.split("_", 1)
        else:
            category, name = "Sonstiges", filename_without_ext

        category = category.strip().capitalize()
        name = name.replace("_", " ").strip()
        categories.add(category)
        
        filepath = f"menus/{f}"
        full_filepath = os.path.join(MENU_DIR, f)
        mod_time = datetime.fromtimestamp(os.path.getmtime(full_filepath)).strftime("%d.%m.%Y")
        
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
            <a href="{filepath}" target="_blank" rel="noopener" class="btn">
                <span>Speisekarte öffnen</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            </a>
        </article>
        """

# Filter-Buttons HTML dynamisch erzeugen
sorted_categories = sorted(list(categories))
filter_buttons_html = '<button class="filter-btn active" onclick="filterCategory(\'all\')">Alle</button>'
for cat in sorted_categories:
    filter_buttons_html += f'<button class="filter-btn" onclick="filterCategory(\'{cat}\')">{cat}</button>'

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

        /* Horizontal scrollbare Filter-Leiste für Mobilgeräte */
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
                grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
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
            transition: transform 0.2s ease, opacity 0.2s ease;
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

        .btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background-color: var(--primary);
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 12px 16px;
            border-radius: 10px;
            transition: background-color 0.15s ease;
            -webkit-tap-highlight-color: transparent;
        }}

        .btn:hover {{
            background-color: var(--primary-hover);
        }}

        .no-cards {{
            text-align: center;
            padding: 40px 20px;
            background: var(--card-bg);
            border-radius: var(--radius);
            border: 1px dashed var(--border-color);
            color: var(--text-muted);
            font-size: 0.95rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>🍕 Mittagspause</h1>
        <p>Aktuelle Speisekarten im Überblick</p>
    </header>

    <nav class="filter-container">
        {filter_buttons_html}
    </nav>

    <main class="grid">
        {cards_html}
    </main>

    <script>
        function filterCategory(cat) {{
            // Button-Styles aktualisieren
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');

            // Kacheln filtern
            const cards = document.querySelectorAll('.card');
            cards.forEach(card => {{
                if (cat === 'all' || card.getAttribute('data-category') === cat) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}
    </script>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write(html_content)

print(f"index.html erfolgreich mit {len(files)} Speisekarte(n) und {len(categories)} Kategorie(n) erstellt.")
