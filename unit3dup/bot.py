# -*- coding: utf-8 -*-

import argparse

from common.config import config
from common.custom_console import custom_console
from common.external_services.theMovieDB.service.tmdb_service import TmdbService
from unit3dup.media_manager.ContentManager import ContentManager
from unit3dup.media_manager.TorrentManager import TorrentManager


class Bot:
    """
    A class to manage and execute media-related tasks including file processing,
    torrent management, and interaction with the TMDB service.
    """

    def __init__(
            self, path: str, tracker_name: str, cli: argparse.Namespace, mode="man"
    ):
        """
        Initialize the Bot instance with path, tracker name, command-line interface object, and mode

        Args:
            path (str): The path to the directory or file to be managed
            tracker_name (str): The name of the tracker configuration to use
            cli (argparse.Namespace): The command-line arguments object
            mode (str): The mode of operation, default is 'man'
        """
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

        # TMDB service
        self.tmdb_service = TmdbService()

    def run(self) -> None:
        """
        Executes the main workflow of the bot

        This method analyzes files, retrieves media content, logs the contents being processed,
        and then processes them using the Torrent Manager
        """
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
        # Examples

        # Now Playing by country
        releases_latest = self.tmdb_service.latest_movie_by_country(country_code="IT")
        custom_console.log(releases_latest)
        custom_console.rule()

        # Alternative title for a movie
        alternative_title = self.tmdb_service.movie_alternative_title(movie_id=533535)
        custom_console.log(alternative_title)
        custom_console.rule()

        # Search for a movie title
        search_movie = self.tmdb_service.search_movies(query="Blade Runner 2049")
        custom_console.log(search_movie)
        custom_console.rule()

        # On The Air by country
        tv_shows = self.tmdb_service.latest_show_by_country(country_code="IT")
        custom_console.log(tv_shows)
        custom_console.rule()

        # Tv Show Details by ID
        tv_show_details = self.tmdb_service.tv_show_details(tv_show_id=84773)
        custom_console.log(tv_show_details)
        custom_console.rule()

        # Search for a tv show title
        search_tv_show = self.tmdb_service.search_tv_show(query="Il Signore degli Anelli: Gli Anelli del Potere")
        custom_console.log(search_tv_show)
        custom_console.rule()
