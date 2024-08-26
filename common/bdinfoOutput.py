# -*- coding: utf-8 -*-


class BDInfo:
    def __init__(self, disc_label, disc_size, protection, playlist, size, length, total_bitrate, video, languages,
                 subtitles):
        self.disc_label = disc_label
        self.disc_size = disc_size
        self.protection = protection
        self.playlist = playlist
        self.size = size
        self.length = length
        self.total_bitrate = total_bitrate
        self.video = video
        self.languages = languages
        self.subtitles = subtitles

    @classmethod
    def from_bdinfo_string(cls, bd_info_string):
        lines = bd_info_string.strip().split('\n')
        data = {
            'audio': [],
            'subtitles': []
        }

        for line in lines:
            # Parsing
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip().replace(' ', '_').lower()

                if key == 'audio':
                    data['audio'].append(value.strip().lower())
                elif key == 'subtitle':
                    data['subtitles'].append(value.strip().lower())
                else:
                    data[key] = value.strip()

        return cls(
            disc_label=data.get('disc_label'),
            disc_size=data.get('disc_size'),
            protection=data.get('protection'),
            playlist=data.get('playlist'),
            size=data.get('size'),
            length=data.get('length'),
            total_bitrate=data.get('total_bitrate'),
            video=data.get('video'),
            languages=data['audio'],
            subtitles=data['subtitles']
        )

