#define MyAppName "SkyBridge"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "WireNux"
#define MyPublishDir "..\mod\bin\Release\net10.0-windows\win-x64\publish"
#define MyServerDir "..\server\dist"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=SkyBridge_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcuts"; GroupDescription: "Additional icons:"

[Files]
; ── Mod C# ──────────────────────────────────────────────────────────────────
Source: "{#MyPublishDir}\SkyBridge.exe";                            DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyPublishDir}\SkyBridge.dll";                            DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyPublishDir}\SkyBridge.deps.json";                      DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyPublishDir}\SkyBridge.runtimeconfig.json";             DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyPublishDir}\Microsoft.FlightSimulator.SimConnect.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyPublishDir}\SimConnect.dll";                           DestDir: "{app}"; Flags: ignoreversion

; ── Serveur Python ───────────────────────────────────────────────────────────
Source: "{#MyServerDir}\SkyBridgeServer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Menu démarrer
Name: "{group}\SkyBridge (Mod)";    Filename: "{app}\SkyBridge.exe"
Name: "{group}\SkyBridge (Server)"; Filename: "{app}\SkyBridgeServer.exe"
Name: "{group}\Uninstall SkyBridge"; Filename: "{uninstallexe}"

; Bureau
Name: "{commondesktop}\SkyBridge (Mod)";    Filename: "{app}\SkyBridge.exe";       Tasks: desktopicon
Name: "{commondesktop}\SkyBridge (Server)"; Filename: "{app}\SkyBridgeServer.exe"; Tasks: desktopicon

[Run]
; Lance le serveur en arrière-plan puis le mod
Filename: "{app}\SkyBridgeServer.exe"; Description: "Launch SkyBridge Server"; Flags: nowait postinstall skipifsilent runasoriginaluser; Parameters: ""
Filename: "{app}\SkyBridge.exe";       Description: "Launch SkyBridge Mod";    Flags: nowait postinstall skipifsilent runasoriginaluser; Check: IsModChecked

[Code]
function IsModChecked: Boolean;
begin
  Result := True;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
