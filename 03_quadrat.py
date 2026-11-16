"""Der Dobot zeichnet (in der Luft) ein Quadrat. Passe SEITE und HOEHE an."""

SEITE = 60      # Kantenlänge in mm
HOEHE = 50      # z-Wert in mm
MITTE_X = 200   # Abstand zur Basis in mm
MITTE_Y = 0


def ausfuehren(device):
    device.speed(100, 100)
    h = SEITE / 2
    ecken = [
        (MITTE_X - h, MITTE_Y - h),
        (MITTE_X + h, MITTE_Y - h),
        (MITTE_X + h, MITTE_Y + h),
        (MITTE_X - h, MITTE_Y + h),
        (MITTE_X - h, MITTE_Y - h),
    ]
    for nr, (ex, ey) in enumerate(ecken, start=1):
        print(f"Punkt {nr}/{len(ecken)}: x={ex:.0f} y={ey:.0f} z={HOEHE}")
        device.move_to(ex, ey, HOEHE, 0, wait=True)
    print("Quadrat fertig.")


if __name__ == "__main__":
    from dobot_helper import verbinde

    device = verbinde()
    ausfuehren(device)
    device.close()
