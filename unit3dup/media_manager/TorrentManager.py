# -*- coding: utf-8 -*-

import argparse

from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.models.qbitt import QBittorrent
from unit3dup.media_manager.GameManager import GameManager
from unit3dup.media_manager.DocuManager import DocuManager
from common.custom_console import custom_console
from common.trackers.trackers import ITTData
from common.constants import my_language
from common.clients.qbitt import Qbitt
from common.config import config


class TorrentManager:
    def __init__(self, cli: argparse.Namespace, tracker_name=None):  # todo tracker_name
        self.cli = cli

        tracker_data = ITTData.load_from_module()

        self.movie_category = tracker_data.category.get("movie")
        self.serie_category = tracker_data.category.get("tvshow")
        self.docu_category = tracker_data.category.get("edicola")
        self.game_category = tracker_data.category.get("game")
        self.preferred_lang = my_language(config.PREFERRED_LANG)

    def process(self, contents: list) -> None:

        game_process_results: list["QBittorrent"] = []
        video_process_results: list["QBittorrent"] = []
        docu_process_results: list["QBittorrent"] = []
        custom_console.rule()

        # // GAME
        games = [
            content for content in contents if content.category == self.game_category
        ]

        # Build the torrent file and upload each game to the tracker
        if games:
            custom_console.bot_log("Searching for duplicate.Please wait..")
            game_manager = GameManager(contents=games, cli=self.cli)
            game_process_results = game_manager.process()

        # // VIDEO
        videos = [
            content
            for content in contents
            if content.category in {self.movie_category, self.serie_category}
        ]

        # Build the torrent file and upload each video to the tracker
        if videos:
            if config.DUPLICATE_ON:
                custom_console.bot_log("Searching for duplicate.Please wait..")
            video_manager = VideoManager(contents=videos, cli=self.cli)
            video_process_results = video_manager.process()

            # // Doc
        doc = [
            content for content in contents if content.category == self.docu_category
        ]

        if doc:
            docu_manager = DocuManager(contents=doc, cli=self.cli)
            docu_process_results = docu_manager.process()

        # // QBITTORRENT
        if game_process_results:
            # Seeds if -torrent is off
            if not self.cli.torrent:
                self.send_to_qbittorrent(game_process_results)

        if video_process_results:
            # Seeds if -torrent is off
            if not self.cli.torrent:
                self.send_to_qbittorrent(video_process_results)

        if docu_process_results:
            # Seeds if -torrent is off
            if not self.cli.torrent:
                self.send_to_qbittorrent(docu_process_results)

    @staticmethod
    def send_to_qbittorrent(qbittorrent_list: list["QBittorrent"]) -> None:

        custom_console.panel_message("\nSending torrents to the client... Please wait")
        for qbittorrent_file in qbittorrent_list:
            if qbittorrent_file.tracker_response:
                qb = Qbitt.connect(
                    tracker_data_response=qbittorrent_file.tracker_response,
                    torrent=qbittorrent_file.torrent_response,
                    contents=qbittorrent_file.content,
                )
                if qb:
                    qb.send_to_client()
