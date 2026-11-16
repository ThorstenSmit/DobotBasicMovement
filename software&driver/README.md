# Software & Treiber – Downloadhinweise

Hier liegen (bzw. gehören hin) die Installationsdateien für den Dobot Magician unter Windows.

| Datei | Größe | Im Repository? | Pflicht? |
|---|---|---|---|
| `CP210x_VCP_Windows.zip` | ca. 4 MB | **ja** | **ja** – USB-Treiber, ohne ihn gibt es keinen COM-Port |
| `DobotLink-6.7.7-edu-x86-64-stable.exe` | ca. 420 MB | nein (zu groß für GitHub) | empfohlen – Dobot-Kommunikationssoftware |
| `DobotLabSetup-2.4.6-x86-64-stable.exe` | ca. 880 MB | nein (zu groß für GitHub) | optional – grafische Oberfläche, für die Python-Programme nicht nötig |

GitHub erlaubt nur Dateien bis 100 MB. Die beiden `.exe`-Dateien sind deshalb in der `.gitignore` ausgeschlossen. Du bekommst sie von deiner Lehrkraft (Schul-Laufwerk/USB-Stick) oder direkt vom Hersteller.

## 1. DobotLink und DobotLab (Hersteller Dobot)
1. <https://www.dobot-robots.com/> öffnen → **Unterstützung / Support → Download Center**.
2. Links im Filter **Products → Education → Magician** wählen.
3. Im Bereich **Control Software** herunterladen:
   - **DobotLink** (Windows, „Win Local version“)
   - **DobotLab** (Windows, „Win Local version“), optional
4. Die Datei in diesen Ordner legen und installieren (Reihenfolge: zuerst DobotLink, dann der CP210x-Treiber, dann optional DobotLab; siehe [INSTALLREADME.md](../INSTALLREADME.md)).

> **Wichtig:** Das **„DobotStudioPro“** auf der Download-Seite gehört zu den großen Robotern (CR, Nova, MG400, M1 Pro) und ist für den **Magician nicht geeignet**.
>
> Stand der Prüfung: Auf der Magician-Seite waren zuletzt DobotLink 6.7.2 und DobotLab 2.3.13 gelistet. Die hier verwendeten, neueren Versionen (6.7.7 / 2.4.6) lagen vom Hersteller vor. Wenn eine neuere Version angeboten wird, kannst du sie nehmen, hat der Dobot Probleme, nimm die hier genannte.

## 2. CP210x-Treiber (Hersteller Silicon Labs)
Der Magician meldet sich mit einem **CP210x**-Chip („CP2102 USB to UART Bridge Controller“) am PC an.

- **Im Repository:** `CP210x_VCP_Windows.zip` (entpacken, `CP210xVCPInstaller_x64.exe` starten).
- **Selbst herunterladen:** Im Netz nach **„CP210x USB to UART Bridge VCP Drivers“** suchen (Silicon Labs, silabs.com) und den **Windows-Treiber** laden.

Prüfen: Im **Geräte-Manager → Anschlüsse (COM & LPT)** sollte danach `Silicon Labs CP210x USB to UART Bridge (COMx)` erscheinen.

## 3. Was du NICHT brauchst
- DobotStudioPro (andere Roboter)
- Dobot_Mcuisp und die Firmware (nur für Firmware-Updates)
- Demo-/API-Pakete (wir nutzen `pydobot`)

## Lizenz
Für die hier abgelegten Programme und Treiber gelten die Lizenzen der Hersteller (Dobot, Silicon Labs), nicht die MIT-Lizenz des Projekts. Die Lizenz von Silicon Labs liegt der ZIP-Datei bei.
