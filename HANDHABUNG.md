# Handhabung – so arbeitest du mit dem Dobot

Diese Anleitung gilt **nach** der [INSTALLREADME.md](INSTALLREADME.md). Es gibt zwei Wege, den Dobot zu steuern:

| Weg | Wann sinnvoll |
|---|---|
| **A) Weboberfläche** (`python app.py`) | Schnell ausprobieren, Arm von Hand verfahren, Programme per Klick starten |
| **B) Einzelne Skripte** (`python 02_erste_bewegung.py`) | Eigenen Code schreiben und testen |

> **Nur einer von beiden darf gleichzeitig laufen** (ebenso DobotLink/DobotLab): Der Dobot hat nur einen COM-Port, und den kann immer nur ein Programm belegen.

---

## 1. Jedes Mal vor dem Start (Checkliste)

1. Arbeitsbereich um den Dobot **frei räumen** (ca. 40 cm), Hände weg.
2. Dobot per Schalter **einschalten**, USB-Kabel angesteckt.
3. **DobotLink und DobotLab beenden** (auch im Infobereich neben der Uhr).
4. Projektordner in VS Code öffnen, Terminal öffnen (Strg+ö) und die Umgebung aktivieren:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   Vorn im Terminal steht dann `(.venv)`.

---

## 2. Weg A: Weboberfläche

### Starten
```powershell
python app.py
```
Im Browser **<http://127.0.0.1:5000>** öffnen. Beenden: im Terminal **Strg+C**.
(Die Seite lädt das Design aus dem Internet, ohne Internet sieht sie unformatiert aus, funktioniert aber trotzdem.)

### Aufbau der Seite

| Bereich | Bedeutung |
|---|---|
| **Statusanzeige** (oben rechts) | grau = getrennt, grün = verbunden, gelb = ein Programm läuft |
| **■ STOPP** (rot, oben rechts) | **Not-Aus per Software:** bricht Programm und Verfahren sofort ab. Auch mit der Taste **Esc**. Der Dobot-Schalter bleibt der echte Not-Aus. |
| **Alarm-Leiste** (rot) | Erscheint, wenn der Dobot einen Alarm meldet (z. B. Endlage, Ziel außer Reichweite). Arm mittig stellen, dann **Alarm löschen**. |
| **Verbinden / Trennen** | Baut die Verbindung zum Dobot auf bzw. beendet sie |
| **Programme** | Startet die Skripte 01 bis 04 per Klick |
| **Position** | Zeigt x, y, z (mm) und r (Grad) des Arms live |
| **Manuell verfahren** | Bewegungstasten (siehe unten) |
| **Protokoll** | Ausgaben der Programme und Fehlermeldungen |

### Schritt für Schritt
1. **Verbinden** klicken. Die Suche nach dem COM-Port dauert bis zu ca. 10 Sekunden („Suche Dobot ...“). Danach wird die Statusanzeige grün.
2. **Position lesen** klicken: Das Protokoll zeigt die aktuelle Position, der Arm bewegt sich nicht. Ein guter Test, ob alles funktioniert.
3. Programme starten:

   | Knopf | Skript | Was passiert |
   |---|---|---|
   | Position lesen | `01_verbindung_testen.py` | Liest Position und Gelenkwinkel, **keine Bewegung** |
   | Erste Bewegung | `02_erste_bewegung.py` | Fährt 50 mm nach links, rechts und zurück (Höhe 50 mm) |
   | Quadrat fahren | `03_quadrat.py` | Fährt ein Quadrat (60 mm Kantenlänge) in der Luft |
   | Saugnapf Test | `04_greifer_saugnapf.py` | Pumpe 2 Sekunden an, dann aus (nur mit Saugnapf-Aufsatz) |

   Während ein Programm läuft, sind alle Knöpfe gesperrt und die Statusanzeige ist gelb.
4. **Trennen**, wenn du fertig bist (oder die Seite einfach schließen und im Terminal Strg+C drücken).

### Manuell verfahren (05_move_man.py)
**Taste gedrückt halten → Arm fährt. Taste loslassen → Arm stoppt.**

```
        x / y (Draufsicht)                z (Höhe)       r (Drehung)
             [ ▲ ]  x+ (nach vorn)         [ ↑ ] hoch     [ ⟲ ] [ ⟳ ]
      [ ◀ ]         [ ▶ ]                  [ ↓ ] runter
   y+ (links)  [ ▼ ]  y− (rechts)
               x− (zurück)
```

