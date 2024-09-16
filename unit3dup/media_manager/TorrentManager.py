# -*- coding: utf-8 -*-

import argparse
from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.DocuManager import DocuManager
from common.config import config
from common.constants import my_language
from common.clients.qbitt import Qbitt
from common.custom_console import custom_console
from common.trackers.trackers import ITTData


class TorrentManager:
    def __init__(self, cli: argparse.Namespace, tracker_name=None):  # todo tracker_name
        self.cli = cli

        tracker_data = ITTData.load_from_module()

        self.movie_category = tracker_data.category.get("movie")
        self.serie_category = tracker_data.category.get("tvshow")
        self.docu_category = tracker_data.category.get("edicola")
        self.preferred_lang = my_language(config.PREFERRED_LANG)

    def process(self, contents: list) -> None:
        for content in contents:
            # custom_console.bot_log(content.file_name)
            tracker_response: str | None = None
            torrent_response: str | None = None

            if content.category in {self.movie_category, self.serie_category}:
                tracker_response, torrent_response = self.process_video_content(content)

            elif content.category == self.docu_category:
                tracker_response, torrent_response = self.process_docu_content(content)

            if tracker_response:
                self.qbitt(tracker_response, torrent_response, content)

    def process_video_content(self, content) -> (str | None, str | None):
        custom_console.rule()
        video_manager = VideoManager(content=content)

        if "not found" not in content.audio_languages:
            if config.PREFERRED_LANG.lower():
                if config.PREFERRED_LANG.lower() not in content.audio_languages:
                    custom_console.bot_error_log(
                        "[Languages] ** Your preferred lang is not in your media being uploaded"
                        ", skipping ! **"
                    )
                    return None, None

        if self.cli.duplicate or config.DUPLICATE_ON == "True":
            results = video_manager.check_duplicate()
            if results:
                custom_console.bot_error_log(
                    f"\n*** User chose to skip '{content.file_name}' ***\n"
                )
                return None, None

        torrent_response = video_manager.torrent()
        if not self.cli.torrent and torrent_response:
            tracker_response = video_manager.upload()
        else:
            tracker_response = None

        return tracker_response, torrent_response

    def process_docu_content(self, content) -> (str | None, str | None):
        docu_manager = DocuManager(content=content)
        torrent_response = docu_manager.torrent()
        tracker_response = None
        if not self.cli.torrent and torrent_response:
            tracker_response = docu_manager.upload()

        return tracker_response, torrent_response

    @staticmethod
    def qbitt(tracker_response: str, torrent_response, content) -> None:
        qb = Qbitt.connect(
            tracker_data_response=tracker_response,
            torrent=torrent_response,
            contents=content,
        )
        if qb:
            qb.send_to_client()
