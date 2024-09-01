# -*- coding: utf-8 -*-

import os
from unit3dup.pvtTorrent import Mytorrent
from unit3dup.upload import UploadVideo
from unit3dup.contents import Contents
from unit3dup.pvtVideo import Video
from unit3dup.duplicate import Duplicate
from media_db.search import TvShow


class VideoManager:

    def __init__(self, content: Contents):
        self.content = content
        self.file_name = str(os.path.join(content.folder, content.file_name))
        self._my_tmdb = TvShow(content)
        self._tv_show_result = self._my_tmdb.start(content.file_name)
        self._my_torrent = Mytorrent(contents=content, meta=content.metainfo)
        self._duplicate = Duplicate(content=content)
        self._unit3d_up = UploadVideo(content)

    def tmdb(self):
        return self._tv_show_result

    def _video_info(self):
        return Video.info(self.file_name)

    def torrent(self):
        self._my_torrent.hash()
        return self._my_torrent if self._my_torrent.write() else None

    def check_duplicate(self):
        return self._duplicate.process(self._tv_show_result)

    def upload(self):
        # Create a new payload
        data = self._unit3d_up.payload(
            tv_show=self._tv_show_result, video_info=self._video_info()
        )

        # Get a new tracker instance
        tracker = self._unit3d_up.tracker(data=data)

        # Send the payload
        return self._unit3d_up.send(tracker=tracker)
