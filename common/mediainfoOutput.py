import pprint
import re
from typing import Optional, Dict, List


class AudioFormat:
    """ Create a new object with the audio attributes"""

    def __init__(self, id, format, format_info, commercial_name, codec_id, duration, bit_rate_mode, bit_rate,
                 channels, channel_layout, sampling_rate, frame_rate, compression_mode, stream_size, title, language,
                 service_kind, default, forced, max_bit_rate, delay_relative_to_video):
        self.id = id
        self.format = format
        self.format_info = format_info
        self.commercial_name = commercial_name
        self.codec_id = codec_id
        self.duration = duration
        self.bit_rate_mode = bit_rate_mode
        self.bit_rate = bit_rate
        self.channels = channels
        self.channel_layout = channel_layout
        self.sampling_rate = sampling_rate
        self.frame_rate = frame_rate
        self.compression_mode = compression_mode
        self.stream_size = stream_size
        self.title = title
        self.language = language
        self.service_kind = service_kind
        self.default = default
        self.forced = forced
        self.max_bit_rate = max_bit_rate
        self.delay_relative_to_video = delay_relative_to_video

    @classmethod
    def from_dict(cls, audio_info: Dict[str, str]):
        return cls(
            id=audio_info.get('ID', ''),
            format=audio_info.get('Format', ''),
            format_info=audio_info.get('Format/Info', ''),
            commercial_name=audio_info.get('Commercial name', ''),
            codec_id=audio_info.get('Codec ID', ''),
            duration=audio_info.get('Duration', ''),
            bit_rate_mode=audio_info.get('Bit rate mode', ''),
            bit_rate=audio_info.get('Bit rate', ''),
            channels=audio_info.get('Channel(s)', ''),
            channel_layout=audio_info.get('Channel layout', ''),
            sampling_rate=audio_info.get('Sampling rate', ''),
            frame_rate=audio_info.get('Frame rate', ''),
            compression_mode=audio_info.get('Compression mode', ''),
            stream_size=audio_info.get('Stream size', ''),
            title=audio_info.get('Title', ''),
            language=audio_info.get('Language', ''),
            service_kind=audio_info.get('Service kind', ''),
            default=audio_info.get('Default', ''),
            forced=audio_info.get('Forced', ''),
            max_bit_rate=audio_info.get('Maximum bit rate', ''),
            delay_relative_to_video=audio_info.get('Delay relative to video', '')
        )


class Parser:

    def __init__(self, media_info: str):

        # Mediainfo.parsed() output string from the tracker
        self.media_info = media_info

    def audio_sections(self) -> Optional[List[Dict[str, str]]]:

        # Get each Audio section from the Mediainfo.parsed() output string
        mediainfo_audio_sections_regex = r'Audio #\d+\n([\s\S]*?)(?=\nAudio #\d+|\n\n|$)'
        audio_sections = re.findall(mediainfo_audio_sections_regex, self.media_info)

        # One audio track only
        if not audio_sections:
            mediainfo_audio_sections_regex = r'Audio([\s\S]*?)(?=\nAudio #\d+|\n\n|$)'
            audio_sections = re.findall(mediainfo_audio_sections_regex, self.media_info)

        audio_info_list = []

        # For each audio section
        for i, audio_section in enumerate(audio_sections, 1):
            audio_info = {}
            # print(f"Audio #{i}")
            audio_lines = audio_section.strip().split('\n')
            for line in audio_lines:
                # Get key and value when a section is found
                if ':' in line:
                    key, value = line.split(':', 1)
                    # Create a dictionary with key (left) and value(right) string
                    audio_info[key.strip()] = value.strip()
            # Add each section to list
            audio_info_list.append(audio_info)
        return audio_info_list

    def get_audio_formats(self) -> Optional[list]:
        # Get list of Audio sections
        audio_info_list = self.audio_sections()
        if audio_info_list:
            # return a new object AudioFormat for each section
            return [AudioFormat.from_dict(info) for info in audio_info_list]
        return None
