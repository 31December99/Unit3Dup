# -*- coding: utf-8 -*-
import argparse
import os

from common.external_services.theMovieDB.core.api import DbOnline
from common.bittorrent import BittorrentData

from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup.pvtVideo import Video
from unit3dup.media import Media
from unit3dup import config_settings

from view import custom_console

class VideoManager:

    def __init__(self, contents: list[Media], cli: argparse.Namespace):
        """
        Initialize the VideoManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """

        self.torrent_found:bool = False
        self.contents: list[Media] = contents
        self.cli: argparse = cli

    def process(self, selected_tracker: str, tracker_name_list: list) -> list[BittorrentData] | None:
        """
           Process the video contents to filter duplicates and create torrents

           Returns:
               list: List of Bittorrent objects created for each content
        """

        # -multi : no announce_list . One announce for multi tracker
        if self.cli.mt:
            tracker_name_list = [selected_tracker.upper()]

        #  Init the torrent list
        bittorrent_list = []
        for content in self.contents:
            # Filter contents based on existing torrents or duplicates
            if UserContent.is_preferred_language(content=content):

                if self.cli.watcher:
                    if os.path.exists(content.torrent_path):
                        custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue

                torrent_response = UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                                       selected_tracker=selected_tracker)

                # Skip if it is a duplicate
                if (self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON
                        and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                    continue

                # Search for VIDEO ID
                db_online = DbOnline(media=content,category=content.category)
                db = db_online.media_result

                # Get meta from the media video
                video_info = Video(media=content, tmdb_id=db.video_id, trailer_key=db.trailer_key)
                video_info.build_info()

                # Don't upload if -noup is set to True
                if self.cli.noup:
                    custom_console.bot_warning_log(f"No Upload active. Done.")
                    continue

                # Tracker payload
                unit3d_up = UploadBot(content=content, tracker_name=selected_tracker)

                # Send data to the tracker
                tracker_response, tracker_message =  unit3d_up.send(show_id=db.video_id, imdb_id=db.imdb_id,
                                                                    show_keywords_list=db.keywords_list,
                                                                    video_info=video_info)

                bittorrent_list.append(
                    BittorrentData(
                        tracker_response=tracker_response,
                        torrent_response=torrent_response,
                        content=content,
                        tracker_message = tracker_message
                    ))

        # // end content
        return bittorrent_list
