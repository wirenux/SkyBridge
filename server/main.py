import threading

import udp_listener
from app import app, socketio

if __name__ == "__main__":
    udp_listener.init(socketio)
    t = threading.Thread(target=udp_listener.start, daemon=True)
    t.start()
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, use_reloader=False)
