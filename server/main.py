import os

from app import app

if __name__ == "__main__":
    # Bind to 0.0.0.0 to listen on ALL network interfaces (localhost + local network + external IP)
    # This allows access from:
    # - localhost/127.0.0.1 (your machine)
    # - 192.168.x.x (your local network/phone)
    # - Your machine's public IP (if applicable)
    print("\n🚀 SkyBridge is running!")
    print("Local access: http://127.0.0.1:5000")
    print("Local network access: http://192.168.1.232:5000")
    print("(Replace 192.168.1.232 with your actual local IP)\n")

    app.run(debug=True, host="0.0.0.0", port=5001)
