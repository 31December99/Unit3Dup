# -*- coding: utf-8 -*-
import os
import re

TAG_TYPES = {
    "WEB-DL": "source",
    "WEBDL": "source",
    "WEB-DLMUX": "source",
    "WEBDLMUX": "source",
    "WEBRIP": "source",
    "BD-UNTOUCHED": "source",
    "VU": "source",
    "UHD": "source",
    "BLURAY": "source",
    "AMC": "source",
    "CN": "source",
    "CR": "source",
    "DCU": "source",
    "DISC": "source",
    "DSCP": "source",
    "DSNY": "source",
    "DSNP": "source",
    "DPLY": "source",
    "ESPN": "source",
    "FOOD": "source",
    "FOX": "source",
    "PLAY": "source",
    "HBO": "source",
    "HMAX": "source",
    "HGTV": "source",
    "HIST": "source",
    "HULU": "source",
    "ID": "source",
    "IT": "source",
    "MTOD": "source",
    "NATG": "source",
    "NF": "source",
    "NICK": "source",
    "NOW": "source",
    "PMNT": "source",
    "PMTP": "source",
    "PCOK": "source",
    "RKTN": "source",
    "SHO": "source",
    "SKST": "source",
    "STAN": "source",
    "STRP": "source",
    "STZ": "source",
    "TIMV": "source",

    "SUB": "subtitle",
    "ITA": "flag",
    "ENG": "flag",
    "FRA": "flag",
    "GER": "flag",
    "ESP": "flag",

    "TRUEHD": "audio",
    "DDP5.1": "audio",
    "DDP2.0": "audio",
    "DD5.1": "audio",
    "DD2.0": "audio",
    "AAC2.0": "audio",
    "AAC5.1": "audio",
    "AC3": "audio",
    "AAC": "audio",

    "7.1": "audio",
    "5.1": "audio",
    "2.0": "audio",

    "H.264": "video",
    "X.264": "video",
    "X264": "video",
    "H264": "video",
    "H.265": "video",
    "X.265": "video",
    "X265": "video",
    "H265": "video",
    "HEVC": "video",
    "4320P": "resolution",
    "2160P": "resolution",
    "1080P": "resolution",
    "720P": "resolution",
    "576P": "resolution",
    "480P": "resolution",
}


class P2pTags:
    def __init__(self, filename: str, title: str, year: str, mediafile_resolution: str, season: int, episode: int,
                 releaser_sign: str):

        self.filename = filename
        self.title = title
        self.year = year
        self.mediafile_resolution = mediafile_resolution
        self.season = season
        self.episode = episode
        self.releaser_sign = releaser_sign
        self.sign_in_title: str | None = None

        filename = filename.upper()

        search_tags = sorted(TAG_TYPES.keys(), key=len, reverse=True)

        pattern = re.compile(
            r'\b(?:' + '|'.join(map(re.escape, search_tags)) + r')\b',
            re.IGNORECASE
        )

        # Search for tags
        tags_match = pattern.findall(filename)
        # remove dope
        tags_match = list(dict.fromkeys(tags_match))

        # Check if a 'resolution' tag exists and add mediafile resolution if it doesn't
        if not any(TAG_TYPES.get(tag.upper()) == "resolution" for tag in tags_match):
            tags_match.append(self.mediafile_resolution.upper())

        # Fixed priority
        precedence = ["resolution", "source", "audio", "flag", "subtitle", "video"]

        # Assign an index to the 'precedence' keywords
        precedence_index = {}
        for i, v in enumerate(precedence):
            precedence_index[v] = i

        # Started based on precedence
        self.tags_sorted = sorted(
            tags_match,
            key=lambda tag: precedence_index.get(TAG_TYPES[tag.upper()], 999)
        )

    def process(self) -> str:
        se_str = ''
        if self.season is not None and self.episode is not None:
            se_str = f"S{self.season:02d}E{self.episode:02d}"
        elif self.season is not None:
            se_str = f"S{self.season:02d}"
        elif self.episode is not None:
            se_str = f"E{self.episode:02d}"

        if not self.releaser_sign:
            # Search for a sign in the title
            base_name = os.path.basename(self.filename)
            filename, file_ext = os.path.splitext(base_name)
            sign = filename.rsplit('-', 1)
            if len(sign) > 1 and sign[1]:
                self.sign_in_title = f"-{sign[1]}"
            else:
                self.sign_in_title = ""
        else:
            self.sign_in_title = f"-{self.releaser_sign}"

        parts = [self.title, str(self.year), se_str]
        filtered_parts = [part for part in parts if part]
        title = ' '.join(filtered_parts)
        return f"{title} {' '.join(self.tags_sorted)}{self.sign_in_title}"
