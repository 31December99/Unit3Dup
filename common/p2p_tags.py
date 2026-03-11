# -*- coding: utf-8 -*-
import os
import re

TAG_TYPES = {
    "WEB-DL": "source",
    "WEB-DLMUX": "source",
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
    "HEVC-FHC": "video",
    "4320P": "resolution",
    "2160P": "resolution",
    "1080P": "resolution",
    "720P": "resolution",
    "576p": "resolution",
    "480P": "resolution",
}


class P2pTags:
    def __init__(self, filename: str, title: str, year: str, resolution: str, season: int, episode: int,
                 releaser_sign: str):
        self.filename = filename
        self.title = title
        self.year = year
        self.resolution = resolution
        self.season = season
        self.episode = episode
        self.releaser_sign = releaser_sign

        filename = filename.upper()

        search_tags = sorted(TAG_TYPES.keys(), key=len, reverse=True)

        pattern = re.compile(
            r'\b(?:' + '|'.join(map(re.escape, search_tags)) + r')\b',
            re.IGNORECASE
        )

        tags_match = pattern.findall(filename)

        precedence = ["resolution", "source", "audio", "flag", "subtitle", "video"]

        precedence_index = {}
        for i, v in enumerate(precedence):
            print(i, v)
            precedence_index[v] = i

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
            search_sign = filename.split('-')

            if len(search_sign) > 1:
                # uses the sign from the filename
                self.releaser_sign = search_sign[-1]

        parts = [self.title, str(self.year), se_str]
        filtered_parts = [p for p in parts if p]
        title = ' '.join(filtered_parts)
        if self.releaser_sign:
            self.releaser_sign = f"-{self.releaser_sign}"  # TODO fix sign and resolution

        return f"{title} {' '.join(self.tags_sorted)} {self.releaser_sign}"
