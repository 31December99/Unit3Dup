# -*- coding: utf-8 -*-

from common.mediainfoOutput import Parser
class MediaInfoManager:

    def __init__(self, media_info_output: str):
        self.parser = Parser(media_info=media_info_output)
        self.audio = self.parser.get_audio_formats()

    def languages(self):
        """ return every languages present in audioFormat """
        return [audio.language.lower() for audio in self.audio] if self.audio else []

    def search_language(self, language: str) -> bool:
        if language.lower() in self.languages():
            return True
        return False
