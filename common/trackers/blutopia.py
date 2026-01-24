# -*- coding: utf-8 -*-
"""
Blutopia Tracker Configuration

Blutopia is a popular HD Unit3D tracker focused on high-quality
movie and TV show releases.

Website: https://blutopia.cc
API Docs: Check tracker documentation for latest IDs
"""

blutopia_data = {
    "CATEGORY": {
        "movie": 1,
        "tv": 2,
        "music": 3,
        "game": 4,
        "software": 5,
        "ebook": 6,
        "xxx": 7,
    },
    
    "FREELECH": {
        "size20": 100,  # 100% freeleech
        "size15": 75,   # 75% freeleech
        "size10": 50,   # 50% freeleech
        "size5": 25,    # 25% freeleech
    },
    
    "TYPE_ID": {
        # Blu-ray releases
        "full-disc": 1,
        "remux": 2,
        "bdremux": 2,
        "untouched": 1,
        "bd-untouched": 1,
        
        # Encodes
        "encode": 3,
        "bluray": 3,
        "fullhd": 3,
        "hevc": 3,
        "hdrip": 3,
        
        # Web releases
        "web-dl": 4,
        "webdl": 4,
        "web": 4,
        "web-dlmux": 4,
        "webrip": 5,
        
        # TV
        "hdtv": 6,
        
        # Platform/Software
        "windows": 13,
        "pc": 13,
        "mac": 12,
        "macos": 12,
        "linux": 14,
        "android": 15,
        
        # Other video types
        "dvdrip": 7,
        "bdrip": 8,
        "hdtvrip": 9,
        "sdtv": 10,
        
        # Game consoles
        "ps4": 16,
        "ps5": 17,
        "xbox": 18,
        "nintendo": 19,
        "nsw": 19,
        
        # Documents
        "pdf": 20,
        "epub": 21,
        "cbr-cbz": 22,
        
        # Default
        "altro": 99,
    },
    
    "RESOLUTION": {
        "4320p": 1,  # 8K
        "2160p": 2,  # 4K UHD
        "1440p": 3,  # 2K QHD
        "1080p": 4,  # Full HD
        "1080i": 5,
        "720p": 6,   # HD
        "576p": 7,   # SD PAL
        "576i": 8,
        "480p": 9,   # SD NTSC
        "480i": 10,
        "altro": 11,
    },
    
    "CODEC": [
        # Modern codecs
        "h264", "x264", "avc",
        "h265", "x265", "hevc",
        "av1",
        "vp8", "vp9",
        
        # Legacy codecs
        "h261", "h262", "h263",
        "mpeg-1", "mpeg-4",
        "xvid", "divx",
        "wmv", "wmv3",
        
        # Professional codecs
        "prores", "dnxhd",
        "mjpeg", "dv",
        
        # Other
        "theora", "vorbis",
        "bluray", "nvenc",
    ],
}
