# -*- coding: utf-8 -*-
import argparse
import os

from common.external_services.theMovieDB.core.api import DbOnline
from common.bittorrent import BittorrentData
from common.utility import System

from unit3dup.media_manager.SeedManager import SeedManager
from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup import config_settings
from unit3dup.pvtVideo import Video
from unit3dup.media import Media

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

    def process(self, selected_tracker: str, tracker_name_list: list, tracker_archive: str) -> list[BittorrentData] | None:
        """
           Process the video contents to filter duplicates and create torrents

           Returns:
               list: List of Bittorrent objects created for each content
        """

        # Tracker administration
        seed_manager = SeedManager(cli=self.cli, trackers_name_list=tracker_name_list)

        # -multi : no announce_list . One announce for multi tracker
        if self.cli.mt:
            tracker_name_list = [selected_tracker.upper()]

        #  Init the torrent list
        bittorrent_list = []
        for content in self.contents :

            # -notitle flags works only with Tv
            if content.category not in  System.category_list.get(System.TV_SHOW) and self.cli.notitle:
                continue

            # get the archive path
            archive = os.path.join(tracker_archive, selected_tracker)
            os.makedirs(archive, exist_ok=True)
            torrent_filepath = os.path.join(tracker_archive,selected_tracker, f"{content.torrent_name}.torrent")

            # Filter contents based on existing torrents or duplicates
            if UserContent.is_preferred_language(content=content):

                if self.cli.watcher:
                    if os.path.exists(content.torrent_path):
                        custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                    continue

                torrent_response = UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                                       selected_tracker=selected_tracker, this_path=torrent_filepath)

                # Skip if it is a duplicate
                if (self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON
                        and UserContent.is_duplicate(content=content, tracker_name=selected_tracker)):
                    continue

                # Search for VIDEO ID
                db_online = DbOnline(media=content,category=content.category, season=self.cli.notitle)
                db = db_online.media_result

                # If it is 'None' we skipped the imdb search (-notitle)
                if not db:
                    continue

                # Update display name with Serie Title when requested by the user (-notitle)
                if self.cli.notitle:
                    # Add generated metadata to the display_title
                    if self.cli.gentitle:
                        content.display_name = f"{db_online.media_result.result.get_title()}.{db_online.media_result.year}."
                        content.display_name+= content.generate_title
                    else:
                        # otherwise keep the old meta_data and add the new display_title to it
                         meta_info_title = content.display_name.replace(content.guess_title, "")
                         content.display_name = (f"{db_online.media_result.result.get_title()}."
                                                 f"{db_online.media_result.year}.{meta_info_title}")


                # Run the seeding process if requested by the user
                if self.cli.reseed:
                    seed_manager.process(media_id = db.video_id, category = content.category)
                    seed_manager.run(trackers_name_list=tracker_name_list)
                    continue

                # Get meta from the media video
                video_info = Video(media=content, tmdb_id=db.video_id, trailer_key=db.trailer_key)
                video_info.build_info()

                # Tracker instance
                unit3d_up = UploadBot(content=content, tracker_name=selected_tracker)

                # Get the data
                unit3d_up.data(show_id=db.video_id, imdb_id=db.imdb_id, show_keywords_list=db.keywords_list,
                               video_info=video_info)

                # Don't upload if -noup is set to True
                if self.cli.noup:
                    custom_console.bot_warning_log(f"No Upload active. Done.")
                    continue

                # Send to the tracker
                tracker_response, tracker_message =  unit3d_up.send(torrent_archive=torrent_filepath)


                # Store response for the torrent clients
                bittorrent_list.append(
                    BittorrentData(
                        tracker_response=tracker_response,
                        torrent_response=torrent_response,
                        content=content,
                        tracker_message = tracker_message,
                        archive_path=torrent_filepath,
                    ))

        # // end content
        return bittorrent_list
