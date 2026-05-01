from base62 import decode, encode
from flask import Flask, jsonify, render_template, request

app = Flask(
    __name__,
    template_folder="../frontend/",
)


@app.route("/")
def web():
    return render_template("portal/index.html")


@app.route("/api/decode/<code>", methods=["GET"])
def decode_code(code: str):
    # Decode base62 code back to IP:port
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
