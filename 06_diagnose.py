"""Diagnose: prüft Schritt für Schritt, auf welchen Befehl der Dobot antwortet.

Vorher die Weboberfläche beenden (Strg+C)! Der Arm bewegt sich dabei NICHT
(der Testbefehl fährt zur aktuellen Position).
"""
import time
from dobot_helper import verbinde


def schritt(name, funktion):
    t = time.time()
    try:
        ergebnis = funktion()
        print(f"OK     {name} ({time.time() - t:.1f}s) -> {ergebnis}")
        return ergebnis
    except Exception as e:
        print(f"FEHLER {name} ({time.time() - t:.1f}s) -> {e}")


device = verbinde()
pose = schritt("Position lesen", device.pose)
schritt("Alarme lesen (leer = kein Alarm)", device.alarme)
schritt("Geschwindigkeit setzen", lambda: device.speed(100, 100))
if pose:
    x, y, z, r, *_ = pose
    schritt("move_to aktuelle Position (ohne Warten)", lambda: device.move_to(x, y, z, r, wait=False))
    schritt("Index der Warteschlange lesen", device._get_queued_cmd_current_index)
    schritt("move_to aktuelle Position (mit Warten)", lambda: device.move_to(x, y, z, r, wait=True))
device.close()
print("Diagnose fertig. Bitte die komplette Ausgabe schicken.")
