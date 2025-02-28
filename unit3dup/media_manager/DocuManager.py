# -*- coding: utf-8 -*-
import argparse

from common.bittorrent import BittorrentData
from common.custom_console import custom_console

from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup.media import Media
from unit3dup import config


class DocuManager:

    def __init__(self, contents: list["Media"], cli: argparse.Namespace):
        self._my_tmdb = None
        self.contents: list['Media'] = contents
        self.cli: argparse = cli
        self.torrent_found: bool = False


    def process(self) -> list["BittorrentData"]:
        bittorrent_list = []
        for content in self.contents:

            # Torrent creation
            if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                self.torrent_found = False
            else:
                # Torrent found, skip if the watcher is active
                if self.cli.watcher:
                    custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue
                self.torrent_found = True

            # Skip if it is a duplicate
            if (self.cli.duplicate or config.user_preferences.DUPLICATE_ON) and UserContent.is_duplicate(content=content):
                continue

            # Does not create the torrent if the torrent was found earlier
            if not self.torrent_found:
                torrent_response = UserContent.torrent(content=content)
            else:
                torrent_response = None

            # Tracker payload
            unit3d_up = UploadBot(content)

            # Upload
            tracker_response, tracker_message = unit3d_up.send_docu()

            if not self.cli.torrent:
                bittorrent_list.append(
                    BittorrentData(
                        tracker_response=tracker_response,
                        torrent_response=torrent_response,
                        content=content,
                        tracker_message=tracker_message,
                    ))

        return bittorrent_list