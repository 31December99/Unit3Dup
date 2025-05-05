# -*- coding: utf-8 -*-
import time
import requests

from urllib.parse import urljoin
from view import custom_console
from common.trackers.data import trackers_api_data


class Myhttp:
    def __init__(self, tracker_name: str, pass_key=''):

        # Load the tracker data
        api_data = trackers_api_data.get(tracker_name.upper())
        if not api_data:
            custom_console.bot_error_log(
                f"Tracker '{tracker_name}' not found. Please check your configuration or set it using the '-t' flag.")
            raise TrackerAPIError("Invalid tracker name")

        # Load the baseurl
        self.base_url = api_data['url']

        # Load the api_key
        self.api_token = api_data['api_key']

        # Build the endpoints
        # // UPLOAD
        self.upload_url = urljoin(self.base_url, "api/torrents/upload")
        # // Filter
        self.filter_url = urljoin(self.base_url, "api/torrents/filter?")
        # // TORRENT
        self.fetch_url = urljoin(self.base_url, "api/torrents/")
        # // ANNOUNCE
        self.tracker_announce_url = urljoin(self.base_url, f"announce/{pass_key}")

        # Create the Agent...
        self.headers = {
            "User-Agent": "Unit3D-up/0.0 (Linux 5.10.0-23-amd64)",
            "Accept": "application/json",
        }

        # Params gets the token
        self.params = {
            "api_token": self.api_token,
        }

        # Initialize the Payload
        self.default_data = {
            "name": "TEST.torrent",
            "description": "",    # mandatory
            "mediainfo": "",
            "bdinfo": " ",
            "type_id": "1",
            "resolution_id": 10,  # mandatory
            "tmdb": "",           # mandatory
            "imdb": "0",
            "tvdb": "0",
            "mal": "0",
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

        # Create a new session and keep it up
        self.session = requests.Session()
        # Add the header to new http session
        self.session.headers.update(self.headers)
        # The default params
        self.default_params = {"api_token": self.api_token}


class Tracker(Myhttp):
    def _get(self, extra_params: dict) -> dict:
        params = self.default_params.copy()
        params.update(extra_params)

        while True:
            try:
                response = self.session.get(self.filter_url, params=params, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code
                if status == 429:
                    custom_console.bot_error_log("Rate limit hit. Waiting 60 seconds...")
                    time.sleep(60)
                else:
                    custom_console.bot_error_log(f"HTTP Error {status}")
                    raise TrackerAPIError(f"HTTP Error {status}") from e
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                custom_console.bot_error_log("Tracker connection error or timeout.")
                raise TrackerAPIError("Tracker offline") from e

    def _post(self, file: dict, extra_data: dict, extra_params: dict):

        # Create a copy of the default data to initialize it on the next call
        # prima chiamava e usciva dal programma
        data = self.default_data.copy()
        data.update(extra_data)
        params = self.default_params.copy()
        params.update(extra_params)

        # Open the torrent file
        with open(file['torrent'], "rb") as torrent:
            # Fill the attribute
            files = {"torrent": ("filename.torrent", torrent, "application/octet-stream")}
            # Add the .NFO file if it exists
            if file.get("nfo"):
                files["nfo"] = ("filename.nfo", file["nfo"], "text/plain")

            try:
                # // UP
                response = self.session.post(
                    self.upload_url,
                    files=files,
                    data=data,
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                return response
            except requests.exceptions.ReadTimeout as e:
                custom_console.bot_error_log(f"Timeout: {e}")
                raise TrackerAPIError("Upload timeout") from e


class Uploader(Tracker):
    def upload_t(self, data: dict, torrent_archive_path: str, nfo_path=None) -> requests:
        file_torrent = {"torrent": torrent_archive_path}
        if nfo_path:
            file_torrent.update({"nfo": self.encode_utf8(file_path=nfo_path)})
        return self._post(file=file_torrent, extra_data=data, extra_params=self.params)

    @staticmethod
    def encode_utf8(file_path: str) -> str:
        encodings = ['utf-8', 'iso-8859-1', 'windows-1252', 'latin1']
        with open(file_path, 'rb') as f:
            raw_data = f.read()

        for encoding in encodings:
            try:
                return raw_data.decode(encoding)
            except (UnicodeDecodeError, TypeError):
                continue

        return "Error: Unable to read the NFO file!"


class FilterAPI(Tracker):
    def filter_by(self, **filters) -> dict:
        if "perPage" not in filters:
            filters["perPage"] = 100
        return self._get(filters)


class Unit3d(FilterAPI, Uploader):
    pass


class TrackerAPIError(Exception):
    pass
