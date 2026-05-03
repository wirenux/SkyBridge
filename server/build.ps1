$ROOT = "C:\Users\louis\Developer\SkyBridge"

Write-Host "Building Python server..." -ForegroundColor Cyan
Set-Location "$ROOT\server"
python -m PyInstaller SkyBridgeServer.spec
if ($LASTEXITCODE -ne 0) { Write-Host "Server build failed" -ForegroundColor Red; exit 1 }

Write-Host "Building C# mod..." -ForegroundColor Cyan
Set-Location "$ROOT\mod"
dotnet publish -c Release -r win-x64 --self-contained false
if ($LASTEXITCODE -ne 0) { Write-Host "Mod build failed" -ForegroundColor Red; exit 1 }

Write-Host "Copying SimConnect DLLs..." -ForegroundColor Cyan
Copy-Item "$ROOT\mod\lib\Microsoft.FlightSimulator.SimConnect.dll" "$ROOT\mod\bin\Release\net10.0-windows\win-x64\publish\" -Force
Copy-Item "$ROOT\mod\lib\SimConnect.dll" "$ROOT\mod\bin\Release\net10.0-windows\win-x64\publish\" -Force
