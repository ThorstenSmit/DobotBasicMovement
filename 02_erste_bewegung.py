"""Erste Bewegung: kleine, sichere Fahrt nach vorne, links, rechts und zurück.

ACHTUNG: Der Arbeitsbereich muss frei sein! Hand und Gegenstände weg vom Roboter.
"""


def ausfuehren(device):
    device.speed(100, 100)  # (Geschwindigkeit, Beschleunigung) - klein halten!

    x, y, z, r, *_ = device.pose()
    print(f"Start: x={x:.1f} y={y:.1f} z={z:.1f}")

    # wait=True: Das Skript wartet, bis die Position erreicht ist
    device.move_to(200, 0, 50, 0, wait=True)    # geradeaus, Höhe 50 mm
    device.move_to(200, 50, 50, 0, wait=True)   # 50 mm nach links
    device.move_to(200, -50, 50, 0, wait=True)  # 50 mm nach rechts
    device.move_to(200, 0, 50, 0, wait=True)    # zurück zur Mitte
    print("Fertig.")


if __name__ == "__main__":
    from dobot_helper import verbinde

    device = verbinde()
    ausfuehren(device)
    device.close()
