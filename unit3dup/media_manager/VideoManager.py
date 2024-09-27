# -*- coding: utf-8 -*-
import argparse
import os

from unit3dup.media_manager.models.qbitt import QBittorrent
from common.custom_console import custom_console
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.duplicate import Duplicate
from unit3dup.upload import UploadVideo
from unit3dup.contents import Contents
from unit3dup.pvtVideo import Video
from media_db.search import TvShow
from common.config import config


class VideoManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        self.tv_show_result = None
        self._my_tmdb = None
        self.file_name = None
        self.contents = contents
        self.cli = cli

    def process(self) -> list["QBittorrent"]:
        custom_console.rule()

        qbittorrent_list = []
        for content in self.contents:
            self.file_name = str(os.path.join(content.folder, content.file_name))
            self._my_tmdb = TvShow(content)

            # Look for an existing torrent file before to start
            if self.torrent_file_exists(content=content):
                continue

            # Verify if your preferred lang is in your media being uploaded
            preferred_lang = self.check_language(content=content)
            if not preferred_lang:
                custom_console.bot_error_log(
                    "[Languages] ** Your preferred lang is not in your media being uploaded"
                    ", skipping ! **"
                )
                continue

            # Check for duplicate video. Search in the tracker e compare with your video
            if self.cli.duplicate or config.DUPLICATE_ON:
                results = self.check_duplicate(content=content)
                if results:
                    custom_console.bot_error_log(
                        f"\n*** User chose to skip '{content.file_name}' ***\n"
                    )
                    continue

            torrent_response = self.torrent(content=content)
            if not self.cli.torrent and torrent_response:
                tracker_response = self.upload(content=content)
            else:
                tracker_response = None

            data_for_torrent_client = QBittorrent(
                tracker_response=tracker_response,
                torrent_response=torrent_response,
                content=content,
            )
            qbittorrent_list.append(data_for_torrent_client)

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
    def check_language(content: Contents) -> bool:
        if "not found" not in content.audio_languages:
            if config.PREFERRED_LANG.lower():
                if config.PREFERRED_LANG.lower() not in content.audio_languages:
                    return False
        return True

    def tmdb(self, content: Contents):
        tv_show_result = self._my_tmdb.start(content.file_name)
        return tv_show_result

    def _video_info(self):
        return Video.info(self.file_name)

    @staticmethod
    def torrent(content: Contents):
        my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    def check_duplicate(self, content: Contents):
        self.tv_show_result = self.tmdb(content=content)
        duplicate = Duplicate(content=content)
        return duplicate.process()

    def upload(self, content: Contents):

        # Search for TMDB ID if there is no previous result from duplicate
        if not config.DUPLICATE_ON:
            self.tv_show_result = self.tmdb(content=content)

        unit3d_up = UploadVideo(content)

        # Create a new payload
        data = unit3d_up.payload(
            tv_show=self.tv_show_result, video_info=self._video_info()
        )

        # Get a new tracker instance
        tracker = unit3d_up.tracker(data=data)

        # Send the payload
        return unit3d_up.send(tracker=tracker)
