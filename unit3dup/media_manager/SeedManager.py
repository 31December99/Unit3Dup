# -*- coding: utf-8 -*-

import argparse

from unit3dup.torrent import Torrent
from view import custom_console

class SeedManager:
    def __init__(self, cli: argparse.Namespace, trackers_name_list: list):
         self.cli = cli
         self.trackers_name_list = trackers_name_list
         self.tracker_name = self.trackers_name_list[0]
         self.torrent_info = Torrent(tracker_name=self.tracker_name)

    def process(self, tmdb_id: int) -> None:
        dead = self.torrent_info.get_dead()
        for torrent in dead['data']:
            if tmdb_id == torrent['attributes']['tmdb_id']:
                attribute = torrent['attributes']['details_link']
                name = torrent['attributes']['name']
                tmdb = torrent['attributes']['tmdb_id']
                custom_console.bot_warning_log(f"-> Possible seed {name}: {attribute} : TMDB {tmdb}")


    def run(self, trackers_name_list: list):
        pass



