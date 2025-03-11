# -*- coding: utf-8 -*-
import argparse

from common.external_services.theMovieDB.core.api import DbOnline
from common.bittorrent import BittorrentData

from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup.pvtVideo import Video
from unit3dup.media import Media
from unit3dup import config_settings

from view import custom_console

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


        if self.cli.cross:
            self.trackers_name_list = config_settings.tracker_config.MULTI_TRACKER
        else:
            self.trackers_name_list = []

        if self.cli.tracker:
            self.trackers_name_list = [self.cli.tracker.upper()]


    def process(self, selected_tracker: str) -> list["BittorrentData"] | None:
        """
           Process the video contents to filter duplicates and create torrents

           Returns:
               list: List of Bittorrent objects created for each content
        """

        bittorrent_list = []
        for content in self.contents:
            # Filter contents based on existing torrents or duplicates

            if UserContent.is_preferred_language(content=content):
                # Torrent creation
                if not UserContent.torrent_file_exists(content=content, announces_list=self.trackers_name_list):
                    self.torrent_found = False
                else:
                    # Torrent found, skip if the watcher is active
                    if self.cli.watcher:
                        custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                        continue
                    self.torrent_found = True

                # Skip if it is a duplicate
                if (self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON
                        and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                    continue

                # Does not create the torrent if the torrent was found earlier
                if not self.torrent_found:
                    torrent_response = UserContent.torrent(content=content, tracker_name=selected_tracker)
                else:
                    torrent_response = None

                # Search for VIDEO ID
                db_online = DbOnline(query=content.guess_title,category=content.category)
                db = db_online.media_result

                # Don't upload if -noup is set to True
                if self.cli.noup:
                    custom_console.bot_warning_log(f"No Upload active. Done.")
                    return []

                # Get meta from the media video
                video_info = Video(content.file_name, tmdb_id=db.video_id, trailer_key=db.trailer_key)
                video_info.build_info()

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
