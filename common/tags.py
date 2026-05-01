# -*- coding: utf-8 -*-
import re
from common.utility import ManageTitles
from common.mediainfo import MediaFile
from unit3dup.media import Media
from view import custom_console

# From hdr format
hdr_map = {
    "DOLBY VISION": "DV",
    "DOLBY VISION HDR": "DV HDR",
    "DOLBY VISION HDR10": "DV HDR10",
    "DOLBY VISION HDR10+": "DV HDR10+",
    "HDR10PLUS": "HDR10+",
    "HDRPLUS+": "HDR10+",
    "HDR10+": "HDR10+",
    "HDR10": "HDR10",
    "BLU-RAY / HDR10": "HDR10",
    "HDR10 / HDR10": "HDR10",
    "HDR10 / HDR10 / HDR10": "HDR10",
    "HDR10 / HDR10+": "HDR10+",
    "HDR10 / HDR10 / HDR10+": "HDR10+",
    "SMPTE ST 2086": "HDR10",
    "SMPTE ST 2094": "HDR10+",

    "DOVI": "DV",
    "HDR": "HDR",
}

audio_translate = {
    "AC3": "DD",
    "AAC LC": "AAC",
    "AAC LC SBR": "HE-AAC",
    "AC-3": "DD",
    "EAC3": "DD+",
    "E-AC3": "DD+",
    "E-AC-3": "DD+",
    "E-AC-3 JOC": "DD+",
    "DTS": "DTS",
    "DTS ES": "DTS-ES",
    "DTS ES XLL": "DTS-HD MA",
    "DTS XLL": "DTS-HD MA",
    "MLP FBA 16-ch": "TrueHD",
    "MPEG Audio": "MPEG",
}

video_translate = {
    "AVC": "H.264",
    "HEVC": "H.265",
    "H265": "H.265",
    "H264": "H.264",
}

video_encoder_translate = {
    "X265": "x.265",
    "X264": "x.264",
}

TAG_NORMALIZE = {
    "BLURAY": "BluRay",
    "WEB": "WEB-DL",
    "WEBDL": "WEB-DL",
    "WEBMUX": "WEBMux",
    "BDRIP": "BDRip",
    "WEBRIP": "WEBRip",
    "UHDRIP": "UHDRip",
}


