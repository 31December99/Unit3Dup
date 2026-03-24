# -*- coding: utf-8 -*-
import os
import re
from common.mediainfo import MediaFile
from common.utility import ManageTitles

# From hdr format
hdr_map = {
    "DOLBY VISION": "DV",
    "DOLBY VISION HDR": "DV HDR",
    "DOLBY VISION HDR10": "DV HDR10",
    "HDR10PLUS": "HDR10+",
    "HDRPLUS+": "HDR10+",
    "HDR10+": "HDR10+",
    "HDR10": "HDR10",
    "HDR10 / HDR10": "HDR10",
    "DOVI": "DV",
    "HDR": "HDR",
}

audio_translate = {
    "AC3": "DD",
    "AAC LC": "AAC",
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


class SearchTags(object):
    def __init__(self, filename, title: str, year: str, season: int, episode: int,
                 mediafile: MediaFile, tags_position: list, tags_list: dict, releaser_sign: str):

        self.tags_position = tags_position
        self.releaser_sign = releaser_sign
        self.mediafile = mediafile
        self.filename = filename
        self.episode = episode
        self.season = season
        self.title = title
        self.year = year
        self.tags_dict = {}
        self.tags_position = tags_position
        self.TAG_TYPES = tags_list

    @staticmethod
    def normalize_version_tag(tag: str) -> str:
        tag_esc = re.escape(tag)
        # Filter hyphenated,space compounds
        tag_esc = tag_esc.replace(r'\ ', r'[.\s_-]*')
        return tag_esc

    @staticmethod
    def normalize_platform_tag(tag: str) -> str:
        # escape
        tag_esc = re.escape(tag)
        return tag_esc

    @staticmethod
    def normalize_sources(tag: str) -> str:
        tag_esc = re.escape(tag)
        # Filter hyphenated,space compounds
        tag_esc = tag_esc.replace(r'\ ', r'[.\s_-]*')
        return tag_esc

    @staticmethod
    def normalize_video_encoder(tag: str) -> str:
        tag_esc = re.escape(tag)
        tag_esc = re.sub(r'([A-Z])(\d+)', r'\1[._-]?\2', tag_esc)
        return tag_esc

    def process(self) -> str:
        patterns = []

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
                self.tags_dict.setdefault(category, []).append(matches[0])

        # /// Read from mediainfo
        updated_category = {}
        for category in self.tags_position:
            if category == "acodec":
                updated_category = self.mediainfo_audio(category=category)

            elif category == "vcodec":
                updated_category = self.mediainfo_video(category=category)

            elif category == "hdr":
                updated_category = self.mediainfo_hdr(category=category)

            elif category == "uhd":
                updated_category = self.mediainfo_uhd(category=category)

            elif category == "subtitle":
                if self.mediafile.subtitle_track:
                    updated_category = {'subtitle': "SUBS" if len(self.mediafile.subtitle_track) > 1 else "SUB"}

            if updated_category:
                self.tags_dict.update(updated_category)

        # /// Add S#E#, title, Year
        se_str = ''
        if self.season is not None and self.episode is not None:
            se_str = f"S{self.season:02d}E{self.episode:02d}"
        elif self.season is not None:
            se_str = f"S{self.season:02d}"
        elif self.episode is not None:
            se_str = f"E{self.episode:02d}"

        self.tags_dict.update({'title': self.title})
        if self.year:
            self.tags_dict.update({'year': self.year})
        if se_str:
            self.tags_dict.update({'season': se_str})

        # /// Add Sign
        if not self.releaser_sign:
            filename, _ = os.path.splitext(os.path.basename(self.filename))
            m = re.search(r'-([A-Za-z0-9]+)$', filename)
            self.releaser_sign = f"-{m.group(1)}" if m and m.group(1) not in self.TAG_TYPES else ""
        else:
            self.releaser_sign = f"-{self.releaser_sign}"

        # /// Order according to tag position
        tags_dict = {
            k: self.tags_dict[k]
            for k in self.tags_position
            if k in self.tags_dict
        }

        # /// Build the title
        build = []
        for k, v in tags_dict.items():
            if isinstance(v, list):
                build.append(' '.join(v))
            else:
                build.append(str(v))

        refactored = ' '.join(build) + self.releaser_sign
        return refactored

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
                # Check hdr
                if hdr_format_commercial:
                    print(f"hdr_format_commercial: {hdr_format_commercial}")
                    print(f"hdr_format: {hdr_format}")
                    hdr = ''
                    if hdr_format_commercial in hdr_map:
                        print(
                            f"hdr_format_commercial: {hdr_format_commercial} -> Tag: {hdr_map[hdr_format_commercial]}")
                        hdr = hdr_map[hdr_format_commercial]
                        # Check dolby vision
                    if 'DOLBY VISION' in hdr_format_commercial.upper() or 'DOLBY VISION' in hdr_format.upper():
                        hdr = f"DOLBY VISION {hdr}"
                        print(hdr)
                    return {category: hdr_map[hdr]}
        return {}

    def mediainfo_uhd(self, category: str) -> dict:
        """
        identify resolution based on Height and Width tolerance 5%
        """
        result = {}
        if self.mediafile.video_track:
            video_height = int(self.mediafile.video_track[0].get('height', 0))
            video_width = int(self.mediafile.video_track[0].get('width', 0))

            # print(f"VideoTrack : W{video_width} x H{video_height}")

            # Calculate range 5%
            def in_range(value, standard):
                tol = standard * 0.05
                return standard - tol <= value <= standard + tol

            # /// UHD
            if video_height >= 2000 or video_width >= 3840:
                result[category] = 'UHD'
                result['resolution'] = '2160p'
            # /// Full HD
            elif in_range(video_height, 1080) or in_range(video_width, 1920):
                result[category] = 'FullHD'
                result['resolution'] = '1080p'
            # /// HD
            elif in_range(video_height, 720) or in_range(video_width, 1280):
                result[category] = 'HD'
                result['resolution'] = '720p'
            # /// SD 576p
            elif in_range(video_height, 576) or in_range(video_width, 768):
                result[category] = 'SD'
                result['resolution'] = '576p'
            # /// SD 480p
            elif in_range(video_height, 480) or in_range(video_width, 640):
                result[category] = 'SD'
                result['resolution'] = '480p'
            else:
                result[category] = 'unknown'
                result['resolution'] = f'{video_width}x{video_height}'

        return result
