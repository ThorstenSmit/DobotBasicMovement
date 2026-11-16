"""Gibt die aktuelle Position aus. Der Arm bewegt sich NICHT."""


def ausfuehren(device):
    x, y, z, r, j1, j2, j3, j4 = device.pose()
    print(f"Position: x={x:.1f} y={y:.1f} z={z:.1f} r={r:.1f}")
    print(f"Gelenke:  j1={j1:.1f} j2={j2:.1f} j3={j3:.1f} j4={j4:.1f}")
    print("Verbindung OK!")


if __name__ == "__main__":
    from dobot_helper import verbinde

    device = verbinde()
    ausfuehren(device)
    device.close()
