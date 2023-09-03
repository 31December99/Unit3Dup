#!/usr/bin/env python3.9
from datetime import datetime
import requests


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Utility:

    @staticmethod
    def console(message: str, level: int):
        now = datetime.now()
        date_now = datetime.today().strftime('%d-%m-%Y')
        time_now = now.strftime("%H:%M:%S")
        if level == 1:
            print(f"<{date_now} {time_now}>{bcolors.FAIL}{message}{bcolors.ENDC}")
        if level == 2:
            print(f"<{date_now} {time_now}>{bcolors.OKGREEN}{message}{bcolors.ENDC}")
        if level == 3:
            print(f"<{date_now} {time_now}>{bcolors.WARNING}{message}{bcolors.ENDC}")


class Myhttp:

    def __init__(self, base_url: str, api_token: str, pass_key: str):
        self.base_url = base_url
        self.api_token = api_token
        self.pass_key = pass_key

        self.upload_url = f"{self.base_url}api/torrents/upload"
        self.filter_url = f"{self.base_url}api/torrents/filter?"
        self.fetch_url = f"{self.base_url}api/torrents/"
        self.tracker_announce_url = f"{self.base_url}announce/{pass_key}"

        self.headers = {
            "User-Agent": "Test/0.0 (Linux 5.10.0-23-amd64)",
            # "Content-Type": "application/json",
        }
        self.params = {
            "api_token": self.api_token,
        }

        self.data = {
            "name": "TEST.torrent",
            "description": "",  # mandatory
            "mediainfo": "",
            "bdinfo": " ",
            "type_id": "1",  # web_dl etcc
            "resolution_id": "3",  # mandatory todo: implementare
            "tmdb": "",  # mandatory
            "imdb": "0",  # no ancora implementato
            "tvdb": "0",  # no ancora implementato
            "mal": "0",  # no ancora implementato
            "igdb": "0",  # no ancora implementato
            "anonymous": "0",
            "stream": "1",  # no ancora implementato
            "sd": "0",
            "keywords": "",
            "personal_release": "0",  # no ancora implementato
            "internal": 0,  # no ancora implementato
            "featured": 0,  # no ancora implementato
            "free": 0,
            "doubleup": 0,  # no ancora implementato
            "sticky": 0  # no ancora implementato
        }

    def _post(self, files: str, data: dict, params: dict):
        pass

    def _get(self, params: str):
        pass


class Tracker(Myhttp):

    def _get(self, params: dict) -> requests:
        return requests.get(url=self.filter_url, headers=self.headers, params=params).json()

    def _post(self, file: dict, data: dict, params: dict):
        return requests.post(url=self.upload_url, files=file, data=data, headers=self.headers, params=params).json()

    def _fetch_all(self, params: dict) -> requests:
        return requests.get(url=self.fetch_url, headers=self.headers, params=params).json()

    def _fetch_id(self, torrent_id: int) -> requests:
        return requests.get(url=f"{self.fetch_url}{torrent_id}", headers=self.headers, params=self.params)


class filterAPI(Tracker):
    def tmdb(self, tmdb_id: int, perPage: int = None) -> requests:
        self.params['tmdbId'] = tmdb_id
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def imdb(self, imdb_id: int, perPage: int = None) -> requests:
        self.params['imdbId'] = imdb_id
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def tvdb(self, tvdb_id: int, perPage: int = None) -> requests:
        self.params['tvdbId'] = tvdb_id
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def mal(self, mal_id: int, perPage: int = None) -> requests:
        self.params['malId'] = mal_id
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def name(self, name: str, perPage: int = None) -> requests:
        self.params['name'] = name
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def description(self, description: str, perPage: int = None) -> requests:
        self.params['description'] = description
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def mediainfo(self, mediainfo: str, perPage: int = None) -> requests:
        self.params['mediainfo'] = mediainfo
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def uploader(self, uploader: str, perPage: int = None) -> requests:
        self.params['uploader'] = uploader
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def alive(self, alive: bool, perPage: int = None) -> requests:
        self.params['alive'] = alive
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def dying(self, dying: bool, perPage: int = None) -> requests:
        self.params['dying'] = dying
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def dead(self, dead: bool, perPage: int = None) -> requests:
        self.params['dead'] = dead
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def file_name(self, file_name: str, perPage: int = None) -> requests:
        self.params['file_name'] = file_name
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def seasonNumber(self, seasonNumber: str, perPage: int = None) -> requests:
        self.params['seasonNumber'] = seasonNumber
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def episodeNumber(self, episodeNumber: int, perPage: int = None) -> requests:
        self.params['episodeNumber'] = episodeNumber
        self.params['perPage'] = perPage
        return self._get(params=self.params)


class Torrents(Tracker):
    def torrents(self, perPage: int = None) -> requests:
        self.params['perPage'] = perPage
        return self._fetch_all(params=self.params)

    def torrent(self, torrent_id: int) -> requests:
        return self._fetch_id(torrent_id)


class Uploader(Tracker):
    def upload_t(self, data: dict, file_name: str, video_id: int = None) -> requests:
        self.data['tmdb'] = video_id
        with open(f'{file_name}.torrent', 'rb') as torrent:
            file_torrent = {'torrent': torrent}
            return self._post(file=file_torrent, data=data, params=self.params)


class ITT(filterAPI, Torrents, Uploader):
    def get_tmdb(self, tmdb_id: int, perPage: int = None) -> requests:
        return self.tmdb(tmdb_id=tmdb_id, perPage=perPage)

    def get_tvdb(self, tvdb_id: int, perPage: int = None) -> requests:
        return self.tvdb(tvdb_id=tvdb_id, perPage=perPage)

    def get_imdb(self, imdb_id: int, perPage: int = None) -> requests:
        return self.imdb(imdb_id=imdb_id, perPage=perPage)

    def get_mal(self, mal_id: int, perPage: int = None) -> requests:
        return self.mal(mal_id=mal_id, perPage=perPage)

    def get_name(self, name: str, perPage: int = None) -> requests:
        return self.name(name=name, perPage=perPage)

    def get_description(self, description: str, perPage: int = None) -> requests:
        return self.description(description=description, perPage=perPage)

    def get_mediainfo(self, mediainfo: str, perPage: int = None) -> requests:
        return self.mediainfo(mediainfo=mediainfo, perPage=perPage)

    def get_uploader(self, uploader: str, perPage: int = None) -> requests:
        return self.uploader(uploader=uploader, perPage=perPage)

    def get_alive(self, alive: bool, perPage: int = None) -> requests:
        return self.alive(alive=alive, perPage=perPage)

    def get_dying(self, dying: bool, perPage: int = None) -> requests:
        return self.dying(dying=dying, perPage=perPage)

    def get_dead(self, dead: bool, perPage: int = None) -> requests:
        return self.dead(dead=dead, perPage=perPage)

    def get_filename(self, file_name: str, perPage: int = None) -> requests:
        return self.file_name(file_name=file_name, perPage=perPage)

    def get_seasonNumber(self, file_name: str, perPage: int = None) -> requests:
        return self.file_name(file_name=file_name, perPage=perPage)

    def get_episodeNumber(self, episodeNumber: int, perPage: int = None) -> requests:
        return self.episodeNumber(episodeNumber=episodeNumber, perPage=perPage)

    def fetch_all(self, perPage: int = None) -> requests:
        return self.torrents(perPage=perPage)

    def fetch_id(self, torrent_id: int) -> requests:
        return self.torrent(torrent_id=torrent_id)
