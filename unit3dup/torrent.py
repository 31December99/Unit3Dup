# -*- coding: utf-8 -*-
import re

import requests

from unit3dup import pvtTracker
from rich.console import Console
from unit3dup import config

console = Console(log_path=False)


class Torrent:

    def __init__(self):
        self.perPage = 30
        self.tracker = pvtTracker.Unit3d(
            base_url=config.BASE_URL, api_token=config.API_TOKEN, pass_key=""
        )

        print()

    def get_unique_id(self, media_info: str) -> str:
        # Divido per campi
        raw_media = media_info.split("\r")
        unique_id = "-" * 40
        if len(raw_media) > 1:
            match = re.search(r"Unique ID\s+:\s+(\d+)", media_info)
            if match:
                unique_id = match.group(1)
        return unique_id

    def search(self, keyword: str) -> requests:
        return self.tracker.get_name(name=keyword, perPage=self.perPage)

    def get_by_description(self, description: str) -> requests:
        return self.tracker.get_description(
            description=description, perPage=self.perPage
        )

    def get_by_bdinfo(self, bdinfo: str) -> requests:
        return self.tracker.get_bdinfo(bdinfo=bdinfo, perPage=self.perPage)

    def get_by_uploader(self, username: str) -> requests:
        return self.tracker.get_uploader(
            uploader=username, perPage=self.perPage
        )

    def get_by_start_year(self, startyear: str) -> requests:
        return self.tracker.start_year(
            start_year=startyear, perPage=self.perPage
        )

    def get_by_end_year(self, end_year: str) -> requests:
        return self.tracker.end_year(end_year=end_year, perPage=self.perPage)

    def get_by_mediainfo(self, mediainfo: str) -> requests:
        return self.tracker.get_mediainfo(
            mediainfo=mediainfo, perPage=self.perPage
        )

    def get_by_types(self, type_name: str) -> requests:
        return self.tracker.get_types(
            type_id=config.tracker_values.type_id(type_name), perPage=self.perPage
        )

    def get_by_res(self, res_name: str) -> requests:
        return self.tracker.get_res(
            res_id=config.tracker_values.res_id(res_name), perPage=self.perPage
        )

    def get_by_filename(self, file_name: str) -> requests:
        return self.tracker.get_filename(
            file_name=file_name, perPage=self.perPage
        )

    def get_by_tmdb_id(self, tmdb_id: int) -> requests:
        return self.tracker.get_tmdb(tmdb_id=tmdb_id, perPage=self.perPage)

    def get_by_imdb_id(self, imdb_id: int) -> requests:
        return self.tracker.get_imdb(imdb_id=imdb_id, perPage=self.perPage)

    def get_by_tvdb_id(self, tvdb_id: int) -> requests:
        return self.tracker.get_tvdb(tvdb_id=tvdb_id, perPage=self.perPage)

    def get_by_mal_id(self, mal_id: int) -> requests:
        return self.tracker.get_mal(mal_id=mal_id, perPage=self.perPage)

    def get_by_playlist_id(self, playlist_id: int) -> requests:
        return self.tracker.get_playlist_id(
            playlist_id=playlist_id, perPage=self.perPage
        )

    def get_by_collection_id(self, collection_id: int) -> requests:
        return self.tracker.get_collection_id(
            collection_id=collection_id, perPage=self.perPage
        )

    def get_by_freeleech(self, freeleech: int) -> requests:
        return self.tracker.get_freeleech(
            freeleech=freeleech, perPage=self.perPage
        )

    def get_by_season(self, season: int) -> requests:
        return self.tracker.get_season_number(
            se_number=season, perPage=self.perPage
        )

    def get_by_episode(self, episode: int) -> requests:
        return self.tracker.get_episode_number(
            ep_number=episode, perPage=self.perPage
        )

    def get_alive(self) -> requests:
        return self.tracker.get_alive(alive=True, perPage=self.perPage)

    def get_dead(self) -> requests:
        return self.tracker.get_dead(dead=True, perPage=self.perPage)

    def get_dying(self) -> requests:
        return self.tracker.get_dying(dying=True, perPage=self.perPage)

    def get_doubleup(self) -> requests:
        return self.tracker.get_double_up(double_up=True, perPage=self.perPage)

    def get_featured(self) -> requests:
        return self.tracker.get_featured(featured=True, perPage=self.perPage)

    def get_refundable(self) -> requests:
        return self.tracker.get_refundable(
            refundable=True, perPage=self.perPage
        )

    def get_stream(self) -> requests:
        return self.tracker.get_stream(stream=True, perPage=self.perPage)

    def get_sd(self) -> requests:
        return self.tracker.get_sd(sd=True, perPage=self.perPage)

    def get_highspeed(self) -> requests:
        return self.tracker.get_highspeed(highspeed=True, perPage=self.perPage)

    def get_internal(self) -> requests:
        return self.tracker.get_internal(internal=True, perPage=self.perPage)

    def get_personal(self) -> requests:
        return self.tracker.get_personal_release(
            personalRelease=True, perPage=self.perPage
        )


