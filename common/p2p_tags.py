# -*- coding: utf-8 -*-
import os
import re
from common.utility import ManageTitles
from common.mediainfo import MediaFile
from collections import deque

TAG_TYPES = {
    "WEB-DL": "source",
    "WEBDL": "source",
    "WEB-DLMUX": "source",
    "WEBDLMUX": "source",
    "WEBMUX": "source",
    "WEBRIP": "source",
    "BD-UNTOUCHED": "source",
    "REMUX": "source",
    "VU": "source",
    "UHD": "source",
    "BLURAY": "source",

    "AMZN": "platform",
    "AMC": "platform",
    "CN": "platform",
    "CR": "platform",
    "DCU": "platform",
    "DISC": "platform",
    "DSCP": "platform",
    "DSNY": "platform",
    "DSNP": "platform",
    "DPLY": "platform",
    "ESPN": "platform",
    "FOOD": "platform",
    "FOX": "platform",
    "PLAY": "platform",
    "HBO": "platform",
    "HMAX": "platform",
    "HGTV": "platform",
    "HIST": "platform",
    "HULU": "platform",
    "MTOD": "platform",
    "NATG": "platform",
    "NF": "platform",
    "NICK": "platform",
    "NOW": "platform",
    "PMNT": "platform",
    "PMTP": "platform",
    "PCOK": "platform",
    "RKTN": "platform",
    "SHO": "platform",
    "SKST": "platform",
    "STAN": "platform",
    "STRP": "platform",
    "STZ": "platform",
    "TIMV": "platform",

    "SUB": "subtitle",
    "SUBS": "subtitle",
    "ITA": "flag",
    "ENG": "flag",
    "FRA": "flag",
    "GER": "flag",
    "ESP": "flag",
    "JPN": "flag",
    "JAP": "flag",
    "POR": "flag",
    "PRT": "flag",

    "ATMOS": "audio",
    "TRUEHD": "audio",
    "DTSHD": "audio",
    "DTS-HD": "audio",
    "DTS-HD MA": "audio",
    "DDP7.1": "audio",
    "DDP5.1": "audio",
    "DDP2.0": "audio",
    "DTS": "audio",

    "DD7.1": "audio",
    "DD5.1": "audio",
    "DD2.0": "audio",

    "DD+ 7.1": "audio",
    "DD+ 5.1": "audio",
    "DD+ 2.0": "audio",

    "DD 7.1": "audio",
    "DD 5.1": "audio",
    "DD 2.0": "audio",

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

    "7.1": "channels",
    "5.1": "channels",
    "2.0": "channels",

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
    "FHDRIP": "video",
    "UHDRIP": "video",
    "FULL HD": "video",
    "FULLHD": "video",
    "HD": "video",
    "UHD 4K": "video",

    "REPACK": "version",
    "EXTENDED": "version",

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

        # Search for tags in the title
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
            video_codec = self.mediafile.video_track[0].get('format', "") if self.mediafile.video_track else ""
            tags_match.append(video_codec)

        # Add audio codec only if there is no audio categories
        if 'audio' not in categories:
            audio_format = self.mediafile.audio_track[0].get('format', "") if self.mediafile.audio_track else ""
            tags_match.append(audio_format)

        # Add tag language if there is no tag
        flags = self._audio_lang()
        # are all the language tags from mediaInfo available in the title?
        if len(flags) != tags_match.count('flag'):
            missing_flags = [tag for tag in flags if tag not in tags_match]
            tags_match.extend(missing_flags)

        # Add subtitle tag if subtitle_track exist and there is no 'sub' in the title
        if 'subtitle' not in categories:
            sub_tag = "SUBS" if len(self.mediafile.subtitle_track) > 1 else "SUB"
            if self.mediafile.subtitle_track:
                tags_match.append(sub_tag)

        # Translate audio codec
        audio_translate = {
            "AC3": "DD",
            "AC-3": "DD",
            "EAC3": "DD+",
            "E-AC3": "DD+",
            "DDP2.0": "DD+",
            "DDP5.1": "DD+",
            "DDP7.1": "DD+",
            "DDP": "DD+",
        }

        # Translate video codec
        video_translate = {
            "H.264": "x264",
            "X.264": "x264",
            "X264": "x264",
            "AVC": "x264",
            "H.265": "x265",
            "H265": "x265",
            "X.265": "x265",
            "X265": "x265",
            "HEVC": "x265",
        }

        # lower the res..
        resolution_lower = {"4320P", "2160P", "1080P", "720P", "576P", "480P"}
        codec_lower = {'X.264', 'X265', 'X.265', 'X264'}

        has_channel_tag = ch in tags_match
        new_tags = []

        # verify the tags found in the title
        for tag in tags_match:
            t = tag.upper()
            if t in audio_translate:
                codec = audio_translate[t]
                # Add channels only if it does not exist
                if ch and not has_channel_tag:
                    tag = f"{codec} {ch}"
                else:
                    tag = codec

            elif t in video_translate:
                tag = video_translate[t]

            # Lower the res
            elif t in resolution_lower:
                tag = t.lower()

            # Fix the 'sub' word
            elif t == "SUB":
                sub_tag = "SUBS" if len(self.mediafile.subtitle_track) > 1 else "SUB"
                tag = sub_tag

            elif t in codec_lower:
                tag = t.lower()

            new_tags.append(tag)

        tags_match = new_tags

        # Check if a 'resolution' tag exists and add mediafile resolution if it doesn't
        if not any(TAG_TYPES.get(tag.upper()) == "resolution" for tag in tags_match):
            tags_match.append(self.mediafile_resolution)

        # /// Sort tags based on 2 rules:
        # 1) Order by tag_positions
        # 2) For audio and flag categories alternate them (audio/flag/audio/flag)
        # We can't sort each tags so we create dedicated list
        audio_q = deque()
        flag_q = deque()
        channel_q = deque()

        # This dict is for other categories
        other_groups = {}

        # Isolate audio and flag tags
        # All other tags will follow the normal precedence order
        for tag in tags_match:
            cat = TAG_TYPES.get(tag.upper(), "unknown")
            if cat == "audio":
                # Add audio tag to its queue
                audio_q.append(tag)
            elif cat == "channels":
                channel_q.append(tag)
            elif cat == "flag":
                # Add flag tag to its queue
                flag_q.append(tag)
            else:
                # Add the other tags to other_groups
                other_groups.setdefault(cat, []).append(tag)

        # Alternate only if we have at least 2 audio and 2 flag tags
        if len(audio_q) >= 2 and len(flag_q) >= 2:
            mixed_audio_ch_flag = []
            # Alternate
            while audio_q or flag_q:
                if audio_q:
                    # get the first left audio and append to new list
                    mixed_audio_ch_flag.append(audio_q.popleft())
                if channel_q:
                    mixed_audio_ch_flag.append(channel_q.popleft())
                if flag_q:
                    # get the first right flag and append to new list
                    mixed_audio_ch_flag.append(flag_q.popleft())
        else:
            # otherwise goes for normal precedence
            mixed_audio_ch_flag = list(audio_q) + list(channel_q) + list(flag_q)

        # Rebuild the title ordering each tag+ audio/flag by tag_position
        result = []

        for cat in self.tags_position:
            if cat in ("audio", "channels", "flag"):
                # Insert the audio/flag processed tags
                if mixed_audio_ch_flag:
                    result.extend(mixed_audio_ch_flag)
                    # clear
                    mixed_audio_ch_flag = []
            elif cat in other_groups:
                result.extend(other_groups[cat])
        self.tags_sorted = result

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
                        if isinstance(c, list):
                            lang.extend(c)
                            break
                        else:
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

            if m and m.group(1) not in TAG_TYPES:
                self.sign_in_title = f"-{m.group(1)}"
            else:
                self.sign_in_title = ""
        else:
            self.sign_in_title = f"-{self.releaser_sign}"

        parts = [self.title, str(self.year), se_str, self.episode_title]
        filtered_parts = [part for part in parts if part]
        title = ' '.join(filtered_parts)

        return f"{title} {' '.join(self.tags_sorted)}{self.sign_in_title}"
