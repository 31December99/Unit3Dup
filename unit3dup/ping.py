# -*- coding: utf-8 -*-

import qbittorrent
import requests

from qbittorrent import Client
from urllib.parse import urlparse
from unit3dup import pvtTracker
from common.config import config
from common.custom_console import custom_console

offline_uploaders = []

class Ping:
    test_image = "unit3dup/test_image.png"

    def __init__(self):

        # Getting ready for testing Image Host
        self.imgbb_key = config.IMGBB_KEY
        self.free_image_key = config.FREE_IMAGE_KEY

        # Getting ready for testing Tracker
        self.api_token = config.API_TOKEN
        self.base_url = config.BASE_URL

        # Getting ready for testing qbittorrent
        self.qbit_user = config.QBIT_USER
        self.qbit_pass = config.QBIT_PASS
        self.qbit_url = config.QBIT_URL
        self.qbit_port = config.QBIT_PORT

        # Getting ready for testing TMDB
        self.tmdb_apikey = config.TMDB_APIKEY

    def is_ip(self, ip_address) -> bool:
        """
        false if it's not an ip address

        """
        parts = ip_address.split(".")
        # Each part must be(and) a digit and between 0 and 255
        return len(parts) == 4 and all(
            part.isdigit() and 0 <= int(part) <= 255 for part in parts
        )

    def url_check(self, url: str):
        """
        Search for scheme (https) and netloc (domain)
        """
        valid = {"http", "https"}
        try:
            check = urlparse(url)
            if check.port:
                str(check.port).isdigit()
            return all([check.scheme, check.netloc != "", check.scheme in valid])
        except AttributeError as e:
            # Return False if input is not a string or valid URI
            return False
        except ValueError as e:
            # Return False if Port is not an integer
            return False

    def process_tmdb(self) -> bool:

        # Getting ready for testing tmdb
        base_url = "https://api.themoviedb.org/3"
        endpoint = "/movie/popular"
        tmdb_api_url = f"{base_url}{endpoint}?api_key={self.tmdb_apikey}"

        # TMDB test
        status_code = ""
        try:
            response = requests.get(tmdb_api_url)
            status_code = response.status_code
            response.raise_for_status()
            custom_console.bot_log("[TMDB host]...... [Ok]")

        except requests.exceptions.HTTPError:
            if status_code == 401:
                custom_console.bot_error_log(
                    f"[TMDB ERR] '{status_code}' Check your API_KEY in service configuration file")
            return False
        return True

    def process_qbit(self) -> bool:

        # Qbittorent Test run process
        # Return if the url is invalid
        complete_url = f"{self.qbit_url}:{self.qbit_port}"
        result = self.url_check(complete_url)
        if not self.url_check(f"{self.qbit_url}:{self.qbit_port}"):
            custom_console.bot_error_log(
                f"[QBIT ERR] 'Url:{self.qbit_url}' 'port:{self.qbit_port}'. Check your 'Qbit config'")
            return False

        try:
            qb = Client(f"{self.qbit_url}:{self.qbit_port}/")
            qb.login(username=self.qbit_user, password=self.qbit_pass)
            qb.torrents()
            custom_console.bot_log(f"[QBIT HOST]...... [Ok]")
        except requests.exceptions.HTTPError as http_err:
            custom_console.bot_error_log(
                f"[QBIT ERR] {http_err}. Http Error. Check ip/port or run qbittorrent")
            return False
        except requests.exceptions.ConnectionError as http_err:
            custom_console.bot_error_log(
                f"[QBIT ERR] {http_err}. Connection Error. Check ip/port or run qbittorrent")
            return False
        except qbittorrent.client.LoginRequired as http_err:
            custom_console.bot_error_log(
                f"[QBIT ERR] {http_err}. Check your username and password")
            return False
        return True

    def process_tracker(self) -> bool:

        # Return if the url is invalid
        if not self.url_check(self.base_url):
            custom_console.bot_error_log(
                f"[TRACKER ERR] '{self.base_url}' Check your url")
            return False

        tracker = pvtTracker.Unit3d(
            base_url=self.base_url, api_token=self.api_token, pass_key=""
        )
        test = tracker.get_alive(alive=True, perPage=1)
        if test:
            custom_console.bot_log(f"[TRACKER HOST]... [Ok]")
            return True
        return False
