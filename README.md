# ResolutionScaler

**ResolutionScaler** is a utility designed to dynamically scale and align a graphics tablet's working area with your screen resolution. This app integrates with [OpenTabletDriver](https://github.com/OpenTabletDriver/OpenTabletDriver) to detect supported tablets and adjust mappings in real time, allowing for optimal drawing precision and screen-to-tablet ratio consistency across different monitor setups.
I made this to play osu but it could be useful for artists maybe.

## Features

- Allows scaling the tablet work area based on screen resolution
- Clean and responsive UI with real-time feedback

## Run
With python:
```
pip install -r requirements.txt
python proportion.py
```
or use the precompiled pyinstaller exe

## Supported Tablets

<details>
<summary>Click to expand the list of supported tablets</summary>

- Acepen AP1060 (254mm / 152mm)
- Acepen AP906 (230mm / 132mm)
- Adesso Cybertablet K8
- Artisul A1201
- Artisul AP604
- Artisul D16 Pro
- Artisul M0610 Pro
- FlooGoo FMA100
- Gaomon 1060 Pro
- Gaomon GM116HD
- Gaomon GM156HD
- Gaomon M106K Pro
- Gaomon M106K
- Gaomon M10K Pro
- Gaomon M10K
- Gaomon M1220
- Gaomon M1230
- Gaomon M6
- Gaomon M8 (Variant 2)
- Gaomon M8
- Gaomon PD1161
- Gaomon PD156 Pro
- Gaomon PD1560
- Gaomon PD1561
- Gaomon PD2200
- Gaomon S56K
- Gaomon S620
- Gaomon S630
- Gaomon S830
- Genius G-Pen 560
- Genius i405x
- Genius i608x
- Huion 1060 Plus
- Huion 420
- Huion G10T
- Huion G930L
- Huion GC610
- Huion GT-156HD V2
- Huion GT-220 V2
- Huion GT-221 Pro
- Huion GT-221
- Huion H1060P
- Huion H1061P
- Huion H1161
- Huion H320M
- Huion H420
- Huion H420X
- Huion H430P
- Huion H580X
- Huion H610 Pro V2
- Huion H610 Pro V3
- Huion H610 Pro
- Huion H610X
- Huion H640P
- Huion H641P
- Huion H642
- Huion H690
- Huion H950P
- Huion H951P
- Huion HC16
- Huion HS610
- Huion HS611
- Huion HS64
- Huion HS95
- Huion Kamvas 12
- Huion Kamvas 13 (Gen 3)
- Huion Kamvas 13
- Huion Kamvas 16 (2021)
- Huion Kamvas 16
- Huion Kamvas 20
- Huion Kamvas 22 Plus
- Huion Kamvas 22
- Huion Kamvas 24 Plus
- Huion Kamvas Pro 12
- Huion Kamvas Pro 13 (2.5k)
- Huion Kamvas Pro 13
- Huion Kamvas Pro 16 (2.5k)
- Huion Kamvas Pro 16 (4k)
- Huion Kamvas Pro 16 Plus (4k)
- Huion Kamvas Pro 16
- Huion Kamvas Pro 19 (4K)
- Huion Kamvas Pro 20
- Huion Kamvas Pro 22 (2019)
- Huion Kamvas Pro 24 (4K)
- Huion Kamvas Pro 24
- Huion New 1060 Plus (2048)
- Huion New 1060 Plus
- Huion Q11K V2
- Huion Q11K
- Huion Q620M
- Huion Q630M
- Huion RDS-160
- Huion RTE-100
- Huion RTM-500
- Huion RTP-700
- Huion WH1409 V2 (Variant 2)
- Huion WH1409 V2
- Huion WH1409
- KENTING K5540
- LifeTec LT9570
- Monoprice 10594
- Monoprice MP1060-HA60
- Parblo A609
- Parblo A610 Pro
- Parblo A610
- Parblo A640 V2
- Parblo A640
- Parblo Intangbo M
- Parblo Intangbo S
- Parblo Ninos M
- Parblo Ninos N4
- Parblo Ninos N7
- Parblo Ninos N7B
- Parblo Ninos S
- RobotPen T9A
- Trust Flex Design Tablet
- Turcom TS-6580
- UC-Logic 1060N
- UC-Logic PF1209
- UGEE M708 V2
- UGEE M708
- UGEE M808
- UGEE M908
- UGEE S1060
- UGEE S640
- UGEE U1200
- UGEE U1600
- VEIKK A15 Pro
- VEIKK A15 V2
- VEIKK A15
- VEIKK A30 V2
- VEIKK A30
- VEIKK A50 (Variant 2)
- VEIKK A50
- VEIKK S640 V2
- VEIKK S640
- VEIKK VK1060
- VEIKK VK1060PRO
- VEIKK VK430 V2
- VEIKK VK430
- VEIKK VK640
- VEIKK Voila (VO1060)
- ViewSonic Woodpad PF0730
- ViewSonic Woodpad PF1030
- Wacom CTC-4110WL
- Wacom CTC-6110WL
- Wacom CTE-430
- Wacom CTE-440
- Wacom CTE-450
- Wacom CTE-460
- Wacom CTE-630
- Wacom CTE-640
- Wacom CTE-650
- Wacom CTE-660
- Wacom CTF-430
- Wacom CTH-300
- Wacom CTH-301
- Wacom CTH-460
- Wacom CTH-461
- Wacom CTH-470
- Wacom CTH-480
- Wacom CTH-490
- Wacom CTH-661
- Wacom CTH-670
- Wacom CTH-680
- Wacom CTH-690
- Wacom CTL-4100
- Wacom CTL-4100WL
- Wacom CTL-460
- Wacom CTL-470
- Wacom CTL-471
- Wacom CTL-472
- Wacom CTL-480
- Wacom CTL-490
- Wacom CTL-6100
- Wacom CTL-6100WL
- Wacom CTL-671
- Wacom CTL-672
- Wacom CTL-680
- Wacom CTL-690
- Wacom DTC-133
- Wacom DTH-1320
- Wacom Movink 13 (DTH-135)
- Wacom Cintiq Pro 27 (DTH-271)
- Wacom Cintiq 13HD (DTK-1300)
- Wacom Cintiq 16 (DTK1660)
- Wacom Cintiq 22HD (DTK-2200)
- Wacom Cintiq 12WX (DTZ-1200W)
- Wacom ET-0405-U
- Wacom ET-0405A-U
- Wacom FT-0405-U
- Wacom GD-0405-U
- Wacom GD-0608-U
- Wacom GD-0912-U
- Wacom GD-1212-U
- Wacom GD-1218-U
- Wacom MTE-450
- Wacom PTH-450
- Wacom PTH-451
- Wacom PTH-460
- Wacom PTH-650
- Wacom PTH-651
- Wacom PTH-660
- Wacom PTH-850
- Wacom PTH-851
- Wacom PTH-860
- Wacom PTK-1240
- Wacom PTK-440
- Wacom PTK-450
- Wacom PTK-540WL
- Wacom PTK-640
- Wacom PTK-650
- Wacom PTK-840
- Wacom PTU-600U
- Wacom PTZ-1230
- Wacom PTZ-1231W
- Wacom PTZ-430
- Wacom PTZ-431W
- Wacom PTZ-630
- Wacom PTZ-631W
- Wacom PTZ-930
- Wacom XD-0405-U
- Wacom XD-0608-U
- Wacom XD-0912-U
- Wacom XD-1212-U
- Wacom XD-1218-U
- Waltop Slim Tablet 5.8"
- XenceLabs Pen Tablet Medium
- XenceLabs Pen Tablet Small
- XENX P1-640
- XENX P3-1060
- XENX X1-640
- XP-Pen Artist 10 (2nd Gen)
- XP-Pen Artist 10S
- XP-Pen Artist 12 (2nd Gen)
- XP-Pen Artist 12 Pro
- XP-Pen Artist 12
- XP-Pen Artist 13 (2nd Gen)
- XP-Pen Artist 13.3 Pro
- XP-Pen Artist 13.3
- XP-Pen Artist 15.6 Pro
- XP-Pen Artist 15.6
- XP-Pen Artist 16 (2nd Gen)
- XP-Pen Artist 16 Pro
- XP-Pen Artist 16
- XP-Pen Artist 22 (2nd Gen)
- XP-Pen Artist 22HD
- XP-Pen Artist 24 Pro
- XP-Pen Artist 24
- XP-Pen Artist Pro 16 (Gen2)
- XP-Pen Artist Pro 16TP
- XP-Pen CT1060
- XP-Pen CT430
- XP-Pen CT640
- XP-Pen Deco 01 V2 (Variant 2)
- XP-Pen Deco 01 V2
- XP-Pen Deco 01 V3
- XP-Pen Deco 01
- XP-Pen Deco 02
- XP-Pen Deco 03
- XP-Pen Deco L
- XP-Pen Deco M
- XP-Pen Deco mini4
- XP-Pen Deco mini7 V2
- XP-Pen Deco mini7
- XP-Pen Deco Pro LW Gen2
- XP-Pen Deco Pro Medium
- XP-Pen Deco Pro Small
- XP-Pen Deco Pro SW
- XP-Pen Deco Pro XLW Gen2
- XP-Pen Innovator 16
- XP-Pen Star 02
- XP-Pen Star 03 Pro
- XP-Pen Star 03
- XP-Pen Star 05 V3
- XP-Pen Star 06
- XP-Pen Star 06C
- XP-Pen Star G430
- XP-Pen Star G430S V2
- XP-Pen Star G430S (101.6mm / 76.2mm)
- XP-Pen Star G540 Pro
- XP-Pen Star G540
- XP-Pen Star G640 (Variant 2)
- XP-Pen Star G640
- XP-Pen Star G640S
- XP-Pen Star G960
- XP-Pen Star G960S Plus
- XP-Pen Star G960S
