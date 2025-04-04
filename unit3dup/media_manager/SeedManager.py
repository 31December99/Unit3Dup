# -*- coding: utf-8 -*-

import argparse

from unit3dup.media import Media
from unit3dup.torrent import Torrent
from view import custom_console
from common.utility import System


class SeedManager:
    def __init__(self, cli: argparse.Namespace, trackers_name_list: list):

         # Command line
         self.cli = cli
         # Tracker list from the command line
         self.trackers_name_list = trackers_name_list
         # Default tracker
         self.tracker_name = self.trackers_name_list[0]
         # class for general torrent requests
         self.torrent_info = Torrent(tracker_name=self.tracker_name)

    def process(self, media_id: int, content: Media) -> list[Torrent]:

        # Get a list of dead torrents
        no_seeded = self.torrent_info.get_dead()

        # Get the IDs
        dead_torrent = []
        if content.category in [System.category_list.get(System.MOVIE), System.category_list.get(System.TV_SHOW)]:
            dead_torrent = [torrent for torrent in no_seeded['data'] if media_id == torrent['attributes']['tmdb_id']]

        if content.category in [System.category_list.get(System.GAME)]:
            dead_torrent = [torrent for torrent in no_seeded['data'] if media_id == torrent['attributes']['igdb_id']]

        # Compare and add the matching torrent to seed list
        seed_list = []
        for torrent in dead_torrent:
            attribute = torrent['attributes']['details_link']
            name = torrent['attributes']['name']
            tmdb = torrent['attributes']['tmdb_id']
            igdb = torrent['attributes']['igdb_id']

            if media_id==tmdb:
                custom_console.bot_warning_log(f"\n-> Possible seed {name}: {attribute}")
                seed_list.append(torrent)
        return seed_list




