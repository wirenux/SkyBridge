import socket

import udp_listener
from base62 import decode, encode
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO

app = Flask(
    __name__,
    template_folder="../frontend/",
    static_folder="../frontend/assets",
    static_url_path="/assets",
)

socketio = SocketIO(app, cors_allowed_origins="*")


def get_local_ip():
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


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/index.html")


@app.route("/api/data")
def get_data():
    return jsonify(udp_listener.get_data())


@app.route("/api/decode/<code>", methods=["GET"])
def decode_code(code: str):
    try:
        ip, port = decode(code)
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
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/encode", methods=["POST"])
def encode_ip():
    try:
        data = request.json
        ip, port = data.get("ip"), data.get("port")
        if not ip or not port:
            return jsonify({"success": False, "error": "Missing IP or port"}), 400
        return jsonify(
            {"success": True, "ip": ip, "port": port, "code": encode(ip, int(port))}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/local-ip", methods=["GET"])
def get_local_ip_endpoint():
    try:
        local_ip = get_local_ip()
        port = request.args.get("port", 5000, type=int)
        code = encode(local_ip, port)
        return jsonify({"success": True, "ip": local_ip, "port": port, "code": code})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
