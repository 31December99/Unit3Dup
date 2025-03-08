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
        self.torrent_found: bool = False
        self.contents: list['Media'] = contents
        self.cli: argparse = cli
        self.igdb = IGDBClient()

    def process(self, selected_tracker: str) -> list["BittorrentData"]:
        """
        Process the game contents to filter duplicates and create torrents

        Returns:
            list: List of QBittorrent objects created for each content
        """
        login = self.igdb.connect()
        if not login:
            exit(1)

        bittorrent_list = []
        for content in self.contents:

            # Torrent creation
            if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                self.torrent_found = False
            else:
                # Torrent found, skip if the watcher is active
                if self.cli.watcher:
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue
                self.torrent_found = True

            # Search for the game on IGDB using the content's title and platform tags
            game_data_results = self.igdb.game(content=content)

            # Skip the upload if there is no valid IGDB
            if not game_data_results:
                continue

            # Skip if it is a duplicate
            if ((self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON)
                    and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                continue

            # Does not create the torrent if the torrent was found earlier
            if not self.torrent_found:
                torrent_response = UserContent.torrent(content=content)
            else:
                torrent_response = None

            # Prepare the upload game data with the search results
            if not self.cli.noupload:
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

