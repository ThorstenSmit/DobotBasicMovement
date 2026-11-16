"""Saugnapf ein-/ausschalten (nur mit angebautem Saugnapf-Aufsatz und Luftschlauch).
Für den Greifer: device.grip(True) = schließen, device.grip(False) = öffnen."""
import time


def ausfuehren(device):
    print("Saugnapf an ...")
    device.suck(True)    # Pumpe an
    time.sleep(2)
    device.suck(False)   # Pumpe aus
    print("Saugnapf aus.")


if __name__ == "__main__":
    from dobot_helper import verbinde

    device = verbinde()
    ausfuehren(device)
    device.close()
