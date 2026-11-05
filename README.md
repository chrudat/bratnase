# 🍕 Speisekarten-Verzeichnis

Willkommen im Speisekarten-Verzeichnis! Hier sammeln wir aktuelle Speisekarten für unsere Mittagspausen. 
Neue Speisekarten oder Online-Links können ganz einfach direkt über die GitHub-Weboberfläche hinzugefügt, aktualisiert oder gelöscht werden.

---

## 📁 Neue Speisekarte hinzufügen

Gehe oben in den Ordner **`menus/`** und klicke oben rechts auf **Add file** ➔ **Upload files** (für PDFs) oder **Create new file** (für Links).

### Dateinamen-Schema

Damit die Speisekarte automatisch richtig einsortiert, benannt und mit Anruf-Button versehen wird, muss die Datei nach folgendem Muster benannt werden:

`[Name]_[Kategorie(n)]_[Ort]_[Telefon].[pdf|url]`

> **Tipp:** Durch den Namen am Anfang sind alle Speisekarten im Ordner alphabetisch nach Restaurants sortiert. So lassen sich alte oder geschlossene Läden im Repository blitzschnell finden und löschen!

---

### Beispiele für Dateinamen:

| Fall | Dateiname | Ergebnis auf der Webseite |
| :--- | :--- | :--- |
| **Name + Mehrfachkategorien + Ort + Telefon** | `Edessa_Döner+Pizza+Salat_Garbsen_0511123456.pdf` | Name: **Edessa**<br>Badges: **Döner**, **Pizza**, **Salat**<br>Ort: **Garbsen**<br>Button: **0511123456** (Anrufen) |
| **PDF mit Ort & Telefon** | `Pizza Luigi_Italienisch_Hannover_051199999.pdf` | Name: **Pizza Luigi**<br>Kategorie: **Italienisch**<br>Ort: **Hannover**<br>Button: **051199999** (Anrufen) |
| **PDF ohne Ort** | `Syrtaki_Griechisch_01701234567.pdf` | Name: **Syrtaki**<br>Kategorie: **Griechisch**<br>Button: **01701234567** (Anrufen) |
| **PDF ohne Telefon** | `Bambus_Asia_Garbsen.pdf` | Name: **Bambus**<br>Kategorie: **Asia**<br>Ort: **Garbsen** |
| **Web-Link statt PDF** | `Jim Block_Burger+Pizza_Hannover_0511000.url` | Zeigt statt des PDF-Buttons einen Button **"Webseite"** zur Online-Speisekarte |

---

## 🔗 Wie erstelle ich eine `.url`-Datei für Webseiten-Links?

Hat das Restaurant eine eigene Online-Speisekarte (statt einer PDF)?

1. Klicke im Ordner `menus/` auf **Add file** ➔ **Create new file**.
2. Nenne die Datei nach dem Schema oben (z. B. `Jim Block_Burger+Pizza_Hannover_0511000.url`).
3. Füge in das große Textfeld einfach **nur die Internetadresse** ein:
   ```text
   [https://www.jim-block.de/speisekarte](https://www.jim-block.de/speisekarte)