- Ein Schritt sind **5 mm** (bzw. 5 Grad) alle 0,15 Sekunden.
- Der Arm bleibt automatisch im **sicheren Bereich**: x 150–300 mm, y −150…150 mm, z 0…150 mm, r ±90°. Zusätzlich darf der Abstand zur Basis höchstens 300 mm sein (`MAX_RADIUS`), die Ecken des Rechtecks sind sonst außer Reichweite. Am Rand bleibt der Arm einfach stehen.
- Die Werte kannst du in `05_move_man.py` bei `GRENZEN` und `SCHRITT` ändern. Das z-Minimum vorsichtig senken, der Arm könnte gegen den Tisch fahren.
- Während ein Programm läuft, sind die Tasten gesperrt.

### Programm abbrechen
Der rote **■ STOPP** (oder **Esc**) stoppt den Arm, leert die Bewegungswarteschlange und beendet das laufende Programm (Protokoll: „ABGEBROCHEN (Stopp)“). Bei echter Gefahr zusätzlich den **Dobot am Schalter ausschalten**.

Das Protokoll zeigt den Fortschritt live (z. B. „Punkt 3/5“). Antwortet der Dobot nicht mehr, steht dort nach 2 Sekunden „Keine Antwort vom Dobot“. Dann Alarmleiste prüfen, ggf. Dobot aus- und einschalten und neu verbinden.

### Was die Weboberfläche NICHT kann
- Mehrere Browser-Fenster/Nutzer gleichzeitig. Es gibt eine Verbindung zum Dobot.

---

## 3. Weg B: Einzelne Skripte im Terminal

Aktivierte Umgebung vorausgesetzt (Schritt 1):

```powershell
python 00_ports_anzeigen.py       # Zeigt COM-Ports, hilft bei Treiberproblemen (dauert bis ~10 s)
python 01_verbindung_testen.py    # Position lesen, keine Bewegung
python 02_erste_bewegung.py       # Kleine Fahrt
python 03_quadrat.py              # Quadrat
python 04_greifer_saugnapf.py     # Saugnapf an/aus
```

Die Skripte verbinden sich selbst, fahren und trennen die Verbindung wieder. Bevor du sie startest, muss die **Weboberfläche beendet** sein (Strg+C).

### COM-Port festlegen (schneller Start)
Findest du den Port im Geräte-Manager (z. B. `COM6`), trage ihn in [dobot_helper.py](dobot_helper.py) ein:
```python
STANDARD_PORT = "COM6"
```
Dann entfällt die ca. 10 Sekunden lange Suche, sowohl in den Skripten als auch in der Weboberfläche.

### Eigene Skripte schreiben
Kopiere zum Beispiel `02_erste_bewegung.py` und ändere die Koordinaten. Aufbau:

```python
from dobot_helper import verbinde

def ausfuehren(device):
    device.speed(100, 100)
    device.move_to(200, 0, 50, 0, wait=True)

if __name__ == "__main__":
    device = verbinde()
    ausfuehren(device)
    device.close()      # immer am Ende!
```
Mit `ausfuehren(device)` lässt sich ein Skript später auch in `app.py` unter `AKTIONEN` als Knopf einhängen.

---

## 4. Wichtige Regeln

- `device.close()` **immer am Ende**, sonst bleibt der COM-Port belegt und der nächste Start schlägt mit `Zugriff verweigert` fehl. Hilft nichts mehr: Terminal schließen oder Dobot aus- und einschalten.
- `wait=True` bei `move_to` benutzen, damit das Skript auf das Ende der Bewegung wartet.
- Mit niedriger Geschwindigkeit (≤ 100) beginnen.
- Neue Positionen zuerst **hoch über dem Tisch** (z ≥ 50) testen.

## 5. Sicherheit
- Nie in den Arm greifen, solange er fährt. Haare, Kabel und Ärmel fernhalten.
- Bei Fehlverhalten sofort **Dobot am Schalter ausschalten**.
- Nur eine Person bedient den Dobot, die anderen halten Abstand.

## 6. Probleme?

| Meldung / Verhalten | Ursache und Lösung |
|---|---|
| `Kein Dobot gefunden` / „Verbinden“ schlägt fehl | Dobot an? USB angesteckt? Treiber im Geräte-Manager prüfen? |
| `PermissionError` / `Zugriff verweigert` | Ein anderes Programm hat den Port: DobotLink, DobotLab, die Weboberfläche oder ein altes Terminal beenden. |
| Seite sieht unformatiert aus | Kein Internet für das Design. Funktion bleibt erhalten. |
| Tasten reagieren nicht | Erst **Verbinden** klicken; während ein Programm läuft, sind sie gesperrt. |
| Arm fährt nicht / Alarm-LED rot | Ziel außerhalb des Arbeitsbereichs. Dobot aus- und einschalten, Arm mittig stellen. |
| Weitere Hilfe | [INSTALLREADME.md](INSTALLREADME.md) → Fehlersuche |
