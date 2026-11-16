# DobotBasicMovement – Dobot Magician mit Python steuern

Grundprojekt, um den **Dobot Magician** aus **VS Code** mit Python zu programmieren. Ideal als Einstieg in Robotik / Physical AI.

> Zuerst die **[INSTALLREADME.md](INSTALLREADME.md)** durcharbeiten (Treiber, Python, Umgebung), dann die **[HANDHABUNG.md](HANDHABUNG.md)** lesen.

## Projektstruktur

| Datei | Zweck |
|---|---|
| `INSTALLREADME.md` | Installation Schritt für Schritt |
| `HANDHABUNG.md` | Bedienung: Weboberfläche, Skripte, Regeln, Fehlersuche |
| `software&driver/` | Installationsdateien (DobotLink, CP210x-Treiber, DobotLab) |
| `requirements.txt` | Python-Pakete (`pydobot`, `pyserial`, `flask`) |
| `dobot_helper.py` | Port-Suche, Verbindung, Stopp, Alarmabfrage (inkl. Korrektur der pydobot-Prüfsumme) |
| `00_ports_anzeigen.py` | Listet COM-Ports (Treibertest) |
| `01_verbindung_testen.py` | Liest die Position, **bewegt nichts** |
| `02_erste_bewegung.py` | Kleine Fahrt vor/zurück |
| `03_quadrat.py` | Quadrat in der Luft |
| `04_greifer_saugnapf.py` | Saugnapf/Greifer schalten |
| `05_move_man.py` | Manuelles Verfahren per Taste (Jog), mit Sicherheitsgrenzen |
| `06_diagnose.py` | Diagnose, falls der Dobot nicht antwortet |
| `app.py` + `templates/index.html` | Web-Frontend (Flask + Bootstrap/Bootswatch Flatly) |

## Handhabung nach der Installation
Ausführliche Anleitung: **[HANDHABUNG.md](HANDHABUNG.md)**. Kurzfassung:

**Vor jedem Start:** Arbeitsbereich frei, Dobot einschalten, DobotLink/DobotLab beenden, im Projektordner die Umgebung aktivieren:
```powershell
.venv\Scripts\Activate.ps1
```

**Weg A – Weboberfläche** (Programme per Klick, Arm per Taste verfahren):
```powershell
python app.py
```
Dann <http://127.0.0.1:5000> öffnen, **Verbinden** klicken (Suche ca. 10 s) und Programme 01–04 starten oder mit den Pfeiltasten verfahren. Taste halten = Arm fährt, loslassen = Stopp. Beenden mit Strg+C.

**Weg B – Einzelne Skripte:**
```powershell
python 00_ports_anzeigen.py
python 01_verbindung_testen.py
python 02_erste_bewegung.py
```

**Nur ein Zugriff gleichzeitig:** Weboberfläche, Einzelskripte, DobotLink und DobotLab teilen sich einen COM-Port, es darf immer nur eins laufen. Der rote **■ STOPP** (Taste Esc) bricht Programme und Bewegungen ab. Im Notfall zusätzlich den Dobot am Schalter ausschalten.

## Das Koordinatensystem
Der Dobot arbeitet mit kartesischen Koordinaten in **Millimetern** (Ursprung = Mitte der Basis):

- **x** – nach vorne (weg vom Roboter)
- **y** – nach links (+) / rechts (−)
- **z** – Höhe (0 ≈ Tischhöhe der Basis, + nach oben)
- **r** – Drehung des Endeffektors in Grad

Typischer Arbeitsbereich: x ≈ 150–300 mm, y ≈ −150…150 mm, z ≈ 0…150 mm (das Frontend begrenzt so). Außerhalb davon fährt der Dobot nicht oder meldet einen Alarm.

## Die wichtigsten Befehle (`pydobot`)

```python
from dobot_helper import verbinde

device = verbinde()                       # Verbindung (Port wird automatisch gesucht)
device.speed(100, 100)                    # Geschwindigkeit, Beschleunigung
device.move_to(200, 0, 50, 0, wait=True)  # Fahre zu x, y, z, r und warte bis angekommen
x, y, z, r, j1, j2, j3, j4 = device.pose()  # Aktuelle Position + Gelenkwinkel
device.suck(True)                         # Saugnapf an  (False = aus)
device.grip(True)                         # Greifer zu   (False = auf)
device.close()                            # Verbindung beenden – immer am Ende!
```

## Aufgaben für Schüler
1. Lass den Dobot ein **Rechteck** statt eines Quadrats fahren.
2. Fahre ein **Dreieck** und lasse ihn am Ende zur Startposition zurückkehren.
3. Schreibe eine Funktion `gehe_zu(x, y)`, die immer erst hoch (z=50) fährt, dann seitlich, dann runter.
4. Nimm mit dem Saugnapf einen Gegenstand auf und lege ihn 10 cm weiter ab (Pick & Place).
5. Lies per Hand die Position aus (Arm sanft bewegen, `pose()` ausgeben) und fahre sie wieder an.

## Sicherheitshinweise
- **Arbeitsbereich frei halten**, nie in den Arm greifen, solange er fährt.
- Mit **niedriger Geschwindigkeit** (≤ 100) beginnen.
- Z-Werte nahe 0 oder negativ nur testen, wenn nichts im Weg ist – der Arm kann gegen den Tisch fahren.
- Bei Fehlverhalten: Dobot am Schalter **ausschalten**.
- **DobotLink/DobotLab, die Weboberfläche und Python-Skripte können nicht gleichzeitig** auf den Dobot zugreifen.

## Häufige Probleme
Siehe [HANDHABUNG.md](HANDHABUNG.md) (Bedienung) und die Fehlersuche-Tabelle in der [INSTALLREADME.md](INSTALLREADME.md) (Installation).

## Weiterführend
- `pydobot` auf PyPI: <https://pypi.org/project/pydobot/>
- Offizielle Dobot-Downloads: <https://www.dobot-robots.com/>

## Lizenz
Der Code und die Anleitungen dieses Projekts stehen unter der [MIT-Lizenz](LICENSE). Für den mitgelieferten CP210x-Treiber (`software&driver/`) gilt die Lizenz von Silicon Labs, die in der ZIP-Datei beiliegt.
