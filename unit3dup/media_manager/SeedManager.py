# -*- coding: utf-8 -*-

import argparse

from unit3dup.torrent import Torrent
from view import custom_console
from common.utility import System


class SeedManager:
    def __init__(self, cli: argparse.Namespace, trackers_name_list: list):
         self.cli = cli
         self.trackers_name_list = trackers_name_list
         self.tracker_name = self.trackers_name_list[0]
         self.torrent_info = Torrent(tracker_name=self.tracker_name)

    def process(self, media_id: int, category: int) -> None:

        no_seeded = self.torrent_info.get_dead()

        dead_torrent = []
        if category in [System.category_list.get(System.MOVIE), System.category_list.get(System.TV_SHOW)]:
            dead_torrent = [torrent for torrent in no_seeded['data'] if media_id == torrent['attributes']['tmdb_id']]

        if category in [System.category_list.get(System.GAME)]:
            dead_torrent = [torrent for torrent in no_seeded['data'] if media_id == torrent['attributes']['igdb_id']]


        for torrent in dead_torrent:
            attribute = torrent['attributes']['details_link']
            name = torrent['attributes']['name']
            tmdb = torrent['attributes']['tmdb_id']
            igdb = torrent['attributes']['igdb_id']
            custom_console.bot_warning_log(f"\n-> Possible seed {name}: {attribute} : TMDB {tmdb} IGDB {igdb}")
            input("Press enter to continue...")






    def run(self, trackers_name_list: list):
        pass



