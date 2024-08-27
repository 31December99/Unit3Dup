# -*- coding: utf-8 -*-
from typing import Optional

from common.utility.mediainfoOutput import MediaInfo
from common.utility.bdinfoOutput import BDInfo


class MediaInfoManager:

    def __init__(self, media_info_output: dict):

        if media_info_output['media_info']:
            self.parser = MediaInfo(media_info=media_info_output['media_info'])
            self.audio = self.parser.get_audio_formats()
            self.languages = [audio.language.lower() for audio in self.audio if audio.language] if self.audio else []
            self.languages = ','.join(set(self.languages))

        if media_info_output['bd_info']:
            self.parser = BDInfo.from_bdinfo_string(media_info_output['bd_info'])
            self.languages = self.parser.languages
            self.languages = ','.join(set(self.languages))

    def search_language(self, language: str) -> Optional[bool]:
        return language.lower() in self.languages.lower() if self.languages else None
