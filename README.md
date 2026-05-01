# SkyBridge - Roadmap & Implementation Plan

## Project Overview
SkyBridge is a real-time flight simulator mod that bridges in-game telemetry with external applications via UDP networking. Capture flight data, screenshots.

---

## Phase 1: Mod In-Game

### Simulator Support Strategy
- **MSFS 2020/2024** → C# + SimConnect SDK (primary target)
- **X-Plane 11/12** → C/C++ + X-Plane SDK
- **DCS World** → Lua (built-in export scripts)
- **Kerbal Space Program** → C# (Unity plugin)

### Telemetry Data to Expose
- **Altitude**: MSL & AGL
- **Heading**: Magnetic & True
- **Airspeed**: IAS, TAS, GS
- **Vertical Speed**: fpm or m/s
- **Motor Power**: Percentage per engine
- **Motor State**: ON / OFF / FAULT per engine
- **Position**: Latitude & Longitude
- **Screenshot**: PNG capture of game render

### UDP Communication Protocol
- Socket: UDP local (e.g., 127.0.0.1:5005)
- Frequency: 1 Hz (adjustable)
- Payload Format (JSON):
```json
{
  "alt": 3500,
  "hdg": 270,
  "ias": 145,
  "vs": -200,
  "lat": 48.85,
  "lon": 2.35,
  "motors": [
    {"id": 1, "pct": 82, "state": "ON"},
    {"id": 2, "pct": 78, "state": "ON"}
  ]
}
```

---

## Phase 2: Local Server

### Technology Stack
- **Language**: Python 3
- **Framework**: Flask (lightweight, zero-config)
- **Real-time**: Flask-SocketIO (WebSocket)
- **Image Processing**: Pillow (PNG encode/decode)
- **Optional**: qrcode (QR code generation)

### Python Dependencies
```
flask
flask-socketio
pillow
qrcode
python-socketio
```

### Base62 Encoding ✅
- **Goal**: Encode IP + port into 9 alphanumeric characters
- **Alphabet**: 0-9 a-z A-Z (62 symbols)
- **Capacity**: 62^9 ≈ 13.8 trillion combinations
- **Example**: 192.168.1.42:8080 → 'SN17xl9Y0'
- **Storage**: In-memory dict mapping code → URL

### Flask API Endpoints
- `GET /` → Main dashboard (real-time HTML)
- `GET /api/data` → Raw JSON telemetry
- `GET /api/screenshot` → PNG image
- `POST /api/code` → Generate short code
- `GET /decode/<code>` → Redirect to decoded URL

### Server Architecture
1. UDP listener thread (receives mod data)
2. Flask HTTP server (serves API + frontend)
3. WebSocket handler (pushes live updates)
4. Screenshot capture & encoding pipeline

---

## Phase 3: Mobile Client (PWA)

### Approach
- Progressive Web App (PWA) - no native app needed
- Hosted on same Flask server
- HTML/JS based portal for code entry

### User Flow
1. Mobile user opens browser
2. Navigates to portal/code-entry page
3. Enters 9-character code from mod
4. JavaScript calls `GET /decode/<code>`
5. Client redirected to `http://192.168.X.X:PORT` (dashboard)

### Implementation Options

**Option A: Direct Redirection** (Recommended)
- Simpler implementation
- Always works (HTTP on LAN)
- Pro: Clean, no browser limitations
- Con: Leaves portal page

**Option B: Iframe Embedding**
- Keeps portal visible
- Con: HTTPS/HTTP mixed content issues
- Con: Some mobile browsers block HTTP iframes from HTTPS

**Recommendation**: Use direct redirection for LAN-only access.

### Key Features
- QR code display for easy sharing
- Code validation (9 chars, alphanumeric)
- Mobile-responsive design
- Offline-first if needed (service worker)

---

## Stack Summary

| Layer | Component | Technology |
|-------|-----------|------------|
| **Mod** | Flight data capture | C# (MSFS) / C++ (X-Plane) / Lua (DCS) |
| **Network** | Data transmission | UDP JSON |
| **Server** | HTTP API | Flask + SocketIO |
| **Telemetry** | Data encoding | Custom base62 (9 chars) |
| **Frontend** | Dashboard | HTML/CSS/JS + WebSocket |
| **Mobile** | Portal | PWA (HTML/JS) |

---

## Development Priorities
1. ✅ Base62 encoding
2. Python server scaffold (Flask setup)
3. UDP listener implementation
4. API endpoints (data, screenshot, code)
5. Dashboard frontend
6. Mobile PWA portal
7. Multi-simulator support expansion
