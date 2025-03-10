# -*- coding: utf-8 -*-

import argparse

from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.GameManager import GameManager
from unit3dup.media_manager.DocuManager import DocuManager
from unit3dup import config_settings

from common.bittorrent import BittorrentData
from common.constants import my_language
from common.utility import System

from unit3dup.media_manager.common import UserContent
from view import custom_console


class TorrentManager:
    def __init__(self, cli: argparse.Namespace):
        self.cli = cli
        self.preferred_lang = my_language(config_settings.user_preferences.PREFERRED_LANG)

    def process(self, contents: list) -> None:

        game_process_results: list["BittorrentData"] = []
        video_process_results: list["BittorrentData"] = []
        docu_process_results: list["BittorrentData"] = []

        # // Build a GAME list
        games = [
            content for content in contents if content.category == System.category_list.get(System.GAME)
        ]

        # // Build a VIDEO list
        videos = [
            content
            for content in contents
            if content.category in {System.category_list.get(System.MOVIE), System.category_list.get(System.TV_SHOW)}
        ]

        # // Build a Doc list
        doc = [
            content for content in contents if content.category == System.category_list.get(System.DOCUMENTARY)
        ]

        if config_settings.user_preferences.DUPLICATE_ON:
            custom_console.bot_log("'[ACTIVE]' Searching for duplicate")

        # Selected one tracker using -tracker flags or selected all the trackers with no flags
        trackers = [self.cli.tracker] if self.cli.tracker is not None else config_settings.tracker_config.MULTI_TRACKER

        # Send content to each tracker in the tracker list
        for tracker_in_list in trackers:
            # Build the torrent file and upload each GAME to the tracker
            if games:
                game_manager = GameManager(contents=games, cli=self.cli)
                game_process_results = game_manager.process(selected_tracker=tracker_in_list)

            # Build the torrent file and upload each VIDEO to the trackers
            if videos:
                video_manager = VideoManager(contents=videos, cli=self.cli)
                video_process_results = video_manager.process(selected_tracker=tracker_in_list)

            # Build the torrent file and upload each DOC to the tracker
            if doc:
                docu_manager = DocuManager(contents=doc, cli=self.cli)
                docu_process_results = docu_manager.process(selected_tracker=tracker_in_list)

            # No seeding or upload allowed
            if self.cli.noseed or self.cli.noup:
                custom_console.bot_warning_log(f"No seeding active. Done.")
                return None


            # custom_console.panel_message("\nSending torrents to the client... Please wait")
            custom_console.bot_warning_log(f"\nSending torrents to the client "
                                           f"{config_settings.torrent_client_config.TORRENT_CLIENT.upper()}"
                                           f"... Please wait")

            if game_process_results:
                UserContent.send_to_bittorrent(game_process_results)

            if video_process_results:
                UserContent.send_to_bittorrent(video_process_results)

            if docu_process_results:
                UserContent.send_to_bittorrent(docu_process_results)
            custom_console.bot_log(f"Tracker '{tracker_in_list}' Done.")
            custom_console.rule()
        custom_console.bot_log(f"Done.")
