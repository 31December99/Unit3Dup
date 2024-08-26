# -*- coding: utf-8 -*-


class BDInfo:
    def __init__(self, disc_label, disc_size, protection, playlist, size, length, total_bitrate, video, audio,
                 languages, subtitles):
        self.disc_label = disc_label
        self.disc_size = disc_size
        self.protection = protection
        self.playlist = playlist
        self.size = size
        self.length = length
        self.total_bitrate = total_bitrate
        self.video = video
        self.audio = audio
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
            # Parsing Audio
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip().replace(' ', '_').lower()

                if key == 'audio':
                    data['audio'].append(value.strip().lower())
                elif key == 'subtitle':
                    data['subtitles'].append(value.strip().lower())
                else:
                    data[key] = value.strip()

        # Parsing Languages
        languages_parsed = []
        for item in data['audio']:
            item = item.replace("(", " ")
            item = item.replace(")", " ")
            item = item.split('/')
            languages_parsed.append(item[0].strip())
        #languages = ','.join(set(languages_parsed))

        return cls(
            disc_label=data.get('disc_label'),
            disc_size=data.get('disc_size'),
            protection=data.get('protection'),
            playlist=data.get('playlist'),
            size=data.get('size'),
            length=data.get('length'),
            total_bitrate=data.get('total_bitrate'),
            video=data.get('video'),
            audio=data['audio'],
            languages=languages_parsed,
            subtitles=data['subtitles']
        )