class View(Torrent):

    def __init__(self):
        super().__init__()
        self.perPage = 30
        self.tracker = pvtTracker.Unit3d(
            base_url=config.BASE_URL, api_token=config.API_TOKEN, pass_key=""
        )

        print()

    def get_unique_id(self, media_info: str) -> str:
        # Divido per campi
        raw_media = media_info.split("\r")
        unique_id = "-" * 40
        if len(raw_media) > 1:
            match = re.search(r"Unique ID\s+:\s+(\d+)", media_info)
            if match:
                unique_id = match.group(1)
        return unique_id

    def print_info(self, tracker_data: dict):
        data = [item for item in tracker_data["data"]]
        for item in data:
            # Ottengo media info
            media_info = item["attributes"]["media_info"]
            unique_id = (
                self.get_unique_id(media_info=media_info) if media_info else "-" * 40
            )
            # console.print o log non stampa info_hash !
            print(
                f"[{str(item['attributes']['release_year'])}] - [{item['attributes']['info_hash']}] [{unique_id}]"
                f" -> {item['attributes']['name']}"
            )

    def print_normal(self, tracker_data: dict):
        data = [item for item in tracker_data["data"]]
        for item in data:
            console.log(
                f"[{str(item['attributes']['release_year'])}] - {item['attributes']['name']}"
            )

    def page_view(self, tracker_data: dict, tracker: pvtTracker, info=False):

        self.print_normal(tracker_data) if not info else self.print_info(tracker_data)
        page = 0
        while True:
            if not tracker_data["links"]["next"]:
                break

            page += 1
            console.print(
                f"\n Prossima Pagina '{page}' - Premi un tasto per continuare, Q(quit) - ",
                end="",
            )
            if input().lower() == "q":
                break
            print()
            console.rule(f"\n[bold blue]'Page -> {page}'", style="#ea00d9")
            tracker_data = tracker.next(url=tracker_data["links"]["next"])
            (
                self.print_normal(tracker_data)
                if not info
                else self.print_info(tracker_data)
            )

    def view_search(self, keyword: str, info=False):
        tracker_data = self.search(keyword=keyword)
        console.log(f"Searching.. '{keyword}'")
        (
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)
            if not info
            else self.page_view(
                tracker_data=tracker_data, tracker=self.tracker, info=True
            )
        )

    def view_by_description(self, description: str):
        tracker_data = self.get_by_description(description=description)
        console.log(f"Filter by the torrent's description.. '{description.upper()}'")
        self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_bdinfo(self, bdinfo: str):
        tracker_data = self.get_by_bdinfo(self, bdinfo=bdinfo)

        console.log(f"Filter by the torrent's BDInfo.. '{bdinfo.upper()}'")
        self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_uploader(self, username: str):
        tracker_data = self.get_by_uploader(username=username)
        console.log(f"Filter by the torrent uploader's username.. '{username.upper()}'")
        self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_start_year(self, startyear: str):
        tracker_data = self.get_by_start_year(startyear=startyear)
        console.log(
            f"StartYear torrents.. Return only torrents whose content was released"
            f" after or in the given year '{startyear.upper()}'"
        )
        self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_end_year(self, end_year: str):
        tracker_data = self.tracker.end_year(end_year=end_year)
        console.log(
            f"EndYear torrents.. Return only torrents whose content was released before or in the given year"
            f"'{end_year.upper()}'"
        )
        self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_mediainfo(self, mediainfo: str):
        tracker_data = self.get_by_mediainfo(mediainfo=mediainfo)
        console.log(
            f"Mediainfo torrents.. Filter by the torrent's mediaInfo.. '{mediainfo.upper()}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_types(self, type_name: str):
        tracker_data = self.get_by_types(type_name=config.tracker_values.type_id(type_name))
        console.log(
            f"Types torrents.. Filter by the torrent's type.. '{type_name.upper()}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_res(self, res_name: str):
        tracker_data = self.get_by_res(res_name=config.tracker_values.res_id(res_name))
        console.log(
            f"Resolutions torrents.. Filter by the torrent's resolution.. '{res_name.upper()}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_filename(self, file_name: str):
        tracker_data = self.get_by_filename(file_name=file_name)
        console.log(
            f"Filename torrents.. Filter by the torrent's filename.. '{file_name.upper()}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_tmdb_id(self, tmdb_id: int):
        tracker_data = self.get_by_tmdb_id(tmdb_id=tmdb_id)
        console.log(f"TMDB torrents.. Filter by the torrent's tmdb.. '{tmdb_id}'")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_imdb_id(self, imdb_id: int):
        tracker_data = self.get_by_imdb_id(imdb_id=imdb_id)
        console.log(f"IMDB torrents.. Filter by the torrent's imdb.. '{imdb_id}'")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_tvdb_id(self, tvdb_id: int):
        tracker_data = self.get_by_tvdb_id(tvdb_id=tvdb_id)
        console.log(f"TVDB torrents.. Filter by the torrent's tvdb.. '{tvdb_id}'")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_mal_id(self, mal_id: int):
        tracker_data = self.get_by_mal_id(mal_id=mal_id)
        console.log(f"MAL torrents.. Filter by the torrent's mal.. '{mal_id}'")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_playlist_id(self, playlist_id: int):
        tracker_data = self.get_by_playlist_id(playlist_id=playlist_id)
        console.log(
            f"Playlist torrents.. Return only torrents within the playlist of the given ID.. '{playlist_id}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_collection_id(self, collection_id: int):
        tracker_data = self.get_by_collection_id(collection_id=collection_id)
        console.log(
            f"Collection torrents.. Return only torrents within the collection of the given ID.. '{collection_id}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_freeleech(self, freeleech: int):
        tracker_data = self.get_by_freeleech(freeleech=freeleech)
        console.log(
            f"Freeleech torrents.. Filter by the torrent's freeleech discount (0-100).. '{freeleech}'"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_season(self, season: int):
        tracker_data = self.get_by_season(season=season)
        console.log(f"Seasons torrents.. Filter by the torrent's seasons.. '{season}'")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_by_episode(self, episode: int):
        tracker_data = self.get_by_episode(episode=episode)
        console.log(f"Episode torrents.. Filter by the torrent's episode.. '{episode}'")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_alive(self):
        tracker_data = self.get_alive()
        console.log(f"Alive torrents.. Filter by if the torrent has 1 or more seeders")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_dead(self):
        tracker_data = self.get_dead()
        console.log(f"Dead torrents.. Filter by if the torrent has 0 seeders")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_dying(self):
        tracker_data = self.get_dying()
        console.log(
            f"Dying torrents.. Filter by if the torrent has 1 seeder and has been downloaded more than 3 times"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_doubleup(self):
        tracker_data = self.get_doubleup()
        console.log(
            f"DoubleUp torrents.. Filter by if the torrent offers double upload"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_featured(self):
        tracker_data = self.get_featured()
        console.log(
            f"Featured torrents.. Filter by if the torrent is featured on the front page"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_refundable(self):
        tracker_data = self.get_refundable()
        console.log(f"Refundable torrents.. Filter by if the torrent is refundable")
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_stream(self):
        tracker_data = self.get_stream()
        console.log(
            f"Stream torrents.. Filter by if the torrent's content is stream-optimised"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_sd(self):
        tracker_data = self.get_sd()
        console.log(
            f"Standard torrents.. Filter by if the torrent's content is standard definition"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_highspeed(self):
        tracker_data = self.get_highspeed()
        console.log(
            f"Highspeed torrents.. Filter by if the torrent has seeders whose IP address has been registered"
            f" as a seedbox"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_internal(self):
        tracker_data = self.get_internal()
        console.log(
            f"Internal torrents.. Filter by if the torrent is an internal release"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)

    def view_personal(self):
        tracker_data = self.get_personal()
        console.log(
            f"Personal Release torrents.. Filter by if the torrent's content is created by the uploader"
        )
        if tracker_data:
            self.page_view(tracker_data=tracker_data, tracker=self.tracker)
