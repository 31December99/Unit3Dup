# -*- coding: utf-8 -*-
import argparse
import os

from unit3dup.media_manager.models.qbitt import QBittorrent
from unit3dup.upload import UploadDocument
from unit3dup.contents import Contents

from common.utility.contents import UserContent
from common.config import config

class DocuManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        self._my_tmdb = None
        self.file_name = None
        self.contents = contents
        self.cli = cli

    def process(self) -> list["QBittorrent"]:
        qbittorrent_list = []
        for content in self.contents:
            self.file_name = str(os.path.join(content.folder, content.file_name))

            # Filter contents based on existing torrents or duplicates
            if (self.cli.duplicate or config.DUPLICATE_ON) and not UserContent.is_duplicate(content=content):

                # Tracker payload
                unit3d_up = UploadDocument(content)
                data = unit3d_up.payload()

                # Torrent creation
                if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                    torrent_response = UserContent.torrent(content=content)
                else:
                    torrent_response = None

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