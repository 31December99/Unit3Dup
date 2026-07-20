# -*- coding: utf-8 -*-
import os

from unit3dup.common.external_services.theMovieDB.core.api import DbOnline
from unit3dup.common.bittorrent import BittorrentData
from unit3dup.common.bot_config import BotConfig
from unit3dup.common.tags import SearchTags
from unit3dup.common.utility import System
from unit3dup.media_manager.common import UserContent
from unit3dup.upload import UploadBot
from unit3dup import config_settings
from unit3dup.pvtVideo import Video
from unit3dup.media import Media
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
            torrent_filepath = System.get_torrent_archive_path(tracker_archive, selected_tracker, content.torrent_name)

            # Filter contents based on existing torrents or duplicates
            if UserContent.is_preferred_language(content=content):

                if self.cli.watcher:
                    if os.path.exists(torrent_filepath):
                        custom_console.bot_log(f"Watcher Active.. skip the old upload '{content.file_name}'")
                        continue

                torrent_response = UserContent.torrent(content=content, tracker_name_list=tracker_name_list,
                                                       selected_tracker=selected_tracker, this_path=torrent_filepath)

                # Skip(S) if it is a duplicate or let the user choose to continue (C)
                if (self.cli.duplicate or config_settings.user_preferences.DUPLICATE_ON
                        and UserContent.is_duplicate(content=content, tracker_name=selected_tracker,
                                                     cli=self.cli)):
                    continue

                # Search for VIDEO ID
                db_online = DbOnline(media=content, no_title=self.cli.notitle)
                # db = db_online.media_result

                # If it is 'None' we skipped the imdb search (-notitle)
                if not db_online.media_result:
                    continue

                # Get meta from the media video
                # video_info = Video(media=content, tmdb_id=db.video_id, trailer_key=db.trailer_key)
                video_info = Video(media=content, db_online=db_online)
                video_info.build_info()

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
                processed_data = unit3d_up.data(show_id=db.video_id, imdb_id=db.imdb_id, tvdb_id=db.tvdb_id,
                                                show_keywords_list=db.keywords_list, video_info=video_info)

                # Do not upload if an error occurs
                if not processed_data:
                    continue

                # Don't upload if -noup is set to True
                if self.cli.noup:
                    custom_console.bot_warning_log(f"No Upload active. Done.")
                    continue

                # Send data to the tracker
                tracker_response, tracker_message = unit3d_up.send(torrent_archive=torrent_filepath)

                # Download the updated torrent file from the tracker
                # # https://github.com/HDInnovations/UNIT3D/pull/4910/files
                if tracker_response:
                    UserContent.download_file(url=tracker_response, destination_path=torrent_filepath)

                # Store response for the torrent clients
                bittorrent_list.append(
                    BittorrentData(
                        tracker_response=tracker_response,
                        torrent_response=torrent_response,
                        content=content,
                        tracker_message=tracker_message,
                        archive_path=torrent_filepath,
                    ))

        # // end content
        return bittorrent_list
