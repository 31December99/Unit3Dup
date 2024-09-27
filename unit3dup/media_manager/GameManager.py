# -*- coding: utf-8 -*-
import argparse

from common.external_services.igdb.core.igdb_api import IGdbServiceApi
from common.external_services.igdb.core.models.game import Game
from unit3dup.media_manager.models.qbitt import QBittorrent
from common.custom_console import custom_console
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.upload import UploadGame
from unit3dup.contents import Contents


class GameManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        self.contents = contents
        self.cli = cli

        # IGDB service
        self.ig_db_data: list["Game"] = []

    def process(self) -> list["QBittorrent"]:
        custom_console.rule()
        if IGdbServiceApi.cls_login():
            custom_console.bot_log("IGDB Login successful!")
            ig_dbapi = IGdbServiceApi()
        else:
            custom_console.bot_error_log(
                "IGDB Login failed. Please check your credentials"
            )
            exit(1)

        qbittorrent_list = []
        for content in self.contents:
            # Look for the IGDB ID #todo if it does not exist, report it at the end of the process
            game_data = ig_dbapi.request(
                title=content.game_title, platform=content.game_tags
            )

            # Print the results
            custom_console.bot_log('\nResults:')
            [custom_console.bot_log(result) for result in game_data]

            if not game_data:
                custom_console.bot_error_log(
                    f"IGDB ID not found for the title {content.game_title}"
                )
                exit(1)

            # Hash
            torrent_response = self.torrent(content=content)

            if not self.cli.torrent and torrent_response:
                # Upload only if it is after the torrent was created
                tracker_response = self.upload(content=content, ig_db_data=game_data)
            else:
                tracker_response = None

            data_for_torrent_client = QBittorrent(
                tracker_response=tracker_response,
                torrent_response=torrent_response,
                content=content,
            )
            qbittorrent_list.append(data_for_torrent_client)

        return qbittorrent_list

    @staticmethod
    def torrent(content: Contents):
        my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    @staticmethod
    def upload(content: Contents, ig_db_data: list["Game"]):
        unit3d_up = UploadGame(content)

        # Create a new payload
        # todo : choose the best match not [0]
        if not ig_db_data:
            custom_console.bot_error_log("IGDB ID non trovato")
            exit(1)
        data = unit3d_up.payload(igdb=ig_db_data[0])

        # Get a new tracker instance
        tracker = unit3d_up.tracker(data=data)

        # Send the payload
        return unit3d_up.send(tracker=tracker)
