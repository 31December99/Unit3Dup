# -*- coding: utf-8 -*-

import argparse

from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.GameManager import GameManager
from unit3dup.media_manager.DocuManager import DocuManager
from unit3dup.media_manager.SeedManager import SeedManager

from unit3dup import config_settings
from unit3dup.media import Media

from common.bittorrent import BittorrentData
from common.constants import my_language
from common.utility import System

from unit3dup.media_manager.common import UserContent
from view import custom_console


class TorrentManager:
    def __init__(self, cli: argparse.Namespace, tracker_archive: str):

        self.preferred_lang = my_language(config_settings.user_preferences.PREFERRED_LANG)
        self.tracker_archive = tracker_archive
        self.videos: list[Media] = []
        self.games: list[Media] = []
        self.doc: list[Media] = []
        self.cli = cli
        self.fast_load = config_settings.user_preferences.FAST_LOAD
        if self.fast_load < 1 or self.fast_load > 150:
            # full list
            self.fast_load = None


    async def process(self, contents: list) -> None:
        """
        Send content to each selected tracker with the trackers_name_list.
        trackers_name_list can be a list of tracker names or the current tracker for the upload process

        Args:
            contents: torrent contents
        Returns:
            NOne
        """
        # // Build a GAME list
        self.games = [
            content for content in contents if content.category == System.category_list.get(System.GAME)
        ]

        if self.games:
            if 'no_key' in config_settings.tracker_config.IGDB_CLIENT_ID:
                custom_console.bot_warning_log("Skipping game upload, no IGDB credentials provided")
                self.games = []

        # // Build a VIDEO list
        self.videos = [
            content
            for content in contents
            if content.category in {System.category_list.get(System.MOVIE), System.category_list.get(System.TV_SHOW)}
        ]


        # // Build a Doc list
        self.doc = [
            content for content in contents if content.category == System.category_list.get(System.DOCUMENTARY)
        ]

    async def run(self, trackers_name_list: list):
        """

        Args:
            trackers_name_list: list of tracker names to update the torrent file ( -cross or -tracker)
        Returns:

        """

        game_process_results: list[BittorrentData] = []
        video_process_results: list[BittorrentData] = []
        docu_process_results: list[BittorrentData] = []

        for selected_tracker in trackers_name_list:
            # Build the torrent file and upload each GAME to the tracker
            if self.games:
                game_manager = GameManager(contents=self.games[:self.fast_load],
                                           cli=self.cli)
                game_process_results = await game_manager.process(selected_tracker=selected_tracker,
                                                            tracker_name_list=trackers_name_list,
                                                            tracker_archive=self.tracker_archive)

            # Build the torrent file and upload each VIDEO to the trackers
            if self.videos:
                video_manager = VideoManager(contents=self.videos[:self.fast_load],
                                             cli=self.cli)
                video_process_results = await video_manager.process(selected_tracker=selected_tracker,
                                                              tracker_name_list=trackers_name_list,
                                                              tracker_archive=self.tracker_archive)

            # Build the torrent file and upload each DOC to the tracker
            if self.doc and not self.cli.reseed:
                docu_manager = DocuManager(contents=self.doc[:self.fast_load],
                                           cli=self.cli)
                docu_process_results = await docu_manager.process(selected_tracker=selected_tracker,
                                                            tracker_name_list=trackers_name_list,
                                                            tracker_archive=self.tracker_archive)

            # No Upload
            if self.cli.noup:
                custom_console.bot_warning_log(f"No seeding active. Done.")
                custom_console.rule()
                continue


            if not self.cli.noseed:
                # // GAME
                torrents_list = await UserContent.send(torrents=game_process_results)
                await UserContent.send_to_bittorrent(bittorrent_list=torrents_list)

                # // VIDEO
                torrents_list = await UserContent.send(torrents=video_process_results)
                await UserContent.send_to_bittorrent(bittorrent_list=torrents_list)

                # // DOCUMENTS
                torrents_list = await UserContent.send(torrents=docu_process_results)
                await UserContent.send_to_bittorrent(bittorrent_list=torrents_list)

            custom_console.bot_log(f"Tracker '{selected_tracker}' Done.")
            custom_console.rule()

    custom_console.bot_log(f"Done.")
    custom_console.rule()

    async def reseed(self, trackers_name_list: list) -> None:
        """

        Reseed : compare local file with remote tracker file. Download if found

        Args:
            trackers_name_list: list of tracker names
        Returns:

        """

        for selected_tracker in trackers_name_list:
            # From the contents
            if self.videos:
                # Instance
                seed_manager = SeedManager(contents=self.videos, cli=self.cli)
                # Search your content to see if there is a title present in the tracker
                seed_manager_results = seed_manager.process(selected_tracker=selected_tracker,
                                                            trackers_name_list=trackers_name_list,
                                                            tracker_archive=self.tracker_archive)

                #if so download the torrent files from the tracker for seeding
                if seed_manager_results:
                    for result in await seed_manager_results:
                        await UserContent.download_file(url=result.tracker_response, destination_path=result.archive_path)
                        # Send the data to the torrent client
                        await UserContent.send_to_bittorrent([result])
