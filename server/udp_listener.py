import json
import socket
import threading

HOST = "0.0.0.0"
PORT = 5005

# Données partagées entre le listener UDP et Flask
latest_data: dict = {}
data_lock = threading.Lock()


def start(port: int = PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, port))
    print(f"[UDP] Listening on {HOST}:{port}")

    while True:
        try:
            raw, addr = sock.recvfrom(4096)
            parsed = json.loads(raw.decode("utf-8"))
            with data_lock:
                latest_data.update(parsed)
        except Exception as e:
            print(f"[UDP] Error: {e}")


def get_data() -> dict:
    with data_lock:
        return dict(latest_data)
