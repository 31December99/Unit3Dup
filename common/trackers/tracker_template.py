# -*- coding: utf-8 -*-
"""
Tracker Template - Base template for adding new Unit3D trackers.

This module provides a template and documentation for adding
support for new Unit3D-based trackers to the system.

To add a new tracker:
1. Copy this template
2. Rename to <tracker_name>.py (e.g., blutopia.py)
3. Fill in the tracker-specific values
4. Add tracker to __init__.py tracker_list
5. Add API credentials to settings.py
"""

# Template for new tracker data
# Replace ALL_CAPS_VALUES with actual tracker values

TRACKER_NAME_data = {
    "CATEGORY": {
        "movie": 1,           # Movie category ID
        "tv": 2,              # TV Show category ID
        "game": 4,            # Game category ID
        "software": 23,       # Software category ID (if supported)
        "edicola": 6,         # eBook/Magazine category ID
        "music": 3,           # Music category ID (if supported)
        "xxx": 19,            # XXX category ID (if supported)
    },
    
    "FREELECH": {
        "size20": 100,        # 100% freeleech
        "size15": 75,         # 75% freeleech
        "size10": 50,         # 50% freeleech
        "size5": 25,          # 25% freeleech
    },
    
    "TYPE_ID": {
        # Blu-ray types
        "full-disc": 1,
        "remux": 2,
        "bdremux": 2,
        "untouched": 2,
        
        # Encode types
        "encode": 3,
        "bluray": 3,
        "hevc": 3,
        
        # Web types
        "web-dl": 4,
        "webdl": 4,
        "web": 4,
        "webrip": 5,
        
        # TV/HDTV
        "hdtv": 6,
        
        # Platform types for games/software
        "windows": 13,
        "pc": 13,
        "mac": 12,
        "macos": 12,
        "linux": 39,
        "android": 38,
        
        # Console platforms
        "ps4": 18,
        "ps5": 35,
        "nintendo": 17,
        "nsw": 17,
        
        # Document types
        "pdf": 16,
        "epub": 19,
        
        # Other
        "altro": 15,
    },
    
    "RESOLUTION": {
        "4320p": 1,     # 8K
        "2160p": 2,     # 4K
        "1440p": 3,     # 2K
        "1080p": 3,     # Full HD
        "1080i": 4,
        "720p": 5,      # HD
        "576p": 6,      # SD
        "576i": 7,
        "480p": 8,
        "480i": 9,
        "altro": 10,
    },
    
    # Video codecs for filtering
    "CODEC": [
        "h264", "x264", "avc",
        "h265", "x265", "hevc",
        "vp8", "vp9", "av1",
        "mpeg-1", "mpeg-4",
        "xvid", "divx",
        "prores", "dnxhd",
    ],
}


# Example: Popular Unit3D trackers you could add
"""
Popular Unit3D Trackers to consider adding:

1. Blutopia (https://blutopia.cc)
   - General tracker with movies, TV, music
   - High quality encodes

2. Aither (https://aither.cc)
   - HD content focused
   - Movies and TV shows

3. ReelFliX (https://reelflix.xyz)
   - Movies and TV focused
   - Scene and P2P releases

4. HUNO (https://hawke.uno)
   - General tracker
   - All media types

5. LST (https://lst.gg)
   - Sports and entertainment
   - Live content

6. OnlyEncodes (https://onlyencodes.cc)
   - High quality encodes only
   - Strict quality standards

To add any of these:
1. Get API access from the tracker
2. Copy this template to <trackername>.py
3. Fill in category/type IDs from tracker's API docs
4. Add to tracker_list in __init__.py
5. Test with the tracker's API
"""


# Helper function for tracker maintainers
def validate_tracker_data(tracker_data: dict) -> bool:
    """
    Validate tracker data structure.
    
    Args:
        tracker_data: Dictionary with tracker configuration
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ["CATEGORY", "FREELECH", "TYPE_ID", "RESOLUTION", "CODEC"]
    
    for key in required_keys:
        if key not in tracker_data:
            print(f"Missing required key: {key}")
            return False
    
    # Check that CATEGORY has basic types
    if "movie" not in tracker_data["CATEGORY"]:
        print("Warning: 'movie' category not defined")
    
    if "tv" not in tracker_data["CATEGORY"]:
        print("Warning: 'tv' category not defined")
    
    print("Tracker data structure is valid!")
    return True


# Example usage:
if __name__ == "__main__":
    # Test the template data
    print("Validating tracker template...")
    validate_tracker_data(TRACKER_NAME_data)
    print("\nTo use this template:")
    print("1. Copy to new file: <your_tracker_name>.py")
    print("2. Replace TRACKER_NAME with your tracker name")
    print("3. Update category IDs based on tracker's API")
    print("4. Add to __init__.py")
    print("5. Test with actual tracker API")
