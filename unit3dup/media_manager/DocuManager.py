# -*- coding: utf-8 -*-

from unit3dup.pvtTorrent import Mytorrent
from unit3dup.uploader import UploadDocument
from unit3dup.contents import Contents


class DocuManager:

    def __init__(self, content: Contents):
        self.content = content
        self._my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        self._unit3d_up = UploadDocument(content)

    def torrent(self):
        self._my_torrent.hash()
        return self._my_torrent if self._my_torrent.write() else None

    def upload(self):
        # Create a new payload
        data = self._unit3d_up.payload()

        # Get a new tracker instance
        tracker = self._unit3d_up.tracker(data=data)

        # Send the payload
        return self._unit3d_up.send(tracker=tracker)
