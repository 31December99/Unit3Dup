# -*- coding: utf-8 -*-

import argparse
import os
import pprint
import requests

from common.external_services.theMovieDB.core.api import DbOnline
from unit3dup.media_manager.common import UserContent
from unit3dup.media import Media
from unit3dup.torrent import Torrent

from common.bittorrent import BittorrentData
from common.trackers.trackers import TRACKData
from common.utility import System
from common import title


from view import custom_console

class SeedManager:
    def __init__(self, contents: list[Media], cli: argparse.Namespace):

         self.contents = contents
         # Command line
         self.cli = cli
         # Tracker list from the command line
         # self.trackers_name_list = trackers_name_list

         # Default tracker
         # self.tracker_name = self.trackers_name_list[0]

         # torrent archive path
         # self.torrent_archive_path = torrent_archive_path
         # class for general torrent requests
         # Get tracker data for the current tracker name


    def process(self, selected_tracker: str, trackers_name_list: list, tracker_archive: str) -> BittorrentData | None:

        # Tracker new instance
        torrent_info = Torrent(tracker_name=selected_tracker)
        # self.tracker_data = TRACKData.load_from_module(tracker_name=select_tracker)

        # Get a list of dead torrents
        no_seed = torrent_info.get_dead()

        # Iterate user content
        if self.contents:
            for content in self.contents:

                # get the archive path
                archive = os.path.join(tracker_archive, selected_tracker)
                os.makedirs(archive, exist_ok=True)
                torrent_filepath = os.path.join(tracker_archive, selected_tracker, f"{content.torrent_name}.torrent")

                # Search for tmdb ID
                db_online = DbOnline(media=content, category=content.category, no_title=self.cli.notitle)
                db = db_online.media_result
                # Compare the user's video ID against the tracker tmdb id
                tracker_download_url = self.death(media_id=db.video_id, content=content, dead_torrents=no_seed)
                if tracker_download_url:
                    return BittorrentData(
                        tracker_response=tracker_download_url,
                        torrent_response=None,
                        content=content,
                        tracker_message={},
                        archive_path=torrent_filepath,
                    )

    @staticmethod
    def death(media_id: int, content: Media, dead_torrents: requests) -> str | None:

        # Get the IDs
        dead_torrent = []
        if content.category in [System.category_list.get(System.MOVIE), System.category_list.get(System.TV_SHOW)]:
            dead_torrent = [torrent for torrent in dead_torrents['data'] if media_id == torrent['attributes']['tmdb_id']]

        for dead in dead_torrent:
            if media_id == dead['attributes']['tmdb_id']:
                tracker_title = title.Guessit(dead['attributes']['name'])
                tracker_download_url = dead['attributes']['download_link']
                tracker_title_season = tracker_title.guessit_season
                tracker_title_episode = tracker_title.guessit_episode
                if tracker_title_season == content.guess_season and tracker_title_episode == content.guess_episode:
                    custom_console.bot_warning_log(f"'SEED'........ {dead['attributes']['name']}:"
                                                   f" {dead['attributes']['details_link']}\n")
                return tracker_download_url
        print()
        return None