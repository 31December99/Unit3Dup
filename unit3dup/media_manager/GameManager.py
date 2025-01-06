# -*- coding: utf-8 -*-
import argparse
import os

from common.external_services.igdb.client import IGDBClient
from unit3dup.media_manager.models.qbitt import QBittorrent
from common.custom_console import custom_console
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.duplicate import Duplicate
from unit3dup.contents import Contents
from unit3dup.upload import UploadGame
from common.config import config



class GameManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        """
        Initialize the GameManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """
        self.contents = contents
        self.cli = cli
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

        # Filter contents based on existing torrents or duplicates
        self.contents = [
            content for content in self.contents
            if not (
                self.torrent_file_exists(content=content) or
                (self.cli.duplicate or config.DUPLICATE_ON) and self.is_duplicate(content=content)
            )
        ]

        qbittorrent_list = []
        for content in self.contents:
            # Search for the game on IGDB using the content's title and platform tags
            game_data_results = self.igdb.game(game_title=content.game_title , platform_list=content.game_tags)

            # Prepare the upload game data with the search results
            unit3d_up = UploadGame(content)
            data = unit3d_up.payload(igdb=game_data_results)

            # Create the torrent file for the content
            torrent_response = self.torrent(content=content)

            # Get the tracker instance to send the upload request
            tracker = unit3d_up.tracker(data=data)

            # Send the upload request to the tracker
            tracker_response = unit3d_up.send(tracker=tracker)

            if not self.cli.torrent and torrent_response:
                qbittorrent_list.append(
                    QBittorrent(
                        tracker_response=tracker_response,
                        torrent_response=torrent_response,
                        content=content
                    ))
        return qbittorrent_list

    def torrent_file_exists(self, content: Contents) -> bool:
        """
        Check if a torrent file for the given content already exists

        Args:
            content (Contents): The content object

        Returns:
            bool: True if the torrent file exists otherwise False
        """
        base_name = os.path.basename(content.torrent_path)

        if config.TORRENT_ARCHIVE:
            this_path = os.path.join(config.TORRENT_ARCHIVE, f"{base_name}.torrent")
        else:
            this_path = f"{content.torrent_path}.torrent"

        if os.path.exists(this_path):
            custom_console.bot_question_log(
                f"** {self.__class__.__name__} **: This File already exists {this_path}\n"
            )
            return True

    @staticmethod
    def torrent(content: Contents) -> Mytorrent:
        """
        Create a torrent file for the given content

        Args:
            content (Contents): The content object meedia

        Returns:
            Mytorrent or None: Returns a Mytorrent instance if successful, otherwise None.
        """
        my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    @staticmethod
    def is_duplicate(content: Contents) -> bool:
        """
        Check if the given content is a duplicate

        Args:
            content (Contents): The content objet media

        Returns:
            bool: True if the content is a duplicate otherwise False
        """
        duplicate = Duplicate(content=content)
        if duplicate.process():
            custom_console.bot_error_log(
                f"\n*** User chose to skip '{content.file_name}' ***\n"
            )
            return True
