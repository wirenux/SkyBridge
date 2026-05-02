import threading

import udp_listener
from app import app

t = threading.Thread(target=udp_listener.start, daemon=True)
t.start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=False)
