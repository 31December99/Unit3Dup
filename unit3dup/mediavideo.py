# -*- coding: utf-8 -*-

import os
from rich.console import Console
from unit3dup.files import Files
from unit3dup.automode import Auto
from unit3dup.uploader import UploadBot
from unit3dup.search import TvShow
from unit3dup.pvtVideo import Video
from unit3dup.qbitt import Qbitt
from unit3dup import pvtTracker

from unit3dup.pvtTorrent import Mytorrent
from unit3dup.contents import Contents

console = Console(log_path=False)


class MediaVideo:

    def __init__(self, path: str, tracker: str):
        # Path from cli
        self.path = path

        # Tracker name
        self.tracker = tracker

        # List for files
        self.files = []

    def process(self, mode='man'):
        if mode == 'man':
            files = self.manual()
        else:
            files = self.auto()

        for item in files:
            content = self.video_files(item)
            if content is False:
                continue

            # Search for the title in TMDB db
            tv_show_results = self.db_search(content=content)

            # Get info about the video
            video_info = self.video_info(content=content)

            # Create the torrent
            my_torrent = Mytorrent(contents=content, meta=content.metainfo)
            if not my_torrent.write():
                # Skip if the file already exist
                continue

            # Send
            response = self.unit3d(content=content, tv_show_result=tv_show_results, video_info=video_info)

            # If it's ok enter seeding mode
            if response:
                Qbitt(
                    tracker_data_response=response,
                    torrent=my_torrent,
                    contents=content,
                )

    def manual(self):
        auto = Auto(path=self.path, mode='man', tracker_name=self.tracker)
        return auto.upload()

    def auto(self):
        auto = Auto(path=self.path, tracker_name=self.tracker)
        return auto.scan()

    def video_files(self, item):
        """
            Getting ready for tracker upload
            Return
                  - torrent name (filename or folder name)
                  - content category ( movie or serie)
                  - torrent meta_info
            """
        video_files = Files(
            path=item.torrent_path,
            tracker=self.tracker,
            media_type=item.media_type,
        )
        content = video_files.get_data()
        if content is False:
            # skip invalid folder or file
            return
        return content

    def db_search(self, content: Contents):
        # Request results from the TVshow online database
        my_tmdb = TvShow(content.category)
        tv_show_result = my_tmdb.start(content.file_name)
        return tv_show_result

    def video_info(self, content: Contents):
        video_info = Video(
            fileName=str(os.path.join(content.folder, content.file_name))
        )
        return video_info

    def unit3d(self, content: Contents, tv_show_result: list, video_info: pvtTracker):
        unit3d_up = UploadBot(content)
        return unit3d_up.send(tv_show=tv_show_result, video=video_info)
