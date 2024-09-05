# -*- coding: utf-8 -*-

import os
import decouple

from decouple import Config, RepositoryEnv
from rich.text import Text
from common.custom_console import custom_console
from unit3dup.exceptions import BotConfigError, exception_handler
from trackers.trackers import TrackerConfig


class Tracker:
    """
    A class to represent a tracker configuration

    Attributes:
        api_token (str): The API token for the tracker
        base_url (str): The base URL for the tracker
        tracker_values (dict): Additional configuration values for the tracker
    """

    def __init__(self, api_token: str, base_url: str, tracker_values: TrackerConfig):
        self.api_token = api_token
        self.base_url = base_url
        self.tracker_values = tracker_values


class TrackerManager:
    """
    A class to manage multiple trackers

    Attributes:
        message (Text): A message template used for logging
        tracker_name (str): The name of the current tracker
        trackers (dict): A dictionary to store tracker instances

    Methods:
        add_tracker(tracker: Tracker):
            Adds a Tracker instance to the manager
        get_tracker(tracker_name: str) -> Tracker | None:
            Retrieves a Tracker instance by its name
    """

    message = Text("Configuration file ")

    def __init__(self, tracker_name: str):
        self.tracker_name = tracker_name
        self.trackers = {}

    def add_tracker(self, tracker: Tracker):
        """
        Adds a Tracker instance to the TrackerManager

        Args:
            tracker (Tracker): The Tracker instance to add
        """
        self.trackers[self.tracker_name] = tracker

    def get_tracker(self, tracker_name: str) -> Tracker | None:
        """
        Retrieves a Tracker instance by its name

        Args:
            tracker_name (str): The name of the tracker to retrieve

        Returns:
            Tracker: The Tracker instance if found, otherwise logs an error and exits
        """
        tracker = self.trackers.get(tracker_name, None)

        if not tracker:
            self.message.append(
                f"\n Unable to load '{tracker_name}' configuration file",
                style="bold red",
            )
            custom_console.bot_log(self.message)
            exit(1)
        return tracker


