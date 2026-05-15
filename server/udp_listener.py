import json
import socket
import threading

HOST = "0.0.0.0"
PORT = 5005

latest_data: dict = {}
data_lock = threading.Lock()
_socketio = None
_last_sent = {}


def init(sio):
    global _socketio
    _socketio = sio


def round_payload(data: dict) -> dict:
    skip = {"ap", "motors", "spoiler_armed"}
    result = {}
    for k, v in data.items():
        if k in skip:
            result[k] = v
        elif isinstance(v, float):
            result[k] = round(v, 2)
        else:
            result[k] = v
    return result


def start(port: int = PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    print(f"[UDP] Listening on {HOST}:{port}")

    while True:
        try:
            raw, _ = sock.recvfrom(4096)
            parsed = json.loads(raw.decode("utf-8"))
            with data_lock:
                latest_data.update(parsed)

            global _last_sent
            if parsed != _last_sent:
                _last_sent = parsed
                if _socketio:
                    _socketio.emit("flight_data", round_payload(parsed))
        except Exception as e:
            print(f"[UDP] Error: {e}")


def get_data() -> dict:
    with data_lock:
        return dict(latest_data)
