using System;
using System.Runtime.InteropServices;
using System.Threading;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using Microsoft.FlightSimulator.SimConnect;

SimConnect? sim = null;
bool connected = false;
bool isJetAircraft = false;

var udpClient = new UdpClient();
var udpEndpoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 5005);

while (true)
{
    if (!connected)
    {
        try
        {
            sim = new SimConnect("FlightDataMod", IntPtr.Zero, 0x0402, null, 0);

            sim.OnRecvOpen += (s, d) =>
            {
                Console.WriteLine($"[OK] Connecté à : {d.szApplicationName}");

                void Add(string var, string unit) =>
                    sim.AddToDataDefinition(DEFINE_ID.FlightData, var, unit,
                        SIMCONNECT_DATATYPE.FLOAT64, 0, SimConnect.SIMCONNECT_UNUSED);

                Add("PLANE ALTITUDE", "feet");
                Add("PLANE ALT ABOVE GROUND", "feet");
                Add("PLANE HEADING DEGREES MAGNETIC", "degrees");
                Add("NUMBER OF ENGINES", "number");

                Add("GENERAL ENG RPM:1", "rpm");
                Add("GENERAL ENG RPM:2", "rpm");
                Add("GENERAL ENG RPM:3", "rpm");
                Add("GENERAL ENG RPM:4", "rpm");
                Add("GENERAL ENG RPM:5", "rpm");
                Add("GENERAL ENG RPM:6", "rpm");
                Add("GENERAL ENG RPM:7", "rpm");
                Add("GENERAL ENG RPM:8", "rpm");

                Add("TURB ENG N1:1", "percent");
                Add("TURB ENG N1:2", "percent");
                Add("TURB ENG N1:3", "percent");
                Add("TURB ENG N1:4", "percent");
                Add("TURB ENG N1:5", "percent");
                Add("TURB ENG N1:6", "percent");
                Add("TURB ENG N1:7", "percent");
                Add("TURB ENG N1:8", "percent");

                Add("ROTOR RPM:1", "rpm");
                Add("GPS GROUND SPEED", "knots");
                Add("AIRSPEED INDICATED", "knots");
                Add("AIRSPEED TRUE", "knots");
                Add("AIRSPEED MACH", "mach");
                Add("GEAR TOTAL PCT EXTENDED", "percent");
                Add("VERTICAL SPEED", "feet per minute");
                Add("PLANE LATITUDE", "degrees");
                Add("PLANE LONGITUDE", "degrees");
                Add("FUEL TOTAL QUANTITY WEIGHT", "pounds");
                Add("INCIDENCE ALPHA", "degrees");
                Add("G FORCE", "gforce");
                Add("AUTOPILOT MASTER", "bool");
                Add("AUTOPILOT ALTITUDE LOCK VAR:1", "feet");
                Add("AUTOPILOT ALTITUDE LOCK VAR:2", "feet");
                Add("AUTOPILOT ALTITUDE LOCK VAR:3", "feet");
                Add("AUTOPILOT AIRSPEED HOLD VAR", "knots");
                Add("AUTOPILOT HEADING LOCK DIR", "degrees");
                Add("FLAPS HANDLE INDEX", "number");
                Add("TRAILING EDGE FLAPS LEFT ANGLE", "degrees");
                Add("ATTITUDE INDICATOR PITCH DEGREES", "degrees");
                Add("ATTITUDE INDICATOR BANK DEGREES", "degrees");

                sim.RegisterDataDefineStruct<FlightData>(DEFINE_ID.FlightData);
                sim.RequestDataOnSimObject(REQUEST_ID.FlightData, DEFINE_ID.FlightData,
                    SimConnect.SIMCONNECT_OBJECT_ID_USER,
                    SIMCONNECT_PERIOD.SECOND,
                    SIMCONNECT_DATA_REQUEST_FLAG.DEFAULT,
                    0, 1, 0);
            };

            sim.OnRecvQuit += (s, d) => { Console.WriteLine("[!] MSFS fermé."); connected = false; isJetAircraft = false; };
            sim.OnRecvException += (s, d) => Console.WriteLine($"[ERR] {d.dwException}");

            sim.OnRecvSimobjectData += (s, d) =>
            {
                var f = (FlightData)d.dwData[0];

                // ── Altitude ────────────────────────────────────────────────
                string altStr = f.AGL < 1000
                    ? $"{f.AGL:F0} ft AGL"
                    : $"{f.ALT:F0} ft MSL";

                // ── Engine ──────────────────────────────────────────────────
                int engCount = (int)f.EngineCount;
                if (!isJetAircraft)
                    isJetAircraft = f.N1_1 > 0.1 || f.N1_2 > 0.1 || f.N1_3 > 0.1 || f.N1_4 > 0.1 ||
                                    f.N1_5 > 0.1 || f.N1_6 > 0.1 || f.N1_7 > 0.1 || f.N1_8 > 0.1;

                bool isJet = isJetAircraft;
                bool isRotor = f.RotorRPM > 1;

                var engLines = new System.Text.StringBuilder();
                if (isRotor)
                {
                    engLines.AppendLine($"║  ROTOR   : {f.RotorRPM:F0} rpm{"",-15}║");
                }
                else
                {
                    for (int i = 1; i <= engCount; i++)
                    {
                        double rpm = i switch { 1 => f.RPM1, 2 => f.RPM2, 3 => f.RPM3, 4 => f.RPM4, 5 => f.RPM5, 6 => f.RPM6, 7 => f.RPM7, _ => f.RPM8 };
                        double n1 = i switch { 1 => f.N1_1, 2 => f.N1_2, 3 => f.N1_3, 4 => f.N1_4, 5 => f.N1_5, 6 => f.N1_6, 7 => f.N1_7, _ => f.N1_8 };
                        string val = isJet ? $"N1  ENG{i}: {n1:F1}%" : $"RPM ENG{i}: {rpm:F0}";
                        engLines.Append($"║  {val,-33}║\n");
                    }
                }

                // ── Autopilot ───────────────────────────────────────────────
                bool apOn = f.AP > 0.5;
                // string apAlt = f.APAltOn > 0.5 ? $"ALT {f.APAlt:F0} ft" : "ALT ---";
                // string apIas = f.APIasOn > 0.5 ? $"IAS {f.APIas:F0} kt" : "IAS ---";
                // string apHdg = f.APHdgOn > 0.5 ? $"HDG {f.APHdg:F0}°" : "HDG ---";

                // ── DEBUG ───────────────────────────────────────────────────
                // Console.Clear();
                // Console.WriteLine("╔══════════════════════════════════╗");
                // Console.WriteLine("║      SkyBridge · Live Data       ║");
                // Console.WriteLine("╠══════════════════════════════════╣");
                // Console.WriteLine($"║  ALT     : {altStr,-23}║");
                // Console.WriteLine($"║  HDG     : {f.HDG:F1}°{"",-22}║");
                // Console.Write(engLines.ToString().TrimEnd('\n'));
                // Console.WriteLine();
                // Console.WriteLine($"║  FLAPS   : {f.FlapsIndex:F0} ({f.FlapsDeg:F1}°){"",-14}║");
                // Console.WriteLine("╠══════════════════════════════════╣");
                // Console.WriteLine($"║  GS      : {f.GS:F1} kt{"",-20}║");
                // Console.WriteLine($"║  IAS     : {f.IAS:F1} kt{"",-20}║");
                // Console.WriteLine($"║  TAS     : {f.TAS:F1} kt{"",-20}║");
                // Console.WriteLine($"║  MACH    : {f.Mach:F3}{"",-22}║");
                // Console.WriteLine("╠══════════════════════════════════╣");
                // Console.WriteLine($"║  VS      : {f.VS:F0} fpm{"",-19}║");
                // Console.WriteLine($"║  LAT     : {f.Lat:F6}{"",-22}║");
                // Console.WriteLine($"║  LON     : {f.Lon:F6}{"",-22}║");
                // Console.WriteLine($"║  FUEL    : {f.Fuel:F1} lbs{"",-19}║");
                // Console.WriteLine($"║  AOA     : {f.AOA:F2}°{"",-22}║");
                // Console.WriteLine($"║  G       : {f.G:F2} g{"",-22}║");
                // Console.WriteLine("╠══════════════════════════════════╣");
                // Console.WriteLine($"║  AP      : {(apOn ? "ON " : "OFF"),-23}║");
                // if (apOn)
                // {
                //     Console.WriteLine($"║    {apAlt,-30}║");
                //     Console.WriteLine($"║    {apIas,-30}║");
                //     Console.WriteLine($"║    {apHdg,-30}║");
                // }
                // Console.WriteLine("╚══════════════════════════════════╝");

                // ── UDP payload ─────────────────────────────────────────────
                var payload = new
                {
                    alt = f.AGL < 1000 ? f.AGL : f.ALT,
                    alt_msl = f.ALT,
                    alt_agl = f.AGL,
                    hdg = f.HDG,
                    motors = Enumerable.Range(1, (int)f.EngineCount).Select(i => new
                    {
                        id = i,
                        rpm = i switch { 1 => f.RPM1, 2 => f.RPM2, 3 => f.RPM3, 4 => f.RPM4, 5 => f.RPM5, 6 => f.RPM6, 7 => f.RPM7, _ => f.RPM8 },
                        n1 = i switch { 1 => f.N1_1, 2 => f.N1_2, 3 => f.N1_3, 4 => f.N1_4, 5 => f.N1_5, 6 => f.N1_6, 7 => f.N1_7, _ => f.N1_8 },

                        is_jet = isJetAircraft,
                    }).ToArray(),
                    gear = f.GearPercent,
                    gs = f.GS,
                    ias = f.IAS,
                    tas = f.TAS,
                    mach = f.Mach,
                    vs = f.VS,
                    lat = f.Lat,
                    lon = f.Lon,
                    fuel_gal = f.Fuel / 6.7,
                    flaps_index = (int)f.FlapsIndex,
                    flaps_deg = f.FlapsDeg,
                    aoa = f.AOA,
                    g = f.G,
                    pitch = f.Pitch,
                    bank = f.Bank,
                    ap = new
                    {
                        on = f.AP > 0.5,
                        alt_val = new[] { f.APAlt1, f.APAlt2, f.APAlt3 }.Where(v => v != 10000).DefaultIfEmpty(10000).Max(),
                        alt_on = f.AP > 0.5,
                        ias_val = f.APIas,
                        ias_on = f.AP > 0.5 && f.APIas > 0,
                        hdg_val = f.APHdg,
                        hdg_on = f.AP > 0.5,
                    },
                    ts = DateTimeOffset.UtcNow.ToUnixTimeSeconds()

                };
                var json = JsonSerializer.Serialize(payload);
                var bytes = Encoding.UTF8.GetBytes(json);
                udpClient.Send(bytes, bytes.Length, udpEndpoint);
            };

            connected = true;
        }
        catch
        {
            Console.WriteLine("[...] MSFS non détecté, retry dans 5s");
            // Thread.Sleep(5000);
            continue;
        }
    }

    try { sim?.ReceiveMessage(); }
    catch { connected = false; }

    Thread.Sleep(50);
}

