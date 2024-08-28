# -*- coding: utf-8 -*-
import pprint

# import cv2
import qbittorrent
import requests

from rich.console import Console
from qbittorrent import Client
from urllib.parse import urlparse
from unit3dup import pvtTracker
from common.external_services.imageHost import ImgBB, Freeimage, ImageUploaderFallback
from common.config import config

console = Console(log_path=False)

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
            console.log(f"[TMDB host]...... [Ok]", style="bold green")
        except requests.exceptions.HTTPError:
            if status_code == 401:
                console.log(
                    f"[TMDB ERR] '{status_code}' Check your API_KEY in service configuration file",
                    style="bold red",
                )
            return False
        return True

    def process_qbit(self) -> bool:

        # Qbittorent Test run process
        # Return if the url is invalid
        complete_url = f"{self.qbit_url}:{self.qbit_port}"
        result = self.url_check(complete_url)
        if not self.url_check(f"{self.qbit_url}:{self.qbit_port}"):
            console.log(
                f"[QBIT ERR] 'Url:{self.qbit_url}' 'port:{self.qbit_port}'. Check your 'Qbit config'",
                style="bold red",
            )
            return False

        try:
            qb = Client(f"{self.qbit_url}:{self.qbit_port}/")
            qb.login(username=self.qbit_user, password=self.qbit_pass)
            qb.torrents()
            console.log(f"[QBIT HOST]...... [Ok]", style="bold green")
        except requests.exceptions.HTTPError as http_err:
            console.log(http_err)
            return False
        except requests.exceptions.ConnectionError as http_err:
            console.log(
                f"[QBIT ERR] Connection Error. Check ip/port or run qbittorrent",
                style="bold red",
            )
            return False
        except qbittorrent.client.LoginRequired as http_err:
            console.log(
                f"[QBIT ERR] {http_err}. Check your username and password",
                style="bold red",
            )
            return False
        return True

    def process_tracker(self) -> bool:

        # Return if the url is invalid
        if not self.url_check(self.base_url):
            console.log(
                f"[TRACKER ERR] '{self.base_url}' Check your url",
                style="bold red",
            )
            return False

        tracker = pvtTracker.Unit3d(
            base_url=self.base_url, api_token=self.api_token, pass_key=""
        )
        test = tracker.get_alive(alive=True, perPage=1)
        if test:
            console.log(f"[TRACKER HOST]... [Ok]", style="bold green")
            return True
        return False

    """
    def process_imghost(self) -> bool:

        # Getting ready for testing image host
        img = cv2.imread(self.test_image)
        success, encoded_image = cv2.imencode(".png", img)
        if not success:
            raise Exception("Could not encode image")  # todo

        # List of host available uploaders
        uploaders = [
            ImgBB(encoded_image.tobytes(), self.imgbb_key),
            Freeimage(encoded_image.tobytes(), self.free_image_key),
        ]

        # Return true if at least one host is online
        at_least = False

        # For each host
        for uploader in uploaders:

            # Upload a small image
            fallback_uploader = ImageUploaderFallback(uploader)

            # If the host is not online add it to the list of offline uploaders
            if not fallback_uploader.upload(test=True):
                offline_uploaders.append(uploader.__class__.__name__)
            else:
                at_least = True

        return at_least
    """