class SearchTags(object):
    def __init__(self, filename, title: str, year: str, season: int, episode: int,
                 media: Media, tags_position: list, tags_list: dict, sign_list: dict, ban_list: dict,
                 releaser_sign: str):

        self.mediafile: MediaFile = media.mediafile
        self.tags_position = tags_position
        self.releaser_sign = releaser_sign
        self.media: Media = media
        self.filename = filename
        self.episode = episode
        self.season = season
        self.title = title
        self.year = year
        self.tags_dict = {}
        self.tags_position = tags_position
        self.TAG_TYPES: dict = tags_list
        self.SIGNS_LIST: dict = sign_list
        self.BAN_LIST: dict = ban_list

    @staticmethod
    def normalize_version_tag(tag: str) -> str:
        tag_esc = re.escape(tag)
        return tag_esc

    @staticmethod
    def normalize_part_tag(title: str) -> str | None:
        """
        Extract substring PartX
        Try to remove noisy chars and return a normalized tag
        Part1, Part 1, Part.1, [Part 1], Parte1, Pt1, Prt 2,
        """
        pattern = r'[\[\(]?\b(?:Part|Parte|Pt|Prt)[\s\.-]*?(\d+)\b[\]\)]?'
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            part_number = match.group(1)
            return f"Part {part_number}"
        return None

    @staticmethod
    def normalize_platform_tag(tag: str) -> str:
        tag_esc = re.escape(tag)
        return tag_esc

    @staticmethod
    def normalize_sources(tag: str) -> str:
        tag_esc = re.escape(tag)
        return tag_esc

    @staticmethod
    def normalize_video_encoder(tag: str) -> str:
        tag_esc = re.escape(tag)
        tag_esc = re.sub(r'([A-Z])(\d+)', r'\1[._-]?\2', tag_esc)
        return tag_esc

    def build_title(self, dictionary: dict) -> str:
        # /// Build the title
        build = []
        for k, v in dictionary.items():
            if isinstance(v, list):
                for item in v:
                    build.append(str(item))
            else:
                build.append(str(v))

        refactored = ' '.join(build) + self.releaser_sign
        return refactored

    def process(self) -> str:
        patterns = []

        # Remove banned items from categories
        self.tags_position = [x for x in self.tags_position if x not in self.BAN_LIST]

        # loop sorted TAG_TYPES dictionary
        for i, (tag, category) in enumerate(
                sorted(self.TAG_TYPES.items(), key=lambda x: len(x[0]), reverse=True)
        ):
            if category == "version":
                norm = self.normalize_version_tag(tag)
            elif category == "platform":
                norm = self.normalize_platform_tag(tag)
            elif category == "source":
                norm = self.normalize_sources(tag)
            elif category == "video_encoder":
                norm = self.normalize_video_encoder(tag)
            else:
                norm = re.escape(tag)
                # Save a regex pattern for each category
            patterns.append([norm, category])

        # Run regex
        for p, category in patterns:
            regex = re.compile(r'(?<!\w)' + p + r'(?!\w)', re.IGNORECASE)
            matches = regex.findall(self.filename)
            if matches:
                # Normalize Tag_list
                normalized_tag = TAG_NORMALIZE.get(matches[0].upper(), None)
                if normalized_tag:
                    matches[0] = normalized_tag
                self.tags_dict.setdefault(category, []).append(matches[0])

        # /// Tags with no categories
        # Identify PartX
        norm = self.normalize_part_tag(self.filename)
        if norm:
            # Skip if it is part of title es: "Wicked.Parte.2.2025.iTA" Title = Wicked Parte 2
            if not any(t in self.title.lower() for t in ['part', 'parte']):
                self.tags_dict.update({'part': norm})

        # /// Read from mediainfo
        updated_category = {}
        for category in self.tags_position:
            if category == "acodec":
                updated_category = self.mediainfo_audio(category=category)

            elif category == "vcodec":
                updated_category = self.mediainfo_video(category=category)

            elif category == "video_encoder":
                if self.tags_dict.get('video_encoder', None):
                    self.tags_dict['video_encoder'][0] = self.tags_dict['video_encoder'][0].lower()

            elif category == "hdr":
                updated_category = self.mediainfo_hdr(category=category)
                if not updated_category:
                    updated_category = {category: 'SDR'}

            elif category == "uhd":
                updated_category = self.mediainfo_uhd(category=category)


            elif category == "subtitle":
                if self.mediafile.subtitle_track:
                    updated_category = {'subtitle': "SUBS" if len(self.mediafile.subtitle_track) > 1 else "SUB"}

            if updated_category:
                self.tags_dict.update(updated_category)

        # /// Add S#E#, title, Year
        if not self.media.torrent_pack:
            se_str = ''
            if self.season is not None and self.episode is not None:
                se_str = f"S{self.season:02d}E{self.episode:02d}"
            elif self.season is not None:
                se_str = f"S{self.season:02d}"
            elif self.episode is not None:
                se_str = f"E{self.episode:02d}"
        else:
            se_str = self.media.pack

        self.tags_dict.update({'title': self.title})
        if self.year:
            self.tags_dict.update({'year': self.year})
        if se_str:
            self.tags_dict.update({'season': se_str})

        if not self.releaser_sign:
            # If releaser_sign is not defined in the configuration file,
            # try to detect a known sign from SIGN_LIST
            self.releaser_sign = self.detect_releaser(self.filename, self.SIGNS_LIST)

        # /// Order according to tag position
        tags_dict = {
            k: self.tags_dict[k]
            for k in self.tags_position
            if k in self.tags_dict
        }

        new_title = self.build_title(tags_dict)

        return new_title

    def mediainfo_audio(self, category: str) -> dict:
        languages = []
        audio_codecs = []
        if self.mediafile.audio_track:
            for audio in self.mediafile.audio_track:
                other_format = audio.get('other_format', [])
                if other_format:
                    codec_translated = audio_translate.get(other_format[0], '')
                    if not codec_translated:
                        codec_translated = other_format[0]
                    # Check Atmos
                    dolby = audio.get('commercial_name', "").lower()
                    atmos = 'Atmos' if 'atmos' in dolby else ''
                    # Add audio codec
                    channel_s = audio.get('channel_s', 0)
                    # Add channels
                    ch = {2: "2.0", 6: "5.1", 8: "7.1"}.get(channel_s, "")
                    if f"{codec_translated} {ch} {atmos}".strip() not in audio_codecs:
                        audio_codecs.append(f"{codec_translated} {ch} {atmos}".strip())
                    # print(f"Mediainfo {other_format} -> {codec_translated} {ch} {atmos}")

                # Add flags
                for l in audio.get('other_language', []):
                    c = ManageTitles.convert_iso(l)
                    if c:
                        if isinstance(c, list):
                            languages.append(c[0])
                        else:
                            languages.append(c)
                        break
                languages = list(dict.fromkeys(languages))
                # Add multilanguage tag when languages > 2
                if len(languages) > 2:
                    self.tags_dict.update({'multi': 'MULTI'})

            audio_codecs.extend(languages)
        return {category: audio_codecs}

    def mediainfo_video(self, category: str) -> dict:
        codec_translated = {}
        if self.mediafile.video_track:
            for video in self.mediafile.video_track:
                video_format = video.get('format', "")
                codec_translated = video_translate.get(video_format, video_format)
        if codec_translated:
            return {category: codec_translated}
        return codec_translated

    def mediainfo_hdr(self, category: str) -> dict:
        if self.mediafile.video_track:
            for video in self.mediafile.video_track:
                hdr_format_commercial = video.get('hdr_format_commercial', "")
                hdr_format = video.get('hdr_format', "")
                other_hdr_format = video.get('other_hdr_format', "")
                colour_primaries = video.get('color_primaries', "")
                matrix_coefficients = video.get('matrix_coefficients', "")
                bit_depth = video.get('bit_depth', "")
                transfer_characteristics = video.get('transfer_characteristics', "")

                # Check hdr
                if hdr_format_commercial:
                    # print(f"hdr_format_commercial: {hdr_format_commercial}")
                    # print(f"hdr_format: {hdr_format}")
                    hdr = ''
                    if hdr_format_commercial.upper() in hdr_map:
                        # print(
                        #     f"hdr_format_commercial: {hdr_format_commercial} -> Tag: {hdr_map[hdr_format_commercial]}")
                        hdr = hdr_map[hdr_format_commercial.upper()]
                        # Check dolby vision
                    if hdr not in hdr_map:
                        custom_console.bot_warning_log(
                            f"<> HDR Warning: '{hdr_format_commercial}' not found in hdr_map")
                    if 'DOLBY VISION' in hdr_format_commercial.upper() or 'DOLBY VISION' in hdr_format.upper():
                        # Search for fake remux
                        if any("dvhe.08" in s or "Profile 8" in s for s in other_hdr_format):
                            remux = self.tags_dict.get('remux', '')
                            if remux:
                                remux = remux[0]
                                if 'remux' in remux.lower():
                                    del self.tags_dict[remux.lower()]
                                    self.tags_dict.update({'source': 'ENCODE'})
                                    self.media.file_name = self.media.file_name.replace(remux, 'ENCODE')
                                    custom_console.bot_warning_log(
                                        f"<> Warning: Detected REMUX with {other_hdr_format}")
                                    hdr = f"DOLBY VISION {hdr}"
                                    return {category: f"{hdr_map.get(hdr, '*HDR')}"}

                        hdr = f"DOLBY VISION {hdr}"
                    return {category: hdr_map.get(hdr, '*HDR')}
                else:
                    if "2020" in colour_primaries and "2020" in matrix_coefficients:
                        if bit_depth == 10 and transfer_characteristics.strip() == 'PQ':
                            return {category: 'PQ10'}
                        else:
                            custom_console.bot_warning_log(f"<> PQ10 Warning:")
                            custom_console.bot_log(f"colour_primaries: {colour_primaries}")
                            custom_console.bot_log(f"matrix_coefficients: {matrix_coefficients}")
                            custom_console.bot_log(f"bit_depth: |{bit_depth}|")
                            custom_console.bot_log(f"transfer_characteristics: |{transfer_characteristics}|")

        return {}

    def mediainfo_uhd(self, category: str) -> dict:
        """
        identify resolution based on Height and Width tolerance 5%
        """
        mapping = {
            '2160p': 'UHD',
            '1080p': 'FullHD',
            '720p': 'HD',
            '576p': 'SD',
            '480p': 'SD',
        }
        return {
            'resolution': self.media.resolution,
            'uhd': mapping.get(self.media.resolution, 'unknown')
        }

    @staticmethod
    def detect_releaser(name: str, signs_list: dict) -> str:
        """
            normalize both signs_list and base_name
            find the start/end position of the matched sign
            extract the substring from the original base_name
        """
        # Strip the title
        base_name = str(name).strip()

        # sort dictionary from the longest to shortest to avoid partial result (es. 'crew' instead di 'mircrew')
        tokens_signs_list_sorted = sorted(signs_list.keys(), key=len, reverse=True)

        video_exts = [
            "mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "m4v", "ts", "3gp"
        ]

        # Regex per catturare l'estensione alla fine (case insensitive)
        pattern = rf"\.({'|'.join(video_exts)})$"

        # # Search for signs in the base_name only at the end of the string
        base_name = re.sub(pattern, "", base_name, flags=re.IGNORECASE)

        # Search for signs in the base_name_normalized
        for token in tokens_signs_list_sorted:
            token = str(token)
            pattern = re.escape(token)
            match = re.search(pattern, base_name, re.IGNORECASE)

            if match:
                # Sign must be the last words
                base_name_len = len(base_name)
                match_len = match.end() - base_name_len
                if match_len == 0:
                    # Capture any characters from the start to the end of base_name
                    sign = base_name[match.start(): match.end()]
                    return f"-{sign}"
        return ""
