# -*- coding: utf-8 -*-
import argparse
import os

from unit3dup.pvtTorrent import Mytorrent
from unit3dup.upload import UploadDocument
from unit3dup.contents import Contents
from unit3dup.media_manager.models.qbitt import QBittorrent
from common.custom_console import custom_console


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

    @staticmethod
    def torrent(content: Contents):
        my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        my_torrent.hash()
        return my_torrent if my_torrent.write() else None

    def upload(self, content: Contents):

        unit3d_up = UploadDocument(content)

        # Create a new payload
        data = unit3d_up.payload()

        # Get a new tracker instance
        tracker = unit3d_up.tracker(data=data)

        # Send the payload
        return unit3d_up.send(tracker=tracker)
