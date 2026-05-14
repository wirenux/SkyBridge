import json
import math
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TARGET = ("127.0.0.1", 5005)

t = 0

while True:
    # Simulate smooth movement
    hdg = (t * 2) % 360
    pitch = math.sin(t * 0.05) * 15  # -15° to +15°
    bank = math.sin(t * 0.03) * 30  # -30° to +30°
    alt = 8500 + math.sin(t * 0.02) * 200
    vs = math.sin(t * 0.02) * 200 * 0.02 * 60  # fpm derived from alt change
    ias = 230 + math.sin(t * 0.01) * 10
    n1 = 82 + math.sin(t * 0.04) * 3

    payload = {
        "alt": alt,
        "alt_msl": alt,
        "alt_agl": alt - 2300,
        "hdg": hdg,
        "pitch": pitch,
        "bank": bank,
        "motors": [
            {"id": 1, "rpm": 0, "n1": n1, "is_jet": True},
            {"id": 2, "rpm": 0, "n1": n1 - 0.5, "is_jet": True},
        ],
        "gear": 0,
        "gs": ias + 15,
        "ias": ias,
        "tas": ias + 20,
        "mach": round(ias / 600, 3),
        "vs": vs,
        "lat": 48.85 + t * 0.01,
        "lon": 2.35 + t * 0.01,
        "fuel_gal": 4200 / 6.7 - t * 0.05,
        "flaps_index": 0,
        "flaps_deg": 0.0,
        "aoa": pitch * 0.4,
        "g": 1.0 + abs(math.sin(t * 0.03)) * 0.3,
        "ap": {
            "on": True,
            "alt_on": True,
            "alt_val": 9000,
            "ias_on": True,
            "ias_val": 230,
            "hdg_on": True,
            "hdg_val": 45,
        },
        "ts": int(time.time()),
    }

    sock.sendto(json.dumps(payload).encode(), TARGET)
    print(
        f"[mock] hdg={hdg:.0f}° pitch={pitch:.1f}° bank={bank:.1f}° alt={alt:.0f}ft ias={ias:.0f}kt"
    )

    t += 1
    time.sleep(0.5)
