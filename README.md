# 🍕 Speisekarten-Verzeichnis

Willkommen im Speisekarten-Verzeichnis! Hier sammeln wir aktuelle Speisekarten für unsere Mittagspausen. 
Neue Speisekarten oder Online-Links können ganz einfach direkt über die GitHub-Weboberfläche hinzugefügt oder aktualisiert werden.

---

## 📁 Neue Speisekarte hinzufügen

Gehe oben in den Ordner **`menus/`** und klicke oben rechts auf **Add file** ➔ **Upload files** (für PDFs) oder **Create new file** (für Links).

### Dateinamen-Schema

Damit die Speisekarte automatisch richtig einsortiert, benannt und mit Anruf-Button versehen wird, muss die Datei nach folgendem Muster benannt werden:

`[Kategorie(n)]_[Name]_[Ort]_[Telefon].[pdf|url]`

> **Tipp für Mehrfachkategorien:** Wenn ein Lokal verschiedene Speisen anbietet (z. B. Döner, Pizza und Salat), kannst du die Kategorien im ersten Abschnitt einfach mit einem Pluszeichen (`+`) oder Komma (`,`) trennen.

---

### Beispiele für Dateinamen:

| Fall | Dateiname | Ergebnis auf der Webseite |
| :--- | :--- | :--- |
| **Mehrfachkategorien** | `Döner+Pizza+Salat_Edessa_Garbsen_0511123456.pdf` | Zeigt die Badges **Döner**, **Pizza** und **Salat**. Der Eintrag wird bei allen drei Kategorie-Filterbuttons gefunden. |
| **PDF mit Ort & Telefon** | `Italienisch_Pizza Luigi_Hannover_0511123456.pdf` | Kategorie: **Italienisch**<br>Name: **Pizza Luigi**<br>Ort: **Hannover**<br>Button: **0511123456** (Anrufen) |
| **PDF nur mit Ort** | `Döner_Edessa_Garbsen.pdf` | Kategorie: **Döner**<br>Name: **Edessa**<br>Ort: **Garbsen** |
| **PDF nur mit Telefon** | `Griechisch_Syrtaki_01701234567.pdf` | Kategorie: **Griechisch**<br>Name: **Syrtaki**<br>Button: **01701234567** (Anrufen) |
| **Web-Link statt PDF** | `Burger+Asia_Bambus_Hannover_0511987654.url` | Zeigt statt des PDF-Buttons einen Button **"Webseite"** zur Online-Speisekarte |

---

## 🔗 Wie erstelle ich eine `.url`-Datei für Webseiten-Links?

Hat das Restaurant eine eigene Online-Speisekarte (statt einer PDF)?

1. Klicke im Ordner `menus/` auf **Add file** ➔ **Create new file**.
2. Nenne die Datei nach dem Schema oben (z. B. `Burger+Pizza_Jim Block_Hannover_0511000.url`).
3. Füge in das große Textfeld einfach **nur die Internetadresse** ein:
   ```text
   [https://www.jim-block.de/speisekarte](https://www.jim-block.de/speisekarte)
