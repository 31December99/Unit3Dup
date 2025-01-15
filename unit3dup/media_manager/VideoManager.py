# -*- coding: utf-8 -*-
import argparse
import os
import diskcache

from unit3dup.media_manager.models.qbitt import QBittorrent
from unit3dup.upload import UploadVideo
from unit3dup.contents import Contents
from unit3dup.pvtVideo import Video

from common.utility.contents import UserContent
from common.config import config, default_env_path_cache
from common.custom_console import custom_console

class VideoManager:

    def __init__(self, contents: list["Contents"], cli: argparse.Namespace):
        """
        Initialize the VideoManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """

        self.contents = contents
        self.cli = cli

        # description cache
        self.cache = diskcache.Cache(str(default_env_path_cache))

    def process(self) -> list["QBittorrent"] | None:
        """
           Process the video contents to filter duplicates and create torrents

           Returns:
               list: List of QBittorrent objects created for each content
        """
        qbittorrent_list = []
        for content in self.contents:

            # Filter contents based on existing torrents or duplicates
            if (
                UserContent.is_preferred_language(content=content) or
                (self.cli.duplicate or config.DUPLICATE_ON)
            ):

                if not UserContent.is_duplicate(content=content):
                    # Search for the TMDB ID
                    tmdb_result = UserContent.tmdb(content=content)

                    # if the cache description is enabled
                    video_info = self.load_cache(index_=tmdb_result.video_id)
                    # if there is no available cached description
                    if not video_info:
                        # get a new description if cache is disabled
                        file_name = str(os.path.join(content.folder, content.file_name))
                        video_info = Video.info(file_name, tmdb_id=tmdb_result.video_id, trailer_key=tmdb_result.trailer_key)
                    # cache it if cache is enabled
                    self.cache_it(index_=tmdb_result.video_id, data=video_info )

                    # Tracker payload
                    unit3d_up = UploadVideo(content)
                    data = unit3d_up.payload(tv_show=tmdb_result, video_info=video_info)

                    # Torrent creation
                    if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                        torrent_response = UserContent.torrent(content=content)
                    else:
                        torrent_response = None

                    # Get a new tracker instance
                    tracker = unit3d_up.tracker(data=data)

                    # Upload
                    tracker_response = unit3d_up.send(tracker=tracker)

                    qbittorrent_list.append(
                        QBittorrent(
                            tracker_response=tracker_response,
                            torrent_response=torrent_response,
                            content=content
                        ))
        # // end content
        return qbittorrent_list


    def cache_it(self, index_: int, data: Video)-> bool:
        if config.CACHE_SCR:
            # cache only if it's a new description
            if index_ not in self.cache:
                self.cache[index_] = data.description
                custom_console.bot_warning_log("Cached !")
                return True
        return False

    def load_cache(self, index_: int)-> Video:
            # if Cache is enabled
            if config.CACHE_SCR:
                # if a description is found
                if index_ in self.cache:
                    custom_console.bot_warning_log(f"** {self.__class__.__name__} **: Using cached Description !")
                    try:
                        # Return frames from the cache
                        return self.cache[index_]
                    except KeyError:
                        custom_console.bot_error_log("Cached frame not found or cache file corrupted")
                        custom_console.bot_error_log("Proceed to extract the screenshot again. Please wait..")