enum DEFINE_ID { FlightData }
enum REQUEST_ID { FlightData }

[StructLayout(LayoutKind.Sequential, Pack = 1)]
struct FlightData
{
    public double ALT;           // PLANE ALTITUDE
    public double AGL;           // PLANE ALT ABOVE GROUND
    public double HDG;           // PLANE HEADING DEGREES MAGNETIC
    public double EngineCount;   // NUMBER OF ENGINES
    public double RPM1, RPM2, RPM3, RPM4, RPM5, RPM6, RPM7, RPM8;
    public double N1_1, N1_2, N1_3, N1_4, N1_5, N1_6, N1_7, N1_8;
    public double RotorRPM;      // ROTOR RPM:1
    public double GS;            // GPS GROUND SPEED
    public double IAS;           // AIRSPEED INDICATED
    public double TAS;           // AIRSPEED TRUE
    public double Mach;          // AIRSPEED MACH
    public double GearPercent;   // GEAR TOTAL PCT EXTENDED  ← ici, pas après Mach dans l'ancienne
    public double VS;            // VERTICAL SPEED
    public double Lat;           // PLANE LATITUDE
    public double Lon;           // PLANE LONGITUDE
    public double Fuel;          // FUEL TOTAL QUANTITY WEIGHT
    public double AOA;           // INCIDENCE ALPHA
    public double G;             // G FORCE
    public double AP;            // AUTOPILOT MASTER
    public double APAlt1;    // AUTOPILOT ALTITUDE LOCK VAR:1
    public double APAlt2;    // AUTOPILOT ALTITUDE LOCK VAR:2
    public double APAlt3;    // AUTOPILOT ALTITUDE LOCK VAR:3
    public double APIas;         // AUTOPILOT AIRSPEED HOLD VAR
    public double APHdg;         // AUTOPILOT HEADING LOCK DIR
    public double FlapsIndex;    // FLAPS HANDLE INDEX
    public double FlapsDeg;      // TRAILING EDGE FLAPS LEFT ANGLE
    public double Pitch;  // ATTITUDE INDICATOR PITCH DEGREES
    public double Bank;   // ATTITUDE INDICATOR BANK DEGREES
}
