# -*- coding: utf-8 -*-
import re

from unit3dup import pvtTracker
from decouple import Config, RepositoryEnv
from rich.console import Console
from database.trackers import TrackerConfig

console = Console(log_path=False)


class Torrent:

    def __init__(self, args_tracker=None):
        tracker_name = args_tracker[0]
        self.tracker_file_env = f"{tracker_name}.env"
        self.tracker_file_json = f"{tracker_name}.json"
        config_load = Config(RepositoryEnv(self.tracker_file_env))
        self.PASS_KEY = config_load("PASS_KEY")
        self.API_TOKEN = config_load("API_TOKEN")
        self.BASE_URL = config_load("BASE_URL")
        self.tracker_values = TrackerConfig(self.tracker_file_json)

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
        tracker_data = tracker.get_name(name=keyword[0], perPage=50)
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
        tracker_data = tracker.get_uploader(uploader=username[0], perPage=50)
        console.log(f"Filter by the torrent uploader's username.. '{username[0].upper()}'")
        self.print_normal(data=tracker_data['data'])

    def get_by_start_year(self, startyear: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.start_year(start_year=startyear[0], perPage=50)
        console.log(f"StartYear torrents.. Return only torrents whose content was released"
                    f" after or in the given year '{startyear[0].upper()}'")
        self.print_normal(data=tracker_data['data'])

    def get_by_end_year(self, end_year: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.end_year(end_year=end_year[0], perPage=50)
        console.log(f"EndYear torrents.. Return only torrents whose content was released before or in the given year"
                    f"'{end_year[0].upper()}'")
        self.print_normal(data=tracker_data['data'])

    def get_by_mediainfo(self, mediainfo: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_mediainfo(mediainfo=mediainfo[0], perPage=50)
        console.log(f"Mediainfo torrents.. Filter by the torrent's mediaInfo.. '{mediainfo[0].upper()}'")
        self.print_normal(data=tracker_data['data'])


    def get_alive(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_alive(alive=True, perPage=50)
        console.log(f"Alive torrents.. Filter by if the torrent has 1 or more seeders")
        self.print_normal(tracker_data['data'])

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
