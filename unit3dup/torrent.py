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
        print()

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
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_types(self, type_name: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_types(type_id=self.tracker_values.type_id(type_name[0]), perPage=25)
        console.log(f"Types torrents.. Filter by the torrent's type.. '{type_name[0].upper()}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_res(self, res_name: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_res(res_id=self.tracker_values.res_id(res_name[0]), perPage=25)
        console.log(f"Resolutions torrents.. Filter by the torrent's resolution.. '{res_name[0].upper()}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_filename(self, file_name: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_filename(file_name=file_name[0], perPage=25)
        console.log(f"Filename torrents.. Filter by the torrent's filename.. '{file_name[0].upper()}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_tmdb_id(self, tmdb_id: int):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_tmdb(tmdb_id=tmdb_id, perPage=25)
        console.log(f"TMDB torrents.. Filter by the torrent's tmdb.. '{tmdb_id}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_imdb_id(self, imdb_id: int):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_imdb(imdb_id=imdb_id, perPage=25)
        console.log(f"IMDB torrents.. Filter by the torrent's imdb.. '{imdb_id}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_tvdb_id(self, tvdb_id: int):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_tvdb(tvdb_id=tvdb_id, perPage=25)
        console.log(f"TVDB torrents.. Filter by the torrent's tvdb.. '{tvdb_id}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_mal_id(self, mal_id: int):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_mal(mal_id=mal_id, perPage=25)
        console.log(f"MAL torrents.. Filter by the torrent's mal.. '{mal_id}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_season(self, season: int):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_season_number(se_number=season, perPage=25)
        console.log(f"Seasons torrents.. Filter by the torrent's seasons.. '{season}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_by_episode(self, episode: int):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_episode_number(ep_number=episode, perPage=25)
        console.log(f"Episode torrents.. Filter by the torrent's episode.. '{episode}'")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_alive(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_alive(alive=True, perPage=50)
        console.log(f"Alive torrents.. Filter by if the torrent has 1 or more seeders")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_dead(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_dead(dead=True, perPage=50)
        console.log(f"Dead torrents.. Filter by if the torrent has 0 seeders")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_dying(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_dying(dying=True, perPage=50)
        console.log(f"Dying torrents.. Filter by if the torrent has 1 seeder and has been downloaded more than 3 times")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])

    def get_doubleup(self):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_double_up(double_up=True, perPage=50)
        console.log(f"DoubleUp torrents.. Filter by if the torrent offers double upload")
        if tracker_data:
            self.print_normal(data=tracker_data['data'])
