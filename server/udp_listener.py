import json
import socket
import threading

HOST = "0.0.0.0"
PORT = 5005

latest_data: dict = {}
data_lock = threading.Lock()
_socketio = None  # injecté depuis main.py


def init(sio):
    global _socketio
    _socketio = sio


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
            if _socketio:
                _socketio.emit("flight_data", parsed)
        except Exception as e:
            print(f"[UDP] Error: {e}")


def get_data() -> dict:
    with data_lock:
        return dict(latest_data)
