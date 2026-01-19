# -*- coding: utf-8 -*-
import io
import time
import requests

from urllib.parse import urljoin
from view import custom_console
from common.trackers.data import trackers_api_data


class Myhttp:
    def __init__(self, tracker_name: str, pass_key=''):

        api_data = trackers_api_data[tracker_name.upper()] if tracker_name else None
        if not api_data:
            custom_console.bot_error_log(
                f"Tracker '{tracker_name}' not found. Please check your configuration or set it using the '-t' flag.")
            exit(1)

        self.pass_key = pass_key
        self.base_url = api_data['url']
        self.api_token = api_data['api_key']

        self.upload_url = urljoin(self.base_url, "api/torrents/upload")
        self.filter_url = urljoin(self.base_url, "api/torrents/filter?")
        self.fetch_url = urljoin(self.base_url, "api/torrents/")
        self.tracker_announce_url = urljoin(self.base_url, f"announce/{pass_key}")

        self.headers = {
            "User-Agent": "Unit3D-up/0.0 (Linux 5.10.0-23-amd64)",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        self.params = {}

        self.data = {
            "name": "TEST.torrent",
            "description": "",  # mandatory
            "mediainfo": "",
            "bdinfo": " ",
            "type_id": "1",
            "resolution_id": 10,  # mandatory
            "tmdb": "",  # mandatory
            "imdb": "0",
            "tvdb": "0",
            "mal": "0",  # no ancora implementato
            "igdb": "0",
            "anonymous": 0,
            "stream": "0",
            "sd": "0",
            "keywords": "",
            "personal_release": "0",
            "internal": 0,
            "featured": 0,
            "free": 0,
            "doubleup": 0,
            "sticky": 0,
        }


    def _post(self, files: str, data: dict, params: dict):
        pass

    def _get(self, params: str):
        pass


class Tracker(Myhttp):
    def _get(self, params: dict) -> requests:
        while True:
            try:
                response = requests.get(
                    url=self.filter_url, headers=self.headers, params=params, timeout=10
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    custom_console.bot_error_log(f"TRACKER HTTP Error {e.response.status_code} Rate limit (wait for 60 secs)...")
                    time.sleep(60)
                else:
                    custom_console.bot_error_log(
                        f"TRACKER HTTP Error {e.response.status_code}. Check your configuration file"
                        f" or verify if the tracker is online")
                    break

            except requests.exceptions.ConnectionError:
                custom_console.bot_error_log(
                    f"TRACKER Connection error. Please check your configuration data "
                    f"or verify if the tracker is online",
                )
                exit(1)
            except requests.exceptions.ReadTimeout as e:
                custom_console.bot_error_log(f"TRACKER HTTP Error {e}. Tracker Offline !")
                exit(1)

    def _post(self, file: dict, data: dict, params: dict):
            try:
                return requests.post(
                    url=self.upload_url,
                    files=file,
                    data=data,
                    headers=self.headers,
                    params=params,
                    timeout=10
                )
            except requests.exceptions.ReadTimeout as e:
                custom_console.bot_error_log(f"TRACKER HTTP Error {e}. Tracker Offline !")
                exit(1)


    def _fetch_all(self, params: dict) -> requests:
        return requests.get(
            url=self.fetch_url, headers=self.headers, params=params
        ).json()

    def _fetch_id(self, torrent_id: int) -> requests:
        return requests.get(
            url=f"{self.fetch_url}{torrent_id}",
            headers=self.headers,
            params=self.params,
        )

    def _next_page(self, url: str) -> requests:
        try:
            response = requests.get(url=url, headers=self.headers, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            custom_console.bot_error_log(f"Report {http_err}")
            exit(1)


class filterAPI(Tracker):
    def tmdb(self, tmdb_id: int, perPage: int = None) -> requests:
        self.params["tmdbId"] = tmdb_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def imdb(self, imdb_id: int, perPage: int = None) -> requests:
        self.params["imdbId"] = imdb_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def igdb(self, igdb_id: int, perPage: int = None) -> requests:
        """
        self.params["igdbId"] = igdb_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)
        """
        print("The tracker has not implemented it yet")
        exit()

    def tvdb(self, tvdb_id: int, perPage: int = None) -> requests:
        self.params["tvdbId"] = tvdb_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def mal(self, mal_id: int, perPage: int = None) -> requests:
        self.params["malId"] = mal_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def playlist_id(self, playlistId: int, perPage: int = None) -> requests:
        self.params["playlistId"] = playlistId
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def collection_id(self, collectionId: int, perPage: int = None) -> requests:
        self.params["collectionId"] = collectionId
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def freeleech(self, freeleech: int, perPage: int = None) -> requests:
        self.params["free"] = freeleech
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def name(self, name: str, perPage: int = None) -> requests:
        self.params["name"] = name
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def description(self, description: str, perPage: int = None) -> requests:
        self.params["description"] = description
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def mediainfo(self, mediainfo: str, perPage: int = None) -> requests:
        self.params["mediainfo"] = mediainfo
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def bdinfo(self, bdinfo: str, perPage: int = None) -> requests:
        self.params["bdinfo"] = bdinfo
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def start_year(self, start_year: str, perPage: int = None) -> requests:
        self.params["startYear"] = start_year
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def end_year(self, end_year: str, perPage: int = None) -> requests:
        self.params["endYear"] = end_year
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def uploader(self, uploader: str, perPage: int = None) -> requests:
        self.params["uploader"] = uploader
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def alive(self, alive: bool, perPage: int = None) -> requests:
        self.params["alive"] = alive
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def dying(self, dying: bool, perPage: int = None) -> requests:
        self.params["dying"] = dying
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def dead(self, dead: bool, perPage: int = None) -> requests:
        self.params["dead"] = dead
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def file_name(self, file_name: str, perPage: int = None) -> requests:
        self.params["file_name"] = file_name
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def seasonNumber(self, seasonNumber: int, perPage: int = None) -> requests:
        self.params["seasonNumber"] = seasonNumber
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def episodeNumber(self, episodeNumber: int, perPage: int = None) -> requests:
        self.params["episodeNumber"] = episodeNumber
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def types(self, type_id: str, perPage: int = None) -> requests:
        self.params["types[]"] = type_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def resolution(self, res_id: str, perPage: int = None) -> requests:
        self.params["resolutions[]"] = res_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def doubleup(self, double_up: bool, perPage: int = None) -> requests:
        self.params["doubleup"] = double_up
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def featured(self, featured: bool, perPage: int = None) -> requests:
        self.params["featured"] = featured
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def refundable(self, refundable: bool, perPage: int = None) -> requests:
        self.params["refundable"] = refundable
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def stream(self, stream: bool, perPage: int = None) -> requests:
        self.params["stream"] = stream
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def sd(self, sd: bool, perPage: int = None) -> requests:
        self.params["sd"] = sd
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def highspeed(self, high_speed: bool, perPage: int = None) -> requests:
        self.params["highspeed"] = high_speed
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def internal(self, internal: bool, perPage: int = None) -> requests:
        self.params["internal"] = internal
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def personal_release(self, personalRelease: bool, perPage: int = None) -> requests:
        self.params["personalRelease"] = personalRelease
        self.params["perPage"] = perPage
        return self._get(params=self.params)

    def next(self, url: str) -> requests:
        return self._next_page(url=url)


    # Filter "Combo"
    def tmdb_res(self, tmdb_id: int, res_id: str, perPage: int = None) -> requests:
        self.params["tmdbId"] = tmdb_id
        self.params["resolutions[]"] = res_id
        self.params["perPage"] = perPage
        return self._get(params=self.params)



class Torrents(Tracker):
    def torrents(self, perPage: int = None) -> requests:
        self.params["perPage"] = perPage
        return self._fetch_all(params=self.params)

    def torrent(self, torrent_id: int) -> requests:
        return self._fetch_id(torrent_id)


class Uploader(Tracker):
    def upload_t(self, data: dict, torrent_archive_path: str, nfo_path=None) -> requests.Response:
        files = {}
        # Binary mode
        with open(torrent_archive_path, 'rb') as torrent_file:
            files['torrent'] = ('upload.torrent', torrent_file, 'application/x-bittorrent')

            # Add the info file
            if nfo_path:
                with open(nfo_path, 'rb') as nfo_file:
                    files['nfo'] = ('file.nfo', nfo_file, 'text/plain')
                    # Post both
                    response = self._post(file=files, data=data, params=self.params)
            else:
                # Post the torrent
                response = self._post(file=files, data=data, params=self.params)

        return response


    @staticmethod
    def encode_utf8(file_path:str) -> bytes | io.BytesIO:
        """
        Try to decode the nfo file
        """
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'latin1']
        decoded_content = None

        # Trey to open and decode
        with open(file_path, 'rb') as f:
            raw_data = f.read()

        for encoding in encodings:
            try:
                decoded_content = raw_data.decode(encoding)
                break # OK
            except (UnicodeDecodeError, TypeError):
                continue # try next

        # Success. Return the contents in bytes
        if decoded_content is not None:
            return decoded_content.encode('utf-8')
        else:
            error_message = "Error: Unable to read the NFO file !"
            # Prepare a message of type File to post to the tracker
            return io.BytesIO(error_message.encode('utf-8'))



class Unit3d(filterAPI, Torrents, Uploader):
    def get_tmdb(self, tmdb_id: int, perPage: int = None) -> requests:
        return self.tmdb(tmdb_id=tmdb_id, perPage=perPage)

    def get_tvdb(self, tvdb_id: int, perPage: int = None) -> requests:
        return self.tvdb(tvdb_id=tvdb_id, perPage=perPage)

    def get_imdb(self, imdb_id: int, perPage: int = None) -> requests:
        return self.imdb(imdb_id=imdb_id, perPage=perPage)

    def get_igdb(self, igdb_id: int, perPage: int = None) -> requests:
        return self.igdb(igdb_id=igdb_id, perPage=perPage)

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


    # Filter "Combo"
    def get_tmdb_res(self, tmdb_id: int, res_id: str, perPage: int = None) -> requests:
        if tmdb_id and res_id:
            return self.tmdb_res(tmdb_id=tmdb_id, res_id=res_id, perPage=perPage)
        return None