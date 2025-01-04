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

    def process(self) -> list["QBittorrent"] | None:

        self.contents = [
            content for content in self.contents
            if not (
                    self.torrent_file_exists(content=content) or
                    not self.is_preferred_language(content=content) or
                    (self.cli.duplicate or config.DUPLICATE_ON) and self.is_duplicate(content=content)
            )
        ]

        qbittorrent_list = []
        for content in self.contents:
            self.file_name = str(os.path.join(content.folder, content.file_name))
            self.tv_show_result = self.tmdb(content=content)

            video_info = Video.info(self.file_name, trailer_key=self.tv_show_result.trailer_key)
            # Tracker payload
            unit3d_up = UploadVideo(content)
            data = unit3d_up.payload(tv_show=self.tv_show_result, video_info=video_info)

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
    def is_preferred_language(content: Contents) -> bool:
        preferred_lang = config.PREFERRED_LANG.lower()

        if "not found" in content.audio_languages:
            return True

        if preferred_lang == 'all' or preferred_lang in content.audio_languages:
            return True

        custom_console.bot_error_log(
            "[Languages] ** Your preferred lang is not in your media being uploaded, skipping ! **"
        )
        return False

    def tmdb(self, content: Contents):
        # Search for a title (Movie or Season) and return the episode title
        self._my_tmdb = TvShow(content)
        tv_show_result = self._my_tmdb.start(content.file_name)

        # Remove episode title from display_name if it exists
        if not content.episode_title and self._my_tmdb.episode_title:
            content.display_name = content.display_name.replace(self._my_tmdb.episode_title, '')

        return tv_show_result

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