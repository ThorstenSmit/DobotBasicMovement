"""Zeigt alle COM-Ports an. Hilft beim Prüfen, ob der Treiber funktioniert."""
from dobot_helper import alle_ports, finde_dobot_port

print("Suche COM-Ports (kann ca. 10 Sekunden dauern) ...")
ports = alle_ports()
if not ports:
    print("Keine COM-Ports gefunden -> Treiber fehlt oder Dobot nicht angeschlossen/eingeschaltet.")
else:
    for port, beschreibung in ports:
        print(f"{port}: {beschreibung}")
    print("\nVermuteter Dobot-Port:", finde_dobot_port(ports) or "nicht erkannt")
