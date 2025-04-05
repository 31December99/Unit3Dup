# -*- coding: utf-8 -*-

import argparse
import os
from unit3dup.media_manager.common import UserContent
from unit3dup.media import Media
from unit3dup.torrent import Torrent

from common.trackers.trackers import TRACKData
from common.utility import System
from common import title

from view import custom_console

class SeedManager:
    def __init__(self, cli: argparse.Namespace, trackers_name_list: list, torrent_archive_path: str):

         # Command line
         self.cli = cli
         # Tracker list from the command line
         self.trackers_name_list = trackers_name_list
         # Default tracker
         self.tracker_name = self.trackers_name_list[0]
         # torrent archive path
         self.torrent_archive_path = torrent_archive_path
         # class for general torrent requests
         torrent_info = Torrent(tracker_name=self.tracker_name)
         # Get a list of dead torrents
         self.no_seed = torrent_info.get_dead()
         # Get tracker data for the current tracker name
         self.tracker_data = TRACKData.load_from_module(tracker_name=self.tracker_name)



    def process(self, media_id: int, content: Media) -> str | None:

        # Get the IDs
        dead_torrent = []
        if content.category in [System.category_list.get(System.MOVIE), System.category_list.get(System.TV_SHOW)]:
            dead_torrent = [torrent for torrent in self.no_seed['data'] if media_id == torrent['attributes']['tmdb_id']]

        if content.category in [System.category_list.get(System.GAME)]:
            dead_torrent = [torrent for torrent in self.no_seed['data'] if media_id == torrent['attributes']['igdb_id']]

        for dead in dead_torrent:
            if media_id == dead['attributes']['tmdb_id']:
                tracker_title = title.Guessit(dead['attributes']['name'])
                tracker_title_season = tracker_title.guessit_season
                tracker_title_episode = tracker_title.guessit_episode
                if tracker_title_season == content.guess_season and tracker_title_episode == content.guess_episode:
                    custom_console.bot_warning_log(f"'SEED'........ {dead['attributes']['name']}:"
                                                   f" {dead['attributes']['details_link']}\n")
                    return content.torrent_path
        print()
        return None

    def send(self, torrent_path: str):
        # Send a torrent file that has already been created for seeding
        client = UserContent.get_client()
        for selected_tracker in self.trackers_name_list:
                custom_console.bot_warning_log(f"Seeding for {selected_tracker}..Please wait")
                torrent_filepath = os.path.join(self.torrent_archive_path, selected_tracker,
                                                f"{os.path.basename(torrent_path)}.torrent")
                if os.path.exists(torrent_filepath):
                    client.send_file_to_client(torrent_path=torrent_filepath, media_location=os.path.dirname(torrent_path))
                else:
                    custom_console.bot_error_log(f"Torrent file {torrent_filepath} does not exist")
