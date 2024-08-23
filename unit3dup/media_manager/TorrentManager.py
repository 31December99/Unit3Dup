# -*- coding: utf-8 -*-
import argparse
from typing import List
from rich.console import Console
from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.DocuManager import DocuManager
from unit3dup.qbitt import Qbitt
from unit3dup.config import config

console = Console(log_path=False)


class TorrentManager:
    def __init__(self, cli: argparse.Namespace, tracker_config):
        self.cli = cli
        self.tracker_config = tracker_config

        # Load the json file
        self.movie_category = self.tracker_config.tracker_values.category("movie")
        self.serie_category = self.tracker_config.tracker_values.category("tvshow")
        self.docu_category = self.tracker_config.tracker_values.category("edicola")

    def process(self, contents: List) -> None:
        for content in contents:
            console.rule(content.file_name)
            tracker_response = None
            torrent_response = None

            if content.category in {self.movie_category, self.serie_category}:
                video_manager = VideoManager(content=content)

                if self.cli.duplicate or config.DUPLICATE == "True":
                    results = video_manager.check_duplicate()
                    if results:
                        console.log(
                            f"\n*** User chose to skip '{content.file_name}' ***\n"
                        )
                        continue

                torrent_response = video_manager.torrent()
                if not self.cli.torrent and torrent_response:
                    tracker_response = video_manager.upload()

            elif content.category == self.docu_category:
                docu_manager = DocuManager(content=content)
                torrent_response = docu_manager.torrent()
                if not self.cli.torrent and torrent_response:
                    tracker_response = docu_manager.upload()

            if tracker_response:
                Qbitt(
                    tracker_data_response=tracker_response,
                    torrent=torrent_response,
                    contents=content,
                )
