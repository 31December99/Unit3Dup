# -*- coding: utf-8 -*-
import argparse
import os

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
        self.contents: list[Media] = contents
        self.cli: argparse = cli
        self.igdb = IGDBClient()

    def process(self, selected_tracker: str, tracker_name_list: list,  tracker_archive: str) -> list[BittorrentData]:
        """
        Process the game contents to filter duplicates and create torrents

        Returns:
            list: List of Bittorrent objects created for each content
        """

        login = self.igdb.connect()
        if not login:
            exit(1)

        # -multi : no announce_list . One announce for multi tracker
        if self.cli.mt:
            tracker_name_list = [selected_tracker.upper()]

        if self.cli.upload:
            custom_console.bot_error_log("Game upload works only with the '-f' flag.You need to specify a folder name.")
            return []


        #  Init the torrent list
        bittorrent_list = []
        for content in self.contents:
            # get the archive path
            archive = os.path.join(tracker_archive, selected_tracker)
            os.makedirs(archive, exist_ok=True)
            torrent_filepath = os.path.join(tracker_archive,selected_tracker, f"{content.torrent_name}.torrent")

            # Filter contents based on existing torrents or duplicates
            if self.cli.watcher:
                if os.path.exists(content.torrent_path):
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                continue

            torrent_response = UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                                       selected_tracker=selected_tracker, this_path=torrent_filepath)


            # Skip if it is a duplicate
            if ((self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON)
                    and UserContent.is_duplicate(content=content, tracker_name=selected_tracker, cli=self.cli)):
                continue

            # Search for the game on IGDB using the content's title and platform tags
            game_data_results = self.igdb.game(content=content)
            # print the title will be shown on the torrent page
            custom_console.bot_log(f"'DISPLAYNAME'...{{{content.display_name}}}\n")

            # Skip the upload if there is no valid IGDB
            if not game_data_results:
                continue

            # Tracker instance
            unit3d_up = UploadBot(content=content, tracker_name=selected_tracker, cli = self.cli)

            # Get the data
            unit3d_up.data_game(igdb=game_data_results)

            # Don't upload if -noup is set to True
            if self.cli.noup:
                custom_console.bot_warning_log(f"No Upload active. Done.")
                continue

            # Send to the tracker
            tracker_response, tracker_message = unit3d_up.send(torrent_archive=torrent_filepath, nfo_path=content.game_nfo)

            bittorrent_list.append(
                BittorrentData(
                    tracker_response=tracker_response,
                    torrent_response=torrent_response,
                    content=content,
                    tracker_message=tracker_message,
                    archive_path = torrent_filepath,
                ))
        return bittorrent_list

