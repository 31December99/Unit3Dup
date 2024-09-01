import argparse
from typing import List, Optional
from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.DocuManager import DocuManager
from common.config import config
from common.constants import my_language
from common.clients.qbitt import Qbitt
from common.custom_console import custom_console


class TorrentManager:
    def __init__(self, cli: argparse.Namespace, tracker_config):
        self.cli = cli
        self.tracker_config = tracker_config
        self.movie_category = self.tracker_config.tracker_values.category("movie")
        self.serie_category = self.tracker_config.tracker_values.category("tvshow")
        self.docu_category = self.tracker_config.tracker_values.category("edicola")
        self.preferred_lang = my_language(config.PREFERRED_LANG)

    def process(self, contents: List) -> None:
        for content in contents:
            # custom_console.bot_log(content.file_name)
            tracker_response: Optional[str] = None
            torrent_response: Optional[str] = None

            if content.category in {self.movie_category, self.serie_category}:
                tracker_response, torrent_response = self.process_video_content(content)

            elif content.category == self.docu_category:
                tracker_response, torrent_response = self.process_docu_content(content)

            if tracker_response:
                self.qbitt(tracker_response, torrent_response, content)

    def process_video_content(self, content) -> (Optional[str], Optional[str]):
        video_manager = VideoManager(content=content)

        # custom_console.bot_log(f"Audio Upload language -> {(','.join(content.audio_languages)).upper()}")
        # custom_console.bot_log(f"Preferred language    -> {self.preferred_lang.upper()}\n")

        if 'audio language not found' not in content.audio_languages:
            if config.PREFERRED_LANG.lower() not in content.audio_languages:
                custom_console.bot_error_log("[Languages] ** Your preferred lang is not in your media being uploaded"
                                             ", skipping ! **")
                return None, None

        if self.cli.duplicate or config.DUPLICATE == "True":
            results = video_manager.check_duplicate()
            if results:
                custom_console.bot_error_log(f"\n*** User chose to skip '{content.file_name}' ***\n")
                return None, None

        torrent_response = video_manager.torrent()
        if not self.cli.torrent and torrent_response:
            tracker_response = video_manager.upload()
        else:
            tracker_response = None

        return tracker_response, torrent_response

    def process_docu_content(self, content) -> (Optional[str], Optional[str]):
        docu_manager = DocuManager(content=content)
        torrent_response = docu_manager.torrent()
        tracker_response = None
        if not self.cli.torrent and torrent_response:
            tracker_response = docu_manager.upload()

        return tracker_response, torrent_response

    def qbitt(self, tracker_response: str, torrent_response, content) -> None:
        Qbitt(
            tracker_data_response=tracker_response,
            torrent=torrent_response,
            contents=content,
        )
