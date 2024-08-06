# -*- coding: utf-8 -*-
from unit3dup.torrent import Torrent
from unit3dup.contents import Contents
from rich.console import Console
from unit3dup import title
from unit3dup import config
from unit3dup import pvtTracker

console = Console(log_path=False)


class Dupe:

    def __init__(self, content: Contents, tracker_name: str, new_info_hash: str):
        self.content: Contents = content
        self.torrent_info = Torrent()
        self.new_info_hash = new_info_hash
        self.config = config.trackers.get_tracker(tracker_name)
        self.API_TOKEN = self.config.api_token
        self.BASE_URL = self.config.base_url
        self.guess_filename = title.Guessit(content.name)

        self.tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=""
        )

    def search(self) -> bool:
        self.torrent_info.search(self.guess_filename.guessit_title)
        tracker_data = self.tracker.get_name(name=self.guess_filename.guessit_title, perPage=30)
        for t_data in tracker_data['data']:
            info_hash = t_data['attributes']['info_hash']
            if self.new_info_hash in info_hash:
                console.log("Already uploaded.Same info_hash !")
                return False
        console.log(" New entry !")
        return True
