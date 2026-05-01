from base62 import decode, encode
from flask import Flask, jsonify, render_template, request
import socket

app = Flask(
    __name__,
    template_folder="../frontend/",
)

# Disable host header validation for local network access
app.config['ENV'] = 'development'
app.config['PREFERRED_URL_SCHEME'] = 'http'

@app.before_request
def before_request():
    # Allow requests from any host (necessary for local network access)
    pass


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


@app.route("/")
def web():
    return render_template("portal/index.html")


@app.route("/host")
def host():
    return render_template("portal/host.html")


@app.route("/api/decode/<code>", methods=["GET"])
def decode_code(code: str):
    # Decode base62 code back to IP:port
    try:
        ip, port = decode(code)
        print(f"SUCCESS: http://{ip}:{port}")
        return jsonify(
            {
                "success": True,
                "code": code,
                "ip": ip,
                "port": port,
                "link": f"http://{ip}:{port}",
            }
        )
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/encode", methods=["POST"])
def encode_ip():
    # Encode IP:port to base62 code
    try:
        data = request.json
        ip = data.get("ip")
        port = data.get("port")

        if not ip or not port:
            return jsonify({"success": False, "error": "Missing IP or port"}), 400

        code = encode(ip, int(port))
        return jsonify({"success": True, "ip": ip, "port": port, "code": code})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/local-ip", methods=["GET"])
def get_local_ip_endpoint():
    # Get local IP and optionally encode with port
    try:
        local_ip = get_local_ip()
        port = request.args.get("port", 5000, type=int)
        code = encode(local_ip, port)
        return jsonify({"success": True, "ip": local_ip, "port": port, "code": code})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
