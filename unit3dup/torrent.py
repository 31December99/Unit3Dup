# -*- coding: utf-8 -*-
import re

from unit3dup import pvtTracker
from decouple import Config, RepositoryEnv
from rich.console import Console

console = Console(log_path=False)


class Torrent:

    def __init__(self, tracker_name=None):
        self.tracker = "itt.env" if not tracker_name else f"{tracker_name[0]}.env"
        config_load = Config(RepositoryEnv(self.tracker))
        self.PASS_KEY = config_load("PASS_KEY")
        self.API_TOKEN = config_load("API_TOKEN")
        self.BASE_URL = config_load("BASE_URL")

    def get_unique_id(self, media_info: str) -> str:
        # Divido per campi
        raw_media = media_info.split('\r')
        unique_id = '-' * 40
        if len(raw_media) > 1:
            match = re.search(r"Unique ID\s+:\s+(\d+)", media_info)
            if match:
                unique_id = match.group(1)
        return unique_id

    def print_info(self, data: list):
        for item in data:
            # Ottengo media info
            media_info = item['attributes']['media_info']
            unique_id = self.get_unique_id(media_info=media_info) if media_info else '-' * 40
            # console.print o log non stampa info_hash !
            print(f"[{str(item['attributes']['release_year'])}] - [{item['attributes']['info_hash']}] [{unique_id}]"
                  f" -> {item['attributes']['name']}")

    def print_normal(self, data: list):
        for item in data:
            console.log(f"[{str(item['attributes']['release_year'])}] - {item['attributes']['name']}")

    def search(self, keyword: str, info=False):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_name(keyword[0], 50)
        console.log(f"Searching.. '{keyword[0]}'")
        # float(inf) in caso di None utilizza il suo valore (infinito) come key di ordinamento (ultimo)
        data = sorted(
            tracker_data["data"],
            key=lambda x: x["attributes"].get("release_year", float("inf"))
                          or float("inf"),
        )

        if info:
            self.print_info(data=data)
        else:
            self.print_normal(data=data)

    def get_by_uploader(self, username: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_uploader(username[0], 50)
        console.log(f"Filter by the torrent uploader's username.. '{username[0].upper()}'")
        self.print_normal(data=tracker_data['data'])

    def get_dead(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_dead(dead=True, perPage=50)
        console.log(f"Dead torrents.. Filter by if the torrent has 0 seeders")
        self.print_normal(tracker_data['data'])

    def get_dying(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_dying(dying=True, perPage=50)
        console.log(f"Dying torrents.. Filter by if the torrent has 1 seeder and has been downloaded more than 3 times")
        self.print_normal(tracker_data['data'])
