# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("../frontend", "frontend"),
    ],
    hiddenimports=[
        "engineio.async_drivers.threading",
        "socketio.async_drivers.threading",
        "flask_socketio",
        "engineio",
        "socketio",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="SkyBridgeServer",
    debug=False,
    strip=False,
    upx=True,
    console=True,
)
