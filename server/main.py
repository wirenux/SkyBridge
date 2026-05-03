import logging
import os
import sys
import threading

import udp_listener
from app import app, get_local_ip, socketio
from base62 import encode

DEBUG = "--debug" in sys.argv

if not DEBUG:
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    logging.getLogger("socketio").setLevel(logging.ERROR)
    logging.getLogger("engineio").setLevel(logging.ERROR)
    app.logger.setLevel(logging.ERROR)

    class NoTLSFilter(logging.Filter):
        def filter(self, record):
            msg = record.getMessage()
            return not any(
                x in msg
                for x in [
                    "Bad request version",
                    "Bad HTTP/0.9",
                    "Bad request syntax",
                ]
            )

    log.addFilter(NoTLSFilter())

if __name__ == "__main__":
    udp_listener.init(socketio)
    t = threading.Thread(target=udp_listener.start, daemon=True)
    t.start()

    import time

    flask_thread = threading.Thread(
        target=lambda: socketio.run(
            app, debug=DEBUG, host="0.0.0.0", port=5000, use_reloader=False
        ),
        daemon=True,
    )
    flask_thread.start()

    time.sleep(0.5)
    os.system("cls" if os.name == "nt" else "clear")

    print(r"""
  ███████╗██╗  ██╗██╗   ██╗██████╗ ██████╗ ██╗██████╗  ██████╗ ███████╗
  ██╔════╝██║ ██╔╝╚██╗ ██╔╝██╔══██╗██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝
  ███████╗█████╔╝  ╚████╔╝ ██████╔╝██████╔╝██║██║  ██║██║  ███╗█████╗
  ╚════██║██╔═██╗   ╚██╔╝  ██╔══██╗██╔══██╗██║██║  ██║██║   ██║██╔══╝
  ███████║██║  ██╗   ██║   ██████╔╝██║  ██║██║██████╔╝╚██████╔╝███████╗
  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝
""")
    print("  v1.0.0 · WireNux")

    if DEBUG:
        print("  [DEBUG MODE]")
    print()

    PORT = 5000
    local_ip = get_local_ip()
    code = encode(local_ip, PORT)

    print(f"  Server  : http://{local_ip}:{PORT}")
    print(f"  Code    : {code}")
    print()

    flask_thread.join()
