# SkyBridge

> Real-time flight dashboard for MSFS 2020 — stream telemetry from your simulator to any device on your local network.

---

## Overview

SkyBridge connects Microsoft Flight Simulator 2020 to a mobile-friendly web dashboard via a local network. A C# mod reads live flight data through SimConnect and streams it over UDP to a Python server, which pushes it to any browser on your LAN in real time via WebSocket.

---

## Features

- **Live telemetry** — Altitude (MSL/AGL), heading, IAS/TAS/GS/Mach, vertical speed, position, fuel, AOA, G-force, OAT, trim, spoilers
- **Engine data** — RPM or N1% per engine (up to 8), auto-detects piston / jet / turboprop / helicopter
- **Autopilot status** — AP on/off, target ALT / IAS / HDG
- **Instruments** — Attitude indicator (ADI) and heading tape with smooth animation
- **Live map** — OpenStreetMap with plane marker, follow mode, and airport overlays
- **Gear & flaps** — position and state
- **9-character access code** — encode your local IP + port into a short alphanumeric code to share with any device on the network
- **WebSocket push** — no polling, data arrives as soon as the sim sends it
- **Collapsible cards** — clean mobile UI, hide what you don't need

---

## Architecture

```
MSFS 2020
  └── SimConnect SDK
        └── SkyBridge.exe  (C# mod)
              └── UDP:5005 ──▶ SkyBridgeServer.exe  (Python + Flask)
                                    └── WebSocket ──▶ Browser (mobile / desktop)
```

---

## Stack

| Layer | Technology |
|-------|------------|
| Mod | C# (.NET 10) + SimConnect SDK |
| Transport | UDP (sim -> server) + WebSocket (server -> browser) |
| Server | Python 3 - Flask - Flask-SocketIO |
| Frontend | HTML - CSS - Vanilla JS - Leaflet.js |
| Encoding | Custom base62 (9 chars = IP + port) |
| Installer | Inno Setup |

---

## Getting Started

### Prerequisites (If you want to build from source)

**On the Windows PC running MSFS 2020:**
- MSFS 2020 with Developer Mode enabled (Options → General → Developers)
- MSFS SDK installed (Dev Mode menu → SDK Download)
- .NET 10 Runtime

**On any machine for the server (can be the same PC or a Mac/Linux on the same network):**
- Python 3.9+

---

### Installation (recommended)

Download `SkyBridge_Setup.exe` from the [releases page](https://github.com/wirenux/SkyBridge/releases) and run it. The installer includes both the mod and the server.

---

### Manual Setup

#### 1. Install server dependencies

```bash
cd server
pip install -r requirements.txt
```

#### (Optional) 2. Configure the UDP target

##### If the server runs on the same PC as MSFS, keep `127.0.0.1` and don't modify anything !.

In `mod/src/Program.cs`, set the IP of the machine running the server:

```csharp
var udpEndpoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 5005);
```


#### 3. Build mod + server

```powershell
.\build.ps1
```

---

### Running

**Start the server** (on the host machine):

```bash
cd server
python main.py
```

The terminal will display the ASCII logo, your local IP, and the 9-character access code.

**Start the mod** (on the Windows PC with MSFS):

```
SkyBridge.exe
```

Launch MSFS 2020, load a flight — data will start streaming immediately.

**Access the dashboard** from any device on the same network:

Use the portal to enter the 9-character code:

```
http://<server-ip>:5000/
```

---

### Testing without MSFS

```bash
python tools/mock_sim.py
```

Sends simulated flight data to the server so you can develop and test the dashboard without launching the simulator.

---

## Access Code System

SkyBridge encodes your server's local IP and port into a 9-character alphanumeric code using base62.

```
192.168.1.42:5000  →  HddRxl9Y0
```

Share this code with anyone on your local network. They enter it at `/` (the portal page) and get redirected straight to your dashboard — no need to know your IP.

**Alphabet:** `0-9 a-z A-Z` (62 symbols)  
**Capacity:** 62⁹ ≈ 13.8 trillion combinations

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Portal — enter access code |
| `GET` | `/host` | Generate your access code |
| `GET` | `/dashboard` | Live flight dashboard |
| `GET` | `/api/data` | Latest telemetry as JSON |
| `GET` | `/api/local-ip?port=5000` | Get local IP + encoded code |
| `GET` | `/api/decode/<code>` | Decode a 9-char code → IP:port |

---

## Telemetry Payload

```json
{
  "alt": 8500,
  "alt_msl": 8500,
  "alt_agl": 6200,
  "hdg": 270.0,
  "pitch": -2.1,
  "bank": 0.0,
  "ias": 245.0,
  "tas": 268.0,
  "gs": 251.0,
  "mach": 0.412,
  "vs": -200.0,
  "lat": 48.850000,
  "lon": 2.350000,
  "fuel_gal": 320.5,
  "aoa": 3.2,
  "g": 1.01,
  "oat": -32.5,
  "trim_pct": 2.1,
  "spoiler_pct": 0.0, "spoiler_armed": false,
  "gear": 0.0,
  "flaps_index": 0,
  "flaps_deg": 0.0,
  "motors": [
    { "id": 1, "rpm": 0, "n1": 84.2, "is_jet": true },
    { "id": 2, "rpm": 0, "n1": 83.9, "is_jet": true }
  ],
  "ap": {
    "on": true,
    "alt_on": true,  "alt_val": 9000,
    "ias_on": true,  "ias_val": 245,
    "hdg_on": false, "hdg_val": 0
  },
  "ts": 1714500000
}
```

---

## License

MIT - see [LICENSE](./LICENSE).

---

*Built by [WireNux](https://github.com/wirenux)*
