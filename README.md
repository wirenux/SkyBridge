# SkyBridge

A real-time Microsoft Flight Simulator mod that bridges in-game telemetry with external applications via UDP networking. Capture flight data, stream live screenshots, and synchronize multiple clients with zero latency.

## Features

- **Real-time Telemetry** - Live flight data streaming via UDP
- **Compact Encoding** - IP/Port compression using base62 for efficient network transfer
- **Multi-client Support** - Connect multiple dashboards and monitoring tools
- **Dashboard & Portal** - Web-based flight control and visualization

## Architecture

- **Server** - Python UDP listener and telemetry engine
- **Mod** - MSFS integration module
- **Frontend** - Dashboard, portal, and web assets

## Quick Start
