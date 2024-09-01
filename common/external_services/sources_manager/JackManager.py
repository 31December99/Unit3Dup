# -*- coding: utf-8 -*-

import requests
from common.config import config
from common.external_services.jack import NowPlaying, LatestRelease
from common.custom_console import custom_console


class JackManager:

    def search_jack(self, query):
        params = {
            "apikey": config.JACK_API_KEY,
            "Query": query,
            "Category[]": [2000],
        }

        try:
            response = requests.get(config.JACK_URL, params=params)
            response.raise_for_status()

            results = response.json().get("Results", [])
            for result in results:
                title = result["Title"]
                # Controlla se il torrent è in italiano
                if self.is_italian(title):
                    print(f"[Jack] Title: {title}")
                    # print(f"Link: {result['Link']}")
                    # print(f"Seeders: {result['Seeders']}")
                    # print(f"Peers: {result['Peers']}")
                    print("-" * 40)

        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta: {e}")

    def is_italian(self, title):
        italian_keywords = [
            "ITA",
            "Italian",
            "Italiano",
            "[ITA]",
            "Sub Ita",
            "Ita Subs",
        ]
        return any(keyword.lower() in title.lower() for keyword in italian_keywords)

    def now_playing(self):
        now_playing_list = NowPlaying.get_now_playing()

        for media in now_playing_list:
            latest_release = LatestRelease.get_latest(media.movie_id)
            release = latest_release.release_date()

            # if you preferred language is found
            if release:
                custom_console.print(
                    f"[green]MovieID[/green] {media.movie_id} [green]Title[/green] {media.title}"
                    f" [green]ReleaseDate[/green] {media.release_date}"
                    f" [green]Language[/green] {media.language}"
                )

                # TODO: search for media in the tracker beforehand

                # Search in Jack
                self.search_jack(media.title)
                input("Push a button to continue")
