# -*- coding: utf-8 -*-
import os

from unit3dup.external.torrent.bittorrent import BittorrentData
from unit3dup.external.video.media_service.tags import SearchTags
from unit3dup.external.video.pvtVideo import Video
from unit3dup.external.movie_db.api import DbOnline
from unit3dup.external.media import Media
from unit3dup.external.tracker.upload import UploadBot

from unit3dup.application.user_content import UserContent
from unit3dup.config.bot_config import BotConfig
from unit3dup.shared.utility import System
from unit3dup import config_settings
from unit3dup.view import custom_console


class VideoManager:

    def __init__(self, contents: list[Media], cli: BotConfig):
        """
        Initialize the VideoManager with the given contents

        Args:
            contents (list): List of content media objects
            cli (argparse.Namespace): user flag Command line
        """

        self.torrent_found: bool = False
        self.contents: list[Media] = contents
        self.cli: BotConfig = cli

    def process(self, selected_tracker: str, tracker_name_list: list, tracker_archive: str) -> list[BittorrentData]:
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
        # Tags list extracted used to build title ( -b flag)
        tags_dictionary = {}
        for content in self.contents:
            # /// User request to build the title; overwriting display_name
            if self.cli.buildtags:
                search_tags = SearchTags(media=content)
                content.display_name, tags_dictionary = search_tags.process()

            # get the archive path
            content.torrent_metadata_path = System.get_torrent_archive_path(tracker_archive, selected_tracker,
                                                                            content.torrent_name)

            # Filter contents based on existing torrents or duplicates
            if UserContent.is_preferred_language(content=content):

                if self.cli.watcher:
                    if os.path.exists(content.torrent_metadata_path):
                        custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                        continue

                # Create a new torrent
                UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                    selected_tracker=selected_tracker, this_path=content.torrent_metadata_path)

                # Skip(S) if it is a duplicate or let the user choose to continue (C)
                if (self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON
                        and UserContent.is_duplicate(content=content, tracker_name=selected_tracker,
                                                     cli=self.cli)):
                    continue

                # Search for VIDEO ID
                db_online = DbOnline(media=content, no_title=self.cli.notitle)
                content.media_result = db_online.media_result

                # If it is 'None' we skipped the imdb search (-notitle)
                if not db_online.media_result:
                    continue

                # Get meta from the media video
                video_info = Video(media=content, tmdb_id=content.media_result.video_id,
                                   trailer_key=content.media_result.trailer_key)
                video_info.build_info()
                content.torrent_description = video_info.description
                content.is_hd = video_info.is_hd

                # Tags found ( -b flag)
                if tags_dictionary:
                    custom_console.bot_log(f"\n[GENERATING DISPLAYNAME..]")
                    for key, value in tags_dictionary.items():
                        if isinstance(value, list):
                            value = " ".join(value)
                        custom_console.bot_log(f"{key:<13} '{value}'")
                    custom_console.bot_log(f"Done.\n")
                else:
                    # print the title will be shown on the torrent page
                    custom_console.bot_log(f"'DISPLAYNAME'...{{{content.display_name}}}\n")

                # Tracker instance
                unit3d_up = UploadBot(content=content, tracker_name=selected_tracker, cli=self.cli)

                # Get the data
                processed_data = unit3d_up.data(content=content)

                # Do not upload if an error occurs
                if not processed_data:
                    continue

                # Don't upload if -noup is set to True
                if self.cli.noup:
                    custom_console.bot_warning_log(f"No Upload active. Done.")
                    continue

                # Send data to the tracker
                tracker_response, tracker_message = unit3d_up.send()

                # Download the updated torrent file from the tracker
                # # https://github.com/HDInnovations/UNIT3D/pull/4910/files
                if tracker_response:
                    UserContent.download_file(url=tracker_response, destination_path=content.torrent_metadata_path)

                # Store response for the torrent clients
                bittorrent_list.append(
                    BittorrentData(
                        tracker_response=tracker_response,
                        content=content,
                        tracker_message=tracker_message,
                        archive_path=content.torrent_metadata_path,
                    ))

        # // end content
        return bittorrent_list