class ConfigUnit3D:
    """
    A class to handle the configuration of the Unit3D application

    Attributes:
        BASE_URL (str): The base URL for the API
        API_TOKEN (str): The API token
        tracker_values (dict): Configuration values for trackers
        message (Text): A message template used for logging
        current_folder (str): The current directory of the script
        root_folder (str): The root directory of the project
        TMDB_APIKEY (str): API key for TMDB
        IMGBB_KEY (str): API key for IMGBB
        FREE_IMAGE_KEY (str): API key for Free Image
        QBIT_USER (str): Username for qBittorrent
        QBIT_PASS (str): Password for qBittorrent
        QBIT_URL (str): URL for qBittorrent
        QBIT_PORT (str): Port for qBittorrent
        API_TOKEN (str): API token for the application
        BASE_URL (str): Base URL for the application
        DUPLICATE (str): Duplicate setting
        SCREENSHOTS (int): Number of screenshots
        TORRENT_ARCHIVE (str): Path to the torrent archive
        PREFERRED_LANG (str): Preferred language
        SIZE_TH (int): Size threshold
        JACK_API_KEY (str): API key for Jackett
        JACK_URL (str): URL for Jackett
        COMPRESS_SCSHOT (int): Compression level for screenshots

    Methods:
        service():
            Loads configuration from the `service.env` file and sets instance variables
        validate():
            Validates and loads configuration files for trackers and sets up `TrackerManager` instances
    """

    BASE_URL = None
    API_TOKEN = None
    tracker_values = None
    message = Text("Configuration file ")

    def __init__(self):
        """
        Initializes the configuration with default values
        """
        self.current_folder = os.path.dirname(__file__)
        self.root_folder = os.path.abspath(os.path.join(self.current_folder, ".."))
        self.TMDB_APIKEY: str = ""
        self.IMGBB_KEY: str = ""
        self.FREE_IMAGE_KEY: str = ""
        self.QBIT_USER: str = ""
        self.QBIT_PASS: str = ""
        self.QBIT_URL: str = ""
        self.QBIT_PORT: str = ""
        self.API_TOKEN: str = ""
        self.BASE_URL: str = ""
        self.DUPLICATE: str = ""
        self.SCREENSHOTS = 0
        self.TORRENT_ARCHIVE: str = ""
        self.PREFERRED_LANG: str = ""
        self.SIZE_TH: int = 100
        self.JACK_API_KEY: str = ""
        self.JACK_URL: str = ""
        self.COMPRESS_SCSHOT: int = 6

        self.tracker_values: dict = {}
        self.trackers = None

    @exception_handler
    def service(self):
        """
        Loads configuration from the `service.env` file and sets instance variables

        Reads the `service.env` file to initialize various configuration parameters
        Logs errors and exits if the file is missing or contains invalid values
        """
        service_not_found: bool = False

        current_folder = os.path.dirname(__file__)
        root_folder = os.path.abspath(os.path.join(current_folder, ".."))
        service_path = os.path.join(root_folder, "service.env")

        if not os.path.isfile(service_path):
            service_not_found = True

        if service_not_found:
            self.message.append(
                f"\n'Env' file 'Service.env' not found in {service_path.upper()}",
                style="bold red",
            )

        try:
            config_load_service = Config(RepositoryEnv(service_path))
        except decouple.UndefinedValueError as e:
            custom_console.bot_error_log(f"* service.env * {e}")
            exit(1)
        except FileNotFoundError as e:
            custom_console.bot_error_log(f"* service.env * {e}")
            exit(1)

        self.TMDB_APIKEY = config_load_service("TMDB_APIKEY")
        self.IMGBB_KEY = config_load_service("IMGBB_KEY")
        self.FREE_IMAGE_KEY = config_load_service("FREE_IMAGE_KEY")
        self.QBIT_USER = config_load_service("QBIT_USER")
        self.QBIT_PASS = config_load_service("QBIT_PASS")
        self.QBIT_URL = config_load_service("QBIT_URL")
        self.QBIT_PORT = config_load_service("QBIT_PORT")
        self.JACK_API_KEY = config_load_service("JACK_API_KEY")
        self.TORRENT_ARCHIVE = config_load_service("TORRENT_ARCHIVE")
        self.JACK_URL = config_load_service.get(
            "JACK_URL", default="http://127.0.0.1:9117/"
        )
        self.PREFERRED_LANG = config_load_service.get("PREFERRED_LANG", default="")
        self.SIZE_TH = config_load_service.get("SIZE_TH", default=100)
        self.COMPRESS_SCSHOT = config_load_service.get("COMPRESS_SCSHOT", default=6)
        self.DUPLICATE = config_load_service.get("DUPLICATE_ON", default="false")
        self.SCREENSHOTS = config_load_service.get("NUMBER_OF_SCREENSHOTS", default=6)

        if self.SCREENSHOTS.isdigit():
            self.SCREENSHOTS = min(max(int(self.SCREENSHOTS), 3), 10)
        else:
            raise BotConfigError(
                f"Bad value for 'Number of screenshot' {self.SCREENSHOTS} in {service_path}"
            )

        if self.COMPRESS_SCSHOT.isdigit():
            self.COMPRESS_SCSHOT = min(max(int(self.COMPRESS_SCSHOT), 0), 9)
        else:
            raise BotConfigError(
                f"Bad value for 'Compression level' {self.COMPRESS_SCSHOT} in {service_path}"
            )

        if self.SIZE_TH.isdigit():
            self.SIZE_TH = min(max(int(self.SIZE_TH), 0), 100)
        else:
            raise BotConfigError(
                f"Bad value for 'Size Threshold' {self.SIZE_TH} in {service_path}"
            )

        if self.TORRENT_ARCHIVE:  # TODO
            if not os.path.exists(self.TORRENT_ARCHIVE):
                custom_console.bot_error_log(
                    f"[Service.env] The path {self.TORRENT_ARCHIVE} doesn't exist"
                )
                exit(1)

    def validate(self):
        """
        Validates and loads configuration files for trackers

        Scans for `.env` files, loads their configurations, and sets up `TrackerManager` instances
        Logs errors and exits if configurations are missing or invalid
        """
        env_files = [
            os.path.splitext(file_name)[0].lower()
            for file_name in os.listdir()
            if os.path.isfile(file_name)
               and os.path.splitext(file_name)[1].lower() == ".env"
               and "service.env" not in file_name.lower()
               and "console.env" not in file_name.lower()
        ]

        for tracker_name in env_files:
            tracker_env_name = f"{tracker_name}.env"
            tracker_json_name = f"{tracker_name}.json"

            tracker_env_path = os.path.join(self.root_folder, tracker_env_name)
            tracker_json_path = os.path.join(
                self.root_folder, "trackers", tracker_json_name
            )

            config_load_tracker = Config(RepositoryEnv(tracker_env_path))
            try:
                self.API_TOKEN = config_load_tracker("API_TOKEN")
                self.BASE_URL = config_load_tracker("BASE_URL")
            except decouple.UndefinedValueError as e:
                custom_console.bot_error_log(f"[CONFIG] * {tracker_name}.env * {e}")
                exit(1)

            tracker_values = TrackerConfig(tracker_json_path)

            self.trackers = TrackerManager(tracker_name)
            self.trackers.add_tracker(
                Tracker(
                    api_token=self.API_TOKEN,
                    base_url=self.BASE_URL,
                    tracker_values=tracker_values,
                )
            )


config = ConfigUnit3D()
config.validate()
config.service()
