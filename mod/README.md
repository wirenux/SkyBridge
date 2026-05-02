copy file located at C:\MSFS SDK\SimConnect SDK\lib\managed\Microsoft.FlightSimulator.SimConnect.dll to lib/

copy file located at C:\MSFS SDK\SimConnect SDK\lib\SimConnect.dll to lib/

## Build:

```bash
dotnet publish -c Release -r win-x64 --self-contained false
```

then :

```bash
.\bin\Release\net10.0-windows\win-x64\publish\SkyBridge
```
