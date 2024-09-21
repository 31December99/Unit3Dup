# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass


@dataclass
class MediainfoAudioFormat:
    """Create a new object with the audio attributes"""

    id: str
    format: str
    format_info: str
    commercial_name: str
    codec_id: str
    duration: str
    bit_rate_mode: str
    bit_rate: str
    channels: str
    channel_layout: str
    sampling_rate: str
    frame_rate: str
    compression_mode: str
    stream_size: str
    title: str
    language: str
    service_kind: str
    default: str
    forced: str
    max_bit_rate: str
    delay_relative_to_video: str

    @staticmethod
    def from_mediainfo_string(audio_info: dict[str, str]) -> "MediainfoAudioFormat":
        """Create an instance from a dictionary"""
        return MediainfoAudioFormat(
            id=audio_info.get("ID", ""),
            format=audio_info.get("Format", ""),
            format_info=audio_info.get("Format/Info", ""),
            commercial_name=audio_info.get("Commercial name", ""),
            codec_id=audio_info.get("Codec ID", ""),
            duration=audio_info.get("Duration", ""),
            bit_rate_mode=audio_info.get("Bit rate mode", ""),
            bit_rate=audio_info.get("Bit rate", ""),
            channels=audio_info.get("Channel(s)", ""),
            channel_layout=audio_info.get("Channel layout", ""),
            sampling_rate=audio_info.get("Sampling rate", ""),
            frame_rate=audio_info.get("Frame rate", ""),
            compression_mode=audio_info.get("Compression mode", ""),
            stream_size=audio_info.get("Stream size", ""),
            title=audio_info.get("Title", ""),
            language=audio_info.get("Language", ""),
            service_kind=audio_info.get("Service kind", ""),
            default=audio_info.get("Default", ""),
            forced=audio_info.get("Forced", ""),
            max_bit_rate=audio_info.get("Maximum bit rate", ""),
            delay_relative_to_video=audio_info.get("Delay relative to video", ""),
        )


class MediaInfo:
    def __init__(self, media_info: str):
        # Mediainfo.parsed() output string from the tracker
        self.media_info = media_info

    def audio_sections(self) -> list[dict[str, str]] | None:
        """Get each Audio section from the Mediainfo.parsed() output string"""
        mediainfo_audio_sections_regex = (
            r"Audio #\d+\n([\s\S]*?)(?=\nAudio #\d+|\n\n|$)"
        )
        audio_sections = re.findall(mediainfo_audio_sections_regex, self.media_info)

        # One audio track only
        if not audio_sections:
            mediainfo_audio_sections_regex = r"Audio([\s\S]*?)(?=\nAudio #\d+|\n\n|$)"
            audio_sections = re.findall(mediainfo_audio_sections_regex, self.media_info)

        audio_info_list = []

        # For each audio section
        for i, audio_section in enumerate(audio_sections, 1):
            audio_info = {}
            audio_lines = audio_section.strip().split("\n")
            for line in audio_lines:
                # Get key and value when a section is found
                if ":" in line:
                    key, value = line.split(":", 1)
                    # Create a dictionary with key (left) and value(right) string
                    audio_info[key.strip()] = value.strip()
            # Add each section to list
            audio_info_list.append(audio_info)
        return audio_info_list

    def get_audio_formats(self) -> list[MediainfoAudioFormat] | None:
        """Get list of Audio sections and return MediainfoAudioFormat objects"""
        audio_info_list = self.audio_sections()
        if audio_info_list:
            # return a new object AudioFormat for each section
            return [
                MediainfoAudioFormat.from_mediainfo_string(info)
                for info in audio_info_list
            ]
        return None
