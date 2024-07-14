# -*- coding: utf-8 -*-

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

    def search(self, keyword: str):
        tracker = pvtTracker.Unit3d(
            base_url=self.BASE_URL, api_token=self.API_TOKEN, pass_key=self.PASS_KEY
        )
        tracker_data = tracker.get_name(keyword[0])
        console.log(f"Searching.. '{keyword[0]}'")

        # float(inf) in caso di None utilizza il suo valore (infinito) come key di ordinamento (ultimo)
        data = sorted(
            tracker_data["data"],
            key=lambda x: x["attributes"].get("release_year", float("inf"))
            or float("inf"),
        )

        for item in data:
            console.log(
                f"[{item['attributes']['release_year']}] - {item['attributes']['name']}"
            )
        print()