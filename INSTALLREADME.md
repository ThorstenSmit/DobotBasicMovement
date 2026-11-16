# Installation – Dobot Magician unter Windows + VS Code

Diese Anleitung bringt dich vom leeren Rechner bis zur ersten Bewegung. **Reihenfolge einhalten!**

## 0. Voraussetzungen
- Windows 10/11
- Dobot Magician mit Netzteil und USB-Kabel (USB-A auf USB-B)
- Python 3.10 oder neuer (siehe 1.1) und Visual Studio Code (siehe 1.2)

## 1. Software und Treiber installieren

Alle benötigten Installationsdateien liegen im Ordner **`software&driver/`**:

| Datei | Wofür | Reihenfolge |
|---|---|---|
| `DobotLink-6.7.7-edu-x86-64-stable.exe` | Dobot-Kommunikationssoftware | **1.** |
| `CP210x_VCP_Windows.zip` | USB-Treiber (Silicon Labs CP210x) | **2.** |
| `DobotLabSetup-2.4.6-x86-64-stable.exe` | Bedienoberfläche (optional, nicht nötig für Python) | optional |

> Die großen `.exe`-Dateien (DobotLink ca. 420 MB, DobotLab ca. 880 MB) liegen nicht auf GitHub, weil GitHub nur Dateien bis 100 MB erlaubt. Hol sie von deiner Lehrkraft (Schul-Laufwerk/USB-Stick) oder von <https://www.dobot-robots.com/> (Download Center → Magician → Control Software).

### 1.1 Python
1. Von <https://www.python.org/downloads/> installieren.
2. Im Installer **unbedingt** „Add python.exe to PATH“ anhaken.
3. Test im Terminal: `python --version`

### 1.2 Visual Studio Code
1. <https://code.visualstudio.com/> installieren.
2. Erweiterung **Python** (Microsoft) installieren (Strg+Shift+X → „Python“).

### 1.3 DobotLink installieren
1. `DobotLink-6.7.7-edu-x86-64-stable.exe` starten und der Installation folgen.

### 1.4 CP210x-Treiber installieren
Der Dobot meldet sich über einen **CP210x**-Chip („CP2102 USB to UART Bridge Controller“) am PC an. Ohne diesen Treiber gibt es keinen COM-Port.

1. `CP210x_VCP_Windows.zip` entpacken.
2. `CP210xVCPInstaller_x64.exe` starten (bei einem alten 32-Bit-Windows: `..._x86.exe`) und der Installation folgen.

### 1.5 DobotLab (optional)
`DobotLabSetup-2.4.6-x86-64-stable.exe` installieren, wenn du den Dobot zusätzlich mit der grafischen Oberfläche testen möchtest. Für die Python-Programme in diesem Projekt ist sie **nicht nötig**.

> **Wichtig:** DobotLink und DobotLab **müssen beendet sein**, wenn du Python-Skripte startest. Sonst blockieren sie den COM-Port. Prüfe auch den Infobereich der Taskleiste (neben der Uhr): DobotLink läuft dort gern im Hintergrund weiter.

## 2. Dobot aufstellen und anschließen
1. Dobot auf eine ebene, stabile Fläche stellen. **Um den Roboter ca. 40 cm Platz freihalten.**
2. Arm vorsichtig in eine **mittlere, aufrechte Stellung** bringen (nicht an den Anschlag drücken).
3. Netzteil anschließen und den Schalter an der Basis einschalten.
4. USB-Kabel mit dem PC verbinden.

## 3. Treiber prüfen
1. Rechtsklick auf Start → **Geräte-Manager** → **Anschlüsse (COM & LPT)**.
2. Es sollte ein Eintrag wie `Silicon Labs CP210x USB to UART Bridge (COM6)` erscheinen. Merke dir die COM-Nummer.
3. Steht stattdessen unter „Andere Geräte“ ein **gelbes Warndreieck** bei „CP2102 USB to UART Bridge Controller“, fehlt der Treiber (Schritt 1.4 wiederholen, danach Kabel neu stecken).

## 4. Projekt holen
```powershell
git clone https://github.com/ThorstenSmit/DobotBasicMovement.git
cd DobotBasicMovement
```
(Oder die ZIP von GitHub entpacken.) Den Ordner dann in VS Code öffnen: **Datei → Ordner öffnen**.

## 5. Virtuelle Umgebung und Pakete
Im VS-Code-Terminal (Strg+ö):

**Schritt 5a – nur wenn der Ordner `.venv` noch NICHT existiert** (z. B. nach `git clone`, denn `.venv` wird nicht auf GitHub gespeichert):
```powershell
python -m venv .venv
```
Ist `.venv` schon im Projektordner vorhanden (z. B. weil du die vorbereitete Projektkopie von der Lehrkraft bekommen hast), **überspringst du diesen Befehl**.

**Schritt 5b – immer:**
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Falls PowerShell die Aktivierung blockiert („Skriptausführung deaktiviert“), einmalig:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Danach in VS Code mit **Strg+Shift+P → „Python: Select Interpreter“** den Interpreter aus `.venv` auswählen.

## 6. Testen
```powershell
python 00_ports_anzeigen.py       # Zeigt COM-Ports (dauert bis ~10 s); der Dobot sollte auftauchen
python 01_verbindung_testen.py    # Verbindet und liest die Position (Arm bewegt sich nicht)
python 02_erste_bewegung.py       # Erste kleine Bewegung
```
Wenn die Bewegung ausgeführt wird, ist alles bereit. 🎉

Optional startest du die Weboberfläche mit `python app.py` und öffnest <http://127.0.0.1:5000> (siehe README). Die Skripte und das Frontend nicht gleichzeitig laufen lassen.

## Fehlersuche

| Problem | Lösung |
|---|---|
| `Kein Dobot gefunden` | Dobot eingeschaltet? Anderes USB-Kabel/anderer USB-Port? Treiber im Geräte-Manager prüfen. |
| `PermissionError(13, ...)` / `Zugriff verweigert` | Ein anderes Programm hält den Port: **DobotLink und DobotLab beenden** (auch im Infobereich der Taskleiste), andere Python-Terminals schließen. |
| Port-Suche dauert ~10 s oder findet nichts | COM-Nummer aus dem Geräte-Manager in `dobot_helper.py` bei `STANDARD_PORT = "COM6"` eintragen. Das überspringt die Suche. |
| Skript hängt nach dem Verbinden | Dobot aus- und wieder einschalten, Skript neu starten. |
| Dobot bewegt sich nicht / Alarm-LED rot | Position außerhalb des Arbeitsbereichs oder Arm am Anschlag. Dobot ausschalten, Arm mittig platzieren, neu starten. |
| `ModuleNotFoundError: pydobot` | `.venv` nicht aktiv oder Paketinstallation fehlt: Schritt 5 wiederholen und richtigen Interpreter in VS Code wählen. |
| Treiber lässt sich nicht installieren | Installer per Rechtsklick „Als Administrator ausführen“, danach PC neu starten. |
