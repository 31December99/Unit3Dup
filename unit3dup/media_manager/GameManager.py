# -*- coding: utf-8 -*-
import argparse
import os

from common.external_services.igdb.core.igdb_api import IGdbServiceApi
from common.external_services.igdb.core.models.game import Game
from unit3dup.media_manager.models.qbitt import QBittorrent
from common.custom_console import custom_console
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.duplicate import Duplicate
from unit3dup.contents import Contents
from unit3dup.upload import UploadGame
from common.config import config


class GameManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        self.contents = contents
        self.cli = cli

        # IGDB service
        self.ig_db_data: list["Game"] = []

    def process(self) -> list["QBittorrent"]:

        ig_dbapi = IGdbServiceApi()
        login = ig_dbapi.cls_login()
        if not login:
            exit(1)

        self.contents = [
            content for content in self.contents
            if not (
                    self.torrent_file_exists(content=content) or
                    (self.cli.duplicate or config.DUPLICATE_ON) and self.is_duplicate(content=content)
            )
        ]

        qbittorrent_list = []
        for content in self.contents:
            # Look for the IGDB ID
            game_data_results = ig_dbapi.request(title=content.game_title, platform=content.game_tags)

            # Tracker payload
            unit3d_up = UploadGame(content)
            data = unit3d_up.payload(igdb=game_data_results)

            # Torrent creation
            torrent_response = self.torrent(content=content)

            # Get a new tracker instance
            tracker = unit3d_up.tracker(data=data)

            # Upload
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
        """Look for an existing torrent file"""

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
    def torrent(content: Contents):
        my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    @staticmethod
    def is_duplicate(content: Contents) -> bool:
        duplicate = Duplicate(content=content)
        if duplicate.process():
            custom_console.bot_error_log(
                f"\n*** User chose to skip '{content.file_name}' ***\n"
            )
            return True

