# -*- coding: utf-8 -*-
import os
import re
from collections import deque
from common.utility import ManageTitles
from common.mediainfo import MediaFile

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
    "UHDRIP": "source",
    "BLURAY": "source",

    "ATVP": "platform",
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

    "ITA": "flag",
    "ENG": "flag",
    "FRA": "flag",
    "GER": "flag",
    "ESP": "flag",
    "JPN": "flag",
    "JAP": "flag",
    "POR": "flag",
    "PRT": "flag",

    "SUB": "subtitle",
    "SUBS": "subtitle",

    "ATMOS": "audio",
    "TRUEHD": "audio",
    "DTSHD": "audio",
    "DTS-HD": "audio",
    "DTS-HD MA": "audio",
    "DDP7.1": "audio",
    "DDP5.1": "audio",
    "DDP2.0": "audio",
    "DTS": "audio",
    "XLL": "audio",
    "DD7.1": "audio",
    "DD5.1": "audio",
    "DD2.0": "audio",
    "DD+ 7.1": "audio",
    "DD+ 5.1": "audio",
    "DD+ 2.0": "audio",
    "DTS-HD MA 7.1": "audio",
    "DTS-HD MA 5.1": "audio",
    "DTS-HD MA 2.0": "audio",
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
    "E-AC-3": "audio",
    "EAC3": "audio",
    "AC-3": "audio",
    "AAC": "audio",
    "AAC LC": "audio",
    "AVC": "audio",

    "7.1": "channels",
    "5.1": "channels",
    "2.0": "channels",

    "X.264": "video_encoder",
    "X264": "video_encoder",
    "X.265": "video_encoder",
    "X265": "video_encoder",

    "H.264": "video",
    "H.265": "video",
    "H264": "video",
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
    def __init__(
            self, filename: str, title: str, year: str, mediafile_resolution: str,
            season: int, episode: int, episode_title: str, releaser_sign: str,
            tags_position: list, mediafile: MediaFile
    ):
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

        self.tags_sorted = self._extract_tags()

    def _extract_tags(self) -> list:
        search_tags = sorted(TAG_TYPES.keys(), key=len, reverse=True)
        pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, search_tags)) + r')\b', re.IGNORECASE)

        # Search for tags in the title
        tags_match = list(dict.fromkeys(pattern.findall(self.filename)))
        # Search for channels
        ch = ''
        if self.mediafile.audio_track:
            channel_s = self.mediafile.audio_track[0].get('channel_s', 0)
            ch = {2: "2.0", 6: "5.1", 8: "7.1"}.get(channel_s, "")

        # Categories of found tags
        categories = [TAG_TYPES.get(tag.upper()) for tag in tags_match]
        # Add video codec only if there is no video categories
        if 'video' not in categories and self.mediafile.video_track:
            video_codec = self.mediafile.video_track[0].get('format', "")
            if video_codec:
                tags_match.append(video_codec)

        # Add audio codec only if there is no video categories
        if 'audio' not in categories and self.mediafile.audio_track:
            for audio in self.mediafile.audio_track:
                # Other_format https://github.com/sbraz/pymediainfo/discussions/119#discussioncomment-2330673
                # con format mi restituisce solo DTS
                # Use other_format per format che hanno uno o piu tag
                other_format = audio.get('other_format', [])
                if other_format:
                    tags_match.append(other_format[0])

        # Add tag language if there is no tag
        flags = self._audio_lang()
        missing_flags = [tag for tag in flags if tag not in tags_match]
        tags_match.extend(missing_flags)

        # Add subtitle tag if subtitle_track exist and there is no 'sub' in the title
        if 'subtitle' not in categories and self.mediafile.subtitle_track:
            tags_match.append("SUBS" if len(self.mediafile.subtitle_track) > 1 else "SUB")

        return self._normalize_tags(tags_match, ch)

    def _audio_lang(self) -> set:
        if not self.mediafile:
            return set()
        langs = set()
        for track in self.mediafile.audio_track:
            for l in track.get('other_language', []):
                c = ManageTitles.convert_iso(l)
                if c:
                    if isinstance(c, list):
                        langs.update(c)
                    else:
                        langs.update(c)
                    break
        return langs

    def _normalize_tags(self, tags_match: list, channel_tag: str) -> list:
        audio_translate = {
            "AC3": "DD",
            "AC-3": "DD",
            "EAC3": "DD+",
            "E-AC3": "DD+",
            "DDP2.0": "DD+",
            "DDP5.1": "DD+",
            "DDP7.1": "DD+",
            "DDP": "DD+",
            "DTS XLL": "DTS-HD MA",
        }

        video_translate = {
            "AVC": "H.264",
            "X265": "x.265",
            "X264": "x.264",
            "HEVC": "H.265",
            "H265": "H.265",
            "H264": "H.264",
        }

        resolution_lower = {"4320P", "2160P", "1080P", "720P", "576P", "480P"}
        codec_lower = {"X.264", "X265", "X.265", "X264"}

        # verify the tags found in the title
        normalized = []
        for tag in tags_match:
            t = tag.upper()
            if t in audio_translate:
                codec = audio_translate[t]
                tag = f"{codec} {channel_tag}" if channel_tag else codec
            elif t in video_translate:
                tag = video_translate[t]
            elif t in resolution_lower or t in codec_lower:
                tag = t.lower()
            elif t == "SUB":
                tag = "SUBS" if len(self.mediafile.subtitle_track) > 1 else "SUB"
            normalized.append(tag)

        # Check if a 'resolution' tag exists and add mediafile resolution if it doesn't
        if not any(TAG_TYPES.get(tag.upper()) == "resolution" for tag in normalized):
            normalized.append(self.mediafile_resolution)

        # Sort and alternate audio/flag tags
        return self._sort_tags(normalized, channel_tag)

    def _sort_tags(self, tags: list, channel_tag: str) -> list:
        # /// Sort tags based on 2 rules:
        # 1) Order by tag_positions
        # 2) For audio and flag categories alternate them (audio/flag/audio/flag)
        # We can't sort each tags so we create dedicated list
        audio_q, flag_q, channel_q = deque(), deque(), deque()
        other_groups = {}

        for tag in tags:
            cat = TAG_TYPES.get(tag.upper(), "unknown")
            if cat == "audio":
                audio_q.append(tag.upper())
            elif cat == "channels":
                channel_q.append(tag)
            elif cat == "flag":
                flag_q.append(tag.upper())
            elif cat == "video":
                other_groups.setdefault(cat, []).append(tag.upper())
            elif cat == "video_encoder":
                # Skip video encoder
                continue
            else:
                other_groups.setdefault(cat, []).append(tag)

        # Alternate only if we have at least 2 audio and 2 flag tags
        mixed = []
        if len(audio_q) >= 2 and len(flag_q) >= 2:
            while audio_q or flag_q:
                if audio_q: mixed.append(audio_q.popleft())
                if channel_q: mixed.append(channel_q.popleft())
                if flag_q: mixed.append(flag_q.popleft())
        else:
            mixed = list(audio_q) + list(channel_q) + list(flag_q)

        result = []
        for cat in self.tags_position:
            if cat in ("audio", "channels", "flag") and mixed:
                result.extend(mixed)
                mixed = []
            elif cat in other_groups:
                result.extend(other_groups[cat])
        return result

    def process(self) -> str:
        se_str = ''
        if self.season is not None and self.episode is not None:
            se_str = f"S{self.season:02d}E{self.episode:02d}"
        elif self.season is not None:
            se_str = f"S{self.season:02d}"
        elif self.episode is not None:
            se_str = f"E{self.episode:02d}"

        # Detect releaser sign in filename if not provided
        if not self.releaser_sign:
            filename, _ = os.path.splitext(os.path.basename(self.filename))
            m = re.search(r'-([A-Za-z0-9]+)$', filename)
            self.sign_in_title = f"-{m.group(1)}" if m and m.group(1) not in TAG_TYPES else ""
        else:
            self.sign_in_title = f"-{self.releaser_sign}"

        parts = [self.title, str(self.year), se_str]
        filtered_parts = [p for p in parts if p]
        return f"{' '.join(filtered_parts)} {' '.join(self.tags_sorted)}{self.sign_in_title}"
