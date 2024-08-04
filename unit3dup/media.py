# -*- coding: utf-8 -*-

import os

import requests

from unit3dup.pvtTorrent import Mytorrent
from unit3dup.uploader import UploadDocument, UploadVideo
from unit3dup.contents import Contents
from unit3dup.pvtVideo import Video
from unit3dup.automode import Auto
from unit3dup.search import TvShow
from rich.console import Console
from unit3dup.files import Files
from unit3dup.qbitt import Qbitt
from unit3dup import pvtTracker
from unit3dup import config

console = Console(log_path=False)


class Media:

    def __init__(self, path: str, tracker_name: str):
        # Path from cli
        self.path = path

        # Tracker name
        self.tracker_name = tracker_name

        # List for files
        self.files = []

        # List for contents
        self.contents = []

        # Load the json file
        self.config = config.trackers.get_tracker(tracker_name=tracker_name)
        self.movie_category = self.config.tracker_values.category("movie")
        self.serie_category = self.config.tracker_values.category("tvshow")
        self.docu_category = self.config.tracker_values.category("e-book")

    def process_contents(self, mode="man"):
        if mode == "man":
            files = self.manual()
        else:
            files = self.auto()

        for item in files:
            content = self.video_files(item)
            if not content:
                continue
            self.contents.append(content)
        return self.contents

    def process(self, mode="man"):
        contents = self.process_contents(mode=mode)

        response = None
        for content in contents:

            # Create the torrent
            my_torrent = Mytorrent(contents=content, meta=content.metainfo)
            if not my_torrent.write():
                # Skip if the file already exist
                continue

            if content.category == self.movie_category or content.category == self.serie_category:
                # Search for the title in TMDB db
                tv_show_results = self.db_search(content=content)

                # Get info about the video
                video_info = self.video_info(content=content)

                # Send
                response = Media.unit3d(
                    content=content,
                    tv_show_result=tv_show_results,
                    video_info=video_info,
                )

            if content.category == self.docu_category:
                # Send
                response = self.unit3d_doc(content=content)

            # If it's ok enter seeding mode
            if response:
                Qbitt(
                    tracker_data_response=response,
                    torrent=my_torrent,
                    contents=content,
                )

    def manual(self):
        auto = Auto(path=self.path, mode="man", tracker_name=self.tracker_name)
        return auto.upload()

    def auto(self):
        auto = Auto(path=self.path, tracker_name=self.tracker_name)
        return auto.scan()

    @staticmethod
    def unit3d(content: Contents, tv_show_result: list, video_info: pvtTracker) -> requests:
        # Prepare for upload
        unit3d_up = UploadVideo(content)

        # Create a new payload
        data = unit3d_up.payload(tv_show=tv_show_result, video_info=video_info)

        # Get a new tracker instance
        tracker = unit3d_up.tracker(data=data)

        # Send the payload
        return unit3d_up.send(tracker=tracker)

    @staticmethod
    def unit3d_doc(content: Contents) -> requests:

        # Prepare for upload
        unit3d_up = UploadDocument(content)

        # Create a new payload
        data = unit3d_up.payload()

        # Get a new tracker instance
        tracker = unit3d_up.tracker(data=data)

        # Send the payload
        return unit3d_up.send(tracker=tracker)

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
            tracker_name=self.tracker_name,
            media_type=item.media_type,
        )
        content = video_files.get_data()
        if content is False:
            # skip invalid folder or file
            return
        return content

    def db_search(self, content: Contents):
        # Request results from the video online database
        my_tmdb = TvShow(content.category)
        tv_show_result = my_tmdb.start(content.file_name)
        return tv_show_result

    def video_info(self, content: Contents):
        video_info = Video(
            fileName=str(os.path.join(content.folder, content.file_name))
        )
        return video_info
