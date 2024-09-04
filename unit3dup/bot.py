# -*- coding: utf-8 -*-

import argparse

from common.config import config
from common.custom_console import custom_console
from common.external_services.theMovieDB.service.tmdb_service import TmdbService
from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.media_manager.TorrentManager import TorrentManager


class Bot:
    def __init__(
            self, path: str, tracker_name: str, cli: argparse.Namespace, mode="man"
    ):
        self.path = path
        self.tracker_name = tracker_name
        self.cli = cli
        self.mode = mode

        # Load Tracker configuration
        self.tracker_config = config.trackers.get_tracker(tracker_name=tracker_name)

        # Get user contents
        self.content_manager = ContentManager(
            path=self.path, tracker_name=self.tracker_name, mode=self.mode
        )

        # Torrent Manager
        self.torrent_manager = TorrentManager(
            cli=self.cli, tracker_config=self.tracker_config
        )

        # Jack Manager
        self.tmdb_service = TmdbService()

    def run(self) -> None:
        custom_console.panel_message("Analyzing... Please wait")

        files = self.content_manager.get_files()
        contents = [
            content
            for item in files
            if (content := self.content_manager.get_media(item))
        ]
        # Print the list of selected files being processed
        custom_console.bot_process_table_log(contents)

        # Process
        self.torrent_manager.process(contents)

    def jack(self):
        custom_console.panel_message("Analyzing... Please wait")

        # Returns a list of Releases
        releases_latest = self.tmdb_service.latest_movie_by_country(country_code='IT')

        custom_console.log(releases_latest)

        tv_shows = self.tmdb_service.latest_show_by_country(country_code='IT')

        custom_console.log(tv_shows)

