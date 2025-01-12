# -*- coding: utf-8 -*-
import argparse
import os

from unit3dup.media_manager.models.qbitt import QBittorrent
from unit3dup.upload import UploadVideo
from unit3dup.contents import Contents
from unit3dup.pvtVideo import Video

from common.utility.contents import UserContent
from common.config import config

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
                (self.cli.duplicate or config.DUPLICATE_ON) and not UserContent.is_duplicate(content=content)
            ):

                # Search for the TMDB ID
                tmdb_result = UserContent.tmdb(content=content)

                # Create a description
                file_name = str(os.path.join(content.folder, content.file_name))
                video_info = Video.info(file_name, tmdb_id=tmdb_result.video_id, trailer_key=tmdb_result.trailer_key)

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
            return qbittorrent_list



