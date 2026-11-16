"""Minimales Web-Frontend für den Dobot Magician.

Start:  python app.py   ->   http://127.0.0.1:5000
"""
import contextlib
import importlib
import io
import threading

from flask import Flask, jsonify, render_template, request

import dobot_helper

# Module mit Ziffer am Anfang lassen sich nur über importlib laden.
jog = importlib.import_module("05_move_man")

# Aktion -> (Modul, Titel)
AKTIONEN = {
    "verbindung": ("01_verbindung_testen", "Position lesen"),
    "bewegung": ("02_erste_bewegung", "Erste Bewegung"),
    "quadrat": ("03_quadrat", "Quadrat fahren"),
    "saugnapf": ("04_greifer_saugnapf", "Saugnapf Test"),
}

app = Flask(__name__)
state = {"device": None, "port": None, "laeuft": None, "log": [], "alarme": []}
lock = threading.Lock()


def log(text):
    state["log"].append(text)
    del state["log"][:-200]


def verbunden():
    return state["device"] is not None


@app.get("/")
def index():
    return render_template("index.html", aktionen=AKTIONEN)


@app.post("/api/verbinden")
def verbinden():
    if verbunden():
        return jsonify(ok=True, meldung="Schon verbunden")
    port = dobot_helper.STANDARD_PORT or dobot_helper.finde_dobot_port()  # Suche: ~10 s
    if not port:
        return jsonify(ok=False, meldung="Kein Dobot gefunden (Treiber? eingeschaltet? DobotLink beendet?)"), 404
    try:
        state["device"] = dobot_helper.Dobot(port=port, verbose=False)
    except Exception as e:
        return jsonify(ok=False, meldung=f"Verbindung fehlgeschlagen: {e}"), 500
    state["port"] = port
    log(f"Verbunden mit {port}")
    return jsonify(ok=True, meldung=f"Verbunden mit {port}")


@app.post("/api/trennen")
def trennen():
    if state["laeuft"]:
        return jsonify(ok=False, meldung="Aktion läuft noch"), 409
    if verbunden():
        state["device"].close()
        state["device"] = None
        jog._ziel = None
        log("Getrennt")
    return jsonify(ok=True)


@app.get("/api/status")
def status():
    pose = None
    if verbunden() and not state["laeuft"] and lock.acquire(blocking=False):
        try:
            x, y, z, r, *_ = state["device"].pose()
            pose = dict(x=x, y=y, z=z, r=r)
            state["alarme"] = state["device"].alarme()
        except Exception as e:
            log(f"Statusfehler: {e}")
        finally:
            lock.release()
    return jsonify(verbunden=verbunden(), port=state["port"], laeuft=state["laeuft"],
                   pose=pose, alarme=state["alarme"], log=state["log"][-30:])


class _LiveLog(io.TextIOBase):
    """Leitet print()-Ausgaben der Programme sofort ins Protokoll (zeilenweise)."""
    def __init__(self):
        self.rest = ""

    def write(self, text):
        self.rest += text
        *zeilen, self.rest = self.rest.split("\n")
        for z in zeilen:
            log(z)
        return len(text)


def _lauf(modul):
    device = state["device"]
    try:
        with lock, contextlib.redirect_stdout(_LiveLog()):
            importlib.import_module(modul).ausfuehren(device)
    except dobot_helper.Abbruch:
        log("ABGEBROCHEN (Stopp)")
    except Exception as e:
        log(f"FEHLER: {e}")
        try:
            device.stopp()  # Warteschlange aufräumen
        except Exception:
            pass
    finally:
        jog._ziel = None
        state["laeuft"] = None


@app.post("/api/aktion/<name>")
def aktion(name):
    if name not in AKTIONEN:
        return jsonify(ok=False, meldung="Unbekannte Aktion"), 404
    if not verbunden():
        return jsonify(ok=False, meldung="Nicht verbunden"), 409
    if state["laeuft"]:
        return jsonify(ok=False, meldung="Es läuft schon eine Aktion"), 409
    modul, titel = AKTIONEN[name]
    state["laeuft"] = titel
    log(f"> {titel}")
    threading.Thread(target=_lauf, args=(modul,), daemon=True).start()
    return jsonify(ok=True)


@app.post("/api/stopp")
def api_stopp():
    """NOT-STOPP: bricht Programme und Verfahren sofort ab (ohne die Aktionssperre)."""
    if not verbunden():
        return jsonify(ok=False), 409
    try:
        state["device"].stopp()
        jog._ziel = None
        log("STOPP")
    except Exception as e:
        log(f"Stopp-Fehler: {e}")
        return jsonify(ok=False, meldung=str(e)), 500
    return jsonify(ok=True)


@app.post("/api/alarme_loeschen")
def api_alarme_loeschen():
    if verbunden() and not state["laeuft"]:
        with lock:
            state["device"].alarme_loeschen()
        state["alarme"] = []
        log("Alarme gelöscht")
    return jsonify(ok=True)


@app.post("/api/jog")
def api_jog():
    if not verbunden() or state["laeuft"]:
        return jsonify(ok=False), 409
    d = request.get_json()
    with lock:
        ziel = jog.jog_schritt(state["device"], d["achse"], int(d["richtung"]))
    return jsonify(ok=True, ziel=ziel)


@app.post("/api/jog/stopp")
def api_jog_stopp():
    if verbunden() and not state["laeuft"]:
        with lock:
            jog.jog_stopp(state["device"])
    return jsonify(ok=True)


if __name__ == "__main__":
    print("Frontend: http://127.0.0.1:5000  (Beenden mit Strg+C)")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
