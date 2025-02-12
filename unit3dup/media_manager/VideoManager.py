# -*- coding: utf-8 -*-
import argparse

from common.external_services.theMovieDB.core.api import DbOnline
from unit3dup.media_manager.common import UserContent
from unit3dup.qbittorrent import QBittorrent
from unit3dup.upload import UploadBot
from unit3dup.pvtVideo import Video
from unit3dup.media import Media
from unit3dup import config


class VideoManager:

    def __init__(self, contents: list["Media"], cli: argparse.Namespace):
        """
        Initialize the VideoManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """

        self.torrent_found:bool = False
        self.contents: list['Media'] = contents
        self.cli: argparse = cli

    def process(self) -> list["QBittorrent"] | None:
        """
           Process the video contents to filter duplicates and create torrents

           Returns:
               list: List of QBittorrent objects created for each content
        """
        qbittorrent_list = []
        for content in self.contents:
            # Filter contents based on existing torrents or duplicates

            if UserContent.is_preferred_language(content=content):
                # Torrent creation
                if not UserContent.torrent_file_exists(content=content, class_name=self.__class__.__name__):
                    self.torrent_found = False
                else:
                    # Torrent found, skip if the watcher is active
                    if self.cli.watcher:
                        continue
                    self.torrent_found = True

                # Skip if it is a duplicate
                if self.cli.duplicate or config.DUPLICATE_ON and UserContent.is_duplicate(content=content):
                    continue

                # Does not create the torrent if the torrent was found earlier
                if not self.torrent_found:
                    torrent_response = UserContent.torrent(content=content)
                else:
                    torrent_response = None


                # Search for the TMDB ID
                db_online = DbOnline(query=content.guess_title,category=content.category)
                tmdb = db_online.media_result

                # Get meta from the media video
                video_info = Video(content.file_name, tmdb_id=tmdb.video_id, trailer_key=tmdb.trailer_key)
                video_info.build_info()


                # Tracker Bot
                unit3d_up = UploadBot(content)

                # Send data to the tracker
                tracker_response, tracker_message =  unit3d_up.send(show_id=tmdb.video_id,
                                                                    show_keywords_list=tmdb.keywords_list,
                                                                    video_info=video_info)
                qbittorrent_list.append(
                    QBittorrent(
                        tracker_response=tracker_response,
                        torrent_response=torrent_response,
                        content=content,
                        tracker_message = tracker_message
                    ))

        # // end content
        return qbittorrent_list
