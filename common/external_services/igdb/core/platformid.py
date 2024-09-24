# -*- coding: utf-8 -*-

platform_id = {
    "LIN": 3,  # Linux
    "LINUX": 3,  # Linux
    "N64": 4,  # Nintendo 64
    "WII": 5,  # Wii
    "PC": 6,  # PC (Microsoft Windows)
    "PS1": 7,  # PlayStation
    "PS2": 8,  # PlayStation 2
    "PS3": 9,  # PlayStation 3
    "XBX": 11,  # Xbox
    "X360": 12,  # Xbox 360
    "DOS": 13,  # PC DOS
    "MAC": 14,  # Mac
    "C64": 15,  # Commodore C64/128
    "AMIGA": 16,  # Amiga
    "NES": 18,  # Nintendo Entertainment System
    "SNES": 19,  # Super Nintendo Entertainment System
    "NDS": 20,  # Nintendo DS
    "NGC": 21,  # Nintendo GameCube
    "GBC": 22,  # Game Boy Color
    "DC": 23,  # Dreamcast
    "GBA": 24,  # Game Boy Advance
    "CPC": 25,  # Amstrad CPC
    "ZX": 26,  # ZX Spectrum
    "MSX": 27,  # MSX
    "MD": 29,  # Sega Mega Drive/Genesis
    "32X": 30,  # Sega 32X
    "SAT": 32,  # Sega Saturn
    "GB": 33,  # Game Boy
    "AND": 34,  # Android
    "GG": 35,  # Sega Game Gear
    "XBLA": 36,  # Xbox Live Arcade
    "3DS": 37,  # Nintendo 3DS
    "PSP": 38,  # PlayStation Portable
    "IOS": 39,  # iOS
    "WIIU": 41,  # Wii U
    "NGAGE": 42,  # N-Gage
    "TZ": 44,  # Tapwave Zodiac
    "PSN": 45,  # PlayStation Network
    "VITA": 46,  # PlayStation Vita
    "VC": 47,  # Virtual Console (Nintendo)
    "PS4": 48,  # PlayStation 4
    "XONE": 49,  # Xbox One
    "XBO": 49,  # Xbox One
    "3DO": 50,  # 3DO Interactive Multiplayer
    "FDS": 51,  # Family Computer Disk System
    "ARC": 52,  # Arcade
    "MSX2": 53,  # MSX2
    "MOB": 55,  # Mobile
    "WIIW": 56,  # WiiWare
    "WS": 57,  # WonderSwan
    "SFC": 58,  # Super Famicom
    "A2600": 59,  # Atari 2600
    "A7800": 60,  # Atari 7800
    "AL": 61,  # Atari Lynx
    "AJ": 62,  # Atari Jaguar
    "AS": 63,  # Atari ST/STE
    "SMS": 64,  # Sega Master System
    "A8": 65,  # Atari 8-bit
    "A5200": 66,  # Atari 5200
    "INT": 67,  # Intellivision
    "CV": 68,  # ColecoVision
    "BBC": 69,  # BBC Microcomputer System
    "VEC": 70,  # Vectrex
    "VIC": 71,  # Commodore VIC-20
    "OUYA": 72,  # Ouya
    "BB": 73,  # BlackBerry OS
    "WP": 74,  # Windows Phone
    "II": 75,  # Apple II
    "X1": 77,  # Sharp X1
    "SCD": 78,  # Sega CD
    "NGM": 79,  # Neo Geo MVS
    "NGA": 80,  # Neo Geo AES
    "WEB": 82,  # Web browser
    "SG": 84,  # SG-1000
    "DM30": 85,  # Donner Model 30
    "TG16": 86,  # TurboGrafx-16/PC Engine
    "VB": 87,  # Virtual Boy
    "ODY": 88,  # Odyssey
    "MV": 89,  # Microvision
    "PET": 90,  # Commodore PET
    "BA": 91,  # Bally Astrocade
    "STEAM": 92,  # SteamOS
    "C16": 93,  # Commodore 16
    "CPLUS": 94,  # Commodore Plus/4
    "P1": 95,  # PDP-1
    "P10": 96,  # PDP-10
    "P8": 97,  # PDP-8
    "GT40": 98,  # DEC GT40
    "FAMICOM": 99,  # Family Computer (FAMICOM)
    "ANA": 100,  # Analogue electronics
    "NIM": 101,  # Ferranti Nimrod Computer
    "EDSAC": 102,  # EDSAC
    "P7": 103,  # PDP-7
    "HP2100": 104,  # HP 2100
    "HP3000": 105,  # HP 3000
    "SIGMA7": 106,  # SDS Sigma 7
    "CALL": 107,  # Call-A-Computer time-shared mainframe computer system
    "P11": 108,  # PDP-11
    "CDC70": 109,  # CDC Cyber 70
    "PLATO": 110,  # PLATO
    "IMLAC": 111,  # Imlac PDS-1
    "MC": 112,  # Microcomputer
    "ONLIVE": 113,  # OnLive Game System
    "CD32": 114,  # Amiga CD32
    "IIGS": 115,  # Apple IIGS
    "ACORN": 116,  # Acorn Archimedes
    "CDI": 117,  # Philips CD-i
    "FMTOWNS": 118,  # FM Towns
    "NGP": 119,  # Neo Geo Pocket
    "NGPC": 120,  # Neo Geo Pocket Color
    "X68000": 121,  # Sharp X68000
    "NUON": 122,  # Nuon
    "WSC": 123,  # WonderSwan Color
    "SWC": 124,  # SwanCrystal
    "PC8801": 125,  # PC-8801
    "TRS80": 126,  # TRS-80
    "FCF": 127,  # Fairchild Channel F
    "PCSX": 128,  # PC Engine SuperGrafx
    "TI99": 129,  # Texas Instruments TI-99
    "NSW": 130,  # Nintendo Switch
    "NPS": 131,  # Nintendo PlayStation
    "AFTV": 132,  # Amazon Fire TV
    "V7000": 133,  # Philips Videopac G7000
    "ELECTRON": 134,  # Acorn Electron
    "NG64": 135,  # Hyper Neo Geo 64
    "NGCD": 136,  # Neo Geo CD
    "N3DS": 137,  # New Nintendo 3DS
    "VC4000": 138,  # VC 4000
    "APVS": 139,  # 1292 Advanced Programmable Video System
    "AY8500": 140,  # AY-3-8500
    "AY8610": 141,  # AY-3-8610
    "PC50X": 142,  # PC-50X Family
    "AY8760": 143,  # AY-3-8760
    "AY8710": 144,  # AY-3-8710
    "AY8603": 145,  # AY-3-8603
    "AY8605": 146,  # AY-3-8605
    "AY8606": 147,  # AY-3-8606
    "AY8607": 148,  # AY-3-8607
    "PC98": 149,  # PC-98
    "TGCD": 150,  # Turbografx-16/PC Engine CD
    "TRS80C": 151,  # TRS-80 Color Computer
    "FM7": 152,  # FM-7
    "DRAGON": 153,  # Dragon 32/64
    "PCW": 154,  # Amstrad PCW
    "EINSTEIN": 155,  # Tatung Einstein
    "MO5": 156,  # Thomson MO5
    "PC6000": 157,  # NEC PC-6000 Series
    "CDTV": 158,  # Commodore CDTV
    "DSI": 159,  # Nintendo DSi
    "ESHOP": 160,  # Nintendo eShop
    "MR": 161,  # Windows Mixed Reality
    "OCULUS": 162,  # Oculus VR
    "STEAMVR": 163,  # SteamVR
    "DAYDREAM": 164,  # Daydream
    "PSVR": 165,  # PlayStation VR
    "PKMN": 166,  # Pokémon mini
}
