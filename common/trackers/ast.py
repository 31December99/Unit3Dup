# -*- coding: utf-8 -*-

ast_data = {
    "CATEGORY": {
        # =========================
        # Movies
        # =========================
        "movie": 4,
        "movies": 4,
        "foreign-movie": 4,
        "english-movie": 4,
        "أفلام أجنبية": 4,

        "arabic-movie": 3,
        "movie-ar": 3,
        "أفلام عربية": 3,

        "anime-movie-dubbed": 1,
        "dubbed-animation-movie": 1,
        "cartoon-movie-dubbed": 1,
        "أفلام رسوم مدبلجة": 1,

        "anime-movie-subbed": 2,
        "subbed-animation-movie": 2,
        "cartoon-movie-subbed": 2,
        "أفلام رسوم مترجمة": 2,

        "classic-cartoon-movie": 21,
        "classic-animation-movie": 21,
        "أفلام كرتون كلاسيك": 21,

        "documentary-movie": 9,
        "doc-movie": 9,
        "أفلام وثائقية": 9,

        "play": 8,
        "theater": 8,
        "مسرحيات": 8,

        # =========================
        # TV / Series
        # =========================
        "tv": 22,
        "series": 22,
        "foreign-tv": 22,
        "english-tv": 22,
        "مسلسلات أجنبية": 22,

        "arabic-tv": 7,
        "series-ar": 7,
        "مسلسلات عربية": 7,

        "anime-tv-dubbed": 5,
        "dubbed-animation-tv": 5,
        "cartoon-tv-dubbed": 5,
        "مسلسلات رسوم مدبلجة": 5,

        "anime-tv-subbed": 6,
        "subbed-animation-tv": 6,
        "cartoon-tv-subbed": 6,
        "مسلسلات رسوم مترجمة": 6,

        "classic-cartoon-tv": 14,
        "classic-animation-tv": 14,
        "كرتون كلاسيك": 14,

        "documentary-tv": 20,
        "doc-tv": 20,
        "مسلسلات وثائقية": 20,

        # =========================
        # General / no_meta
        # =========================
        "islamic": 10,
        "إسلاميات": 10,

        "ramadan": 11,
        "رمضانيات": 11,

        "variety": 12,
        "misc": 12,
        "منوعات": 12,

        "audio": 13,
        "music": 13,
        "صوتيات": 13,

        "raw": 15,
        "raw-torrent": 15,
        "تورنت خام": 15,

        "lost": 19,
        "missing": 19,
        "تورينتات ضائعة": 19,
    },

    "FREELECH": {"size20": 100,
                 "size15": 75,
                 "size10": 50,
                 "size5": 25},


    "TYPE_ID": {
        # 1) Full Disc
        "full-disc": 1,
        "fulldisc": 1,
        "full disc": 1,
        "bd-full": 1,
        "uhd-full": 1,
        "dvd5": 1,
        "dvd9": 1,

        # 2) Remux
        "remux": 2,
        "bdremux": 2,
        "uhdremux": 2,
        "blu-ray remux": 2,
        "untouched": 2,
        "bd-untouched": 2,

        # 3) Encode
        "encode": 3,
        "encoded": 3,
        "bdrip": 3,
        "brrip": 3,
        "hdrip": 3,
        "bluray": 3,

        # 4) WEB-DL
        "web-dl": 4,
        "webdl": 4,
        "web": 4,
        "web-dlmux": 4,
        "webmux": 4,
        "dlmux": 4,

        # 5) WEBRip
        "webrip": 5,
        "web-rip": 5,

        # 6) HDTV
        "hdtv": 6,
        "hdtv1080p": 6,

        # 7) HDR
        "hdr": 7,
        "hdr10": 7,
        "hdr10+": 7,

        # 8) Dolby Vision
        "dolby vision": 8,
        "dolby-vision": 8,
        "dv": 8,

        # 9) 3D
        "3d": 9,
    },
    "TYPE_ID_AUDIO": {
                "flac": 24,
                "alac": 8,
                "ac3": 9,
                "aac": 10,
                "mp3": 25,
    },
    "TAGS": {
                "SD": 1,
                "HD": 0,
    },
    "RESOLUTION": {
        "4320p": 1,
        "2160p": 2,
        "1080p": 3,
        "1080i": 4,
        "720p": 5,
        "576p": 6,
        "576i": 7,
        "480p": 8,
        "480i": 9,

        "other": 10,
        "altro": 10,

        "tvrip": 11,
        "dvbrip": 12,
        "hdtv1080p": 13,
        "dvd": 14,
    },
    "CODEC": [
                "h261",
                "h262",
                "h263",
                "h264",
                "x264",
                "x265",
                "avc",
                "h265",
                "hevc",
                "vp8",
                "vp9",
                "av1",
                "mpeg-1",
                "mpeg-4",
                "wmv",
                "theora",
                "divx",
                "xvid",
                "prores",
                "dnxhd",
                "cinepak",
                "indeo",
                "dv",
                "ffv1",
                "sorenson",
                "rv40",
                "cineform",
                "huffyuv",
                "mjpeg",
                "lagarith",
                "msu",
                "rle",
                "dirac",
                "wmv3",
                "vorbis",
                "smpte",
                "mjpeg",
                "ffvhuff",
                "v210",
                "yuv4:2:2",
                "yuv4:4:4",
                "hap",
                "sheervideo",
                "ut",
                "quicktime",
                "rududu",
                "h.266",
                "vvc",
                "mjpeg 4:2:0",
                "h.263+",
                "h.263++",
                "vp4",
                "vp5",
                "vp6",
                "vp7",
                "vp8",
                "vp9",
                "vp10",
                "vp11",
                "vp12",
                "vp3",
                "vp2",
                "vp1",
                "amv",
                "daala",
                "gecko",
                "nvenc",
                "bluray",
            ],
}