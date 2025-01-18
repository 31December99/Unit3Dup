# -*- coding: utf-8 -*-
import argparse
import os

from unit3dup.media_manager.models.qbitt import QBittorrent
from unit3dup.upload import UploadDocument
from unit3dup.contents import Contents

from common.utility.contents import UserContent
from unit3dup import config

class DocuManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        self._my_tmdb = None
        self.file_name = None
        self.contents: list['Contents'] = contents
        self.cli: argparse = cli
        self.torrent_found: bool = False


    def process(self) -> list["QBittorrent"]:
        qbittorrent_list = []
        for content in self.contents:
            self.file_name = str(os.path.join(content.folder, content.file_name))

            # Torrent creation
            if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                self.torrent_found = False
            else:
                # Skip if the watcher is active
                if self.cli.watcher:
                    continue
                self.torrent_found = True

            # Filter contents based on existing torrents or duplicates
            if (self.cli.duplicate or config.DUPLICATE_ON) and not UserContent.is_duplicate(content=content):

                # Tracker payload
                unit3d_up = UploadDocument(content)
                data = unit3d_up.payload()

                # Get a new tracker instance
                tracker = unit3d_up.tracker(data=data)

                # Upload
                tracker_response = unit3d_up.send(tracker=tracker)

                if not self.cli.torrent:
                    qbittorrent_list.append(
                        QBittorrent(
                            tracker_response=tracker_response,
                            torrent_response=torrent_response,
                            content=content
                        ))

        return qbittorrent_list