# -*- coding: utf-8 -*-

from common.mediainfoOutput import MediaInfo
from common.bdinfoOutput import BDInfo


class MediaInfoManager:

    def __init__(self, media_info_output: dict):

        if media_info_output['media_info']:
            self.parser = MediaInfo(media_info=media_info_output['media_info'])
            self.audio = self.parser.get_audio_formats()

        if media_info_output['bd_info']:
            self.parser = BDInfo.from_bdinfo_string(media_info_output['bd_info'])
            print(self.parser.audio)
            input("MediaInfoManager . .-> ")

    def languages(self):
        """ return every languages present in audioFormat """
        return [audio.language.lower() for audio in self.audio] if self.audio else []

    def search_language(self, language: str) -> bool:
        if language.lower() in self.languages():
            return True
        return False
