"""Manuelles Verfahren (Jog): Der Arm fährt, solange eine Bewegungstaste gedrückt ist.

Wird vom Frontend (app.py) benutzt: pro Tick (ca. alle 150 ms) wird ein kleiner Schritt
in die gewünschte Richtung gefahren. Beim Loslassen wird die Warteschlange geleert.

Alle Zielpositionen werden auf den sicheren Bereich GRENZEN begrenzt.
"""

SCHRITT = {"x": 5.0, "y": 5.0, "z": 5.0, "r": 5.0}   # mm bzw. Grad pro Tick

# Sicherer Arbeitsbereich (mm / Grad). Bei Bedarf anpassen - z-Minimum vorsichtig senken!
GRENZEN = {
    "x": (150.0, 300.0),
    "y": (-150.0, 150.0),
    "z": (0.0, 150.0),
    "r": (-90.0, 90.0),
}

MAX_RADIUS = 300.0  # mm: maximaler Abstand zur Basis (x,y). Reichweite des Magician ca. 320 mm

_ziel = None  # zuletzt angefahrenes Ziel [x, y, z, r]; None = noch nicht gelesen


def _begrenze(wert, achse):
    unten, oben = GRENZEN[achse]
    return max(unten, min(oben, wert))


def jog_schritt(device, achse, richtung):
    """Ein Schritt in Richtung +1 / -1 auf der Achse 'x', 'y', 'z' oder 'r'."""
    global _ziel
    if achse not in SCHRITT:
        raise ValueError(f"Unbekannte Achse: {achse}")
    if _ziel is None:
        x, y, z, r, *_ = device.pose()
        _ziel = [x, y, z, r]
    i = "xyzr".index(achse)
    neu = list(_ziel)
    neu[i] = _begrenze(neu[i] + richtung * SCHRITT[achse], achse)
    if (neu[0] ** 2 + neu[1] ** 2) ** 0.5 > MAX_RADIUS and achse in ("x", "y"):
        return tuple(_ziel)  # außer Reichweite: nicht weiterfahren (sonst Alarm)
    _ziel = neu
    device.move_to(*_ziel, wait=False)
    return tuple(_ziel)


def jog_stopp(device):
    """Taste losgelassen: laufende/wartende Bewegungen abbrechen."""
    global _ziel
    device.stopp()
    _ziel = None  # beim nächsten Jog die echte Position neu lesen


if __name__ == "__main__":
    print("Diese Funktion wird über das Frontend benutzt:  python app.py")
