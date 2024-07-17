# -*- coding: utf-8 -*-
import sys
import requests
from rich.console import Console

console = Console(log_path=False)


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
            "Accept": "application/json",
        }
        self.params = {
            "api_token": self.api_token,
        }

        self.data = {
            "name": "TEST.torrent",
            "description": "",  # mandatory
            "mediainfo": "",
            "bdinfo": " ",
            "type_id": "1",
            "resolution_id": 10,  # mandatory
            "tmdb": "",  # mandatory
            "imdb": "0",  # no ancora implementato
            "tvdb": "0",  # no ancora implementato
            "mal": "0",  # no ancora implementato
            "igdb": "0",  # no ancora implementato
            "anonymous": "0",
            "stream": "0",
            "sd": "0",
            "keywords": "",
            "personal_release": "0",
            "internal": 0,
            "featured": 0,
            "free": 0,
            "doubleup": 0,
            "sticky": 0
        }

    def _post(self, files: str, data: dict, params: dict):
        pass

    def _get(self, params: str):
        pass


class Tracker(Myhttp):

    def _get(self, params: dict) -> requests:
        try:
            response = requests.get(url=self.filter_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            console.print(f"Report {http_err}")
            sys.exit()

    def _post(self, file: dict, data: dict, params: dict):
        return requests.post(url=self.upload_url, files=file, data=data, headers=self.headers, params=params)

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

    def playlist_id(self, playlistId: int, perPage: int = None) -> requests:
        self.params['playlistId'] = playlistId
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def collection_id(self, collectionId: int, perPage: int = None) -> requests:
        self.params['collectionId'] = collectionId
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def freeleech(self, freeleech: int, perPage: int = None) -> requests:
        self.params['free'] = freeleech
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

    def bdinfo(self, bdinfo: str, perPage: int = None) -> requests:
        self.params['bdinfo'] = bdinfo
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def start_year(self, start_year: str, perPage: int = None) -> requests:
        self.params['startYear'] = start_year
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def end_year(self, end_year: str, perPage: int = None) -> requests:
        self.params['endYear'] = end_year
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

    def seasonNumber(self, seasonNumber: int, perPage: int = None) -> requests:
        self.params['seasonNumber'] = seasonNumber
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def episodeNumber(self, episodeNumber: int, perPage: int = None) -> requests:
        self.params['episodeNumber'] = episodeNumber
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def types(self, type_id: str, perPage: int = None) -> requests:
        self.params['types[]'] = type_id
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def resolution(self, res_id: str, perPage: int = None) -> requests:
        self.params['resolutions[]'] = res_id
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def doubleup(self, double_up: bool, perPage: int = None) -> requests:
        self.params['doubleup'] = double_up
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def featured(self, featured: bool, perPage: int = None) -> requests:
        self.params['featured'] = featured
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def refundable(self, refundable: bool, perPage: int = None) -> requests:
        self.params['refundable'] = refundable
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def stream(self, stream: bool, perPage: int = None) -> requests:
        self.params['stream'] = stream
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def sd(self, sd: bool, perPage: int = None) -> requests:
        self.params['sd'] = sd
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def highspeed(self, high_speed: bool, perPage: int = None) -> requests:
        self.params['highspeed'] = high_speed
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def internal(self, internal: bool, perPage: int = None) -> requests:
        self.params['internal'] = internal
        self.params['perPage'] = perPage
        return self._get(params=self.params)

    def personal_release(self, personalRelease: bool, perPage: int = None) -> requests:
        self.params['personalRelease'] = personalRelease
        self.params['perPage'] = perPage
        return self._get(params=self.params)


class Torrents(Tracker):
    def torrents(self, perPage: int = None) -> requests:
        self.params['perPage'] = perPage
        return self._fetch_all(params=self.params)

    def torrent(self, torrent_id: int) -> requests:
        return self._fetch_id(torrent_id)


class Uploader(Tracker):
    def upload_t(self, data: dict, file_name: str) -> requests:
        with open(f'{file_name}.torrent', 'rb') as torrent:
            file_torrent = {'torrent': torrent}
            return self._post(file=file_torrent, data=data, params=self.params)


class Unit3d(filterAPI, Torrents, Uploader):
    def get_tmdb(self, tmdb_id: int, perPage: int = None) -> requests:
        return self.tmdb(tmdb_id=tmdb_id, perPage=perPage)

    def get_tvdb(self, tvdb_id: int, perPage: int = None) -> requests:
        return self.tvdb(tvdb_id=tvdb_id, perPage=perPage)

    def get_imdb(self, imdb_id: int, perPage: int = None) -> requests:
        return self.imdb(imdb_id=imdb_id, perPage=perPage)

    def get_mal(self, mal_id: int, perPage: int = None) -> requests:
        return self.mal(mal_id=mal_id, perPage=perPage)

    def get_playlist_id(self, playlist_id: int, perPage: int = None) -> requests:
        return self.playlist_id(playlistId=playlist_id, perPage=perPage)

    def get_collection_id(self, collection_id: int, perPage: int = None) -> requests:
        return self.collection_id(collectionId=collection_id, perPage=perPage)

    def get_freeleech(self, freeleech: int, perPage: int = None) -> requests:
        return self.freeleech(freeleech=freeleech, perPage=perPage)

    def get_name(self, name: str, perPage: int = None) -> requests:
        return self.name(name=name, perPage=perPage)

    def get_description(self, description: str, perPage: int = None) -> requests:
        return self.description(description=description, perPage=perPage)

    def get_bdinfo(self, bdinfo: str, perPage: int = None) -> requests:
        return self.bdinfo(bdinfo=bdinfo, perPage=perPage)

    def get_mediainfo(self, mediainfo: str, perPage: int = None) -> requests:
        return self.mediainfo(mediainfo=mediainfo, perPage=perPage)

    def get_uploader(self, uploader: str, perPage: int = None) -> requests:
        return self.uploader(uploader=uploader, perPage=perPage)

    def after_start_year(self, start_year: str, perPage: int = None) -> requests:
        return self.start_year(start_year=start_year, perPage=perPage)

    def before_end_year(self, end_year: str, perPage: int = None) -> requests:
        return self.end_year(end_year=end_year, perPage=perPage)

    def get_alive(self, alive: bool, perPage: int = None) -> requests:
        return self.alive(alive=alive, perPage=perPage)

    def get_dying(self, dying: bool, perPage: int = None) -> requests:
        return self.dying(dying=dying, perPage=perPage)

    def get_dead(self, dead: bool, perPage: int = None) -> requests:
        return self.dead(dead=dead, perPage=perPage)

    def get_filename(self, file_name: str, perPage: int = None) -> requests:
        return self.file_name(file_name=file_name, perPage=perPage)

    def get_season_number(self, se_number: int, perPage: int = None) -> requests:
        return self.seasonNumber(seasonNumber=se_number, perPage=perPage)

    def get_episode_number(self, ep_number: int, perPage: int = None) -> requests:
        return self.episodeNumber(episodeNumber=ep_number, perPage=perPage)

    def get_types(self, type_id: str, perPage: int = None) -> requests:
        if type_id:
            return self.types(type_id=type_id, perPage=perPage)

    def get_res(self, res_id: str, perPage: int = None) -> requests:
        if res_id:
            return self.resolution(res_id=res_id, perPage=perPage)

    def fetch_all(self, perPage: int = None) -> requests:
        return self.torrents(perPage=perPage)

    def fetch_id(self, torrent_id: int) -> requests:
        return self.torrent(torrent_id=torrent_id)

    def get_double_up(self, double_up: bool, perPage: int = None):
        return self.doubleup(double_up=double_up, perPage=perPage)

    def get_featured(self, featured: bool, perPage: int = None):
        return self.featured(featured=featured, perPage=perPage)

    def get_refundable(self, refundable: bool, perPage: int = None):
        return self.refundable(refundable=refundable, perPage=perPage)

    def get_stream(self, stream: bool, perPage: int = None):
        return self.stream(stream=stream, perPage=perPage)

    def get_sd(self, sd: bool, perPage: int = None):
        return self.sd(sd=sd, perPage=perPage)

    def get_highspeed(self, highspeed: bool, perPage: int = None):
        return self.highspeed(high_speed=highspeed, perPage=perPage)

    def get_internal(self, internal: bool, perPage: int = None):
        return self.internal(internal=internal, perPage=perPage)

    def get_personal_release(self, personalRelease: bool, perPage: int = None):
        return self.personal_release(personalRelease=personalRelease, perPage=perPage)
