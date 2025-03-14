# -*- coding: utf-8 -*-
import argparse

from common.external_services.igdb.client import IGDBClient
from common.bittorrent import BittorrentData

from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup import config_settings
from unit3dup.media import Media

from view import custom_console

class GameManager:

    def __init__(self, contents: list["Media"], cli: argparse.Namespace):
        """
        Initialize the GameManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """
        self.contents: list['Media'] = contents
        self.cli: argparse = cli
        self.igdb = IGDBClient()

    def process(self, selected_tracker: str, tracker_name_list: list) -> list["BittorrentData"]:
        """
        Process the game contents to filter duplicates and create torrents

        Returns:
            list: List of Bittorrent objects created for each content
        """
        login = self.igdb.connect()
        if not login:
            exit(1)

        if self.cli.upload:
            custom_console.bot_error_log("Game upload works only with the '-f' flag.You need to specify a folder name.")
            return []

        bittorrent_list = []
        for content in self.contents:

            # Torrent creation
            if not UserContent.torrent_file_exists(path=content.torrent_path, tracker_name_list=tracker_name_list):
                torrent_response = UserContent.torrent(content=content, trackers=tracker_name_list)
            else:
                # Torrent found, skip if the watcher is active
                if self.cli.watcher:
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue
                torrent_response = None

            # Don't upload if -noup is set to True
            if self.cli.noup:
                custom_console.bot_warning_log(f"No Upload active. Done.")
                return []

            # Skip if it is a duplicate
            if ((self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON)
                    and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                continue

            # Search for the game on IGDB using the content's title and platform tags
            game_data_results = self.igdb.game(content=content)

            # Skip the upload if there is no valid IGDB
            if not game_data_results:
                continue

            # Tracker payload
            unit3d_up = UploadBot(content=content, tracker_name=selected_tracker)
            tracker_response, tracker_message = unit3d_up.send_game(igdb=game_data_results, nfo_path=content.game_nfo)

            bittorrent_list.append(
                BittorrentData(
                    tracker_response=tracker_response,
                    torrent_response=torrent_response,
                    content=content,
                    tracker_message=tracker_message
                ))
        return bittorrent_list

