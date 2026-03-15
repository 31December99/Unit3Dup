# -*- coding: utf-8 -*-
import os
import re
from common.utility import ManageTitles
from common.mediainfo import MediaFile

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
    "AMZN": "source",
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
    "SUBS": "subtitle",
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
    "DD+ 7.1": "audio",
    "DD+ 5.1": "audio",
    "DD+ 2.0": "audio",
    "AAC2.0": "audio",
    "AAC5.1": "audio",
    "AC3": "audio",
    "DD": "audio",
    "DD+": "audio",
    "DDP": "audio",
    "E-AC3": "audio",
    "EAC3": "audio",
    "AC-3": "audio",
    "AAC": "audio",
    "AVC": "audio",

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
    "DV": "video",
    "HDR10": "video",
    "DVHDR10": "video",
    "DVHDR": "video",
    "HDRPLUS+": "video",
    "HDR10PLUS": "video",
    "HDR": "video",
    "HDR10+": "video",

    "4320P": "resolution",
    "2160P": "resolution",
    "1080P": "resolution",
    "720P": "resolution",
    "576P": "resolution",
    "480P": "resolution",
}


class P2pTags:
    def __init__(self, filename: str, title: str, year: str, mediafile_resolution: str, season: int, episode: int,
                 episode_title: str, releaser_sign: str, tags_position: list, mediafile: MediaFile):

        self.filename = filename
        self.title = title
        self.year = year
        self.mediafile_resolution = mediafile_resolution
        self.season = season
        self.episode = episode
        self.episode_title = episode_title
        self.releaser_sign = releaser_sign
        self.mediafile = mediafile
        self.tags_position = tags_position
        self.sign_in_title: str | None = None

        search_tags = sorted(TAG_TYPES.keys(), key=len, reverse=True)
        pattern = re.compile(
            r'\b(?:' + '|'.join(map(re.escape, search_tags)) + r')\b',
            re.IGNORECASE
        )

        # Search for tags
        tags_match = pattern.findall(filename.upper())

        # remove dope
        tags_match = list(dict.fromkeys(tags_match))

        # Search for channels
        channel_s = self.mediafile.audio_track[0].get('channel_s', None)
        ch: str = ''
        # map channels
        if channel_s == 6:
            ch = "5.1"
        elif channel_s == 8:
            ch = "7.1"
        elif channel_s == 2:
            ch = "2.0"

        # extract categories results
        categories = [TAG_TYPES.get(tag) for tag in tags_match]

        # Add video codec only if there is no video categories
        if 'video' not in categories:
            video_format = self.mediafile.video_track[0].get('format', "") if self.mediafile.video_track else ""
            video_encode = self.mediafile.video_track[0].get('encoded_library_name',
                                                             "") if self.mediafile.video_track else ""
            tags_match.append(video_format)

        # Add audio codec only if there is no audio categories
        if 'audio' not in categories:
            audio_format = self.mediafile.audio_track[0].get('format', "") if self.mediafile.audio_track else ""
            tags_match.append(audio_format)

        # Add audio language if there is no audio categories
        if 'flag' not in categories:
            tags_match.extend(self._audio_lang())

        # Translate audio codec
        audio_translate = {
            "AC3": "DD",
            "AC-3": "DD",
            "EAC3": "DD+",
            "E-AC3": "DD+",
            "DDP2.0": "DD+ 2.0",
            "DDP5.1": "DD+ 5.1",
            "DDP7.1": "DD+ 7.1",
            "DDP": "DD+",
        }
        # lower the res..
        resolution_lower = {"4320P", "2160P", "1080P", "720P", "576P", "480P"}

        has_channel_tag = ch in tags_match
        new_tags = []

        for tag in tags_match:
            t = tag.upper()
            if t in audio_translate:
                codec = audio_translate[t]

                # Add channels only if it does not exist
                if ch and not has_channel_tag:
                    tag = f"{codec} {ch}"
                else:
                    tag = codec

            # Lower the res
            elif t in resolution_lower:
                tag = t.lower()

            # Fix the 'sub' word
            elif t == "SUB":
                tag = "SUBS"

            new_tags.append(tag)

        tags_match = new_tags

        # Check if a 'resolution' tag exists and add mediafile resolution if it doesn't
        if not any(TAG_TYPES.get(tag.upper()) == "resolution" for tag in tags_match):
            tags_match.append(self.mediafile_resolution.upper())

        # Assign an index to the 'precedence' keywords
        precedence_index = {}
        for i, v in enumerate(self.tags_position):
            precedence_index[v] = i

        # Started based on precedence
        self.tags_sorted = sorted(
            tags_match,
            key=lambda tag: precedence_index.get(TAG_TYPES[tag.upper()], 100)
        )

    def _audio_lang(self) -> list:

        if not self.mediafile:
            return []

        lang: list = []
        for track in self.mediafile.audio_track:
            l = track.get('other_language', None)
            if l:
                for t in l:
                    c = ManageTitles.convert_iso(t)
                    if c:
                        lang.append(c)
                        break
        return lang

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
            m = re.search(r'-([A-Za-z0-9]+)$', filename)
            if m:
                self.sign_in_title = f"-{m.group(1)}"
            else:
                self.sign_in_title = ""
        else:
            self.sign_in_title = f"-{self.releaser_sign}"

        parts = [self.title, str(self.year), se_str, self.episode_title]
        filtered_parts = [part for part in parts if part]
        title = ' '.join(filtered_parts)

        return f"{title} {' '.join(self.tags_sorted)}{self.sign_in_title}"
