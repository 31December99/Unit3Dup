# -*- coding: utf-8 -*-
import argparse

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
        result = 0
        for content in self.contents:
            # Look for the IGDB ID #todo if it does not exist, report it at the end of the process
            game_data_results = ig_dbapi.request(
                title=content.game_title, platform=content.game_tags
            )

            # Print the results and ask the user for their choice
            if len(game_data_results) > 1:
                result = self.select_result(results=game_data_results)

            # Check for duplicate game result. Search in the tracker e compare with your game title
            if self.cli.duplicate or config.DUPLICATE_ON:
                results = self.check_duplicate(content=content)
                if results:
                    custom_console.bot_error_log(
                        f"\n*** User chose to skip '{content.file_name}' ***\n"
                    )
                    continue

            # Hash
            torrent_response = self.torrent(content=content)

            if not self.cli.torrent and torrent_response:
                # Upload only if it is after the torrent was created
                tracker_response = self.upload(content=content, ig_db_data=game_data_results[result])
            else:
                tracker_response = None

            data_for_torrent_client = QBittorrent(
                tracker_response=tracker_response,
                torrent_response=torrent_response,
                content=content,
            )
            qbittorrent_list.append(data_for_torrent_client)

        return qbittorrent_list

    # Ask user to choice a result
    def select_result(self, results: list["Game"]) -> None | int:

        # Print the results
        custom_console.bot_log("\nResults:")
        if results:
            for index, result in enumerate(results):
                custom_console.bot_log(f"{index} {result}")

            while 1:
                result = self.input_manager()
                if result is not None and 0 <= result < len(results):
                    custom_console.bot_log(f"Selected: {results[result]}")
                    return result

    @staticmethod
    def input_manager() -> int | None:
        custom_console.print("\nChoice a result to send to the tracker (Q=exit) ", end='', style='violet bold')
        user_choice = input()
        if user_choice.upper() == "Q":
            exit(1)
        if user_choice.isdigit():
            return int(user_choice)

    @staticmethod
    def torrent(content: Contents):
        my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    @staticmethod
    def check_duplicate(content: Contents):
        duplicate = Duplicate(content=content)
        return duplicate.process()

    @staticmethod
    def upload(content: Contents, ig_db_data: Game):
        unit3d_up = UploadGame(content)

        # Create a new payload
        if not ig_db_data:
            custom_console.bot_error_log("IGDB ID non trovato")
            exit(1)
        data = unit3d_up.payload(igdb=ig_db_data)

        # Get a new tracker instance
        tracker = unit3d_up.tracker(data=data)

        # Send the payload
        return unit3d_up.send(tracker=tracker)
