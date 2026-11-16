"""Kleine Hilfsfunktionen, damit die Beispielskripte kurz und lesbar bleiben."""
import sys
from serial.tools import list_ports
import struct
import threading
import time
import pydobot
from pydobot.message import Message


class Abbruch(Exception):
    """Wird ausgelöst, wenn ein laufendes Programm mit stopp() abgebrochen wurde."""


def korrigiere_pruefsumme(msg):
    """pydobot berechnet die Prüfsumme bei ca. 1 von 128 Nachrichten falsch (z. B. Ziel
    x=170, y=-30, z=50) und der Dobot verwirft den Befehl dann stillschweigend.
    Richtig: (256 - Summe(id, ctrl, params) % 256) % 256."""
    msg.checksum = None
    msg.refresh()                      # setzt Länge (und die fehlerhafte Prüfsumme)
    summe = msg.id + msg.ctrl + sum(msg.params)
    msg.checksum = (256 - summe % 256) % 256
    return msg


class Dobot(pydobot.Dobot):
    """pydobot mit robusterem Lesen, Abbruch (stopp) und Alarmabfrage.

    Fixes gegenüber pydobot:
    - berechnet die Prüfsumme korrekt (pydobot-Fehler: manche Befehle wurden still verworfen)
    - wartet bis zu 2 s auf die Antwort (pydobot nur 0,1 s -> "'NoneType' ... 'params'")
    - gibt die interne Sperre auch bei Fehlern wieder frei (sonst hängt alles für immer)
    - wait=True-Bewegungen lassen sich mit stopp() abbrechen und haben ein Zeitlimit
    """

    def __init__(self, port, verbose=False):
        self._abbruch = threading.Event()
        self._wartende = 0
        super().__init__(port, verbose)

    def _send_message(self, msg):
        self.ser.reset_input_buffer()          # alte, unerwartete Daten verwerfen
        korrigiere_pruefsumme(msg)
        self._letzte_id = msg.id
        super()._send_message(msg)

    def _read_message(self):
        ende = time.time() + 2.0
        time.sleep(0.1)
        b = b""
        while True:
            b += self.ser.read_all()
            # Frame: AA AA len ... checksum  -> Gesamtlänge = len + 4
            if len(b) >= 3 and len(b) >= b[2] + 4:
                return Message(b)
            if time.time() > ende:
                if len(b) == 0:
                    raise TimeoutError(f"Keine Antwort vom Dobot auf Befehl-ID {self._letzte_id} "
                                       "(eingeschaltet? Alarm? Kabel? DobotLink/DobotLab beendet?)")
                return Message(b)
            time.sleep(0.02)

    def _send_command(self, msg, wait=False, timeout=120):
        with self.lock:                        # wird auch bei Fehlern freigegeben
            self._send_message(msg)
            response = self._read_message()
        if not wait:
            return response

        erwartet = struct.unpack_from('L', response.params, 0)[0]
        ende = time.time() + timeout
        self._wartende += 1
        try:
            while True:
                if self._abbruch.is_set():
                    raise Abbruch("Abgebrochen")
                if time.time() > ende:
                    raise TimeoutError("Bewegung dauert zu lange (Alarm? Ziel unerreichbar?)")
                if self._get_queued_cmd_current_index() == erwartet:
                    return response
                time.sleep(0.1)
        finally:
            self._wartende -= 1

    def stopp(self):
        """Stoppt die Bewegung sofort, leert die Warteschlange und bricht wartende Programme ab."""
        self._abbruch.set()
        try:
            self._set_queued_cmd_stop_exec()
            self._set_queued_cmd_clear()
            self._set_queued_cmd_start_exec()
            ende = time.time() + 3
            while self._wartende > 0 and time.time() < ende:
                time.sleep(0.05)
        finally:
            self._abbruch.clear()

    def alarme(self):
        """Liste aktiver Alarm-Bytes (leer = kein Alarm)."""
        msg = Message()
        msg.id = 20            # GetAlarmsState
        msg.ctrl = 0
        antwort = self._send_command(msg)
        return [f"{i}:{b:02X}" for i, b in enumerate(antwort.params) if b]

    def alarme_loeschen(self):
        msg = Message()
        msg.id = 21            # ClearAllAlarmsState
        msg.ctrl = 1
        self._send_command(msg)


# Wenn du deinen COM-Port kennst (Geräte-Manager), trage ihn hier ein, z. B. "COM6".
# Dann entfällt die automatische Suche, die auf manchen PCs ~10 Sekunden dauert
# (wegen Bluetooth-Ports).
STANDARD_PORT = None

# Typische Namen der USB-Seriell-Chips, die im Dobot Magician stecken
BEKANNTE_CHIPS = ("CH340", "CH341", "CP210", "SILICON LABS", "USB-SERIAL", "DOBOT")


def alle_ports():
    """Gibt alle gefundenen COM-Ports als Liste von (Port, Beschreibung) zurück."""
    return [(p.device, p.description) for p in list_ports.comports()]


def finde_dobot_port(ports=None):
    """Sucht den COM-Port des Dobot. Gibt z. B. 'COM3' zurück oder None."""
    for port, beschreibung in (ports if ports is not None else alle_ports()):
        if any(name in beschreibung.upper() for name in BEKANNTE_CHIPS):
            return port
    return None


def verbinde(port=None):
    """Verbindet sich mit dem Dobot. Ohne Angabe wird der Port automatisch gesucht."""
    port = port or STANDARD_PORT or finde_dobot_port()
    if port is None:
        print("FEHLER: Kein Dobot gefunden.")
        print("Gefundene Ports:", alle_ports() or "keine")
        print("Tipps: Dobot eingeschaltet? USB-Kabel verbunden? Treiber installiert?")
        print("       Läuft DobotStudio noch? (Das blockiert den Port - bitte schließen!)")
        sys.exit(1)
    print(f"Verbinde mit Dobot auf {port} ...")
    return Dobot(port=port, verbose=False)
