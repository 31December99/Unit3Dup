# -*- coding: utf-8 -*-
import argparse

from unit3dup.media_manager.models.qbitt import QBittorrent
from unit3dup.contents import Contents
from unit3dup.upload import UploadGame
from unit3dup import config

from common.external_services.igdb.client import IGDBClient
from common.utility.contents import UserContent



class GameManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        """
        Initialize the GameManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """
        self.torrent_found: bool = False
        self.contents: list['Contents'] = contents
        self.cli: argparse = cli
        self.igdb = IGDBClient()

    def process(self) -> list["QBittorrent"]:
        """
        Process the game contents to filter duplicates and create torrents

        Returns:
            list: List of QBittorrent objects created for each content
        """
        login = self.igdb.connect()
        if not login:
            exit(1)

        qbittorrent_list = []
        for content in self.contents:

            # Torrent creation
            if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                self.torrent_found = False
            else:
                # Skip if the watcher is active
                if self.cli.watcher:
                    continue
                self.torrent_found = True

            # Search for the game on IGDB using the content's title and platform tags
            game_data_results = self.igdb.game(content=content)

            # Skip the upload if there is no valid IGDB
            if not game_data_results:
                continue

            # Skip if it is a duplicate
            if (self.cli.duplicate or config.DUPLICATE_ON) and UserContent.is_duplicate(content=content):
                continue

            # Does not create the torrent if the torrent was found earlier
            if not self.torrent_found:
                torrent_response = UserContent.torrent(content=content)
            else:
                torrent_response = None

            # Prepare the upload game data with the search results
            unit3d_up = UploadGame(content)
            data = unit3d_up.payload(igdb=game_data_results)

            # Get the tracker instance to send the upload request
            tracker = unit3d_up.tracker(data=data)

            # Send the upload request to the tracker
            tracker_response = unit3d_up.send(tracker=tracker, nfo_path=content.game_nfo)

            qbittorrent_list.append(
                QBittorrent(
                    tracker_response=tracker_response,
                    torrent_response=torrent_response,
                    content=content
                ))
        return qbittorrent_list

