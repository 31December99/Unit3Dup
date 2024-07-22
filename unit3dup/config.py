import os
import sys
import cv2
import qbittorrent
import requests

from decouple import Config, RepositoryEnv
from rich.console import Console
from rich.text import Text
from unit3dup.imageHost import ImgBB
from qbittorrent import Client
from unit3dup import pvtTracker
from urllib.parse import urlparse


console = Console(log_path=False)


class ConfigUnit3D:
    # Little image for testing upload
    test_image = "unit3dup/test_image.png"

    def __init__(self, tracker_env_name: str, service_env_name: str):

        # Get the current folder
        self.current_folder = os.path.dirname(__file__)

        # Get the current project folder
        self.root_folder = os.path.abspath(os.path.join(self.current_folder, ".."))

        # Build the complete tracker path
        self.tracker_path = os.path.join(self.root_folder, tracker_env_name)

        # Build the complete service path
        self.service_path = os.path.join(self.root_folder, service_env_name)

        # Load configs
        self.config_tracker = Config(RepositoryEnv(self.tracker_path))
        self.config_service = Config(RepositoryEnv(self.service_path))

    @staticmethod
    def is_ip(ip_address) -> bool:
        """
        false if it's not an ip address

        """
        parts = ip_address.split('.')
        # Each part must be(and) a digit and between 0 and 255
        return (len(parts) == 4 and
                all(part.isdigit() and 0 <= int(part) <= 255 for part in parts))

    @staticmethod
    def url_check(url: str):
        """
        Search for scheme (https) and netloc (domain)
        """
        valid = {"http", "https"}
        try:
            check = urlparse(url)
            if check.port:
                str(check.port).isdigit()
            return all([check.scheme, check.netloc != '', check.scheme in valid])
        except AttributeError as e:
            # Return False if input is not a string or valid URI
            return False
        except ValueError as e:
            # Return False if Port is not an integer
            return False

    @classmethod
    def process_tmdb(cls, service_path: str) -> bool:

        # Verified path
        service_config = Config(RepositoryEnv(service_path))

        # Getting ready for testing tmdb
        tmdb_apikey = service_config("TMDB_APIKEY")
        base_url = "https://api.themoviedb.org/3"
        endpoint = "/movie/popular"
        tmdb_api_url = f"{base_url}{endpoint}?api_key={tmdb_apikey}"

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
                    f"[TMDB ERR] '{status_code}' Check your API_KEY in {service_path}",
                    style="bold red",
                )
            return False
        return True

    @classmethod
    def process_qbit(cls, service_path: str) -> bool:

        # Verified path
        service_config = Config(RepositoryEnv(service_path))

        # Getting ready for testing qbit
        qbit_user = service_config("QBIT_USER")
        qbit_pass = service_config("QBIT_PASS")
        qbit_url = service_config("QBIT_URL")
        qbit_port = service_config("QBIT_PORT")

        # Qbittorent Test run process
        # Return if the url is invalid
        complete_url = f"{qbit_url}:{qbit_port}"
        result = ConfigUnit3D.url_check(complete_url)
        if not ConfigUnit3D.url_check(f"{qbit_url}:{qbit_port}"):
            console.log(
                f"[QBIT ERR] 'Url:{qbit_url}' 'port:{qbit_port}'. Check your 'Qbit config'",
                style="bold red",
            )
            return False


        try:
            qb = Client(f"{qbit_url}:{qbit_port}/")
            qb.login(username=qbit_user, password=qbit_pass)
            qb.torrents()
            console.log(f"[QBIT HOST]...... [Ok]", style="bold green")
        except requests.exceptions.HTTPError as http_err:
            console.log(http_err)
            return False
        except requests.exceptions.ConnectionError as http_err:
            console.log(f"[QBIT ERR] {http_err}", style="bold red")
            return False
        except qbittorrent.client.LoginRequired as http_err:
            console.log(
                f"[QBIT ERR] {http_err}. Check your username and password",
                style="bold red",
            )
            return False
        return True

    @classmethod
    def process_tracker(cls, tracker_path: str) -> bool:
        # Verified path
        tracker_config = Config(RepositoryEnv(tracker_path))

        # Getting ready for testing tracker
        # pass_key = tracker_config("PASS_KEY")
        api_token = tracker_config("API_TOKEN")
        base_url = tracker_config("BASE_URL")

        # Return if the url is invalid
        if not ConfigUnit3D.url_check(base_url):
            console.log(
                f"[TRACKER ERR] '{base_url}' Check your url",
                style="bold red",
            )
            return False

        tracker = pvtTracker.Unit3d(base_url=base_url, api_token=api_token, pass_key="")
        test = tracker.get_alive(alive=True, perPage=1)
        if test:
            console.log(f"[TRACKER HOST]... [Ok]", style="bold green")
            return True
        return False

    @classmethod
    def process_imghost(cls) -> bool:

        # Getting readyfor testing image host
        img = cv2.imread(ConfigUnit3D.test_image)
        success, encoded_image = cv2.imencode(".png", img)
        if not success:
            raise Exception("Could not encode image")  # todo

        # ImageBB Test
        # To test the ImageBB API, uploading an image is the only available method?
        test_img_host = ImgBB(encoded_image.tobytes())
        test = test_img_host.upload["data"]["display_url"]
        if test:
            console.log("[Image host]..... [Ok]", style="bold green")
        else:
            return False
        return True

    @classmethod
    def process(cls, service_path: str, tracker_path: str) -> bool:

        console.rule("\nChecking configuration files")
        track_err = cls.process_tracker(tracker_path=tracker_path)
        qbit_err = cls.process_qbit(service_path=service_path)
        tmdb_err = cls.process_tmdb(service_path=service_path)
        imghost_err = cls.process_imghost()
        if tmdb_err and qbit_err and imghost_err and track_err:
            return True
        return False

    @classmethod
    def validate(cls, tracker_env_name: str, service_env_name: str):

        # Flags for os file
        tracker_not_found: bool = False
        service_not_found: bool = False

        # Build an error message string
        message = Text("Configuration file ")

        # Get the current folder
        current_folder = os.path.dirname(__file__)
        root_folder = os.path.abspath(os.path.join(current_folder, ".."))

        # Build complete paths
        tracker_path = os.path.join(root_folder, tracker_env_name)
        service_path = os.path.join(root_folder, service_env_name)

        # Does it Exist ?
        if not os.path.isfile(tracker_path):
            tracker_not_found = True

        # Does it Exist ?
        if not os.path.isfile(service_path):
            service_not_found = True

        if tracker_not_found:
            message.append(
                f"\nEnv file '{tracker_env_name.upper()}' not found in {tracker_path.upper()}",
                style="bold red",
            )

        if service_not_found:
            message.append(
                f"\nEnv file '{service_env_name.upper()}' not found in {service_path.upper()}",
                style="bold red",
            )

        if tracker_not_found or service_not_found:
            raise FileNotFoundError(message)
        else:
            if not cls.process(service_path=service_path, tracker_path=tracker_path):
                console.log("Error found. Please check your config file..Exit", style="bold red")
                sys.exit()

        print()
        return cls(tracker_env_name, service_env_name)
