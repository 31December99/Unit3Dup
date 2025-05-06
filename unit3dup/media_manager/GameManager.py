# -*- coding: utf-8 -*-
import argparse
import os

from common.external_services.igdb.client import IGDBClient
from common.bittorrent import BittorrentData, Payload

from unit3dup.media_manager.common import UserContent
from unit3dup.media import Media

from view import custom_console

class GameManager:

    def __init__(self, contents: list[Media], cli: argparse.Namespace):
        """
        Initialize the GameManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """
        self.contents: list[Media] = contents
        self.cli: argparse = cli
        self.igdb = IGDBClient()

    async def process(self, selected_tracker: str, tracker_name_list: list,  tracker_archive: str) -> list[BittorrentData]:
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

            torrent_response = await UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                                       selected_tracker=selected_tracker, this_path=torrent_filepath)

            # Search for the game on IGDB using the content's title and platform tags
            game_data_results = self.igdb.game(content=content)
            # print the title will be shown on the torrent page
            custom_console.bot_log(f"'DISPLAYNAME'...{{{content.display_name}}}\n")

            # Skip the upload if there is no valid IGDB
            if not game_data_results:
                continue

            payload = Payload(
                tracker_name=selected_tracker,
                cli=self.cli,
                show_id=None,
                show_keywords=None,
                video_info=None,
                imdb_id=None,
                igdb=game_data_results,
                docu_info= None
            )

            # Store response for the torrent clients
            bittorrent_list.append(
                BittorrentData(
                    tracker_response= None, # tracker_response,
                    torrent_response=torrent_response,
                    content=content,
                    tracker_message = None, # tracker_message,
                    archive_path=torrent_filepath,
                    payload=payload
                ))

        # // end content
        return bittorrent_list