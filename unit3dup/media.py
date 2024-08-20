# -*- coding: utf-8 -*-

from unit3dup.automode import Auto
from rich.console import Console
from unit3dup.files import Files
from unit3dup.qbitt import Qbitt
from unit3dup import config
from unit3dup.media_manager.VideoManager import VideoManager
from unit3dup.media_manager.DocuManager import DocuManager

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
        self.docu_category = self.config.tracker_values.category("edicola")

    def process_contents(self, mode="man"):
        if mode == "man":
            files = self.manual()
        else:
            files = self.auto()

        # for each item we have to grab media info
        for item in files:
            content = self.get_media(item)
            if not content:
                continue
            self.contents.append(content)
        return self.contents

    def process(self, mode="man"):
        contents = self.process_contents(mode=mode)

        response = None
        my_torrent = None
        for content in contents:
            console.rule(content.file_name)

            if (
                    content.category == self.movie_category
                    or content.category == self.serie_category
            ):
                video_manager = VideoManager(content=content)

                if config.DUPLICATE == 'True':
                    results = video_manager.check_duplicate()
                    if results:
                        console.log(
                            f"\n*** User chose to skip '{content.file_name}' ***\n"
                        )
                        continue

                my_torrent = video_manager.torrent()
                if my_torrent:
                    response = video_manager.upload()
                else:
                    # If writing the torrent fails, it skips the uploading and seeding
                    continue

            if content.category == self.docu_category:
                docu_manager = DocuManager(content=content)
                my_torrent = docu_manager.torrent()
                if my_torrent:
                    response = docu_manager.upload()

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

    def get_media(self, item):
        """
        Getting ready for tracker upload
        Return
              - torrent name (filename or folder name)
              - content category ( movie or serie)
              - torrent meta_info
        """
        files = Files(
            path=item.torrent_path,
            tracker_name=self.tracker_name,
            media_type=item.media_type,
        )
        content = files.get_data()
        if content is False:
            # skip invalid folder or file
            return
        return content
